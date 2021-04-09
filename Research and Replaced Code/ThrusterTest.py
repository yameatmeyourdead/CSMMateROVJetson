from adafruit_motor.servo import ContinuousServo
from adafruit_servokit import ServoKit
from . import Controller

kit = ServoKit(channels=16)

kit.continuous_servo[0].set_pulse_width_range(1100,1900)

go = True

while True:
    input("Toggle")
    if(go):
        kit.continuous_servo[0].throttle = .25
        go = False
    else:
        kit.continuous_servo[0].throttle = 0.0
        go = True