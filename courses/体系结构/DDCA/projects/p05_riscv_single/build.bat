@echo off
rem p05 build & run (Windows)。需要 Icarus Verilog（iverilog/vvp）在 PATH 中。
rem 若修改了 prog.s，先用 Python 重新汇编：python asm2mem.py prog.s prog.mem
iverilog -g2005 -o sim.vvp tb_p05.v riscv_single.v imem.v dmem.v || exit /b 1
vvp sim.vvp
