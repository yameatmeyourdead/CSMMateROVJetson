from .Component import Component
from . import ROVMap

class MicroROV(Component):
    def __init__(self):
        # Do setup things
        MicroROV.logEvent("MICROROV CONSTRUCTED")

    def Update(self):
        print("MicroROV Update")
    
    def autoUpdate(self):
        print("MicroROV autoUpdate")
    
    def kill(self):
        print("MicroROV received kill command")
    
    def logEvent(string):
        ROVMap.log(string)