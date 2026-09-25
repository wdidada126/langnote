# CS122 论文与应用清单（papers.md）

## 经典论文

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| Access Path Selection in a Relational Database Management System (Selinger et al.) | 1979 | System R 代价优化器奠基之作：统计 + 代价 + 连接顺序 DP，A3 与 Challenge 的蓝本 | L08–L10/L15 |
| The Design and Implementation of Modern Column-Oriented Database Systems (Abadi et al.) | 2008 | 列存统计/谓词选择率优势的实证分析 | L08/L12 |
| The Volcano Optimizer Generator (Graefe) | 1993 | 规则驱动的扩展式优化器框架，理解「规则改写 + 枚举」的经典 | L06/L15 |
| Query Execution and Query Scheduling in Database Systems (Graefe 综述) | 1993 | 迭代器/排序/哈希算子体系化综述 | L06/L12 |
| Database Buffer Management (Breen, ACM Computing Surveys) | 1984 | 缓冲池管理综述，pin/淘汰策略源头 | L03 |
| The Ubiquitous B-Tree (Comer) | 1979 | B/B+ 树系统综述 | L11 |
| Optimal Query Processing Strategies for Subqueries (Graefe & Kim) | 1988 | 子查询去相关与执行策略的经典处理方案 | L13 |
| ARIES: A Transaction Recovery Method (Mohan et al.) | 1992 | WAL 恢复标准算法 | L14 |
| Architecture of a Database System (Hellerstein, Stonebraker, Hamilton) | 2007 | DBMS 全栈架构综述，定位本课各 Assignment 在系统中的位置 | L01 |
| Morsel-Driven Parallelism (Leis et al.) | 2014 | 现代并行执行/优化的调度模型 | L15 |
| How Good Are Query Optimizers, Really? (Leis et al.) | 2015 | 用 JOB 基准揭示基数估计是优化器最大短板 | L09–L10 |

## 近 5 年论文（2021–2026）

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| BtrBlocks: Efficient Column-Oriented Compression (Kohn, Leis, Marks) | 2023 | 列压缩新标杆，统计与选择率估计受益 | L08/L12 |
| Unicorn: Error-Optimized Query Planning (Rios, Lu et al.) | 2023 | 以基数估计误差为代价函数的学习型优化器路线 | L15 |
| Bao: Making Learned Query Optimization Practical (Marcus, Papaemmanouil) | 2021 | 用提示集 + 模型选择接管传统优化器决策 | L15 |
| Lakehouse: A New Generation of Open Platforms (Armbrust et al.) | 2021 | 湖仓上统计收集与代价估计的新场景 | L08 |

## 知识点在开源项目中的应用

| 知识点 | 开源项目 | 说明 |
| --- | --- | --- |
| SQL 解析/翻译 | PostgreSQL parse/analyze、Calcite | L05 的工业级对照 |
| 计划生成与迭代器执行 | DuckDB、Calcite Enumerable | L06/L12 火山模型 |
| 代价优化器 | PostgreSQL planner、Calcite Volcano planner | L06–L10/L15 直接对应 |
| 统计与选择率 | PostgreSQL ANALYZE/直方图、MySQL histogram (8.0) | L08–L10 落地 |
| 子查询去相关 | Calcite 规则集、CockroachDB optimizer | L13 |
| B+ 树 | InnoDB、SQLite、LMDB(B 树) | L11 |
| Buffer Pool | PostgreSQL bufmgr、InnoDB | L03 |
| WAL | PostgreSQL/InnoDB/MongoDB (WiredTiger) | L14 |
