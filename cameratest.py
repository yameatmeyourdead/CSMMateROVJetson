#CAPTURES CAMERA INPUT AND PLACES IT INTO ".\CameraTesting" DIRECTORY

import os
import cv2
import numpy
import time
from datetime import datetime

currentTime = "Current Time : " + str(datetime.time(datetime.now()))
print(currentTime)

CAMERA_OUTPUT_FILEPATH = "CameraTesting\\crying.avi" #"CameraTesting\\" + currentTime + "." + "avi"

if os.path.isfile(CAMERA_OUTPUT_FILEPATH):
    print("path is set to existing file. deleting and continuing")
    os.remove(CAMERA_OUTPUT_FILEPATH)

# Create Camera object and Video Writer Object
capture = cv2.VideoCapture(0)
fps = capture.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*'MPEG')
output = cv2.VideoWriter(CAMERA_OUTPUT_FILEPATH, fourcc, fps, (640, 480))

# While the camera is capturing, show frames and record them into file
start = time.time()
while(capture.isOpened()):
    t_end = start + 30
    if time.time()<t_end:
        ret, frame = capture.read()
        if ret == True:
            cv2.imshow('your dumb face', frame)
            output.write(frame)
        else:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

capture.release()
output.release()
cv2.destroyAllWindows()