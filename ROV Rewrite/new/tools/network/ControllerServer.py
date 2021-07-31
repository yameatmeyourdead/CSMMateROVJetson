# Original methods written by yingtongli under GNU Affero General Public License © 2019
# Source code here -> https://yingtongli.me/git/input-over-ssh
# Modified by Zac Stanton
# Note: this no longer does input over ssh, but rather input over a scuffed implementation of TCP

from json.decoder import JSONDecodeError
import socket
import threading
from traceback import format_exc
from typing import List
try:
    import evdev
except ModuleNotFoundError:
    print("This code only works on linux machines with evdev installed.....Exiting this program")
    exit()
import json
import time
from tools import Logger

# Data for Xbox One Controller
# VENDOR = 1118
# PRODUCT = 746
# VERSION = 769

HOST = "10.0.0.2" # jetson's static ip address
PORT = 7777 # port to listen to
EOM = b"<<"
EOM_DECODE = EOM.decode()

def doServer():
    # create new socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT)) # bind our socket to our port
        s.listen() # listen for connections
        # outside loop to enable restarting the server
        while True:
            conn, addr = s.accept() # once connection available, accept it (THIS IS BLOCKING)
            try:
                with conn:
                    # Start by getting controller information json (first packet received)
                    # print("Connected to", addr) # print who we are connected with
                    data:bytes = b""
                    while not data:
                        data += conn.recv(4096)
                        # if message post-curser not found, keep polling the socket
                        if(EOM not in data):
                            continue
                    split = data.index(EOM)
                    controllerInformation = data[:split]
                    data = data[split+len(EOM):]
                    controllerInformation = controllerInformation.decode()
                    try:
                        controllerInformation = json.loads(controllerInformation)
                    except JSONDecodeError: # JSONDecode error here is FATAL, abort the connection (and retry connection)
                        Logger.logError(format_exc())
                        s.close()
                        raise ConnectionAbortedError
                    
                    # TODO: MAKE OBSOLETE
                    # parse any events grabbed from socket at this time
                    events:List[List] = []
                    while EOM in data:
                        split = data.index(EOM)
                        try:
                            events.append(json.loads(data[:split].decode().replace('\n','')))
                        except JSONDecodeError:
                            Logger.logError(format_exc())
                        data = data[split+len(EOM):] # if we cut off data, leave cut off data in buffer
                    
                    # once we start getting data, get the first thing sent (our controller information)
                    devices_json = controllerInformation
                    devices = []
                    for device_json in devices_json:
                        capabilities = {}
                        for k, v in device_json['capabilities'].items(): # parse capabilities json
                            capabilities[int(k)] = [x if not isinstance(x, list) else (x[0], evdev.AbsInfo(**x[1])) for x in v]
                        # create new EVDev device
                        devices.append(evdev.UInput(capabilities, name=device_json['name'], vendor=device_json["vendor"], product=device_json["product"], version=device_json["version"]))
                        Logger.log('Controller Device created')
                    
                    # while we are connected read controller data (and try not to miss any events)
                    while True:
                        # poll the socket
                        start = time.time()
                        while EOM not in data: # grab data until EOM character reached
                            data += conn.recv(4096)
                            if(not data and time.time() - start > 60): # 60 second timeout for controller server
                                raise ConnectionResetError
                        
                        # parse data
                        # deocde, remove EOM character, split events into list
                        dataLST:List[str] = data.decode()[:len(data)-len(EOM)].split('\n') 
                        for possibleEvent in dataLST:
                            if(possibleEvent == ''): # check if event is valid
                                continue
                            try:
                                events.append(json.loads(possibleEvent.replace('\n',''))) # get rid of unwanted \n's if they exist
                            except JSONDecodeError: # Error here is not FATAL, ignore the event and continue parsing events
                                Logger.logError(format_exc())
                                continue

                        # apply pending events
                        for event in events:
                            if(event == ''):
                                continue
                            # write events to applicable device
                            devices[int(event[0])].write(int(event[1]), int(event[2]), int(event[3]))
                        events = []
            # connection was reset from other side (or maybe your network dropped)
            except ConnectionResetError:
                Logger.logError(format_exc())
                time.sleep(1) # wait second before retrying connection
                continue

def startControllerServer():
    Logger.log("Controller Server Started")
    while True:
        try:
            doServer()
        except ConnectionAbortedError:
            Logger.logError(format_exc())
            time.sleep(2)
            continue
    

ControllerThread = threading.Thread(target=startControllerServer)
ControllerThread.setName("ControllerThread")
ControllerThread.setDaemon(True)