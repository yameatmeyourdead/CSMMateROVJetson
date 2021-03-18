from multiprocessing import Process, set_start_method, Queue
from tkinter import *
import cv2
import numpy as np
from PIL import Image
from PIL import ImageTk


def updateCams(queues, panel):
    while True:
        frames = []
        for index in range(4):
            if (queues[index].qsize()):
                # Do thing with frame
                # this is disgusting but it fine don't worry
                frame = queues[index].get()
                frame = cv2.cvtColor(cv2.COLOR_BGR2RGB, frame)
                frame = Image.fromarray(frame)
                frame = ImageTk.PhotoImage(frame)
                frames.append(frame)

        other_list = [[frames[0], frames[1]], [frames[2], frames[3]]]  # man, naming variables is hard
        output = concat_tile_resize(other_list)

        # if panel doesnt exist yet, initialize it
        if panel is None:
            panel = Label(image=output)
            panel.image = output
            panel.pack(side="left", padx=10, pady=10)

        # otherwise, simply update the panel
        else:
            panel.configure(image=output)
            panel.image = output


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


def toColor(img):
    return cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)


class CameraGUIDriver:

    def __init__(self, que):
        """
        GOD IS DEAD AND I KILLED HIM. NO IM NOT EXPLAINING WHY THIS IS A THING (until i calm down, come read the class comments)
        """
        self.queues = que
        self.root = Tk()
        self.panel = None

    def start(self):
        set_start_method("spawn")
        self.guiDriver = Process(target=updateCams, args=(self.queues, self.panel))
        self.guiDriver.start()

    def kill(self):
        self.guiDriver.kill()
