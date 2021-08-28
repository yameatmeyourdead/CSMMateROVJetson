from Components import Component
import ms5803py

# constants
RHO = 1000 # kg/L TODO: DETERMINE DENSITY OF THE WATER WE ARE IN
gravitationalAcceleration = 9.81 # m/s TODO: contemplate replacing this with IMU.getGravity() for more accurate gravitational acceleration (probably doesnt matter for the error we have)
ATMOSPHERIC_PRESSURE = 0 # Average for denver is ~1015.92
class DepthMeter(Component):
    def __init__(self) -> None:
        self.MS5803 = ms5803py.MS5803(address=0x76)

    def calcDepth(self):
        """Returns current depth in m determined by current pressure given by the MS5803"""
        # 1 mBar = 100 N/m^2
        pressure = self.MS5803.read_raw_pressure(osr=2048) * 100 #TODO: determine if this sampling rate is too slow for our purposes
        return (pressure +  ATMOSPHERIC_PRESSURE) / (RHO * gravitationalAcceleration) # TODO: determine if we need to add atmospheric pressure to this for accurate depth calculation
    
    def calcTemp(self):
        """Returns current temperature in C determined by MS5803"""
        return self.MS5803.read_raw_temperature(osr=1024)

    def update(self):
        return

    def autoUpdate(self):
        return
    
    def kill(self):
        return