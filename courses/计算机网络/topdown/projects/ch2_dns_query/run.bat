@echo off
rem 语法自检：py -m py_compile dns_query.py
cd /d %~dp0
py -m py_compile dns_query.py || exit /b 1
if "%~1"=="" (py dns_query.py) else (py dns_query.py %*)
