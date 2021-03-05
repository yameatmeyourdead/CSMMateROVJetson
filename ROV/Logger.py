import time

# Use this class for all logging needs. Instance of Logger has already been created -> main -> logger variable
class Logger:
    # Constructor creates global file object named f
    def __init__():
        global f
        time = Logger.getTimeFormatted('_')
        f = open("Robot/Logs/" + f"{time}" + ".txt", "w")

    # Call this method to log something compatible with all data types capable of conversion to str through str()
    def log(strin):
        f.write('[' + Logger.getTimeFormatted(':') + '] ' + str(strin))

    def getTimeFormatted(delim):
        SYSTIME = time.gmtime(time.time())
        return (str(SYSTIME.tm_hour) + delim + str(SYSTIME.tm_min) + delim + str(SYSTIME.tm_sec))
    
    def finishLog():
        f.close()