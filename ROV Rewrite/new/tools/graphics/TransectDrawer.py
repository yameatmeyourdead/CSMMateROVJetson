import pathlib
from typing import Tuple, Union
import cv2
import time
from PIL import Image, ImageDraw
import numpy as np
from tools.events.event import SubscribeEvent, post_event
from pathlib import Path

transectView = [[None for x in range(9)], [None for x in range(9)], [None for x in range(9)]]

height = 480
width = 640
image = np.full(shape=(height, width, 3), fill_value=255, dtype=np.uint8)
IMAGE_PATH = Path("testing\\testTransectImage.png")
# defines default width and height of image where we have 32x32 squares arranged in 9x3 formation with 16 pixels of padding on all sides
DWIDTH = 320
DHEIGHT = 128
GRID_PAD = 16
CELL_SIZE_X = 32
CELL_SIZE_Y = 32
CIRCLE_DIAMETER = 20
CIRCLE_PAD = 6

# create event subscribers drawing during transect object detection
@SubscribeEvent("LargeCoralColonyDetected")
def onLargeCoralColonyDetected(cell_1: Tuple[int, int], cell_2: Tuple[int, int]):
    assert transectView[cell_1[0]][cell_1[1]] == None and transectView[cell_2[0]][cell_2[1]] == None, "Object already present at position in Transect"
    transectView[cell_1[0]][cell_1[1]] = "Large Coral Colony Cell1"
    transectView[cell_2[0]][cell_2[1]] = "Large Coral Colony Cell2"
    if abs(cell_1[0] - cell_2[0]) == abs(cell_1[1] - cell_2[1]):
        raise AssertionError("Large Coral Colony must take up two cells directly adjacent in the 4 cardinal directions")
    start = (min(cell_1[1], cell_2[1]) * CELL_SIZE_X + CIRCLE_PAD + GRID_PAD, min(cell_1[0], cell_2[0]) * CELL_SIZE_Y + CIRCLE_PAD + GRID_PAD)
    end = (max(cell_1[1], cell_2[1]) * CELL_SIZE_X + CIRCLE_PAD + GRID_PAD + CIRCLE_DIAMETER, max(cell_1[0], cell_2[0]) * CELL_SIZE_Y + CIRCLE_PAD + GRID_PAD + CIRCLE_DIAMETER)
    drawEllipseAtCoords(start, end, (255, 0, 0))

@SubscribeEvent("OutplantDetected")
def onOutplantDetected(row=None, col=None):
    assert transectView[row][col] == None, "Object already present at position in Transect"
    start = (col * CELL_SIZE_X + CIRCLE_PAD + GRID_PAD, row * CELL_SIZE_Y + CIRCLE_PAD + GRID_PAD)
    end = (start[0] + CIRCLE_DIAMETER, start[1] + CIRCLE_DIAMETER) 
    drawEllipseAtCoords(start, end, color=(255, 255, 0))

@SubscribeEvent("CrownOfThornsDetected")
def onCrownOfThornsDetected(row=None, col=None):
    assert transectView[row][col] == None, "Object already present at position in Transect"
    start = (col * CELL_SIZE_X + CIRCLE_PAD + GRID_PAD, row * CELL_SIZE_Y + CIRCLE_PAD + GRID_PAD)
    end = (start[0] + CIRCLE_DIAMETER, start[1] + CIRCLE_DIAMETER)
    drawEllipseAtCoords(start, end, color=(0, 0, 255))

@SubscribeEvent("SpongeDetected")
def onSpongeDetected(row=None, col=None):
    assert transectView[row][col] == None, "Object already present at position in Transect"
    start = (col * CELL_SIZE_X + CIRCLE_PAD + GRID_PAD, row * CELL_SIZE_Y + CIRCLE_PAD + GRID_PAD)
    end = (start[0] + CIRCLE_DIAMETER, start[1] + CIRCLE_DIAMETER)
    drawEllipseAtCoords(start, end, (0, 255, 0))

@SubscribeEvent("TransectEdgeDetected")
def onTransectEdgeDetected(side=None, color=None):
    pass

@SubscribeEvent("TransectStart")
def onTransectStart():
    print("Transect started")

def resetTransect():
    global im, transectView
    # reset current internal description of transect
    transectView = [[None for x in range(9)], [None for x in range(9)], [None for x in range(9)]]
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
            draw.rectangle(((col * CELL_SIZE_X + GRID_PAD, row * CELL_SIZE_Y + GRID_PAD), (col * CELL_SIZE_X + GRID_PAD + CELL_SIZE_X, row * CELL_SIZE_Y + GRID_PAD + CELL_SIZE_Y)), fill=(255,255,255,255), outline=(0,0,0,255), width=1)
    # save reset Image
    im.save(IMAGE_PATH)

def initialize():
    resetTransect()

def getImageCTX():
    if(Path.exists(IMAGE_PATH)):
        return Image.open(IMAGE_PATH)
    else:
        raise FileNotFoundError

def getImageDrawCTX():
    if(Path.exists(IMAGE_PATH)):
        im = Image.open(IMAGE_PATH)
        return im, ImageDraw.Draw(im)
    else:
        raise FileNotFoundError

def drawEllipseAtCoords(start:Tuple[int,int] = 0, end:Tuple[int,int] = 0, color:Tuple[int, int, int]=(255,255,255)):
    im, draw = getImageDrawCTX()
    draw.ellipse((start,end), fill=color, outline=0)
    im.save(IMAGE_PATH)


# DEBUG
# def run():
#     initialize()
#     post_event("TransectStart")
#     post_event("SpongeDetected", row=0, col=0)
#     post_event("OutplantDetected", row=1, col=1)
#     post_event("CrownOfThornsDetected", row=1, col=4)
#     post_event("LargeCoralColonyDetected", cell_1=(2,5), cell_2=(2,6))
#     post_event("CrownOfThornsDetected", row=2, col=8)
#     post_event("OutplantDetected", row=0, col=7)
#     getImageCTX().show()