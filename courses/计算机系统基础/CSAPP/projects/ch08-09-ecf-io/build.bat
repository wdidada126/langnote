@echo off
rem ch08-09-ecf-io 构建脚本（MSVC cl）
rem 需先 call vcvarsall.bat x64（或于 x64 Native Tools 命令行中运行）
setlocal
if not exist bin mkdir bin
cl /nologo /W3 /O2 /Fe:bin\mini_shell.exe src\mini_shell.c
cl /nologo /W3 /O2 /Fe:bin\cp_like.exe  src\robust_copy.c
if errorlevel 1 exit /b 1
echo built: bin\mini_shell.exe bin\cp_like.exe
