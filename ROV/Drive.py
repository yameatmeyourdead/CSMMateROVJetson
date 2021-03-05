from ROV.Logger import Logger
from .Component import Component
from .__main__ import logger

class Drive(Component):

    def __init__(self):
        print("DRIVE CONSTRUCTED")

    def Update(self):
        print("Drive Update")
    
    def autoUpdate(self):
        print("Drive autoUpdate")
    
    def kill(self):
        print("Drive received kill command")

    def logEvent(string):
        logger.log("Test from Drive")

