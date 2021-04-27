from time import sleep
import busio
import board
import adafruit_lsm9ds1

i2c = busio.I2C(board.SCL, board.SDA)
NineAxisSensor = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)


while True:
    print(f"Acceleration (m/s^2): {NineAxisSensor.acceleration}")
    print(f"Magnetometer (gauss): {NineAxisSensor.magnetic}")
    print(f"Gyro (deg/sec): {NineAxisSensor.gyro}")
    sleep(.5)