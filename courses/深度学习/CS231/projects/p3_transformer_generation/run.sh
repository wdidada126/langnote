#!/usr/bin/env bash
# P3 语法检查模式：只编译不运行（本轮工程约定"只写不编译"）。
# 真正运行演示：pip install numpy && python3 main.py all
set -e
cd "$(dirname "$0")"
python3 -m py_compile mlp.py data.py attention.py layernorm.py vit.py gan.py vae.py gradient_check.py main.py
echo "[P3] py_compile OK —— 运行演示请执行: python3 main.py all (需 numpy)"
