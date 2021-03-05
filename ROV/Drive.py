from .Component import Component
from . import ROVMap

class Drive(Component):
    def __init__(self):
        # Do setup things
        Drive.logEvent("DRIVE CONSTRUCTED")

    def Update(self):
        print("Drive Update")
    
    def autoUpdate(self):
        print("Drive autoUpdate")
    
    def kill(self):
        print("Drive received kill command")

    def logEvent(string):
        ROVMap.LOGGER.log(string)

