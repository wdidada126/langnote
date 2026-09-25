#!/bin/sh
# p06 build & run。需要 Icarus Verilog（Verilog 部分）与 gcc（C 模拟器部分）。
set -e
iverilog -g2005 -o sim.vvp tb_p06.v cache.v
vvp sim.vvp
gcc -O2 -o cache_sim cache_sim.c
./cache_sim
