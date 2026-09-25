@echo off
rem ch02-bits-float 构建脚本（MSVC cl）
rem 需要 Visual Studio 环境：先执行
rem   call "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat" x64
rem 或使用 "x64 Native Tools Command Prompt" 再运行本脚本。
setlocal
if not exist bin mkdir bin
cl /nologo /W4 /O2 /std:c11 /Fe:bin\bits_test.exe src\bits.c src\main.c
if errorlevel 1 exit /b 1
bin\bits_test.exe
