@echo off
cl /nologo /W3 /O2 /std:c11 main.c /Fe:mini_shell.exe
if errorlevel 1 exit /b 1
echo run: mini_shell.exe
