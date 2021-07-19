import time
from enum import Enum
import socket
import threading
import numpy as np
import pickle
import struct
from gui import GUI

IP = "0.0.0.0" # listen to all ips
PORT = 7777

EOM = b"<<"

class messageType(Enum):
    command = "0001"
    stop = "1000"
    idle = "0100"
    teleop = "0010"
    auto = "1111"
    controller = "0000"
    data = "1001"
    camera = "0110"

payloadsize = struct.calcsize("L")

def handleConn(connectionInformation):
    conn:socket.socket = connectionInformation[0]
    addr = connectionInformation[1]
    print('Connected by', addr)
    # ensure all data is received
    header = messageType(conn.recv(4).decode())
    if(header == messageType.data):
        data = b""
        while len(data) < payloadsize:
            data += conn.recv(4096)
            
    else:
        data = conn.recv(4096)
        while EOM not in data:
            data += conn.recv(4096)
    # decode data
    if(header == messageType.data):
        data = data.decode()[0:-len(EOM)]
        split = data.index(":")
        GUI.varData[data[0:split]] = data[split+1:]
    elif(header == messageType.camera):
        GUI.cameraBuffer.put((0, pickle.loads(data)))

def server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((IP,PORT))
        s.listen()
        while True:
            threading.Thread(target=handleConn, args=(s.accept(),)).start()

def startServer():
    global serverThread
    serverThread = threading.Thread(target=server)
    serverThread.setName("clientThread")
    serverThread.start()

if __name__ == "__main__":
    startServer()
    while True:
        time.sleep(1)