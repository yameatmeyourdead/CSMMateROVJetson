from .CameraDriver import CameraDriver
from . import DriverStationMap as DSM
from .IMU import IMUManager
from .ControllerClient import ControllerProcess

DSM.log("Attempt Camera Driver Start")
cameraDriver = CameraDriver()
cameraDriver.start()
DSM.log("Camera Driver Started")

DSM.log("Attempt to Pass Controller")
ControllerProcess.start()
DSM.log("Controller Process Started")

DSM.log("Attempt to start networking")
DSM.DriverStationNetworking.start()
DSM.log("Networking process started")

IMUManager.start()

input("Enter to stop\n")
cameraDriver.kill()
ControllerProcess.kill()
DSM.DriverStationNetworking.kill()
IMUManager.kill()
DSM.log("Killing ", endO='')