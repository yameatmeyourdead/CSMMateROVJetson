import asyncio
import evdev
import json

# CHANGE THIS FOR DIFFERENT CONTROLLERS (alternatively implement method to ask the user which device they want (print /dev/input devices and their names) :)  )
CONTROLLERNAME = "Microsoft X-Box One S pad"

async def do_forward_device(i, device):
	async for event in device.async_read_loop():
		print(json.dumps([i, event.type, event.code, event.value]))

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
	
	devices = []
	devices.append(devices_by_name["Microsoft X-Box One S pad".lower()])
	
	
	# Report devices
	print(json.dumps([encode_device(device) for device in devices]))
	
	# tasks = []
	# for i, device in enumerate(devices):
		# tasks.append(asyncio.create_task(forward_device(i, device)))
	
	# await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

# start the run_forward function
loop = asyncio.get_event_loop()
loop.run_until_complete(run_forward())
loop.close()