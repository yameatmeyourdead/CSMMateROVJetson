from time import sleep
from .Component import Component
from . import ROVMap

class Manip(Component):
    def __init__(self):
        # Do setup things
        Manip.logEvent("MANIPULATOR CONSTRUCTED")

    def Update(self):
        print("Manipulator Update")
        # Test controls
        desired_angle = (ROVMap.getLeftStick[0]+1)/2*180
        ROVMap.kit.servo[ROVMap.PCA9685PINOUT["MANIP_PLACEHOLDER_SERVO1"]].angle=desired_angle
    
    def autoUpdate(self):
        print("Manipulator autoUpdate")
    
    def kill(self):
        print("Manipulator received kill command")

    def logEvent(string):
        ROVMap.log(string)