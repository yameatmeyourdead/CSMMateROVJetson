import time
import os

# =======================
# =======================
# =======================
# =======================

# LOGGER IMPLEMENTATION

def log(strin, endO="\n"):
    """
    Call this method to log something  \n
    Compatible with all data types capable of conversion to str through str(value)
    """
    strin = '[' + getTimeFormatted(':') + '] ' + str(strin) + endO
    with open(LOGGER_FILE_PATH, 'a') as f:
        f.write(strin)

def getTimeFormatted(delim):
    """
    Get current system time formatted with given delimiter \n
    -> Hour\delim\Min\delim\Sec
    """
    SYSTIME = time.localtime(time.time())
    return (str(SYSTIME.tm_hour) + delim + str(SYSTIME.tm_min) + delim + str(SYSTIME.tm_sec))

# Constructor creates file object named f
currentTime = getTimeFormatted('_')
LOGGER_FILE_PATH = f"DriverStation/Logs/{currentTime}.txt"
if(os.path.exists(LOGGER_FILE_PATH)):
    os.remove(LOGGER_FILE_PATH)
with open("DriverStation/Logs/" + f"{currentTime}" + ".txt", "w") as f:
    f.write(f"[{currentTime}] Logger Created")

# =======================
# =======================
# =======================
# =======================