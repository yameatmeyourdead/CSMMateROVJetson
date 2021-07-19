import cv2
import numpy as np

cam = cv2.VideoCapture(1)
image:np.ndarray = cam.read()[1]

# print(image.shape)
toSend = image.dumps()

cv2.imshow("did it work", np.loads(toSend))
cv2.waitKey(10000)