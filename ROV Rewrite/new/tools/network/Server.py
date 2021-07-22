from enum import Enum
from abc import ABC, abstractmethod
import socket
from tools.network.messageType import messageType
import threading
import numpy as np
import json

IP = "0.0.0.0" # listen to all ips
PORT = 7777

EOM = b"<<"

class messageDecoder(ABC):
    @abstractmethod
    def decode(obj):
        return ""

class imageDecoder(messageDecoder):
    def decode(metaData:str, array:bytes) -> np.ndarray:
        metaData = json.loads(metaData)
        return np.ndarray(metaData["shape"], dtype=metaData["dtype"], buffer=array)

def handleConn(connectionInformation):
    conn:socket.socket = connectionInformation[0]
    addr = connectionInformation[1]
    print('Connected by', addr)
    data = None
    while True:
        # ensure all data is received
        data = conn.recv(1024)
        if EOM not in data:
            continue
        # remove EOM
        header = data[0:4]
        data = data[4:-len(EOM)]
        print("header: " + header.decode() + " data: " + data.decode())
        break
def server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((IP,PORT))
        s.listen()
        while True:
            threading.Thread(target=handleConn, args=(s.accept(),)).start()

def startServer():
    global serverThread
    serverThread = threading.Thread(target=server)
    serverThread.setName("serverThread")
    serverThread.start()
