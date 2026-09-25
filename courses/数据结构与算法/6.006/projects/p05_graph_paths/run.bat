@echo off
rem p05 图遍历与最短路：语法自检 + 运行自测与实验
rem 仅编译检查（不执行）：python -m py_compile main.py
cd /d %~dp0
python -m py_compile main.py || goto :err
python main.py || goto :err
goto :eof
:err
exit /b 1
