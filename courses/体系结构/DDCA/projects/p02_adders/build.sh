#!/bin/sh
# p02 build & run。需要安装 Icarus Verilog（apt install iverilog / brew install icarus-verilog / scoop install iverilog）
set -e
iverilog -g2005 -o sim.vvp tb_p02.v half_adder.v full_adder.v rca.v cla4.v
vvp sim.vvp
