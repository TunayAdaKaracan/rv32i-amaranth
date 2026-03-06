# pyright: reportInvalidTypeForm=false

from amaranth import *
from amaranth.lib import wiring


class ALU(wiring.Component):
    # Inputs
    value1:     wiring.In(32)
    value2:     wiring.In(32)

    funct3:     wiring.In(3)
    funct7:     wiring.In(7)

    # Outputs
    result:     wiring.Out(32)

    def __init__(self):
        super().__init__()
    
    def elaborate(self, platform):
        m = Module()

        # TODO: Alu
        
        return m