from adafruit_servokit import ServoKit
from adafruit_motor import servo
from .Vector import Vector
from . import Controller
import math

# if you can decipher this eldritch horror of vector math I love you forever :))))

# TODO: fix bug where since joysticks are naturally bounded for r_max = 1 they do not mesh well with this implementation of Z-axis Thrust due to r_max > 1
# current workaround: do not increase velocity mod past .8
# unexpected side affect : this shifts velocity_max from velocity_mod and to some weird function im not going to attempt to find :)

# SLOW DOWN MAN
VELOCITY_MOD = .5
SQRT2 = math.sqrt(2)
SQRT05 = math.sqrt(.5)

  
THRUSTER_FRONT_LEFT_THRUST_VECTOR = Vector(SQRT2/2, SQRT2/2, 0)
THRUSTER_FRONT_RIGHT_THRUST_VECTOR = Vector(-SQRT2/2, SQRT2/2, 0)
THRUSTER_BACK_LEFT_THRUST_VECTOR = Vector(SQRT2/2, -SQRT2/2, 0)
THRUSTER_BACK_RIGHT_THRUST_VECTOR = Vector(-SQRT2/2, -SQRT2/2, 0)

THRUSTER_FRONT_LEFT_TORQUE_VECTOR = Vector(-SQRT2/2, SQRT2/2, 0).crossProduct(THRUSTER_FRONT_LEFT_THRUST_VECTOR)
THRUSTER_FRONT_RIGHT_TORQUE_VECTOR = Vector(SQRT2/2, SQRT2/2, 0).crossProduct(THRUSTER_FRONT_RIGHT_THRUST_VECTOR)
THRUSTER_BACK_LEFT_TORQUE_VECTOR = Vector(-SQRT2/2, -SQRT2/2, 0).crossProduct(THRUSTER_BACK_LEFT_THRUST_VECTOR)
THRUSTER_BACK_RIGHT_TORQUE_VECTOR = Vector(SQRT2/2, -SQRT2/2, 0).crossProduct(THRUSTER_BACK_RIGHT_THRUST_VECTOR)

THRUSTER_Z_0_THRUST_VECTOR = Vector(0, 0, 1)
THRUSTER_Z_1_THRUST_VECTOR = Vector(0, 0, 1)
THRUSTER_Z_2_THRUST_VECTOR = Vector(0, 0, 1)
THRUSTER_Z_3_THRUST_VECTOR = Vector(0, 0, 1)

THRUSTER_Z_0_TORQUE_VECTOR = Vector(-.5, .5, SQRT05).crossProduct(THRUSTER_Z_0_THRUST_VECTOR)
THRUSTER_Z_1_TORQUE_VECTOR = Vector(.5, .5, SQRT05).crossProduct(THRUSTER_Z_1_THRUST_VECTOR)
THRUSTER_Z_2_TORQUE_VECTOR = Vector(-.5, -.5, SQRT05).crossProduct(THRUSTER_Z_2_THRUST_VECTOR)
THRUSTER_Z_3_TORQUE_VECTOR = Vector(.5, -.5, SQRT05).crossProduct(THRUSTER_Z_3_THRUST_VECTOR)

THRUSTER_FRONT_LEFT_THRUST_VECTOR = Vector(SQRT2/2, SQRT2/2, 0)
THRUSTER_FRONT_RIGHT_THRUST_VECTOR = Vector(-SQRT2/2, SQRT2/2, 0)
THRUSTER_BACK_LEFT_THRUST_VECTOR = Vector(SQRT2/2, -SQRT2/2, 0)
THRUSTER_BACK_RIGHT_THRUST_VECTOR = Vector(-SQRT2/2, -SQRT2/2, 0)

def start(debug=False):
    print("3 Axis Drive / Rotation Script Started")
    kit = ServoKit(channels=16)

    turn = False
    zup = False
    zdown = False

    # creating all of the thrusters
    THRUSTER_FRONT_LEFT = kit._items[0] = servo.ContinuousServo(kit._pca.channels[0])
    THRUSTER_FRONT_RIGHT = kit._items[1] = servo.ContinuousServo(kit._pca.channels[1])
    THRUSTER_BACK_LEFT = kit._items[2] = servo.ContinuousServo(kit._pca.channels[2])
    THRUSTER_BACK_RIGHT = kit._items[3] = servo.ContinuousServo(kit._pca.channels[3])
    # THRUSTER_Z_0 = kit._items[4] = servo.ContinuousServo(kit._pca.channels[4])
    # THRUSTER_Z_1 = kit._items[5] = servo.ContinuousServo(kit._pca.channels[5])
    # THRUSTER_Z_2 = kit._items[6] = servo.ContinuousServo(kit._pca.channels[6])
    # THRUSTER_Z_3 = kit._items[7] = servo.ContinuousServo(kit._pca.channels[7])
    THRUSTER_FRONT_LEFT.set_pulse_width_range(1200,2000)
    THRUSTER_FRONT_RIGHT.set_pulse_width_range(1200,2000)
    THRUSTER_BACK_LEFT.set_pulse_width_range(1200,2000)
    THRUSTER_BACK_RIGHT.set_pulse_width_range(1200,2000)
    # THRUSTER_Z_0.set_pulse_width_range(1200,2000)
    # THRUSTER_Z_1.set_pulse_width_range(1200,2000)
    # THRUSTER_Z_2.set_pulse_width_range(1200,2000)
    # THRUSTER_Z_3.set_pulse_width_range(1200,2000)

    while True:
        # poll the controller
        Controller.updateController()
        presses = Controller.getButtonPresses()
        RS = Controller.getRightStick()
        targetTorque = Vector()
        targetTranslation = Vector()
        targetThrottles = [0 for i in range(8)]

        if(presses.rs):
            turn = not turn

        # Translation
        if(not turn):
            # Set target x,y
            targetTranslation = Vector(RS[0], RS[1], 0)

            # Ignore small values (without this we would get unwanted torques)
            if(abs(targetTranslation.getX()) < .1):
                targetTranslation.setX(0)
            if(abs(targetTranslation.getY()) < .1):
                targetTranslation.setY(0)

            if(debug):
                pass
                # print(f"Translation Target = {targetTranslation}")
            
            # TODO: consider changing this to slave thrusters together (kinda hard with this implementation)
            targetThrottles[0] = THRUSTER_FRONT_LEFT_THRUST_VECTOR.dotProduct(targetTranslation)
            targetThrottles[1] = THRUSTER_FRONT_RIGHT_THRUST_VECTOR.dotProduct(targetTranslation)
            targetThrottles[2] = THRUSTER_BACK_LEFT_THRUST_VECTOR.dotProduct(targetTranslation)
            targetThrottles[3] = THRUSTER_BACK_RIGHT_THRUST_VECTOR.dotProduct(targetTranslation)
        # Turning
        else:
            # set X
            targetTorque.setX(RS[0])
            # set Y
            targetTorque.setY(RS[1])
            # set Z TODO: change this shitty implementation (create 3 axis joystick out of two joysticks???)
            if(presses.dup):
                zdown = False
                zup = not zup
            if(presses.ddown):
                zup = False
                zdown = not zdown
            if(zup):
                targetTorque.setZ(SQRT05)
            if(zdown):
                targetTorque.setZ(-SQRT05)
                
            
            # Ignore small values (without this we would get unwanted torques)
            if(abs(targetTorque.getX()) < .1):
                targetTorque.setX(0)
            if(abs(targetTorque.getY()) < .1):
                targetTorque.setY(0)

            if(debug):
                print(f"Torque Target = {targetTorque}")

            # Explanation incoming.....
            # Each thruster has a specific thruster torque (torque created on COM if only that thruster was activated) defined as r cross F where F is their thrust vector
            # In order to get the throttle, you must dot this torque vector with the target Torque vector to see how much their torque vector acts upon the target torque vector
            # This should return maximum of 1 and minimum of -1 (float inaccuracies make it slightly different so we must check it is within [-1,1]
            targetThrottles[0] = (THRUSTER_FRONT_LEFT_TORQUE_VECTOR.dotProduct(targetTorque))
            targetThrottles[1] = (THRUSTER_FRONT_RIGHT_TORQUE_VECTOR.dotProduct(targetTorque))
            targetThrottles[2] = (THRUSTER_BACK_LEFT_TORQUE_VECTOR.dotProduct(targetTorque))
            targetThrottles[3] = (THRUSTER_BACK_RIGHT_TORQUE_VECTOR.dotProduct(targetTorque))
            # targetThrottles[4] = (THRUSTER_Z_0_TORQUE_VECTOR.dotProduct(targetTorque))
            # targetThrottles[5] = (THRUSTER_Z_1_TORQUE_VECTOR.dotProduct(targetTorque))
            # targetThrottles[6] = (THRUSTER_Z_2_TORQUE_VECTOR.dotProduct(targetTorque))
            # targetThrottles[7] = (THRUSTER_Z_3_TORQUE_VECTOR.dotProduct(targetTorque))

        # Check for incorrect throttle values
        for throttleValue in targetThrottles:
            if(throttleValue > 1):
                throttleValue = 1
            elif(throttleValue < -1):
                throttleValue = -1
            throttleValue *= VELOCITY_MOD
        
        # always write thrusters (defaults are 0)
        for Thruster in range(4):
            kit._items[Thruster].throttle = targetThrottles[Thruster]

        # if(debug):
        #     # shouldnt really have to ever uncomment this one (these values shouldnt change once set)
        #     # print(f"""
        #     #     Torque Vectors: 
        #     #     Front Left:     {THRUSTER_FRONT_LEFT_TORQUE_VECTOR.toString()}
        #     #     Front Right:    {THRUSTER_FRONT_RIGHT_TORQUE_VECTOR.toString()}
        #     #     Back Left:      {THRUSTER_BACK_LEFT_TORQUE_VECTOR.toString()}
        #     #     Back Right:     {THRUSTER_BACK_RIGHT_TORQUE_VECTOR.toString()} 
        #     #     Z0:             {THRUSTER_Z_0_TORQUE_VECTOR.toString()}
        #     #     Z1:             {THRUSTER_Z_1_TORQUE_VECTOR.toString()}
        #     #     Z2:             {THRUSTER_Z_2_TORQUE_VECTOR.toString()}
        #     #     Z3:             {THRUSTER_Z_3_TORQUE_VECTOR.toString()}
        #     #     """)

            print(f"""
                Throttles:
                Front Left:     {targetThrottles[0]}
                Front Right:    {targetThrottles[1]}
                Back Left:      {targetThrottles[2]}
                Back Right:     {targetThrottles[3]}""")
                # Z0:             {targetThrottles[4]}
        #         Z1:             {targetThrottles[5]}
        #         Z2:             {targetThrottles[6]}
        #         Z3:             {targetThrottles[7]}
        #         """)