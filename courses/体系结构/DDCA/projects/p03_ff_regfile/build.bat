@echo off
rem p03 build & run (Windows)。需要安装 Icarus Verilog 并在 PATH 中。
iverilog -g2005 -o sim.vvp tb_p03.v dff.v reg_en.v counter.v regfile.v || exit /b 1
vvp sim.vvp
