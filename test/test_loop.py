import numpy as np
import pytest
from sensorsim import instruments, montages

# from sensorsim.instruments import Environment, Recorder, TestEnclosure, TimeGenerator


@pytest.mark.unit_test
def test_loop():

    tg = instruments.TimeGenerator(60, 100, 10)
    # - Pression :
    # la pression est paramétrée pour aller de p1 à p2
    simu_P = np.linspace(101325.0,26442.18910734488 , tg.size_exp) 

    # - Température :
    simu_T = np.ones(tg.size_exp)*20

    # Instruments utilisés :
    env = instruments.Environment(tg)
    TE = instruments.TestEnclosure(env, simu_P, simu_T, tg)

    # Initialisation de la membrane
    L= 2.8e-3
    e= 1e-5
    E = 130e9
    Igz = e*L/12*(e**2+L**2)
    P_atm = 1.2e5
    P = 1.013e5
    membrane = instruments.Membrane(E = env, EIgz=E*Igz, e=e , diameter= L, P_calib = P_atm)

    # On choisit ici la qualité des générateurs :
    noise = 1e-6 
    # par défaut 1e-3 : on prend plus précis pour améliorer la précision : paramètre à faire
    # varier quand une première calibration est faite

    # Generateur 
    gen = instruments.Generateur(v_alim=5.0,noise=noise)


    ### Pour avoir des résistances plus précises on définit la qualité des résistances 
    quality = "high" # paramètre à faire varier pour jouer sur la précision du capteur

    # Initialisation des résistances
    R1 = instruments.Resistance(E=env, R=10e3, quality=quality)
    R2 = instruments.Resistance(E=env, R=17.9e3, quality=quality)
    R3 = instruments.Resistance(E=env, R=1e3,K=3.2, quality=quality)
    R4 = instruments.Resistance(E=env, R=1.79e3,K=3.2, quality=quality)


    # on attache la résistance à la membrane 
    R4.attach_membrane(membrane,-1)
    R3.attach_membrane(membrane,1)

    wheastone = montages.Wheastone(R1, R2, R3, R4)

    # Resistances gain

    R1_ao = instruments.Resistance(E=env, R=2.7e3)
    R2_ao = instruments.Resistance(E=env, R=92e3)
    R3_ao = instruments.Resistance(E=env, R=10)
    R4_ao = instruments.Resistance(E=env, R=100e3)

    gen_ao = instruments.Generateur(v_alim=89/250, noise=noise)

    # Etage du CAN
    h = instruments.Horloge(env, 10, 1000)
    EB = instruments.EchantillonneurBloqueur(h,2)
    can = instruments.CanCompare(h, 8, 5) # 8 bits / 5V alim

    # CPU
    cpu = instruments.Cpu(env,h)

    # init recorder

    r = instruments.Recorder(env)
    r.config_name(
        {
            "P":"P",
            "T":"T",
            "M":"Membrane",
            "V_mesure":"V_mesure",
            "V_gain":"V_gain",
            "vb":"vb",
            "R1":"R1",
            "R2":"R2",
            "R3":"R3",
            "R4":"R4",
            "hh":"horloge",
            "EB":"EB",
            "cout":"can output",
            "cint":"can internal",
            "cpu":"cpu"
        }
    )
    r.config_plot ({
            'P': False,
            'T': False,
            "Membrane":False,
            'V_mesure': False,
            'V_gain': False,
            'vb': False,
            'R1': False,
            'R2': False,
            'R3': False,
            'R4': False,
            'hh': True,
            'EB': True,
            'cout': True,
            'cint': True,
            "cpu":True})

    for tt in tg:
        print(tt, env.time, h.value)
        V_mesure = wheastone(gen())
        V_gain = montages.montage_ampli_op(gen_ao(), V_mesure, R1_ao(), R2_ao(), R3_ao(), R4_ao())
        vb=EB(V_gain)
        can(vb)
        cpu(can.out)

        snp = {        
            "P":env.P,
            "T":env.T,
            "M":membrane.L_def,
            "V_mesure":V_mesure,
            "V_gain":V_gain,
            "vb":vb,
            "R1":R1(),
            "R2":R2(),
            "R3":R3(),
            "R4":R4(),
            "hh":h.value,
            "EB":vb,
            "cout":can.out,
            "cint":can.internal,
            "cpu":cpu.altitude}

        r.snapshot(snp)

    r.plot(
        {
            1:"P",2:"T",7:"M",3:["V_mesure","V_gain"],4:["R3","R4"],5:["cint","cout","EB"], 6:"hh",8:"cpu"
        }
    )