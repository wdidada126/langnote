@echo off
rem P3 运行脚本（Windows）。语法自检命令：
rem python -m py_compile linked.py trees.py odict.py minisql.py main.py
cd /d %~dp0
python main.py
