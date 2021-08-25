import socket
import queue
from typing import ByteString

IP = "127.0.0.1"
PORT = 7777

SOC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SOC.bind((IP, PORT))
SOC.listen()
conn, addr = SOC.accept()


closer = "<"
buffer = b""
while True:
    try:
        buffer = conn.recv(1024) # wait for incoming messages for max .1 seconds
    except socket.timeout:
        pass
    if(buffer): # if incoming message detected, finish gathering message
        while not closer in buffer:
            try:
                buffer += conn.recv(1024)
            except socket.timeout:
                pass
        # extract the message
        header = buffer[0:4]
        pos = buffer.find(closer)
        rval = buffer[:pos + len(closer)]
        buffer = buffer[pos + len(closer):]
        # classify messages based on header
        # 100 = Fatal interrupt
        # 010 = Interrupt
        # 000 = Message
        if header == b"100":
            pass
        elif header == b"010":
            pass
        elif header == b"000":
            print(rval.decode()) # add message to the recv queue