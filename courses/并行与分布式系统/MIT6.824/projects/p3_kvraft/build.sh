#!/bin/sh
# P3 分布式 KV 构建脚本（类 Unix）
# 需要本机安装 Go 工具链（https://go.dev/dl），本项目仅用标准库。
# 本轮任务约定"只写不编译"，因此本脚本不会被自动执行。
set -e
cd "$(dirname "$0")"
echo "[p3_kvraft] go build ./..."
go build ./...
echo "BUILD OK"
echo
echo "测试: go test ./tests/ -v -count=1"
echo "演示: go run ."
