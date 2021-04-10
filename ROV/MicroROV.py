from .Component import Component
from . import ROVMap

class MicroROV(Component):
    def __init__(self):
        # Do setup things
        ROVMap.log("MICROROV CONSTRUCTED")

    def Update(self):
        # (DEBUG)
        # print("MicroROV Update")
        pass
    
    def autoUpdate(self):
        print("MicroROV autoUpdate")
    
    def kill(self):
        print("MicroROV received kill command")