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

class ThrusterConfiguration:
    def __init__(self, size) -> None:
        super().__init__()
        assert(size != 0), "Thruster Configuration cannot have 0 thrusters"
        self.size = size
        self.thrusters:List["Thruster"] = [None for i in range(size)]

    @classmethod
    def fromThrusters(cls, *args:"Thruster") -> "ThrusterConfiguration":
        toRet = cls(len(args))
        for thruster in args:
            toRet.thrusters[thruster.ID] = thruster
        return toRet
    
    @classmethod
    def fromConfigFile(cls, path="data/DefaultThrusterConfig.dat") -> "ThrusterConfiguration":
        with open(path, 'r') as f:
            rep = loads(''.join(f.readlines()).replace('\n', '')) # get data from file and get dictionary representation
    
    def toConfigFile(self, path="data/DefaultThrusterConfig.dat") -> None:
        thrusterRep = {"thrusters":[]}
        for thruster in self.thrusters:
            thrusterRep["thrusters"].append(thruster.toDict())
        with open(path, 'w') as f:
            f.write(dumps(thrusterRep, sort_keys=True, indent=4))

    def getSize(self) -> int:
        return self.size
    
    def killAllThrusters(self):
        for thruster in self.thrusters:
            thruster.kill()

    def __getitem__(self, item) -> Any:
        return self.thrusters[item]
    
    def __setitem__(self, item, val) -> None:
        self.thrusters[item] = val

class Thruster:
    def __init__(self, ID:int, vectors:Tuple[Vector3f, Vector3f]=None, thrustVector:Vector3f=None, positionVector:Vector3f=None) -> None:
        self.ID = ID # ID of thruster (corresponds to PWM Out on PCA9685)
        # Create PWM object from ID
        PCA9685._kit._items[ID] = PCA9685.servo.ContinuousServo(PCA9685._kit._pca.channels[ID])
        PCA9685._kit._items[ID].set_pulse_width_range(1200,2000)
        self.thrusterPWM = PCA9685._kit._items[ID]

        # store/calculate important vectors
        if(vectors is not None):
            positionVector = vectors[0]
            thrustVector = vectors[1]

        self.thrustVector = thrustVector
        self.positionVector = positionVector
        self.torqueVector = Vector3f.cross(self.positionVector, self.thrustVector) # no need to calculate this multiple times, just do it once
    
    @classmethod
    def fromString(cls, string):
        components = loads(string)
        return cls(components["ID"], components["thrustVector"], components["positionVector"])

    def kill(self):
        self.thrusterPWM.throttle = 0

    def __str__(self):
        return f'{{\n\t"ID":{self.ID},\n\t"thrustVector":{self.thrustVector},\n\t"positionVector":{self.positionVector}\n}}'
    
    def toDict(self):
        return {"ID":self.ID, "thrustVector":str(self.thrustVector), "positionVector":str(self.positionVector)}


class Drive(Component):
    def __init__(self, thrusterConfiguration=ThrusterConfiguration.fromConfigFile(), debug=False):
        # set variable defaults
        self.debug = debug
        self.velocity_mod = 1
        self.idle = False
        self.thrusterConfiguration:"ThrusterConfiguration" = thrusterConfiguration
        self.trgt_velocity = Vector3f()
        self.trgt_angular_velocity = Vector3f()
        self.thruster_events = [0 for x in range(8)] # list of events for indexed thruster
        self.now = 0
        self.last = time.time_ns() / 1000000 # TODO: this does not ensure startup PID spike is removed (it should help but not by much)
        Logger.log("Drive Constructed")

    def setSpeedLimit(self, limit) -> None:
        if(limit > 1):
            self.velocity_mod = 1
            return
        self.velocity_mod = limit

    def update(self) -> None:
        self.now = time.time_ns() / 1000000 # get time in ms
        # get controller's presses/stick positions
        presses = Controller.getButtonPresses()
        LS = Controller.getLeftStick()
        RS = Controller.getRightStick()

        # set deadzone
        if(LS[0] < CONTROLLER_DEADZONE):
            LS[0] = 0
        if(LS[1] < CONTROLLER_DEADZONE):
            LS[1] = 0
        if(RS[0] < CONTROLLER_DEADZONE):
            RS[0] = 0
        if(RS[1] < CONTROLLER_DEADZONE):
            RS[1] = 0

        # TODO: IMPLEMENT PID
    
    def autoUpdate(self) -> None:
        raise NotImplementedError()
        # if(self.state == State.translation):
        #     pass
        # elif(self.state == State.rotation):
        #     pass
        # else:
        #     raise IllegalStateException("Drive is in undefined state")
    
    def kill(self) -> None:
        self.thrusterConfiguration.killAllThrusters()
        Logger.log("Drive Thrusters Successfully Killed")


