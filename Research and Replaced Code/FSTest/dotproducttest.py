from adafruit_servokit import ServoKit
from adafruit_motor import servo
from .Vector import Vector
from . import Controller

SQRT2 = 1.4142136

def start():
    kit = ServoKit(channels=16)

    VELOCITY_MOD = .75
    
    THRUSTER_FRONT_LEFT = kit._items[0] = servo.ContinuousServo(kit._pca.channels[0])
    THRUSTER_FRONT_LEFT_THRUST_VECTOR = Vector(SQRT2/2, SQRT2/2, 0)
    THRUSTER_FRONT_RIGHT = kit._items[1] = servo.ContinuousServo(kit._pca.channels[1])
    THRUSTER_FRONT_RIGHT_THRUST_VECTOR = Vector(SQRT2/2, -SQRT2/2, 0)
    THRUSTER_FRONT_LEFT.set_pulse_width_range(1200,2000)
    THRUSTER_FRONT_RIGHT.set_pulse_width_range(1200,2000)
    while True:
        poll = Controller.getRightStick()
        target = Vector(poll[0], poll[1], 0)
        print(target.toString())
        THRUSTER_FRONT_LEFT.throttle = -THRUSTER_FRONT_LEFT_THRUST_VECTOR.dotProduct(target) * VELOCITY_MOD
        THRUSTER_FRONT_RIGHT.throttle = THRUSTER_FRONT_RIGHT_THRUST_VECTOR.dotProduct(target) * VELOCITY_MOD