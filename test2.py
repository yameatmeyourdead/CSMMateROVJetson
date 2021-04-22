import socket
import json

HOST, PORT = "localhost", 7777

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen()
conn, addr = sock.accept()
while True:
    data = conn.recv(1024)
    if not data:
        continue
    data = data.decode().split('\n')[-2]
    # print(data)
    print(type(list(data)))