@echo off
rem build.bat — alloc demo (run inside "Developer Command Prompt for VS", cl available)
cl /nologo /W3 /O2 /std:c11 main.c firstfit.c buddy.c /Fe:alloc_demo.exe
if errorlevel 1 exit /b 1
alloc_demo.exe
