from .Vector import Vector
import math

SQRT2 = math.sqrt(2)
SQRT05 = math.sqrt(.5)

THRUSTER_FRONT_LEFT_THRUST_VECTOR = Vector(SQRT2/2, SQRT2/2, 0)
THRUSTER_FRONT_RIGHT_THRUST_VECTOR = Vector(-SQRT2/2, SQRT2/2, 0)
THRUSTER_BACK_LEFT_THRUST_VECTOR = Vector(SQRT2/2, -SQRT2/2, 0)
THRUSTER_BACK_RIGHT_THRUST_VECTOR = Vector(-SQRT2/2, -SQRT2/2, 0)

THRUSTER_FRONT_LEFT_TORQUE_VECTOR = Vector(-SQRT2/2, SQRT2/2, 0).crossProduct(THRUSTER_FRONT_LEFT_THRUST_VECTOR)
THRUSTER_FRONT_RIGHT_TORQUE_VECTOR = Vector(SQRT2/2, SQRT2/2, 0).crossProduct(THRUSTER_FRONT_RIGHT_THRUST_VECTOR)
THRUSTER_BACK_LEFT_TORQUE_VECTOR = Vector(-SQRT2/2, -SQRT2/2, 0).crossProduct(THRUSTER_BACK_LEFT_THRUST_VECTOR)
THRUSTER_BACK_RIGHT_TORQUE_VECTOR = Vector(SQRT2/2, -SQRT2/2, 0).crossProduct(THRUSTER_BACK_RIGHT_THRUST_VECTOR)

THRUSTER_Z_0_THRUST_VECTOR = Vector(0, 0, 1)
THRUSTER_Z_1_THRUST_VECTOR = Vector(0, 0, 1)
THRUSTER_Z_2_THRUST_VECTOR = Vector(0, 0, 1)
THRUSTER_Z_3_THRUST_VECTOR = Vector(0, 0, 1)

THRUSTER_Z_0_TORQUE_VECTOR = Vector(-.5, .5, SQRT05).crossProduct(THRUSTER_Z_0_THRUST_VECTOR)
THRUSTER_Z_1_TORQUE_VECTOR = Vector(.5, .5, SQRT05).crossProduct(THRUSTER_Z_1_THRUST_VECTOR)
THRUSTER_Z_2_TORQUE_VECTOR = Vector(-.5, -.5, SQRT05).crossProduct(THRUSTER_Z_2_THRUST_VECTOR)
THRUSTER_Z_3_TORQUE_VECTOR = Vector(.5, -.5, SQRT05).crossProduct(THRUSTER_Z_3_THRUST_VECTOR)

targetTorque = Vector(.5,.5,SQRT05)

def start():
    print(f"""
        Torque Vectors: 
        Front Left:     {THRUSTER_FRONT_LEFT_TORQUE_VECTOR.toString()}
        Front Right:    {THRUSTER_FRONT_RIGHT_TORQUE_VECTOR.toString()}
        Back Left:      {THRUSTER_BACK_LEFT_TORQUE_VECTOR.toString()}
        Back Right:     {THRUSTER_BACK_RIGHT_TORQUE_VECTOR.toString()} 
        Z0:             {THRUSTER_Z_0_TORQUE_VECTOR.toString()}
        Z1:             {THRUSTER_Z_1_TORQUE_VECTOR.toString()}
        Z2:             {THRUSTER_Z_2_TORQUE_VECTOR.toString()}
        Z3:             {THRUSTER_Z_3_TORQUE_VECTOR.toString()}
        """)

    print(f"""
        Throttles:
        Front Left:     {THRUSTER_FRONT_LEFT_TORQUE_VECTOR.dotProduct(targetTorque)}
        Front Right:    {THRUSTER_FRONT_RIGHT_TORQUE_VECTOR.dotProduct(targetTorque)}
        Back Left:      {THRUSTER_BACK_LEFT_TORQUE_VECTOR.dotProduct(targetTorque)}
        Back Right:     {THRUSTER_BACK_RIGHT_TORQUE_VECTOR.dotProduct(targetTorque)}
        Z0:             {THRUSTER_Z_0_TORQUE_VECTOR.dotProduct(targetTorque)}
        Z1:             {THRUSTER_Z_1_TORQUE_VECTOR.dotProduct(targetTorque)}
        Z2:             {THRUSTER_Z_2_TORQUE_VECTOR.dotProduct(targetTorque)}
        Z3:             {THRUSTER_Z_3_TORQUE_VECTOR.dotProduct(targetTorque)}
        """)
