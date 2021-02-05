import imagezmq
import socket
import cv2

# initialize the ImageSender object with the socket address of the
# server
sender = imagezmq.ImageSender(connect_to="10.0.0.1:5555")

rpiName = socket.gethostname()
stream = cv2.VideoCapture(0)

while True:
    ret, frame = stream.read()
    sender.send_image(rpiName, frame)