import numpy as np
import pytest

from sensorsim.instruments import CanCompare, EchantillonneurBloqueur, Environment, Horloge, Recorder, TestEnclosure, TimeGenerator

b = 1

@pytest.mark.unit_test
def test_time_generator():
    tg = TimeGenerator(6, 1000, 10)
    assert len(tg.t_real) == 601
    a=1

    # tg.experiment_step_ms = 1000
    assert len(tg.t_experiment) == 7

    assert tg.get_time_second == 7

@pytest.mark.unit_test
def test_enclosure():

    tg = TimeGenerator(10, 1000, 10)
    # - Pression :
    # la pression est paramétrée pour aller de p1 à p2
    simu_P = np.linspace(1e5, 1e6 , tg.size_exp) 

    # - Température :
    simu_T = np.ones(tg.size_exp)*20
    # simu_T1 = np.ones_like(tg.t_experiment*20

    E = Environment(tg)
    TE = TestEnclosure(E, simu_P, simu_T, tg)
    
    old_P=0
    for tt in tg:
        assert tt == E.time 
        if tg.is_exp_time:
            assert E.P != old_P
        old_P = E.P
    
 
@pytest.mark.unit_test
def test_recorders():
    
    # dict_record = {"a":"var a", "b":"var b", "c":"var c"}
    # tg = TimeGenerator(10, 1000, 10)
    # # - Pression :
    # # la pression est paramétrée pour aller de p1 à p2
    # simu_P = np.linspace(1e5, 1e6 , tg.get_time_second) 

    # # - Température :
    # simu_T = np.ones(tg.get_time_second)*20


    E = Environment()
    # TE = TestEnclosure(E, simu_P, simu_T, tg)



    r = Recorder(E)
    a = 1
    b=2
    d = {"a":a, "b":b}
    r.snapshot2(d)

    assert r.recordings== {}


    r.config({"var a":"a", "var b":"b"})
    r.snapshot2(d)
    assert r.recordings["a"] == [1]

    r.snapshot2({"a":3})
    assert r.recordings["a"] == [1,3]
    assert r.recordings["b"] == [2,None]

    a=11
    r.autosnap(locals())
    assert r.recordings["a"] == [1,3,11]
    assert r.recordings["b"] == [2,None,]

    # c=1
    # d = {"var a":a, "var b":b, "var c":c}
    # r.snapshot2(d)

@pytest.mark.unit_test
def test_clock_with_numeric_stack():
    tg = TimeGenerator(6, 1000, 10)
    E = Environment(tg)

    h = Horloge(E, 10, 1000)

    EB = EchantillonneurBloqueur(h, 2)

    CAN = CanCompare(h, 10, 5)

    for tt in tg:
        vb=EB(tt/1000)
        CAN(vb)
        h1 = h.value
        if E.time % h.tf_s == 0:
            h.value != h1
        print(E.time, h.value, vb, CAN.internal, CAN.out)