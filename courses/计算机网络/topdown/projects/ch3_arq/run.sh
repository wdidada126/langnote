#!/usr/bin/env bash
# 语法自检：python3 -m py_compile arq_sim.py
set -e
cd "$(dirname "$0")"
python3 -m py_compile arq_sim.py
python3 arq_sim.py
