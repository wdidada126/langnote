# CS186 论文与应用清单（papers.md）

## 经典论文

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| Access Path Selection in a Relational Database Management System (Selinger et al.) | 1979 | System R 优化器：统计信息 + 代价模型 + 连接顺序动态规划，CBO 的开山之作 | L15–L16 |
| The Ubiquitous B-Tree (Comer) | 1979 | B 树/B+ 树索引结构系统性综述，索引章节标准参考 | L10–L11 |
| Concurrency Control and Recovery in Database Systems (Bernstein, Hadzilacos, Goodman) | 1987 | 并发控制与恢复理论的集大成综述（书） | L17–L22 |
| A History and Evaluation of System R (Selinger et al.) | 1981 | SQL 关系系统的原型验证：优化器与并发控制的工程化起点 | L05/L16 |
| Architecture of a Database System (Hellerstein, Stonebraker, Hamilton) | 2007 | 用一张图讲清 DBMS 全栈组件，与本课六 Project 一一对应 | L01/L25 |
| ARIES: A Transaction Recovery Method (Mohan et al.) | 1992 | Steal+No-force 下的 redo/undo 恢复算法与日志协议 | L21–L22 |
| A Critique of ANSI SQL Isolation Levels (Adya) | 1998 | 指出标准隔离级别定义的漏洞，提出弱隔离理论 | L18–L19 |
| Dynamo: Amazon's Highly Available Key-value Store (DeCandia et al.) | 2007 | 无主复制 + quorum + 最终一致的代表性 NoSQL 系统 | L07/L23 |
| MapReduce: Simplified Data Processing (Dean & Barroso) | 2004 | 大规模并行数据处理的编程模型，分片/并行执行的思想源头 | L24 |
| Spanner: Google's Globally-Distributed Database (Corbett et al.) | 2012 | 外部一致性 + TrueTime，NewSQL 分布式数据库标杆 | L23–L24 |
| Morsel-Driven Parallelism (Leis et al.) | 2014 | 多核并行查询执行的弹性分区调度 | L24 |
| The Design and Implementation of Modern Column-Oriented Database Systems (Abadi et al.) | 2008 | 列存为何赢分析负载：压缩、扫描、谓词下推 | L08/L24 |
| Bigtable: A Distributed Storage System (Chang et al.) | 2006 | LSM-Tree 落地的分布式列族存储原型 | L07 |

> 填正式笔记时以上表「关联讲次」为准逐条精读；每条目均有免费电子版可查。

## 近 5 年论文（2021–2026）

| 标题 | 年份 | 一句话贡献 | 关联讲次 |
| --- | --- | --- | --- |
| Lakehouse: A New Generation of Open Platforms that Unify Data Warehousing and Advanced Analytics (Armbrust et al.) | 2021 | 数据湖+仓库融合架构（Databricks 提出），存储层新范式 | L07/L24 |
| BtrBlocks: Efficient Column-Oriented Compression for Data Analytics (Kohn, Leis, Marks) | 2023 | 级联编码把列存压缩率/速度推到新高度 | L08/L15 |
| A Concurrency Control Story of Two Locked Copies (Wang et al., USENIX ATC) | 2021 | 无锁 B+ 树并发新方案，教科书级并发实验分析 | L11/L18 |
| Umbra: A Disk-Based System with In-Memory Performance 的后续 (Fretags et al.) | 2021–2023 系列 | 编译器生成代码 + 指针钉住的混合存储引擎 | L12–L16 |

## 知识点在开源项目中的应用

| 知识点 | 开源项目 | 说明 |
| --- | --- | --- |
| B+ 树索引 | MySQL/InnoDB、PostgreSQL、SQLite | InnoDB 聚簇索引即 L10–L11 的工业版 |
| LSM-Tree（NoSQL 存储） | RocksDB、Cassandra、HBase | L07 列族/键值系统的引擎层 |
| Buffer Pool | PostgreSQL `src/bufmgr.c`、InnoDB buffer pool | L09 的 clock/淘汰策略对照 |
| 迭代器执行/向量化 | DuckDB、ClickHouse | L12 火山模型→向量化演进 |
| 查询优化器 | PostgreSQL planner、Calcite、DuckDB | L15–L16 统计/代价/连接枚举 |
| MVCC/2PL | PostgreSQL（快照+SSI）、MySQL InnoDB（RR+间隙锁） | L18–L19 隔离级别实况 |
| WAL/ARIES | PostgreSQL/InnoDB redo log、etcd/RocksDB WAL | L21–L22 恢复路径 |
| 分布式复制/共识 | CockroachDB、TiDB（Raft） | L23–L24 Spanner 思路开源实现 |
