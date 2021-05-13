import numpy as np
import cv2
NULLFRAME = cv2.imread("./Assets/NullFrame.jpg")

while True:
	cv2.imshow("bruh", NULLFRAME)
	cv2.waitKey(1)