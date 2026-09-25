#!/usr/bin/env bash
# P4 运行脚本。语法自检：python -m py_compile utils.py scheme.py
# 用法：./run.sh [--test | demo.scm]
cd "$(dirname "$0")" && python scheme.py "$@"
