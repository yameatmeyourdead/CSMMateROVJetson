import cv2
import threading
from multiprocessing import Queue
from tools.network.Client import sendQueue, messageType

# intialize 4 cams
cams = tuple(cv2.VideoCapture(i) for i in range(4))
meta = [True for i in range(4)]

def update():
    for i, camera in enumerate(cams):
        # if camera is enabled, put newest frame into sendQueue
        if(meta[i]):
            sendQueue.put((messageType.camera, camera.read()[1]))
            

def start():
    cameraThread = threading.Thread(target=update)
    cameraThread.setName("cameraThread")
    cameraThread.start()