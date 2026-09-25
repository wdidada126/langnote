# 04 新一代 DBMS 架构：列存、内存与 OLTP 的现实（书第 4 章 New DBMS Architectures）

> 对应书章：Chapter 4，评论作者 Michael Stonebraker——全书论点"one size fits all 之死"的正式出场地。
> 收录三篇：
> ① Stonebraker, Abadi, Batkin, Chen, Cherniack, Ferreira, Lau, Lin, Madden, O'Neil, O'Neil, Rasin, Tran & Zdonik,
> *C-Store: A Column-oriented DBMS*（SIGMOD 2005）；
> ② Harizopoulos, Abadi, Madden & Stonebraker, *OLTP Through the Looking Glass, and What We Found There*（SIGMOD 2008）；
> ③ Diaconu, Freedman, Ismert, Larson, Mittal, Stonecipher, Verma & Zwilling,
> *Hekaton: SQL Server's Memory-optimized OLTP Engine*（SIGMOD 2013）。
> 三篇构成一个完整论证：**仓库负载该用列存（①）；OLTP 在内存时代背着磁盘时代的包袱（②）；
> 把包袱卸掉的整机长什么样（③）。**

## 核心概念速览（中英对照）

- **一刀切之死** — Death of one size fits all：行存磁盘 DBMS 通吃一切负载的格局在 2000s 碎裂为按负载特化的多个架构
- **列式布局** — Column-store layout：同列连续存储；扫描只读所需列（100 列取 6 列 → IO 省一个数量级）、单列同型压缩率高、无记录头开销
- **向量化/列式执行** — Column-at-a-time execution：内循环按列批量过滤，CPU 检查开销从每行降到每列批，缓存与分支友好
- **写优化/读优化双存储** — WOS/ROS（Write/Read Optimized Store）：小事务先落行式 WOS，攒够"凸出"（outfit）批量转列式 ROS——写路径与读路径各得其所
- **投影** — Projection：为不同查询簇预建的列子集物化；列存的"索引"哲学（多投影重叠 + 稀疏索引，少 B 树）
- **只读优化者的困境** — Read-optimized trade-off：C-Store 明赌"数据不局部性 + 分析查询重复规律"两个仓库特征
- **OLTP 镜像反思** — OLTP through the looking glass：当数据全在内存，磁盘 DBMS 的缓冲池/行头/日志顺序写等"保险"全变成纯开销
- **指针追逐与索引开销** — Pointer chasing & index-only overhead：内存 OLTP 的两大时间贼：跳指针、锁/闩与缓冲池管理比读数据还贵
- **MVCC** — Multi-Version Concurrency Control：读旧版本不阻塞、写建新版本；内存 OLTP 的默认并发模型（评论预言"没人再用传统 2PL"）
- **原生编译** — Native compilation（Hekaton）：存储过程编译为机器码，取代解释执行火山模型——与 Neumann 同期同向的工业印证
- **无闩锁数据结构** — Latch-free hash/b-tree：原子 CAS + epoch 式内存回收，多核扩展的地基
- **检查点而非常驻日志流** — Memory checkpointing：内存引擎用周期快照+日志增量控制恢复成本
- **NoSQL 回摆** — NoSQL pressure on RDBMS：易用+半结构化两板斧逼得商业库加 JSON；评论预言 NoSQL 与 SQL 市场合流

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 4.1 C-Store | 列存从 1970s 的 idea 变成 2005 的整机 | 仓库场景 50–100 倍优势的四本账 |
| 4.2 Looking Glass | 用测量回答"OLTP 为什么慢" | 慢在磁盘时代的遗产，不在业务 |
| 4.3 Hekaton | 微软把"反思"变成产品 | 内存 OLTP 的工程模板：编译+MVCC+无闩锁 |
| 4.4 三篇合读与评论的预言清单 | 2013 年的三个判断哪些兑现了 | 逐条验收 |
| 4.5 工业落地与书外更新 | Vertica/SAP HANA/Postgres 路线/In-Memory 现状 | 分化后又在互相回抄 |

## 核心精讲

### 4.1 C-Store：把列存的三个"不公平优势"算成整机

**解决什么问题**：数据仓库负载（星型模型、宽表上百列、重复规律查询+临时查询混合、几乎无人 `SELECT *`）
与行存引擎的根本错位。Stonebraker 评论把列存优势拆成**四本可审计的账**：

| 账目 | 行存 | 列存 | 评论量级 |
| --- | --- | --- | --- |
| IO 账 | 取 6/100 列也要读全行 | 只读 6 列 | 少读 16 倍起步（例子账） |
| 压缩账 | 块内混 100 种字段 | 块内同字段同型 | 压缩率天壤之别 |
| CPU 账 | 内循环逐行检查有效性 | 逐列批量过滤 | 每列摊销而非每行付费 |
| 头开销 | SQL Server 每行 16B 记录头 | 无行头 | 长表白省两位数 |

**C-Store 的独特设计不是"列存"本身**（评论明说技术可追溯到 1970s，Sybase IQ 与 MonetDB 在前），
而是**WOS/ROS 双存储 + 投影 + 只读整机**的成套取舍：

- **写路径**：小事务进内存行式 WOS → 攒成"凸出"（outfit）→ 后台批量转列式 ROS。OLTP 般的提交语义
  与列存的读性能**用换出时间做隔离**；这也埋下"近实时分析"的延迟税。
- **投影（projections）**：物化的列子集 + 每列稀疏块索引，多个投影可重叠。查询规划=选投影，
  "索引即物化视图"的哲学在仓库语境压过 B 树。
- **赌注清单**：分析查询重复且规律、数据局部性弱、写少读多、廉价硬件上并行。赌赢=Vertica（2005 成立）；
  赌输的负载（高频小更新、点查）C-Store 自己声明不接——**专用架构的诚实就是写明不接什么单**。

**为什么被收录**：红书把它放在"新架构"第一篇，是因为它是**"one size fits all 之死"的第一例死亡现场**：
一个为特定负载特化到骨头里的 DBMS 反而在商业上碾压通才。评论冷账：若 Sybase 当年对 IQ 做对等多节点
投资，列存革命可提前十年——**技术领先不等于架构兑现**，这是 Stonebraker 自揭家史式的史观。

### 4.2 OLTP Through the Looking Glass：一场对自家房子的审计

**解决什么问题**：内存便宜到 OLTP 工作集全装得下（评论：1TB $25K 时代，"1MB 都算大的 OLTP 库"），
为什么磁盘行存引擎在内存机器上仍快不起来？论文用 TPC-C 式剖析回答——**三大税**（评论归纳）：

1. **索引/缓冲池税**：数据已在 RAM，还在走"页→缓冲池→查找"的路径；内存 OLTP 理想态是索引即数据、无页概念。
2. **日志/闩锁税**：每元组的锁管理器交互、闩锁、行头维护——管理开销大于业务计算本身。
3. **解释执行税**：查询解释执行的开销在内存时代占比放大（此点通向 Hekaton 与仓库 Neumann 精读）。

并给出"镜像世界"处方：索引重设计（跳过页的 hash/tree）、日志结构化与检查点折中、乐观并发
（读多写少竞争可容忍时 OCC 翻盘——呼应 3.3 的适用域地图）、编译执行。**论文的野心是测量，不是整机**；
整机在下一篇由微软交卷。

**为什么被收录**：它是 3.3（Agrawal 模拟研究）的精神续作：**用数字终结直觉争论**。
Bailis/Stonebraker 都爱这种"先量再吵"的文体。

### 4.3 Hekaton：卸掉所有包袱的工业答案

**解决什么问题**：SQL Server 需要一个"当数据全在内存"时的 OLTP 引擎（目标：10 倍性能 + 零停机内存扩容 +
与 In-Memory OLTP 的兼容性妥协）。设计清单：

| 决策 | Hekaton 的答案 | 对比 03 章经典 |
| --- | --- | --- |
| 缓冲池 | 删除。数据常驻内存，检查点文件承担持久化与恢复 | anatomy 的第一部件整个移除 |
| 并发控制 | 时间戳式 + 多版本，无锁表；读不阻塞写 | 评论："我猜没人再用传统 2PL"——在 Hekaton 兑现 |
| 索引 | 无闩锁 hash（桶数组+CAS）与无闩锁 B-tree（页级版本） | 锁管理税→原子指令税 |
| 执行 | 存储过程原生编译（LLVM）为本机码 | 解释执行税→零；与 Neumann 2011 互为工业/学术双证 |
| 恢复 | 周期内存检查点 + 增量日志 | ARIES 的血脉改造成"内存为主"的形态 |
| 热冷分层 | 内存表可异步归档到磁盘表 | 直面"内存太贵"的运维账 |

**为什么被收录**：三篇里唯一"上市公司财报级"的落地证据（2014 随 SQL Server 2014 GA）。
红书用它把第 2 章的"System R 时代架构"正式送进"退休软件之家"——Stonebraker 在第 1 章评论里
已经预告（SQL Server 14 = Hekaton + 传统引擎的双头怪物，旧解析器下挂新引擎的"创新者困境"解法）。

### 4.4 评论的三个预言，2026 年逐条验收

| 预言（2013 评论） | 兑现度 |
| --- | --- |
| 数据仓库世界整体转向列存 | ✅ 彻底兑现（Snowflake/BigQuery/Redshift/DuckDB 皆列存+向量化或 morsel） |
| OLTP 市场变内存市场；并发控制转向 MVCC/时间戳，2PL 退位 | ✅ 大方向兑现；⚠️ 2PL 并未死透（Postgres 的 Serializable 仍基于 SSI 图，InnoDB 默认行锁 RR 仍是锁协议） |
| NoSQL 与 SQL 市场合流（RDBMS 学会 JSON 与易用） | ✅ 部分兑现：文档/宽表模型大多并入 SQL 引擎（Postgres JSONB、Mongo 加 SQL 接口）；"专用引擎"则改头换面继续长（向量库） |

### 4.5 工业落地与书外更新

- **列存一支**：Vertica（C-Store 直系）、Sybase IQ 改旗、开源自 MonetDB/X100→Vectorize（MonetDB/X100
  一脉）到 DuckDB；湖仓表格式（Parquet + Iceberg）把列存从"引擎特权"变"文件格式日常"——机制见
  [../Engineering_Lakehouses_with_Open_Table_Formats/](../Engineering_Lakehouses_with_Open_Table_Formats/00-总览与阅读地图.md)。⚠️ 书外补充。
- **内存 OLTP 一支**：SAP HANA（同代竞对，评论未收）、SQL Server In-Memory、VoltDB/H-Store 的"单线程
  分区+存储过程"路线（与本节的"乐观+编译"是同一问题的不同解）；PostgreSQL 以 unlogged table/逻辑复制
  等温和方式吃内存红利。⚠️ 书外补充。
- **执行模型的下一拍**：Hekaton/Neumann 之后，"解释火山→编译/morsel 并行"完成范式转移——
  仓库精读：[../../paper/doi_10.14778_2002938.2002940/00-精读笔记.md](../../paper/doi_10.14778_2002938.2002940/00-精读笔记.md)。

## 常见误区

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "C-Store=列存发明者" | 评论明说技术源于 1970s、Sybase IQ/MonetDB 在前；C-Store 的贡献是**整机化与商业引爆** |
| 2 | "列存对一切负载都快" | 更新密集/点查宽行是列存弱区；WOS/ROS 换出延迟与写放大是列存的结构性税 |
| 3 | "Looking Glass 只是吐槽，没有建设性" | 它给出了"该重做什么"的清单，Hekaton 基本照单施工 |
| 4 | "内存 OLTP 不需要恢复算法" | 删的是缓冲池不是持久性；检查点+日志从 ARIES 血脉换了实现形态 |
| 5 | "Hekaton 的 MVCC 从此一统 OLTP" | 预言部分兑现；Postgres 式"无锁读+SSI"、VoltDB 式"单线程分区"同样活着——**专用化不止列一种轴** |

## 与仓库其他笔记的联系

- → Neumann 2011 精读（4.2"解释执行税"的另一半答案）：
  [../../paper/doi_10.14778_2002938.2002940/00-精读笔记.md](../../paper/doi_10.14778_2002938.2002940/00-精读笔记.md)
- → [03-人人都该掌握的核心技术.md](03-人人都该掌握的核心技术.md)：Hekaton 卸的正是第 3 章装的包（2PL、ARIES、页）。
- → [05-大规模数据流引擎.md](05-大规模数据流引擎.md)：列存+廉价硬件与"数据湖上的引擎"合流处。
- → ../MySQL技术内幕_InnoDB存储引擎2.md（2PL+MVCC 混合的现实工业形态，与 Hekaton 纯 MVCC 对照）。
- → ../湖仓架构大规模数据平台的设计和实现/03-存储湖仓架构的核心.md（列存文件格式在湖仓里的角色）。
