# pyright: reportInvalidTypeForm=false

from decoder import Decoder
from regfile import RegisterFile

from amaranth import *
from amaranth.lib import wiring
from amaranth.lib.memory import Memory

class ExecutionStage:
    FETCH_INSTRUCTION   = "FETCH_INSTRUCTION"
    FETCH_REGISTERS     = "FETCH_REGISTERS"
    EXECUTE             = "EXECUTE"


class CPU(wiring.Component):
    def __init__(self, code):
        self.regs       = RegisterFile()
        self.decoder    = Decoder()

        self.memory     = Memory(shape=32, depth=len(code), init=code)
        self.mem_write  = self.memory.write_port()
        self.mem_read   = self.memory.read_port(transparent_for=(self.mem_write,)) # TODO: Write-through is possibly redundant. Research

        super().__init__({})
    
    def elaborate(self):
        m = Module()

        m.submodules.memory     = self.memory
        m.submodules.regs       = regs = self.regs
        m.submodules.decoder    = decoder = self.decoder

        return m

