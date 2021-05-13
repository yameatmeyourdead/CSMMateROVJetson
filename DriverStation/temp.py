import imagezmq
import cv2
imageHub = imagezmq.ImageHub()

while True:
	(clientName, frame) = imageHub.recv_image()
	imageHub.send_reply(b"OK")
	cv2.imshow(clientName, frame)