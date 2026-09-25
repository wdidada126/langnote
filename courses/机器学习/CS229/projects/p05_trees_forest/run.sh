#!/usr/bin/env bash
# p05 运行脚本（CS229 L11-L12）。先 py_compile 自检，再执行。
set -e
cd "$(dirname "$0")"
python3 -m py_compile tree.py ensemble.py         # 语法自检
python3 tree.py
python3 ensemble.py
