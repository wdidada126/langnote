#!/usr/bin/env bash
# L12 MDP 项目：py_compile 自检 + 运行（本轮只写不编译，用户自行执行）
set -e
cd "$(dirname "$0")"
python3 -m py_compile grid_mdp.py
python3 grid_mdp.py
