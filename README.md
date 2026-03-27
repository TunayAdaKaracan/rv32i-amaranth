# Fox-V
A simple single-cycle RV32IZicsr core written in AmaranthHDL. Designed to be readable.

### Planned Features
- Base I extension
- Zicsr extension
- Memory Mapped IO Peripherals: I2C, SPI, UART, GPIO
- Wishbone Bus (Classic)

### Why AmaranthHDL?
- Not a Domain Specific Language. I have the entire python ecosystem at my hands
- Maps to hardware much better in my opinion compared to VHDL/Verilog
- Very easy to upload design to FPGA boards using `amaranth_boards`
- Built-in Simulator
- More explicit compared to VHDL/Verilog.
- Syntax can be learned within a single day
- Rich standard library

### To use
As of now, the core is still unfinished. There is no way to run it yet.