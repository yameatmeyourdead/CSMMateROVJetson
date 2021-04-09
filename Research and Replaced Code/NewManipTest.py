from adafruit_platformdetect.board import Board
from adafruit_servokit import ServoKit
import busio
import adafruit_pca9685
from adafruit_motor import motor
import board

i2c = busio.I2C(board.SCL, board.SDA)
pca = adafruit_pca9685.PCA9685(i2c, address=0x40)
pca.frequency=300

servo1 = pca.channels[4]

servo1.duty_cycle = 0x7fff

while True:
    servo1.duty_cycle = int(input("VAL> "), 16)