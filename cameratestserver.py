import imagezmq
import socket
import cv2

imageHub = imagezmq.ImageHub()

# start looping over all the frames
while True:
    # receive RPi name and frame from the RPi and acknowledge
    # the receipt
    (rpiName, frame) = imageHub.recv_image()
    cv2.imshow('dumb stupid code hopefully this works', frame)
    imageHub.send_reply(b'OK')
