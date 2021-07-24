from queue import Full
import cv2
import threading
from tools.network import Client
from tools.network.messageType import messageType
import time

# intialize 4 cams
cams = tuple(cv2.VideoCapture(i) for i in range(4))
camStatus = [True, False, False, False]

def doCameraLoop():
    while True:
        # if cams have been destroyed, break loop
        if(len(cams) == 0): break
        for i, camera in enumerate(cams):
            # if camera is enabled, put newest frame into sendQueue
            if(camStatus[i] and camera.isOpened()):
                try:
                    Client.sendQueue.put_nowait((messageType.camera, (i, camera.read()[1])))
                except Full:
                    pass


def start():
    global cameraThread
    cameraThread = threading.Thread(target=doCameraLoop)
    cameraThread.setName("cameraThread")
    cameraThread.start()