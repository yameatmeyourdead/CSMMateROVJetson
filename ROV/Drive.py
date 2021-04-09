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
        for ESCS in ROVMap.PCA9685PINOUT[0]:
            for ESC in ESCS.values():
                try:
                    ROVMap.kit._items[ESC].duty_cycle = 0
                except:
                    pass
        print("Drive received kill command")

    def logEvent(string):
        ROVMap.log(string)

