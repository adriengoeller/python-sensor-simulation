"""
This module provides some classical electronic circuits as functions and the sensor membrane

"""


from math import pi, asin

class Membrane:
    """
        Sensor membrane : (formulas from wikipedia and Capteurs : Pressions, accélération et forces à pont de Wheastone, Jean Louis Rouvet - Giacintec)
            Simulate membrane sensor for input pressure
            - Use compute_force to get the force applied on the surface
            - Use compute_def_z to get z displacement
            - Use get_def_x to get x elongation.

        Params :
            - E : environment object
            - EIgz : Young modulus x Igz
            - diameter : diameter of the membrane
            - P_calib : static pressure on the other side of the membrane
            - e : thickness (m) (default : 1e-5)
            - Y : young modulus (Pa)
            - alpha : time inertia coefficient (simulate delay)

    """
    # https://fr.wikipedia.org/wiki/Th%C3%A9orie_des_poutres
    def __init__(self,E , EIgz, diameter, P_calib, e = 1e-5, Y = 130e9, alpha = 0.4):
        self.E = E
        self.Y = Y
        self.EIgz = EIgz
        self.S = (diameter/2)**2 *pi
        self.L = diameter
        self.F = 0
        self.epais = e
        self.P_calib = P_calib
        self.L_def = diameter
        self.alpha = alpha

    def compute_force(self):
        self.F = (self.E.P-self.P_calib)/self.S

    def compute_def_z(self,x=None):
        if x == None :
            x = self.L/2
            # out = 
        return  3*(self.E.P- self.P_calib) * ( 1 - 0.4**2 ) / (16 * self.Y*self.epais**3  ) * (self.L/2)**4
        # return 1/self.EIgz * (self.F/12*(x)**3-self.F*self.L**2*(x)/16)

    def check_state(self):
        return (self.L_def-self.L)/self.L

    def compute_def_x(self,):
        """
        
        """
        y = self.compute_def_z()

        L_def = 2*(y**2+self.L**2/4)**.5
        L_def *= (1+ 0.409e-6 + 0.686e-9*self.E.T)
        self.L_def = self.alpha*self.L_def + (1-self.alpha)*L_def
        return self.L_def

    def get_def_x(self):
        self.compute_force()
        return self.compute_def_x()



def wheastone(V_0, R1,R2,R3,R4):
    """
    Wheastone formula function

    Params : 
        - V_0 working voltage
        - R1, R2, R3, R4 the resistances
    """

    Vs = V_0 * (R4/(R1+R4)-R3/(R2+R3))

    return Vs

def montage_ampli_op(V1,V2,R1,R2,R3,R4):

    """
    amplification stage of the sensor.
    Here a substractor AOP is coded

    Params : 
        - V_1, V_2 input voltage
        - R1, R2, R3, R4 the resistances
    """

    Vs = (R1+R2)/R1 * R4/(R3+R4) * V2 - R2/R1*V1
    return Vs