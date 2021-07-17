from datetime import datetime
from tools.IllegalStateException import IllegalStateException
import os
import threading

# Path to Current log
CURRENTLOG = ""

def getTime():
    """Return _ delimited 24hr time"""
    return datetime.now().strftime("%H_%M_%S")

def log(*message):
    """Log given message  
    \nPlease only log important events as log file can get quite large"""
    # allow for same functionality as print(x,y,z)
    message = " ".join(message)
    if(CURRENTLOG == ""):
        raise IllegalStateException("Attempted to use logger without first creating a log")
    with open(CURRENTLOG, 'a') as f:
        f.write(f"\n[{getTime()}] {'[' + str(threading.get_ident()) + '/' + threading.current_thread().name +']'}: " + message)

def logError(*message):
    """Log traceback"""
    message = " ".join(message)
    if(CURRENTLOG == ""):
        raise IllegalStateException("Attempted to use logger without first creating a log")
    log(f"Caught unexpected error: " + message)

def createNewLog(purge=False):
    """Create new empty log"""
    time = getTime()
    global CURRENTLOG 
    CURRENTLOG = f"./new/Logs/latest.txt"
    if(os.path.exists("./new/Logs/latest.txt") and not purge):
        with open(CURRENTLOG, 'r') as f:
            timeOfCreation = f.read()[1:9]
        os.rename("./new/Logs/latest.txt", f"./new/Logs/{timeOfCreation}.txt")
    with open(CURRENTLOG, 'w') as f:
        f.write(f"[{getTime()}] {'[' + str(threading.get_ident()) + '/' + threading.current_thread().name +']'}: " + "Created New Log")