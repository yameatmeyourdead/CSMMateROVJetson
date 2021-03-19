from time import sleep
from .Component import Component
from . import ROVMap

class Manip(Component):
    def __init__(self):
        # Do setup things
        Manip.logEvent("MANIPULATOR CONSTRUCTED")
        # Try to set servo to specific angle

    def Update(self):
        print("Manipulator Update")
        with ROVMap.CONTROLLER as joystick:
            joystick_lx = (joystick['lx']+1)/2*100
            ROVMap.kit.servo[ROVMap.PCA9685PINOUT["MANIP_PLACEHOLDER_SERVO1"]].angle=joystick_lx
    
    def autoUpdate(self):
        print("Manipulator autoUpdate")
    
    def kill(self):
        print("Manipulator received kill command")

    def logEvent(string):
        ROVMap.LOGGER.log(string)