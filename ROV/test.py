import numpy as np
import imagezmq
import cv2

cap = cv2.VideoCapture(0)
sender = imagezmq.ImageSender(connect_to="tcp://10.0.2.15:5555")

while True:
    ret, frame = cap.read()
    sender.send_image("jetson0", frame)