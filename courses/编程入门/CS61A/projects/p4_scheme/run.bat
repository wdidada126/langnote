@echo off
rem P4 运行脚本（Windows）。语法自检命令：
rem python -m py_compile utils.py scheme.py
rem 用法：run.bat            -> REPL
rem       run.bat --test     -> 自测
rem       run.bat demo.scm   -> 批处理
cd /d %~dp0
python scheme.py %*
