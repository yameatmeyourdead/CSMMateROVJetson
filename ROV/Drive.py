from .Component import Component
from . import ROVMap

class Drive(Component):
    def __init__(self):
        # if you can decipher this eldritch horror of vector math I love you forever :))))

        # TODO: fix bug where since joysticks are naturally bounded for r_max = 1 they do not mesh well with this implementation of Z-axis Thrust due to r_max > 1
        # current workaround: do not increase velocity mod past .8
        # unexpected side affect : this shifts velocity_max from velocity_mod and to some weird function im not going to attempt to find :)

        # should we allow turning / going up / going down
        self._turn = False
        self._zup = False
        self._zdown = False

        # physical thruster objects (continuous servo-like pwm devices)
        self._THRUSTER_FRONT_LEFT = ROVMap.THRUSTER_FRONT_LEFT
        self._THRUSTER_FRONT_RIGHT = ROVMap.THRUSTER_FRONT_RIGHT
        self._THRUSTER_BACK_LEFT = ROVMap.THRUSTER_BACK_LEFT
        self._THRUSTER_BACK_RIGHT = ROVMap.THRUSTER_BACK_RIGHT
        self._THRUSTER_Z_0 = ROVMap.THRUSTER_Z_0
        self._THRUSTER_Z_1 = ROVMap.THRUSTER_Z_1
        self._THRUSTER_Z_2 = ROVMap.THRUSTER_Z_2
        self._THRUSTER_Z_3 = ROVMap.THRUSTER_Z_3
        
        # azimuthal thruster vectors
        self._THRUSTER_FRONT_LEFT_THRUST_VECTOR = ROVMap.THRUSTER_FRONT_LEFT_THRUST_VECTOR
        self._THRUSTER_FRONT_RIGHT_THRUST_VECTOR = ROVMap.THRUSTER_FRONT_RIGHT_THRUST_VECTOR
        self._THRUSTER_BACK_LEFT_THRUST_VECTOR = ROVMap.THRUSTER_BACK_LEFT_THRUST_VECTOR
        self._THRUSTER_BACK_RIGHT_THRUST_VECTOR = ROVMap.THRUSTER_BACK_RIGHT_THRUST_VECTOR
        self._THRUSTER_FRONT_LEFT_TORQUE_VECTOR = ROVMap.THRUSTER_FRONT_LEFT_TORQUE_VECTOR
        self._THRUSTER_FRONT_RIGHT_TORQUE_VECTOR = ROVMap.THRUSTER_FRONT_RIGHT_TORQUE_VECTOR
        self._THRUSTER_BACK_LEFT_TORQUE_VECTOR = ROVMap.THRUSTER_BACK_LEFT_TORQUE_VECTOR
        self._THRUSTER_BACK_RIGHT_TORQUE_VECTOR = ROVMap.THRUSTER_BACK_RIGHT_TORQUE_VECTOR

        # elevation thruster vectors
        self._THRUSTER_Z_0_THRUST_VECTOR = ROVMap.THRUSTER_Z_0_THRUST_VECTOR
        self._THRUSTER_Z_1_THRUST_VECTOR = ROVMap.THRUSTER_Z_1_THRUST_VECTOR
        self._THRUSTER_Z_2_THRUST_VECTOR = ROVMap.THRUSTER_Z_2_THRUST_VECTOR
        self._THRUSTER_Z_3_THRUST_VECTOR = ROVMap.THRUSTER_Z_3_THRUST_VECTOR
        self._THRUSTER_Z_0_TORQUE_VECTOR = ROVMap.THRUSTER_Z_0_TORQUE_VECTOR
        self._THRUSTER_Z_1_TORQUE_VECTOR = ROVMap.THRUSTER_Z_1_TORQUE_VECTOR
        self._THRUSTER_Z_2_TORQUE_VECTOR = ROVMap.THRUSTER_Z_2_TORQUE_VECTOR
        self._THRUSTER_Z_3_TORQUE_VECTOR = ROVMap.THRUSTER_Z_3_TORQUE_VECTOR

        # initial values of vectors/throttles
        self._targetTorque = ROVMap.Vector()
        self._targetTranslation = ROVMap.Vector()
        self._targetThrottles = [0 for i in range(8)]
        
        # self.thruster_power_draw = 0
        # self.thruster_current_draw = 0

        ROVMap.log("DRIVE CONSTRUCTED")
    
    def Update(self):
        RS = ROVMap.getRightStick()
        presses = ROVMap.getButtonPresses()
        self._targetThrottles = [0, 0, 0, 0, 0, 0, 0, 0] # always reset throttles to 0

        # Toggle Between Turning/Translation
        if(presses.rs):
            self._zdown = False
            self._zup = False
            self._turn = not self._turn

        # Translation
        if(not self._turn):
            # Set target x,y,z
            _targetTranslation = ROVMap.Vector(RS[0], RS[1], 0)
            if(presses.dup):
                self._zdown = False
                self._zup = not self._zup
            elif(presses.ddown):
                self._zup = False
                self._zdown = not self._zdown
            if(self._zup):
                _targetTranslation.setZ(ROVMap.SQRT05)
            elif(self._zdown):
                _targetTranslation.setZ(-ROVMap.SQRT05)

            # Ignore small values (without this we would get unwanted torques)
            if(abs(_targetTranslation.getX()) < .1):
                _targetTranslation.setX(0)
            if(abs(_targetTranslation.getY()) < .1):
                _targetTranslation.setY(0)
            
            # TODO: consider changing this to slave thrusters together (kinda hard with this implementation)
            self._targetThrottles[1] = self._THRUSTER_FRONT_RIGHT_THRUST_VECTOR.dotProduct(_targetTranslation)
            self._targetThrottles[0] = self._THRUSTER_FRONT_LEFT_THRUST_VECTOR.dotProduct(_targetTranslation)
            self._targetThrottles[2] = self._THRUSTER_BACK_LEFT_THRUST_VECTOR.dotProduct(_targetTranslation)
            self._targetThrottles[3] = self._THRUSTER_BACK_RIGHT_THRUST_VECTOR.dotProduct(_targetTranslation)
            self._targetThrottles[4] = self._THRUSTER_Z_0_THRUST_VECTOR.dotProduct(_targetTranslation)
            self._targetThrottles[5] = self._THRUSTER_Z_1_THRUST_VECTOR.dotProduct(_targetTranslation)
            self._targetThrottles[6] = self._THRUSTER_Z_2_THRUST_VECTOR.dotProduct(_targetTranslation)
            self._targetThrottles[7] = self._THRUSTER_Z_3_THRUST_VECTOR.dotProduct(_targetTranslation)
        # Turning
        else:
            # set X,Y
            self._targetTorque.setXYZ((RS[0],RS[1],0))
            # set Z TODO: change this shitty implementation (create 3 axis joystick out of two joysticks???)
            if(presses.dup):
                self._zdown = False
                self._zup = not self._zup
            if(presses.ddown):
                self._zup = False
                self._zdown = not self._zdown
            if(self._zup):
                self._targetTorque.setZ(ROVMap.SQRT05)
            if(self._zdown):
                self._targetTorque.setZ(-ROVMap.SQRT05)
                
            # Ignore small values (without this we would get unwanted torques)
            if(abs(self._targetTorque.getX()) < .1):
                self._targetTorque.setX(0)
            if(abs(self._targetTorque.getY()) < .1):
                self._targetTorque.setY(0)

            # Explanation incoming.....
            # Each thruster has a specific thruster torque (torque created on COM if only that thruster was activated) defined as r cross F where F is their thrust vector
            # In order to get the throttle, you must dot this torque vector with the target Torque vector to see how much their torque vector acts upon the target torque vector
            # This should return maximum of 1 and minimum of -1 (float inaccuracies make it slightly different so we must check it is within [-1,1]
            self._targetThrottles[0] = (self._THRUSTER_FRONT_LEFT_TORQUE_VECTOR.dotProduct(self._targetTorque))
            self._targetThrottles[1] = (self._THRUSTER_FRONT_RIGHT_TORQUE_VECTOR.dotProduct(self._targetTorque))
            self._targetThrottles[2] = (self._THRUSTER_BACK_LEFT_TORQUE_VECTOR.dotProduct(self._targetTorque))
            self._targetThrottles[3] = (self._THRUSTER_BACK_RIGHT_TORQUE_VECTOR.dotProduct(self._targetTorque))
            self._targetThrottles[4] = (self._THRUSTER_Z_0_TORQUE_VECTOR.dotProduct(self._targetTorque))
            self._targetThrottles[5] = (self._THRUSTER_Z_1_TORQUE_VECTOR.dotProduct(self._targetTorque))
            self._targetThrottles[6] = (self._THRUSTER_Z_2_TORQUE_VECTOR.dotProduct(self._targetTorque))
            self._targetThrottles[7] = (self._THRUSTER_Z_3_TORQUE_VECTOR.dotProduct(self._targetTorque))

        # Check for incorrect throttle values (ensure we do not try to set |throttle| >1)
        for throttleValue in self._targetThrottles:
            if(throttleValue > 1):
                throttleValue = 1
            elif(throttleValue < -1):
                throttleValue = -1
            throttleValue *= ROVMap.VELOCITY_MOD # scale velocity
        
        # always write thrusters (defaults are 0)
        # update estimated power and current draw as well
        # throttle * throttle decently faster than throttle ** 2
        # estimated_current = [0, 0, 0, 0, 0, 0, 0, 0]
        # estimated_power_draw = 0
        for Thruster in range(8):
            # NOTE: calculated power draw and current replaced by physical monitoring
            # throttle = self._targetThrottles[Thruster]
            # estimated_power_draw += (-7.96 - .0434 * throttle + 209 * throttle * throttle)
            # estimated_current[Thruster] = (-.664 -.0036 * throttle + 17.4 * throttle * throttle)
            # if(ROVMap.kit._items[Thruster] is not None): # ensure thruster object exists (shouldn't be needed unless testing less than 8 thrusters)
            ROVMap.kit._items[Thruster].throttle = self._targetThrottles[Thruster]

        # TODO: Ping the DC-DC Converter to get physical monitoring of power
        
        # self.thruster_current_draw = round(max(estimated_current),2)
        # self.thruster_power_draw = round(estimated_power_draw,2)
        # ROVMap.sendQueue.put(b"010>" + str(self.thruster_current_draw).encode() + b">" + str(self.thruster_power_draw).encode() + b"<")

    def autoUpdate(self):
        print("Drive autoUpdate")
    
    def kill(self):
        for Thruster in range(8):
            if(ROVMap.kit._items[Thruster] is not None):
                ROVMap.kit._items[Thruster].throttle = 0
        ROVMap.log("Drive killed")