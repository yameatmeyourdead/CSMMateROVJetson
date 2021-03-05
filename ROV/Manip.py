from .Component import Component
from .__main__ import logger

class Manip(Component):
    def __init__(self):
        print("MANIPULATOR CONSTRUCTED")

    def Update(self):
        print("Manipulator Update")
    
    def autoUpdate(self):
        print("Manipulator autoUpdate")
    
    def kill(self):
        print("Manipulator received kill command")

    def logEvent(string):
        logger.log("Test from Manip")