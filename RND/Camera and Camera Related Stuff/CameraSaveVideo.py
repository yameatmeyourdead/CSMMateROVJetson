#CAPTURES CAMERA INPUT AND PLACES IT INTO ".\CameraTestingLogs" DIRECTORY

import os
import cv2
import time

# create file for outputting camera data to
currentTime = str(time.time_ns())
CAMERA_OUTPUT_FILEPATH = "CameraTestingLogs\\" + currentTime + "." + "avi"



if os.path.isfile(CAMERA_OUTPUT_FILEPATH):
    print("path is set to existing file. deleting and continuing")
    os.remove(CAMERA_OUTPUT_FILEPATH)

# Checks for valid camera indexes
def returnCameraIndexes():
    # checks the first 10 indexes.
    index = 0
    arr = []
    i = 10
    while i > 0:
        cap = cv2.VideoCapture(index)
        if cap.read()[0]:
            arr.append(index)
            cap.release()
        index += 1
        i -= 1
    return arr

# print("(DEBUG) VALID CAMERA INDEXES :", returnCameraIndexes())

# Create Camera object and Video Writer Object
capture = cv2.VideoCapture(0)
fps = capture.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*'MPEG')
output = cv2.VideoWriter(CAMERA_OUTPUT_FILEPATH, fourcc, fps, (640, 480), True)

# While the camera is capturing, show frames and record them into file
while(True):
    # capture and display frame
    ret, frame = capture.read()
    cv2.imshow('frame', frame)

    # write output to file
    output.write(frame)

    # if q has been pressed, quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
output.release()
cv2.destroyAllWindows()