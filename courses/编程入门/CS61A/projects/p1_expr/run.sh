#!/usr/bin/env bash
# P1 运行脚本（Linux/macOS/Git Bash）。语法自检命令：
# python -m py_compile rat.py expr.py main.py
cd "$(dirname "$0")" && python main.py
