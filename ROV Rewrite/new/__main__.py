from typing import List
from Components.Component import Component
from Components.Drive import Drive
from Components.Manipulator import Manipulator
from tools import Logger, Controller
from tools.IllegalStateException import IllegalStateException
from tools.network import Client, Server
from enum import Enum
from traceback import format_exc
import time

# Debug Tools
purgeLogs = True

# Stores state of ROV
class State(Enum):
    teleop = 0
    auto = 1
    idle = -1

# define new list of components
components: List[Component] = list()

def initialize():
    """Initialize all relevant robot components/tools here"""
    Logger.createNewLog(purgeLogs)
    Client.startClient()
    Server.startServer()
    # initialize all components here
    components.append(Drive())
    components.append(Manipulator())
    Logger.log("Components initialized")

# Start Robot
initialize()
try:
    # Define initial state
    STATE = State.idle
    last = time.time()
    while True:
        # place update methods for things that should be updated at idle here
        Controller.updateController()
        if(STATE == State.idle):
            # when idle, continue doing nothing
            continue

        # when not idle, decide what to do
        for component in components:
            if(STATE == State.teleop):
                component.update()
            elif(STATE == State.auto):
                component.autoUpdate()
            else:
                raise IllegalStateException("Robot state is undefined")
except:
    # Log Exception (removes \n from the end)
    Logger.logError(format_exc()[0:-1])
finally:
    Logger.log("Killing Components")
    for component in components:
        component.kill()