import pytest

# import test
import sensorsim.instruments as test


@pytest.fixture()
def env():
    return test.Environment()

@pytest.mark.unit_test
def test_make_plot():
    a = [1,2,2,3,4]
    b = [1,3,4,5,6]
    c = [20,30,40,10,5] 
    t = [1,2,3,4,5]

    fig = test.make_plot(t=t, list_y= [a,[b,c]], titles=("a",("b","c") )) 


    assert 1==1

@pytest.mark.unit_test
def test_horloge(env):
    h = test.Horloge(env,500)
    a = []
    b = []
    for i in range(1,1000,1):
        env.time = i/1000
        a.append(h.get_clock())
        b.append(h.get_pulse())
    
    assert 1==1

from montages import Membrane
from instruments import Environment, Resistance

@pytest.mark.unit_test
def test_horloge(env):
    env = Environment()
    R1 = Resistance(E=env, R=10e3)

    L= 1e-3
    e= 1e-4
    E = 500e9
    Igz = e*L/12*(e**2+L**2)
    P_atm = 1.013e5
    P = 1.013e5
    membrane = Membrane(E = env, EIgz=E*Igz,  diameter= L, P_calib = P_atm+0.3e5)
    a = []
    b = []
    x = []
    for i in range(1,1000,1):
        env.P = .25e5+i*100
        x.append(env.P)
        a.append(membrane.get_def_x()-membrane.L)
        b.append(membrane.check_state())
    
    assert 1==1


@pytest.mark.unit_test
def test_CanCompare():
    can = test.CanCompare(5, 5)

    v_m = 4.1324
    for _ in range(0,5):
        can.compare(v_m)
        print( can.get_v_numerisee() )
        print(can.nb)
    for _ in range(0,5):
        can.compare(3.1324)
        print( can.get_v_numerisee() )
        print(can.nb)
    assert 1==1




