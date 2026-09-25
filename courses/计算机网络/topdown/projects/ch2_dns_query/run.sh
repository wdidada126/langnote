#!/usr/bin/env bash
# 语法自检：python3 -m py_compile dns_query.py
set -e
cd "$(dirname "$0")"
python3 -m py_compile dns_query.py
python3 dns_query.py "${1:-www.example.com}"
