# Original methods written by yingtongli under GNU Affero General Public License © 2019
# Source code here -> https://yingtongli.me/git/input-over-ssh
# Modified by Zac Stanton
# Note: this no longer does input over ssh, but rather input over a scuffed implementation of TCP

import asyncio
import evdev
import json
import socket
import time
from multiprocessing import Process
# from . import DriverStationMap

# CHANGE THIS FOR DIFFERENT CONTROLLERS (alternatively implement method to ask the user which device they want (print /dev/input devices and their names) :)  )
CONTROLLERNAME = "Microsoft X-Box One S pad"

async def do_forward_device(i, device):
	async for event in device.async_read_loop():
		# Sends data to jetson (bytes)
		SOC.send(json.dumps([i, event.type, event.code, event.value]).encode())

async def forward_device(i, device):
	await do_forward_device(i, device)

def encode_device(device):
	cap = device.capabilities()
	del cap[0] # Filter out EV_SYN, otherwise we get OSError 22 Invalid argument
	cap_json = {}
	for k, v in cap.items():
		cap_json[k] = [x if not isinstance(x, tuple) else [x[0], x[1]._asdict()] for x in v]
	return {'name': device.name, 'capabilities': cap_json, 'vendor': device.info.vendor, 'product': device.info.product}

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
	SOC.send(json.dumps([encode_device(device) for device in devices]).encode())
	
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

IP = "localhost" # Loopback IP (if testing this network functionality on a single device USE THIS IP)
# IP = "10.0.0.1"
PORT = 7777

def startControllerForwarding():
	print("Attempting to connect to Server")
	SOC.connect((IP, PORT))
	time.sleep(.01) # wait 10 milliseconds before sending anything (no reason, just be safe i guess)
	print("Sucessfully conected......starting controller")
	asyncio.run(run_forward())

SOC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ControllerProcess = Process(target=startControllerForwarding)