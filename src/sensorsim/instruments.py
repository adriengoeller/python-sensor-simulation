"""
This module provides all the instruments
"""

from random import random
from math import pi, asin

from sensorsim.tools import compute_error


class Environment:
    """
    Object for controlling environment during experiment
    Usage : inside a time for-loop where P and T can be changed function of current time

    Param : 
    - T : temperature
    - time : current time
    - P : pressure
    """
    def __init__(self, T=20, time=0, P=1e6):
        self.T = T
        self._time = time
        self.P = P
        self._observers= []

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, t):
        self._time = t
        for callback in self._observers:
            # print('announcing change')
            callback(self._time)

    def bind_to(self, callback):
        # print('bound')
        self._observers.append(callback)

# Definition des objets du tp
class Resistance:
    """
    Object Resistance : simulate a electrical resistance with noise, temperature and strength effect
    The resistance can be used as a classical resistance or attached to an object to measure deformation.
    For this use the attach_membrane method
    To get the resistance value, use .get_resistance method at each step you want to perform a measure/calculus.

    Params : 
    - E : environement object
    - R : resistance value in ohms
    - K : jauge effect parameter
    - alpha : temperature effect
    """

    def __init__(self, E, R, L = 1e-2 , K=2, alpha=0.0002): 
        self.E = E
        self.R = R
        self.T = E.T 
        self.eps = 1e-3 
        self.L = L 
        self.dL = 0 
        self.membrane = None
        self.side = None
        self.K = K # typiquement 2 pour les métaux, 200 pour les piezo 
        self.alpha = alpha # tres petit ( 0.000009 à 0.00002 ohm/(ohm degC) ou 9 à 20 ppm/ degC) est par  exemple  un  choix  judicieux  par  rapport  au  cuivre  ( 0.0043  ohm/(ohm degC)  ou  4 300 ppm/ degC) 
        
    def compute_R(self):
        return self.R * (1 + self.dL/self.L *self.K) * (1 + self.alpha * self.E.T)*(1 + self.eps*(2*random()-1) )
    
    def set_deformation(self, dL): 
        self.dL = dL 

    def attach_membrane(self, membrane, side):
        """
        Attach resistance to an existing Paroi object.
        Params : 
            - membrane : membrane object
            - side : side of the membrane (1 or -1)
        """
        self.membrane = membrane
        self.side = side
        self.L = membrane.L
    
    # def set_environnement(self, T): 
    #     self.T = T 
    
    def get_resistance(self): 
        """
        Get resistance value
        Params :
            - No params
        """
        if self.membrane != None:
            self.set_deformation( self.side*(self.membrane.get_def_x()-self.membrane.L))
        return self.compute_R() 

class Generateur:
    """
    Object voltage generator
    
    Params : 
        - v_alim : output voltage
        - noise : noise (default : 1e-3)
    """
    def __init__(self, v_alim, noise=1e-3):
        self.v_alim = v_alim
        self.noise = noise

    def get_v_alim(self):
        return self.v_alim *(1+ self.noise*(2*random()-1) )




class Horloge: 
    """
        This object is simulating a clock.
        Usage : declare it and link it with your environment object
        The clock object is auto updating.
        To get clock state (True/False value), use get_pulse or get_clock

        Params : 
            - E : environment object
            - frequence : frequency
            - granularity_env_time : granularity of the time in the environmnent object (ex: your step time is 0.1 sec)
    """

    def __init__(self, E, frequence, granularity_env_time):
        self.E = E
        self.E.bind_to(self.update_time)
        self.frequence = frequence
        self.tf_s = 1/frequence*granularity_env_time
        self.factor = granularity_env_time
        self.value = False
        self._time = 0
   
    def update_time(self, time):
        self._time = time*self.factor
        self.update_clock()

    @property
    def discrete_clock(self):
        return self._time - (self._time % self.tf_s)

    @property
    def pulse_clock(self):
        return (self._time % self.tf_s == 0)
    
    
    def update_clock(self):
        if self.pulse_clock:
            self.value = not(self.value)


    def get_pulse(self):
        """
        return True if there is a change level
        """
        return self.pulse_clock


    def get_clock(self):
        """
        return at any moment the state of the clock
        """
        return self.value


class EchantillonneurBloqueur:
    """
    Based on the horloge object, it blocks the input signal periodically every clock pulse x multiple.
    To get value, use get_echantillon method

    Params :
        - horloge : clock "horloge" object
        - multiple : number of clock pulse before blocking a new input value
        - v_entree : input signal to block
    """
    def __init__(self, horloge, multiple, v_entree=0):
        self.horloge = horloge
        self.count = 0
        self.multiple = multiple
        self.v_bloquee = v_entree

    def get_echantillon(self, v_entree):
        """
        get blocked value of your v_entree (input signal)
        Params :
            - v_entree : input signal to block
        """
        if self.horloge.get_pulse() :
            self.count += 1
        else:
            pass        
        if self.count == self.multiple :
            self.v_bloquee = v_entree
            self.count = 0
        return self.v_bloquee


class CanCompare():
    """
    CAN object

    Description :
        Simulate a CAN with successive approximation technology https://en.wikipedia.org/wiki/Analog-to-digital_converter or described here in french : https://fr.wikipedia.org/wiki/Convertisseur_analogique-num%C3%A9rique

    Params : 
        - horloge : clock (horloge) object of your experiment
        - resolution : resolution f your CAN
        - v_alim : voltage working range of the CAN


    Example : 
        To make work the can, you have to 
        1) initialise can object outside the time loop
        inside the time loop : 
        2) To process :
            can.compare(signal_you_want)
        3) To get final value (after comparison cycle)
            can.get_v_numerisee()
        4) To get final value (during comparison cycle)
            can.get_v_numerisee_courante()
    """
    def __init__(self,horloge, resolution, v_alim):
        self.horloge = horloge
        self.resolution = resolution
        self.v_alim = v_alim
        self.quantum = v_alim / (2**resolution)
        self.nb = 1
        self.qs = 0b0


    def compare(self, v_m ):
        if self.horloge.get_pulse():
            self.qs = 0
            self.nb = 1
        if self.nb <= self.resolution:
            if ( (self.qs + (1 << (self.resolution - self.nb) )) * self.quantum ) < v_m:
                self.qs +=  (1 << (self.resolution - self.nb) )
            else:
                pass
            self.nb += 1

    def get_bytes(self):
        return self.qs

    def get_v_numerisee_courante(self):
        return self.qs * self.quantum
    
    def get_v_numerisee(self):
        if self.nb > self.resolution:
            return self.qs * self.quantum
        else:
            return None


class Cpu():
    """
    Cpu object

    Description : 
        perform more intensitve calculus. Here the altimeter formula is implemented.
        Use check_value method for general input. It launches a two step process : correction (calibration) then compute method
        Inside you can use method "calibrate" to add regression coefficient obtained with numpy.polyfit

    Params : 
        - E : environment object

    Example :
        inside the time loop :
        altitude = cpu.check_value(horloge.get_pulse(), signal_from_can)
    """


    def __init__(self,E):
        self.E = E
        self.value_can = 0
        self.time = E.time
        self.pression = 0
        self.coefficient_correction = reg = [ 94.95021929  ,-626.54622693,  2315.98491463, 10241.5233834,22504.35066598]

    def check_value(self, value_eb, value_can):

        if value_eb:
            self.time = self.E.time
        if value_can is not None:
            self.value_can = value_can
            self.process()
            return self.altitude
        else:
            return None

    def get_input_value(self):
        return (self.time,self.value_can)

    def process(self):
        self.correction()
        self.compute()


    def set_value_can(self, value_can):
        self.value_can = value_can

    def correction(self):
        # reg = [17905.19555648, 14468.22756158]
        # self.pression = self.value_can *reg[0] + reg[1] 
        # reg = [ 94.95021929  ,-626.54622693,  2315.98491463, 10241.5233834,22504.35066598]
        
        if isinstance(self.coefficient_correction, (float, int)):
            self.coefficient_correction = [self.coefficient_correction]

        if isinstance(self.coefficient_correction, list):
            degree = len(self.coefficient_correction)
            self.pression = 0
            for i in range(0,degree):
                self.pression += self.value_can**(degree-i) * self.coefficient_correction[i]

        else:
            self.pression = self.value_can

        # self.pression = self.value_can**4 *reg[0] + self.value_can**3 *reg[1] +self.value_can**2 *reg[2] + self.value_can**1 *reg[3] + reg[4] 

    def calibrate(self,coef):
        self.coefficient_correction = coef

    def compute(self):
        self.altitude = 288.15/0.0065*(1-(self.pression/1.013e5)**(1/5.255))
        


from plotly.subplots import make_subplots
import plotly.graph_objects as go

def make_plot(t, list_y, titles=(), graph_type=None, height=600, width=600, title_text="Stacked Subplots"):

    """
    Description : 
        function for plotting simply variables as lists of numbers. The variable x is the same for all the graphics.
        It use plotly to provide a interactive graph.

    Params :
        - t : common time value for all graphs
        - list_y : list of y values of the different graphs to plot
        - titles : tuple of the titles for each graphics. Warning : a lot of errors comes from list_y, titles or graph_type which do not have the same length.
        - graph_type : True for step graph (simulate numeric value), False for spline graph (simulate analogic value)
        - height : height of the whole generated graph
        - width : width of the whole generated graph
        - title_text : title of the whole generated graph

    Example :
        fig = instruments.make_plot(
            record_time, 
            [
                record_L,
                [record_R1,record_R2,record_R3,record_R4], # if you want to put several variable in one graph
                record_cpu      
            ], 
            titles=(
                "Length of membrane",
                ("R1","R2","R3","R4"), # careful here : ()
                'CPU'
                ),
                # Mettez True pour les grandeurs digitales et False pour les grandeurs continues
            graph_type = [
                False,
                [False,False, False,False], # Resistance are analogic. /!\ careful here : []
                True        # cpu output numeric values
                ] ,
                height = variable_number*300
                
                )
    """


    rows = len(list_y)
    fig = make_subplots(rows=rows, cols=1, subplot_titles = [str(t) for t in titles])

    i = 0
    
    for y in list_y:
        i += 1



        if any(isinstance(el, list) for el in y):
            j=0
            for yy in y:
                j += 1
                if graph_type is not None:
                    if graph_type[i-1][j-1]:
                        shape = 'hv'
                    else:
                        shape = 'spline'
                fig.append_trace(go.Scatter(
                    x=t,
                    y=yy,
                    name = titles[i-1][j-1],
                    line= {"shape": shape},
                ), row=i, col=1)
        else:
            if graph_type is not None:    
                if graph_type[i-1]:
                        shape = 'hv'
                else:
                    shape = 'spline'
            fig.append_trace(go.Scatter(
                x=t,
                y=y,
                name = titles[i-1],
                line= {"shape": shape},
            ), row=i, col=1)


    fig.update_layout(height=height, width=width, title_text=title_text)
    return fig





    



