@echo off
chcp 65001 >nul
rem 规划项目(L02-L03 应用)：py_compile 自检 + 运行（本轮只写不编译，用户自行执行）
cd /d %~dp0
py -3 -m py_compile grape_world.py
if errorlevel 1 exit /b 1
py -3 grape_world.py
