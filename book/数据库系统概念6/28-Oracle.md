# 第 28 章 Oracle

> **本章地图**：历史（1977 SDL → Oracle V2 → 商业关系数据库的先驱）→ **实例架构**（**SGA** + 后台进程 + PGA）→ **存储结构**（表空间 / 段 / 区 / 块）→ **一致性读与 SCN**（undo 表空间、**ORA-01555 snapshot too old**）→ **RAC**（共享磁盘 + **Cache Fusion**）与 **Data Guard** → 高级特性（分区、物化视图与**查询重写**、Result Cache、**In-Memory Column Store**、Flashback、PL/SQL）→ 隔离级别与锁（Oracle 无读锁、**ITL 等待与 enqueue**）→ 与其他系统的对比。

## 二、核心精讲

### 28.1 架构：实例 = 内存 + 进程
- **SGA（System Global Area）**：`Buffer Cache`（数据块缓存）、`Shared Pool`（解析后的 SQL、数据字典缓存、`library cache`）、`Redo Log Buffer`、`Large Pool`、`Java Pool`、`Streams Pool`。
- **后台进程**：`DBWn`（数据库写进程，把脏块写入数据文件）、`LGWR`（日志写，触发条件：commit / 每 3 秒 / buffer 1/3 满 / DBWn 写前）、`CKPT`（检查点，更新控制文件与数据文件头）、`SMON`（实例恢复、空间合并）、`PMON`（进程清理与回滚）、`ARCn`（归档）、`RECO`（分布式事务恢复）。
- **PGA**：每个会话的私有内存（排序区、hash 区、游标状态）→ **PGA 聚合**与 `workarea_size_policy=AUTO` 是现代调优重点。
- 🔧 与 PostgreSQL 对比：Oracle 是**多线程/多进程混合 + 共享缓存**的经典架构；PG 是"每连接一进程 + shared_buffers + OS cache"。Oracle 的 `Buffer Cache + Log Buffer` 设计是理解**共享磁盘集群（RAC）**的前提。

### 28.2 存储结构
- 层次：**数据库 → 表空间（tablespace）→ 段（segment）→ 区（extent）→ 块（block）**；逻辑结构与数据文件（datafile）解耦 → 支持在线迁移与 OMF（Oracle Managed Files）。
- 块内结构：块头 + 行目录 + 空闲空间（`PCTFREE` 保留给后续更新，`PCTUSED` 控制重新入队）→ **行迁移（row migration）** 与 **行链接（row chaining）** 是 Oracle 特有的性能问题（更新导致行跨块）。
- `ASSM`（自动段空间管理）用位图块替代 freelist，减少争用。

### 28.3 一致性读、SCN 与 undo
- **SCN（System Change Number）**：全局单调递增的逻辑时钟，是 Oracle 一致性（以及 Data Guard、Flashback）的基石。
- **一致性读（consistent read, CR）**：查询以启动时刻的 SCN 为快照；读到被修改过的块时，**从 undo 表空间取旧版本在内存中构造 CR 块**（Oracle 是"undo 段式 MVCC"，与 PG 的堆内多版本相对）。
- **ORA-01555: snapshot too old**：查询运行时间过长，所需的前镜像已 **被其他事务的 undo 覆盖** → 查询失败。🔧 这是 Oracle 独有的经典故障，根因是 **undo_retention 不足 / undo 表空间太小 / 长查询**；与 PostgreSQL 的"长事务阻止 vacuum"是**同一类问题的两种表现**（版本回收 vs 版本保留）。
- 隔离级别：**Read Committed（默认）**、**Serializable**（Oracle 的实现是**快照隔离**语义，非 SSI）、**Read Only**。🔧 Oracle **没有 Read Uncommitted**，也没有"脏读"选项（DB2 才有 UR）；Oracle 的 Serializable 实际允许写偏斜。

### 28.4 锁与并发
- **Oracle 的核心特性：读不加锁**（MVCC），写加**行级锁**（事务槽 ITL + 锁字节），不升级为表锁（这点与 SQL Server/DB2 不同）。
- 争用表现：`enq: TX - row lock contention`（行锁等待）、`enq: TX - allocate ITL entry`（块内事务槽不足，`initrans` 太小）、`latch: cache buffers chains`（热点块闩争用）、`buffer busy waits`（写写冲突）。
- 🔧 死锁：Oracle 自动检测并回滚语句（`ORA-00060`），诊断靠 trace 文件中的等待图。

### 28.5 RAC：共享磁盘集群
- **RAC（Real Application Clusters）**：多实例共享同一存储（shared-disk），通过 **Cache Fusion** 经互联网络在实例间传输脏块，由 **GCS/GES**（全局缓存/队列服务）维护一致性。
- 关键组件：**GRD（全局资源目录）**、**LMS/LMD**（缓存融合与锁管理进程）、**OCR/Voting Disk**（集群配置与脑裂投票）、**ASM**（自动存储管理）。
- 评价：扩展性好、高可用（实例级故障自动接管）；但**应用需"RAC 感知"**（热点块跨实例 ping、序列缓存、分区对齐），且共享存储是故障单点。🔧 云时代对比：**Aurora/PolarDB 用存算分离 + 共享存储池**实现类似效果，而无需 RAC 的复杂锁协议。

### 28.6 高级特性
- **分区**（range/list/hash/interval/reference/composite + 分区裁剪 + 分区级维护）。
- **物化视图与查询重写**（第 20/13 章的工业实现：自动把查询重定向到 MV，需 `query_rewrite_enabled`）。
- **Result Cache / In-Memory Column Store**（12c：内存列存双格式，一个表同时服务 OLTP 与 OLAP → 对应 HTAP）。
- **Flashback**（基于 undo 与 Flashback Logs 的查询回退/表回退/数据库回退）、**LogMiner**（日志挖掘 → CDC）。
- **PL/SQL**：过程化语言（`%ROWTYPE`、`bulk collect` 减少上下文切换、`FORALL` 批量绑定）；🔧 现代反思：PL/SQL 极大提高单库能力，但也造成**业务逻辑锁定在数据库**，与微服务/可测试性诉求冲突。
- **AQ / Advanced Queuing**：数据库内消息队列（对应第 26 章 TP monitor 的持久队列）。

## 三、经典论文与原始文献

| 论文/资料 | 出处 | 贡献 |
| --- | --- | --- |
| Oracle《Oracle Database Concepts》《Oracle Database Administrator's Guide》 | 官方文档 | 一手权威（本章最佳实践参考） |
| Lahdenmäki & Leach《Oracle Physical Database Design》 | 2004（书） | 存储与索引设计 |
| Kyte《Expert Oracle Database Architecture》 | 2014（书） | 架构深度解析 |
| Bridge, Joshi, Keihl et al.《The Oracle Universal Server Buffer Manager》 | VLDB 1997 | 缓冲区管理 |
| Oracle RAC / Cache Fusion 相关技术白皮书 | Oracle | 共享磁盘集群 |
| 《Oracle In-Memory: A Dual Format In-Memory Database》 | IEEE ICDE 2015 | 双格式内存列存 |

## 四、近年研究与工业界开源实践

- **近年研究**：**HTAP 双格式存储**（Oracle Dual Format 是 HTAP 的先行者，对照 TiDB TiFlash、SQL Server 的 operational analytics）；**自治数据库（Autonomous Database，AI4DB 旋钮调优的商用形态）**；**持久化内存上的 redo 优化**。
- **对读本章有用的开源对照**（star 数 2026-09 实测）：
  - `postgresql/postgres`（≈17k★）：用开源实现对照理解 SCN（PG 用 XID + 快照）、undo（PG 堆内版本 vs Oracle undo 段）、进程模型差异。
  - `mysql/mysql-server`：`innodb` 的 redo/undo 与 Oracle 概念最接近（undo 段、回滚段、purge）。
  - `pingcap/tidb`（≈40.6k★）/`cockroachdb/cockroach`（≈32.5k★）：**RAC 的现代对照物**——用 Raft + shared-nothing 达到（甚至超过）RAC 的高可用，代价是需要分片键设计。
  - `orafce/orafce`：`PostgreSQL 的 Oracle 兼容层`，迁移 Oracle 应用时的实用工具。
  - `debezium/debezium`（≈13.1k★）：Oracle LogMiner/XStream 的 CDC 连接器，是把 Oracle 数据接进现代数据栈的标准方案。

## 五、常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "Oracle 有脏读（Read Uncommitted）" | 无；Oracle 最低就是 **Read Committed** |
| 2 | "Oracle Serializable 是真正的可串行化" | 其实现是**快照隔离**语义，仍可能写偏斜 |
| 3 | "行锁会自动升级为表锁" | Oracle **不做锁升级**（与 SQL Server/DB2 不同），代价是每行的锁开销 |
| 4 | "RAC 就是性能线性扩展" | 跨实例缓存融合开销大；需热点分区与"应用亲和" |
| 5 | "ORA-01555 是 bug" | 是 undo 保留期不足的设计后果，需调 undo_retention / 缩短长查询 |
| 6 | 🔧 本书定位 | 本章偏"商业数据库介绍"，学习价值在于**用 Oracle 对照理解通用机制**（UNDO vs 堆内 MVCC、共享磁盘 vs shared-nothing）；具体产品特性应以官方文档为准 |
