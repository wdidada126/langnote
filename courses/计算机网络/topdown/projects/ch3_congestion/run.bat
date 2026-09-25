@echo off
rem 语法自检：py -m py_compile congestion_sim.py
cd /d %~dp0
py -m py_compile congestion_sim.py || exit /b 1
py congestion_sim.py
