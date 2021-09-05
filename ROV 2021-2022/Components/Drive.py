import Components.PCA9685 as PCA9685
from enum import Enum
from tools import Logger, Controller
from tools.IllegalStateException import IllegalStateException
from tools.Vectors import Vector3f
from Components.Component import Component
import time
from json import loads, dumps
from math import sqrt
from typing import Any, Dict, List, Tuple
from tools.Vectors import Vector3f

CONTROLLER_DEADZONE = .1

# azimuth plane thruster vectors
# metadata as (position, thrust)
THRUSTER_FRONT_LEFT_META = (Vector3f(), Vector3f(sqrt(2)/2, -sqrt(2)/2, 0))
THRUSTER_FRONT_RIGHT_META = (Vector3f(), Vector3f(sqrt(2)/2, sqrt(2)/2, 0))
THRUSTER_BACK_RIGHT_META = (Vector3f(), Vector3f(-sqrt(2)/2, sqrt(2)/2, 0))
THRUSTER_BACK_LEFT_META = (Vector3f(), Vector3f(-sqrt(2)/2, -sqrt(2)/2, 0))

# elevation thruster vectors
THRUSTER_Z0_META = (Vector3f(), Vector3f(0, 0, 1))
THRUSTER_Z1_META = (Vector3f(), Vector3f(0, 0, 1))
THRUSTER_Z2_META = (Vector3f(), Vector3f(0, 0, 1))
THRUSTER_Z3_META = (Vector3f(), Vector3f(0, 0, 1))

# function to define expected thrust given a throttle
def expectedThrust(throttle):
    return 3.68 * (throttle) * (throttle) * (throttle) + 0.839 * (throttle) * (throttle) + 2.5(throttle) - .0186

# function to simplify getting time in ms
def time_ms():
    return time.time_ns() / 1000000

class ThrusterConfiguration:
    def __init__(self, size) -> None:
        super().__init__()
        assert(size != 0), "Thruster Configuration cannot have 0 thrusters"
        self._size = size
        self._thrusters:List["Thruster"] = [None for i in range(size)]

    @classmethod
    def fromThrusters(cls, *args:"Thruster") -> "ThrusterConfiguration":
        toRet = cls(len(args))
        for thruster in args:
            toRet._thrusters[thruster.ID] = thruster
        return toRet
    
    @classmethod
    def fromConfigFile(cls, path="data/DefaultThrusterConfig.dat") -> "ThrusterConfiguration":
        with open(path, 'r') as f:
            rep = loads(''.join(f.readlines()).replace('\n', '')) # get data from file and get dictionary representation
        return cls.fromThrusters(rep["thrusters"])
    
    def toConfigFile(self, path="data/DefaultThrusterConfig.dat") -> None:
        thrusterRep = {"thrusters":[]}
        for thruster in self._thrusters:
            thrusterRep["thrusters"].append(thruster.toDict())
        with open(path, 'w') as f:
            f.write(dumps(thrusterRep, sort_keys=True, indent=4))

    def getSize(self) -> int:
        return self._size
    
    def setThrusterThrottle(self, thruster, throttle) -> None:
        self[thruster].throttle = throttle
    
    def getThrusters(self) -> List["Thruster"]:
        return self._thrusters

    def killAllThrusters(self) -> None:
        for thruster in self._thrusters:
            thruster.kill()

    def __getitem__(self, item) -> Any:
        return self._thrusters[item]
    
    def __setitem__(self, item, val) -> None:
        self._thrusters[item] = val

class Thruster:
    def __init__(self, ID:int, vectors:Tuple[Vector3f, Vector3f]=None, thrustVector:Vector3f=None, positionVector:Vector3f=None) -> None:
        self.ID = ID # ID of thruster (corresponds to PWM Out on PCA9685)

        # Create PWM object from ID
        PCA9685._kit._items[ID] = PCA9685.servo.ContinuousServo(PCA9685._kit._pca.channels[ID])
        PCA9685._kit._items[ID].set_pulse_width_range(1200,2000) # should be 1100,1900 but it dont work properly like that
        self.thrusterPWM:PCA9685.servo.ContinuousServo = PCA9685._kit._items[ID]

        # store/calculate important vectors
        if(vectors is not None):
            positionVector = vectors[0]
            thrustVector = vectors[1]

        self.thrustUnitVector = thrustVector.toUnitVector()
        self.positionVector = positionVector
        self.torqueUnitVector = Vector3f.cross(self.positionVector, self.thrustUnitVector).toUnitVector() # no need to calculate this multiple times, just do it once
    
    @classmethod
    def fromString(cls, string):
        components = loads(string)
        return cls(components["ID"], components["thrustVector"], components["positionVector"])

    def kill(self) -> None:
        self.thrusterPWM.throttle = 0

    def __str__(self):
        return f'{{\n\t"ID":{self.ID},\n\t"thrustVector":{self.thrustUnitVector},\n\t"positionVector":{self.positionVector}\n}}'
    
    def toDict(self):
        return {"ID":self.ID, "thrustVector":str(self.thrustUnitVector), "positionVector":str(self.positionVector)}

G = 9.81

class Drive(Component):
    def __init__(self, thrusterConfiguration=ThrusterConfiguration.fromConfigFile(), debug=False) -> None:
        self.started = False
        self.killed = False

        self.debug = debug
        self.thrusterConfiguration:"ThrusterConfiguration" = thrusterConfiguration

        self.linear_position = Vector3f()
        self.angular_position = Vector3f()
        self.linear_velocity = Vector3f()
        self.angular_velocity = Vector3f()
        self.moment_of_inertia = Vector3f()

        self.mass = 0 # TODO: GET MASS ESTIMATE

        self.setPointTranslation = Vector3f()
        self.setPointRotation = Vector3f()

        self.KP = 0
        self.KI = 0
        self.KD = 0

        self.error = Vector3f() # desired - actual
        self.error_last = Vector3f() # used for derivative: (error-error_last)/dt
        self.error_accumulated = Vector3f() # used for integral: error_accumulated += error * dt

        self.t = 0.0
        self.t_last = 0.0
    
    def control_thrust(self):
        f = Vector3f()
        for thruster in self.thrusterConfiguration.getThrusters():
            f += Vector3f.fromMagnitudeAndDirection(expectedThrust(thruster.thrusterPWM.throttle), thruster.thrustUnitVector)
        return f

    def control_torque(self):
        # calculate torque applied about COM due to speed of all thrusters
        t = Vector3f()
        for thruster in self.thrusterConfiguration.getThrusters():
            t += Vector3f.fromMagnitudeAndDirection(expectedThrust(thruster.thrusterPWM.throttle), thruster.torqueUnitVector)
        return t


    def start(self):
        assert(self.started == False), "Cannot start PID; it is already started"
        self.started = True
        self.t_last = time_ms()

    def update(self):
        if(self.killed or not self.started):
            return
        self.t = time_ms()
        dt = self.t - self.t_last
        
        # update control signals here
    
    def autoUpdate(self):
        self.update()
    
    def kill(self):
        self.thrusterConfiguration.killAllThrusters()