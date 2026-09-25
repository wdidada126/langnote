@echo off
rem ch03-asm 构建脚本（MSVC cl）
rem 需先 call vcvarsall.bat x64（或于 x64 Native Tools 命令行中运行）
setlocal
if not exist bin mkdir bin
cl /nologo /W4 /O2 /Fabin\funcs.asm /Fdbin\ /Fe:bin\funcs.exe src\funcs.c
if errorlevel 1 exit /b 1
echo == run ==
bin\funcs.exe
echo == 反汇编: dumpbin /disasm bin\funcs.obj ==
dumpbin /disasm:bytes bin\funcs.obj | more +0
