from queue import Full
import cv2
import threading
from tools.network import Client
from tools.network.messageType import messageType
import time

def doCameraLoop():
    while True:
        # if cams have been destroyed, break loop
        if(len(cams) == 0): break
        for i, camera in enumerate(cams):
            # if camera is enabled, put newest frame into sendQueue
            if(camera is not None and camera.isOpened() and camStatus[i]):
                try:
                    Client.sendQueue.put_nowait((messageType.camera, (i, camera.read()[1])))
                except Full:
                    pass

def start():
    # intialize 4 cams
    global cams, camStatus
    tempCams = list(cv2.VideoCapture(i) for i in range(4))
    camStatus = [False for i in range(4)]
    cams = [None, None, None, None]
    for i,cam in tempCams:
        if(cam is None or not cam.isOpened):
            cams[i] = None
        camStatus[i] = cam.isOpened()

    global cameraThread
    cameraThread = threading.Thread(target=doCameraLoop)
    cameraThread.setName("cameraThread")
    cameraThread.setDaemon(True)
    cameraThread.start()