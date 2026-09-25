# 06 — Mini SQL（子集解析 + 接执行器）

- **对应讲次**：L02 Advanced SQL → L12 执行 → L14 规划（把 SQL 串到算子树）
- **机制**：手写 **词法分析 + 递归下降解析器**，支持子集语法
  `SELECT <cols|*> FROM <t> [WHERE <cond> [AND ...]] [ORDER BY <col> [DESC]]`，cond 为 `col {=,!=,<,<=,>,>=} <int>`；
  解析成 `Query` AST → `Planner` 生成 `SeqScan → Filter → OrderBy → Project` 火山算子树 → 执行。
- **文件**：`main.cpp`。
- **测试覆盖**：投影裁剪、`*` 全列、AND 复合谓词、ORDER BY DESC、非法 SQL 抛异常。

## 构建
- Windows：`build.bat`　Linux/macOS：`bash build.sh`

## 与讲义的接缝
- "书写顺序 ≠ 执行顺序"：解析保留语义、Planner 决定算子顺序（谓词下推的雏形 = 先 Filter 再 Project）。
- 这正是 CS143 的"源码→AST→IR→执行"在数据库里的翻版（L14 类比）。
- 可扩展点：加 `GROUP BY` 复用 05 的 HashAgg；加 `JOIN` 复用 L11 三算法。
