from .CameraDriver import CameraDriver
from . import DriverStationMap as DSM

DSM.log("Attempt Camera Driver Start")
cameraDriver = CameraDriver()

print("bruh")
cameraDriver.start()
DSM.log("Camera Driver Started")
input("Enter to stop")
cameraDriver.kill()
DSM.log("Killing ", endO='')