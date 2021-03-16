from time import sleep
from .Component import Component
from . import ROVMap

class Manip(Component):
    def __init__(self):
        # Do setup things
        Manip.logEvent("MANIPULATOR CONSTRUCTED")
        # Try to set servo to specific angle
        ROVMap.kit.servo[ROVMap.PCA9685PINOUT["MANIP_PLACEHOLDER_SERVO1"]].angle=137

    def Update(self):
        sleep(5)
        print("Manipulator Update")
        ROVMap.kit.servo[ROVMap.PCA9685PINOUT["MANIP_PLACEHOLDER_SERVO1"]].angle=100
        sleep(5)
    
    def autoUpdate(self):
        print("Manipulator autoUpdate")
    
    def kill(self):
        print("Manipulator received kill command")

    def logEvent(string):
        ROVMap.LOGGER.log(string)