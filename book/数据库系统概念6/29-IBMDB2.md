# 第 29 章 IBM DB2

> **本章地图**：历史（**System R 1974–1979 → SQL 的诞生 → SQL/DS → DB2 for MVS 1983**）→ 产品线（**DB2 for LUW** vs **DB2 for z/OS**）→ 架构（实例 / 数据库 / 表空间 / 缓冲池 / agent 进程模型）→ **隔离级别**（**CS/RR/RS/UR**，UR 即脏读，DB2 独有）→ 特性（**pureXML**、**BLU Acceleration** 列存、**DPF** 无共享分区、**pureScale** 共享磁盘集群、HADR、federation）→ 与第 17–19 章架构分类的对照。

## 二、核心精讲

### 29.1 历史地位：关系数据库的源头之一
- **System R**（IBM San Jose Research，1974–1979）：第一个实现 **SQL（当时称 SEQUEL）** 的关系数据库原型；产出**两篇奠基论文**：
  - Astrahan et al.《System R: Relational Approach to Database Management》, ACM TODS 1976 —— 系统架构与 SQL；
  - Selinger et al.《Access Path Selection in a Relational Database Management System》, SIGMOD 1979 —— **基于代价的查询优化**（本书第 13 章的核心来源，Selinger 论文至今仍是优化器入门必读）。
- **SQL/DS**（1981）→ **DB2 for MVS**（1983）→ DB2 UDB（LUW）→ Db2（2017 更名）→ Db2 for z/OS 仍是大型机核心数据库的绝对主力。
- 🔧 学习价值：读 System R 的两篇论文可以同时打通**第 3 章（SQL）** 与 **第 13 章（查询优化）** 的源头；本书的优化器章节本质上是 Selinger 1979 的展开。

### 29.2 架构与存储
- 层次：**实例（instance）→ 数据库 → 表空间（tablespace，SMS 系统管理 / DMS 数据库管理 / 自动存储）→ 容器（container）→ 区 / 页（4K/8K/16K/32K）**。
- **缓冲池（bufferpool）**：可创建多个并分配给不同表空间（把热表与冷表物理隔离，是 DB2 调优的常用手段）。
- **进程/线程模型**：`db2sysc` 主进程 + 一组 **EDU（engine dispatchable unit）**；连接由 **agent（协调 agent / 子 agent）** 服务，可配置为**集中器（connection concentrator）**复用 agent（对应 pgbouncer 的作用）。DB2 for z/OS 则完全不同（地址空间 + MVS 子系统）。
- 日志：**主日志 + 辅助日志**（循环日志 vs 归档日志模式），对应 PG 的 WAL 段与 Oracle 的 redo log group。

### 29.3 隔离级别：DB2 的四档（本章最值得记住的差异点）
| 级别 | 缩写 | 含义 | 对应 |
| --- | --- | --- | --- |
| **Uncommitted Read** | **UR** | **允许脏读**（DB2 独有，Oracle/MySQL 默认没有） | Read Uncommitted |
| **Cursor Stability** | **CS** | 默认；只锁当前游标行（防止丢失更新，可能不可重复读） | ≈ Read Committed |
| **Read Stability** | **RS** | 锁住**查询返回的所有行**（其他事务不能改已见行，但可插入新行） | 介于 RC 与 RR 之间 |
| **Repeatable Read** | **RR** | 锁住**扫描到的所有行与范围**（含幻读防护） | ≈ Serializable（严格 2PL） |

- 🔧 关键差异：DB2 的 RR 是**锁实现**（严格 2PL + 范围锁），而 PostgreSQL 的 RR 是**快照隔离** —— 同名不同义是跨库迁移的经典陷阱（第 14、15 章）。
- **UR 的工程价值**：只读报表查询加 `WITH UR` 可**完全不加锁**，避免阻塞 OLTP（代价是可能读到未提交数据）；这是 DB2 运维里非常实用的手段。

### 29.4 关键特性
- **pureXML**（Db2 9, 2006）：原生存储 XML（不拆成关系表），支持 **XQuery** 与 XML 索引 → 直接对应第 23 章；🔧 是 XML 时代最彻底的原生方案（对比 Oracle XML DB 的 CLOB+索引路线）。
- **BLU Acceleration**（Db2 10.5, 2013）：**列存 + 内存 + 向量化 + 可操作压缩（字典编码直接在压缩数据上运算）** —— Raman et al., *DB2 with BLU Acceleration*, PVLDB 2013。🔧 是本书第 18/20 章「列存与向量化」思想的商业集大成实现，与 ClickHouse/DuckDB 属同一代技术。
- **DPF（Database Partitioning Feature）**：**shared-nothing 分区**（按分区键哈希分布，自动并行执行）→ 第 18 章的商业实现。
- **pureScale**（2009）：**shared-disk 集群 + CF（Cluster Caching Facility）** 集中管理全局锁与缓存一致性 → 第 17 章共享磁盘架构的典型（与 Oracle RAC 同类，但把锁管理集中在 CF 上，减少 ping）。
- **HADR（High Availability Disaster Recovery）**：基于日志传输的主备（同步/近同步/异步/超级异步四档），对应 Data Guard / 流复制。
- **Federation / Federation Server**：异构数据源联邦查询（对应 Presto/Trino 与 Calcite 的现代形态）。
- **工具**：`db2expln` / `db2exfmt`（执行计划，`db2exfmt` 输出的信息量在业界公认最详尽）、`RUNSTATS`（统计信息收集）、`REORG`（重组）、`db2advis`（索引建议）。

### 29.5 与其他产品的对照
| 维度 | Db2 LUW | Oracle | PostgreSQL | MySQL/InnoDB |
| --- | --- | --- | --- | --- |
| 并发控制 | 锁为主 + 部分 MVCC | undo 段 MVCC | 堆内 MVCC | undo 段 MVCC |
| 默认隔离 | **CS**（游标稳定性） | RC | RC | **RR**（SI+间隙锁） |
| 脏读选项 | **有（UR）** | 无 | 无 | 有（RU） |
| 集群 | pureScale（共享磁盘）/ DPF（无共享） | RAC（共享磁盘） | Citus / Patroni | Group Replication / InnoDB Cluster |
| 列存 | **BLU** | In-Memory | 扩展（cstore_fdw 等） | ClickHouse（独立） |

## 三、经典论文与原始文献

| 论文 | 出处 | 贡献 |
| --- | --- | --- |
| Astrahan et al.《System R: Relational Approach to Database Management》 | ACM TODS 1976 | 关系系统 + SQL 原型 |
| Selinger et al.《Access Path Selection in a Relational Database Management System》 | SIGMOD 1979 | **代价优化器**（第 13 章源头） |
| Chamberlin et al.《SEQUEL 2: A Unified Approach to Data Definition, Manipulation, and Control》 | IEEE ToSE 1976 | SQL 前身 |
| Raman et al.《DB2 with BLU Acceleration: So Much More than Just a Column Store》 | PVLDB 2013 | 列存 + 向量化 + 可操作压缩 |
| Baragiola et al.（pureXML 相关） | IBM Systems Journal 2006 | 原生 XML |
| 《DB2 pureScale》技术论文 | IBM | 共享磁盘集群 |
| Haerder & Reuter《Principles of Transaction-Oriented Database Recovery》 | 1983 | 恢复（Gray/System R 传统） |

## 四、近年研究与工业界开源实践

- **近年研究**：**列存上的可操作压缩**（BLU 提出后，成为 C-Store 系与 DuckDB/ClickHouse 的通用能力）；**混合负载的资源治理**（Db2 的 Workload Manager 对应现代的 cgroup / 云资源隔离）；**AI 驱动的优化器与索引推荐**（Db2 自调优内存管理器 STMM 是早期自治数据库尝试）。
- **工业界开源对照**（star 数 2026-09 实测）：
  - `clickhouse/clickhouse`（≈50.1k★）/ `duckdb/duckdb`（≈41.7k★）：体验 BLU 思想（列存 + 向量化 + 压缩上计算）的最佳开源替代。
  - `postgresql/postgres`（≈17k★）：用 `pg_stat_activity` + `pg_locks` 对照理解 DB2 的 CS/RS/RR 锁差异；PG 无 UR，可用 `READ UNCOMMITTED`（被降级为 RC）对比。
  - `apache/calcite`（≈5.2k★）：DB2 Federation 的现代开源等价物。
  - `apache/parquet-format` / `apache/arrow`（≈15k★ 量级）：BLU 的"向量化 + 列式内存格式"在开源世界的标准载体。

## 五、常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "DB2 的 RR 和 PG 的 RR 一样" | DB2 RR = 严格 2PL + 范围锁（真可串行化级），PG RR = 快照隔离 |
| 2 | "UR（脏读）是 bug 级选项" | 是**刻意提供的只读报表加速手段**，在不关心精确性的统计场景合理 |
| 3 | "CS 就是可重复读" | CS 只保证当前游标行；同一事务内两次查询可能不一致 |
| 4 | "pureScale 和 DPF 是一回事" | pureScale = 共享磁盘（高可用/扩展写）；DPF = 无共享（分析型并行） |
| 5 | 🔧 本书定位 | 与第 27、28 章一样属"产品案例"章；**真正值得带走的只有两件事**：System R/Selinger 的历史脉络（第 3、13 章的源头）与**四档隔离级别的语义差异**（第 14 章的最佳对照） |
