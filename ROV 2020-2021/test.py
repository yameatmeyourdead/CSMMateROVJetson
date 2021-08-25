import socket
import _thread
import time
import queue
from multiprocessing import Process

IP = "10.0.0.2" # Jetson IP
CLIENT = "10.0.0.1" # IP of Driver Station
# use different ports to ensure they are always available for binding
SENDPORT = 6667
RECVPORT = 6666

# queues to handle different data (allows for communication between processes and threads)
errQueue = queue.Queue()
dataQueue = queue.Queue()

sendQueue = queue.Queue()

def server(host, port):
    print("starting server")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host,port))
    server.listen(5)
    while True:
        _thread.start_new_thread(handle_connection, server.accept())

def handle_connection(client, address):
    """Data MUST be structured like this  
    000< for EStopInterrupt
    001< for Interrupt
    010(data)< for all other data"""
    print("incoming connection")
    client.settimeout(0.1)
    data = recvall(client)
    data = data.decode()
    if(data == ""): # error check
        client.shutdown(socket.SHUT_RD)
        client.close()
        return
    tod = data[0:3] # type of data header
    if(tod == "000"):
        errQueue.put("InterruptFatal")
    elif(tod == "001"):
        errQueue.put("Interrupt")
    elif(tod == "010"):
        dataQueue.put(data[4:])
    client.shutdown(socket.SHUT_RD)
    client.close()

def recvall(connection):
    """Receive all data from socket and return it as bytestring"""
    buffer = b""
    while "<" not in buffer:
        try:
            buffer += connection.recv(1024)
        except socket.timeout:
            pass
    try:
        toReturn = buffer[:buffer.index('<')]
    except ValueError:
        toReturn = b""
    finally:
        return toReturn

def client(host, port):
    """If item exists in sendQueue, it will get sent"""
    print("starting client")
    while True:
        try:
            time.sleep(.001)
            data = sendQueue.get(block=False)
        except queue.Empty:
            continue
        else:
            doClientConnection(data)

def doClientConnection(data, host, port):
    print("do client connection")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        time.sleep(0.1) # wait for server to start listening for clients
        s.connect((host, port))
        time.sleep(0.1) # wait for thread to display connection
        # send all data
        s.sendall(data.encode() + b"<")
    print("did")

def startJetsonNetworking():
    _thread.start_new_thread(server, ("", RECVPORT))
    client(CLIENT, SENDPORT)

JetsonNetworking = Process(target=startJetsonNetworking) # two threaded process (one child)

if __name__ == "__main__":
    JetsonNetworking.start()