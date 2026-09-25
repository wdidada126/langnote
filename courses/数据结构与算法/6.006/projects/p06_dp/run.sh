#!/usr/bin/env bash
# p06 动态规划：语法自检 + 运行自测与实验
# 仅编译检查（不执行）：python -m py_compile main.py
set -e
cd "$(dirname "$0")"
python -m py_compile main.py
python main.py
