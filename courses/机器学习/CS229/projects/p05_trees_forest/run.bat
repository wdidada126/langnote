@echo off
rem p05 运行脚本（CS229 L11-L12）。先 py_compile 语法自检，再执行。
cd /d %~dp0
python -m py_compile tree.py ensemble.py || goto :err
python tree.py      || goto :err
python ensemble.py  || goto :err
goto :eof
:err
echo 运行失败：请确认 Python 与 numpy（唯一第三方依赖）。
exit /b 1
