#!/bin/sh
# p05 build & run。需要 Icarus Verilog（见 p01 README 安装说明）。
# 若修改了 prog.s，先用 Python 重新汇编：python3 asm2mem.py prog.s prog.mem
set -e
# prog.mem 已随仓库附带；如需从 prog.s 重新生成：python3 asm2mem.py prog.s prog.mem
iverilog -g2005 -o sim.vvp tb_p05.v riscv_single.v imem.v dmem.v
vvp sim.vvp
