# p06 动态规划（dynamic programming）

- 对应讲次：L08（重叠子问题/memo/自底向上）、L04 对照（分治 vs DP）、L10（依赖顺序）。
- 知识点：编辑距离（三维转移 + 回溯操作序列）、矩阵链乘法（区间 DP + 括号化重构）、0-1 背包（表 + 方案重构）；Fibonacci 四写法的调用计数对比（指数 → 线性 → 常数空间）。
- 文件：`main.py`（四个 DP + 两个参考实现 + 60×3 组对拍 + 两张实验表）。
- 运行：`run.bat` / `bash run.sh`；手动 `python -m py_compile main.py && python main.py`。
- 预期输出：全部断言通过；fib 表显示 n=28 时裸递归约 1.2M 次调用 vs memo 57 次；编辑距离表的 ms/百万格近似恒定（Θ(mn) 实锤）。
- 延伸：背包改滚动数组 O(cap) 空间（L08 V4 模式）；矩阵链维数改随机大 n 观察 Θ(n³)。
