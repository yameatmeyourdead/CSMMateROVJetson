from adafruit_platformdetect.board import Board
from adafruit_servokit import ServoKit
import busio
import adafruit_pca9685
from adafruit_motor import motor
import board

i2c = busio.I2C(board.SCL, board.SDA)
pca = adafruit_pca9685.PCA9685(i2c, address=0x40)
pca.frequency=300

pca.channels[0].duty_cycle = 0xFFFF

motor1 = motor.DCMotor(1900,1100)

motor1.throttle = 0



# # initialize pca9685
# kit = ServoKit(channels=16)

# # declare motor esc as continuous servo because it expects servo like PWM input
# kit.continuous_servo[0].set_pulse_width_range(1100,1900)

# # allow myself to control it
# while True:
#     kit.continuous_servo[0].throttle = float(input("Throttle?"))