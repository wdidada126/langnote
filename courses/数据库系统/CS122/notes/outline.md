# CS122 讲义骨架笔记（notes/outline.md）

> 骨架级要点，围绕 NanoDB 实现主线（详见 README 的讲次映射）。

## L01 数据库总览与 NanoDB 架构
- DBMS 五层在 NanoDB 包结构中的落点：storage / operator / parser / optimizer。
- 本课主线与 15-445 差异：从「能执行」升级到「执行得好（SQL 层 + 优化器）」。

## L02 存储与页管理
- 页内记录槽目录与 free-space；堆表随机 I/O 行为。
- 记录格式对 A1 性能/膨胀问题的影响。

## L03 Buffer Pool 与 pin/unpin
- pin 计数与淘汰时机：漏 pin → 数据被提前换出；漏 release → 内存泄漏。
- A1 任务本质：在读源码中定位生命周期错误。

## L04 DML 执行路径（A1）
- delete 标记删除 + 回收；update = delete + insert 的副作用。
- 提升 insert 吞吐同时抑制文件膨胀的策略选择。

## L05 SQL 解析与翻译
- 词法/语法 → AST；Translate 做名字绑定与星号/别名展开。

## L06 计划生成（A2）
- AST → 算子树；无索引时全表扫描 + 过滤。
- Volcano 迭代器接口在 NanoDB 的形态。

## L07 Join 实现（A2）
- Nested-loop：朴素 vs 索引；inner/outer 的 NULL 补齐。
- 用单测保证 inner/outer join 正确性（A2 明确要求）。

## L08 统计信息收集（A3）
- 表/列统计：元组数、页数、NDV、直方图；采样式 ANALYZE。

## L09 代价模型（A3）
- 各计划节点成本公式（I/O + CPU）；代价比较依赖基数估计。

## L10 选择率与统计传播（A3）
- 谓词选择率估计；输出元组统计随谓词/Join 沿树传播更新。

## L11 B+ 树索引
- 分裂/合并/游标；访问路径选择在计划生成中的作用。

## L12 聚合与 GROUP BY
- Hash 聚合 vs 排序聚合代价；分组后的统计传播。

## L13 子查询
- IN/EXISTS/标量子查询翻译与去相关；提升为 Join 的等价改写。

## L14 事务与 WAL 恢复
- WAL 协议、redo/undo 与检查点；在 NanoDB 中的最小实现。

## L15 优化器 Challenge
- 更强的连接顺序枚举与代价估计；从贪心到动态规划。
