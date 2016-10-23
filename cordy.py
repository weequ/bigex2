import time
import sys
import subprocess

line_count = -1;

unsearched_nodes = set()

OPERATION_TYPE_ATTACK = "A"
OPERATION_TYPE_SEARCH = "S"

RESULT_TYPE_FOUND = "F"
RESULT_TYPE_GOT = "G"

CAT_NAME_JAZZY = "Jazzy"
CAT_NAME_CATTY = "Catty"

def read_ukkonodes_file():
  unsearched_nodes.clear()
  with open("ukkonodes", 'r') as f:
    for line in f:
      unsearched_nodes.add(line.rstrip())

def start_chase_cat(ukkonode, operation_type, cat_name):
  print("cordy.py: calling 'chase_cat.py "+operation_type+" "+cat_name+"' at "+ukkonode)
  subprocess.Popen("ssh "+ukkonode+".hpc.cs.helsinki.fi python3 chase_cat.py "+operation_type+" "+cat_name, shell=True)


class CmsgLine:
  result_type = ""
  ukkonode = ""
  catname = ""


def get_new_line_in_cmsg_file():
  global line_count
  with open("cmsg", 'r') as f:
    current_line = 0
    for line in f:
      current_line = current_line+1
      if (line_count < current_line):
        line_count = current_line
        lineparts = line.rstrip().split()
        result = CmsgLine()
        result.result_type = lineparts[0]
        result.ukkonode = lineparts[1]
        result.catname = lineparts[2]
        return result
  return False#No new line found


read_ukkonodes_file()

#Exploring the nodes start:
first_line = False
while (not first_line):
  node_to_search = unsearched_nodes.pop()
  start_chase_cat(node_to_search, OPERATION_TYPE_SEARCH, CAT_NAME_CATTY)
  if (len(unsearched_nodes) > 0):
    node_to_search = unsearched_nodes.pop()
    start_chase_cat(node_to_search, OPERATION_TYPE_SEARCH, CAT_NAME_JAZZY)
  time.sleep(12)
  first_line = get_new_line_in_cmsg_file()
  if (not first_line and len(unsearched_nodes) <= 0):
    print("cordy.py: all nodes have been explored but mouse was not found")
    sys.exit()#All nodes have been visited without fiding the mouse
#Exploring the nodes end.

if (first_line.result_type != RESULT_TYPE_FOUND):
  print("cordy.py: first result type in cmsg should be F (FOUND), but it wasn't")
  sys.exit()#first result type should be F (FOUND) but it wasn't

#Search the mouse with the other cat:
if (first_line.catname == CAT_NAME_JAZZY):
  start_chase_cat(first_line.ukkonode, OPERATION_TYPE_SEARCH, CAT_NAME_CATTY)
if (first_line.catname == CAT_NAME_CATTY): 
  start_chase_cat(first_line.ukkonode, OPERATION_TYPE_SEARCH, CAT_NAME_JAZZY)
time.sleep(12)

second_line = get_new_line_in_cmsg_file()
if (second_line.result_type != RESULT_TYPE_FOUND):
  print("cordy.py: second result type in cmsg should be F (FOUND), but it wasn't")
  sys.exit()#second result type should be F (FOUND) but it wasn't

#Attack the mouse with one of the cats (always with Jazzy)
start_chase_cat(second_line.ukkonode, OPERATION_TYPE_ATTACK, CAT_NAME_JAZZY)

time.sleep(14)#14 comes from 6+8 (time it takes for cat to attack + time the cat waits for MEOW)
third_line = get_new_line_in_cmsg_file()
if (third_line.result_type != RESULT_TYPE_GOT):
  print("cordy.py: third result type in cmsg should be G (GOT), but it wasn't")
  sys.exit()#third result type should be G (GOT) but it wasn't
print("cordy.py: Got the cat! Terminating.")
