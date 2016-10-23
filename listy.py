import socket
import sys
import _thread

def read_port_from_file():
  with open("port_number", 'r') as f:
    for line in f:
      port = int(line)
      return port;

def append_to_cmsg_file(msg):
  with open("cmsg", 'a+') as f:
    f.write(msg)

#Clears the contents of the cmsg file. Creates a new one if it does not exist.
def clear_cmsg_file():
  with open("cmsg", 'w+') as f:
    print("listy.py: cmsg cleared")


def client_reader_thread(conn, addr):
  while True:
    buf = conn.recv(1024)
    if not buf:
      break
    received_msg = buf.decode('UTF-8')
    append_to_cmsg_file(received_msg+"\n")
  conn.close();

clear_cmsg_file()
port = read_port_from_file()
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host=socket.gethostname()
s.bind((host,port))
s.listen(10)

while True:
  try:
    conn, addr = s.accept()
    _thread.start_new_thread(client_reader_thread, (conn, addr))
  except Exception as ex:
    print("listy_py: got exception: "+ex)
  
