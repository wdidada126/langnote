@echo off
rem p06 build & run (Windows)。需要 Icarus Verilog（Verilog 部分）与 gcc（C 模拟器，MinGW-w64 等）。
iverilog -g2005 -o sim.vvp tb_p06.v cache.v || exit /b 1
vvp sim.vvp
gcc -O2 -o cache_sim.exe cache_sim.c && cache_sim.exe
