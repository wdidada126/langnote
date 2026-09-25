@echo off
rem 语法自检：py -m py_compile chat_tcp.py chat_udp.py
cd /d %~dp0
py -m py_compile chat_tcp.py || exit /b 1
py -m py_compile chat_udp.py || exit /b 1
if "%1"=="server" py chat_tcp.py --server
if "%1"=="client" py chat_tcp.py --name %2
if "%1"=="udp-server" py chat_udp.py --server
if "%1"=="udp-client" py chat_udp.py --name %2
if "%1"=="" py chat_tcp.py --server
