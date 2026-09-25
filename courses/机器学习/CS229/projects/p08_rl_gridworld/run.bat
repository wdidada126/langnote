@echo off
rem p08 运行脚本（CS229 L20-L21）。先 py_compile 语法自检，再执行。
cd /d %~dp0
python -m py_compile gridworld.py qlearn.py || goto :err
python gridworld.py || goto :err
python qlearn.py    || goto :err
goto :eof
:err
echo 运行失败：请确认 Python 与 numpy（唯一第三方依赖）。
exit /b 1
