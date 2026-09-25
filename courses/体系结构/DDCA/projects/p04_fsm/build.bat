@echo off
rem p04 build & run (Windows)。需要安装 Icarus Verilog 并在 PATH 中。
iverilog -g2005 -o sim.vvp tb_p04.v seq_detect.v traffic_light.v || exit /b 1
vvp sim.vvp
