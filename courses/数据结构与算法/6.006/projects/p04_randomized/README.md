# p04 随机化（randomization）

- 对应讲次：L26（随机化算法总纲、quickselect 期望分析）、L09/L10（BFS 数分量）、L03/L04（增长率口径）。
- 知识点：随机 pivot 的 quickselect（期望 Θ(n)，实验验证"工作量/n≈常数"）；中位数选取；Erdős–Rényi G(n,p) 生成与连通阈值 p=1/n 的巨分量涌现（图算法实验常用合成数据）。
- 文件：`main.py`（200 组对拍 + 两张实验表）。
- 运行：`run.bat` / `bash run.sh`；手动 `python -m py_compile main.py && python main.py`。
- 预期输出：quickselect 对拍通过；c = 工作量/n 在 n=2000→128000 基本持平（≈2–3）；G(n,p) 表在 p·n 跨过 1 时最大分量从 O(log n) 跳到 Θ(n)。
- 延伸：把随机 pivot 换成 median-of-three 看 c 的变化；用固定种子的"坏运气"演示最坏 Θ(n²)。
