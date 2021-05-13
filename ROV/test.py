import numpy as np
import cv2

cap = cv2.VideoCapture(0)

ret, frame = cap.read()
print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

# When everything done, release the capture
cap.release()