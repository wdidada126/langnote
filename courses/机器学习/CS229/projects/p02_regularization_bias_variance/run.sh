#!/usr/bin/env bash
# p02 运行脚本（CS229 L09）。先 py_compile 自检，再执行。
set -e
cd "$(dirname "$0")"
python3 -m py_compile poly_ridge.py bv_decomp.py    # 语法自检
python3 poly_ridge.py
python3 bv_decomp.py
