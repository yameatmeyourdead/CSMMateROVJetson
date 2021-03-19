from .CameraServer import CameraServer
from .Logger import LOGGER

cameraServer = CameraServer(LOGGER)

LOGGER.log("Attempt Camera Server Start")
cameraServer.start()
LOGGER.log("Camera Server Started")
input("Enter to stop")
cameraServer.kill()
LOGGER.log("Killing ", endO='')