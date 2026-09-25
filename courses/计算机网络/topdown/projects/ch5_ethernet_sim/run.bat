@echo off
rem 语法自检：py -m py_compile ethernet_sim.py
cd /d %~dp0
py -m py_compile ethernet_sim.py || exit /b 1
py ethernet_sim.py
