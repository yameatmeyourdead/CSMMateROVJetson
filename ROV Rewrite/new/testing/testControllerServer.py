import threading
import json
from traceback import format_exc
import socket
from typing import List
import asyncio
try:
    import evdev
except ModuleNotFoundError:
    exit()
import time

IP = "10.0.0.2"
PORT = 7778

EOM = b"<<"

devices = []

async def decode_device():
    data = conn.recv(4096)
    device_data = data[:data.index(EOM)]
    # parse to controller device
    device_json:dict = json.dumps(device_data)
    capabilities = {}
    # format capabilities dict
    for k, v in device_json['capabilities'].items(): 
        capabilities[int(k)] = [x if not isinstance(x, list) else (x[0], evdev.AbsInfo(**x[1])) for x in v]
    # create evdev device
    devices.append(evdev.UInput(capabilities, name=device_json['name'], vendor=device_json["vendor"], product=device_json["product"], version=device_json["version"]))
    await asyncio.wait(asyncio.create_task(do_device_loop(data[data.index(EOM)+len(EOM):])), return_when=asyncio.FIRST_COMPLETED)

async def do_device_loop(data=b""):
    while True:
        start = time.time()
        while EOM not in data:
            data += conn.recv(4096)
            if(not data and time.time() - start > 600): # if nothing received for 5 min, reset connection
                raise ConnectionResetError
        for event in data.decode().split('\n'):
            event = json.loads(event.replace('\n'))
            if(event == ""): continue
            devices[int(event[0])].write(int(event[1]), int(event[2]), int(event[3]))

def doControllerServer():
    global conn
    while True:
        try:
            SOC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            SOC.bind((IP, PORT))
            SOC.listen()
            conn, addr = SOC.accept()
            asyncio.run(decode_device())
        except ConnectionError:
            continue

thread = threading.Thread(target=doControllerServer)
thread.setName("ControllerServerThread")
thread.setDaemon(True)