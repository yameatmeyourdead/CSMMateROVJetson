from adafruit_servokit import ServoKit
import board
from adafruit_motor import servo, stepper, motor

_kit = ServoKit(channels=16, i2c=board.I2C())

# THRUSTERS
THRUSTER_FRONT_LEFT = _kit._items[0] = servo.ContinuousServo(_kit._pca.channels[0])
THRUSTER_FRONT_RIGHT = _kit._items[1] = servo.ContinuousServo(_kit._pca.channels[1])
THRUSTER_BACK_LEFT = _kit._items[2] = servo.ContinuousServo(_kit._pca.channels[2])
THRUSTER_BACK_RIGHT = _kit._items[3] = servo.ContinuousServo(_kit._pca.channels[3])
THRUSTER_Z_0 = _kit._items[4] = servo.ContinuousServo(_kit._pca.channels[4])
THRUSTER_Z_1 = _kit._items[5] = servo.ContinuousServo(_kit._pca.channels[5])
THRUSTER_Z_2 = _kit._items[6] = servo.ContinuousServo(_kit._pca.channels[6])
THRUSTER_Z_3 = _kit._items[7] = servo.ContinuousServo(_kit._pca.channels[7])
THRUSTERS = {
    "THRUSTER_FRONT_LEFT": THRUSTER_FRONT_LEFT, 
    "THRUSTER_FRONT_RIGHT": THRUSTER_FRONT_RIGHT, 
    "THRUSTER_BACK_LEFT": THRUSTER_BACK_LEFT, 
    "THRUSTER_BACK_RIGHT": THRUSTER_BACK_RIGHT, 
    "THRUSTER_Z_0": THRUSTER_Z_0, 
    "THRUSTER_Z_1": THRUSTER_Z_1, 
    "THRUSTER_Z_2": THRUSTER_Z_2, 
    "THRUSTER_Z_3": THRUSTER_Z_3
}

# MANIPULATOR
MANIP_ELBOW_SERVO_2 = _kit._items[8] = servo.Servo(_kit._pca.channels[8])
MANIP_ELBOW_SERVO = _kit._items[9] = servo.Servo(_kit._pca.channels[9])
MANIP_WRIST_SERVO = _kit._items[10] = servo.Servo(_kit._pca.channels[10])
MANIP_LEVEL_SERVO = _kit._items[11] = servo.Servo(_kit._pca.channels[11])
MANIP_CLAMP_SERVO = _kit._items[12] = servo.Servo(_kit._pca.channels[12])
MANIP_SERVOS = {
    "MANIP_ELBOW_SERVO": MANIP_ELBOW_SERVO, 
    "MANIP_ELBOW_SERVO_2": MANIP_ELBOW_SERVO_2, 
    "MANIP_WRIST_SERVO": MANIP_WRIST_SERVO, 
    "MANIP_LEVEL_SERVO": MANIP_LEVEL_SERVO, 
    "MANIP_CLAMP_SERVO": MANIP_CLAMP_SERVO
}

# Manip Servo Mods (Rated pulse width) with modifications to fit our wanted sensitivity
MANIP_ELBOW_SERVO.set_pulse_width_range(500,2500)
MANIP_ELBOW_SERVO_2.set_pulse_width_range(500,2500)
MANIP_WRIST_SERVO.set_pulse_width_range(600,2400)
MANIP_LEVEL_SERVO.set_pulse_width_range(500,2500)
MANIP_CLAMP_SERVO.set_pulse_width_range(500,2500)

# Thruster Mods (Experimentally found pulse width because specs lied to us :) (1100->1900 base)) 
# (in reality its probably a library thing but i dont want to debug/rewrite servo.continuous_servo :P )
for thruster in THRUSTERS.values():
    thruster.set_pulse_width_range(1200,2000)