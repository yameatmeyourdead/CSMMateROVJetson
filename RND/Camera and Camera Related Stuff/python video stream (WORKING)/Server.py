import imagezmq
import cv2

imageHub = imagezmq.ImageHub()

# start looping over all the frames
while True:
    # receive client name and frame from the client and acknowledge
    # the receipt
    (clientName, frame) = imageHub.recv_image()
    cv2.imshow(clientName, frame)
    cv2.waitKey(1)
    imageHub.send_reply(b'OK')
