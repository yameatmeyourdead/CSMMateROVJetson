from queue import Empty
import socket
import threading
from enum import Enum
from multiprocessing import Queue
import time
import random

IP = "10.0.0.2" # connect to JETSON
PORT = 7777

EOM = b"<<"
sendQueue = Queue()

class messageType(Enum):
    command = "0001"
    stop = "1000"
    idle = "0100"
    teleop = "0010"
    auto = "1111"
    controller = "0000"
    data = "1001"
    camera = "0110"

def handleConn(typeOfMessage:messageType, message:str):
    time.sleep(random.random())
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((IP,PORT))
        s.sendall(typeOfMessage.value.encode() + message.encode() + EOM)
        data = s.recv(1024)
    print(repr(data))

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