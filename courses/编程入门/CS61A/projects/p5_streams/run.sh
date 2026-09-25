#!/usr/bin/env bash
# p5 运行脚本。语法自检：python -m py_compile streams.py sieve.py
cd "$(dirname "$0")" && python sieve.py
