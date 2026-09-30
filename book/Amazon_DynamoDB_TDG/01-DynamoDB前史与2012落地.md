# 01 · DynamoDB 前史与 2012 落地（⚠️ 重构章题）

> 章定位：回答「DynamoDB 不是 Dynamo」。同一血管（Amazon 零售底座），两种生物：2007 论文是去中心化共识实验，2012 服务是把复杂度收归 AWS、把自由度从开发者手里收回的托管产品。本章是全书世界观地基。

## 1. 论文源头：Dynamo（SOSP 2007）

- 出处：DeCandia 等，「Dynamo: Amazon's Highly Available Key-value Store」，SOSP 2007。DOI `10.1145/1294261.1294281` 已过 Crossref 200 校验 ✅（题名/日期 2007-10-14 实测返回），论文精读见仓库笔记 [../paper/SOSP/doi_10.1145_1294261.1294281/00-精读笔记.md](../../paper/SOSP/doi_10.1145_1294261.1294281/00-精读笔记.md)。
- 论文关键词 ⚠️ 转述（上述笔记有全文展开）：始终可用（always-on）、去中心化对等节点、一致性哈希 + 虚拟节点、N/R/W 可调 quorum、读修复/反熵、版本向量处理并发写、hinted handoff。
- 商业动机 ⚠️ 转述：Amazon 购物车对「一分钟宕机损失」的敏感度决定其宁可牺牲强一致也要可用性。

## 2. 内部先行者：从购物车到 SimpleDB

- Dynamo 思想首先在 Amazon 内部购物车状态落地 ⚠️ 转述（AWS 官方沿革页未逐一取证）。
- 2009 年前后 SimpleDB 作为早期托管数据服务存在，配额与吞吐模型受限，后被 DynamoDB 取代 ⚠️ 转述，禁编造细节。
- 关键跃迁：内部 Dynamo 集群由 SRE 团队运维、按 Amazon 负载特化；对外产品必须回答「客户不懂 quorum 怎么写代码」——答案是把一致性档位收敛成两档（最终/强），把复制、分区、修复全部藏进服务（见 02/05/08 章）。

## 3. 2012：SIGMOD 论文与正式发布

- SIGMOD 2012 工业论文：题名「Amazon dynamoDB」，DOI `10.1145/2213836.2213945`，Crossref 校验 ✅（容器题名 2012 ACM SIGMOD International Conference on Management of Data，2012-05-20）。同会相关：「Big Data and NoSQL with Amazon DynamoDB」DOI `10.1145/2378356.2378369`（2012-09-21，workshop）✅ Crossref 校验。
- 产品定位一句话（AWS 官方 Introduction 页实抓 ✅，2026-09-27，HTTP 200，https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html）：全托管 NoSQL 数据库服务，「single-digit millisecond performance at any scale」——页面原文含该短语，多次出现。
- Introduction 页同时证实：键值 + 文档双模型、预置与按需两种容量模式、跨可用区自动复制、按需备份/时间点恢复、流、全球表 ⚠️（页面要点逐条，本章引用其能力清单）。

## 4. 服务化对论文的六项收编（对照表）

| 维度 | Dynamo 论文 ⚠️ | DynamoDB 服务 |
|---|---|---|
| 一致性 | N/R/W 逐操作可调 | 仅两档：最终一致 / 强一致读（✅ HowItWorks.ReadConsistency.html 200） |
| 写冲突 | 版本向量多版本合并 | 单写者语义为主 + LWW（后写覆盖），多活区域另付代价（08 章）⚠️ |
| 分区 | 一致性哈希 + 虚拟节点，节点自管 | 服务自动散列分区键，按吞吐自动分裂/再平衡 ⚠️ 转述 |
| 复制 | 去中心化对等、读修复/反熵 | 同步跨 AZ（表内）；跨区域多活交给 Global Tables（异步）⚠️ |
| 容量 | 集群规划归 SRE | RCU/WCU 显式计费，开发者直接面对（05 章）✅ 概念层 |
| 可用性叙事 | 「为购物车而设计」 | 「为任意规模 Web 应用而托管」 | ⚠️ 混合 |

## 5. 血统分叉：三条 Dynamo 后代线

- 内部演化线：Dynamo → DynamoDB（本册）。
- 开源复刻线：Cassandra（Facebook 起家）论文与 Dynamo 概念亲缘——盘上对位 [../Cassandra_The_Definitive_Guide/00-总览与阅读地图.md](../Cassandra_The_Definitive_Guide/00-总览与阅读地图.md)：把「N/R/W 可调」交还用户，代价是自管集群。
- 原理综述线：DDIA [../设计数据密集型应用/00-总览与阅读地图.md](../设计数据密集型应用/00-总览与阅读地图.md) 第 5/6/9 章把 Dynamo 作为「最终一致性谱系」标本 ⚠️ 转述章号对应盘上实名文件（[05-复制.md](../设计数据密集型应用/05-复制.md)、[06-分区.md](../设计数据密集型应用/06-分区.md)）。
- 同厂对照：Redis 也讲「简单模型换规模」，但内存优先、可丢可重建的缓存语义与 DynamoDB 持久语义相反——对位 [../Learning_Redis/00-总览与阅读地图.md](../Learning_Redis/00-总览与阅读地图.md)（其 05 持久化章与本章「持久语义」互读）。

## 6. 时间线：2012 → 2026（要点均指向后续章）

- 2012 GA；2013+ GSI/Streams 生态 ⚠️ 具体月份未逐一取证，不写月日。
- 2017：DAX、Global Tables 首发 ⚠️ 转述（特性页 ✅：DAX.html、GlobalTables.html 均在 200 页证实存在，年份为社区通识）。
- 2018：按需容量模式、事务读写 ⚠️（Introduction 页证实 on-demand 现名 ✅；transactions.html 200 证实事务现名 ✅）。
- 2021-22：Global Tables v2 世代（✅ GlobalTables 页原文含「Version 2」字样，2026-09-27 实抓）。
- 2025+：向量索引与 SearchVectors API（✅ 实抓 VectorSearch.html 200，页面含「ANN」「cosine」「Euclidean」；API 参考 API_SearchVectors.html 200）——10 章展开。
- 本书成书时窗推定 2021-22（00 §1），意味着**书中索引/容量章大概率不覆盖向量检索**，阅读时按本目录 10 章补差。

## 7. 为什么「无账号不可测」仍值得学

DynamoDB 的知识密度不在操作手感，而在**建模即架构**（键选择=分区命运，05/06 章）与**计费即设计**（RCU/WCU 直接改写数据布局）。这也是本册 🔧 类比只用 SQLite/DuckDB 演示「键布局→访问代价」因果、而绝不假装演示 DynamoDB 行为的原因（00 §9 纪律）。类比组见 02（聚类存储）、04（索引副本）、05（计费算术）、06（行尺寸代价）四章。

## 8. 论文六关键词逐条展开 ⚠️（每条=一个后续章的回响）

- **始终可用（always-on）**：任何时刻可读可写，拒绝「维护窗口」。→ 回响 08 章多活：可用性被买到，代价是 LWW 语义。
- **quorum N/R/W**：副本数/读写确认数三参数。→ 服务化后收敛为两档一致性（03 章 §5），用户不再碰 R/W。
- **一致性哈希**：节点进出只搬相邻数据段。→ 服务内部改「按键哈希+自动分裂」（02 章 §2），用户只感知键选择责任。
- **版本向量**：并发写各留版本、读时合并。→ 被 LWW 替换（08 章 §3）——DynamoDB 三十年最大的语义让步。
- **hinted handoff**：节点暂死时邻居代写、复活补交。→ 托管内部黑盒 ⚠️，用户不可见不可调。
- **读修复/反熵**：读时顺手纠偏+后台全量比对双通道。→ 仍存在于服务内部，叙事从「你配置」变「服务负责」（09 章责任边界）。

## 9. 常见误解纠偏（问答式）

- Q：DynamoDB 是 Dynamo 的直接改名吗？
  A：否。共享工程哲学，架构、一致性模型、运维模型都重写 ⚠️/✅（两代论文/文档各自在架）。
- Q：用了 DynamoDB 就自动获得论文级「始终可用」？
  A：服务 SLA 层面高可用，但你的表仍可能因热点键/限流自伤——可用性责任分账（05 章）。
- Q：DynamoDB 与 DocumentDB（兼容 Mongo 的托管服务）同族吗？
  A：不同族：前者 Dynamo 血统键值/文档，后者 Mongo 协议托管 ⚠️；命名易混，谱系各归各。
- Q：Cassandra 是不是「开源 DynamoDB」？
  A：方向相反——Cassandra 借 Dynamo 的去中心化机制，DynamoDB 走 SaaS 集中式路线；详见 [../Cassandra_The_Definitive_Guide/00-总览与阅读地图.md](../Cassandra_The_Definitive_Guide/00-总览与阅读地图.md) 谱系章域。

## 10. 本章自测（合卷作答）

1. 说出论文到服务的六项收编中你认为最痛的两项，并解释痛在哪个章被「收费」。
2. 「DynamoDB 没有版本向量」为什么反而让全局表能商用？（提示：08 章 LWW 账单）
3. 为什么本册坚持「无 AWS 账号」仍能写出有证据的笔记？说出三态纪律在你章内读到的两处实例。
4. SIGMOD 2012 论文的 Crossref 校验结果是什么？它证实了「发布年」到什么粒度？
5. 给 Redis/Cassandra/DynamoDB 各配一句话，沿「自由度 vs 托管度」轴摆放。

## 11. 回链索引（本章概念→落地章）

- quorum 收敛 → 03 §5 一致性两档
- 一致性哈希 → 02 §2 分区键命运 → 06 §5 反模式刑场
- 版本向量被弃 → 08 §3 LWW 账单
- hinted handoff/读修复进黑盒 → 09 责任边界
- on-demand 名词首次落地 → 05 §1
- 「持久语义」对照 Redis 可丢语义 → 02 §5、05 §4
- 论文细节请移步：[../../paper/SOSP/doi_10.1145_1294261.1294281/00-精读笔记.md](../../paper/SOSP/doi_10.1145_1294261.1294281/00-精读笔记.md)（本目录唯一的「论文原文代理」）
- DDIA 坐标：[../设计数据密集型应用/00-总览与阅读地图.md](../设计数据密集型应用/00-总览与阅读地图.md) 全书「Dynamo 条目」的学术表述

## 12. 一句话记忆卡（背下来就带走本章）

- 2007 论文给自由度，2012 服务给确定性——你付的是语义收缩的学费。
- Dynamo≠DynamoDB，如同蓝prints≠量产车。
- 两档一致性是 quorum 参数被托管后的「安全简化」。
- LWW 不是技术上限，是商用妥协（详见 08 章账单）。
- Cassandra 拿走论文的自由端，DynamoDB 拿走托管端，DDIA 拿着讲义。
- 时间线读法：每章只记「哪年上了什么」，细节永远现查文档。
- 引用论文与发布论文两枚 DOI 已 Crossref 校验，可放心具名。

## 核心概念速览（中英对照）

1. **全托管 NoSQL** — fully managed NoSQL：复制/分区/修复由服务承担，用户只面对表与吞吐。
2. **个位数毫秒** — single-digit millisecond：AWS 官方定位语，实抓 Introduction 页 ✅。
3. **N/R/W 副本参数** — replication parameters：Dynamo 论文的可调一致性，服务化后被收敛。
4. **版本向量** — version vector：论文处理并发多写的机制；DynamoDB 以单写者+LWW 替代 ⚠️。
5. **读修复/反熵** — read repair / anti-entropy：论文副本收敛双通道；服务内部实现不外露 ⚠️。
6. **一致性哈希** — consistent hashing：论文分区法；服务改按分区键哈希自动分裂 ⚠️。
7. **简单写者语义** — single-writer emphasis：托管表以「一行一主」常规写为主场景 ⚠️ 转述。
8. **血统分叉** — Dynamo lineage：DynamoDB/Cassandra/DDIA 综述三条后代线。
9. **键值+文档双模** — key-value and document：官方定位的模型表述 ✅。
10. **SIGMOD 2012 工业论文** — Amazon dynamoDB paper：DOI 10.1145/2213836.2213945 ✅ Crossref 校验。
11. **计费即设计** — pricing as design：容量单位直接决定数据布局的因果观。

## 最新演进与工业实践

- **论文与产品分离叙事已成行业模板**：Dynamo(2007)→DynamoDB(2012) 与 Bigtable→Cloud Bigtable、Aurora 论文→服务的谱系同构；盘上对位 [../Database_Internals/00-总览与阅读地图.md](../Database_Internals/00-总览与阅读地图.md)（引擎视角）与 [../Streaming_Systems/00-总览与阅读地图.md](../Streaming_Systems/00-总览与阅读地图.md)（系统→产品同理）。
- **两枚 DOI 复核状态（2026-09-27）**：`api.crossref.org/works/10.1145/1294261.1294281`→200 ✅；`10.1145/2213836.2213945`→记录题名「Amazon dynamoDB」SIGMOD 2012 ✅；引用可放心。
- **AWS 官方沿革页**：Introduction 与「first-time users」资源页持续更新（docs 域名 200 实抓 ✅），2026 视角下 DynamoDB 叙事已加「generative AI 数据底座」章节倾向（向量索引入主文档 ✅ 见 10 章），本书 2021 基线文本需按此补差。
- **工业采用口径 ⚠️**：游戏会话/购物车/无服务器 API 后端为官方 customer story 高频场景，属转述；无本册可实证的部署统计，不编数字。
- **阅读姿态**：把 01 当「词汇表」读——后续 9 章每条「服务为什么这样设计」的追问，答案都能回到本章的六项收编表。
