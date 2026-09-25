@echo off
rem p06 运行脚本（CS229 L16-L17）。先 py_compile 语法自检，再执行。
cd /d %~dp0
python -m py_compile kmeans.py em_gmm.py fa_kde.py || goto :err
python kmeans.py   || goto :err
python em_gmm.py   || goto :err
python fa_kde.py   || goto :err
goto :eof
:err
echo 运行失败：请确认 Python 与 numpy（唯一第三方依赖）。
exit /b 1
