# 01 Apache Cassandra: An Introduction（Apache Cassandra 简介）

> 原书第 1 章章名 ✅ Crossref 实抓；小节结构为推定重构 ⚠️（精读重构，非原书文本）。
> 集群相关内容一律 ⚠️ 文档转述。

## 题纲

本章是全书"为什么要这样运维"的定调章：Cassandra 是什么、从哪来（Dynamo 谱系）、
为谁而设计（写密集/多数据中心/永远在线）、它的取舍（去中心化最终一致 + CQL 的
"看起来像 SQL 但不是 SQL"），以及 Cassandra DBA 与关系库 DBA 工作重心的差异。

## 1. 谱系：从 Dynamo 论文到 Apache 顶石项目

- Cassandra 的公开血统是 Amazon **Dynamo** 论文（VLDB/ACM SOSP'07，DOI
  `10.1145/1294261.1294281`，已过 Crossref 200 校验 ✅）：masterless ring、一致性哈希、
  vector clock、sloppy quorum、hinted handoff、Merkle 反熵，六大件全部被继承。
  论文精读见 [../../paper/SOSP/doi_10.1145_1294261.1294281/00-精读笔记.md](../../paper/SOSP/doi_10.1145_1294261.1294281/00-精读笔记.md)，
  论文线枢纽在 [../../db/db.md](../../db/db.md)。
- 社区通述：源自 Facebook 2007-2008 年为收件箱搜索所做，2010 年成为 Apache 顶石项目 ⚠️
  （成书语境转述，未逐条实证）。
- 与 [../设计数据密集型应用/09-一致性与共识.md](../设计数据密集型应用/09-一致性与共识.md) 的
  分工：DDCA 讲"为什么 Dynamo 要放弃线性一致"，本章之后各章讲"运维这套放弃之后
  的系统要付哪些账"。

## 2. 数据模型：宽列（column-family / wide store）

- 存储单元是**表 = 分区键 →（聚簇列 → 列）**的嵌套有序 map；列可为稀疏、可带 TTL。
- 对比 [../分布式数据库入门进阶与实战/01-什么是分布式数据库与SQL-NoSQL-NewSQL.md](../分布式数据库入门进阶与实战/01-什么是分布式数据库与SQL-NoSQL-NewSQL.md)
  的 NoSQL 四分法：Cassandra 属列族存储，但**不是** HBase 式"列簇物理编码"，也**不是**
  Bigtable 式严格三层 ⚠️（通述）。
- CQL 给了它 SQL 外观，但无 join、无跨分区约束、按查询建模——这是第 4 章全部苦口的来源。
- 中文世界早年语境（郭鹏《Cassandra实战》0.7 时代，thrift 接口为主，见
  [../cassandra实战.md](../cassandra实战.md)）与本册（3.x、CQL-only）几乎是两个物种——
  **辨析登记**：该书与本册非同一书，谱系上是"史前史 vs 运维手册"。

## 3. 架构立场（本章点到，05 章展开）

- **masterless**：所有节点同权，协调者（coordinator）由客户端任选；没有需要运维的"主节点"，
  但有需要运维的 **gossip 健康度、提示堆积、修复欠账**——这三样在 09/10 章接管。
- **可写性优先**：写入先落 commitlog + memtable（本地提交语义），复制/提示在后台完成；
  代价由读路径与修复偿还。写多读少、可用性压倒一切的画像与
  [../设计数据密集型应用/05-复制.md](../设计数据密集型应用/05-复制.md) 的"异步复制阵营"完全重合。
- **多数据中心一等公民**：`NetworkTopologyStrategy` 每 DC 独立 RF（第 3 章），不是事后补丁。

## 4. 本书读者画像与运维重心迁移

- 作者自述本书面向"日终值守 Cassandra 集群的管理者"（Springer 页三句卖点 ✅ 实抓：
  日管手册 / 真实例子 / 任务步骤与命令）。
- 关系库 DBA 技能对位迁移表（⚠️ 推定重构）：

| 关系库 DBA 习惯 | Cassandra 运维对位 |
|---|---|
| 看慢查询日志 | 看 `nodetool tpstats` 积压 + proxyhistograms（10 章） |
| 索引缺失 → 加索引 | **建模缺失 → 改表/加物化视图**；二级索引是最后手段（4/11 章） |
| 备份 = pg_dump/物理备份 | snapshot + commitlog 回放 + sstableloader（8 章） |
| 主从切换 | 无需切换；但要有 decommission/replace 剧本（3/9 章） |
| 锁等待/死锁 | 无锁 → 取而代之是**修复风暴与墓碑膨胀**（5/11 章） |
| binlog 复制监控 | hinted handoff / 复制欠账 / repair 调度（9/10 章） |

## 5. 版本基线与 2026 读者提醒

- 本书 2017-12 上线，主体面向 Cassandra 3.0 系（3.11 次年 2 月才发布 ⚠️ 推定）；
  thrift 在 3.0 已被降级为"默认不启动"（NEWS.txt 3.0 ✅ 实抓），书中命令基线是 CQL/JMX。
- 2026 视角：当前 GA 为 **5.0**（5.0.9，2026-08-07 ✅ 实抓），5.x 的向量检索/SAI/UCS
  不改变本章的"立场"，但改变 4/6/11 章的最优解——各章末「最新演进」逐条对位。

## 6. 本章运维箴言（精读重构）

1. 别用"能不能连上"判断集群健康，用"延迟直方图 + tpstats"（10 章）。
2. 别把"最终一致"读作"不用管"，管它的形式是 **CL 选型 + repair 节奏**，不是故障工单。
3. 多 DC 不是高可用彩蛋，是容量与网络预算问题：DC 间带宽先于 CPU 见底（3 章）。
4. 任何"复制延迟"告警在本系统里等价于"hinted handoff 积压/修复欠账"（9 章）。

## 7. 版本简史（2010→2017 成书年，⚠️ 社区通述口径）

| 时代 | 标志事件（运维语义） |
|---|---|
| 0.6–0.8 | Apache 顶石；thrift 为唯一门；无 CQL 世界 |
| 1.0–1.2 | CQL 成熟、vnodes 前夜；"类 SQL 幻觉"开始流行 |
| 2.0–2.2 | 物化视图实验、roles 统一用户、vnode 默认化；thrift 弃用预告 |
| 3.0（2016） | **本册基线**：LSM 重写（单写路径/分区缓存）、thrift 默认关、commitlog 段化 |
| 3.9/3.11（2017-2018） | SASI 实验、TWCS/LCS 成熟期；3.11 恰在成书后数月 |
| 4.0（2021） | thrift 与 pre-3.0 格式移除、虚拟表、MV 默认关（见各章文末） |
| 5.0（2024→今） | SAI/vector/UCS/trie/JDK17（00 章对位表） |

## 8. 本章十问（自测，答不出即回读对应节）

1. Cassandra 的六大 Dynamo 继承件各是什么？（§1）
2. "宽列"与"关系表+JSON 列"的本质差别在哪？（§2）
3. 为什么 masterless 集群反而更需要 gossip 健康度监控？（§3）
4. 写路径"本地即算成功的前半"具体指哪两样东西？（§3/05 章预告）
5. DBA 技能迁移表里，"锁等待"的对位病是什么？（§4）
6. 本书成书年 Cassandra 处于哪个大版本？thrift 什么状态？（§5）
7. 为什么说"多 DC 是容量问题不是高可用彩蛋"？（§6）
8. "最终一致"在运维语言里的度量单位是什么？（§6）
9. 郭鹏书/本册/DDCA 三者的阅读顺序建议及理由？（§2、00 章互链表）
10. 2026 年 GA 版本号与运行时 JDK？（§5/00 章对位表）

## 核心概念速览（中英对照）

- **masterless ring** — 无主环：节点同权、gossip 维护成员视图，协调者由客户端自选。
- **Dynamo lineage** — Dynamo 谱系：一致性哈希+quorum+反熵一整套继承自 2007 论文。
- **wide column store** — 宽列存储：分区键→聚簇排序的稀疏列 map，非关系表。
- **eventual consistency** — 最终一致：副本收敛由读修复/提示/修复任务三者驱动。
- **quorum** — 法定人数：R+W>N 时读必见最新写；CL 是运维可调的旋钮。
- **hinted handoff** — 提示移交：目标不可达时暂存写意图，恢复后重放（默认窗口 3h，3.x）。
- **anti-entropy / Merkle tree** — 反熵/默克尔树：副本间比对哈希树找分歧再流式补齐。
- **coordination-free** — 去协调：共识代价在写入侧摊薄，冲突以 last-write-wins 时间戳裁决。
- **data-center-aware replication** — 数据中心感知复制：NetworkTopologyStrategy 按 DC 配 RF。
- **commitlog** — 提交日志：本地写持久化凭证，决定"单节点不丢、集群不保证"语义边界。
- **tombstone** — 墓碑：删除以带 TTL 的标记写入，读侧代价的隐形来源。
- **CQL** — Cassandra Query Language：SQL 外观、按分区建模内核的查询语言。
- **DBA 技能迁移** — skill transposition：慢查询→延迟直方图、锁→修复欠账的运维对位。

## 最新演进与工业实践

- **版本线（✅ 实抓 cassandra.apache.org/_/download.html）**：Latest GA 5.0.9（2026-08-07）；
  4.1.12 维护至 7.0、4.0.21 维护至 6.0 发布；6.0 处 alpha2 阶段。3.x 全部退场，存量书读者
  迁移时注意 4.0 已"移除 pre-3.0 直升路径与 thrift"（NEWS.txt 4.0 ✅）。
- **厂商线（✅ 检索件在档）**：IBM 完成对 DataStax 收购（2025-02 报道）；开源驱动全面 Apache 化
  （cassandra-java-driver 4.19.3、cassandra-spark-connector 3.5.1，api.github.com 实抓）。
  任务注记的"Stargate 落幕"经核验仅能部分成立：stargate/stargate 仓未归档、2026-07 仍有 push ✅；
  "UPTOPIA"无法确指 ⚠️。
- **谱系现状**：Dynamo 思想的另一子嗣 Amazon DynamoDB 走全托管路线（db.md 179 行处条目）；
  开源自托管阵营中 Cassandra 仍是多写/多 DC 场景的默认选项之一，理论纵深请回看
  [../设计数据密集型应用/09-一致性与共识.md](../设计数据密集型应用/09-一致性与共识.md) 与
  [../分布式数据库入门进阶与实战/05-BASE与CAP及分布式一致性模型.md](../分布式数据库入门进阶与实战/05-BASE与CAP及分布式一致性模型.md)。
- **向量时代新画像（✅ 官方 5.0 新特性页实抓）**：vector 类型（CEP-30）让 Cassandra 进入
  AI 检索供应商名单，运维侧的索引/内存预算话题由此增加一整节（见 04/11 章对位）。
