import imagezmq
import socket
import cv2

# initialize the ImageSender object with the socket address of the
# server
sender = imagezmq.ImageSender(connect_to="tcp://10.0.0.1:5555")

hostName = socket.gethostname()
stream = cv2.VideoCapture(0)

while True:
    ret, frame = stream.read()
    if ret == True:
        sender.send_image(hostName, frame)
    else:
        break