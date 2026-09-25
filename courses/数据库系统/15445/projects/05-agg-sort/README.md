# 05 — Aggregation & Sort Operators（聚合/排序算子）

- **对应讲次**：L10 Sorting and Aggregations；呼应 L12 的 blocking 算子概念
- **机制**：在迷你火山模型里实现两个**阻塞算子**——
  - `Sort`：Init 时吃光子算子全部输入、按主键+tie 列稳定排序，再逐行吐出（pipeline breaker）；
  - `HashAgg`：内存哈希表 `group_key -> 累加器`，支持 SUM/COUNT/AVG/MIN/MAX，按首见序分组输出（对应 L10 hash-based aggregation）。
- **文件**：`main.cpp`。
- **测试覆盖**：排序输出有序、`GROUP BY dept` 各聚合值正确、`HashAgg` 复合 `Sort`（GROUP BY 后 ORDER BY SUM desc）。

## 构建
- Windows：`build.bat`　Linux/macOS：`bash build.sh`

## 与讲义的接缝
- Sort 一次性物化全部输入 = L10 外部排序"内存放不下要溢写"的那个"内存"边界；本项目假设能装下（真实 spill 见 BusTub/Postgres）。
- HashAgg 溢出应走 L10 的递归哈希分区（grace partitioning）——README 里作为延伸练习。
- 两算子组合演示"物化点"：优化器（L14）据此切 pipeline 段。
