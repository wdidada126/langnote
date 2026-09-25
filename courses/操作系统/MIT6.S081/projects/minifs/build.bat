@echo off
cl /nologo /W3 /O2 /std:c11 main.c minifs.c /Fe:minifs_demo.exe
if errorlevel 1 exit /b 1
minifs_demo.exe
