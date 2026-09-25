@echo off
rem p4 build (MSVC, C++17). 需在 "x64 Native Tools Command Prompt for VS" 中运行，
rem 或先执行 vcvarsall.bat x64。
if not exist bin mkdir bin
cl /nologo /std:c++17 /EHsc /O2 /W4 /Fe:bin\p4.exe src\main.cpp
if errorlevel 1 (echo BUILD FAILED & exit /b 1)
echo OK -> bin\p4.exe
