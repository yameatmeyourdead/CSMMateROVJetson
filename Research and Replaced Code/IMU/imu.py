from time import sleep
import busio
import board
import adafruit_lsm9ds1

i2c = busio.I2C(board.SCL, board.SDA)
NineAxisSensor = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)


while True:
    accel_x, accel_y, accel_z = NineAxisSensor.acceleration
    mag_x, mag_y, mag_z = NineAxisSensor.magnetic
    gyro_x, gyro_y, gyro_z = NineAxisSensor.gyro

    print(f"Acceleration (m/s^2): {accel_x}, {accel_y}, {accel_z}")
    print(f"Magnetometer (gauss): {mag_x}, {mag_y}, {mag_z}")
    print(f"Gyro (deg/sec): {gyro_x}, {gyro_y}, {gyro_z}")
    sleep(.5)