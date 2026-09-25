#!/usr/bin/env bash
# p01 运行脚本（CS229 L01-L03）。先做 py_compile 自检（只编译不运行产物），再依次执行。
set -e
cd "$(dirname "$0")"
python3 -m py_compile common.py linear.py gd_momentum.py logistic.py   # 语法自检
python3 linear.py
python3 gd_momentum.py
python3 logistic.py
