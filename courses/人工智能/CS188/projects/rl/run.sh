#!/usr/bin/env bash
# L13-L14 强化学习项目：py_compile 自检 + 运行（本轮只写不编译，用户自行执行）
set -e
cd "$(dirname "$0")"
python3 -m py_compile q_learning.py
python3 q_learning.py
