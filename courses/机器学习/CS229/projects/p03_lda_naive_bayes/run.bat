@echo off
rem p03 运行脚本（CS229 L05）。先 py_compile 语法自检，再执行。
cd /d %~dp0
python -m py_compile gda_qda.py naive_bayes.py || goto :err
python gda_qda.py      || goto :err
python naive_bayes.py  || goto :err
goto :eof
:err
echo 运行失败：请确认 Python 与 numpy（唯一第三方依赖）。
exit /b 1
