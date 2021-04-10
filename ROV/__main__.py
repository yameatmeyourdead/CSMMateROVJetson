from .Drive import Drive
from .Manip import Manip
from .MicroROV import MicroROV
from . import ROVMap
import sys
import os
import time
import traceback
from multiprocessing import Process, set_start_method

parts = [] # Component list for ease of looping in autoOp/teleOp function
operatingMode = True # Operate in Autonomous or TeleOp? True = TeleOp, False = Auto

# Creation of parts
# Drive thrusters
parts.append(Drive())
# Manipulator(s)
parts.append(Manip())
# MicroROV
parts.append(MicroROV())

ROVMap.log("All parts constructed")

# Defining stop method (Includes E Stop functionality through FATAL bool)
def stop(FATAL = False):
    """
    Stop the robot. Contains Capability for auto-shutdown of computer\n
    WARNING: IF TESTING THIS FATAL FUNCTIONALITY, IT WILL SHUTDOWN YOUR COMPUTER... YOU HAVE BEEN WARNED\n
    usage: stop(FATAL) Fatal=False by default
    """
    ROVMap.log(f"Received Stop Command.....Fatal? => {FATAL}")
    # Calmly deactivate all components
    ROVMap.joystick.__exit__()
    for Comp in parts:
        Comp.kill()
    # If EStop Fatal was triggered, shutdown Jetson immediately
    if(FATAL):
        ROVMap.log("Triggering system shutdown due to EStop", endO="")
        os.system('shutdown /s /t 1')
    ROVMap.log("ROV Successfully Shutdown", endO="")


def eStopListener():
    ROVMap.startNetworkListener()


def start():
    """
    Start the Robot\n
    
    """
    while True:
        # Update each component of the robot depending on the operating mode
        if(operatingMode):
            # Teleop
            for Comp in parts:
                Comp.Update()
        else:
            # Autonomous
            for Comp in parts:
                Comp.autoUpdate()

# Creates two processes, one for keyboard stop/estop and one for actually doing robo
try:
    # try:
    #     set_start_method('spawn', force=True)
    # except RuntimeError:
    #     pass

    if __name__ == "__main__":
        # Process for keyboard listener (EStop etc)
        # EStopListener = Process(target=ROVMap.recvPacket)
        # EStopListener.start()
        
        # Thread for actually running robo code
        functionalProcess = Process(target=start)
        functionalProcess.start()
# If keyboard interrupt, shut down every single part
except (KeyboardInterrupt, ROVMap.EStopInterrupt, ROVMap.EStopInterruptFatal) as e:
    ROVMap.log("Received Keyboard Interrupt.....Stopping")
    stop(e.args)
    