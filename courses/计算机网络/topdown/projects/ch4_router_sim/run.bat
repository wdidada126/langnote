@echo off
rem 语法自检：py -m py_compile router_sim.py
cd /d %~dp0
py -m py_compile router_sim.py || exit /b 1
py router_sim.py
