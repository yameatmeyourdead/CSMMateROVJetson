from .Drive import Drive
from .Manip import Manip
from .MicroROV import MicroROV
from .Logger import Logger
from . import ROVMap
import sys
import os
import time
import traceback
from threading import Thread
from pynput import keyboard
from pynput.keyboard import Listener, Key

# Creation of EStop Exception and its Fatal counterpart (Fatal EStop completely shuts down computer)
class EStopInterruptFatal(Exception): args: True 
class EStopInterrupt(Exception): args: False



class ROV:
    parts = [] # Component list for ease of looping in autoOp/teleOp function
    operatingMode = True # Operate in Autonomous or TeleOp? True = TeleOp, False = Auto

    # Create Logger
    logger = Logger()

    def __init__(self):
        with self.parts as parts:
            # Creation of parts
            # Drive thrusters
            parts.append(Drive())
            # Manipulator(s)
            parts.append(Manip())
            # MicroROV
            parts.append(MicroROV())

    # Defining stop method (Includes E Stop functionality through FATAL bool)
    def stop(self, FATAL = False):
        # Calmly deactivate all components
        for Comp in self.parts:
            Comp.kill()
        # If EStop was triggered, shutdown Jetson immediately
        if(FATAL):
            print("Triggering system shutdown due to EStop")
            #os.system('shutdown /s /t 1')

    # TODO: IMPLEMENT
    # .
    # .
    # Key listener (used for interrupts that arent ctrl+c)
    # def on_press(key):
    #     if(key == Key.enter):
    #         raise EStopInterruptFatal
    #     if(key == Key.space):
    #         raise EStopInterrupt

    # # Setup keyboard listener for EStop
    # def KeyListener():
    #     try:
    #         with Listener(on_press=on_press, on_release=None) as listener:
    #             listener.join()
    #     except(EStopInterruptFatal, EStopInterrupt) as e:
    #         # Adding traceback to file in ./Logs/ directory before deciding if to force shutdown
    #         SYSTIME = time.gmtime(time.time())
    #         SYSTIME = str(SYSTIME.tm_mday) + "_" + str(SYSTIME.tm_hour) + "_" + str(SYSTIME.tm_min) + "_" + str(SYSTIME.tm_sec) + "_Traceback"
    #         f = open("ROV/Logs/" + f"{SYSTIME}" + ".txt", "w")
    #         f.write(traceback.format_exc())
    #         f.close()

    #         # Shutdown NOW (if needed)
    #         stop(e.args)

    def start(self):
        # TODO CONSIDER ADDING TICKRATE HERE?????
        while True:
            # Update each component of the robot depending on the operating mode
            if(self.operatingMode):
                for Comp in self.parts:
                    Comp.Update()
            else:
                for Comp in self.parts:
                    Comp.autoUpdate()

    try:
        # TODO: IMPLEMENT??? (Or am I just being stupid?)
        # Thread for keyboard listener (EStop etc)
        # keyboardThread = Thread(target=KeyListener)
        # keyboardThread.start()

        # Thread for actually doing things
        # functionalThread = Thread(target = start)
        # functionalThread.start()
        start()
    # If keyboard interrupt, shut down every single part
    except (KeyboardInterrupt):
        stop()