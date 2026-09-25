#!/usr/bin/env bash
# 语法自检：python3 -m py_compile congestion_sim.py
set -e
cd "$(dirname "$0")"
python3 -m py_compile congestion_sim.py
python3 congestion_sim.py
