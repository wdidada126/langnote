# 09 收尾、选型与 CAP（Wrapping Up + Database Overview Tables / CAP）

> 对应官方页实抓目录（✅）：Wrapping Up（Genres Redux / Making a Choice / Where Do We Go from Here?）+ 附录（Database Overview Tables / The CAP Theorem / Eventual Consistency / CAP in the Wild / The Latency Trade-Off）。
> 本章为**方法论收束**，不含引擎运行行为；🔧 类比只做「一致性/延迟」的概念演示，**非任何本书引擎行为**。
> 理论纵深：CAP/复制/一致性正规论述见 [../设计数据密集型应用/00-总览与阅读地图.md](../设计数据密集型应用/00-总览与阅读地图.md)；NoSQL 家族定位见 [../nosql精粹.md](../nosql精粹.md)。

## 9.1 Genres Redux：把七库重新按模型归位

读完全书，作者要求「忘掉库名、只记模型」，把七库压回流派表（✅ 本册 01 章的表在此回收）：

| genre | 本册代表 | 一句话记忆钩子 |
| --- | --- | --- |
| 关系 | PostgreSQL（[02](02-PostgreSQL关系锚点.md)） | 默认答案；join + 事务 |
| 键值/结构 | Redis（[08](08-Redis数据结构服务器.md)） | 结构即语义，做缓存/加速 |
| 文档 | MongoDB、CouchDB（[04](04-MongoDB文档模型.md)、[05](05-CouchDB文档与复制.md)） | 嵌套对象；两者差在一致性/复制哲学 |
| 宽列 | HBase、DynamoDB（[03](03-HBase列簇与大数据.md)、[07](07-DynamoDB托管NoSQL.md)） | 海量写按行键；差在自建 vs 托管 |
| 图 | Neo4j（[06](06-Neo4j图数据库.md)） | 关系一等公民，多跳快 |

> 关键洞见：Mongo↔Couch 同模型不同哲学、HBase↔Dynamo 同模型不同运维——说明**「选 genre 只是第一步，同 genre 内还有一致性/运维的二次选择」**。

## 9.2 Making a Choice：选型三问 + 一次权衡

作者的选型框架（⚠️ 转述自 Wrap-Up 口径）：
1. **数据形状**：规范化？嵌套？网络？稀疏行？→ 定 genre。
2. **访问模式**：点查 / 范围扫 / 多跳 / 聚合 / 全文？→ 定该 genre 内的库（如文档里 Mongo 更擅聚合、Couch 更擅复制）。
3. **一致性预算**：能接受最终一致吗？谁容忍冲突？→ 定 CAP 站位。
- 第四现实约束：**运维与团队**（HBase 的 HDFS+ZK、Dynamo 的锁云、Redis 的内存成本）——很多决定其实是「能不能养得起」。

## 9.3 The CAP Theorem（附录核心）

- **三选二（在分区时）**：Consistency（线性一致）/ Availability（每请求有响应）/ Partition tolerance（网络丢包仍工作）。P 在分布式里不可放弃，于是本质是 **CP vs AP 的取舍**。
- 各库站位（⚠️ 转述，附录口径 + 社区共识）：
  - **CP 倾向**：HBase、MongoDB（默认多数派）、PostgreSQL（单机强一致）、Neo4j 因果集群。
  - **AP 倾向**：Cassandra、CouchDB 复制、DynamoDB（最终一致读可选）。
  - Redis 单机强、复制异步偏 AP。
- 概念复现：本册各章 🔧 都是「单机视角」，天然演示不到分区；分区一致性属 ⚠️ 转述域，纵深见 [../设计数据密集型应用/00-总览与阅读地图.md](../设计数据密集型应用/00-总览与阅读地图.md)。
- 文献登记：CAP 原始为 Gilbert & Lynch（2002），附录另引其复盘 *CAP Twelve Years Later*（IEEE Computer, 2012）——⚠️ 按本工程规范，未过 Crossref DOI 校验，故只给作者+出处+年份、**不冒 DOI**。

## 9.4 Eventual Consistency & CAP in the Wild

- **最终一致**：无冲突写入迟早收敛到相同值；带来「读旧值/多版本并存」的应用可见行为（CouchDB `_conflicts` 是其显式化身，见 [05-CouchDB文档与复制.md](05-CouchDB文档与复制.md)）。
- **一致性光谱**（⚠️ 转述）：强一致 → 会话/单调读 → 读己之写 → 最终一致，不是一刀切两档。
- **CAP in the Wild**：现实系统可做「部分操作强一致、部分最终一致」的混合（如 Dynamo 的强一致读选项、Mongo 的 write concern 旋钮）——CAP 是每操作可切换，不是全局站队。

## 9.5 The Latency Trade-Off（延迟权衡）

> 🔧 **类比组（非本书引擎行为，SQLite 3.45.3）**：用一次「索引加速」演示「用空间/写代价换读延迟」——这是贯穿全书的隐藏主题。
> 本机 `kv(k,f,v)` 1 万行按 `f` 过滤：无索引全表 **0.00054s** → `CREATE INDEX` 后 **0.00006s**（≈9×，见 [01-引言与数据模型.md](01-引言与数据模型.md) 🔧）。
> 引申：Postgres B 树、Mongo 多键索引、Neo4j 邻接指针、Redis 内存结构——**都是「读快」的不同投资方式**，代价分别落在写放大、内存占用、运维复杂度。选型即选「把延迟税交给谁交」。声明：数字是 SQLite，非任一本书引擎的真实延迟。

- 附录的「延迟权衡」正题（⚠️ 转述）：跨数据中心一致性往返、缓存命中、批量 vs 单条、本地 vs 托管——每条都在「一致 / 可用 / 延迟」三角里挪点。

## 9.6 Where Do We Go from Here?：多模型与混合持久化

作者收尾指向 **polyglot persistence**（一个系统按子系统混用多库）与「多模型数据库」趋势。本册 2018 的七个独立库，到 2026 已在两端融合：
- **单引擎多模**：PG（+JSONB+pgvector+全文）、Azure Cosmos DB（多 API）。
- **专职极致化**：向量/时序/湖仓各自成峰（见 9.7 对位）。

## 9.7 Database Overview Tables → 盘上纵深导航（实链，写前已验）

| 想要… | 去 |
| --- | --- |
| 关系运维/性能 | [../PostgreSQL_16_Administration_Cookbook/00-总览与阅读地图.md](../PostgreSQL_16_Administration_Cookbook/00-总览与阅读地图.md) |
| Redis 全景/源码 | [../Learning_Redis/00-总览与阅读地图.md](../Learning_Redis/00-总览与阅读地图.md)、[../Redis设计与实现.md](../Redis设计与实现.md) |
| 文档模型纵深 | [../MongoDB_The_Definitive_Guide_3e/00-总览与阅读地图.md](../MongoDB_The_Definitive_Guide_3e/00-总览与阅读地图.md) |
| 图模型/Cypher | [../Neo4j_The_Definitive_Guide/00-总览与阅读地图.md](../Neo4j_The_Definitive_Guide/00-总览与阅读地图.md) |
| 宽列/列簇 | [../Cassandra_The_Definitive_Guide/00-总览与阅读地图.md](../Cassandra_The_Definitive_Guide/00-总览与阅读地图.md) |
| 全文/向量/时序特化 | [../Elasticsearch_The_Definitive_Guide/00-总览与阅读地图.md](../Elasticsearch_The_Definitive_Guide/00-总览与阅读地图.md)、[../Vector_Databases/00-总览与阅读地图.md](../Vector_Databases/00-总览与阅读地图.md)、[../Time_Series_Databases/00-总览与阅读地图.md](../Time_Series_Databases/00-总览与阅读地图.md) |
| 一致性/复制理论 | [../设计数据密集型应用/00-总览与阅读地图.md](../设计数据密集型应用/00-总览与阅读地图.md) |

## 9.8 七库一句话对照（本册最终回收表）

| 库 | genre | 一句话立身 | 一句话短板 | 本册章 |
| --- | --- | --- | --- | --- |
| PostgreSQL | 关系 | 默认答案、join+事务+可编程 | 水平扩展成本高 | [02](02-PostgreSQL关系锚点.md) |
| HBase | 宽列 | 海量写、rowkey 范围扫 | 无 join/二级索引、运维重 | [03](03-HBase列簇与大数据.md) |
| MongoDB | 文档 | 嵌套对象 + 强聚合/索引 | 跨实体事务弱（旧基线） | [04](04-MongoDB文档模型.md) |
| CouchDB | 文档 | HTTP 原生 + 双向复制 | 视图陈旧、无 ad-hoc | [05](05-CouchDB文档与复制.md) |
| Neo4j | 图 | 关系一等、多跳快 | 全量聚合弱 | [06](06-Neo4j图数据库.md) |
| DynamoDB | 宽列/托管 | 托管、低延迟按键读写 | 只能按 key、锁云 | [07](07-DynamoDB托管NoSQL.md) |
| Redis | 键值/结构 | 内存、结构即语义、做加速 | 内存上限、非检索库 | [08](08-Redis数据结构服务器.md) |

## 9.9 落地清单（读完本册能直接用的）

1. **先填三问再选库**：形状/访问/一致性（9.2），拿不准就先 PostgreSQL（9.1 锚点）。
2. **同 genre 再分哲学**：文档里要复制→Couch、要查询→Mongo；宽列里能自建→HBase、要托管→Dynamo。
3. **凡高并发读，先想加 Redis**（[08](08-Redis数据结构服务器.md)）：9.5 延迟权衡的落点。
4. **凡多跳关系，先想 Neo4j**（[06](06-Neo4j图数据库.md)）：别用五表 join 硬撑。
5. **许可与运维入决策**：Redis→Valkey（2024）说明 license 是 CAP 之外的第四约束（9.4）。
6. **纵深转专册**：任一库要上生产，去 9.7 对位表指定的盘上专册，本册只负责「选型直觉 + 手感」。

## 9.10 本册与前七章的收束关系

01 给出坐标系（genre + 四问），02–08 各打一遍七库，09 把七库沿「模型 / 一致性 / 延迟」三轴重新折叠。读完的顺序建议与认知负荷顺序见 [00-总览与阅读地图.md](00-总览与阅读地图.md) 的「阅读地图」。本书的终点不是「记住七库」，而是「拿到新问题能立刻定位 genre、预判坑、选对纵深书继续钻」。

## 核心概念速览（中英对照）

- **genres redux** — 按模型而非库名重排七库。
- **选型三问** — 数据形状 / 访问模式 / 一致性预算。
- **CAP 定理** — 分区时一致性与可用性不可兼得。
- **CP / AP** — 分区下取舍的两极站位。
- **最终一致** — eventual consistency：无冲突写迟早收敛。
- **一致性光谱** — 强一致到最终一致间的多档（单调读/读己之写）。
- **BASE** — Basically Available / Soft state / Eventual consistency：AP 阵营的口头纲领。
- **混合持久化** — polyglot persistence：子系统各选其库，而非一库通吃。
- **读写模型分离** — 写模型贴合实体、读模型贴合查询（物化/CQRS 前奏）。
- **混合一致性** — per-operation：同一库不同操作可不同站位。
- **延迟权衡** — latency trade-off：一致/可用/延迟三角的点挪。
- **多模型 / polyglot** — 单引擎多模 or 系统混用多库。
- **运维约束** — 养得起与否（HDFS/内存/锁云）。

## 最新演进与工业实践

- **CAP 叙事的今天（⚠️ 转述）**：工程界把 CAP 视为「分区下的极端二选一」教学模型，现实更常用**一致性级别菜单**（AWS「最终一致 vs 强一致读」、Mongo `readConcern`、PG 逻辑复制延迟）逐操作调档——与本册「CAP in the Wild」一脉相承且更细。
- **事务回归 NoSQL**：Mongo 多文档事务（4.0+）、Dynamo `TransactWrite`、CockroachDB/Yugabyte 的分布式 SQL——2e「用一致性换扩展」的对立已被「可配置的分布式 ACID」部分调和；见 [../设计数据密集型应用/00-总览与阅读地图.md](../设计数据密集型应用/00-总览与阅读地图.md)。
- **多模 + 向量成默认**：2026 每个主流库都在自家加向量索引/全文；「genre 边界」比 2018 更糊，选型回到「访问模式 + 运维 + 许可」而非「哪个是 NoSQL」。
- **许可进选型**：Redis→Valkey 分叉（2024）、Elastic 许可变更等提醒：**license 也是 CAP 之外的第四约束**——2018 书未及。
- **取证口径**：本章为 ✅ 官方页附录结构实抓 + ⚠️ 转述方法论；🔧 延迟类比 = SQLite 3.45.3 一手数字且非本书引擎行为；CAP 文献只给标题+出处不冒 DOI。
- **本册一句话定位**：它是「七库横向体验 + 选型直觉」的地图册，不是任何一库的说明书；把「模型/一致性/延迟/运维/许可」五轴记住，就拿到了进入盘上任一纵深专册的门票（见 9.7 表）。
- **与兄弟册的关系**：本波 #13/#14 讲「如何设计关系 schema」，本册讲「何时根本不该只用关系」——两者互补构成「关系为默认、NoSQL 为定向逃逸」的完整世界观（波尾主代理统一闭环互链）。
