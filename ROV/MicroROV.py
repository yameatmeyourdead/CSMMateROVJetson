from .Component import Component
from .__main__ import logger

class MicroROV(Component):
    def __init__(self):
        print("MICROROV CONSTRUCTED")

    def Update(self):
        print("MicroROV Update")
    
    def autoUpdate(self):
        print("MicroROV autoUpdate")
    
    def kill(self):
        print("MicroROV received kill command")
    
    def logEvent(string):
        logger.log("Test from Drive")