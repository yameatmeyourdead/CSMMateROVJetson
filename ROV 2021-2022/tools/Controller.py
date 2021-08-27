from typing import Tuple
from approxeng.input.selectbinder import ControllerResource
from approxeng.input import ButtonPresses

def getLeftStick() -> Tuple[float, float]:
    """
    Returns tuple of type int,int ranging from -1 to 1  \n
    -> (x, y)
    """
    return JOYSTICK.l

def getRightStick() -> Tuple[float, float]:
    """
    Returns tuple of type int,int ranging from -1 to 1  \n
    -> (x, y)
    """
    return JOYSTICK.r

def getLeftTrigger() -> float:
    """
    Returns current value from -1 to 1  \n
    """
    return JOYSTICK.lt

def getRightTrigger() -> float:
    """
    Returns current value from -1 to 1  \n
    """
    return JOYSTICK.rt

def getLeftBumper() -> bool:
    """
    Returns 1 if pressed else 0  \n
    """
    return JOYSTICK.l1

def getRightBumper() -> bool:
    """
    Returns 1 if pressed else 0  \n
    """
    return JOYSTICK.r1

def getDPad() -> Tuple[bool, bool, bool, bool]:
    """
    Returns list of DPad states indexed as follows  \n
    -> (dleft, dup, dright, ddown)  \n
    val = 1 if pressed else 0  
    """
    buttonStates = getButtonPresses()
    return (buttonStates.dleft, buttonStates.dup, buttonStates.dright, buttonStates.ddown)

def updateController() -> None:
    """Updates controller. Call at most once per main loop"""
    JOYSTICK.check_presses()

def getButtonPresses() -> ButtonPresses:
    """
    Returns object of all buttons with properties as follows \n 
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
    To determine if one of these buttons is currently pressed, use .held(standard name) \n
    returns none if not held otherwise number of seconds held
    """
    return JOYSTICK.presses

# Constructor creates singleton instance of joystick
JOYSTICK = ControllerResource().__enter__()