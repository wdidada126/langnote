# 第 27 章 PostgreSQL

> **本章地图**：POSTGRES 项目谱系（Ingres → Postgres 1986 → PostgreSQL 1996）→ **架构**（进程模型、共享内存、存储结构）→ **与标准的差异 / 独特特性**（继承、UDT、UDF、规则系统、数组与 JSONB、部分索引与表达式索引、可扩展索引 GIN/GiST/SP-GiST/BRIN、FDW）→ **事务与并发**（堆内 MVCC + 快照、**HOT 更新**、autovacuum、SSI）→ **可靠性**（WAL + PITR、流式与逻辑复制）→ 扩展生态（PostGIS/TimescaleDB/Citus/pgvector）。

## 二、核心精讲

### 27.1 历史与定位
- **Ingres**（1974，Stonebraker/ Wong；QUEL 语言）→ **Postgres**（1986，*The Design of Postgres*, SIGMOD 1986：ADT、规则系统、多版本并发控制）→ **Postgres95**（Andrew Yu / Jolly Chen 改写为 SQL）→ **PostgreSQL 6.0**（1996，国际化命名）→ 至今 30 年持续演进（2025 年为 17.x 系列）。
- 定位：**对象-关系数据库**（第 22 章理论的活样板）+ **最先进的开源关系数据库** + **可扩展的数据库平台**（PostGIS 等扩展使其事实上成为"多模数据库框架"）。
- 🔧 为什么值得深读源码：PostgreSQL 是**教科书算法实现最完整、代码最可读**的开源数据库（B+ 树 `nbtree`、缓冲区 `bufmgr`、WAL `xlog`、优化器 `planner`、执行器 `executor` 一一对应本书第 11–16 章）。

### 27.2 架构
- **进程模型**（与 MySQL 的线程模型相对）：`postmaster` 主进程 fork 出每个连接的 backend 进程；后台进程：`checkpointer`、`background writer`、`walwriter`、`autovacuum launcher`、`logical replication launcher`、`archiver`。
  - 🔧 代价：连接开销大（~几 MB/连接）→ 高并发必须上 **pgbouncer**（transaction pooling）；社区长期讨论改线程模型。
- **共享内存**：`shared_buffers`（数据页缓存，官方建议 25% 内存，与 OS page cache 双缓存）、`WAL buffers`、`CLOG/CommitTs`、`lock space`。
- 存储结构：**堆表（heap）+ 索引分离**；每个元组带系统列 `xmin/xmin`（插入/删除事务 ID）、`ctid`（物理位置）、`infomask`。
  - 🔧 **"索引不存版本信息"**：索引项指向堆元组（line pointer），更新会新增堆元组并更新**所有**索引 —— 这正是 **HOT 更新**（Heap Only Tuple，只更新非索引列时不写新索引项）优化的价值所在（8.3 引入）。

### 27.3 与 SQL 标准/其他库的差异与独特特性
- **继承**（`INHERITS`，第 22 章）+ **分区**（声明式分区，10+ 用继承实现、现在原生支持 range/list/hash）。
- **可扩展类型系统**：`CREATE TYPE`（复合/枚举/range/domain）、`CREATE OPERATOR`、`CREATE FUNCTION`（PLpgSQL/C/Python/Perl/TCL）、`CREATE EXTENSION`。
- **`jsonb`**（9.4）：二进制 JSON，支持 GIN 索引与 `jsonb_path_query`，是「半结构化入库」的最佳实践（对比 MySQL 的 JSON 类型与 MongoDB）。
- **索引类型**（第 11 章的现实延伸）：**B-tree**（默认）、**Hash**、**GiST**（通用搜索树，R-树/全文/几何）、**SP-GiST**（空间分区，quadtree/k-d）、**GIN**（倒排，jsonb/数组/全文/ trigram）、**BRIN**（块级摘要，超大时序表神器）。
  - **部分索引**（`WHERE` 子句）与**表达式索引**（`lower(col)`）是 PostgreSQL 的独门优化手段。
- **FDW（Foreign Data Wrapper）**：把外部数据源（MySQL/CSV/Parquet/S3）当作表 → 联邦查询（第 19 章的开源落地）。
- **规则系统 vs 触发器**：`CREATE RULE`（查询重写，脆弱）与 `CREATE TRIGGER`（事件驱动，推荐）。

### 27.4 事务、并发与清理
- **MVCC 实现**：更新 = 插入新版本 + 标记旧版本（不是把旧版本搬到 undo 段），旧版本留在堆中 → **表膨胀（bloat）** 与 **autovacuum** 的存在理由。
- **可见性判断**：`snapshot`（xmin/xmax/xip 数组）+ 元组 `xmin/xmax` + **CLOG（提交日志）** + hint bits（首次访问时缓存提交状态以加速）。
- **隔离级别**：RC / RR（**快照隔离**，在 PG 9.1 前 RR 即 SI）/ **Serializable（SSI，见 15 章）**。🔧 PG 的 RR **不是**标准 RR（无幻读但允许写偏斜），需要用 Serializable 或显式 `FOR UPDATE`。
- **真空（VACUUM）**：回收死元组空间、冻结事务 ID（**防止 32 位 XID 回卷，这是运维头号事故**）、更新可见性映射（VM）与统计信息（`ANALYZE`）。
  - 🔧 工程要点：长事务会阻塞 vacuum 回收（**"长事务导致表膨胀"**），`autovacuum_vacuum_scale_factor` 对大表需要调小，或用分区 + 独立调优。

### 27.5 可靠性与复制
- **WAL + PITR**：`archive_mode` + 基础备份（`pg_basebackup`）+ WAL 归档 → 任意时间点恢复；`pg_waldump` 可直读 WAL（学习 ARIES 的最佳工具）。
- **流式复制**（物理，字节级同步，备库只读）、**逻辑复制**（`wal2json`/pgoutput → 表级订阅，支持跨版本升级与 CDC）、**同步/仲裁提交**（`synchronous_commit`、`synchronous_standby_names`）。
- 🔧 生态工具：`pgbackrest`、`barman`（备份）、`pgbouncer`（连接池）、`patroni`（高可用 + 自动切换）、`Debezium`（CDC，第 16 章逻辑解码的现实应用）。

## 三、经典论文与原始文献

| 论文 | 出处 | 贡献 |
| --- | --- | --- |
| Stonebraker & Rowe《The Design of Postgres》 | SIGMOD 1986 | ADT、规则、多版本的原始设计 |
| Stonebraker & Kemnitz《The POSTGRES Next-Generation Database Management System》 | CACM 1991 | 系统综述 |
| Momjian《PostgreSQL: Introduction and Concepts》 | 2001（书，官方免费） | 官方入门 |
| PostgreSQL 官方文档（Internals / MVCC / WAL 章节） | postgresql.org/docs | 权威一手资料 |
| Cahill《Serializable Isolation for Snapshot Databases》 | SIGMOD 2008 | PG 9.1 SSI |
| Zimányi et al.《MobilityDB》 | ACM TODS 2020 | 扩展生态范例 |

## 四、近年研究与工业界开源实践

- **近年研究**：**异步 I/O 与直连存储**（PG 18 引入 `io_method`，社区长期争论的 `shared_buffers` vs 直 I/O 问题）；**向量化执行**（PG 17 的列式实验、`pg_analytics` / Hydra / ParadeDB）；**JIT 与并行查询**（9.6 并行 seq scan / agg，11 并行 hash join）；**pgvector 与混合检索**（pgvectorscale，SIGMOD 2025 系统论文候选）。
- **工业界开源**（star 数 2026-09 实测）：
  - `postgresql/postgres`（≈17k★）：主仓库。
  - `postgis/postgis`（≈2.2k★）：空间扩展（第 25 章）。
  - `pgvector/pgvector`（≈23.2k★）：向量检索扩展，RAG 时代最热扩展。
  - `citusdata/citus`：分片扩展（shared-nothing，第 17/18 章落地）。
  - `timescale/timescaledb`：时序超表（自动分区 + 压缩）。
  - `pgbackrest/pgbackrest`、`patroni/patroni`、`pschlump`? 等运维生态。
  - `zalando/pg_view`?/ `postgresml/postgresml`：in-database ML（第 20 章）。

## 五、常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "PG 的 RR 就是标准可重复读" | 是**快照隔离**：无幻读但有写偏斜；需 Serializable(SSI) |
| 2 | "autovacuum 开着就不用管膨胀" | 长事务、复制槽、未使用的 prepared transaction 会阻止回收 → 表膨胀与 XID 回卷 |
| 3 | "更新只改一行，很便宜" | 堆内 MVCC 会写新元组并更新所有索引（HOT 可缓解） |
| 4 | "shared_buffers 越大越好" | 与 OS page cache 双缓存；官方建议 25%，过大反而增加管理开销 |
| 5 | "连接数可以随便开" | 进程模型下每连接 ~MB 级；必须配 **pgbouncer** |
| 6 | 🔧 本书定位 | 本章案例可作为全书的「开源实验靶场」：第 11–16 章的每个算法都可在 PG 源码中找到对应实现 |
