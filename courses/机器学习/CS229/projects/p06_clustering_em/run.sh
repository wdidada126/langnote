#!/usr/bin/env bash
# p06 运行脚本（CS229 L16-L17）。先 py_compile 自检，再执行。
set -e
cd "$(dirname "$0")"
python3 -m py_compile kmeans.py em_gmm.py fa_kde.py   # 语法自检
python3 kmeans.py
python3 em_gmm.py
python3 fa_kde.py
