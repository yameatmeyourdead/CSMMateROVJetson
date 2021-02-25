from . import ROVMap
from . import Logger
import os
import sys
import time
import traceback
import trace
from threading import Thread
from pynput import keyboard
from pynput.keyboard import Listener, Key

# Creation of EStop Exception and its Fatal counterpart (Fatal EStop completely shuts down computer)
class EStopInterruptFatal(Exception): args: True 
class EStopInterrupt(Exception): args: False


parts = [] # Component list for ease of looping in autoOp/teleOp function
operatingMode = True # Operate in Autonomous or TeleOp? True = TeleOp, False = Auto

# Filling components
# parts.append() ...
test = ROVMap.PCA9685PINOUT["FRONT_LEFT_THRUSTER_ESC"]

# Defining stop method (Includes E Stop functionality through FATAL bool)
def stop(FATAL = False):
    print("STOP COMMAND RECEIVED.....STOPPING")
    LOGGER.log("Stop Command Received")
    if(FATAL):
        print("Triggering system shutdown due to EStopFatal")
        # os.system('shutdown /s /t 1')
    # Calmly deactivate all components
    for Comp in parts:
        Comp.kill()
    # If EStop was triggered, shutdown Jetson immediately
    

# Key listener (used for interrupts that arent ctrl+c)
def on_press(key):
    if(key == Key.enter):
        try:
            raise EStopInterruptFatal
        except(EStopInterruptFatal) as e:
            stop(e.args)

    if(key == Key.space):
        try:
            raise EStopInterrupt
        except(EStopInterrupt) as e:
            stop(e.args)
    

# Setup keyboard listener for EStop
def KeyListener():
    with Listener(on_press=on_press, on_release=None) as listener:
        listener.join()
    
def startRobot():
    # TODO CONSIDER ADDING TICKRATE HERE?????
    while True:
        # Update each component of the robot depending on the operating mode
        if(operatingMode):
            for Comp in parts:
                Comp.Update()
        else:
            for Comp in parts:
                Comp.autoUpdate()

try:
    LOGGER = Logger()

     # Thread for actually doing things
    functionalThread = Thread(target=startRobot)
    functionalThread.start()

    # Thread for keyboard listener (EStop etc)
    keyboardThread = Thread(target=KeyListener)
    keyboardThread.start()

    keyboardThread.join()
    functionalThread.join()
# If keyboard interrupt, shut down every single part
except (KeyboardInterrupt):
    stop()