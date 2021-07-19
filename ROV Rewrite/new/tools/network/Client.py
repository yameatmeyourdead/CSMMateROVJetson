from queue import Empty
import socket
import threading
from enum import Enum
from multiprocessing import Queue
import time
import random
import pickle
import numpy as np

IP = "127.0.0.1" # connect to DRIVERSTATION
PORT = 7777

EOM = b"<<"
sendQueue = Queue(maxsize=64)

class messageType(Enum):
    command = "0001"
    stop = "1000"
    idle = "0100"
    teleop = "0010"
    auto = "1111"
    controller = "0000"
    data = "1001"
    camera = "0110"

def handleConn(typeOfMessage:str, message):
    typeOfMessage = messageType(typeOfMessage)
    time.sleep(random.random())
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        while True:
            try:
                s.connect((IP,PORT))
            except ConnectionRefusedError:
                # if connection refused (server not online, wait for it to start)
                time.sleep(1)
                continue
            else:
                break
        if(typeOfMessage != messageType.camera):
            # if it is not a camera, it is string
            s.sendall(typeOfMessage.value.encode() + message.encode() + EOM)
        else:
            s.sendall(typeOfMessage.value.encode() + pickle.dumps(message) + EOM)

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
    clientThread.start()

if __name__ == "__main__":
    startClient()
    import cv2
    cam = cv2.VideoCapture(1)
    while True:
        sendQueue.put((messageType.camera.value, cam.read()[1]))