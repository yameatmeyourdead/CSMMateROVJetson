from multiprocessing.queues import Queue
from queue import Empty
from tools.IllegalStateException import IllegalStateException
import threading
import socket
from typing import Any, Tuple
from tools import Logger

ClientThread = None
sendQueue = Queue()

DRIVERSTATIONIP = "10.0.0.1"
DRIVERSTATIONPORT = 7777

def handleConnection(connectionInformation: Tuple[str, Any], data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # create new TCP socket
        s.connect((connectionInformation[0], str(connectionInformation[1]))) # Port may be passed as integer, ensure correct type
        s.sendall(data + '<EOD>') # send all data suffixed with marker for end of data packet

def doClient(connectionInformation: Tuple[str, Any], queue : Queue):
    """Handles sending data to DriverStation"""
    # None protection
    if(ClientThread is None):
        raise IllegalStateException("ClientThread has not been created. Ensure startClient() has been called.")
    
    # montior sendQueue for instances of data
    data = None
    while(data is None):
        # get data from sendQueue (if available). if available, send the data. Always set data to None
        try:
            data = queue.get_nowait()
        except Empty:
            continue
        else:
            # allows for multiple client handler threads
            threading.Thread(target=handleConnection, args=(connectionInformation, data)).start()
        finally:
            data = None

def startClient():
    """Creates client thread, names it appropriately, and starts monitoring sendQueue"""
    global ClientThread
    ClientThread = threading.Thread(target=doClient, args=((DRIVERSTATIONIP, DRIVERSTATIONPORT), sendQueue))
    ClientThread.setName("ClientThread")
    ClientThread.start()