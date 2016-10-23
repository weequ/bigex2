import time
import sys
import subprocess

line_count = -1;


all_nodes = set()
searched_nodes = set()
exploring_cats = set()

OPERATION_TYPE_ATTACK = "A"
OPERATION_TYPE_SEARCH = "S"
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
  #process = subprocess.Popen("ssh "+ukkonode+".hpc.cs.helsinki.fi python3 chase_cat.py "+operation_type+" "+cat_name, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  #output,stderr = process.communicate()
  #status = process.poll()
  #print(output.decode("UTF-8"))

def wait_new_line_in_cmsg_file():
  global line_count
  while True:
    with open("cmsg", 'r') as f:
      current_line = 0
      for line in f:
        current_line = current_line+1
        if (line_count < current_line):
          line_count = current_line
          print("new line detected")
          return line.rstrip()
      time.sleep(0.1)


print("ok")

read_ukkonodes_file()
read_cmsg_file()
unsearched_nodes = all_nodes - searched_nodes

count = 0

while len(unsearched_nodes) > 0 and count < 10:
  count = count+1
  print(unsearched_nodes)
  #Try to explore with both cats
  if (CAT_NAME_CATTY not in exploring_cats):
    node_to_search = unsearched_nodes.pop()
    start_chase_cat(node_to_search, OPERATION_TYPE_SEARCH, CAT_NAME_CATTY)
  if (len(unsearched_nodes) > 0 and CAT_NAME_JAZZY not in exploring_cats):
    node_to_search = unsearched_nodes.pop()
    start_chase_cat(node_to_search, OPERATION_TYPE_SEARCH, CAT_NAME_JAZZY)

  #new_line = wait_new_line_in_cmsg_file()
  #read_cmsg_file()
  #unsearched_nodes = all_nodes-searched_nodes
  
