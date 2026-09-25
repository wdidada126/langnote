@echo off
rem Stage 01 (MiniC lexer) — build with MSVC.
rem Run from THIS directory inside an "x64 Native Tools Command Prompt for VS"
rem (VS2017+ required for /std:c++17). /EHsc enables the exceptions the lexer
rem uses for error reporting.
cl /nologo /W4 /EHsc /std:c++17 main.cpp /Fe:minic01.exe
if errorlevel 1 (echo BUILD FAILED & exit /b 1)
echo built: minic01.exe  -^>  minic01.exe ..\samples\hello.minic
