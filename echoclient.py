# Echo client program
import socket


HOST = '192.168.2.3'   # The remote host
PORT = 8001            # The same port as used by the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Hello, Jack')
    data = s.recv(1024)
print('Received', repr(data))
