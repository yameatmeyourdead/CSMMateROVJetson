from .CameraServer import CameraServer
from . import DriverStationMap as DSM

cameraServer = CameraServer()

DSM.log("Attempt Camera Server Start")
print("bruh")
cameraServer.start()
DSM.log("Camera Server Started")
input("Enter to stop")
cameraServer.kill()
DSM.log("Killing ", endO='')