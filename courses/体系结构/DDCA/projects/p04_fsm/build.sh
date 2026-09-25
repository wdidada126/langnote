#!/bin/sh
# p04 build & run。需要安装 Icarus Verilog（见 p01 README 安装说明）
set -e
iverilog -g2005 -o sim.vvp tb_p04.v seq_detect.v traffic_light.v
vvp sim.vvp
