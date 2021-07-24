from abc import ABC, abstractmethod
from typing import Any, List
from queue import Empty
import socket
import threading
from enum import Enum
from multiprocessing import Queue
import time
import random
from tools.network.messageType import messageType

IP = "10.0.0.2" # connect to JETSON
PORT = 7777

EOM = b"<<"
sendQueue = Queue()

encoders: List["messageEncoder"] = []

class messageEncoder(ABC):
    def __init__(self) -> None:
        encoders[messageType.data] = self
    @abstractmethod
    def encode(obj: Any) -> bytes:
        """Encode this data type to bytes, by default returns obj.encode()"""
        return obj.encode()

def handleConn(typeOfMessage:messageType, message:str):
    time.sleep(random.random())
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((IP,PORT))
        s.sendall(typeOfMessage.value.encode() + encoders[typeOfMessage].encode(message) + EOM)
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
    clientThread.setDaemon(True)
    clientThread.start()