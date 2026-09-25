#!/usr/bin/env bash
# p08 运行脚本（CS229 L20-L21）。先 py_compile 自检，再执行。
set -e
cd "$(dirname "$0")"
python3 -m py_compile gridworld.py qlearn.py      # 语法自检
python3 gridworld.py
python3 qlearn.py
