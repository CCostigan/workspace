
import pythonfmu
# from pythonfmu import Fmi2Initial, Fmi3Causality, Fmi2Variability, Fmi2Slave, Boolean, Integer, Float64, String
from pythonfmu3 import Fmi3Initial, Fmi3Causality, Fmi3Variability, Fmi3Slave, Boolean, String, Dimension, Float64, Int64, UInt64


class Intel_8088_v3(Fmi3Slave):

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
        self.register_variable(Float64("GND", causality=Fmi3Causality.input))
        self.register_variable(Float64("VCC", causality=Fmi3Causality.input))
        self.register_variable(Float64("NMI", causality=Fmi3Causality.input))
        self.register_variable(Float64("INTR", causality=Fmi3Causality.input))
        self.register_variable(Float64("CLOCK", causality=Fmi3Causality.input))
        self.register_variable(Float64("MN_MX", causality=Fmi3Causality.input))
        self.register_variable(Float64("HOLD", causality=Fmi3Causality.input))
        self.register_variable(Float64("TEST", causality=Fmi3Causality.input))
        self.register_variable(Float64("READY", causality=Fmi3Causality.input))
        self.register_variable(Float64("RESET", causality=Fmi3Causality.input))
        self.register_variable(Float64("AD00_Inp", causality=Fmi3Causality.input))
        self.register_variable(Float64("AD01_Inp", causality=Fmi3Causality.input))
        self.register_variable(Float64("AD02_Inp", causality=Fmi3Causality.input))
        self.register_variable(Float64("AD03_Inp", causality=Fmi3Causality.input))
        self.register_variable(Float64("AD04_Inp", causality=Fmi3Causality.input))
        self.register_variable(Float64("AD05_Inp", causality=Fmi3Causality.input))
        self.register_variable(Float64("AD06_Inp", causality=Fmi3Causality.input))
        self.register_variable(Float64("AD07_Inp", causality=Fmi3Causality.input))
        self.register_variable(Float64("AD08_Inp", causality=Fmi3Causality.input))
        self.register_variable(Float64("AD09_Inp", causality=Fmi3Causality.input))
        self.register_variable(Float64("AD10_Inp", causality=Fmi3Causality.input))
        self.register_variable(Float64("AD11_Inp", causality=Fmi3Causality.input))
        self.register_variable(Float64("AD12_Inp", causality=Fmi3Causality.input))
        self.register_variable(Float64("AD13_Inp", causality=Fmi3Causality.input))
        self.register_variable(Float64("AD14_Inp", causality=Fmi3Causality.input))
        self.register_variable(Float64("AD15_Inp", causality=Fmi3Causality.input))

        self.register_variable(Float64("AD16", causality=Fmi3Causality.output))
        self.register_variable(Float64("AD17", causality=Fmi3Causality.output))
        self.register_variable(Float64("AD18", causality=Fmi3Causality.output))
        self.register_variable(Float64("AD19", causality=Fmi3Causality.output))
        self.register_variable(Float64("BHE_S7", causality=Fmi3Causality.output))
        self.register_variable(Float64("RD", causality=Fmi3Causality.output))
        self.register_variable(Float64("WR__LOCK", causality=Fmi3Causality.output))
        self.register_variable(Float64("M_IO_S2", causality=Fmi3Causality.output))
        self.register_variable(Float64("DT_R_S1", causality=Fmi3Causality.output))
        self.register_variable(Float64("DEN", causality=Fmi3Causality.output))
        self.register_variable(Float64("ALE", causality=Fmi3Causality.output))
        self.register_variable(Float64("INTA", causality=Fmi3Causality.output))
        self.register_variable(Float64("AD00_Out", causality=Fmi3Causality.output))
        self.register_variable(Float64("AD01_Out", causality=Fmi3Causality.output))
        self.register_variable(Float64("AD02_Out", causality=Fmi3Causality.output))
        self.register_variable(Float64("AD03_Out", causality=Fmi3Causality.output))
        self.register_variable(Float64("AD04_Out", causality=Fmi3Causality.output))
        self.register_variable(Float64("AD05_Out", causality=Fmi3Causality.output))
        self.register_variable(Float64("AD06_Out", causality=Fmi3Causality.output))
        self.register_variable(Float64("AD07_Out", causality=Fmi3Causality.output))
        self.register_variable(Float64("AD08_Out", causality=Fmi3Causality.output))
        self.register_variable(Float64("AD09_Out", causality=Fmi3Causality.output))
        self.register_variable(Float64("AD10_Out", causality=Fmi3Causality.output))
        self.register_variable(Float64("AD11_Out", causality=Fmi3Causality.output))
        self.register_variable(Float64("AD12_Out", causality=Fmi3Causality.output))
        self.register_variable(Float64("AD13_Out", causality=Fmi3Causality.output))
        self.register_variable(Float64("AD14_Out", causality=Fmi3Causality.output))
        self.register_variable(Float64("AD15_Out", causality=Fmi3Causality.output))


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