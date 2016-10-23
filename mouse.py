import socket
import _thread

def clientThread(conn, addr):
  while True:
    buf = conn.recv(1024)
    if not buf:
      break
    received_msg = buf.decode('UTF-8')
    print(received_msg)
    if (received_msg == "MEOW"):
      conn.send(bytes("OUCH", 'UTF-8'));
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
print("listening connections");
s.listen(10)
while True:
  try:
    conn, addr = s.accept()
    print("new connection");
    _thread.start_new_thread(clientThread, (conn, addr))
  except:
    break
