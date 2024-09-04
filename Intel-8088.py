
import pythonfmu
from pythonfmu import Fmi2Initial, Fmi2Causality, Fmi2Variability, Fmi2Slave, Boolean, Integer, Real, String


class Intel_8088(Fmi2Slave):

    author = "CCC"
    description = "See what this looks like..."

    def __init__(self, **kwargs):
        super().__init__(**kwargs)        

        # https://ece-research.unm.edu/jimp/310/slides/8086_chipset.html
        self.GND = 0
        self.VCC = 5
        #in = 0
        self.NMI = 0
        self.INTR = 0
        self.CLOCK = 0
        self.MN_MX = 0
        self.HOLD = 0
        self.TEST = 0
        self.READY = 0
        self.RESET = 0
        self.AD00_Inp = 0
        self.AD01_Inp = 0
        self.AD02_Inp = 0
        self.AD03_Inp = 0
        self.AD04_Inp = 0
        self.AD05_Inp = 0
        self.AD06_Inp = 0
        self.AD07_Inp = 0
        self.AD08_Inp = 0
        self.AD09_Inp = 0
        self.AD10_Inp = 0
        self.AD11_Inp = 0
        self.AD12_Inp = 0
        self.AD13_Inp = 0
        self.AD14_Inp = 0
        self.AD15_Inp = 0
        #out = 0
        self.AD16 = 0
        self.AD17 = 0
        self.AD18 = 0
        self.AD19 = 0
        self.BHE_S7 = 0
        self.RD = 0
        self.WR__LOCK = 0
        self.M_IO_S2 = 0
        self.DT_R_S1 = 0
        self.DEN = 0
        self.ALE = 0
        self.INTA = 0
        self.AD00_Out = 0
        self.AD01_Out = 0
        self.AD02_Out = 0
        self.AD03_Out = 0
        self.AD04_Out = 0
        self.AD05_Out = 0
        self.AD06_Out = 0
        self.AD07_Out = 0
        self.AD08_Out = 0
        self.AD09_Out = 0
        self.AD10_Out = 0
        self.AD11_Out = 0
        self.AD12_Out = 0
        self.AD13_Out = 0
        self.AD14_Out = 0
        self.AD15_Out = 0

        #in = 0
        self.register_variable(Real("GND", causality=Fmi2Causality.input))
        self.register_variable(Real("VCC", causality=Fmi2Causality.input))
        self.register_variable(Real("NMI", causality=Fmi2Causality.input))
        self.register_variable(Real("INTR", causality=Fmi2Causality.input))
        self.register_variable(Real("CLOCK", causality=Fmi2Causality.input))
        self.register_variable(Real("MN_MX", causality=Fmi2Causality.input))
        self.register_variable(Real("HOLD", causality=Fmi2Causality.input))
        self.register_variable(Real("TEST", causality=Fmi2Causality.input))
        self.register_variable(Real("READY", causality=Fmi2Causality.input))
        self.register_variable(Real("RESET", causality=Fmi2Causality.input))
        self.register_variable(Real("AD00_Inp", causality=Fmi2Causality.input))
        self.register_variable(Real("AD01_Inp", causality=Fmi2Causality.input))
        self.register_variable(Real("AD02_Inp", causality=Fmi2Causality.input))
        self.register_variable(Real("AD03_Inp", causality=Fmi2Causality.input))
        self.register_variable(Real("AD04_Inp", causality=Fmi2Causality.input))
        self.register_variable(Real("AD05_Inp", causality=Fmi2Causality.input))
        self.register_variable(Real("AD06_Inp", causality=Fmi2Causality.input))
        self.register_variable(Real("AD07_Inp", causality=Fmi2Causality.input))
        self.register_variable(Real("AD08_Inp", causality=Fmi2Causality.input))
        self.register_variable(Real("AD09_Inp", causality=Fmi2Causality.input))
        self.register_variable(Real("AD10_Inp", causality=Fmi2Causality.input))
        self.register_variable(Real("AD11_Inp", causality=Fmi2Causality.input))
        self.register_variable(Real("AD12_Inp", causality=Fmi2Causality.input))
        self.register_variable(Real("AD13_Inp", causality=Fmi2Causality.input))
        self.register_variable(Real("AD14_Inp", causality=Fmi2Causality.input))
        self.register_variable(Real("AD15_Inp", causality=Fmi2Causality.input))

        self.register_variable(Real("AD16", causality=Fmi2Causality.output))
        self.register_variable(Real("AD17", causality=Fmi2Causality.output))
        self.register_variable(Real("AD18", causality=Fmi2Causality.output))
        self.register_variable(Real("AD19", causality=Fmi2Causality.output))
        self.register_variable(Real("BHE_S7", causality=Fmi2Causality.output))
        self.register_variable(Real("RD", causality=Fmi2Causality.output))
        self.register_variable(Real("WR__LOCK", causality=Fmi2Causality.output))
        self.register_variable(Real("M_IO_S2", causality=Fmi2Causality.output))
        self.register_variable(Real("DT_R_S1", causality=Fmi2Causality.output))
        self.register_variable(Real("DEN", causality=Fmi2Causality.output))
        self.register_variable(Real("ALE", causality=Fmi2Causality.output))
        self.register_variable(Real("INTA", causality=Fmi2Causality.output))
        self.register_variable(Real("AD00_Out", causality=Fmi2Causality.output))
        self.register_variable(Real("AD01_Out", causality=Fmi2Causality.output))
        self.register_variable(Real("AD02_Out", causality=Fmi2Causality.output))
        self.register_variable(Real("AD03_Out", causality=Fmi2Causality.output))
        self.register_variable(Real("AD04_Out", causality=Fmi2Causality.output))
        self.register_variable(Real("AD05_Out", causality=Fmi2Causality.output))
        self.register_variable(Real("AD06_Out", causality=Fmi2Causality.output))
        self.register_variable(Real("AD07_Out", causality=Fmi2Causality.output))
        self.register_variable(Real("AD08_Out", causality=Fmi2Causality.output))
        self.register_variable(Real("AD09_Out", causality=Fmi2Causality.output))
        self.register_variable(Real("AD10_Out", causality=Fmi2Causality.output))
        self.register_variable(Real("AD11_Out", causality=Fmi2Causality.output))
        self.register_variable(Real("AD12_Out", causality=Fmi2Causality.output))
        self.register_variable(Real("AD13_Out", causality=Fmi2Causality.output))
        self.register_variable(Real("AD14_Out", causality=Fmi2Causality.output))
        self.register_variable(Real("AD15_Out", causality=Fmi2Causality.output))


    def do_step(self, current_time, step_size):
        return True

# pythonfmu build -f pythonfmu0.py

'''
8088 pinouts

    # "Inp"
    GND
    VCC

    # In out
    AD00_Inp
    AD01_Inp
    AD02_Inp
    AD03_Inp
    AD06_Inp
    AD05_Inp
    AD04_Inp
    AD07_Inp
    AD08_Inp
    AD09_Inp
    AD10_Inp
    AD11_Inp
    AD12_Inp
    AD13_Inp
    AD14_Inp
    AD15_Inp
    AD00_Out
    AD01_Out
    AD02_Out
    AD03_Out
    AD04_Out
    AD05_Out
    AD06_Out
    AD07_Out
    AD08_Out
    AD09_Out
    AD10_Out
    AD11_Out
    AD12_Out
    AD13_Out
    AD14_Out
    AD15_Out

    # In
    NMI
    INTR
    CLOCK
    MN_MX
    HOLD
    TEST
    READY
    RESET
    
    #out
    A16
    A17
    A18
    A19
    BHE_S7
    RD
    WR__LOCK
    M_IO_S2
    DT_R_S1
    DEN
    ALE
    INTA

    
'''