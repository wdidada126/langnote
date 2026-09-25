@echo off
rem P1 运行脚本（Windows）。语法自检命令：
rem python -m py_compile rat.py expr.py main.py
cd /d %~dp0
python main.py
