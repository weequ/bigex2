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
    return line+".hpc.cs.helsinki.fi"#return the first line

listy_location = read_listy_location_from_file()

def send_to_listy(msg):
  s = socket.socket()
  #host = socket.gethostname()
  print("trying to connect to listy at "+listy_location+":"+str(port));
  s.connect((listy_location, port))
  s.send(bytes(msg, 'UTF-8'))


operation_type = sys.argv[1]
if (operation_type == OPERATION_TYPE_SEARCH):
  print("Search");
if (operation_type == OPERATION_TYPE_ATTACK):
  print("Attack");

cat_name = sys.argv[2]


s = socket.socket()
host = socket.gethostname()
try:
  s.connect((host,port))
  print("Mouse port was open");
  if (operation_type == OPERATION_TYPE_ATTACK):
    s.send(bytes("MEOW", 'UTF-8'))
    buf = s.recv(1024);
    received_msg = buf.decode('UTF-8')
    if (received_msg == "OUCH"):
      send_to_listy("G ukkoXXX "+cat_name);
  if (operation_type == OPERATION_TYPE_SEARCH):
    send_to_listy("F ukkoXXX "+cat_name);
except Exception as ex:
  print("mouse not found")
  print(ex)
