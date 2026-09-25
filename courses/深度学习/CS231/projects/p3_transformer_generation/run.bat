@echo off
rem P3 语法检查模式：只编译不运行（本轮工程约定"只写不编译"）。
rem 真正运行演示：pip install numpy && python main.py all
cd /d %~dp0
python -m py_compile mlp.py data.py attention.py layernorm.py vit.py gan.py vae.py gradient_check.py main.py
if errorlevel 1 (
  echo [P3] py_compile FAILED
  exit /b 1
)
echo [P3] py_compile OK —— 运行演示请执行: python main.py all (需 numpy)
