@echo off
rem Stage 06 (MiniC optimizer) — build with MSVC cl.
rem Run from THIS directory in an "x64 Native Tools Command Prompt for VS".
cl /nologo /W4 /EHsc /std:c++17 main.cpp /Fe:minic06.exe
if errorlevel 1 (echo BUILD FAILED & exit /b 1)
echo built: minic06.exe  -^>  minic06.exe ..\samples\dead.minic
