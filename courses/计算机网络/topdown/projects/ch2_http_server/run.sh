#!/usr/bin/env bash
# 语法自检：python3 -m py_compile http_server.py
set -e
cd "$(dirname "$0")"
python3 -m py_compile http_server.py
python3 http_server.py
