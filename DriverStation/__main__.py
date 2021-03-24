from .CameraDriver import CameraDriver
from . import DriverStationMap as DSM

cameraDriver = CameraDriver()

DSM.log("Attempt Camera Driver Start")
print("bruh")
cameraDriver.start()
DSM.log("Camera Driver Started")
input("Enter to stop")
cameraDriver.kill()
DSM.log("Killing ", endO='')