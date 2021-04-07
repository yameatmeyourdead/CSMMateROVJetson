from adafruit_servokit import ServoKit

# kit = ServoKit(channels=16)

# kit.servo[4].set_pulse_width_range(500,2500)
# kit.servo[5].set_pulse_width_range(500,2500)
# kit.servo[6].set_pulse_width_range(500,2500)
# kit.servo[7].set_pulse_width_range(500,2500)

from approxeng.input.selectbinder import ControllerResource
    
def getLeftStick():
    """
    Returns tuple of type int,int ranging from -1 to 1  \n
    -> (x, y)
    """
    return joystick.l

def getRightStick():
    """
    Returns tuple of type int,int ranging from -1 to 1  \n
    -> (x, y)
    """
    return joystick.r

def getLeftTrigger():
    """
    Returns current value from -1 to 1  \n
    """
    return joystick.lt

def getRightTrigger():
    """
    Returns current value from -1 to 1  \n
    """
    return joystick.rt

def getLeftBumper():
    """
    Returns 1 if pressed else 0  \n
    """
    return joystick.l1

def getRightBumper():
    """
    Returns 1 if pressed else 0  \n
    """
    return joystick.r1

def getDPad():
    """
    Returns list of DPad states indexed as follows  \n
    -> (dleft, dup, dright, ddown)  \n
    val = 1 if pressed else 0  
    """
    buttonStates = getButtonPresses()
    return [buttonStates.dleft, buttonStates.dup, buttonStates.dright, buttonStates.ddown]

def getButtonPresses():
    """
    Returns object of all buttons indexed as follows \n 
    INTUITIVE NAME  ->  STANDARD NAME\n
    x->                 .square     \n
    y->                 .triangle   \n
    b->                 .circle     \n
    a->                 .cross      \n
    Left Stick->        .ls         \n
    Right Stick->       .rs         \n
    View->              .select     \n
    Menu->              .start      \n
    XBox->              .home       \n
    DLeft->             .dleft      \n
    DUp->               .dup        \n
    DRight->            .dright     \n
    DDown->             .ddown      \n
    LBTrigger->         .l1         \n
    LTTrigger->         .l2         \n
    RBTrigger->         .r1         \n
    RTTrigger->         .r2         \n
    To determine if one of these buttons are pressed, use .held(standard name) \n
    returns none if not held otherwise number of seconds held
    """
    return joystick.check_presses()



# Constructor creates instance of joystick
joystick = ControllerResource().__enter__()

chicken = 0
elbow_angle = 90       # deg
elbow_angle_old = 90   # deg
wrist_angle = 90       # deg
wrist_angle_old = 90   # deg
level_angle = 90       # deg
level_angle_old = 90   # deg

button_new = 1

elbow_tune = 0     # deg
elbow_tune2 = 0    # deg
level_tune = 0    # deg
wrist_tune = 0    # deg

x_velocity = 0
x_velocity_old = 0
x_velocity_tune = 0 # Tunes zeros of joystick
y_velocity = 0
y_velocity_old = 0
y_velocity_tune = 0 # Tunes zeros of joystick
global_velocity = 90

DELTA_VELOCITY_IGNORE = .075 # Tunes how sensitive joystick is to changes
VELOCITY_SCALING_FACTOR = .25
ELBOW_ANGLE_MAX = 180
ELBOW_ANGLE_MIN = 0
LEVEL_ANGLE_MAX = 180
LEVEL_ANGLE_MIN = 0
WRIST_ANGLE_MAX = 180
WRIST_ANGLE_MIN = 0

slow = 200 # Slows speed of manipulator

# Want to wait some time before shizzle starts to move?
# sleep(3)

while True:
    # Read input from joystick and map it to velocity
    x_velocity = (getLeftStick()[0]) * VELOCITY_SCALING_FACTOR
    y_velocity = (getLeftStick()[1]) * VELOCITY_SCALING_FACTOR

    # Disregard very low delta target velocities (< 10%)
    if(abs(y_velocity) < DELTA_VELOCITY_IGNORE):
        y_velocity = 0
    if(abs(x_velocity) < DELTA_VELOCITY_IGNORE):
        x_velocity = 0

    
    # Determines protocol based on if auto-leveling (chicken) is desired
    # Move all but elbow
    # Else moves elbow servos
    if(chicken):
        elbow_angle = elbow_angle_old + y_velocity
        level_angle = level_angle_old - y_velocity
        wrist_angle = wrist_angle_old + x_velocity
    else:
        level_angle = level_angle_old + y_velocity
        wrist_angle = wrist_angle_old + x_velocity

    # Keeps positions from overshooting max or min angles
    if(elbow_angle > ELBOW_ANGLE_MAX):
        elbow_angle = ELBOW_ANGLE_MAX
    elif(elbow_angle < ELBOW_ANGLE_MIN):
        elbow_angle = ELBOW_ANGLE_MIN
    if(level_angle > LEVEL_ANGLE_MAX):
        level_angle = LEVEL_ANGLE_MAX
    elif(level_angle < LEVEL_ANGLE_MIN):
        level_angle = LEVEL_ANGLE_MIN
    if(wrist_angle > WRIST_ANGLE_MAX):
        wrist_angle = WRIST_ANGLE_MAX
    elif(wrist_angle < WRIST_ANGLE_MIN):
        wrist_angle = WRIST_ANGLE_MIN
    
    # Update Positions

    # # Always write the wrist_servo
    # self.wrist_servo.angle = self.wrist_angle + self.wrist_tune

    # # Determines protocol based on if auto-leveling (chicken) is desired
    # # Move only level servo
    # # Else move all
    # if(self.chicken):
    #     self.elbow_servo.angle = self.elbow_angle + self.elbow_tune
    #     # self.elbow_servo2.angle = 180 - self.elbow_angle + self.elbow_tune
    #     self.level_servo.angle = self.level_angle + self.level_tune
    # else:
    #     self.level_servo.angle = self.level_angle + self.level_tune

    # Update old variables
    elbow_angle_old = elbow_angle
    level_angle_old = level_angle
    wrist_angle_old = wrist_angle
    x_velocity_old = x_velocity
    y_velocity_old = y_velocity

    # Update chicken
    button_new = getButtonPresses().ls

    if(button_new):
        if(chicken):
            chicken = 0
        else:
            chicken = 1

    # (DEBUG)
    print("Elbow :", elbow_angle)
    # print("Wrist :", wrist_angle)
    # print("Level :", level_angle)
    if(button_new):
        print("PRESSED")