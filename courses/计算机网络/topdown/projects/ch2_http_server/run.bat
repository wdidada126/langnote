@echo off
rem 语法自检：py -m py_compile http_server.py
cd /d %~dp0
py -m py_compile http_server.py || exit /b 1
py http_server.py
