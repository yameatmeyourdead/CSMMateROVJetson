from abc import ABC, abstractmethod
from queue import Empty
from typing import Any, List
from tools import Logger
import socket
import threading
from tools.network.messageType import messageType
from multiprocessing import Queue
import json
import time
import numpy as np

IP = "127.0.0.1" # connect to DRIVERSTATION
PORT = 7777

EOM = b"<<"
sendQueue = Queue(maxsize=64)

class messageEncoder(ABC):
    @abstractmethod
    def encode(obj: Any) -> bytes:
        """Encode this data type to bytes, by default returns obj.encode()"""
        return messageType.message.value.encode() + obj.encode() + EOM

class imageEncoder(messageEncoder):
    def encode(camIdent:int, img:np.ndarray) -> bytes:
        assert (camIdent is not None and img is not None)
        return messageType.camera.value.encode() + (json.dumps(dict(dtype=str(img.dtype), shape=img.shape, size=img.size, cam=camIdent)).encode("utf-8") + EOM + img.tobytes() + EOM)


def handleConn(typeOfMessage: messageType, data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        attemptedConnections = 0
        while True:
            try:
                s.connect((IP,PORT))
            except ConnectionRefusedError:
                # if connection refused (server not online, wait for it to start) timeout = 3 sec (NOTE: if experiencing memory/CPU intensive ops this is very memory intensive (1 thread per frame of camera :^)) )
                attemptedConnections += 1
                if(attemptedConnections >= 3):
                    Logger.log(f"Connection to {(IP, PORT)} refused. Is the server online?")
                    return
                time.sleep(1)
                continue
            else:
                break
        if(typeOfMessage != messageType.camera):
            # if it is not a camera, use default message encoder
            s.sendall(messageEncoder.encode(data))
        else:
            s.sendall(imageEncoder.encode(data[0], data[1]))

def client():
    while True:
        try:
            dataToSend = sendQueue.get_nowait()
        except Empty:
            continue
        else:
            threading.Thread(target=handleConn, args=(dataToSend[0], dataToSend[1])).start()

def startClient():
    global clientThread
    clientThread = threading.Thread(target=client)
    clientThread.setName("clientThread")
    clientThread.setDaemon(True)
    clientThread.start()

if __name__ == "__main__":
    startClient()
    import cv2
    cam = cv2.VideoCapture(1)
    cameraIdent = 0
    while True:
        sendQueue.put((messageType.camera.value, (cameraIdent, cam.read()[1])))