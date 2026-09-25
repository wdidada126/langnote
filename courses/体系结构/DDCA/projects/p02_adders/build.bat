@echo off
rem p02 build & run (Windows)。需要安装 Icarus Verilog 并在 PATH 中（见 p01 README 说明）。
iverilog -g2005 -o sim.vvp tb_p02.v half_adder.v full_adder.v rca.v cla4.v || exit /b 1
vvp sim.vvp
