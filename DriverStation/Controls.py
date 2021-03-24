import asyncio
import evdev
import json


async def do_forward_device(i, device):
	async for event in device.async_read_loop():
		print(json.dumps([i, event.type, event.code, event.value]))

async def forward_device(i, device):
	if args.exclusive:
		with device.grab_context():
			await do_forward_device(i, device)
	else:
		await do_forward_device(i, device)

async def run_forward():
	# Find devices
	devices_by_name = {}
	if args.device_by_name:
		for path in evdev.list_devices():
			device = evdev.InputDevice(path)
			devices_by_name[device.name] = device
	
	devices = []
	for path in args.device_by_path:
		devices.append(evdev.InputDevice(path))
	for name in args.device_by_name:
		devices.append(devices_by_name[name])
	
	# Report version
	print(PROTOCOL_VERSION)
	
	# Report devices
	print(json.dumps([encode_device(device) for device in devices]))
	
	tasks = []
	for i, device in enumerate(devices):
		tasks.append(asyncio.create_task(forward_device(i, device)))
	
	await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)