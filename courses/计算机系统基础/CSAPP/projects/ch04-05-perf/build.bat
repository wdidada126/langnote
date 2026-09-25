@echo off
rem ch04-05-perf 构建脚本（MSVC cl）
rem 需先 call vcvarsall.bat x64（或于 x64 Native Tools 命令行中运行）
setlocal
if not exist bin mkdir bin
cl /nologo /W4 /O2 /Fe:bin\matrix.exe src\matrix.c
if errorlevel 1 exit /b 1
bin\matrix.exe
