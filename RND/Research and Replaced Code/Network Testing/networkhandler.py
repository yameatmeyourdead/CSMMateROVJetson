import socket
import queue
import time
from typing import ByteString
from multiprocessing import Process

class EStopInterruptFatal(Exception): ...
class EStopInterrupt(Exception): ...


IP = "127.0.0.1"
PORT = 7777

sendQueue = queue.Queue()
recvQueue = queue.Queue()
errQueue = queue.Queue()

def sendPacket(data):
    """
    Writes data to socket
    """
    if data is not None:
        if (not isinstance(data, ByteString)): # if data is not a bytestring, make it so
            data = data.encode()
        print(f"Attempt send {data}")
        SOC.sendall(data) # send bytestring

# TODO: Implement support for numpy ndarray
def doNetworkHandler():
    sendQueue.put("000cium<".encode())
    SOC.connect((IP, PORT))
    SOC.settimeout(2)
    closer = "<"
    buffer = b""
    while True:
        try:
            item = sendQueue.get(block=False) # if queue has item, send it. throws queue.Empty error if empty
            if item is not None:
                sendPacket(item) 
        except queue.Empty:
            pass
        try:
            buffer = SOC.recv(1024) # wait for incoming messages for max .1 seconds
        except socket.timeout:
            pass
        if(buffer): # if incoming message detected, finish gathering message
            while not closer in buffer:
                try:
                    buffer += SOC.recv(1024)
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
                errQueue.put(EStopInterruptFatal())
            elif header == b"010":
                errQueue.put(EStopInterrupt())
            elif header == b"000":
                print(rval)
                recvQueue.put(rval.decode()) # add message to the recv queue
            
SOC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
NetworkingProcess = Process(target=doNetworkHandler)

if __name__ == "__main__":
    NetworkingProcess.start()
    
    time.sleep(2)
    print(recvQueue.get(block=True))