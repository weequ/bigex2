import socket
import _thread
import sys

OPERATION_TYPE_ATTACK = "A"
OPERATION_TYPE_SEARCH = "S"

def read_port_from_file():
  f = open("port_number", 'r')
  for line in f:
    port = int(line)
    return port#return the first line as int

port = read_port_from_file()

def read_listy_location_from_file():
  f = open("listy_location", 'r')
  for line in f:
    return line.rstrip()+".hpc.cs.helsinki.fi"#return the first line

listy_location = read_listy_location_from_file()

def send_to_listy(msg):
  try:
    s = socket.socket()
    #host = socket.gethostname()
    print("chase_cat.py: trying to send message '"+msg+"' to listy at "+listy_location+":"+str(port));
    s.connect((listy_location, port))
    s.send(bytes(msg, 'UTF-8'))
  except Exception as ex:
    print("chase_cat.py: got exception while trying to connect listy:"+ex)

def get_current_ukko():
  s = socket.socket()
  return socket.gethostname().split(".")[0]

operation_type = sys.argv[1]
cat_name = sys.argv[2]

s = socket.socket()
host = socket.gethostname()
try:
  s.connect((host,port))
  current_ukko = get_current_ukko();
  print("chase_cat.py: Mouse port was open in "+current_ukko);
  if (operation_type == OPERATION_TYPE_ATTACK):
    s.settimeout(6)
    s.send(bytes("MEOW", 'UTF-8'))
    s.settimeout(8)
    buf = s.recv(1024)
    received_msg = buf.decode('UTF-8')
    if (received_msg == "OUCH"):
      print("chase_cat.py: received OUCH from the mouse")
      send_to_listy("G "+current_ukko+" "+cat_name);
  if (operation_type == OPERATION_TYPE_SEARCH):
    send_to_listy("F "+current_ukko+" "+cat_name);
except:
  #Could not find the mouse on this node
  pass
