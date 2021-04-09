from adafruit_servokit import ServoKit
from adafruit_motor import servo

# initialize pca9685
kit = ServoKit(channels=16)


# declare motor esc as continuous servo because it expects servo like PWM input
kit.continuous_servo[0].set_pulse_width_range(1100,1900)
ESC = servo.ContinuousServo(kit._items[0])



# allow myself to control it
while True:
    ESC._pwm_out = int(input("PWM OUT> "))