from Components.PCA9685 import THRUSTERS
from enum import Enum
from tools import Logger, Controller
from tools.IllegalStateException import IllegalStateException
from tools.Vectors import Vector3f
from Component import Component
from math import sqrt

# defines state of drive
class State(Enum):
        translation = 0
        rotation = 1

# constants
SQRT2 = sqrt(2)
SQRT0_5 = sqrt(.5)

CONTROLLER_DEADZONE = .1

# azimuth plane thruster vectors
THRUSTER_FRONT_LEFT_THRUST_VECTOR = Vector3f(-SQRT2/2, -SQRT2/2, 0)
THRUSTER_FRONT_RIGHT_THRUST_VECTOR = Vector3f(SQRT2/2, -SQRT2/2, 0)
THRUSTER_BACK_LEFT_THRUST_VECTOR = Vector3f(-SQRT2/2, SQRT2/2, 0)
THRUSTER_BACK_RIGHT_THRUST_VECTOR = Vector3f(SQRT2/2, SQRT2/2, 0)

THRUSTER_FRONT_LEFT_TORQUE_VECTOR = Vector3f.cross(Vector3f(-SQRT2/2, SQRT2/2, 0), THRUSTER_FRONT_LEFT_THRUST_VECTOR)
THRUSTER_FRONT_RIGHT_TORQUE_VECTOR = Vector3f.cross(Vector3f(SQRT2/2, SQRT2/2, 0), THRUSTER_FRONT_RIGHT_THRUST_VECTOR)
THRUSTER_BACK_LEFT_TORQUE_VECTOR = Vector3f.cross(Vector3f(-SQRT2/2, -SQRT2/2, 0), THRUSTER_BACK_LEFT_THRUST_VECTOR)
THRUSTER_BACK_RIGHT_TORQUE_VECTOR = Vector3f.cross(Vector3f(SQRT2/2, -SQRT2/2, 0), THRUSTER_BACK_RIGHT_THRUST_VECTOR)

# elevation thruster vectors
THRUSTER_Z_0_THRUST_VECTOR = Vector3f(0, 0, 1)
THRUSTER_Z_1_THRUST_VECTOR = Vector3f(0, 0, 1)
THRUSTER_Z_2_THRUST_VECTOR = Vector3f(0, 0, 1)
THRUSTER_Z_3_THRUST_VECTOR = Vector3f(0, 0, 1)

THRUSTER_Z_0_TORQUE_VECTOR = Vector3f.cross(Vector3f(-.5, .5, SQRT0_5), THRUSTER_Z_0_THRUST_VECTOR)
THRUSTER_Z_1_TORQUE_VECTOR = Vector3f.cross(Vector3f(.5, .5, SQRT0_5), THRUSTER_Z_1_THRUST_VECTOR)
THRUSTER_Z_2_TORQUE_VECTOR = Vector3f.cross(Vector3f(-.5, -.5, SQRT0_5), THRUSTER_Z_2_THRUST_VECTOR)
THRUSTER_Z_3_TORQUE_VECTOR = Vector3f.cross(Vector3f(.5, -.5, SQRT0_5), THRUSTER_Z_3_THRUST_VECTOR)

class Drive(Component):
    def __init__(self, debug=False):
        # set variable defaults
        self.debug = debug
        self.velocity_mod = 1
        self.state = State.translation
        self.idle = False
        self.trgt_velocity = Vector3f()
        self.trgt_angular_velocity = Vector3f()
        self.thruster_events = [0 for x in range(8)] # list of events for indexed thruster (TODO: proper indexes TBD)
        Logger.log("Drive Constructed")

    def setSpeedLimit(self, limit) -> None:
        if(limit > 1):
            self.velocity_mod = 1
            return
        self.velocity_mod = limit

    def update(self) -> None:
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
        
        # if left stick was pressed, toggle drive state
        if(presses.ls):
            # if state is idle, do not update on left stick press
            if(not self.idle):
                self.state = State(not self.last_state.value)
        # if right stick was pressed, toggle drive/manipulator defaults to drive being on and manipulator being off
        if(presses.rs):
            self.idle = not self.idle

        # depending upon drive state, update drive accordingly
        # always set target velocity and target torque to 0
        self.trgt_velocity.setComponents((0,0,0))
        self.trgt_angular_velocity.setComponents((0,0,0))
        if(self.state == State.translation):
            self.trgt_velocity.setComponents((LS[0],LS[1],RS[1])) # set target velocity to corresponding stick values
            if(self.debug):
                print(self.trgt_velocity)
            # TODO: get error in velocity from IMU
            # velocity_error = self.trgt_velocity - IMU.getTranslationalVelocity()
        elif(self.state == State.rotation):
            self.trgt_angular_velocity.setComponents((LS[1],LS[0],RS[0])) # set target torque to intuitive stick values
            if(self.debug):
                print(self.trgt_angular_velocity)
            # TODO: get error in angular velocity from IMU
            # angular_velocity_error = self.trgt_angular_velocity - IMU.getAngularVelocity()
        else:
            raise IllegalStateException("Drive is in undefined state")
    
    def autoUpdate(self) -> None:
        raise NotImplementedError()
        # if(self.state == State.translation):
        #     pass
        # elif(self.state == State.rotation):
        #     pass
        # else:
        #     raise IllegalStateException("Drive is in undefined state")
    
    def kill(self) -> None:
        for thruster in THRUSTERS.values():
            thruster.throttle = 0
        Logger.log("Drive Thrusters Successfully Killed")