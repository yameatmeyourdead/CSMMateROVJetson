import pathlib
import cv2
import time
from PIL import Image, ImageDraw
import numpy as np
from tools.events.event import SubscribeEvent, post_event
from pathlib import Path

height = 480
width = 640
image = np.full(shape=(height, width, 3), fill_value=255, dtype=np.uint8)
IMAGE_PATH = Path("testing\\testTransectImage.png")
# defines default width and height of image where we have 32x32 squares arranged in 9x3 formation with 16 pixels of padding on all sides
DWIDTH = 320
DHEIGHT = 128
PAD = 16
CELL_SIZE_X = 32
CELL_SIZE_Y = 32
CIRCLE_SIZE = 11
CIRCLE_OFFSET = 11

# create event subscribers drawing during transect object detection
@SubscribeEvent("LargeCoralColonyDetected")
def onLargeCoralColonyDetected(row=None, col=None):
    pass

@SubscribeEvent("OutplantDetected")
def onOutplantDetected(row=None, col=None):
    pass

@SubscribeEvent("CrownOfThornsDetected")
def onCrownOfThornsDetected(row=None, col=None):
    pass

@SubscribeEvent("SpongeDetected")
def onSpongeDetected(row=None, col=None):
    print("sponge detected at", row, col)
    im, draw = getImageDrawCTX()
    start = (row * CELL_SIZE_X + CIRCLE_OFFSET, col * CELL_SIZE_Y + CIRCLE_OFFSET)
    end = (start[0] + CIRCLE_SIZE//2, start[1] + CIRCLE_SIZE//2)
    draw.ellipse((start, end), fill=(0, 255, 0, 255), outline=(0, 255, 0, 255), width=1)
    im.save(IMAGE_PATH)

@SubscribeEvent("TransectEdgeDetected")
def onTransectEdgeDetected(side=None, color=None):
    pass

@SubscribeEvent("TransectStart")
def onTransectStart():
    print("Transect started")
    resetImage()

def resetImage():
    global im
    # get image if it already exists, else make new one
    if(Path.exists(IMAGE_PATH)):
        im = Image.open(IMAGE_PATH)
    else:
        im = Image.new(mode="RGBA", size=(DWIDTH, DHEIGHT), color=(255, 255, 255, 255))
    draw = ImageDraw.Draw(im)
    # draw background
    draw.rectangle(xy=((0, 0), (DWIDTH, DHEIGHT)), fill=(255, 255, 255, 255))
    # redraw 9x3 grid
    for row in range(3):
        for col in range(9):
            draw.rectangle(((col * CELL_SIZE_X + PAD, row * CELL_SIZE_Y + PAD), (col * CELL_SIZE_X + PAD + CELL_SIZE_X, row * CELL_SIZE_Y + PAD + CELL_SIZE_Y)), fill=(255,255,255,255), outline=(0,0,0,255), width=1)
    # save reset Image
    im.save(IMAGE_PATH)

def initialize():
    resetImage()

def getImageCTX():
    if(Path.exists(IMAGE_PATH)):
        return Image.open(IMAGE_PATH)
    else:
        raise FileNotFoundError

def getImageDrawCTX():
    if(Path.exists(IMAGE_PATH)):
        return Image.open(IMAGE_PATH), ImageDraw.Draw(Image.open(IMAGE_PATH))
    else:
        raise FileNotFoundError

def run():
    initialize()
    # post_event("TransectStart")
    post_event("SpongeDetected", row=1, col=1)
    getImageCTX().show()
    pass