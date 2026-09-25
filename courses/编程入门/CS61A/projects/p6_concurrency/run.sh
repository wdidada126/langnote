#!/usr/bin/env bash
# p6 运行脚本。语法自检：python -m py_compile race.py gil_demo.py main.py
cd "$(dirname "$0")" && python main.py
