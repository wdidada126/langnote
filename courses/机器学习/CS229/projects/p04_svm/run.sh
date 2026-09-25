#!/usr/bin/env bash
# p04 运行脚本（CS229 L06-L07）。先 py_compile 自检，再执行。
set -e
cd "$(dirname "$0")"
python3 -m py_compile hinge_sgd.py smo_toy.py     # 语法自检
python3 hinge_sgd.py
python3 smo_toy.py
