from time import sleep
from Component import Component
from tools import Logger
from tools import Controller
from PCA9685 import MANIP_SERVOS

# CONSTANTS


class Manip(Component):
    def __init__(self):
        # Grab the relevant servos from the map
        self.elbow_servo = MANIP_SERVOS["MANIP_ELBOW_SERVO"]
        self.elbow_servo2 = MANIP_SERVOS["MANIP_ELBOW_SERVO_2"]
        self.level_servo = MANIP_SERVOS["MANIP_LEVEL_SERVO"]
        self.wrist_servo = MANIP_SERVOS["MANIP_WRIST_SERVO"]
        self.clamp_servo = MANIP_SERVOS["MANIP_CLAMP_SERVO"]

        self.enabled = False
        self.chicken = False
        self.clamp = False
        self.elbow_angle = 90
        self.elbow_angle_old = 90
        self.wrist_angle = 90
        self.wrist_angle_old = 90
        self.level_angle = 90
        self.level_angle_old = 90

        self.elbow_tune = 11
        self.elbow_tune2 = 12
        self.level_tune = 0
        self.wrist_tune = 15

        self.x_velocity = 0
        self.y_velocity = 0

        self.VELOCITY_SCALING_FACTOR = .1 # SUBJECT TO CHANGE
        self.VELOCITY_IGNORE = .1 # Tunes how sensitive joystick is to changes
        self.ELBOW_ANGLE_MAX = 180
        self.ELBOW_ANGLE_MIN = 0
        self.LEVEL_ANGLE_MAX = 180
        self.LEVEL_ANGLE_MIN = 0
        self.WRIST_ANGLE_MAX = 180
        self.WRIST_ANGLE_MIN = 0

        self.wrist_servo.angle = 90 + self.wrist_tune
        self.elbow_servo.angle = 90 + self.elbow_tune
        self.elbow_servo2.angle = 90 + self.elbow_tune2
        self.level_servo.angle = 90 + self.level_tune
        self.clamp_servo.angle = 85
        Logger.log("MANIPULATOR CONSTRUCTED")

    def update(self) -> None:
        # get updated controller info
        presses = Controller.getButtonPresses()
        # update state
        if(presses.rs):
            self.enabled = not self.enabled
        if(not self.enabled): return # if not enabled, do nothing in update

        # Read input from joystick and map it to velocity
        poll = Controller.getLeftStick()
        self.x_velocity = poll[0]
        self.y_velocity = poll[1]

        # Disregard very target velocities (< 10%)
        if(abs(self.y_velocity) < self.VELOCITY_IGNORE):
            self.y_velocity = 0
        if(abs(self.x_velocity) < self.VELOCITY_IGNORE):
            self.x_velocity = 0

        # Determines protocol based on if auto-leveling (chicken) is desired
        # Move all but elbow
        # Else moves elbow servos
        if(self.chicken):
            self.elbow_angle = self.elbow_angle_old + self.y_velocity
            self.level_angle = self.level_angle_old - self.y_velocity
            self.wrist_angle = self.wrist_angle_old + self.x_velocity
        else:
            self.level_angle = self.level_angle_old + self.y_velocity
            self.wrist_angle = self.wrist_angle_old + self.x_velocity

        # Keeps positions from overshooting max or min angles
        if(self.elbow_angle > self.ELBOW_ANGLE_MAX):
            self.elbow_angle = self.ELBOW_ANGLE_MAX
        elif(self.elbow_angle < self.ELBOW_ANGLE_MIN):
            self.elbow_angle = self.ELBOW_ANGLE_MIN
        if(self.level_angle > self.LEVEL_ANGLE_MAX):
            self.level_angle = self.LEVEL_ANGLE_MAX
        elif(self.level_angle < self.LEVEL_ANGLE_MIN):
            self.level_angle = self.LEVEL_ANGLE_MIN
        if(self.wrist_angle > self.WRIST_ANGLE_MAX):
            self.wrist_angle = self.WRIST_ANGLE_MAX
        elif(self.wrist_angle < self.WRIST_ANGLE_MIN):
            self.wrist_angle = self.WRIST_ANGLE_MIN
        
        # Update Positions
        # Always write the wrist_servo
        self.wrist_servo.angle = self.wrist_angle + self.wrist_tune

        # Determines protocol based on if auto-leveling (chicken) is desired
        # move all
        # else move only level servo
        if(self.chicken):
            self.elbow_servo.angle = self.elbow_angle + self.elbow_tune
            self.elbow_servo2.angle = 180 - self.elbow_angle + self.elbow_tune2
            self.level_servo.angle = self.level_angle + self.level_tune
        else:
            self.level_servo.angle = self.level_angle + self.level_tune

        # Update old variables
        self.elbow_angle_old = self.elbow_angle
        self.level_angle_old = self.level_angle
        self.wrist_angle_old = self.wrist_angle

        # Update clamp position
        if(self.clamp):
            self.clamp_servo.angle = 130
        else:
            self.clamp_servo.angle = 85

        # Update Clamp
        if(presses.square):
            self.clamp = not self.clamp

        # Update chicken
        if(presses.ls):
            self.chicken = not self.chicken

    def autoUpdate(self) -> None:
        pass
    
    def kill(self) -> None:
        for servo in MANIP_SERVOS.values():
            servo.duty_cycle = 0
        Logger.log("Manipulator Servos Successfully Killed")