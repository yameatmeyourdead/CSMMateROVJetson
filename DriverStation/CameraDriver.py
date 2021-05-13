import queue
import imagezmq
import cv2
# from . import DriverStationMap as DSM
from multiprocessing import Process
from tkinter import *
import numpy as np
from PIL import Image
from PIL import ImageTk

def waitForImage():
    # Create the server
    imageHub = imagezmq.ImageHub()

    # Create TKinter Window
    root = Tk()

    LABEL = Label(root, text="Cams")
    LABEL.pack()
    root.update()

    NULLFRAME = cv2.imread("./Assets/NullFrame.jpg")

    # initialize empty opencv frames so stitching them together works.
    frames = [NULLFRAME, NULLFRAME, NULLFRAME, NULLFRAME]
    organized_frames = [[frames[0], frames[1]], [frames[2], frames[3]]]  # man, naming variables is hard
    output = ImageTk.PhotoImage(Image.fromarray(concat_tile_resize(organized_frames)))

    panel = Label(root, image=output)
    panel.pack(side="left", padx=10, pady=10)
    root.update()

    # start looping over all the frames
    while True:
        # receive client name and frame from the client and acknowledge the receipt
        (clientName, frame) = imageHub.recv_image()

        # if recieved client did not specify camera designation error out
        if (len(clientName) <= 6 or not (0 <= int(clientName[6:]) <= 3)):
            # DSM.log("received image did not contain valid camera designation")
            root.update()
            continue

        # grab camera designation
        cameraDesignation = int(clientName[6:])

        if frame is not None:
            # put the frame where it's supposed to go for stitching
            frames[cameraDesignation] = frame
        
        # Uncomment below line for debug ONLY
        # DSM.log(f"received image from camera {cameraDesignation}")
        # cv2.imshow(cameraDesignation, frame)
        # cv2.waitKey(1)
        imageHub.send_reply(b'OK')

        if (len(frames) == 0):
            continue

        # stitch the frames into one to be displaye
        panel.image = ImageTk.PhotoImage(Image.fromarray(concat_tile_resize([[frames[0], frames[1]], [frames[2], frames[3]]])))

        root.update()



class CameraDriver:
    def __init__(self):
        '''
        Use to create distinct camera server using imagezmq
        One has already been created for you in /DriverStation/__main__.py
        call .kill() on CameraServer object in order to stop process

        Usage:
                newCameraServerObject = CameraServer()\n
                newCameraServerObject.start()\n
                (  Some time passes  )\n
                newCameraServerObject.kill()\n
                (  Process is no longer running :)  )
        '''
        pass
        # DSM.log("Camera Driver Created")

    def start(self):
        self.cameraServer = Process(target=waitForImage)
        self.cameraServer.start()
        print("camera server process")

    def kill(self):
        self.cameraServer.kill()

# use this to put multiple images into one! expects a 2d list of images, and will stack accordingly
def concat_tile_resize(list_2d):
    # stack first two cams horizontally (cam0|cam1)
    firstTwo = cv2.hconcat([list_2d[0][0], list_2d[0][1]])
    # stack second two cams horizontally (cam2|cam3)
    secondTwo = cv2.hconcat([list_2d[1][0], list_2d[1][1]])
    # combine them
    # (cam0|cam1)
    # (cam2|cam3)
    return cv2.vconcat([firstTwo, secondTwo])

# helper method for concatenating picture tiles (use for grayscale images)
def toColor(img):
    return cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)