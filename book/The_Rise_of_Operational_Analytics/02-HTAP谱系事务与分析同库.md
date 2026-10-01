# 02 HTAP 谱系：事务与分析同库

> 主题重构笔记（非原书章对位，⚠️ 取证降级声明见 [00-总览与阅读地图.md](00-总览与阅读地图.md) §2）。
> 本篇是全目录的「HTAP 谱系硬义务」主章：先把「同库」这个词拆成可分辨的技术路线，
> 再给出盘上/云端的谱系坐标与 🔧 类比实验。

## 1. 「同库」至少有三种密度

把「事务与分析在同一套系统里」按**共享到什么层**拆开（⚠️ 本分类为通识重构，非原书图表）：

| 密度 | 形态 | 代表 | 共享物 | 典型风险 |
|---|---|---|---|---|
| D1 引擎内双表征 | 行存+列存同一引擎，内存态同步 | SAP HANA、SingleStore、TiDB(行+列存) | 同一进程/同一存储 | 聚合打爆前台延迟 |
| D2 引擎内旁路结构 | 行存为主，物化视图/列存索引/摘要表旁挂 | PostgreSQL 物化视图、SQL Server 列存索引、SQLite 生成列+影子表 | 同一事务域 | 视图维护滞后/膨胀 |
| D3 同集群分角色 | 主库事务+只读分析副本/外表 | PG 流复制+FDW、MySQL 复制+聚合从库、MongoDB 分片+聚合 | 同一日志流 | 副本延迟=新鲜度上限 |
| D4 同产品不同进程 | 交易引擎与分析引擎分离部署，共享存储/格式 | 湖仓+直连、存算分离云仓（⚠️ 云厂商平台行为，转述） | 同一数据格式 | 语义一致性靠约定 |

D1–D4 的判别价值在于：评审方案时先问密度，再谈指标——D2 的「新鲜度」取决于维护时机
（语句内/事务内/事后 REFRESH），D3 的取决于复制延迟，D1 的取决于隔离与限流策略。**同名不同密度，
风险画像完全不同。**

## 2. 谱系坐标：盘上笔记能接住哪几段

以下互链目标全部经 Glob/ls 验名（00 §谱系表含完整清单）：

- **PostgreSQL 系（D2/D3 教科书样本）**：物化视图与 REFRESH 策略、逻辑解码导出变更、FDW 回联远端——
  性能面看 [../PostgreSQL_10_High_Performance_3e/00-总览与阅读地图.md](../PostgreSQL_10_High_Performance_3e/00-总览与阅读地图.md)
  与 [../PostgreSQL_High_Performance_Cookbook/00-总览与阅读地图.md](../PostgreSQL_High_Performance_Cookbook/00-总览与阅读地图.md)；
  运维面看 [../PostgreSQL_16_Administration_Cookbook/00-总览与阅读地图.md](../PostgreSQL_16_Administration_Cookbook/00-总览与阅读地图.md)
  与 [../Mastering_PostgreSQL_Administration/00-总览与阅读地图.md](../Mastering_PostgreSQL_Administration/00-总览与阅读地图.md)；
  内核面（MVCC/缓冲池，解释 D2/D3 为什么这样表现）看盘上单文件
  [../PostgreSQL数据库内核分析.md](../PostgreSQL数据库内核分析.md) 与
  [../PostgreSQL查询引擎源码技术探析.md](../PostgreSQL查询引擎源码技术探析.md)；
  官方机制文档：预写式日志 https://www.postgresql.org/docs/current/wal-intro.html（✅ curl 200）、
  逻辑解码 https://www.postgresql.org/docs/current/logicaldecoding.html（✅ curl 200）。
- **MongoDB 系（D3/D4 文档库样本）**：Change Streams 把副本集 oplog 变成可订阅变更流
  https://www.mongodb.com/docs/manual/changestreams/（✅ curl 200，301 后落定）；
  聚合框架承担分析侧：[../MongoDB_The_Definitive_Guide_3e/00-总览与阅读地图.md](../MongoDB_The_Definitive_Guide_3e/00-总览与阅读地图.md)、
  [../Practical_MongoDB_Aggregations/00-总览与阅读地图.md](../Practical_MongoDB_Aggregations/00-总览与阅读地图.md)。
- **多模/新SQL 谱系入门**：跨范式对比的读法在 [../Seven_Databases_in_Seven_Weeks_2e/00-总览与阅读地图.md](../Seven_Databases_in_Seven_Weeks_2e/00-总览与阅读地图.md)；
  列存+分布式 OLTP/OLAP 混合的现役文档：TiDB overview https://docs.pingcap.com/tidb/stable/overview（✅ 200）、
  SingleStore 官网 https://www.singlestore.com/（✅ 200，产品口径 ⚠️ 转述）。
- **理论断层侧**：同库混合为何总与规范化/建模假设打架——[../What_Is_Database_Design_Anyway/00-总览与阅读地图.md](../What_Is_Database_Design_Anyway/00-总览与阅读地图.md)。

## 3. D1 的历史包袱：从「内存数据库顺带做分析」说起

2010 年代内存数据库兴起时的经典论证：既然全量在内存，行存点查与列式扫描的硬件差距缩小，
「一套引擎两种姿势」水到渠成；随后的研究线（HTAP 综述，SIGMOD Record 2020，⚠️ DOI 未校验通过）
把难点归为三类——**更新路径的双表征一致性**（改一行要不要同步改列存）、
**调度与资源隔离**（长查询别掐死短事务）、**优化器双目标**。这三条在 2024–2026 依然是
D1 产品差异化的主战场；本目录对任何具体厂商指标一律标 ⚠️ 转述（本机不可实测）。

## 4. D2 的工程学：旁路结构的「维护时机」矩阵

以 PostgreSQL 物化视图为样本（其他引擎同构可移）：

| 维护时机 | 语义 | 代价 |
|---|---|---|
| 语句触发（REFRESH 全量） | 显式批更，视图=上次刷新快照 | 刷新窗口双份开销 |
| CONCURRENTLY 增量 | 依赖唯一索引+diff 算法，不锁读 | 刷新期间写入放大 |
| 触发器同步维护 | 事务内即更，新鲜度最高 | 每笔写付一份维护税（🔧 E5 实测见 04） |
| 物化视图+定时任务 | 新鲜度=调度周期，最省 | 口径易漂移 |

D2 的真相：**没有免费的「同库」**，分析侧的新鲜度全部由「谁在写路径上付税」买断。
SQLite 侧可复刻的最小结构（影子表+触发器）在 🔧 实验 E5 里量过这份税。

## 5. D3 的真相：新鲜度=日志延迟，能力=日志表达力

流复制/FDW/Change Streams 共同点：分析侧看到的是**日志的尾巴**，不是数据库。于是两个变量决定体验：

1. **日志延迟**：网络+回放速度决定最小新鲜度；
2. **日志表达力**：逻辑解码（解码行级变更、可过滤可路由）> 物理复制（只能整库回放）>
   轮询查询（无日志，靠时间戳列猜）。

盘上对位：MySQL 行复制的运维细节见 [../Understanding_MySQL_Internals/00-总览与阅读地图.md](../Understanding_MySQL_Internals/00-总览与阅读地图.md)；
流式回放侧的引擎视角见 [../Streaming_Databases/00-总览与阅读地图.md](../Streaming_Databases/00-总览与阅读地图.md)；
CDC 工具链（Debezium/Flink CDC）在 [03-写前日志与变更数据捕获.md](03-写前日志与变更数据捕获.md) 展开。

## 6. D4 与湖仓的边界收缩

存算分离让「同库」的定义进一步稀释：事务引擎与分析引擎进程不同、**但读同一份表格式**
（Iceberg/Delta/Paimon，湖仓对位见 [07-湖仓对位与运营数据层.md](07-湖仓对位与运营数据层.md)）。
判别口诀：**共享日志=D3；共享格式=D4；共享内存结构=D1/D2**。
2020 年的书把 D1/D2 当未来主流；2024–2026 的现实是 D4 凭成本与隔离性吃掉了大半新增场景 ⚠️（趋势判断，转述）。

## 7. 🔧 类比实验登记（非本书引擎行为）

- **E4·嵌入式分析引擎的并发性格**：本机 DuckDB 1.5.5（Python 包），同一库文件上
  父进程事务持有期间子进程尝试打开并写入：报
  `IO Error: Cannot open file ... 另一个程序正在使用此文件`（实测 0.34s 内返回失败，
  临时件 `D:/develops/tmp/dbwave_w8_rosa/parent_g4.py`）。结论：**DuckDB 是单进程独占的
  分析表征**，天然站在这条谱系的「离线端」；它演示了为什么嵌入式列存不会「成为」HTAP 引擎——
  不是聚合不够快，而是**并发写模型不兼容**（对照 05 的聚合速度数据）。

## 核心概念速览（中英对照）

- **HTAP** — Hybrid Transactional/Analytical Processing：单系统同时承载事务与分析负载的架构族。
- **双表征** — Dual Representation：同一数据同时以行存与列存（或摘要结构）存在，需一致性协议。
- **旁路结构** — Side Structure：物化视图/列存索引/影子表等不进主表征的分析加速件。
- **维护税** — Maintenance Cost on Write Path：为保持旁路结构新鲜而在事务路径上付出的额外开销。
- **日志尾巴** — Log Tail：D3 中分析侧数据边界的本质——受日志延迟而非存储状态支配。
- **逻辑解码** — Logical Decoding：把 WAL 行级变更解码成可订阅事件的机制（PG 术语，见 03）。
- **资源隔离** — Resource Isolation：防止长聚合饿死短事务的限流/优先级/副本手段。
- **共享格式** — Shared Table Format：D4 的「同库」新定义——进程不同但读同一表格式。
- **新鲜度上限** — Freshness Ceiling：每条密度路线由机制决定的最小可达延迟。
- **口径漂移** — Metric Drift：定时刷新/手工维护导致同一指标多版本并存的组织病。

## 最新演进与工业实践

- **D1 现役格局**（⚠️ 厂商口径转述，不作本机实测）：TiDB 官方「行列混存+HTAP」文档线
  https://docs.pingcap.com/tidb/stable/overview（✅ curl 200）；SingleStore 以「代码引擎+列存引擎
  双模」为卖点的官网口径 https://www.singlestore.com/（✅ curl 200）。SAP HANA 仍是 D1 概念的
  历史锚点，2024–2026 公开叙事已转向「BTP 上的分层混合」⚠️。
- **D2 的 PG 主流化**：物化视图/并行查询/逻辑解码长期稳态；版本节奏见官方支持周期页
  https://www.postgresql.org/support/versioning/（✅ curl 200）——2024 年 PG17 发布、
  后续版本延续「旁路结构增强」而非「引擎内列存」（社区路线选择的公开事实）。
- **D3 的服务化**：MongoDB Atlas 把 Change Streams 接进触发器/检索管道，文档入口
  https://www.mongodb.com/docs/manual/changestreams/（✅ curl 200）。
- **D4 的格式战争收尾**：Iceberg 规范成为开放表格式事实标准之一 https://iceberg.apache.org/spec/（✅ curl 200），
  「事务引擎直写湖格式」类需求 2024–2026 多由流式表提交协议（metadata 原子替换）承接，湖仓侧论述见 07。
- **论文线**：HTAP 分类综述（SIGMOD Record 2020）⚠️ DOI 未过 api.crossref.org 校验；
  「同库双表征一致性」在 2018–2021 年间集中于 VLDB/ICDE 的 delta-synchronization 主题 ⚠️（未逐篇核 DOI，不列引用串）。
