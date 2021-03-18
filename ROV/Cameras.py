import imagezmq
import socket
import cv2

sender = imagezmq.ImageSender(connect_to="tcp://10.0.0.1:5555")
hostName = socket.gethostname()

def returnValidCameraIndexes():
    # checks the first 10 indexes
    index = 0
    arr = []
    i = 10
    while i > 0:
        cap = cv2.VideoCapture(index)
        if cap.read()[0]:
            arr.append(index)
            cap.release()
        index += 1
        i -= 1
    return arr

validCameraIndexes = returnValidCameraIndexes()
camList = []

index = 0
for camera in validCameraIndexes:
    camList.append(cv2.VideoCapture(camera))
    # camList[index].open(camera)
    index += 1

while True:
    index = 0
    for index in range(len(camList)):
        ret, frame = camList[index].read()
        sender.send_image(hostName + str(index), frame)