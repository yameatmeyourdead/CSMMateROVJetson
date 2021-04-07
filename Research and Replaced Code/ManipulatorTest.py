from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)

kit.servo[4].set_pulse_width_range(500,2500)
# kit.servo[5].set_pulse_width_range(500,2500)
kit.servo[6].set_pulse_width_range(500,2500)
kit.servo[7].set_pulse_width_range(500,2500)

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



elbow_servo = kit.servo[4]
level_servo = kit.servo[7]
wrist_servo = kit.servo[6]

elbow_servo.angle = 90
level_servo.angle = 90
wrist_servo.angle = 90

while True:
    angle1 = int(input("Elbow : "))
    angle2 = int(input("Level : "))
    angle3 = int(input("Wrist : "))

    elbow_servo.angle = angle1
    level_servo.angle = angle2
    wrist_servo.angle = angle3