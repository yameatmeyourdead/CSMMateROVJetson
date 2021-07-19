from enum import Enum
import socket
import pickle
import threading

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
        conn.sendall(b"header: " + header + b" data: " + data)
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
    serverThread.setName("clientThread")
    serverThread.start()
