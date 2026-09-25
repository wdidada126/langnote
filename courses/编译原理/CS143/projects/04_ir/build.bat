@echo off
rem Stage 04 (MiniC IR generator) — build with MSVC cl.
rem Run from THIS directory in an "x64 Native Tools Command Prompt for VS".
cl /nologo /W4 /EHsc /std:c++17 main.cpp /Fe:minic04.exe
if errorlevel 1 (echo BUILD FAILED & exit /b 1)
echo built: minic04.exe  -^>  minic04.exe ..\samples\hello.minic
