# pyright: reportInvalidTypeForm=false

from amaranth import *
from amaranth.lib import wiring
from amaranth.sim import Simulator, SimulatorContext
from amaranth.lib.memory import Memory


class RegisterFile(wiring.Component):
    # Inputs
    rs1_addr:       wiring.In(5)
    rs2_addr:       wiring.In(5)
    rs_re:          wiring.In(1)

    rd_addr:        wiring.In(5)
    rd_data:        wiring.In(32)
    rd_we:          wiring.In(1)

    # Outputs
    rs1_data:       wiring.Out(32)
    rs2_data:       wiring.Out(32)

    def __init__(self):
        self.regs       = Memory(shape=32, depth=32, init=[])

        self.rd_port    = self.regs.write_port()

        self.rs1_port   = self.regs.read_port(transparent_for=(self.rd_port,))
        self.rs2_port   = self.regs.read_port(transparent_for=(self.rd_port,))

        super().__init__()
    
    def elaborate(self, platform):
        m = Module()

        m.submodules.mem = self.regs

        m.d.comb += [
            self.rs1_port.en.eq(self.rs_re),
            self.rs2_port.en.eq(self.rs_re),

            self.rs1_port.addr.eq(self.rs1_addr),
            self.rs2_port.addr.eq(self.rs2_addr),

            self.rs1_data.eq(self.rs1_port.data),
            self.rs2_data.eq(self.rs2_port.data)
        ]

        m.d.comb += [
            self.rd_port.en.eq((self.rd_addr != 0) & (self.rd_we)),
            self.rd_port.addr.eq(self.rd_addr),
            self.rd_port.data.eq(self.rd_data)
        ]

        return m

if __name__ == "__main__":
    # TODO: Testing Framework
    top = RegisterFile()
    async def bench_different(ctx: SimulatorContext):
        ctx.set(top.rs_re, 1)


        ctx.set(top.rs1_addr, 2)
        await ctx.tick()

        ctx.set(top.rd_addr, 2)
        ctx.set(top.rd_data, 100)
        ctx.set(top.rd_we, 1)
        await ctx.tick()

        ctx.set(top.rd_we, 0)

        await ctx.tick()


    sim = Simulator(top)
    sim.add_clock(1e-6)
    sim.add_testbench(bench_different)
    with sim.write_vcd("sim_output/regfile.vcd"):
        sim.run()