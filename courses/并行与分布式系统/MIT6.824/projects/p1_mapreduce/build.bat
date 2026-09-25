@echo off
rem P1 MapReduce 构建脚本（Windows）
rem 需要本机安装 Go 工具链（https://go.dev/dl），本项目仅用标准库。
rem 本轮任务约定"只写不编译"，因此本脚本不会被自动执行。
cd /d %~dp0
echo [p1_mapreduce] go build ./...
go build ./...
if errorlevel 1 (
  echo BUILD FAILED
  exit /b 1
)
echo BUILD OK
echo.
echo 运行: go run .
echo 该 demo 会在临时目录里跑一个带宕机/备份任务的 wordcount 作业。
