# 14 NoSQL 与大数据

> 单元性质：⚠️ 主题重构。对应教材通行"NoSQL / Big Data / 新技术"收尾单元（本书公开简介明言 "challenges associated with handling large datasets"，此单元为 4e 相对前版的强化方向之一 ⚠️ 推断）。深度对照：[../数据库系统概念6/22-基于对象的数据库.md](../数据库系统概念6/22-基于对象的数据库.md)、[../数据库系统概念6/23-XML.md](../数据库系统概念6/23-XML.md)、../数据库系统概念7.md（NoSQL/NewSQL 扩充章）；中文对照：../数据库系统概论.md 第四篇（大数据管理/内存数据库）；专册四路：DynamoDB/Couchbase/Cassandra 目录（本文件末链接）。

## 1. 动机：三 H 与规模经济学

High performance（海量并发/吞吐）、High scalability（透明扩容）、High availability（异构网络容灾）；当"关系四件套（03 章约束+09–11 保证）"的协调成本超过业务收益，社区选择**换契约**——NoSQL 不是语言（Not Only SQL 的正名），是**契约重新谈判**。

## 2. CAP 与 PACELAC 类谱系

分区容忍不是可选项（跨机房必带），实际二选一在 C 与 A；一致性谱系（线性/顺序/因果/最终）+ BASE（软状态/最终一致，10 章对立面）。⚠️ 严格陈述（Brewer 猜想、Gilbert-Lynch 1902.3360 证明）细节以论文线为准：[../../db/db.md](../../db/db.md)。教学要点：**CAP 只在分区期生效**，平局期 C/A 可兼得——把 CAP 当"永远二选一"是教材级误读。

## 3. 四族模型与代表系统

- **键值（key-value）**：DynamoDB（哈希分区+R/W/CU 配额+条件写/流式 CDC）；最自由契约族（[../Amazon_DynamoDB_TDG/00-总览与阅读地图.md](../Amazon_DynamoDB_TDG/00-总览与阅读地图.md)）。
- **文档（document）**：MongoDB/Couchbase；内嵌数组/子文档正名 02 章"多值属性"；模式灵活≠无模式（应用即校验器）（[../Developing_with_Couchbase_Server/00-总览与阅读地图.md](../Developing_with_Couchbase_Server/00-总览与阅读地图.md)）。
- **列族（wide-column）**：Cassandra/Bigtable/HBase；**分区键+聚簇键**取代索引；反规范化查询驱动（06 章赎买术的体系化）；LSM 写路径（07 章对偶）（[../Cassandra_The_Definitive_Guide/00-总览与阅读地图.md](../Cassandra_The_Definitive_Guide/00-总览与阅读地图.md)）。
- **图（graph）**：Neo4j 等；关系即一等公民（外键的"遍历升格"）；SQL:2023 PGQ 标准化（03 章外键视角对勘）。
选型口令：**访问模式形状决定存储形状**；07 索引思想在列族"聚簇键即索引"处复生。

## 4. 半结构化进关系屋：JSON 的双城记

关系内的 JSON 列 + json 函数：🔧 exp5 实测 SQLite（3.45.3）`json_extract(payload,'$.name')='Eve'`、`json_array_length(...)=2`、表值 `json_each` 展数组为行 [('sql',),('nosql',)]；DuckDB 侧 JSON 类型/`read_json_auto`/UNNEST 同题可跑（专册演练见 [../DuckDB_Up_and_Running/06-DuckDB与JSON文件.md](../DuckDB_Up_and_Running/06-DuckDB与JSON文件.md)）。"文档模型住进 SQL 引擎"意味着教材 NoSQL 章与 SQL 章的边界在 2024–2026 已实质模糊——PG 的 JSONB+GIN 索引、SQLite 生成列+索引把"文档+二级索引"配齐。

## 5. MapReduce 时代与流批之后

教材传统含 Hadoop/MapReduce（分片 map→洗牌→聚合 reduce）与列式（CFile→Parquet）铺垫；2024–2026 实况：批=Spark/引擎直读湖（13 章湖仓）、流=Flink/Kafka 生态；"大数据架构"叙述从三层（LR/Lind 分类）转向湖仓一体+流式物化视图 ⚠️ 术语演进以各平台文档为准。

## 6. NewSQL 与 Polyglot 持久化

NewSQL=关系语义+分布式扩展（Spanner 真时基/F1 异步复制、TiDB/CockroachDB——13 章 2PC 的继任者）；多语言持久化按族用库（用户画像文档+计数键值+社交图），代价=跨库事务与对账逻辑上移应用——09 章幂等、10 章补偿（Saga）在此成套复活。

## 7. 与全书的收束：概念账本清点

| 本书前段概念 | NoSQL 世界的转世 |
|---|---|
| 03 键/参照完整性 | 分区键/聚簇键；应用层引用校验 |
| 02 多值属性 | 文档内嵌数组 |
| 06 反规范化 | 查询驱动宽表设计 |
| 07 B+ 树 vs 散列 | 聚簇有序 vs 哈希分区 |
| 09 事务/10 隔离 | 分区级 ACID、quorum、Saga |
| 11 WAL | LSM 的 WAL 段刷盘 |
| 12 权限 | 托管 IAM 策略 |
| 13 复制 | 多区域/CRDT 系 |

## 8. 常见错误清单

1. "NoSQL=没有 SQL"（查询语言各族都有，CQL/SQL 兼容层渐多）。
2. 把最终一致读当"读到的一定对，只是晚点"——写偏斜/lost update 在新外衣下回归（10 章病例库复用）。
3. 文档内嵌无限膨胀（子文档替代外键→文档 16MB 墙与更新放大）。
4. 分区键选错导致热分区（"访问模式先行"是唯一解药）。
5. 忽略数据本地合规（区域驻留）——12 章治理的分布式变体。

## 9. 小结

NoSQL 章的教学功能不是"介绍时髦库"，而是**给全书的关系契约做反证实验**：每放松一条（原子性/参照/隔离/一致性），病从哪回来，药在哪层配。至此 14 单元闭环；重读顺序建议见 00 第十节。

## 10. 补充：exp5 JSON 实验的逐行讲义（文档↔关系双城记）

```python
c.execute("INSERT INTO docs VALUES(1,'{\"name\":\"Eve\",\"tags\":[\"sql\",\"nosql\"],\"score\":9.5}')")
c.execute("SELECT json_extract(payload,'$.name'), json_array_length(payload,'$.tags') FROM docs")
# 🔧 实测输出 ('Eve', 2)
c.execute("SELECT j.value FROM docs, json_each(json_extract(docs.payload,'$.tags')) j WHERE docs.id=1")
# 🔧 实测输出 [('sql',),('nosql',)]  ——数组"摊平"即隐式 1:N 表
```

要点三连：① `json_each` 是**表值函数**，把内嵌数组临时物化为关系——文档与关系的桥就在这类原语上；② 查询侧可加"生成列+索引"给高频路径（`json_extract(payload,'$.name')` 建索引），复刻文档库二级索引；③ 写入侧无 schema 校验=03 章约束全部让位应用——本单元"契约谈判"的微观现场。DuckDB 侧同题：`SELECT * FROM (SELECT '{"a":[1,2]}'::JSON j), UNNEST(CAST(j.a AS INT[]))` 风格更类型化 ⚠️ 未在目录脚本内实测，仅作写法提示。

## 11. 补充：四族模型的"一个业务四种建法"演练

需求："用户动态流（写多读少、按时间范围拉、可容忍短暂旧）。"

- 关系：`posts(id,user_id,ts,body)`+索引 (user_id,ts)——事务齐但写放大痛（07）。
- 键值：`feed:{user}`→整段 JSON blob——读一次拿全，写即覆盖，并发编辑丢更新（10 章病回魂）。
- 文档：帖子嵌评论——嵌套深度与 16MB 墙（本节错误清单 3）。
- 列族：分区键 user_id、聚簇键 desc(ts)——**为"按时间拉流"这一查询形态而生**，教科书级匹配。
演练目标：让"访问模式决定存储形状"从口号变成能自己论证的选型报告。

## 12. 补充讨论：为什么 NoSQL 章必须放在全书最后

教学逻辑上它是**反证法终章**：ACID/规范化/索引/权限全部讲完后，学生才有资格"有意识地拆"。顺序反过来会教出"先学 MongoDB 的人以为 schema 是束缚"的世代替换事故。本目录把它置于 14 单元末位正是此因；自测标准=能用 03/09/11 三章术语各写一段"如果去掉这个保证会发生什么"。

## 13. 自测四问

1. 聚簇键为何同时是"排序键+索引+分区内约束"三合一？（Cassandra 家族：同一列决定物理序、范围读、以及"分区内键唯一"的参照语义——关系世界拆成三个机制的东西列族焊成一体。）
2. "最终一致"期间用户看到旧值，产品层怎么补？（版本戳/软锁/写回执轮询/乐观 UI——契约放松的成本转嫁到体验层。）
3. 多区域写同一键的冲突解法谱系？（LWW→向量时钟→CRDT→应用级合并；LWW 即"时钟同步假设"的赌博 ⚠️ 转述。）
4. 为什么说"文档模型让 02 章多值属性回家"但也带回 06 章哪些病？（内嵌数组免 JOIN 但更新放大/重复事实/一致性无引擎兜底——反规范化的所有代价按期支付。）

## 14. 延伸阅读路径

- 专册四路：[../Amazon_DynamoDB_TDG/00-总览与阅读地图.md](../Amazon_DynamoDB_TDG/00-总览与阅读地图.md)（键值/托管）、[../Developing_with_Couchbase_Server/00-总览与阅读地图.md](../Developing_with_Couchbase_Server/00-总览与阅读地图.md)（文档/N1QL）、[../Cassandra_The_Definitive_Guide/00-总览与阅读地图.md](../Cassandra_The_Definitive_Guide/00-总览与阅读地图.md)（列族）、[../Data_Mesh/00-总览与阅读地图.md](../Data_Mesh/00-总览与阅读地图.md)（组织视角）。
- 教材对照：../数据库系统概念7.md 的 NoSQL/NewSQL 章（波1 主线里与本单元同题的最近邻）。
- 论文线：[../../db/db.md](../../db/db.md)（Dynamo/CAP/Bigtable 三篇原文谱系，⚠️ DOI 引用前逐条过校验）。
- 湖仓接口：[../DuckDB_Up_and_Running/06-DuckDB与JSON文件.md](../DuckDB_Up_and_Running/06-DuckDB与JSON文件.md)（半结构化的"回关系家"实操）。

## 核心概念速览（中英对照）

- **NoSQL (Not Only SQL)** — 非关系契约族系的正名
- **three highs** — 三高：性能/可扩展/可用动机
- **CAP theorem** — CAP：分区期 C 与 A 的取舍
- **eventual / causal / linearizable consistency** — 最终/因果/线性一致：谱系三标尺
- **BASE** — 软状态+最终一致：对 ACID 的集体弃权书
- **key-value store** — 键值库：最简契约（DynamoDB 代表）
- **document store** — 文档库：内嵌结构正名多值属性
- **wide-column / partition key / clustering key** — 列族/分区键/聚簇键：索引的分布式转世
- **graph database** — 图库：遍历升格；SQL:2023 PGQ
- **quorum R+W>N** — 法定数（13 章）在 NoSQL 的实现体
- **CRDT** — 无冲突复制数据类型：用结构换协调（⚠️ 深化另读）
- **JSON functions / json_each / JSONB** — 关系屋里的文档（🔧 exp5 实测）
- **MapReduce** — 分片映射聚合：批处理古范式
- **NewSQL** — 关系语义+水平扩展的第三路
- **polyglot persistence** — 多语言持久化：按族选库
- **hot partition / partition skew** — 热分区：键选错的代价

## 最新演进与工业实践

- **向量数据库与 AI 检索层（2024–2026 最热增量）**：pgvector/Milvus/Qdrant/各托管向量库把"相似性查询"做成新第五族；教材 NoSQL 四族分类法需加注"向量/混合检索"一栏 ⚠️ 版本生态碎片化。
- **文档族关系化回流**：MongoDB 4+ 多文档事务、DynamoDB 条件写+LWT 类语义——NoSQL 阵营重新赊账 ACID（本目录"契约反证"论的当代注脚）。
- **PostgreSQL 通吃争议**：JSONB+全文+向量+扩展生态令"专用族"收缩；托管 NoSQL 向"平台内多模型"（Aurora DSQL、多模型 Mongo/Redis 平台）迁移 ⚠️ 转述。
- **湖上 NoSQL 形态**：Iceberg/Delta 把宽表/文档半结构化统一为列式文件+事务元数据，Spark/DuckDB 直读（[../DuckDB_in_Action/05-无持久化的数据探索.md](../DuckDB_in_Action/05-无持久化的数据探索.md)）——教材大数据篇的下一代写法大概率以此为默认。
- **教学可复现**：本单元全部"关系侧"断言以 🔧 exp5 的 SQLite/DuckDB JSON 实验为证；NoSQL 侧系统不可本机实测（托管为主），一律 ⚠️ 转述并引盘上专册目录。
