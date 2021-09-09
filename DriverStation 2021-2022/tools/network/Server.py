import time
from abc import ABC, abstractstaticmethod
from enum import Enum
import socket
import threading
from traceback import print_exc
from typing import Any, Dict, Tuple
import cv2
import numpy as np
import json
from gui import GUI
from tools import Logger
from tools.network.messageType import messageType

IP = "0.0.0.0" # listen to all ips
PORT = 7777

EOM = b"<<"

class messageDecoder(ABC):
    @abstractstaticmethod
    def decode(obj:Any) -> Any:
        return obj.decode()

class imageDecoder(messageDecoder):
    @staticmethod
    def decode(metaData:Dict[str, Any], img:bytes) -> Tuple[int, np.ndarray]:
        return (metaData["cam"], np.ndarray(metaData["shape"], dtype=metaData["dtype"], buffer=img))

def handleConn(connectionInformation):
    conn:socket.socket = connectionInformation[0]
    addr = connectionInformation[1]
    # print('Connected by', addr)
    # ensure all data is received
    try:
        header = messageType(conn.recv(4).decode())
    except: # if invalid header is received, ignore the packet
        return
    if(header == messageType.camera):
        try:
            data = b""
            while EOM not in data:
                data += conn.recv(4096)
                split = data.index(EOM)
            metaData = json.loads(data[:split])
            data = data[split+len(EOM):]
            while len(data) < metaData["size"]:
                data += conn.recv(4096)
            # construct image
            GUI.cameraBuffer.put_nowait(imageDecoder.decode(metaData, data))
        except: # if any error occurs, return without updating cams
            Logger.logError(print_exc())
            return
    else:
        data = conn.recv(4096)
        while EOM not in data:
            data += conn.recv(4096)
        # decode data
        data = data.decode()[0:-len(EOM)]
        split = data.index(":")
        GUI.varData[data[0:split]] = data[split+1:]

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
    serverThread.setDaemon(True)
    serverThread.start()

if __name__ == "__main__":
    startServer()
    while True:
        time.sleep(1)