import numpy as np
import pytest
from sensorsim import instruments

# from sensorsim.instruments import Environment, Recorder, TestEnclosure, TimeGenerator


@pytest.mark.unit_test
def test_loop():

    L= 2.8e-3
    e= 1e-5
    EE = 130e9
    Igz = e*L/12*(e**2+L**2)
    P_atm = 1.2e5
    P = 1.013e5

    tg = instruments.TimeGenerator(10, 1000, 10)
    # - Pression :
    # la pression est paramétrée pour aller de p1 à p2
    simu_P = np.linspace(1e5, 1e6 , tg.size_exp) 

    # - Température :
    simu_T = np.ones(tg.size_exp)*20
    # simu_T1 = np.ones_like(tg.t_experiment*20

    E = instruments.Environment(tg)
    TE = instruments.TestEnclosure(E, simu_P, simu_T, tg)

    membrane = instruments.Membrane(E = E, EIgz=EE*Igz, e=e , diameter= L, P_calib = P_atm)
    R1 = instruments.Resistance(E=E, R=10e3, quality="high")
    R1.attach_membrane(membrane=membrane,side=1)

    for tt in tg:
        print(E.time, E.P,membrane.dL, R1.resistance)
    a=1
