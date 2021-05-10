import queue
import imagezmq
import cv2
from . import DriverStationMap as DSM
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

    coordinatesPower = 20, 50, 210, 230
    powerCanvas = Canvas(root, bg="white", width=300, height=300)
    powerCanvas.pack()

    coordinatesCurrent = 40, 100, 420, 460
    currentCanvas = Canvas(root, bg="white", width=300, height=300)
    currentCanvas.pack()

    temp_img = ImageTk.PhotoImage(Image.new("RGB", (800, 800)))

    panel = Label(root, image=temp_img)
    panel.image = temp_img
    panel.pack(side="left", padx=10, pady=10)
    root.update()

    NULLFRAME = cv2.imread("DriverStation/Assets/NullFrame.jpg")

    # initialize empty opencv frames so stitching them together works.
    frames = [NULLFRAME, NULLFRAME, NULLFRAME, NULLFRAME]
    organized_frames = [[frames[0], frames[1]], [frames[2], frames[3]]]  # man, naming variables is hard
    output = concat_tile_resize(organized_frames)

    # start looping over all the frames
    while True:
        # receive client name and frame from the client and acknowledge the receipt
        (clientName, frame) = imageHub.recv_image()

        # if there is updated power draw information, display that information receive
        try:
            currentandpower = DSM.dataQueue.get()
            try:
                current = currentandpower[currentandpower.index():currentandpower.index()+5]
                currentandpower[currentandpower.index()+5:]
                power = currentandpower[currentandpower.index():currentandpower.index()+5]
                currentandpower = ""
            except ValueError:
                current = -1
                power = -1
        except queue.Empty:
            pass
        # 800W @ 12V ~ 67A Max???
        # draw unused portion of circle
        powerCanvas.create_arc(coordinatesPower, start=0, extent=360, fill="yellow")
        currentCanvas.create_arc(coordinatesCurrent, start=0, extend=360, fill="yellow")

        # if recieved client did not specify camera designation error out
        if (len(clientName) <= 6 or not (0 <= int(clientName[6:]) <= 3)):
            DSM.log("received image did not contain valid camera designation")
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

        # stitch the frames into one to be displayed
        organized_frames = [[frames[0], frames[1]], [frames[2], frames[3]]]  # man, naming variables is hard
        output = concat_tile_resize(organized_frames)
        frame = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
        framePil = Image.fromarray(frame)
        output = ImageTk.PhotoImage(framePil)

        panel.configure(image=output)
        panel.image = output

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
        DSM.log("Camera Driver Created")

    def start(self):
        self.cameraServer = Process(target=waitForImage)
        self.cameraServer.start()
        print("camera server process")

    def kill(self):
        self.cameraServer.kill()

# use this to put multiple images into one! expects a 2d list of images, and will stack accordingly
def concat_tile_resize(list_2d):
    # function calling for every
    # list of images

    # stacks cv2 images vertically
    def vconcat_resize(img_list, interpolation=cv2.INTER_CUBIC):
        # take minimum width
        w_min = min(img.shape[1] for img in img_list)
        # resizing images
        im_list_resize = [
            cv2.resize(img, (w_min, int(img.shape[0] * w_min / img.shape[1])), interpolation=interpolation) for img
            in img_list]
        # return final image
        return cv2.vconcat(im_list_resize)


    # stacks cv2 images horizontally
    def hconcat_resize(img_list, interpolation=cv2.INTER_CUBIC):
        h_min = min(img.shape[0] for img in img_list)
        im_list_resize = [
            cv2.resize(img, (int(img.shape[1] * h_min / img.shape[0]), h_min), interpolation=interpolation) for img
            in img_list]
        return cv2.hconcat(im_list_resize)

    img_list_v = [hconcat_resize(list_h, interpolation=cv2.INTER_CUBIC) for list_h in list_2d]

    # return final image
    return vconcat_resize(img_list_v, interpolation=cv2.INTER_CUBIC)

# helper method for concatenating picture tiles (use for grayscale images)
def toColor(img):
    return cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
