# 06 Neo4j（Neo4j Is Whiteboard Friendly）——图数据库

> 对应官方页实抓目录（✅）：Day1 Graphs, Cypher, and CRUD｜Day2 REST, Indexes, and Algorithms｜Day3 Distributed High Availability｜Wrap-Up。
> **2e 的关键更新**：Neo4j 章从原初的 REST/Gremlin 口径迁到 **Cypher**（✅ 官方页作者访谈明确）。
> Neo4j 本机**无安装**（`where neo4j` 无果，⚠️ 不装不测）；Cypher/遍历/集群运行行为 ⚠️ 转述。🔧 类比用 DuckDB 1.5.5 递归 CTE 复现「多跳遍历（friends-of-friends）」的语义，**非 Neo4j 行为**。
> 纵深：[../Neo4j_The_Definitive_Guide/00-总览与阅读地图.md](../Neo4j_The_Definitive_Guide/00-总览与阅读地图.md)、图模型通论 [../Graph_Databases_2e/00-总览与阅读地图.md](../Graph_Databases_2e/00-总览与阅读地图.md)。

## 6.0 「白板友好」：属性图模型

Neo4j 的招牌论点是：当你习惯在白板上画**圆圈（节点）+ 带名字的箭头（关系）**，那就是图数据库的建模语言。属性图（Labeled Property Graph）要素：
- **节点（Node）**：带标签（Label）+ 属性（键值）。
- **关系（Relationship）**：有方向、有类型（type）、可带属性——**关系是一等公民**（这是与关系库「外键」的本质差异：外键只能指向，关系能被命名、带权、被遍历与查询）。
- **路径（Path）**：关系序列，多跳查询的对象。
- 核心赌注：**「关系即数据」**——把连接从「查询期临时 join」提升为「存储期一等结构」，让多跳遍历廉价。

## 6.1 Day 1：图、Cypher 与 CRUD

- **Cypher**：声明式图查询语言（ASCII 画图：`(a)-[:KNOWS]->(b)`）。CRUD：`CREATE/MERGE`（幂等 upsert）、`MATCH … WHERE … RETURN`、`SET/DELETE/REMOVE`。
- **模式匹配**：`MATCH (p:Person {city:'NY'})-[:FRIEND]->(f)` 用「图模式」代替 SQL 的多表 join。
- ⚠️ 转述：Day1 用 Neo4j Browser / Cypher 跑通建图、插关系、按模式查。

## 6.2 Day 2：REST、索引与算法

- **索引**：节点/关系属性的唯一索引与普通索引（早期 `schema:index` 演化为 `CREATE INDEX`）；Neo4j 是**索引自由邻接（index-free adjacency）**——沿关系指针走不需再查索引，故多跳快。
- **REST API**：早期 HTTP 端点（书仍讲，2e 重心已移 Cypher/Bolt）。**Bolt** 二进制协议是后继主线 ⚠️。
- **算法（Graph Algorithms）**：PageRank、连通分量、最短路径、社区发现（Louvain）等图算法内建，用于「跑一遍图得洞察」而非逐查询。
- ⚠️ 转述：Day2 强调「遍历 + 算法」双访问模式——点查走 Cypher，全局洞察走算法库。

> 🔧 **类比组 G：多跳遍历 friends-of-friends（非 Neo4j，DuckDB 1.5.5 递归 CTE）**
> Neo4j「沿关系走两跳」在 SQL 侧的对应物是**递归 CTE**。本机建无向边表 `f(a,b)`（1-2,2-3,3-4,1-5 双向），从节点 2 出发做深度=2 的邻居-of-邻居：
> ```sql
> WITH RECURSIVE p AS (
>   SELECT 2 AS node, 0 AS depth, [2] AS path
>   UNION ALL
>   SELECT CASE WHEN e.a=p.node THEN e.b ELSE e.a END, depth+1,
>          list_append(p.path, CASE WHEN e.a=p.node THEN e.b ELSE e.a END)
>   FROM p JOIN f e ON e.a=p.node OR e.b=p.node
>   WHERE depth<2 AND NOT list_contains(p.path, …))
> SELECT DISTINCT node, depth FROM p WHERE depth=2;
> ```
> 真实输出：`[(4,2),(5,2)]`（✅：2→3→4、2→1→5）。Cypher 里等价 `MATCH (n {id:2})-[:F*2]-(fof) RETURN fof`。声明：DuckDB 用递归 join 模拟遍历，**每次展开都是一层 join 扫描**，而 Neo4j 靠 index-free adjacency 直接指针跳转——这正是「关系即数据」为何让图库多跳更快的一手对照（同一题，SQL 把遍历写成自连接、逐跳扩大中间结果）。可回链 [../Graph_Databases_2e/00-总览与阅读地图.md](../Graph_Databases_2e/00-总览与阅读地图.md) 的遍历成本论述。

## 6.3 Day 3：分布式与高可用

- **因果一致副本 / Causal Consistency**：写后读己之写（session causality）；⚠️ 转述（书时代为 enterprise HA pair）。
- **集群（Neo4j Fabric /因果集群）**：跨实例分布读、分片联邦查询；企业版的多核心（multi-DB）与热备。
- ⚠️ 转述：Day3 的分布式细节 2e 已更新为 Cypher + Bolt 语境，但本机无法运行集群，全部转述。

## 6.4 Wrap-Up：Neo4j 适合什么、不适合什么

- **适合**：关系密集、多跳遍历、推荐/社交/欺诈网络/知识图谱、「查询里要问『A 到 B 是否有关系』」。
- **不适合**：大批量分析型聚合（→ 列存/湖仓）、简单 KV 点查（→ Redis）、规范化事务报表（→ PG）。
- ⚠️ 转述：作者把 Neo4j 作「唯一把连接当一等数据」的代表，专门用来打「用关系库做 5 表 join 查网络」的痛点。

## 6.5 本册内互链

- 图模型通论与遍历成本 → [../Graph_Databases_2e/00-总览与阅读地图.md](../Graph_Databases_2e/00-总览与阅读地图.md)；Cypher 纵深 → [../Neo4j_The_Definitive_Guide/00-总览与阅读地图.md](../Neo4j_The_Definitive_Guide/00-总览与阅读地图.md)。
- 与关系 join 的对照 → [02-PostgreSQL关系锚点.md](02-PostgreSQL关系锚点.md)（🔧 组 A）。

## 6.6 常见坑与设计要点（⚠️ 转述，Neo4j 通识）

- **超级节点（supernode）**：某节点关系数极高（如「关注了百万人」）会让遍历退化成扫关系——用关系属性分桶或降级为批量分析。
- **图不适合全量聚合**：`MATCH ()-[r]->() RETURN count(r)` 这类全图统计是 Neo4j 弱项，应交给批处理/列存。
- **MERGE 幂等要先建索引**：在没索引的属性上 `MERGE` 会全扫且可能重复建，标准做法「先 `CREATE CONSTRAINT`/索引，再 MERGE」。
- **变长路径炸裂**：`-[:REL*1..10]-` 指数级展开，需用最大深度、`DISTINCT`、或算法库替代。
- **ACID 但单机优先**：社区版是单写主，「写扩展」要靠企业因果集群/读写分离——2e Day3 的重点即在此 ⚠️。

## 6.7 Wrap-Up 练习重构（✅ 体例 + ⚠️ 题面转述）

1. 用 `(Person)-[:KNOWS]->(Person)` 建一张 6 人社交图，查「A 的二度好友中未被 A 直接认识的」（friends-of-friends 去重）。
2. 用本机 🔧 组 G（DuckDB 递归 CTE）复现同一二度查询，比较「指针遍历」与「逐层 join」的心智差。
3. **跨库题**：把 Neo4j 的多跳结果**物化回 PostgreSQL**（[02](02-PostgreSQL关系锚点.md)）做报表，体会「图算关系、关系存结果」的分工。
4. 思辨题：知识图谱场景为何不用「Postgres 里建一张边表」？（答案：多跳时 join 链成本 vs 邻接指针 O(1)）

## 6.8 Cypher 小抄（⚠️ 书体例反推 + ✅ 手册常识；手册 URL 实测 200）

| 目的 | Cypher | SQL / 本册对照 |
| --- | --- | --- |
| 建节点关系 | `CREATE (a)-[:R]->(b)` | `INSERT`（但关系即结构） |
| 幂等 upsert | `MERGE (n:Label {k:v})` | `INSERT … ON CONFLICT` |
| 一跳模式 | `MATCH (a)-[:R]->(b)` | 单次 `JOIN` |
| 多跳 | `MATCH (a)-[:R*1..3]->(x)` | 递归 CTE（🔧 组 G） |
| 过滤返回 | `WHERE … RETURN … ORDER BY` | `WHERE/SELECT/ORDER BY` |
| 建索引 | `CREATE INDEX FOR (n:L) ON (n.p)` | `CREATE INDEX` |

## 6.9 图建模法则（⚠️ 转述，Neo4j 通识）

1. **关系要「有名字、有方向、可带属性」**：把动词（`PURCHASED`、`MANAGES`、`SIMILAR_TO`）建成类型化关系，而不是节点上的外键列——这是「关系一等公民」的落地。
2. **标签做分类、属性做过滤、关系做遍历**：能用关系表达的「连接」别塞进属性数组（那样又退回文档模型的多跳代价，见 [04](04-MongoDB文档模型.md)）。
3. **约束/索引先行**：`CREATE CONSTRAINT ON (n:Label) ASSERT n.id IS UNIQUE` 既保唯一又给 `MERGE` 加速——没索引的图写入和匹配都会退化。
4. **遍历与聚合分工**：多跳点查/路径交给 Cypher 遍历，「全图统计/推荐打分」交给 GDS 算法库批量跑（6.2）。

> 何时**不该**用图（⚠️）：数据其实是规范的实体-关系表且查询多为聚合报表 → PostgreSQL（[02](02-PostgreSQL关系锚点.md)）；连接关系少而浅（一两跳）→ 文档内嵌引用（[04](04-MongoDB文档模型.md)）就够。Neo4j 的甜点是「**深度/不确定跳数的关系遍历**」与「关系本身要被查询」。纵深见 [../Neo4j_The_Definitive_Guide/00-总览与阅读地图.md](../Neo4j_The_Definitive_Guide/00-总览与阅读地图.md)、[../Graph_Databases_2e/00-总览与阅读地图.md](../Graph_Databases_2e/00-总览与阅读地图.md)。

## 核心概念速览（中英对照）

- **属性图 / LPG** — labeled property graph：节点+带类型关系+属性。
- **关系一等公民** — first-class relationship：可命名/带向/带属性/被遍历。
- **Cypher** — 声明式图查询语言，ASCII 图模式。
- **模式匹配** — pattern matching：`(a)-[r]->(b)` 代替多表 join。
- **MERGE** — 幂等 upsert（存在即匹配，否则创建）。
- **索引自由邻接** — index-free adjacency：沿关系指针 O(1) 跳转，多跳快的根因。
- **遍历** — traversal：沿路径扩展，与「批量聚合」相对。
- **图算法** — graph algorithms：PageRank/连通分量/最短路径/社区发现。
- **GDS 库** — Graph Data Science：企业级算法库，取代早期内建算法命名 ⚠️。
- **Bolt** — 二进制驱动协议（替代早期 REST 主线）。
- **因果一致** — causal consistency：会话内读己之写。
- **Fabric / 因果集群** — 分布式读与高可用机制 ⚠️。
- **超级节点** — supernode：关系数畸高的节点，遍历退化的根源。
- **GraphRAG** — 知识图谱 + 检索增强生成，图库 2024–2026 回潮风口 ⚠️。

## 最新演进与工业实践

- **Cypher 标准化为 GQL**：ISO/IEC 39012 **GQL**（图查询语言国际标准，2024 发布）以 Cypher 为主要蓝本；`gqlstandard.org` 本轮不可达（000），故只给标准名+年份 ⚠️，不冒 URL/DOI。Neo4j 手册 https://neo4j.com/docs/cypher-manual/current/ ✅ 实测 200。
- **版本与命名**：Neo4j 5.x 长期基线，官方引入**日历式版本（2025.x）**，并强化向量索引（`CREATE VECTOR INDEX`）与 LLM/知识图谱集成；发布说明 https://neo4j.com/release-notes/ ✅ 200。
- **GraphRAG 风口**：2024–2026 图数据库因「知识图谱 + 检索增强生成」回潮，Neo4j 把向量索引与 Cypher 合体，直接连本册未含的向量 genre——对照 [../Vector_Databases/00-总览与阅读地图.md](../Vector_Databases/00-总览与阅读地图.md)。
- **算法库迭代**：GDS（Graph Data Science）库取代早期内建算法命名，PageRank/Louvain/Node2Vec 等持续演进 ⚠️。
- **理论/纵深**：遍历与邻接索引的成本模型详见 [../Graph_Databases_2e/00-总览与阅读地图.md](../Graph_Databases_2e/00-总览与阅读地图.md)；NoSQL 全景定位见 [../nosql精粹.md](../nosql精粹.md)。
- **取证口径**：目录/2e 迁 Cypher ✅ 官方页实抓；集群/Bolt/GDS 运行 ⚠️ 转述；🔧 组 G = DuckDB 1.5.5 递归 CTE 一手数字且非 Neo4j 行为。
- **本册定位提醒**：Neo4j 是七库里唯一「把连接当数据」的一章，读完应能立刻识别「这题该不该上图」——判据是**跳数是否深/是否不确定**，深且不确定→图，浅且固定→文档引用或关系 join（见 6.9）。
