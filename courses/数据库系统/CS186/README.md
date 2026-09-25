# UCB CS186 — Introduction to Database System（数据库系统导论）

## 课程信息

| 项目 | 内容 |
| --- | --- |
| 全称 | Introduction to Database System |
| 学校 | UC Berkeley |
| 主讲 | CS186 教学团队（近年讲师：Joe Davison、Henry Nguyen 等，以当期官网为准） |
| 教材 | 无指定教材（内容大体参照 Silberschatz《Database System Concepts》/ Ramakrishnan《Database Management Systems》） |
| csdiy 路径 | 数据库系统/CS186 |
| 最新期次 | 官网 cs186berkeley.net 当前学期（骨架按近年公开版整理，建议对照 Spring 2024 版） |
| 状态 | 骨架（notes / papers / projects 待后续填充） |

## 为什么学

- 回答「SQL 是如何被执行」的整条链路：SQL 查询怎么被拆解、优化、变成磁盘查询指令；高并发如何实现；故障恢复怎么做；什么是 NoSQL。
- 理论与实践并重：先建立关系型数据库内部细节的完整心智模型，再**动手用 Java 实现一个支持 SQL 并发查询、B+ 树索引和故障恢复的关系型数据库**（6 个 Project）。
- 实用角度：Project 中锻炼 SQL 与 NoSQL 查询编写能力，对构建全栈工程项目有直接帮助。
- csdiy 难度 🌟🌟🌟🌟🌟、约 150 学时——是 15-445 之外的另一条「从零造数据库」路线（Java 版，且包含 SQL 层，与 CS122 类似）。

## 先修与知识联系

- 先修：CS61A、CS61B、CS61C；语言 Java；预计学时 150 小时。
- 知识联系：与 CMU 15-445 互补——CS186 用 Java 且作业覆盖 SQL/NoSQL 使用层，15-445 用 C++ 且不含 SQL 层；后续进阶 CS346/CS122（查询优化专题）、15799（前沿）。OS 知识服务于 buffer pool 与并发控制。

## 讲义章节目录（按主题周整理，具体以当期官网 schedule 为准）

| 讲次 | 标题 | 阅读材料 |
| --- | --- | --- |
| L01 | 课程导论：数据库 vs 文件系统集成、数据模型 | 讲义 Ch1 |
| L02 | ER 模型与数据库设计 | 讲义 Ch2 |
| L03 | 关系模型：元组、键、完整性约束 | 讲义 Ch3 |
| L04 | 关系代数：选择/投影/连接/除 | 讲义 Ch4 |
| L05 | SQL 基础：DDL/DML、连接与嵌套查询 | 讲义 Ch5（配合 Project 1） |
| L06 | SQL 进阶：聚合、分组、窗口、修改查询 | 讲义 Ch5–6 |
| L07 | NoSQL 与半结构化数据：JSON/键值/列族 | 讲义 Ch7（配合 Project 2） |
| L08 | 存储与 I/O：页面、堆文件、记录布局 | 讲义 Ch8/13 |
| L09 | Buffer Pool 管理 | 讲义 Ch13/15 |
| L10 | 索引 I：为什么是 B+ 树 | 讲义 Ch11（配合 Project 3） |
| L11 | 索引 II：B+ 树插入/删除/分裂、游标 | 讲义 Ch11 |
| L12 | 查询执行 I：迭代器模型 | 讲义 Ch15/16 |
| L13 | 查询执行 II：排序（外部归并排序） | 讲义 Ch14（配合 Project 4） |
| L14 | 查询执行 III：连接算法（NLJ/索引/Sort-Merge/Hash） | 讲义 Ch14 |
| L15 | 查询优化 I：统计信息与基数估计 | 讲义 Ch16 |
| L16 | 查询优化 II：代价模型与连接顺序（动态规划） | 讲义 Ch19 |
| L17 | 事务与 ACID | 讲义 Ch17 |
| L18 | 并发控制 I：异常与串行化、2PL | 讲义 Ch17/19 |
| L19 | 并发控制 II：时间戳排序、快照隔离与 MVCC | 讲义 Ch19（配合 Project 5） |
| L20 | 死锁检测与处理 | 讲义 Ch19 |
| L21 | 恢复 I：WAL 与 ARIES 思想 | 讲义 Ch19（配合 Project 6） |
| L22 | 恢复 II：检查点、崩溃/介质故障恢复 | 讲义 Ch19 |
| L23 | 分布式数据库 I：复制、一致性、共识 | 讲义 Ch20 |
| L24 | 分布式数据库 II：分片、NewSQL、并行数据库 | 讲义 Ch21 |
| L25 | 课程总结：数据库全栈回顾（串起 6 个 Project） | 复习讲义 |

## 资源

- 课程网站：https://cs186berkeley.net/ ；课程视频：Bilibili BV13a411c7Qo
- 作业：6 个 Project（P1 SQL、P2 NoSQL、P3 B+ 树索引、P4 查询执行（排序/连接）、P5 事务与并发控制、P6 并行/恢复）
- 资源汇总：PKUFlyingPig/CS186（GitHub，含资源与作业实现）
