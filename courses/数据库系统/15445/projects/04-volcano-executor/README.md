# 04 — Volcano Executor（迭代/火山模型执行器）

- **对应讲次**：L12 Query Execution I（迭代器模型）
- **机制**：每个算子实现 `Init()/Next()` 的 pull 模型；驱动循环反复调用根 `Next()` 直到 nullopt。含 `SeqScan / Values / Filter / Project / Limit`，全部是**流水线（pipelined）算子**。统计 `tuples_in/out` 演示 LIMIT 早停如何"拉住"上游。
- **文件**：`main.cpp`。
- **测试覆盖**：`SELECT id FROM emp WHERE dept=10`、`WHERE age>30 LIMIT 2` 的早停证明、Values 常量行。

## 构建
- Windows：`build.bat`　Linux/macOS：`bash build.sh`

## 与讲义的接缝
- `Next()` 逐元组 + 虚函数 = L12 所述"火山模型原罪"（每元组一次函数调用），L13 向量化正是为消除它。
- 这里全是 pipelined 算子；对比 `05-agg-sort` 里的 blocking 算子，理解"pipeline breaker"。
- 对应 BusTub `src/execution/*_executor.cpp` 的 `Next()`。
