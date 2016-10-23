import time
import sys
import subprocess

line_count = -1;


all_nodes = set()
searched_nodes = set()

OPERATION_TYPE_ATTACK = "A"
OPERATION_TYPE_SEARCH = "S"

RESULT_TYPE_FOUND = "F"
RESULT_TYPE_GOT = "G"

CAT_NAME_JAZZY = "Jazzy"
CAT_NAME_CATTY = "Catty"

def read_ukkonodes_file():
  all_nodes.clear()
  with open("ukkonodes", 'r') as f:
    for line in f:
      all_nodes.add(line.rstrip())



def read_cmsg_file():
  searched_nodes.clear()
  with open("cmsg", 'r') as f:
    for line in f:
      lineparts = line.split()
      operation_type = lineparts[0]
      ukkonode = lineparts[1]
      cat_name = lineparts[2]
      if (operation_type == OPERATION_TYPE_SEARCH):
        searched_nodes.add(ukkonode)

def start_chase_cat(ukkonode, operation_type, cat_name):
  subprocess.Popen("ssh "+ukkonode+".hpc.cs.helsinki.fi python3 chase_cat.py "+operation_type+" "+cat_name, shell=True)
  print("cat "+cat_name+" exploring node "+ukkonode)

def get_new_line_in_cmsg_file():
  global line_count
  with open("cmsg", 'r') as f:
    current_line = 0
    for line in f:
      current_line = current_line+1
      if (line_count < current_line):
        line_count = current_line
        print("new line detected")
        return line.rstrip()
  return false


read_ukkonodes_file()
#read_cmsg_file()
unsearched_nodes = all_nodes - searched_nodes

line = False
while (not line):
  node_to_search = unsearched_nodes.pop()
  start_chase_cat(node_to_search, OPERATION_TYPE_SEARCH, CAT_NAME_CATTY)
  if (len(unsearched_nodes) > 0):
    node_to_search = unsearched_nodes.pop()
    start_chase_cat(node_to_search, OPERATION_TYPE_SEARCH, CAT_NAME_JAZZY)
  time.sleep(12)
  line = get_new_line_in_cmsg_file()
  if (not line and len(unsearched_nodes) <= 0):
    print("all nodes explored but cat was not found")
    sys.exit()#All nodes have been visited without fiding the mouse

lineparts = line.split()
result_type = lineparts[0]
ukkonode = lineparts[1]
catname = lineparts[2]
if (result_type != RESULT_TYPE_FOUND):
  print("error1")
  sys.exit()#first result type should be F (FOUND) but it wasn't
print(catname+" has found the mouse in "+ukkonode);

if (catname == CAT_NAME_JAZZY):
  start_chase_cat(ukkonode, OPERATION_TYPE_SEARCH, CAT_NAME_CATTY)

if (catname == CAT_NAME_CATTY): 
  start_chase_cat(ukkonode, OPERATION_TYPE_SEARCH, CAT_NAME_JAZZY)

time.sleep(12)
line = get_new_line_in_cmsg_file()
lineparts = line.split()
result_type = lineparts[0]
ukkonode = lineparts[1]
catname = lineparts[2]
if (result_type != RESULT_TYPE_FOUND):
  print("error2")
  sys.exit()#second result type should be F (FOUND) but it wasn't
start_chase_cat(ukkonode, OPERATION_TYPE_ATTACK, CAT_NAME_JAZZY)

time.sleep(6)
line = get_new_line_in_cmsg_file()
lineparts = line.split()
result_type = lineparts[0]
ukkonode = lineparts[1]
catname = lineparts[2]
if (result_type != RESULT_TYPE_ATTACK):
  print("error3")
  sys.exit()#third result type should be G (GOT) but it wasn't
print("got the cat!")
