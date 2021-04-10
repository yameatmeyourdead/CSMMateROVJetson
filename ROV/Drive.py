from .Component import Component
from . import ROVMap

class Drive(Component):
    def __init__(self):
        self.thruster_front_left = ROVMap.THRUSTER_FRONT_LEFT
        # TODO: IMPLEMENT
        # self.thruster_front_right = ROVMap.THRUSTER_FRONT_RIGHT
        # self.thruster_back_left = ROVMap.THRUSTER_BACK_LEFT
        # self.thruster_back_right = ROVMap.THRUSTER_BACK_RIGHT
        # self.thruster_z_left = ROVMap.THRUSTER_Z_LEFT
        # self.thruster_z_front = ROVMap.THRUSTER_Z_FRONT
        # self.thruster_z_right = ROVMap.THRUSTER_Z_RIGHT
        # self.thruster_z_back = ROVMap.THRUSTER_Z_BACK

        # Overarching target velocities
        self.x_velocity = 0.0
        self.y_velocity = 0.0
        self.z_velocity = 0.0

        # Individual Thruster Velocities (Throttles)
        self.fl_target_velocity = 0.0
        self.z0_velocity = 0.0
        self.z1_velocity = 0.0
        self.z2_velocity = 0.0
        self.z3_velocity = 0.0
        #TODO: ADD THE REST

        self.VELOCITY_SCALING_FACTOR = .5
        # IMPLEMENT PID
        Drive.logEvent("DRIVE CONSTRUCTED")

    def Update(self):
        # Poll the stick
        poll = ROVMap.getRightStick()
        print(poll)
        self.x_velocity = poll[0]
        self.y_velocity = poll[1]
        
        # Update Throttles
        self.thruster_front_left.throttle = self.x_velocity

        # (DEBUG)
        # print("Drive Update")
    
    def autoUpdate(self):
        print("Drive autoUpdate")
    
    def kill(self):
        print("Drive received kill command")