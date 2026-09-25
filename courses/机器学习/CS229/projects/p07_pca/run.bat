@echo off
rem p07 运行脚本（CS229 L08/L18）。先 py_compile 语法自检，再执行。
cd /d %~dp0
python -m py_compile pca.py ica_spectral.py || goto :err
python pca.py           || goto :err
python ica_spectral.py  || goto :err
goto :eof
:err
echo 运行失败：请确认 Python 与 numpy（唯一第三方依赖）。
exit /b 1
