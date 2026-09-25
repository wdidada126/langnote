# CMU 15-445 — Database Systems（数据库系统）【CORE】

> 状态：全量（2026-09）。本 README 含全章节目录（Fall 2023 官方 26 讲 L00–L25）；notes / papers / projects 正文已全部完成。

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 全称 | 15-445/645 Database Systems |
| 学校 | Carnegie Mellon University |
| 主讲 | Andy Pavlo（数据库领域大牛；名言「这个世界上我只在乎两件事，一是我的老婆，二就是数据库」） |
| 教材 | Database System Concepts（Silberschatz 等；课程以 Andy 自写 Notes/Slides 为主，无必读课本） |
| csdiy 路径 | 数据库系统/15445 |
| 最新期次 | Fall 2023（15445.courses.cs.cmu.edu/fall2023；本 README 章节目录即按 F23 官方 schedule 整理） |
| 状态 | 全量（2026-09） |

## 为什么学

- csdiy 评价：质量极高、资源极全的 Database 入门课。Faculty 与 CMU Database Group 把基础设施（Autograder、Discord）与课程资料（Lectures、Notes、Homework）**完全开源**，自学者可获得几乎等同 CMU 本校的体验。
- 教学用数据库 **Bustub（BusTub）**：为这门课专门开发的方向磁盘的关系型数据库，你要在 4 个 Project 中实现它的关键部件——Buffer Pool Manager（内存管理）、B+ Tree 索引（存储引擎）、Query Executors & Optimizer（算子与优化器）、Concurrency Control（并发控制），分别对应 Project #1–#4。
- 用 `bustub-shell` 实时观测自己实现部件的正反馈非常足；Bustub 本身作为中小型 C++ 项目，其构建、代码规范、单元测试也值得学习。
- 学完后推荐阅读论文 **Architecture of a Database System**（Hellerstein/Stonebraker/Hamilton）建立全局视野。

## 先修与知识联系

- 先修：C++、数据结构与算法、CMU 15-213（CS:APP，CMU 校内 enroll 的先修要求）；难度 🌟🌟🌟🌟；预计学时 100 小时。
- 作业全景：5 个 Project + 5 个 Homework（历史上 Project 内容随学期调整：F19 P2 哈希索引/P4 日志恢复、F20 P2 B 树/P4 并发、F21/F22 P1 缓存池+P2 哈希索引+B+树+P4 并发、S23 P0 起 Copy-On-Write Trie；2020 年前版本已停维护，F19 的 Logging&Recovery Project 已 broken，不建议做）。
- 知识联系：与 UCB CS186（Java 全栈含 SQL 层）互为镜像——15-445 不含 SQL 层，专注存储/索引/执行/并发内核；进阶方向 CMU 15-721（主存数据库，官方推荐的后续课程）、Caltech CS122 与 Stanford CS346（SQL 层/查询优化实现）、CMU 15-799（前沿专题）。

## 讲义全章节目录（Fall 2023 官方 schedule，L00–L25）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L00 | Course Overview（课程与教学安排，纯线上形式） | 课程主页 / Syllabus |
| L01 | The Relational Model（关系模型与关系代数） | BusTub Notes；Silberschatz Ch3–4 |
| L02 | Advanced SQL（高级 SQL） | Silberschatz Ch3–4 / 课程讲义 |
| L03 | Database Storage I（数据库存储·上：磁盘与数据组织） | 课程讲义；LSM/页存储相关章节 |
| L04 | Database Storage II（数据库存储·下：页结构与块设备交互） | 课程讲义 |
| L05 | Storage Models and Compression（存储模型与压缩：行存/列存） | 课程讲义；C-Store 相关 |
| L06 | Memory Management（内存管理：缓冲池调度与分配） | 课程讲义；Project #1 关联 |
| L07 | Hash Tables（散列表：开放寻址/链地址在 DBMS 中的实现） | 课程讲义 |
| L08 | Tree-Based Indexes（B/B+ 树索引构建、查找与维护） | 课程讲义；Project #2 关联 |
| L09 | Index Concurrency Control（索引的多线程并发控制） | Lehman-Yao/B-link tree 相关 |
| L10 | Sorting and Aggregations（外部排序与分组聚合） | 课程讲义 |
| L11 | Join Algorithms（连接算法：NLJ/Sort-Merge/Hash） | 课程讲义；Morsel-Parallel 参考 |
| L12 | Query Execution I（查询执行·上：火山迭代器模型） | 课程讲义；Project #3 关联 |
| L13 | Query Execution II（查询执行·下：向量化与并行执行） | MonetDB/X100、Morsel-Driven 论文 |
| L14 | Query Planning and Optimization（查询计划与优化：代价模型） | Selinger 1979；Project #4 关联 |
| L15 | Concurrency Control Intro（并发控制理论：事务与隔离级别） | 课程讲义；Adya 1998 |
| L16 | Concurrency Control Based on Two-Phase Locking（2PL） | 课程讲义；Project #5 关联 |
| L17 | Concurrency Control Based on Timestamp Ordering（时间戳排序） | 课程讲义 |
| L18 | Multi-Version Concurrency Control（MVCC：快照读与 undo 管理） | 课程讲义 |
| L19 | Database Logging（日志：WAL、redo/undo、检查点） | 课程讲义；ARIES 论文 |
| L20 | Database Recovery（恢复：介质故障、ARIES、崩溃重启） | Mohan 1992 ARIES |
| L21 | Introduction to Distributed Databases（分布式导论：分片/复制/共识） | 课程讲义；CQ 系列 |
| L22 | Distributed OLTP Database Systems（分布式 OLTP：跨节点事务） | Spanner / Percolator / TiDB 论文 |
| L23 | Distributed OLAP Database Systems（分布式 OLAP：MPP 分析负载） | Redshift / Snowflake 论文 |
| L24 | Guest Speaker: Cheng Chen (SingleStore)（嘉宾讲座：商业内存原生数据库） | 讲义/录像 |
| L25 | Final Review + Systems Potpourri（期末串讲与系统杂项） | 复习讲义 |

> 注：假期停课、期中考与 Project 节点未列入；各讲 Notes/Slides 在官网逐讲公开，Fall 2022 视频已在 YouTube 全开源。

## 资源

- 课程网站：Fall 2019 / 2020 / 2021 / 2022 / Spring 2023（历史期次）；最新期以官网为准。
- Bustub 代码与作业：github.com/cmu-db/bustub。
- 通关指南：xzhseh《CMU 15-445/645 (Spring 2023) Database Systems 通关指北》；作业实现参考 ysj1173886760/Learning: db（含 Homework 解与自动判分脚本；应 Andy 要求无 Project 实现）。
- 非官方 Discord：历史聊天记录是极佳的踩坑参考。

## 目录内容说明

- `notes/`：L00–L25 逐讲中文笔记（共 26 篇），每篇含核心概念+机制、前后讲联系、跨课程联系（CSAPP/6.S081/6.824/CS143/6.006 等）、开源项目应用（PostgreSQL/InnoDB/RocksDB/DuckDB/TiDB/CockroachDB/sqlite）、延伸阅读。
- `papers/papers.md`：经典论文表（Codd 关系模型、Bayer&McCreight B 树、Selinger/System-R、Volcano/Graefe、MonetDB-X100、Lehman-Yao B-link、Leviton Bw-tree、ARIES/Mohan、SSI/Cahill、Spanner/Percolator、Redshift/Snowflake、Morsel 并行、C-Store 等）＋近五年(2021–2026)精选（DuckDB/Umbra/ClickHouse/lakehouse/Iceberg·Delta/HNSW·DiskANN/learned index·optimizer/Text-to-SQL 等）＋知识点↔开源映射表。
- `projects/`：8 个 C++17（标准库 only）配套项目，只写不编译，均自带测试 main + `build.bat`/`build.sh` + README；总表见 `projects/README.md`。分别为 01 缓冲池(Clock 置换+固定计数)、02 B+树(插入/分裂+范围扫描)、03 slotted page+堆表、04 火山执行器、05 聚合/排序算子、06 迷你 SQL 解析接执行器、07 WAL redo/undo 恢复、08 2PL 锁管理器(冲突矩阵+死锁等待图)。

## 学习进度建议

1. 通读 L00–L02 建立数据模型与 SQL 底座；
2. L03–L06 存储/内存三件套配 projects 01/03；
3. L07–L09 索引配 projects 02；
4. L10–L14 查询处理配 projects 04/05/06；
5. L15–L20 事务与恢复配 projects 07/08；
6. L21–L25 分布式/前沿——衔接 MIT 6.824 与 CMU 15-721。
