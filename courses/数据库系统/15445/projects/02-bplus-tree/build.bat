@echo off
if not exist build mkdir build
cl /nologo /std:c++17 /EHsc /W3 main.cpp /Fe:build\bplustree.exe
if %errorlevel%==0 (
  echo ---- running ----
  build\bplustree.exe
)
