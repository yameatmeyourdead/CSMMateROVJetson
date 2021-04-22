import socket
import json
import time

HOST, PORT = "localhost", 7777

jsonObj = json.dumps(([0, 0, 0, 0])).encode() + b'\n'



data = jsonObj

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    start = time.time()
    while (time.time() - start < 100000):
        sock.sendall(jsonObj)
finally:
    sock.close()

print("Sent:     {}".format(data))