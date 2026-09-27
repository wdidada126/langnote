# 07 DynamoDB（The "Big Easy" of NoSQL）——托管宽列/键值

> 对应官方页实抓目录（✅）：Day1 Let's Go Shopping!｜Day2 Building a Streaming Data Pipeline｜Day3 Building an "Internet of Things" System Around DynamoDB｜Wrap-Up。
> **这是 2e 新增的一章**（1e 对应位置是 Riak，✅ 官方页访谈明确「new chapter on DynamoDB」）。
> DynamoDB 是 AWS 托管服务，本机**无法安装/连接**（⚠️ 全程转述 + ✅ 官方文档 URL 取证）。🔧 类比用 SQLite 3.45.3 复现「Query（走键）vs Scan（全表）」的成本差，**非 DynamoDB 行为**。
> 谱系：同为宽列/海量写对照见 [03-HBase列簇与大数据.md](03-HBase列簇与大数据.md)、[../Cassandra_The_Definitive_Guide/00-总览与阅读地图.md](../Cassandra_The_Definitive_Guide/00-总览与阅读地图.md)；托管 Dynamo 专册为同波兄弟 #113（登记不链）。

## 7.0 定位：把 NoSQL 运维「外包」给云

DynamoDB 源自亚马逊 Dynamo 论文，是**全托管、按键访问、自动分片、按需/预置吞吐**的 NoSQL。与 HBase/Cassandra「自建、要管一堆节点」相反，Dynamo 的卖点是**你只管数据模型与访问模式，扩展/多活/备份交给 AWS**。代价：**只能用主键访问**（Query/GetItem）、无任意 ad-hoc 查询、按吞吐计费——模型设计（尤其「单表设计 single-table design」）决定一切。

## 7.1 Day 1：Let's Go Shopping!（电商主键建模）

- **表 = 分区键 + 排序键**：`PK`（决定分片分布）+ 可选 `SK`（分区内排序）。`GetItem`(PK+SK 精确) / `Query`(PK 相等 + SK 条件) 是两条主路；**跨分区无键条件查询只能 `Scan`**（贵）。
- **Item**：JSON 文档，属性可有可无（schema-on-write，仅键是强制的）。
- **读写吞吐模型**：预置（RCU/WCU）或按需（on-demand）；热点分区被限速（throttling）。
- ⚠️ 转述：Day1 用产品/订单场景建表，强调「访问模式先于建模」。

> 🔧 **类比组：Query 走键 vs Scan 全表（非 DynamoDB，SQLite 3.45.3）**
> DynamoDB 的「有键才快、无键只能扫」用 SQLite 直接可感。本机 `items(pk,sk,attr)` 灌 **20 万行**（pk=`cust#0..999`、sk=`order#i`），建复合索引 `ix(pk,sk)`：
> ```sql
> SELECT count(*) FROM items WHERE pk='cust#7' AND sk LIKE 'order%';  -- ≈Query(单分区)
> SELECT count(*) FROM items WHERE attr LIKE 'a12%';                 -- ≈Scan(非键条件)
> ```
> 真实输出：**Query 类**命中 200 行、**0.00008s**；**Scan 类**命中 11111 行、**0.00880s**（约 110×，✅）。这与 DynamoDB「Query 只读你分区、Scan 读全表并计费全表」的成本直觉一致。声明：SQLite 是本地文件、无分区/RCU 概念，仅类比「键路径 vs 全扫」的数量级差。

## 7.2 Day 2：Streams → 流式数据管道

- **DynamoDB Streams**：表变更的**近实时追加日志**（`NEW_IMAGE`/`OLD_IMAGE`，键/新/旧/全四种视图），Kinesis 兼容。
- **触发 Lambda**：Streams → AWS Lambda 做 ETL/物化/索引旁路，构成「变更驱动」的无服务器管道（Change Data Capture 范式）。
- **典型模式**：写 Dynamo → Stream → Lambda 同步到 OpenSearch（补 Dynamo 缺的全文检索）或到 S3（数据湖）。
- ⚠️ 转述：Day2 把 Dynamo 放进「事件驱动微服务」中枢；真实触发延迟/重试行为不可本机测。

## 7.3 Day 3：围绕 Dynamo 建 IoT 系统

- **时序写入模式**：设备遥测按 `(设备ID, 时间戳)` 建表，TTL 自动过期冷数据。
- **热点规避**：加盐（salt）分区键、按时间分桶，避免单分区过载 ⚠️。
- **周边拼装**：IoT Core → Dynamo 存状态、Streams → Lambda 告警、Glue/Athena 旁路分析（把「不能 ad-hoc 查」的短板外包给 Athena 扫 S3）。
- 结论（⚠️ 转述）：Dynamo 常作「高并发写 + 低延迟按键读」的**后端粘合层**，而不是唯一数据库。

## 7.4 Wrap-Up：Dynamo 适合什么、不适合什么

- **适合**：可预测访问模式（已知要按哪些键查）、高并发低延迟读写、serverless/微服务栈、需要托管多活与自动扩缩。
- **不适合**：ad-hoc 分析/复杂查询、跨实体即席 join、需要 SQL 报表、成本敏感且访问模式多变（计费随吞吐涨）。
- ⚠️ 转述：与 HBase 同「宽列/海量写」，分野是**运维模型**（托管 vs 自建）与**访问自由度**（仅键 vs 可配覆盖层）。

## 7.5 本册内互链

- 自建宽列对照 → [03-HBase列簇与大数据.md](03-HBase列簇与大数据.md)（同为海量写，运维相反）。
- 补检索短板（Dynamo→OpenSearch）→ [../Elasticsearch_The_Definitive_Guide/00-总览与阅读地图.md](../Elasticsearch_The_Definitive_Guide/00-总览与阅读地图.md)。
- 键值/文档谱系定位 → [../nosql精粹.md](../nosql精粹.md)、[../设计数据密集型应用/00-总览与阅读地图.md](../设计数据密集型应用/00-总览与阅读地图.md)。

## 7.6 常见坑与设计要点（⚠️ 转述，DynamoDB 通识）

- **建模即命运**：访问模式没在建表期想清楚，事后加 GSI（全局二级索引）既贵又受限（每表 GSI 数有上限、写放大）。
- **Scan 是账单炸弹**：无键条件查询走 Scan = 读全表并按容量计费；生产里几乎总该被 Query + 合理 key 取代（🔧 组的 110× 差就是它）。
- **10:1 读写比与 RCU 单位**：强一致读消耗的读单元是最终一致的 2 倍——「能不能接受稍旧」直接决定成本。
- **Item 400KB 上限**：单文档/属性总量受限，大对象走 S3、表里只放引用。
- **条件写与幂等**：`ConditionExpression` + 客户端生成 id 实现乐观锁/幂等，避免「读-改-写」竞态。

## 7.7 Wrap-Up 练习重构（✅ 体例 + ⚠️ 题面转述）

1. 用「单表设计」把 `Customer` 与 `Order` 两类实体放进一张表（PK 复用 `cust#id`、SK 用前缀区分实体），体验 Dynamo 的建模范式。
2. 用本机 🔧（SQLite 复合索引）复现「有 key 的 Query」与「无 key 的 Scan」数量级差，再回到 Dynamo 谈 RCU 计费。
3. **跨库题**：Dynamo 存事件 → Streams → Lambda 写进 OpenSearch 补全文检索（[../Elasticsearch_The_Definitive_Guide/00-总览与阅读地图.md](../Elasticsearch_The_Definitive_Guide/00-总览与阅读地图.md)），体会托管栈的「拼装哲学」。
4. 思辨题：同为宽列，HBase（[03](03-HBase列簇与大数据.md)）「自建可控、能跑 MR/Spark」，Dynamo「托管省心、锁 AWS」——运维 vs 自由，你选哪端？

## 7.8 DynamoDB API/概念小抄（⚠️ 书体例反推 + ✅ 官方文档常识）

| 目的 | DynamoDB 操作 | HBase 对照（[03](03-HBase列簇与大数据.md)） |
| --- | --- | --- |
| 精确取 | `GetItem(PK,SK)` | `get 't','row'` |
| 按键查 | `Query(PK + SK 条件)` | `scan` STARTROW/STOPROW |
| 全表 | `Scan(+Filter)` | `scan 't'`（无 rowkey 过滤） |
| 条件写 | `PutItem + ConditionExpression` | check-and-mutate |
| 二级索引 | GSI / LSI | Coprocessor/反向表 |
| 变更流 | Streams → Lambda | 走 HBase Coprocessor/Phoenix ⚠️ |

> 记忆钩子：Dynamo 把「运维复杂度」外包给 AWS，把「建模复杂度」还给你——省的是 HDFS/ZK（[03](03-HBase列簇与大数据.md)），欠的是「只能按 key 说话」的设计债。

## 7.9 访问模式驱动建模（Single-Table Design，⚠️ 转述）

Dynamo 的「只能按 key」逼出一套独特建模法，AWS 官方称之为**单表设计**：
1. **先枚举所有查询**（如「查某客户全部订单」「按日期取某订单」），每个查询都必须能翻译成一次 `Query(PK=,SK begins with=)`。
2. **把多实体塞进一张表**，用 SK 前缀区分实体类型：`PK=cust#123, SK=order#2024-01#o999`——查询用前缀切片，关联用同 PK 一次取回。
3. **用 GSI 造「第二把钥匙」**：把「按状态查订单」这种非主键需求，通过一个投影 GSI（把 `status` 映射成新 PK）满足——但每把额外钥匙都增写放大与成本。
4. **反模式**：想要「按任意属性即时过滤」→ Dynamo 天生不合（Scan 贵），该换 Mongo（[04](04-MongoDB文档模型.md)）/ES 或加读模型。

> 与 HBase（[03](03-HBase列簇与大数据.md)）的镜像教训：两者都「以 key 为纲」，但 HBase 至少能 `scan` 全表离线交 Spark 补算，Dynamo 把这条也按容量计费堵死——所以 Dynamo 更「设计前置、事后难补」。托管 Dynamo 的纵深专册为同波兄弟（见 [00](00-总览与阅读地图.md) 互链义务登记），本册不并档。

## 7.10 为什么 2e 把 Riak 换成 DynamoDB（取证 + 推断）

- ✅ 官方页作者访谈明确「2e 新增 DynamoDB 一章」，并保留 HBase/Mongo/Couch/Redis/Neo4j/Postgres；结合 1e 中译《七周七数据库》目录（PostgreSQL/Riak/HBase/MongoDB/CouchDB/Neo4j/Redis，见 [00](00-总览与阅读地图.md) 版次辨析），可确认 **2e 用 DynamoDB 替换了 1e 的 Riak**。
- ⚠️ 推断动机：Riak（Basho）在书成后公司停运、生态凋零；Dynamo 作为「托管 NoSQL 的工业代表」更贴近 2018 读者真实选型——这是「Seven Databases」跟着工业界换人的直接证据。
- 结构后果：Riak 时代讲「对象存储 + MapReduce 索引 + Dynamo 式复制」，DynamoDB 章改讲「按键访问 + Streams 管道 + 单表设计」——同为 NoSQL，但一个是自建去中心、一个是托管云原生，教学侧重整体迁移。

## 核心概念速览（中英对照）

- **托管 / serverless** — 扩展、多活、备份由云负责。
- **分区键 / 排序键** — partition key / sort key：唯一强制的 schema，决定分布与访问。
- **GetItem / Query / Scan** — 精确取 / 按键查 / 全表扫（贵）三档访问。
- **单表设计** — single-table design：用 PK/SK 前缀把多实体塞进一张表。
- **RCU / WCU** — 读写容量单元：吞吐与计费的度量。
- **预置 vs 按需** — provisioned vs on-demand capacity。
- **热点 / 加盐** — hot partition / salting：分布不均与规避手法。
- **DynamoDB Streams** — 表变更追加日志（CDC 源）。
- **Kinesis 兼容模式** — Streams 以 Kinesis API 形式被消费 ⚠️。
- **TTL** — 属性级自动过期，用于时序冷数据。
- **Lambda 触发** — Streams 驱动的无服务器处理。
- **GSI / LSI** — 全局/本地二级索引：Dynamo 里「第二把钥匙」的来源。
- **PartiQL** — Dynamo 之上的 SQL 式查询层（2019 后增补 ⚠️）。

## 最新演进与工业实践

- **持续加特性（⚠️ 转述 + ✅ 官方文档）**：AWS DynamoDB 开发者指南 https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ ✅ 实测 200、产品页 https://aws.amazon.com/dynamodb/ ✅ 200。书基线（2018）之后的关键增量：**on-demand 容量模式、global tables 多活、transactional read/write（TransactGet/TransactWrite）、 PartiQL（给 Dynamo 加 SQL 层）、resource-based policy、change data capture to Redshift/Kinesis 集成**。
- **PartiQL 补 ad-hoc**：DynamoDB 引入 PartiQL（`SELECT` 语法 + `INSERT/UPSERT`）正面回应「不能 ad-hoc 查」的批评（⚠️ 部分场景仍以键为骨架）。
- **本地开发 DynamoDB Local**：官方离线容器 `DynamoDB Local`（NoSQL Workbench GUI 建模）——本波纪律下仍 ⚠️ 未装未跑，仅登记为 2e 之后工程体验改善。
- **2025 方向（⚠️ 转述）**：v2 API、Kinesis 兼容流式、`returnValuesOnConditionCheckFailure`、批量分页、`executeTx` 等细粒度增强；全局二级索引（GSI）继续是「补二级访问」的主手段。
- **同源理论**：键值/宽列的一致性与分片论述见 [../设计数据密集型应用/00-总览与阅读地图.md](../设计数据密集型应用/00-总览与阅读地图.md)。
- **取证口径**：目录 + 2e 新增 Dynamo ✅ 官方页实抓；托管行为/计费/Streams 运行 ⚠️ 转述；🔧 Query-vs-Scan = SQLite 3.45.3 一手数字且非 Dynamo 行为。
