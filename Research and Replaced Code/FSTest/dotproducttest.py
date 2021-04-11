from adafruit_servokit import ServoKit
from adafruit_motor import servo
from .Vector import Vector
from . import Controller

SQRT2 = 1.4142136

def start():
    kit = ServoKit(channels=16)

    THRUSTER_FRONT_LEFT = kit._items[0] = servo.ContinuousServo(kit._pca.channels[0])
    THRUSTER_FRONT_LEFT_THRUST_VECTOR = Vector(SQRT2/2, SQRT2/2, 0)

    while True:
        print("Input target velocity")
        target = Vector(input("X> "), input("Y> "), input("Z> "))
        throttle = THRUSTER_FRONT_LEFT_THRUST_VECTOR.dotProduct(target)
        print(throttle)