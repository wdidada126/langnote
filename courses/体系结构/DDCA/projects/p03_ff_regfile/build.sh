#!/bin/sh
# p03 build & run。需要安装 Icarus Verilog（见 p01 README 安装说明）
set -e
iverilog -g2005 -o sim.vvp tb_p03.v dff.v reg_en.v counter.v regfile.v
vvp sim.vvp
