@echo off
rem Stage 05 (MiniC three-address VM) — build with MSVC cl.
rem Run from THIS directory in an "x64 Native Tools Command Prompt for VS".
cl /nologo /W4 /EHsc /std:c++17 main.cpp /Fe:minic05.exe
if errorlevel 1 (echo BUILD FAILED & exit /b 1)
echo built: minic05.exe  -^>  minic05.exe ..\samples\hello.minic
