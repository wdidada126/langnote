@echo off
rem p09 运行脚本（CS229 L19）。先 py_compile 语法自检，再执行。
cd /d %~dp0
python -m py_compile hmm.py gibbs.py || goto :err
python hmm.py    || goto :err
python gibbs.py  || goto :err
goto :eof
:err
echo 运行失败：请确认 Python 与 numpy（唯一第三方依赖）。
exit /b 1
