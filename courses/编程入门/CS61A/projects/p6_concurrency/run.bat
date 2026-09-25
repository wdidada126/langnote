@echo off
rem p6 运行脚本（Windows）。语法自检命令：
rem python -m py_compile race.py gil_demo.py main.py
cd /d %~dp0
python main.py
