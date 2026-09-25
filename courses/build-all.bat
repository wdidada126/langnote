@echo off
rem courses 聚合编译脚本（Windows，集中验证用；本轮开发时只写未执行）
rem 用法:
rem   build-all.bat            依次执行各课程 projects 下的 build.bat
rem   build-all.bat <课程目录>  只处理指定课程，如: build-all.bat "计算机系统基础\CSAPP"
rem 前置:
rem   C/C++  : 在 Developer Command Prompt（vcvarsall）或已配好 cl 的终端运行
rem   Java   : JDK17 在 PATH
rem   Python : python 在 PATH
rem   Go     : go 在 PATH
rem   Verilog: iverilog 在 PATH
setlocal enabledelayedexpansion
chcp 65001 >nul
set "ROOT=%~dp0"
set PASS=0
set FAIL=0

for /d %%C in ("%ROOT%?*\*") do (
  if exist "%%C\projects\" (
    if "%~1"=="" (
      call :process "%%C"
    ) else (
      echo %%C | find "%~1" >nul && call :process "%%C"
    )
  )
)
for /d %%C in ("%ROOT%?*\?*\*") do (
  if exist "%%C\projects\" call :process "%%C"
)

echo.
echo PASS=!PASS! FAIL=!FAIL!
exit /b

:process
for /d %%P in ("%~1\projects\*") do (
  if exist "%%P\build.bat" (
    echo ==^> [build] %%~nxP
    pushd "%%P"
    call build.bat
    if errorlevel 1 (set /a FAIL+=1 & echo   FAIL: %%P) else (set /a PASS+=1)
    popd
  )
)
exit /b
