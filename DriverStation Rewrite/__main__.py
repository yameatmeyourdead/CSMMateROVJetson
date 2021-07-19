from tools import Logger
from gui import GUI
from traceback import format_exc
import cv2

# Debug Tools
purgeLogs = True

def initialize():
    Logger.createNewLog(purgeLogs)
    # GUI already initialized on import resolution
    # Client.startClient()
    # Server.startServer()
    # ControllerClient.startControllerForwarding()
    Logger.log("DriverStation initialized")

initialize()
try:
    count = 0
    skip = 0
    cam = cv2.VideoCapture(1)
    while True:
        # always update GUI (prevent OS from thinking program has stalled)
        GUI.updateWidgets()
        GUI.rootWindow.update()

        # simulate other thread getting camera image
        GUI.cameraBuffer.put((0, cam.read()[1]))
        
except:
    Logger.logError(format_exc()[0:-1])
finally:
    cam.release()
    Logger.log("Shutting down")