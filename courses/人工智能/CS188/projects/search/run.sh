#!/usr/bin/env bash
# L02-L03 搜索项目：py_compile 自检 + 运行（本轮只写不编译，集中编译由用户执行）
set -e
cd "$(dirname "$0")"
python3 -m py_compile maze_search.py   # 语法自检
python3 maze_search.py
