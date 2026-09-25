@echo off
rem p5 运行脚本（Windows）。语法自检命令：
rem python -m py_compile streams.py sieve.py
cd /d %~dp0
python sieve.py
