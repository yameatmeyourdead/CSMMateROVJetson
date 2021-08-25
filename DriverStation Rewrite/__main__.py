from tools import Logger
from tools.network import Client, Server
from gui import GUI
from traceback import format_exc
import cv2

# Debug Tools
purgeLogs = True

def initialize():
    Logger.createNewLog(purgeLogs)
    # GUI already initialized on import resolution
    Client.startClient()
    Server.startServer()
    # ControllerClient.startControllerForwarding()
    Logger.log("DriverStation initialized")

initialize()
try:
    while True:
        # always update GUI (prevent OS from thinking program has stalled)
        GUI.rootWindow.update()
        GUI.updateWidgets()
except:
    Logger.logError(format_exc()[0:-1])
finally:
    Logger.log("Shutting down")