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

def updatePresses():
    joystick.check_presses()

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
    updatePresses()
    return joystick.presses



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
x_velocity_tune = 0 # Tunes zeros of joystick
y_velocity = 0
y_velocity_tune = 0 # Tunes zeros of joystick
global_velocity = 90

slow = 200 # Slows speed of manipulator

# Want to wait some time before shizzle starts to move?
# sleep(3)

def Update():
    # Read input from joystick and map it to velocity
    x_velocity = (getLeftStick()[0]+1)/2*180
    y_velocity = (getLeftStick()[1]+1)/2*180

    # Disregard very low velocities (< 10% max)
    if(y_velocity >= -(global_velocity/10) and y_velocity <= (global_velocity/10)):
        y_velocity = 0
    if(x_velocity >= -(global_velocity/10) and x_velocity <= (global_velocity/10)):
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

    # Keeps velocities from overshooting 0 or 180 deg
    if(elbow_angle >= 180):
        elbow_angle = 180
    elif(elbow_angle <= 0):
        elbow_angle = 0

    if(level_angle >= 140):
        level_angle = 140
    elif(level_angle <= 20):
        level_angle = 20

    if(wrist_angle >= 180):
        wrist_angle = 180
    elif(wrist_angle <= 0):
        wrist_angle = 0
        
    # Update old variables
    elbow_angle_old = elbow_angle
    level_angle_old = level_angle
    wrist_angle_old = wrist_angle

    # Update chicken
    updatePresses()
    button_new = getButtonPresses().ls

    if(button_new):
        if(chicken):
            chicken = 0
        else:
            chicken = 1
        
    print("Manipulator Update")

    # (DEBUG)
    print("Elbow :", elbow_angle, "\nWrist :", wrist_angle, "\nLevel :", level_angle)


while True:
    Update()