#!/usr/bin/env bash
# p09 运行脚本（CS229 L19）。先 py_compile 自检，再执行。
set -e
cd "$(dirname "$0")"
python3 -m py_compile hmm.py gibbs.py             # 语法自检
python3 hmm.py
python3 gibbs.py
