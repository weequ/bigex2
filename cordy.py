import time
import sys
import subprocess

line_count = -1;

OPERATION_TYPE_ATTACK = "A"
OPERATION_TYPE_SEARCH = "S"

def start_chase_cat(ukkonode, operation_type, cat_name):
  process = subprocess.Popen("ssh "+ukkonode+".hpc.cs.helsinki.fi python3 chase_cat.py "+operation_type+" "+cat_name, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  output,stderr = process.communicate()
  status = process.poll()
  print(output.decode("UTF-8"))

print("ok")
start_chase_cat("ukko163", "S", "Catty")#Jazzy
sys.exit(0)

while True:
  with open("cmsg", 'r') as f:
    current_line = 0
    for line in f:
      current_line = current_line+1
      if (line_count < current_line):
        line_count = current_line
        print("new line detected")
    time.sleep(1)
