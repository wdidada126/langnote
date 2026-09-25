# p08 摊还分析（amortization）

- 对应讲次：L19、L20。
- 知识点：动态数组三种增长策略的拷贝总账（聚合法直接计数）；DSU 四配置 find 步数对照（无秩无压缩退化、按秩 O(log n)、双优 ≈ O(α)）；迭代式全路径压缩实现。
- 文件：`main.py`（DynArray、DSU、600 操作 × 4 配置对拍"集合法"参考、账本表）。
- 运行：`run.bat` / `bash run.sh`；手动 `python -m py_compile main.py && python main.py`。
- 预期输出：×2 均摊拷贝 ≈ 1–2，+1 均摊 ~n/2；DSU 表中双优列均摊步数 < 3 且不随 n 涨。
- 延伸：把 DSU 接入 p05 做 Kruskal 最小生成树（L20 预告的 6.046 应用）。
