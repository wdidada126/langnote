#!/usr/bin/env bash
# p07 运行脚本（CS229 L08/L18）。先 py_compile 自检，再执行。
set -e
cd "$(dirname "$0")"
python3 -m py_compile pca.py ica_spectral.py      # 语法自检
python3 pca.py
python3 ica_spectral.py
