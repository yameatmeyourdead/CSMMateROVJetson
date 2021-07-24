import cv2
import time
import numpy as np
from tools.events.event import SubscribeEvent

height = 480
width = 640
image = np.full(shape=(height, width, 3), fill_value=255, dtype=np.uint8)

# create event subscribers for transect object detection
@SubscribeEvent("LargeCoralColonyDetected")
def onLargeCoralColonyDetected(row, col):
    pass

@SubscribeEvent("OutplantDetected")
def onOutplantDetected(row, col):
    pass

@SubscribeEvent("CrownOfThornsDetected")
def onCrownOfThornsDetected(row, col):
    pass

@SubscribeEvent("SpongeDetected")
def onSpongeDetected(row, col):
    pass

@SubscribeEvent("TransectEdgeDetected")
def onTransectEdgeDetected(color):
    pass

@SubscribeEvent("TransectStart")
def onTransectStart():
    print("Transect started")

while True:
    cv2.imshow("image", image)
    cv2.waitKey(1)