from time import sleep
from .Component import Component
from . import ROVMap

class Manip(Component):
    def __init__(self):
        # Grab the relevant servos from the map
        self.elbow_servo = ROVMap.kit.servo[ROVMap.PCA9685PINOUT["ELBOW_SERVO"]]
        self.elbow_servo2 = ROVMap.kit.servo[ROVMap.PCA9685PINOUT["ELBOW_SERVO_2"]]
        self.level_servo = ROVMap.kit.servo[ROVMap.PCA9685PINOUT["LEVEL_SERVO"]]
        self.wrist_servo = ROVMap.kit.servo[ROVMap.PCA9685PINOUT["WRIST_SERVO"]]

        self.chicken = 0
        self.elbow_angle = 90       # deg
        self.elbow_angle_old = 90   # deg
        self.wrist_angle = 90       # deg
        self.wrist_angle_old = 90   # deg
        self.level_angle = 90       # deg
        self.level_angle_old = 90   # deg

        self.button_new = 1
        self.button_old = 1

        self.elbow_tune = 0     # deg
        self.elbow_tune2 = 0    # deg
        self.level_tune = 10    # deg
        self.wrist_tune = 10    # deg

        self.x_velocity = 0
        self.x_velocity_tune = 2 # Tunes zeros of joystick
        self.y_velocity = 0
        self.y_velocity_tune = -3 # Tunes zeros of joystick
        self.global_velocity = 90

        self.slow = 200 # Slows speed of manipulator

        # starting position of the manipulator
        self.elbow_servo.angle = self.elbow_angle + self.elbow_tune
        self.level_servo.angle = 180 - self.elbow_angle + self.level_tune
        self.wrist_servo.angle = self.wrist_angle + self.wrist_tune

        # Want to wait some time before shizzle starts to move?
        # sleep(3)

        Manip.logEvent("MANIPULATOR CONSTRUCTED")

    def Update(self):
        # Read input from joystick and map it to velocity
        self.x_velocity = map(ROVMap.getLeftStick[0], -1, 1, -self.global_velocity, self.global_velocity)
        self.y_velocity = map(ROVMap.getLeftStick[1], -1, 1, self.global_velocity, -self.global_velocity)

        # Disregard very low velocities (< 10% max)
        if(self.y_velocity >= -(self.global_velocity/10) and self.y_velocity <= (self.global_velocity/10)):
            self.y_velocity = 0
        if(self.x_velocity >= -(self.global_velocity/10) and self.x_velocity <= (self.global_velocity/10)):
            self.x_velocity = 0
        
        # TODO: Check this logic still works. I switched the 0 and 1 cases so i didnt have to type ==
        # Determines protocol based on if auto-leveling (chicken) is desired
        # Move all but elbow
        # Else moves elbow servos
        if(self.chicken):
            self.elbow_angle = self.elbow_angle_old + self.y_velocity / self.slow
            self.level_angle = self.level_angle_old - self.y_velocity / self.slow
            self.wrist_angle = self.wrist_angle_old + self.x_velocity / self.slow
        else:
            self.level_angle = self.level_angle_old + self.y_velocity / self.slow
            self.wrist_angle = self.wrist_angle_old + self.x_velocity / self.slow

        # Keeps velocities from overshooting 0 or 180 deg
        # TODO: Ensure logic still works. Changed every other if to else if
        if(self.elbow_angle >= 180):
            self.elbow_angle = 180
        elif(self.elbow_angle <= 0):
            self.elbow_angle = 0

        if(self.level_angle >= 140):
            self.level_angle = 140
        elif(self.level_angle <= 20):
            self.level_angle = 20

        if(self.wrist_angle >= 180):
            self.wrist_angle = 180
        elif(self.wrist_angle <= 0):
            self.wrist_angle = 0

        # Always write the wrist_servo
        self.wrist_servo.angle = self.wrist_angle + self.wrist_tune

        # TODO: Check this logic still works
        # Determines protocol based on if auto-leveling (chicken) is desired
        # Move only level servo
        # Else move all
        if(self.chicken):
            self.elbow_servo.angle = self.elbow_angle + self.elbow_tune
            self.elbow_servo2.angle = 180 - self.elbow_angle + self.elbow_tune
            self.level_servo.angle = self.level_angle + self.level_tune
        else:
            self.level_servo.angle = self.level_angle + self.level_tune
            
        # Update old variables
        self.elbow_angle_old = self.elbow_angle
        self.level_angle_old = self.level_angle
        self.wrist_angle_old = self.wrist_angle

        # Update chicken
        ROVMap.updatePresses()
        self.button_new = ROVMap.getButtonPresses().ls

        # TODO: GET DEVON TO LOOK AT THIS (do we need button_old??) due to implementation of getButtonPresses() it should only return 1 if it has been pressed since last check
        if(self.button_new):
            if(self.chicken):
                self.chicken = 0
            else:
                self.chicken = 1
            
        print("Manipulator Update")

        # (DEBUG)
        # print("Elbow :", self.elbow_angle, "\nWrist :", self.wrist_angle, "\nLevel :", self.level_angle)

        # TODO: implement LED?????? (super easy just make a pin in ROVMap.PCA9685PINOUT map to an LED and change its pulse width accordingly)


    def autoUpdate(self):
        print("Manipulator autoUpdate")
    
    def kill(self):
        print("Manipulator received kill command")

    def logEvent(string):
        ROVMap.log(string)