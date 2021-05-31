from math import pi, asin

class Membrane:
    """
        Sensor membrane

        Params :
            - E : environment object
            - EIgz : Young modulus x Igz
            - diameter : diameter of the membrane
            - P_calib : static pressure on the other side of the membrane

    """
    # https://fr.wikipedia.org/wiki/Th%C3%A9orie_des_poutres
    def __init__(self,E , EIgz, diameter, P_calib, e = 1e-3, Y = 130e9, alpha = 0.4):
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
        y = self.compute_def_z()

        L_def = 2*(y**2+self.L**2/4)**.5
        L_def *= (1+ 0.409e-6 + 0.686e-9*self.E.T)
        self.L_def = self.alpha*self.L_def + (1-self.alpha)*L_def
        return self.L_def

    def get_def_x(self):
        self.compute_force()
        return self.compute_def_x()



def wheastone(V_0, R1,R2,R3,R4):

    Vs = V_0 * (R4/(R1+R4)-R3/(R2+R3))

    return Vs

def montage_ampli_op(V1,V2,R1,R2,R3,R4):
    Vs = (R1+R2)/R1 * R4/(R3+R4) * V2 - R2/R1*V1
    return Vs