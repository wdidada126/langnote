#!/usr/bin/env bash
# p03 运行脚本（CS229 L05）。先 py_compile 自检，再执行。
set -e
cd "$(dirname "$0")"
python3 -m py_compile gda_qda.py naive_bayes.py    # 语法自检
python3 gda_qda.py
python3 naive_bayes.py
