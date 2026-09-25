@echo off
rem p02 运行脚本（CS229 L09）。先 py_compile 语法自检，再执行。
cd /d %~dp0
python -m py_compile poly_ridge.py bv_decomp.py || goto :err
python poly_ridge.py || goto :err
python bv_decomp.py  || goto :err
goto :eof
:err
echo 运行失败：请确认 Python 与 numpy（唯一第三方依赖）。
exit /b 1
