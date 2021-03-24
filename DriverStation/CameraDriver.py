import imagezmq
import cv2
from .CameraGUIDriver import CameraGUIDriver
from multiprocessing import Process, set_start_method
from tkinter import *
import numpy as np
from PIL import Image
from PIL import ImageTk

def waitForImage(LOGGER):
    # Create the server
    imageHub = imagezmq.ImageHub()

    # initialize empty opencv frames so stitching them together works.
    frames = [np.zeros((400,400,3), np.uint8), np.zeros((400,400,3), np.uint8), np.zeros((400,400,3), np.uint8), np.zeros((400,400,3), np.uint8)]

    # TODO REPLACE THIS WITH GUI CODE
    # start looping over all the frames
    while True:
        # receive client name and frame from the client and acknowledge the receipt
        (clientName, frame) = imageHub.recv_image()

        # if recieved client did not specify camera designation error out
        if (len(clientName) <= 6 or not (0 <= int(clientName[6:]) <= 3)):
            LOGGER.log("received image did not contain valid camera designation")
            continue

        # grab camera designation
        cameraDesignation = int(clientName[6:])

        # Uncomment below line for debug ONLY
        # LOGGER.log(f"received image from camera {cameraDesignation}")
        # cv2.imshow(clientName, frame)
        # cv2.waitKey(1)
        imageHub.send_reply(b'OK')

        # put the frame where it's supposed to go for stitching
        frames[cameraDesignation] = frame

        if (len(frames) == 0):
            continue

        # stitch the frames into one to be displayed
        organized_frames = [[frames[0], frames[1]], [frames[2], frames[3]]]  # man, naming variables is hard
        output = concat_tile_resize(organized_frames)
        frame = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
        framePil = Image.fromarray(frame)
        Tk()
        output = ImageTk.PhotoImage(framePil)

        # if panel doesnt exist yet, initialize it
        if panel is None:
            panel = Label(image=output)
            panel.image = output
            panel.pack(side="left", padx=10, pady=10)

        # otherwise, simply update the panel
        else:
            panel.configure(image=output)
            panel.image = output



class CameraDriver:
    def __init__(self, logger):
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
        self.LOGGER = logger

        self.root = Tk()
        self.panel = None

    def start(self):
        try:
            set_start_method('spawn', force=True)
        except RuntimeError:
            pass
        self.cameraServer = Process(target=waitForImage, args=(self.LOGGER))
        self.cameraServer.start()
        self.root.mainloop()  # start the tk window (hopefully)

    def kill(self):
        self.root.quit()
        self.cameraServer.kill()


# stacks cv2 images vertically (don't actually use this, use concat_tile_resize)
def vconcat_resize(img_list, interpolation=cv2.INTER_CUBIC):
    # take minimum width
    w_min = min(img.shape[1] for img in img_list)
    # resizing images
    im_list_resize = [
        cv2.resize(img, (w_min, int(img.shape[0] * w_min / img.shape[1])), interpolation=interpolation) for img
        in img_list]
    # return final image
    return cv2.vconcat(im_list_resize)


# stacks cv2 images horizontally (don't actually use this, use concat_tile_resize)
def hconcat_resize(img_list, interpolation=cv2.INTER_CUBIC):
    h_min = min(img.shape[0] for img in img_list)
    im_list_resize = [
        cv2.resize(img, (int(img.shape[1] * h_min / img.shape[0]), h_min), interpolation=interpolation) for img
        in img_list]
    return cv2.hconcat(im_list_resize)


# use this to put multiple images into one! expects a 2d list of images, and will stack accordingly
def concat_tile_resize(list_2d):
    # function calling for every
    # list of images
    img_list_v = [hconcat_resize(list_h, interpolation=cv2.INTER_CUBIC) for list_h in list_2d]

    # return final image
    return vconcat_resize(img_list_v, interpolation=cv2.INTER_CUBIC)

# helper method for concatenating picture tiles (use for grayscale images)
def toColor(img):
    return cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
