# Original methods written by yingtongli under GNU Affero General Public License © 2019
# Source code here -> https://yingtongli.me/git/input-over-ssh
# Modified by Zac Stanton
# Note: this no longer does input over ssh, but rather input over a scuffed implementation of TCP

import socket
from multiprocessing import Process
try:
    import evdev
except ModuleNotFoundError:
    print("This code only works on linux machines with evdev installed.....Exiting this program")
    exit()
import json
import time

HOST = "10.0.0.2" # jetson's static ip address
PORT = 7777 # port to listen to

def startControllerServer():
    # create new socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT)) # bind our socket to our port
        print("Listening for connections")
        s.listen() # wait for connection
        conn, addr = s.accept() # once connection available, accept it (THIS IS BLOCKING)
        try:
            with conn:
                print("Connected to", addr) # print who we are connected with
                data = conn.recv(1024)
                while not data:
                    data = conn.recv(1024)
                # once we start getting data, get the first thing sent (our controller information)
                devices_json = json.loads(data.decode().split('\n')[0])
                devices = []
                for device_json in devices_json:
                    capabilities = {}
                    for k, v in device_json['capabilities'].items():
                        capabilities[int(k)] = [x if not isinstance(x, list) else (x[0], evdev.AbsInfo(**x[1])) for x in v]
                    devices.append(evdev.UInput(capabilities, name=device_json['name'] + ' (via input-over-ssh)'))
                    print('Device created')
                # while we are connected read controller data
                while True:
                    data = conn.recv(1024)
                    if not data:
                        continue
                    # get relevant event data 
                    event = list(data.decode().split('\n'))[-2]
                    # print(event)
                    devices[event[0]].write(event[1], event[2], event[3])
        # connection was reset from other side (or maybe your network dropped)
        except ConnectionResetError:
            print("Connection with", addr, " forcibly closed")

# TODO: implement restarting of the server if connection is reset

# Module scope only executed once, therefore this is safe (mostly)
ControllerProcess = Process(target=startControllerServer)
ControllerProcess.start()