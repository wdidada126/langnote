# 02 PostgreSQL（That's Post-gre-S-Q-L）——关系锚点

> 对应官方页实抓目录（✅）：Day1 Relations, CRUD, and Joins｜Day2 Advanced Queries, Code, and Rules｜Day3 Full Text and Multidimensions｜Wrap-Up。
> 结构 ✅；PG **具体安装/运行行为本机不可测**（`where psql` 无果，⚠️ 不装不跑）。🔧 类比用本机 DuckDB 1.5.5 / SQLite 3.45.3，**均非 PostgreSQL 行为**，只复现关系语义。
> 纵深让位：[../PostgreSQL_16_Administration_Cookbook/00-总览与阅读地图.md](../PostgreSQL_16_Administration_Cookbook/00-总览与阅读地图.md)、[../PostgreSQL_10_High_Performance_3e/00-总览与阅读地图.md](../PostgreSQL_10_High_Performance_3e/00-总览与阅读地图.md)。

## 2.0 为什么第一库是关系型

PostgreSQL 在书里不是「NoSQL 之一」，而是**对照原点**：它是唯一被完整覆盖 SQL/ACID/规范化的一章，之后每个 NoSQL 都拿它当「我为什么不同」的参照。作者选 PG 而非 MySQL，看重它把「文档（JSONB）、全文、地理、数组」等 NoSQL 特性吸收进单一引擎的能力（2e 更新重点之一）。

## 2.1 Day 1：关系、CRUD 与连接

- **关系模型最小件**：表=元组集合、主键唯一标识行、外键引用他表、约束（NOT NULL/CHECK/UNIQUE）声明式强制。
- **CRUD**：`INSERT / SELECT / UPDATE / DELETE`；`RETURNING` 子句是 PG 特色（写后立即读回）。
- **连接（Joins）**：INNER/LEFT/RIGHT/FULL + CROSS，关系代数的「theta join / natural join」工程化。
- ⚠️ 转述（书基线 PG 9.x/10 时代）：Day1 用 `psql` 交互 + 一个样例库跑通建表/插数/连接。
- **纵深对照**：连接/索引的正规复杂度账本见 [../数据库系统概念6/11-索引与散列.md](../数据库系统概念6/11-索引与散列.md)；B 树访问路径、散列连接概念同源。

> 🔧 **类比组 A：join + 分组 + 窗口（非 PostgreSQL，DuckDB 1.5.5）**
> 本机建 `dept(id,name)` 3 行、`emp(id,dept_id,salary)` 6 行，跑：
> ```sql
> SELECT d.name, COUNT(*) n, SUM(salary) tot,
>        RANK() OVER (ORDER BY AVG(salary) DESC) rk
> FROM emp e JOIN dept d ON e.dept_id=d.id GROUP BY d.name ORDER BY tot DESC;
> ```
> 真实输出：`[('eng',3,360,1), ('sales',2,150,2), ('hr',1,60,3)]`（✅ 数字，方法见上）。要点：连接把「跨表关系」在查询期兑现——这正是文档/宽列模型刻意回避、Neo4j 用「边」替代的东西。PG 的窗口函数 `RANK() OVER` 在 DuckDB 同构，说明关系代数这套表达力是跨引擎通用语言。

## 2.2 Day 2：高级查询、代码与规则

- **子查询 / CTE / 集合操作**：`WITH`（可递归 `RECURSIVE`）、`UNION/INTERSECT/EXCEPT`、相关子查询。
- **视图与物化视图**：`CREATE VIEW`（查询宏）vs `CREATE MATERIALIZED VIEW`（结果落盘、需 `REFRESH`）。
- **窗口函数进阶**：`ROW_NUMBER/RANK/DENSE_RANK`、`LAG/LEAD`、`OVER (PARTITION BY …)`——报表聚合利器。
- **代码（Code）**：PL/pgSQL 存储过程/函数、触发器（trigger）、`DO` 匿名块；把逻辑下推到数据所在处。
- **规则（Rules）**：约束系统（外键级联 `ON DELETE CASCADE`、`CHECK`、排他约束、`RULE`/`INSTEAD OF` 触发器）。
- ⚠️ 转述：书在此 Day 强调 PG「可编程」，是它区别于纯 KV/文档库的核心竞争力之一。

## 2.3 Day 3：全文检索与多维数据

- **全文（Full Text）**：`tsvector`（规范化词位向量）+ `tsquery`（查询）+ `to_tsvector()` + `GIN` 索引 + 排序 `ts_rank`。相比 `LIKE '%kw%'` 全扫，走倒排索引。
- **多维（Multidimensions）**：数组列 `int[]`、范围类型 `daterange`、`ltree`（层级）、`hstore`/`jsonb`（键值/文档内嵌）、`crosstab`（`tablefunc` 扩展做行转列）、`pgcrypto`/地理等扩展生态。
- **JSONB**：把 PG 变成「关系 + 文档」混合体——GIN 索引 JSONB 路径，`@>` 包含查询；这是 2e 特意更新的「PG 吸收 NoSQL」证据。
- ⚠️ 转述（书基线）：Day3 演示用 PG 同时做全文与文档，论证「很多 NoSQL 场景不必换库」。

> 🔧 **类比组 B：全文检索（非 PostgreSQL，SQLite 3.45.3 的 FTS5）**
> PG 的 `tsvector/tsquery` 在 SQLite 侧的对应物是 **FTS5 虚拟表** + `MATCH` + `snippet()`。本机：
> ```sql
> CREATE VIRTUAL TABLE docs USING fts5(body);
> INSERT INTO docs VALUES('relational database joins and indexes'),
>   ('nosql document store nested arrays'),('graph traversal cypher nodes edges'),
>   ('column family wide column store');
> SELECT rowid, snippet(docs,0,'<b>','</b>','...',8) FROM docs
>   WHERE docs MATCH 'database OR graph';
> ```
> 真实输出：`rowid 1 → "relational <b>database</b> joins and indexes"`、`rowid 3 → "<b>graph</b> traversal cypher nodes edges"`（✅ 命中布尔 OR + 高亮）。语义等价 PG 全文：倒排索引 + 词匹配 + 结果摘要；差异（相关词、词干、权重）留 PG 专册。

> 🔧 **类比组 C：多维聚合 CUBE（非 PostgreSQL，DuckDB GROUP BY CUBE）**
> PG 用 `GROUPING SETS/CUBE/ROLLUP` 或 `crosstab` 做多维汇总。本机 `sales(reg,prd,amt)` 4 行跑 `GROUP BY CUBE(reg,prd)`，得 **9 组**（明细 4 + 按 reg 2 + 按 prd 2 + 总计 1）：`('east','a',10)…(None,None,65)` 总计行 ✅。说明「多维 = 一次查询产出多个粒度聚合」，是 PG 相对简单 KV/文档库的报表优势。

## 2.4 Wrap-Up：PG 适合什么、不适合什么

- **适合**：强一致事务、复杂 ad-hoc 查询与 join、需要约束/完整性、中小到中大规模（读写可垂直扩 + 复制 + 分区）、以及「一个库既要关系又要 JSON/全文/地理」的混合诉求。
- **不适合（书语境）**：需极简单点查超高吞吐（KV/Redis 更快）、需海量写线性水平扩展（宽列更省心）、需多跳遍历一等公民（图更自然）。
- ⚠️ 转述：作者结论——PG 常是「先试它」的默认选项，NoSQL 是它成为瓶颈后的定向逃逸。

## 2.5 本册内互链

- 文档嵌套对照 → [04-MongoDB文档模型.md](04-MongoDB文档模型.md)（PG JSONB vs Mongo BSON）。
- 键值/缓存配对 → [08-Redis数据结构服务器.md](08-Redis数据结构服务器.md)（Redis 作 PG 读缓存的经典组合）。
- 全文检索的独立纵深 → [../Elasticsearch_The_Definitive_Guide/00-总览与阅读地图.md](../Elasticsearch_The_Definitive_Guide/00-总览与阅读地图.md)（书未含 ES，但 PG FTS 常与 ES 对照）。

## 2.6 常见坑与设计要点（⚠️ 转述，书 + PG 通识）

- **N+1 查询**：应用层循环里逐行发 SQL——关系库最经典的性能陷阱，正解是批量 `WHERE id IN (…)` 或 join 一把取。
- **索引不是免费的**：每个索引都拖慢写、占空间；`ANALYZE`/`EXPLAIN` 决定用不用索引——见 [../数据库系统概念6/11-索引与散列.md](../数据库系统概念6/11-索引与散列.md)。
- **`LIKE '%x%'` 不走 B 树**：前后通配导致全扫，该上全文（tsvector/GIN，见 2.3）而非 `LIKE`。
- **ORM 屏蔽了连接威力**：过度对象化反而把 join 拆回 N 次往返——读「关系即集合」再决定何时用 ORM。
- **物化视图刷新窗口**：MV 不是实时，`REFRESH` 期间读到旧值——把它当「预计算缓存」而非「镜像表」。

## 2.7 Wrap-Up 练习重构（✅ 体例 + ⚠️ 题面转述）

书每章末尾留练习，本册据 Day1/2/3 重构 PG 章练习方向（非原题逐字）：
1. 把一张宽表**规范化**到 3NF，再反过来用 JSONB **反规范化**同一数据，比较两种模型的读写取舍。
2. 用 `tsvector + GIN` 给一段文章建全文索引，量出 `LIKE` vs 全文的命中差异（🔧 思路可迁移到本机 FTS5，见 2.3）。
3. **跨库题**：拿 Redis（[08](08-Redis数据结构服务器.md)）给一条昂贵的 PG 聚合查询做 TTL 缓存，体会「PG 真相 + Redis 加速」组合。
4. 思辨题：本节的 CUBE 多维聚合，为什么文档库/键值库做不到同等表达力？（答案指向「关系代数 + 声明式聚合」）

## 2.8 PG 命令/子句小抄（⚠️ 书体例反推 + ✅ PG 文档常识）

| 目的 | 关系库写法（PG） | 其它库的对应（本册） |
| --- | --- | --- |
| 建表 + 约束 | `CREATE TABLE … (id PK, fk REFERENCES …, CHECK …)` | Mongo 无强制 schema；Dynamo 只有 PK/SK |
| 取回并回读 | `INSERT … RETURNING id` | Neo4j `CREATE` 返回节点 |
| 跨表取数 | `A JOIN B ON A.k=B.k` | Neo4j 用 `(a)-[:R]->(b)` 替代 join |
| 分组聚合 | `GROUP BY … HAVING …` | Mongo `$group`；CouchDB map/reduce |
| 排名/累计 | `RANK()/SUM() OVER (PARTITION BY …)` | Redis zset `ZREVRANK`（结构即语义） |
| 全文 | `to_tsvector` + `@@ tsquery` + GIN | SQLite FTS5（🔧 组 B）；ES（专册） |
| 多维 | `GROUP BY CUBE(a,b)` | DuckDB 同构（🔧 组 C） |
| 预计算 | `CREATE MATERIALIZED VIEW … REFRESH` | CouchDB 视图（🔧 组：物化表） |

> 这张小抄的用途：**当你从 PG 转读任何一个 NoSQL 章时，用右列把新语法「翻译」回你熟的关系概念**——这正是本书「以 PG 为锚」的实操方法。关系库不是七库之一，而是理解其余六库的**坐标系**。

## 核心概念速览（中英对照）

- **关系** — relation：元组集合 + 属性，PG 的第一类数据结构。
- **主键 / 外键** — primary key / foreign key：行唯一标识与跨表引用完整性。
- **连接** — join：查询期兑现跨表关系，关系代数核心。
- **CTE / 递归查询** — common table expression (WITH)：命名子查询，`RECURSIVE` 支持层级。
- **物化视图** — materialized view：结果落盘、需刷新的预计算查询。
- **窗口函数** — window function：`OVER(PARTITION BY …)` 不折叠行的排名/累计。
- **PL/pgSQL / 触发器** — stored procedure / trigger：把逻辑下推到数据库侧。
- **约束 / 规则** — constraint / rule：声明式完整性（CHECK/CASCADE/RULE）。
- **全文检索** — full-text search (tsvector/tsquery)：倒排 + 词位 + 排序，替代 LIKE 全扫。
- **JSONB** — binary JSON：PG 内的文档能力，可 GIN 索引、`@>` 查询。
- **CUBE / GROUPING SETS** — 多维聚合：一次查询产出多个粒度汇总。
- **GIN 索引** — generalized inverted index：服务数组/JSON/全文的倒排访问路径。

## 最新演进与工业实践

- **大版本（✅ 官方页实抓）**：PG **17**（2024-09，`postgresql.org/about/news/postgresql-17-released-2957/` 实测 200）；PG **18**（`.../postgresql-18-released-3171/` 实测 200，页脚显示最新补丁「18.1 …13.23，2025-11-13」并预告 PG19 Beta）。2018 书基线（≈PG 9.x/10）到 2026 已跨 8 个大版本。
- **18 代际要点（⚠️ 转述自官方发布页口径）**：异步 I/O 顺序扫描、`VACUUM` 改进、虚拟生成列、`NOT NULL` 约束免全表扫描入目录、乐观锁 `FOR KEY SHARE` 增强——都是把 NoSQL 抢走的「扩展性/易用」往回补。
- **JSON/文档线**：SQL:2016 的 JSON 表函数（`JSON_TABLE`）与 JSON 聚合标准化，PG 与 Oracle/MySQL/DB2 趋同——本册「PG 吸收文档」趋势到 2026 更明显。
- **pgvector 生态**：向量检索以扩展 `pgvector` 进入 PG，把「关系 + ANN」合体；纵深见 [../Vector_Databases/00-总览与阅读地图.md](../Vector_Databases/00-总览与阅读地图.md)——书未触及，是 2018→2026 最大空白补位。
- **运维纵深**：分区、逻辑复制、并行查询、连接池（PgBouncer）等生产议题，转 [../PostgreSQL_16_Administration_Cookbook/00-总览与阅读地图.md](../PostgreSQL_16_Administration_Cookbook/00-总览与阅读地图.md) 与 [../PostgreSQL_10_High_Performance_3e/00-总览与阅读地图.md](../PostgreSQL_10_High_Performance_3e/00-总览与阅读地图.md)。
- **方法互证**：本册 🔧 用 DuckDB/SQLite 复现 PG 关系语义的路线，与 [../DuckDB_in_Action/00-总览与阅读地图.md](../DuckDB_in_Action/00-总览与阅读地图.md)、[../Using_SQLite/00-总览与阅读地图.md](../Using_SQLite/00-总览与阅读地图.md) 的「不装重型引擎拿一手直觉」同源。
