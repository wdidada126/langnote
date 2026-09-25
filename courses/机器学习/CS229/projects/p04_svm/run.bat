@echo off
rem p04 运行脚本（CS229 L06-L07）。先 py_compile 语法自检，再执行。
cd /d %~dp0
python -m py_compile hinge_sgd.py smo_toy.py || goto :err
python hinge_sgd.py || goto :err
python smo_toy.py   || goto :err
goto :eof
:err
echo 运行失败：请确认 Python 与 numpy（唯一第三方依赖）。
exit /b 1
