#!/usr/bin/env bash
# 规划项目(L02-L03 应用)：py_compile 自检 + 运行（本轮只写不编译，用户自行执行）
set -e
cd "$(dirname "$0")"
python3 -m py_compile grape_world.py
python3 grape_world.py
