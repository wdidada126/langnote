@echo off
cl /nologo /W3 /O2 /std:c11 main.c /Fe:sched_demo.exe
if errorlevel 1 exit /b 1
sched_demo.exe
