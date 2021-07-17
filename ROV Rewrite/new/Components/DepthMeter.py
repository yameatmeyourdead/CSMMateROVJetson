from Components import Component

# constants
RHO = 1000 # kg/L
g = 9.81 # m/s
RHOg = RHO*g
ATMOSPHERIC_PRESSURE = 0
class DepthMeter(Component):
    def __init__(self) -> None:
        self.depth = 0
    
    @staticmethod
    def calcDepth(pressure):
        """given pressure in N/m^2, returns depth in m"""
        return (pressure +  ATMOSPHERIC_PRESSURE) / RHOg # TODO: determine if we need to add pressures like this
    
    def update(self):
        return

    def autoUpdate(self):
        return
    
    def kill(self):
        return