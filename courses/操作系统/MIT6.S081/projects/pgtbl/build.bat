@echo off
cl /nologo /W3 /O2 /std:c11 main.c pgtbl.c /Fe:pgtbl_demo.exe
if errorlevel 1 exit /b 1
pgtbl_demo.exe
