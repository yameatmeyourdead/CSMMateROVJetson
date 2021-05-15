from multiprocessing import Process
import numpy as np
import imagezmq
import socket
import cv2

sender = imagezmq.ImageSender(connect_to="tcp://10.0.0.1:5555")
hostName = socket.gethostname()

def doStart():
    # check for valid cams
    camList = [cv2.VideoCapture(0), None, None, None]
    # for i in range(4):
    #     potentialCam = cv2.VideoCapture(i)
    #     if(potentialCam.read()[0]):
    #         camList[i] = potentialCam
    # send images
    while True:
        for i in range(4):
            if(camList[i] is not None):
                ret, frame = camList[i].read()
                sender.send_image("jetson" + str(i), frame)
                # cv2.imshow('frame',frame)
                # cv2.waitKey(1)

CameraProcess = Process(target=doStart)

if __name__ == "__main__":
    CameraProcess.start()
    input("Enter to stop")
    CameraProcess.kill()