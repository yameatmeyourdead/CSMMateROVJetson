from .Component import Component
from . import ROVMap

class Manip(Component):
    def __init__(self):
        # Do setup things
        Manip.logEvent("Manipulator Constructed")

    def Update(self):
        print("Manipulator Update")
    
    def autoUpdate(self):
        print("Manipulator autoUpdate")
    
    def kill(self):
        print("Manipulator received kill command")

    def logEvent(string):
        ROVMap.LOGGER.log(string)