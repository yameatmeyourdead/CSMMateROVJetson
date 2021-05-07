from .Component import Component
from . import ROVMap
from time import sleep
import serial

class MicroROV(Component):
    def __init__(self):
        self.__COMPORT = serial.Serial(port=ROVMap.MICROROVCOMPORT, baudrate=9600, write_timeout=0.05) # timeout is is seconds
        self.__clamp = False # set clamp to be open by default
        ROVMap.log("MICROROV CONSTRUCTED")

    # 0x84 0x00 0x70 0x2E
    # set target 0 to 1500
    # 0x84 set target command
    # 0x00 is device
    # 0x70 and 0x2E target in quarter-microseconds 1500*4 & 7F and 1500*4 >> 7 & 7F, respectively :)
    def Update(self):
        def generateCommands(channel, target):
            """sets specific servo to target microseconds"""
            # change from microseconds to quarter microseconds
            target = target*4
            # fancy bit math time
            try:
                self.__COMPORT.write(b"\x84" + channel.to_bytes(length=1, byteorder='big') + (target & 0x7F).to_bytes(length=1, byteorder='big') + (target >> 7 & 0x7F).to_bytes(length=1, byteorder='big')) # write the command to the COMPORT (BLOCKING)
            except(serial.SerialTimeoutException, serial.PortNotOpenError) as e:
                if(isinstance(e, serial.SerialTimeoutException)):
                    ROVMap.log("MicroROV COM Port Write Timeout Occurred")
                else:
                    ROVMap.log("Attempted to write to closed port. Did you kill the MicroROV Object?")
        
        # grab newest copy of button presses
        presses = ROVMap.getButtonPresses()
        # if button has been pressed, update functions accordingly
        if(presses.a):
            self.__clamp = not self.__clamp
        
        # Map specific servo channels to updated targets. command will only be generated if not none (set to None every update) note: 5 maximum servo devices
        targets = {0:None, 1:None, 2:None, 3:None, 4:None, 5:None}
        
        if(self.__clamp):
            targets[0] = 2500
        else:
            targets[0] = 0

        # generate updated commands as necessary (and check limits on servos)
        for channel in targets:
            target = targets[channel]
            if(target is None):
                continue
            # limit test
            if(target > 2500):
                target = 2500
            elif(target < 500):
                target = 500
            generateCommands(channel, target)
    
    def autoUpdate(self):
        print("MicroROV autoUpdate")
    
    def kill(self):
        self.__COMPORT.cancel_write()
        self.__COMPORT.close()
        print("MicroROV received kill command")

if __name__ == "__main__":
    microrov = MicroROV()
    
    microrov.Update()