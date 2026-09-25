@echo off
rem p01 build & run (Windows). 需要先安装 Icarus Verilog 并把 bin 目录加入 PATH：
rem   https://steveicarus.github.io/iverilog  （或 pip 之外的独立安装包/包管理器，如 scoop install iverilog）
rem 本脚本只做语法：iverilog 编译出 sim.vvp，再用 vvp 运行；本轮仓库约定"只写不编译"，请自行执行。
iverilog -g2005 -o sim.vvp tb_p01.v mux2.v mux4.v decoder.v alu.v || exit /b 1
vvp sim.vvp
