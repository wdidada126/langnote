@echo off
rem ch10-11-net-conc 构建脚本（MSVC cl + Winsock2）
rem 需先 call vcvarsall.bat x64（或于 x64 Native Tools 命令行中运行）
setlocal
if not exist bin mkdir bin
cl /nologo /W3 /O2 /Fe:bin\echo_server.exe src\echo_server.c /link ws2_32.lib
cl /nologo /W3 /O2 /Fe:bin\echo_client.exe src\echo_client.c /link ws2_32.lib
cl /nologo /W3 /O2 /Fe:bin\producer_consumer.exe src\producer_consumer.c
if errorlevel 1 exit /b 1
echo built: bin\echo_server.exe bin\echo_client.exe bin\producer_consumer.exe
echo 试跑： start bin\echo_server.exe 8000 ^&^& bin\echo_client.exe localhost 8000 hello
