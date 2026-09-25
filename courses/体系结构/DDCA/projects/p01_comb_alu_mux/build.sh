#!/bin/sh
# p01 build & run (Linux/macOS/WSL/Git Bash)。需要先安装 Icarus Verilog：
#   Ubuntu: sudo apt install iverilog | macOS: brew install icarus-verilog | scoop (Win): scoop install iverilog
# 用法：./build.sh （本轮仓库约定"只写不编译"，请自行执行）
set -e
iverilog -g2005 -o sim.vvp tb_p01.v mux2.v mux4.v decoder.v alu.v
vvp sim.vvp
