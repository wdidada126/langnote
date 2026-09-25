@echo off
rem Build 01-buffer-pool with MSVC (cl), C++17. Run from this directory.
if not exist build mkdir build
cl /nologo /std:c++17 /EHsc /W4 main.cpp /Fe:build\bufferpool.exe
if %errorlevel%==0 (
  echo ---- running ----
  build\bufferpool.exe
)
