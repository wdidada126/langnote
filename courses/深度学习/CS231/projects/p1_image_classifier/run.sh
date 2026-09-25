#!/usr/bin/env bash
# P1 语法检查模式：只编译不运行（本轮工程约定"只写不编译"）。
# 真正运行演示：pip install numpy && python3 main.py
set -e
cd "$(dirname "$0")"
python3 -m py_compile data.py knn.py svm.py softmax.py gradient_check.py main.py
echo "[P1] py_compile OK —— 运行演示请执行: python3 main.py (需 numpy)"
