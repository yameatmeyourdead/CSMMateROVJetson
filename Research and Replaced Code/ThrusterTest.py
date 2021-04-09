from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)

kit.continuous_servo[0].set_pulse_width_range(1100,1900)

go = True

while True:
    kit.continuous_servo[0].throttle = float(input("Throttle?"))