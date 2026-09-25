@echo off
rem 项目 heap 构建脚本（JDK 17：javac/java，无外部依赖；-encoding UTF-8 因源码含中文注释）
setlocal
if not exist build mkdir build
javac -encoding UTF-8 -d build src\cs61b\heap\*.java
if errorlevel 1 exit /b 1
java -cp build cs61b.heap.Main
endlocal
