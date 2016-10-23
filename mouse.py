import socket
import _thread
import sys

def clientThread(conn, addr):
  while True:
    buf = conn.recv(1024)
    if not buf:
      break
    received_msg = buf.decode('UTF-8')
    print("mouse.py: received message:"+received_msg)
    if (received_msg == "MEOW"):
      conn.send(bytes("OUCH", 'UTF-8'));
      print("mouse.py: Sent ouch message to attacking cat. Terminating")
      conn.close()
      sys.exit()
    if not buf:
      break
  conn.close()


def read_port_from_file():
  f = open("port_number", 'r')
  for line in f:
    port = int(line)
    return port#return the first line as int
  

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host=socket.gethostname()
port = read_port_from_file()

s.bind((host,port))
print("mouse.py: accepting connections");
s.listen(10)
while True:
  try:
    conn, addr = s.accept()
    print("mouse.py: got new connection");
    _thread.start_new_thread(clientThread, (conn, addr))
  except Exception as ex:
    print("mouse.py : got exception while accepting connections:"+ex)
    break
