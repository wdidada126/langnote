@echo off
rem Stage 02 (MiniC parser + AST dump) — build with MSVC cl.
rem Run from THIS directory in an "x64 Native Tools Command Prompt for VS"
rem (VS2017+ for /std:c++17). /EHsc: the parser's panic-mode uses exceptions.
cl /nologo /W4 /EHsc /std:c++17 main.cpp /Fe:minic02.exe
if errorlevel 1 (echo BUILD FAILED & exit /b 1)
echo built: minic02.exe  -^>  minic02.exe ..\samples\hello.minic
