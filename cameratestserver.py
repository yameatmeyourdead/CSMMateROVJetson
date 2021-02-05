import imagezmq
import socket
import cv2

imageHub = imagezmq.ImageHub()

# start looping over all the frames
while True:
    # receive client name and frame from the client and acknowledge
    # the receipt
    (clientName, frame) = imageHub.recv_image()
    imageHub.send_reply(b'OK')
    cv2.imshow('dumb stupid code hopefully this works', frame)
