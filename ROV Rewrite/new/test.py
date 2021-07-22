import time
import cv2
import numpy as np
import json
from tools import Logger
from tools.network import Client
from tools.network.messageType import messageType

cam = cv2.VideoCapture(0)
time.sleep(2)

Logger.createNewLog(purge=True)
Client.IP = "127.0.0.1"
status = True
Client.startClient()


cameraIdent = 0
while True:
    img:np.ndarray = cam.read()[1]
    Client.sendQueue.put_nowait((messageType.camera, (cameraIdent, img)))

cam.release()