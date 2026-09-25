@echo off
rem Stage 03 (MiniC semantic analysis) — build with MSVC cl.
rem Run from THIS directory in an "x64 Native Tools Command Prompt for VS".
cl /nologo /W4 /EHsc /std:c++17 main.cpp /Fe:minic03.exe
if errorlevel 1 (echo BUILD FAILED & exit /b 1)
echo built: minic03.exe  -^>  minic03.exe ..\samples\bad.minic
