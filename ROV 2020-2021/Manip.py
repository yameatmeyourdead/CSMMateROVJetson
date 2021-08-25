from time import sleep
from .Component import Component
from . import ROVMap

class Manip(Component):
    def __init__(self):
        # Grab the relevant servos from the map
        self.elbow_servo = ROVMap.MANIP_ELBOW_SERVO
        # TODO: IMPLEMENT
        self.elbow_servo2 = ROVMap.MANIP_ELBOW_SERVO_2
        self.level_servo = ROVMap.MANIP_LEVEL_SERVO
        self.wrist_servo = ROVMap.MANIP_WRIST_SERVO
        # TODO: IMPLEMENT
        self.clamp_servo = ROVMap.MANIP_CLAMP_SERVO

        self.chicken = False
        self.clamp = False
        self.elbow_angle = 90       # deg
        self.elbow_angle_old = 90   # deg
        self.wrist_angle = 90       # deg
        self.wrist_angle_old = 90   # deg
        self.level_angle = 90       # deg
        self.level_angle_old = 90   # deg

        self.elbow_tune = 11     # deg
        self.elbow_tune2 = 12    # deg
        self.level_tune = 0    # deg
        self.wrist_tune = 15    # deg

        self.x_velocity = 0
        self.y_velocity = 0

        self.VELOCITY_SCALING_FACTOR = .1 # SUBJECT TO CHANGE
        self.DELTA_VELOCITY_IGNORE = .1 # Tunes how sensitive joystick is to changes
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
        ROVMap.log("MANIPULATOR CONSTRUCTED")

    def Update(self):
        # Read input from joystick and map it to velocity
        poll = ROVMap.getLeftStick()
        self.x_velocity = (poll[0])
        self.y_velocity = (poll[1])

        # Disregard very low delta target velocities (< 10%)
        if(abs(self.y_velocity) < self.DELTA_VELOCITY_IGNORE):
            self.y_velocity = 0
        else:
            self.y_velocity *= self.VELOCITY_SCALING_FACTOR
        if(abs(self.x_velocity) < self.DELTA_VELOCITY_IGNORE):
            self.x_velocity = 0
        else:
            self.x_velocity *= self.DELTA_VELOCITY_IGNORE

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
        if(ROVMap.getButtonPresses().square):
            self.clamp = not self.clamp

        # Update chicken
        if(ROVMap.getButtonPresses().ls):
            self.chicken = not self.chicken # Note: changed this implementation it MAY break things

    def autoUpdate(self):
        print("Manipulator autoUpdate")
    
    def kill(self):
        for servo in ROVMap.MANIP_SERVOS:
            servo.duty_cycle = 0
        ROVMap.log("Manipulator Servos Successfully Killed")