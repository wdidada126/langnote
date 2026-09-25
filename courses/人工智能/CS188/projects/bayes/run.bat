@echo off
chcp 65001 >nul
rem L09-L10 贝叶斯推断项目：py_compile 自检 + 运行（本轮只写不编译，用户自行执行）
cd /d %~dp0
py -3 -m py_compile bayes_inference.py
if errorlevel 1 exit /b 1
py -3 bayes_inference.py
