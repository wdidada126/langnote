# CMU 15-445/645 论文清单（Papers）

> 配合 `notes/` 逐讲阅读。分三部分：经典论文（打地基）、近五年（2021–2026，看演进）、知识点↔开源映射表。
> 建议顺序：先读经典里与当讲对应的那篇，课后翻映射表动手验证。

## 一、经典论文（按主题，含对应讲次）

### 关系模型与理论
| 论文 | 作者/年份 | 要点 | 讲次 |
|---|---|---|---|
| A Relational Model of Data for Large Shared Data Banks | E. Codd, 1970 | 关系模型奠基：用关系(集合)+代数替代导航式记录链接 | L01 |
| The Modeling of Subsystems in a Relational Database / 规范化 | Codd, 1972 | 函数依赖、范式 | L01 |
| Relational Completeness of SQL | Date 等 | SQL 与关系代数的完备性/偏离 | L02 |

### 存储 / 缓冲池 / 索引
| 论文 | 作者/年份 | 要点 | 讲次 |
|---|---|---|---|
| Organization and Maintenance of Large Ordered Indexes (B-tree) | Bayer & McCreight, 1972 | B 树原始定义与动态维护 | L08 |
| The Ubiquitous B-Tree | Comer, 1979 | B 树家族综述，入门必读 | L08 |
| Efficient Locking for Concurrent Operations on B-Trees (B-link tree) | Lehman & Yao, 1981 | 兄弟右链 + 无死锁并发下降 | L09 |
| Extendible Hashing / Linear Hashing | Fagin 1981 / Litwin 1980 | 动态哈希目录/增量分裂 | L07 |
| The Log-Structured Merge-Tree (LSM-Tree) | O'Neil et al., 1996 | 写优化，顺序写替代随机写 | L03/L08 |
| The Bw-Tree: A Latch-free... | Levitin & Mohan (Leviton), VLDB 2014 | mapping table + delta + CAS 无闩索引 | L09 |
| Adaptive Replacement Cache (ARC) | Megiddo & Modha, 2003 | 自适配置换策略 | L06 |
| Access Methods for Relational DBMS (Bufferpool) | DeWitt/Gray 等综述 | 缓冲池与访问路径 | L06 |

### 存储模型 / 列存 / 压缩
| 论文 | 作者/年份 | 要点 | 讲次 |
|---|---|---|---|
| Column-Stores vs. Row-Stores: How Different Are They Really? | Abadi et al., VLDB 2008 | 行列对比实证 | L05 |
| C-Store: A Column-oriented DBMS | Stonebraker et al., VLDB 2005 | 列存 + 读优化 + WOS/ROS | L05 |
| MonetDB/X100: Hyper-Pipelining Query Execution | Idreos & Kersten, CIDR 2005 | 向量化/批量执行鼻祖 | L13 |
| Data Encoding in MonetDB / Vectorwise | Idreos 2012 | 列压缩编码与 compressed execution | L05/L13 |
| SpaceO/压缩决策 | Zukowski, 2009 (thesis) | 编码选择树 | L05 |

### 查询执行 / 优化器
| 论文 | 作者/年份 | 要点 | 讲次 |
|---|---|---|---|
| Volcano: An Extensible and Parallel Query Evaluation System | Graefe, 1990 | 迭代器/火山模型 + 可扩展 | L12 |
| Access Path Selection in a Relational DBMS (System-R) | Selinger et al., SIGMOD 1979 | 代价模型 + 自底向上 DP 优化器 | L14 |
| The Cascades Framework for Query Optimization | Graefe, 1995 | 自顶向下 + 规则枚举 + memo | L14 |
| Query Evaluation Techniques for Large Databases | Graefe, ACM CSUR 1993 | join/排序算法百科 | L10/L11 |
| Morsel-Driven Parallelism | Leis et al., SIGMOD 2014 | 原子认领 morsel 的并行执行 | L11/L13 |
| Efficiently Enlisting Ad-hoc ... Dash / Symmetric Hash Join | Leis/Freitag 等 2020 | 单遍/自适应 hash join | L11 |

### 并发控制
| 论文 | 作者/年份 | 要点 | 讲次 |
|---|---|---|---|
| A Consistency Model for DBs: The Notions of Consistency and Predicate Locks | Eswaran et al., 1976 | 2PL + 谓词锁 + 可串行化 | L16 |
| Concurrency Control in RDBMS (Survey) / 教科书 | Bernstein et al., 1987 | 并发控制总论 | L15-18 |
| Weak Consistency: A Generalized Theory... (Aghast 前身) | Adya, PhD 1999 | 用依赖图广义定义隔离级别 | L15 |
| A Critique of ANSI SQL Isolation Levels | Berenson et al., SIGMOD 1995 | 指出标准定义漏洞 + 定义 anomaly | L15 |
| Serializable Isolation for Snapshot Databases (SSI) | Cahill et al., SIGMOD 2008 | SI 之上补可串行化 | L18 |
| High-Available... Hekaton / MVCC | Diaconu 2013 | 内存主存 DB 多版本 | L18/L24 |

### 日志与恢复
| 论文 | 作者/年份 | 要点 | 讲次 |
|---|---|---|---|
| ARIES: A Transaction Recovery Method... | Mohan et al., ACM TODS 1992 | Redo/Undo + 分析三趟 + REPEAT HISTORY | L19/L20 |
| Arbitration: Recovery... / 恢复综述 | Mohan & Haderle 1992 (IBM System Journal) | ARIES 姊妹篇 | L20 |
| The Transaction Concept: Virtues and Limitations | Gray, 1981 | 事务/ACID 哲学 | L15/L19 |
| Generalized Isolation / Recovery | Gray & Reuter, 1993 (book) | 事务处理圣经 | L19 |

### 分布式 / NewSQL / 云
| 论文 | 作者/年份 | 要点 | 讲次 |
|---|---|---|---|
| Spanner: Google's Globally-Distributed Database | Corbett et al., OSDI 2012 | TrueTime + 外部一致性 + 2PL/2PC/Paxos | L22 |
| Percolator (Bigtable 上的分布式事务) | Rao, 2010 | 乐观事务 + TSO + 无协调者 2PC | L22 |
| In Search of an Understandable Consensus (Raft) | Ongaro & Ousterhout, 2014 | 共识算法，分布式 DB 基石 | L21 |
| Paxos Made Live / Cheap Paxos | Lamport/ 等 | 共识理论 | L21 |
| TiDB: A Raft-based HTAP Database | Huang et al., VLDB 2020 | 开源 NewSQL + HTAP | L22/L24 |
| Amazon Redshift Design | Barbette et al. (ParAccel) / Gupta 2015 | MPP 列存数仓 | L23 |
| The Snowflake Elastic Data Warehouse | Dageville et al., SIGMOD 2016 | 存算分离云数仓 | L23 |
| Aurora: On Avoiding Distributed Consensus for I/Os, Commits... | Verbitski et al., SIGMOD 2017 | "log is the database" 云 OLTP | L22/L23 |
| Socrates: The New SQL Server in the Cloud | Antonopoulos et al., SIGMOD 2019 | 存算分离 OLTP | L23 |
| Architecture of a Database System | Hellerstein/Stonebraker/Hamilton, 2007 | 全局图景综述，课后必读 | 全课 |

## 二、近五年（2021–2026）精选

| 论文 | 年份 | 主题 | 一句话 |
|---|---|---|---|
| DuckDB: an Embeddable OLAP Database System | CIDR 2021 | 嵌入式向量化 OLAP | 火山骨架+列式批执行，进程内分析 |
| Data-Juicer / Lakehouse 系列 (Databricks) | 2021–2022 | Lakehouse | 数据湖+仓库融合，开放表格式 |
| Apache Iceberg: A Open Table Format / 元数据演进 | 2022+ | 表格式 | schema 演进、隐藏分区、time travel |
| Delta Lake: ACID Table Storage over Object Stores | VLDB 2020/21 延续 | 数据湖事务 | Parquet 上的 MVCC + 事务日志 |
| Lakehouse 综述 / Databricks "What is a Lakehouse" | 2021 | 架构 | 对象存储上同时服务 BI + ML |
| Umbra: Disrupting Data System Construction... | CIDR 2020/持续至2022 | 编译式 DB 框架 | 可冻结的自适应 codegen DB 编译器 |
| ClickHouse - Lightning Fast Analytics for Everyone | 2023 | 向量化 OLAP | 工业级列存向量化引擎复盘 |
| An Empirical Evaluation of Vector Database Management Systems | 2023 | 向量 DB 评测 | Milvus/Qdrant/Weaviate/... ANN 对比 |
| DiskANN / FreshDiskANN (NeurIPS 2019→VLDB 2021) | 2021 | ANN 索引 | SSD 上十亿级近邻，图索引 |
| HNSW: Efficient and robust approximate nearest neighbor search | TPAMI 2021（2016 原版） | 图 ANN | 分层可导航小世界，向量索引主流 |
| pgvector 生态与半结构化 embedding 检索 | 2023 | 向量扩展 | 关系库里做相似检索 |
| BytePlus Vela / OceanBase 4.x HTAP | 2022–2023 | HTAP | 单机分布式一体化 + 行列混合 |
| CaaS / 云原生数据库弹性与 Serverless | 2022–2024 | 云 | 存算分离 + 冷启动 + 计费的工程化 |
| Learned Index / Rose / ALEX / PGM-index 演进 | 2021–2023 | 学习型索引 | 递归/分段模型逼近 B+ 树，更新改进 |
| Bao: Learned Query Optimization (Presto) | 2021 | 学习型优化 | 用强化学习选 hint，可移植优化 |
| LLM-based Text-to-SQL / Spider 2.0 / Spider 2 | 2023–2024 | NL→SQL | 大模型生成查询，DB 前端新范式 |
| Autonomous DB (Autonomous JSON / OtterTune 后继 / DBSherlock, Noelle) | 2021–2024 | 自驱动 | 自动调参、异常诊断、索引推荐 |
| Serverless / disaggregated 内存 (Disaggregation for DBs, PASE 2022 / Scylla 等) | 2022 | 近数据/内存池 | CXL/RDMA 下的 DB 架构再思考 |
| FoundationDB 事务/LogAnnotated 系列工程复现 | 持续 | 严格可串行 KV | 开源可串行化存储底座 |
| VLLM/向量-关系混合检索 for RAG | 2023–2025 | 检索增强 | 向量 ANN + 关键词 BM25 混合，DB 与 LLM 交汇 |

> 注：向量 DB / Lakehouse / Learned Index / HTAP 是本方向近五年最活跃的四大主题，与 L05/L08/L14/L23/L25 直接对应。

## 三、知识点 ↔ 开源项目映射表

| 知识点（讲次） | PostgreSQL | MySQL/InnoDB | RocksDB | DuckDB | TiDB | CockroachDB | SQLite |
|---|---|---|---|---|---|---|---|
| 关系模型/代数（L01） | 查询树 parse→plan | 同 | —(KV) | 表达式树 | 上层 TiDB SQL | SQL 层 | — |
| 高级 SQL/窗口/CTE（L02） | WindowAgg/CTE | 8.0 窗口函数 | — | QUALIFY/窗口 | 继承 PG 生态 | 支持 CTE | 3.25 窗口 |
| 块设备/SSD（L03） | 8K 块+O_DIRECT | 16K 页 | block+FTL | 4K/块 | LSM(Raft) | KV | 4K 页 |
| 页/slotted page（L04） | PageHeader+ItemId | compact 行格式 | block | row-group | 复用 RocksDB | KV 值 | b-tree cell |
| 行/列存与压缩（L05） | TOAST/BRIN | 行存 | Snappy/LZ4块 | 列存+FOR/RLE | TiFlash 列存 | 行存(列索引规划) | 行存 |
| 缓冲池/置换（L06） | clock sweep+bgwriter | young/old LRU | block cache(LRU/Clock) | 缓冲管理器 | (交给 TiKV) | 依赖 KV | page cache |
| 哈希索引（L07） | HASH 索引 | AHI 自适应哈希 | hash index in SST | 聚合 hash 表 | — | — | — |
| B+树（L08） | nbtree | 聚簇 B+树 | (LSM 非B+树) | ART/segment | RocksDB LSM | Pebble(LSM) | b-tree 页 |
| 索引并发（L09） | B-link/split 处理 | latch coupling+gap | 跳表 memtable | 并行构建 | Raft+MVCC | MVCC+Raft | 文件锁/WAL |
| 排序/聚合（L10） | Sort/HashAgg | filesort/临时表 | 外部(Iterator) | radix hash agg | 分布式聚合 | 分布式 | 临时 B 树 |
| Join 算法（L11） | NL/Merge/Hash | 8.0 hash join | — | partitioned+perfect | HashJoin/SMJ/IdxJoin | lookup join | NL+自动索引 |
| 火山执行（L12） | ExecProcNode 逐行 | iterator | —(存储层) | 算子接口 | 火山 | 火山 | VDBE 逐行 |
| 向量化（L13） | (有限/17聚合) | — | — | DataChunk+SIMD | TiFlash 向量化 | 向量化(部分) | — |
| 优化器（L14） | DP+GEQO+统计 | 贪心/8.0改进 | 无 | 自适应+统计 | CBO+统计 | Cascades-like | 代价+统计 |
| 事务/隔离（L15） | 4级+SSI | 4级(默认RR) | Snapshot | 单写事务 | SI+TSO | Serializable | WAL/rollback |
| 2PL（L16） | 行锁+超时检测 | RR 2PL+NextKey | (写串行) | 文件锁 | 悲观锁模式 | 悲观+SI | RESERVED |
| TO（L17） | —(MVTO 血统) | — | — | — | TSO=中心TO | HLC+push | — |
| MVCC（L18） | xmin/xmax+vacuum | undo log+ReadView | snapshot+seq | 单写 | Percolator式 | Pebble MVCC | WAL 快照 |
| 日志/WAL（L19） | WAL(xlog) | redo+undo+binlog | WAL+MANIFEST | 事务日志 | Raft log | Raft log | WAL/journal |
| 恢复/PITR（L20） | basebackup+PITR | xtrabackup+binlog | checkpoint+backup | attach/备份 | 快照+BR | 快照恢复 | 文件拷贝 |
| 分布式/共识（L21） | 流复制/Citus | group repl(Paxos) | —(单机) | — | Raft region | Raft range | — |
| 分布式事务（L22） | 2PC/FDW | XA | — | — | TSO+2PC-like | HLC+并行提交 | — |
| 云/存算分离（L23） | 云托管 | Aurora 风格 | S3 后端 | httpfs/parquet | S3 存算分离 | 对象存储备份 | 只读副本 |
| HTAP（L24） | +列存fdw | HeatWave | — | 内嵌OLAP | TiFlash | (OLTP 专注) | — |
| 图/向量/AI4DB（L25） | AGE/pgvector | vector 规划 | — | 向量扩展 | 生态 | — | sqlean 向量 |

> 使用建议：学到某个机制，直接在表中挑 1–2 个引擎去读其对应源码文件（如 Postgres `nbtinsert.c`、DuckDB `hash_join.cpp`、RocksDB `db/column_family.cc`），把抽象落成能调试的具体代码。
