from multiprocessing.queues import Queue
from queue import Empty
from tools.IllegalStateException import IllegalStateException
import threading
import socket
from typing import Any, Dict, List, Tuple
from tools import Logger
try:
    import evdev
except ModuleNotFoundError:
    print("This code only works on linux machines with evdev installed.....Exiting this program")
    exit()
import json
import time
from traceback import format_exc

serverThread: threading.Thread = None
controllerThread: threading.Thread = None
recvQueue = Queue()

# Constants
JETSONIP = "10.0.0.2"
JETSONRECVPORT = 7778 # general data port
CONTROLLERPORT = 7776 # controller specific data

def handleConnection(conn: Tuple[socket.socket, str], queue: Queue):
    """Handles data receiving and putting in queue"""
    try:
        recvQueue.put(recvall(conn[0]))
    except:
        Logger.logError(format_exc()[0:-1])

def recvall(conn) -> str:
    """Receive all data from socket and return it as string"""
    buffer = b""
    while "<EOD>" not in buffer:
        try:
            buffer += conn.recv(1024)
        except socket.timeout:
            pass
    try:
        toReturn = buffer[:buffer.index("<EOD>")]
    except ValueError:
        raise IllegalStateException("Data received was \"\". Did client forcibly close connection before <EOD> was received?")
    finally:
        return toReturn.decode()

def doServer(conn: Tuple[socket.socket, str], queue: Queue):
    if(serverThread is None):
        raise IllegalStateException("ServerThread has not been created. Ensure startServer() has been called.")
    
    # monitor socket for incoming connections
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((JETSONIP, JETSONRECVPORT))
    server.listen(5)
    while True:
        # start independent thread for each connection
        threading.Thread(target=handleConnection, args=(server.accept(), recvQueue)).start()

def doController():
    # defines an Xbox One Controller (make this dynamic so that we can plug in any type of input device and get approxeng.input to like it)
    VENDOR = 1118
    PRODUCT = 746
    VERSION = 769
    # create new socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((JETSONIP, CONTROLLERPORT)) # bind our socket to our port
        # outside loop to enable restarting the server
        while True:
            Logger.log("Listening for connections")
            s.listen() # wait for connection
            conn, addr = s.accept() # once connection available, accept it (THIS IS BLOCKING)
            try:
                with conn:
                    Logger.log("Connected to", addr) # log who we are connected with
                    data = b""
                    while not data:
                        data += conn.recv(2048)
                        # if message suffix not found, keep polling the socket
                        if(b"<" not in data):
                            continue
                    data = data.decode().split('\n')
                    devices_json = json.loads(data[0][0:-1])

                    # if controller event was captured in packet, add it to event queue to be processed
                    events = Queue()
                    if(len(data) > 1):
                        for i in range(1, len(data)):
                            events.put(data[i])
                    
                    # once we start getting data, get the first thing sent (our controller information)
                    devices = []
                    for device_json in devices_json:
                        capabilities = {}
                        for k, v in device_json['capabilities'].items():
                            capabilities[int(k)] = [x if not isinstance(x, list) else (x[0], evdev.AbsInfo(**x[1])) for x in v]
                        devices.append(evdev.UInput(capabilities, name=device_json['name'], vendor=VENDOR, product=PRODUCT, version=VERSION))
                        Logger.log("Controller Device Created")

                    data = b""
                    # while we are connected read controller data (and try not to miss any events)
                    while True:
                        # poll the socket
                        start = int(time.time())
                        while not data: # if socket was empty, keep trying
                            data += conn.recv(2048)
                            if(b"<" not in data): # wait until EOM character
                                if(int(time.time()) - start >= 600): # 600 second timeout for controller server
                                    raise ConnectionResetError
                                continue
                        # split by line
                        data = data.decode().split('\n')
                        data[-1].replace('<','') # trash EOM character
                        
                        # parse each received event into list of strings
                        for event in data:
                            if(event == ''):
                                continue
                            events.put(json.loads(event.replace('\n',''))) # get rid of nasty \n characters if they exist

                        # apply pending events
                        try:
                            while True:
                                event = events.get_nowait()
                                devices[int(event[0])].write(int(event[1]), int(event[2]), int(event[3]))
                        except Empty:
                            pass
                        data = b""
            # connection was reset from other side (or maybe your network dropped)
            except ConnectionResetError:
                Logger.log("Connection with", addr, " forcibly closed")
                continue
            except:
                Logger.log(f"Caught unexpected error: " + format_exc()[0:-1])
            finally:
                # destroy controller object(s)
                for device in devices:
                    Logger.log(f"Closing device {device}")
                    device.close()

def startServer():
    global serverThread
    serverThread = threading.Thread(target=doServer, args=(recvQueue,))
    serverThread.setName("ServerThread")
    serverThread.start()

    global controllerThread
    controllerThread = threading.Thread(target=doController)
    controllerThread.setName("ControllerThread")
    controllerThread.start()