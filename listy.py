import socket
import _thread

def read_port_from_file():
  with open("port_number", 'r') as f:
    for line in f:
      port = int(line)
      return port;

def append_to_cmsg_file(msg):
  with open("cmsg", 'a') as f:
     f.write(msg)#+\n


def client_reader_thread(conn, addr):
  while True:
    buf = conn.recv(1024)
    if not buf:
      break
    received_msg = buf.decode('UTF-8')
    append_to_csmg_file(received_msg)
  conn.close();


port = read_port_from_file()
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host=socket.gethostname()
s.bind((host,port))
s.listen(10)

while True:
  try:
    conn, addr = s.accept()
    _thread.start_new_thread(clientReaderThread, (conn, addr))
  except Exception as ex:
    print(ex)
  
