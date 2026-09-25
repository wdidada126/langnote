@echo off
rem P3 分布式 KV 构建脚本（Windows）
rem 需要本机安装 Go 工具链（https://go.dev/dl），本项目仅用标准库。
rem 本轮任务约定"只写不编译"，因此本脚本不会被自动执行。
cd /d %~dp0
echo [p3_kvraft] go build ./...
go build ./...
if errorlevel 1 (
  echo BUILD FAILED
  exit /b 1
)
echo BUILD OK
echo.
echo 测试: go test ./tests/ -v -count=1
echo 演示: go run .
