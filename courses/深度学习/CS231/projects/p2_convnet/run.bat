@echo off
rem P2 语法检查模式：只编译不运行（本轮工程约定"只写不编译"）。
rem 真正运行演示：pip install numpy && python main.py
cd /d %~dp0
python -m py_compile data.py layers.py model.py gradient_check.py main.py
if errorlevel 1 (
  echo [P2] py_compile FAILED
  exit /b 1
)
echo [P2] py_compile OK —— 运行演示请执行: python main.py (需 numpy)
