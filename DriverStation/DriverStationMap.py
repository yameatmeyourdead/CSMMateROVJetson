import time
import os

# =======================
# =======================
# =======================
# =======================

# LOGGER IMPLEMENTATION

def log(strin, endO="\n"):
    """
    Call this method to log something  \n
    Compatible with all data types capable of conversion to str through str(value)
    """
    strin = '[' + getTimeFormatted(':') + '] ' + str(strin) + endO
    with open(LOGGER_FILE_PATH, 'a') as f:
        f.write(strin)

def getTimeFormatted(delim):
    """
    Get current system time formatted with given delimiter \n
    -> Hour\delim\Min\delim\Sec
    """
    SYSTIME = time.localtime(time.time())
    return (str(SYSTIME.tm_hour) + delim + str(SYSTIME.tm_min) + delim + str(SYSTIME.tm_sec))

# Constructor creates file object named f
currentTime = getTimeFormatted('_')
LOGGER_FILE_PATH = f"DriverStation/Logs/{currentTime}.txt"
if(os.path.exists(LOGGER_FILE_PATH)):
    os.remove(LOGGER_FILE_PATH)
with open("DriverStation/Logs/" + f"{currentTime}" + ".txt", "w") as f:
    f.write(f"[{currentTime}] Logger Created")

# =======================
# =======================
# =======================
# =======================

# NETWORKING
import socket
import _thread
import time
import queue
from multiprocessing import Process

IP = "10.0.0.1" # My IP
CLIENT = "10.0.0.2" # IP of Jetson
# use different ports to ensure they are always available for binding
SENDPORT = 6666
RECVPORT = 6667

# queues to handle different data (allows for communication between processes and threads)
errQueue = queue.Queue()
dataQueue = queue.Queue()

sendQueue = queue.Queue()

def server(host, port):
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
    # close connection
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
    while True:
        try:
            data = sendQueue.get(block=False)
            doClientConnection(data)
        except queue.Empty:
            pass

def doClientConnection(data, host, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    time.sleep(0.1) # wait for server to start listening for clients
    client.connect((host, port))
    time.sleep(0.1) # wait for thread to display connection
    # send all data
    client.sendall(data.encode() + b"<")
    # close connection
    client.shutdown(socket.SHUT_WR)
    client.close()

def startDriverStationNetworking():
    _thread.start_new_thread(server, ("", RECVPORT))
    client(CLIENT, SENDPORT) 

DriverStationNetworking = Process(target=startDriverStationNetworking)

if __name__ == "__main__":
    DriverStationNetworking.start()
    input()
    DriverStationNetworking.kill()