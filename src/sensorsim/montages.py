"""
This module provides some classical electronic circuits as functions and the sensor membrane

"""





class Wheastone:
    def __init__(self,R1,R2,R3,R4) -> None:
        self.R1 = R1
        self.R2 = R2
        self.R3 = R3
        self.R4 = R4
    def wheastone(self, V_0):
        Vs = V_0 * (self.R4()/(self.R1()+self.R4())-self.R3()/(self.R2()+self.R3()))
        return Vs
    __call__=wheastone

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