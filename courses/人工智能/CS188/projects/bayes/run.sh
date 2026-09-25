#!/usr/bin/env bash
# L09-L10 贝叶斯推断项目：py_compile 自检 + 运行（本轮只写不编译，用户自行执行）
set -e
cd "$(dirname "$0")"
python3 -m py_compile bayes_inference.py
python3 bayes_inference.py
