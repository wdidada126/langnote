@echo off
cl /nologo /W3 /O2 /std:c11 main.c /Fe:lock_demo.exe
if errorlevel 1 exit /b 1
lock_demo.exe
