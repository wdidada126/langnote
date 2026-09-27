# 04 MongoDB（Hu(mongo)us）——文档模型

> 对应官方页实抓目录（✅）：Day1 CRUD and Nesting｜Day2 Indexing, Aggregating, MapReduce｜Day3 Replica Sets, Sharding, GeoSpatial, and GridFS｜Wrap-Up。
> MongoDB 本机**无安装**（`where mongo` 无果，⚠️ 不装不测）；聚合/复制/分片的运行行为一律 ⚠️ 转述。🔧 类比用 DuckDB 1.5.5 复现「嵌套数组展开→分组」即 `$unwind`+`$group` 的语义，**非 MongoDB 行为**。
> 纵深：[../MongoDB_The_Definitive_Guide_3e/00-总览与阅读地图.md](../MongoDB_The_Definitive_Guide_3e/00-总览与阅读地图.md)（官方团队著）与聚合专册 [../Practical_MongoDB_Aggregations/00-总览与阅读地图.md](../Practical_MongoDB_Aggregations/00-总览与阅读地图.md)。

## 4.0 文档模型的核心赌注

MongoDB 存 **BSON 文档**（JSON 的二进制超集），一个文档=一个自包含、可嵌套的对象。赌注：**「让数据按应用对象的天然形状存，读写以文档为单位，减少 join」**。schema 灵活（无强制列定义）换来字段演化自由，代价是跨文档关系与一致性要自己设计。

## 4.1 Day 1：CRUD 与嵌套

- **CRUD**：`insertOne/insertMany`、`find` + 查询选择器（`{field:value}`、比较 `$gt/$in`、逻辑 `$and/$or`）、`updateOne/$set`、`deleteMany`。
- **嵌套（Nesting）**：文档内可放**子文档数组**（如 user 里嵌 `tags:[…]`、`orders:[…]`）——「反规范化优先」：读多写少的关联直接塞进一个文档。
- **设计取舍**：内嵌 vs 引用（`$ref`/手工外键）；16MB 文档上限约束内嵌规模（⚠️ 转述，书基线）。
- ⚠️ 转述：Day1 用 `mongosh`（书时代是 `mongo` shell）跑通建库、插嵌套文档、条件查。

## 4.2 Day 2：索引、聚合与 MapReduce

- **索引**：单字段、复合、**多键索引（multikey，自动为数组每个元素建索引）**、文本、TTL、地理；`explain()` 看是否命中。
- **聚合管道（Aggregation Pipeline）**：`$match → $group → $unwind → $project → $sort → $limit …` 的流水线算子；取代早期脆弱的 `group`。
- **MapReduce**：`map` 发键值、`reduce` 归并——聚合管道出现前的复杂聚合手段，现已基本被 pipeline 取代 ⚠️。
- **纵深对照**：聚合管道的每一算子语义在专册有穷举，见 [../Practical_MongoDB_Aggregations/00-总览与阅读地图.md](../Practical_MongoDB_Aggregations/00-总览与阅读地图.md)。

> 🔧 **类比组 D：`$unwind` + `$group`（非 MongoDB，DuckDB 1.5.5 读 JSON）**
> 本机把 3 条含 `tags` 数组的文档塞进表 `t(j JSON)`，用 SQL 模拟「展开数组再按标签计数」：
> ```sql
> SELECT tag, COUNT(*) c FROM (
>   SELECT json_extract(j,'$.user') u,
>          UNNEST(from_json(json_extract(j,'$.tags'),'["VARCHAR"]')) tag FROM t)
> GROUP BY tag ORDER BY c DESC;
> ```
> 真实输出：`[('y',3), ('x',2), ('z',1)]`（✅，3 文档）。这精确对应 Mongo 管道 `[{$unwind:"$tags"},{$group:{_id:"$tags",c:{$sum:1}}}]`：`UNNEST`≈`$unwind`、`GROUP BY … COUNT`≈`$group`。声明：DuckDB ≠ Mongo，无 BSON/多键索引，仅类比「展开-分组」的计算语义。与 02 章 🔧 组 A「join 后分组」形成文档模型 vs 关系模型的手感对照（都写 SQL，数据流不同）。

## 4.3 Day 3：副本集、分片、地理与 GridFS

- **副本集（Replica Set）**：1 主多从、多数派选举、写关注（write concern `w:majority`）、读偏好；高可用的主轴。
- **分片（Sharding）**：按**分片键**把集合切成分块分布到 shard 集群；config server + mongos 路由；分片键选错=热点/全扫。
- **GeoSpatial**：`2dsphere` 索引 + `$near/$geoWithin` 做位置查询。
- **GridFS**：把超 16MB 的大文件切片存库（图片/视频等）——⚠️ 转述，2026 更推荐对象存储。
- ⚠️ 转述：Day3 是本册「从单机玩具到分布式」的跃迁章，但**具体副本/分片命令运行不可本机测**。

## 4.4 Wrap-Up：Mongo 适合什么、不适合什么

- **适合**：对象天然嵌套、字段频繁演化、读以文档为单位、敏捷迭代的中大规模 Web/移动端；用聚合管道做库内分析。
- **不适合**：高度规范化、强跨实体事务（2e 书基线时事务弱；4.0+ 引入多文档事务后差距缩小 ⚠️）、需要复杂关系 join 的报表。
- ⚠️ 转述：与 CouchDB 同属文档 genre，差异在一致性模型（Couch 乐观复制冲突）、查询能力（Mongo 索引/聚合更强）。

## 4.5 本册内互链

- 文档模型另一支（+ 复制/最终一致）→ [05-CouchDB文档与复制.md](05-CouchDB文档与复制.md)。
- 「关系库也能存 JSON」对照 → [02-PostgreSQL关系锚点.md](02-PostgreSQL关系锚点.md) 的 JSONB 一节。
- 键值结构对照 → [08-Redis数据结构服务器.md](08-Redis数据结构服务器.md)。

## 4.6 常见坑与设计要点（⚠️ 转述，Mongo 通识）

- **内嵌的 16MB 天花板**：无限增长的数组内嵌（如「一条帖子下所有评论」）会撑爆文档——该「引用 + 分页」而非无脑内嵌。
- **分片键选错 = 全集群 Scan**：低基数或单调分片键造成热点与「查询广播到所有 shard」；分片键要贴合主查询谓词。
- **multikey 索引不能覆盖排序方向混用**：一个文档多数组 + 复合索引时，`$unwind` 顺序影响能否用索引。
- **写关注/读偏好拉出「读旧」**：`w:1` + 从节点读会读到未同步副本——要读己之写需 `readConcern:majority`。
- **`explain()` 是第一课**：文档库没有「看起来快」，只有 `COLLSCAN` vs `IXSCAN` 的铁证。

## 4.7 Wrap-Up 练习重构（✅ 体例 + ⚠️ 题面转述）

1. 把一组关系表（user + orders）改造成两种方案：**内嵌 orders 进 user** vs **引用**，比较读写放大。
2. 用聚合管道做「按 tag 统计文章数」，再用 🔧 组 D（DuckDB UNNEST）复现同一计算，直观 `$unwind`。
3. **跨库题**：给 Mongo 的热点读加 Redis（[08](08-Redis数据结构服务器.md)）缓存层，谈 cache-aside 与失效。
4. 思辨题：Mongo 的 `$lookup` 已能「join」，这是否让关系库（[02](02-PostgreSQL关系锚点.md)）的优势消失？（答案：join 语义与代价模型仍不同）

## 4.8 mongo shell / 管道小抄（⚠️ 书体例反推 + ✅ 官方常识）

| 目的 | Mongo 写法 | 关系库对照（[02](02-PostgreSQL关系锚点.md)） |
| --- | --- | --- |
| 插文档 | `db.c.insertOne({...})` | `INSERT INTO` |
| 条件查 | `db.c.find({age:{$gt:30}})` | `WHERE age>30` |
| 建索引 | `db.c.createIndex({age:1})` | `CREATE INDEX` |
| 展开数组 | `$unwind:"$tags"` | `UNNEST(...)`（🔧 组 D） |
| 分组 | `$group:{_id, c:{$sum:1}}` | `GROUP BY` |
| 关联 | `$lookup` | `JOIN`（代价模型不同） |
| 副本高可用 | `ReplicaSet` + `w:majority` | PG 流复制 + 同步复制 |

## 4.9 文档建模三法则（⚠️ 转述，Mongo 社区共识）

1. **按查询建模，不按实体建模**：先列出应用的读写访问路径，再决定内嵌/引用——「规范化到第三范式」在文档库里常是反模式。
2. **读写一起涨的放一起，单独更新的分开放**：一个会被独立高频更新的子对象若内嵌，会放大文档搬移（⚠️ 旧版 relocate；现代版已缓解）——用「内嵌有界数据 + 引用无界数据」的经验线。
3. **让索引跟着访问谓词走**：每个主查询都应有一条能命中的复合索引，`ESR 规则`（Equal-Sort-Range 排列复合索引列）是 Mongo 索引设计口诀。

> 与 PostgreSQL 的 JSONB（[02](02-PostgreSQL关系锚点.md) 2.3）对照：两者都能存文档，差别是 Mongo 以文档为一等存储/更新单位、PG 以关系为骨架把 JSON 当列。选谁常取决于「你要不要那套 join/事务/约束」。盘上文档库纵深见 [../MongoDB_The_Definitive_Guide_3e/00-总览与阅读地图.md](../MongoDB_The_Definitive_Guide_3e/00-总览与阅读地图.md)，聚合专题见 [../Practical_MongoDB_Aggregations/00-总览与阅读地图.md](../Practical_MongoDB_Aggregations/00-总览与阅读地图.md)。

## 4.10 高可用与扩展的两条正交轴（⚠️ 转述，Mongo 通识）

- **复制（副本集）**解决「可用性/耐久性」：一主多从、心跳选主、oplog 回放；读写可在主/从间按 `readPreference` 分流。
- **分片**解决「容量/写吞吐」：mongos 路由 + config server 元数据 + 按分片键把集合切成 chunk 自动均衡。
- **两者独立又常同用**：分片集群的每个 shard 本身就是一个副本集——即「先副本、再分片」的标准拓扑。
- 与 HBase（[03](03-HBase列簇与大数据.md)）对照：HBase 靠 RegionServer+ZooKeeper 做区域归属与故障恢复，Mongo 靠副本集+分片键做数据分布——**同为水平扩展，控制面哲学不同**（ZK 中心化 vs 集内置 mongos/config）。

## 核心概念速览（中英对照）

- **BSON / 文档** — 自包含嵌套对象，Mongo 的基本存储单元。
- **查询选择器** — query selector：`{field:{$gt:x}}` 式的声明式过滤。
- **内嵌 vs 引用** — embedding vs referencing：反规范化优先的建模二选一。
- **多键索引** — multikey index：为数组每元素自动建索引。
- **聚合管道** — aggregation pipeline：`$match/$group/$unwind/$project` 流式算子。
- **`$unwind`** — 展开数组为多文档，分组前置步骤（🔧 组 D 类比）。
- **MapReduce** — map/reduce 聚合旧范式，已被 pipeline 边缘化 ⚠️。
- **副本集** — replica set：主从 + 多数派，高可用单元。
- **分片键** — shard key：决定数据分布与查询路由的核心选择。
- **写关注 / 读偏好** — write concern / read preference：一致性与延迟的旋钮。
- **GeoSpatial** — `2dsphere` + `$near` 地理位置查询。
- **GridFS** — 大文件分块存储机制 ⚠️（今多让位对象存储）。
- **mongos / config server** — 分片集群的路由进程与元数据节点。
- **ESR 规则** — Equal-Sort-Range：复合索引列排序口诀。

## 最新演进与工业实践

- **大版本（⚠️ 转述 + 官方文档现状）**：MongoDB 从书基线 3.x 演进到 **8.x**——官方发布说明页 https://www.mongodb.com/docs/manual/release-notes/ ✅ 实测 200，页面枚举 8.0/8.1/8.2/8.3 等现版。
- **事务补齐**：4.0 起多文档 ACID 事务、5.0 分布式事务、`$merge`/窗口函数进 pipeline、查询语言向 SQL 靠拢（`$lookup` 等价 join）——直接削弱了 2e 书里「Mongo 不擅关系/事务」的短板论述。
- **Atlas 与特化能力**：托管 MongoDB Atlas 提供 **向量搜索（Atlas Vector Search）**、时间序列集合、搜索（$search 集成 Lucene）；本册的文档模型 2026 常与「向量 + RAG」组合，见 [../Vector_Databases/00-总览与阅读地图.md](../Vector_Databases/00-总览与阅读地图.md)。
- **一致性/复制原理**：副本集选主、多数派写与「读己之写」的正规论述在 [../设计数据密集型应用/00-总览与阅读地图.md](../设计数据密集型应用/00-总览与阅读地图.md) 复制章节；NoSQL 家族定位见 [../nosql精粹.md](../nosql精粹.md)。
- **取证口径**：目录 ✅ 官方页实抓；聚合/分片/复制运行细节 ⚠️ 转述（本机无 Mongo）；🔧 组 D 为 DuckDB 1.5.5 一手数字且非 Mongo 行为。
