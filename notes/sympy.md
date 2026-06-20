# sympy

Python + SymPy
- 特点：开源免费，结合 SymPy 可进行符号运算。
- 适合场景：教育、编程爱好者、轻量级研究。
- 安装命令：
  ```bash
  pip install sympy
  ```
- 示例代码（求导）：
  ```python
  import sympy as sp

  x = sp.symbols('x')
  f = sp.sin(x)
  df = sp.diff(f, x)
  print(df)  # 输出 cos(x)
  ```
- 官网: [https://www.sympy.org/](https://www.sympy.org/)
