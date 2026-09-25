@echo off
rem p01 运行脚本（CS229 L01-L03）。先 py_compile 语法自检，再依次执行。
cd /d %~dp0
python -m py_compile common.py linear.py gd_momentum.py logistic.py || goto :err
python linear.py       || goto :err
python gd_momentum.py  || goto :err
python logistic.py     || goto :err
goto :eof
:err
echo 运行失败，请确认已安装 Python 与 numpy（唯一第三方依赖）。
exit /b 1
