# pyright: reportInvalidTypeForm=false

from amaranth import *
from amaranth.lib import wiring

from .isa import AluOp

class ALU(wiring.Component):
    # Inputs
    value1:     wiring.In(32)
    value2:     wiring.In(32)

    funct3:     wiring.In(3)
    funct7:     wiring.In(7)
    immediate:  wiring.In(1)

    # Outputs
    result:     wiring.Out(32)

    def __init__(self):
        super().__init__()

    def elaborate(self, platform):
        m = Module()

        out     = Signal(32)
        shamt   = Signal(5)

        m.d.comb += shamt.eq(self.value2[0:5])

        with m.Switch(self.funct3):
            with m.Case(AluOp.ADD):
                m.d.sync += out.eq(
                    Mux(
                        self.funct7[5] & (~self.immediate),
                        self.value1 - self.value2,
                        self.value1 + self.value2,
                    )
                )
            with m.Case(AluOp.SLL):
                m.d.sync += out.eq(self.value1 << shamt)
            with m.Case(AluOp.SLT):
                m.d.sync += out.eq(self.value1.as_signed() < self.value2.as_signed())
            with m.Case(AluOp.SLTU):
                m.d.sync += out.eq(self.value1 < self.value2)
            with m.Case(AluOp.XOR):
                m.d.sync += out.eq(self.value1 ^ self.value2)
            with m.Case(AluOp.SRA | AluOp.SRL):
                m.d.sync += out.eq(
                    Mux(
                        self.funct7[5],
                        self.value1.as_signed() >> shamt,
                        self.value1 >> shamt,
                    )
                )
            with m.Case(AluOp.OR):
                m.d.sync += out.eq(self.value1 | self.value2)
            with m.Case(AluOp.AND):
                m.d.sync += out.eq(self.value1 & self.value2)

        m.d.comb += self.result.eq(out)

        return m