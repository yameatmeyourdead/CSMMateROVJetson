# Original methods written by yingtongli under GNU Affero General Public License © 2019
# Source code here -> https://yingtongli.me/git/input-over-ssh
# Modified by Zac Stanton
# Note: this no longer does input over ssh, but rather input over a scuffed implementation of TCP

import asyncio
try:
    import evdev
except ModuleNotFoundError:
    print("This code only works on linux machines with evdev installed.....Exiting this program")
    exit()
import json
import socket
import time
from tools import Logger
from multiprocessing import Process
import threading

# CHANGE THIS FOR DIFFERENT CONTROLLERS (alternatively implement method to ask the user which device they want (print /dev/input devices and their names) :)  )
CONTROLLERNAME = "Microsoft X-Box One S pad"
CONTROLLERVENDORID = 1118
CONTROLLERPRODUCTID = 746

EOM = b"<<"

async def do_forward_device(i, device):
	async for event in device.async_read_loop():
		# Sends data to jetson (bytes) wrapped in delimeters
		SOC.send(json.dumps(([i, event.type, event.code, event.value])).encode() + b'\n')

async def forward_device(i, device):
	await do_forward_device(i, device)

def encode_device(device):
	cap = device.capabilities()
	del cap[0] # Filter out EV_SYN, otherwise we get OSError 22 Invalid argument
	cap_json = {}
	for k, v in cap.items():
		cap_json[k] = [x if not isinstance(x, tuple) else [x[0], x[1]._asdict()] for x in v]
	# have to replace device.info.vendor with 1118 and device.info.product with 746 (identifies controller as XBox Controller)
	return {'name': device.name, 'capabilities': cap_json, 'vendor': CONTROLLERVENDORID, 'product': CONTROLLERPRODUCTID}

async def run_forward():
	# Find devices
	devices_by_name = {}
	for path in evdev.list_devices():
		device = evdev.InputDevice(path)
		devices_by_name[device.name.lower()] = device
	
	# Choose the device you want (hardcoded because im a lamo)
	devices = []
	devices.append(devices_by_name[CONTROLLERNAME.lower()])
	
	# Report devices to server
	print(json.dumps([encode_device(device) for device in devices]))
	SOC.sendall(json.dumps([encode_device(device) for device in devices]).encode() + b"<\n")
	time.sleep(.25) # wait for little time to prevent overlapping messages
	tasks = []
	for i, device in enumerate(devices):
		tasks.append(asyncio.create_task(forward_device(i, device)))
	
	await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

async def list_devices():
	for path in evdev.list_devices():
			device = evdev.InputDevice(path)
			print(f"{device.path}  {device.name}")

# NETWORK STUFF!!!!!! (boo) (i lied there is network thing in do_forward_device)
# This hurts me and I understand nothing written in this file
# Port     Use
# 7777    Controller

# IP = "localhost" # Loopback IP (if testing this network functionality on a single device USE THIS IP)
IP = "10.0.0.2"
PORT = 7778

def doControllerForwarding():
	# try to connect to server
	while True:
		try:
			Logger.log("Attempting to connect to Controller Server")
			SOC.connect((IP, PORT))
			time.sleep(.01) # wait 10 milliseconds before sending anything (no reason, just be safe i guess)
			Logger.log("Sucessfully connected to Controller Server......starting controller")
			break
		except: # in case of error (such as server not running yet), retry connection in 5 seconds
			Logger.log("Connection unable to be established. Retrying in 2 seconds")
			time.sleep(2)
			continue
	# after ensuring connection to controller server, start sending data
	asyncio.run(run_forward())

def startControllerForwarding():
	global ControllerThread
	ControllerThread = threading.Thread(target=doControllerForwarding)
	ControllerThread.setName("ControllerThread")
	ControllerThread.setDaemon(True)
	ControllerThread.start()

SOC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)