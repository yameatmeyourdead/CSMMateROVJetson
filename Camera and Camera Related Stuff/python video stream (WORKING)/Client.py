import imagezmq
import socket
import cv2

# initialize the ImageSender object with the socket address of the
# server
sender = imagezmq.ImageSender(connect_to="tcp://10.0.0.1:5555")

dispW=320
dispH=240
flip=2
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'

hostName = socket.gethostname()
stream = cv2.VideoCapture(camSet)
if(not stream.isOpened()):
    stream.open()
while True:
    ret, frame = stream.read()
    sender.send_image(hostName, frame)