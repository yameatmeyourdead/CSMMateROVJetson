from adafruit_servokit import ServoKit
from adafruit_motor import servo

# initialize pca9685
kit = ServoKit(channels=16)


# declare motor esc as continuous servo because it expects servo like PWM input
kit._items[0] = servo.ContinuousServo(kit._pca.channels[0])
ESC = kit._items[0]
ESC.set_pulse_width_range(1200,1900)

# allow myself to control it
while True:
    ESC.throttle = float(input("OUT> "))