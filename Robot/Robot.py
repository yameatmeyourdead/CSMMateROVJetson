import os
from threading import Thread, Lock
from pynput.keyboard import Listener, Key

# Creation of EStop Exception
class EStopInterrupt(Exception): args: True

parts = [] # Component list for ease of looping in autoOp/teleOp function
operatingMode = True # Operate in Autonomous or TeleOp? True = TeleOp, False = Auto

# Filling components
# parts.append() ...



# Defining stop method (Includes E Stop functionality through SHUTDOWN bool)
def stop(SHUTDOWN = False):
    for Comp in parts:
        Comp.kill()
    # If EStop was triggered, shutdown Jetson immediately
    if(SHUTDOWN):
        print("Triggering system shutdown due to EStop")
        #os.system('shutdown /s /t 1')
    pass

# Key listener
def on_press(key):
    if(key == 'q'):
        raise EStopInterrupt

# Setup keyboard listener for EStop
def KeyListener():
    with Listener() as listener:
        listener.join()

t = Thread(target=KeyListener)
t.start()

try:
    # TODO CONSIDER ADDING TICKRATE HERE?????
    while True:
        # Update each component of the robot depending on the operating mode
        if(operatingMode):
            for Comp in parts:
                Comp.Update()
            print("Hello from update")
        else:
            for Comp in parts:
                Comp.autoUpdate()
# If keyboard interrupt, shut down every single part
except (KeyboardInterrupt, EStopInterrupt) as e:
    stop(e.args)
    

