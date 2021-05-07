import os
import time

def log(data, endO="\n"):
    """
    Call this method to log something  \n
    Compatible with all data types capable of conversion to str
    """
    strin = '[' + getTimeFormatted(':') + '] ' + str(data) + endO
    with open(LOGGER_FILE_PATH, 'a') as f:
        f.write(strin)

def getTimeFormatted(delim):
    """
    Get current system time formatted with given delimiter \n
    -> Hour\delim\Min\delim\Sec
    """
    SYSTIME = time.localtime(time.time())
    return (str(SYSTIME.tm_hour) + delim + str(SYSTIME.tm_min) + delim + str(SYSTIME.tm_sec))

currentTime = getTimeFormatted(':')

LOGGER_FILE_PATH = "./Logs/latest.txt"
if(os.path.exists(LOGGER_FILE_PATH)):
    if(os.path.exists("./Logs/last.txt")):
        os.remove("./Logs/last.txt")
    os.rename(LOGGER_FILE_PATH, "./Logs/last.txt")
with open(LOGGER_FILE_PATH, 'w') as f:
    f.write(f"[{currentTime}] Logger Created\n")