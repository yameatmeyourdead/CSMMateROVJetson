import pathlib
from typing import Tuple, Union
import cv2
import time
from PIL import Image, ImageDraw
import numpy as np
from tools.events.event import SubscribeEvent, post_event, LargeCoralColonyDetected, OutplantDetected, CrownOfThornsDetected, SpongeDetected, TransectEdgeDetected, TransectStart, TransectFailed
from pathlib import Path

height = 480
width = 640
image = np.full(shape=(height, width, 3), fill_value=255, dtype=np.uint8)
IMAGE_PATH = Path("output\\TransectImage.png")
# defines default width and height of image where we have 32x32 squares arranged in 9x3 formation with 16 pixels of padding on all sides
DWIDTH = 320
DHEIGHT = 128
GRID_PAD = 16
CELL_SIZE_X = 32
CELL_SIZE_Y = 32
CIRCLE_DIAMETER = 20
CIRCLE_PAD = 6

# create event subscribers responsible for drawing during transect object detection
@SubscribeEvent(LargeCoralColonyDetected)
async def onLargeCoralColonyDetected(cell_1: Tuple[int, int], cell_2: Tuple[int, int]):
    if abs(cell_1[0] - cell_2[0]) == abs(cell_1[1] - cell_2[1]):
        raise AssertionError("Large Coral Colony must take up two cells directly adjacent in the 4 cardinal directions")
    start = (min(cell_1[1], cell_2[1]) * CELL_SIZE_X + CIRCLE_PAD + GRID_PAD, min(cell_1[0], cell_2[0]) * CELL_SIZE_Y + CIRCLE_PAD + GRID_PAD)
    end = (max(cell_1[1], cell_2[1]) * CELL_SIZE_X + CIRCLE_PAD + GRID_PAD + CIRCLE_DIAMETER, max(cell_1[0], cell_2[0]) * CELL_SIZE_Y + CIRCLE_PAD + GRID_PAD + CIRCLE_DIAMETER)
    drawEllipseAtCoords(start, end, (255, 0, 0))

@SubscribeEvent(OutplantDetected)
async def onOutplantDetected(row=None, col=None):
    start = (col * CELL_SIZE_X + CIRCLE_PAD + GRID_PAD, row * CELL_SIZE_Y + CIRCLE_PAD + GRID_PAD)
    end = (start[0] + CIRCLE_DIAMETER, start[1] + CIRCLE_DIAMETER) 
    drawEllipseAtCoords(start, end, color=(255, 255, 0))

@SubscribeEvent(CrownOfThornsDetected)
async def onCrownOfThornsDetected(row=None, col=None):
    start = (col * CELL_SIZE_X + CIRCLE_PAD + GRID_PAD, row * CELL_SIZE_Y + CIRCLE_PAD + GRID_PAD)
    end = (start[0] + CIRCLE_DIAMETER, start[1] + CIRCLE_DIAMETER)
    drawEllipseAtCoords(start, end, color=(0, 0, 255))

@SubscribeEvent(SpongeDetected)
async def onSpongeDetected(row=None, col=None):
    start = (col * CELL_SIZE_X + CIRCLE_PAD + GRID_PAD, row * CELL_SIZE_Y + CIRCLE_PAD + GRID_PAD)
    end = (start[0] + CIRCLE_DIAMETER, start[1] + CIRCLE_DIAMETER)
    drawEllipseAtCoords(start, end, (0, 255, 0))

@SubscribeEvent(TransectEdgeDetected)
async def onTransectEdgeDetected(side=None, color=None):
    pass

@SubscribeEvent(TransectStart)
async def onTransectStart():
    print("Transect started")

@SubscribeEvent(TransectFailed)
async def onTransectFailed(reason=None):
    print(f"Transect failed; reason given: '{reason}'")

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