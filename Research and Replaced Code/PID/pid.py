from tclab import clock, setup, Historian, Plotter
import numpy as np

def PID(Kp, Ki, Kd, MV_bar=0, beta=1, gamma=0):
    # initialize stored data
    eD_prev = 0
    t_prev = -100
    P = 0
    I = 0
    D = 0
    
    # initial control
    MV = MV_bar
    
    while True:
        # yield MV, wait for new t, SP, PV, TR
        data = yield MV
        
        # see if a tracking data is being supplied
        if len(data) < 4:
            t, PV, SP = data
        else:
            t, PV, SP, TR = data
            I = TR - MV_bar - P - D
        
        # PID calculations
        P = Kp*(beta*SP - PV)
        I = I + Ki*(SP - PV)*(t - t_prev)
        eD = gamma*SP - PV
        D = Kd*(eD - eD_prev)/(t - t_prev)
        MV = MV_bar + P + I + D
        
        # Constrain MV to range 0 to 100 for anti-reset windup
        MV = 0 if MV < 0 else 100 if MV > 100 else MV
        #I = MV - MV_bar - P - D
        
        # update stored data for next iteration
        eD_prev = eD
        t_prev = t

TCLab = setup(connected=False, speedup=10)

controller = PID(1, 0.2, 0, beta=0)   # create pid control
controller.send(None)                 # initialize

tfinal = 1200

with TCLab() as lab:
    h = Historian([('SP', lambda: SP), ('T1', lambda: lab.T1), ('MV', lambda: MV), ('Q1', lab.Q1)])
    p = Plotter(h, tfinal)
    Tlo = lab.T1
    Thi = 120
    for t in clock(tfinal, 2):
        SP =  Thi if (t % 600 < 100) else Tlo                    # get setpoint
        PV = lab.T1                                   # get measurement
        MV = controller.send([t, PV, SP])   # compute manipulated variable
        lab.Q1(MV)                                    # apply 
        p.update(t)                                   # update information display