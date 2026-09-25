#!/usr/bin/env bash
# L04 局部搜索项目：py_compile 自检 + 运行（本轮只写不编译，用户自行执行）
set -e
cd "$(dirname "$0")"
python3 -m py_compile nqueens_local.py
python3 nqueens_local.py
