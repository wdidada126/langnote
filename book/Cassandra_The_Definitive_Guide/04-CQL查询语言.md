# 04 CQL 查询语言（原书第 4 章域 ⚠️ 推定重构）

> 精读重构（非原书文本）。CQL 语法按 2.x 时代口径转述，⚠️ 未实测；3.11/5.0 官方 CQL 参考为
> 校验基线。同题管理员向版本：#89 册 06-CQL入门.md（互链见文末）。

## 4.1 题纲

1. CQL 的自我定位：SQL 外观 + 分区语义内核（"学习曲线在 PRIMARY KEY 定义那一刻"）
2. DDL：CREATE/ALTER TABLE、`WITH`/`AND` 表属性、索引与视图对象
3. DML 四件套：INSERT/UPDATE/DELETE 在 Cassandra 里的同构真相（都是写分区变更）
4. SELECT 的约束世界：ALLOW FILTERING 的屈辱、IN 的分区局部性、范围谓词的聚簇序依赖
5. 批量语句 BATCH：为"单分区原子性"服务，不是性能工具（书中最常被误读的一段）
6. 聚合与计数：COUNT 的扫描本质、DISTINCT 限制（2.2 前夜）、无 JOIN/无子查询/无窗口
7. 分页与游标：`LIMIT` + token 分页（驱动侧）⚠️；cqlsh 的自动 fetch-size
8. 函数与转换族：dateOf/now/uuid/toTimestamp（2.1+ ⚠️）等纯 CQL 工具

## 4.2 INSERT≠存在性检查，UPDATE≠读改写

2.x 语境最颠覆直觉的一组等价：

```sql
INSERT INTO users (id, name) VALUES (uuid(), 'a');
UPDATE users SET name='a' WHERE id=...;
-- 在 Cassandra（2.x）里这两句几乎同义：都生成列的时间戳写入，
-- INSERT 不做"主键是否存在"检查（除非 IF NOT EXISTS=LWT，08 章）。
-- 于是：
--   * 主键不存在的 UPDATE = 静默创建一行（部分列存在即可"复活"幽灵行）⚠️
--   * 反复 INSERT 同一主键 = 覆盖，而不是报错
--   * DELETE 一行=给每列立墓碑；DELETE 分区键=墓碑雨（11 章性能账）
```

这组语义的源头是 LSM 的"写只是追加"（06 章）：CQL 选择忠实暴露存储本质而非模拟关系幻象。
读 CQL 代码的正确心态：每个写语句=对分区的一次时间戳化修改指令。

## 4.3 SELECT 约束：为什么 WHERE 要"从分区键开头"

CQL 查询分类（书中口径 ⚠️）：

- **Partition key 等值 + clustering 前缀范围**：最优路径，单分区内有序读。
- **等值分区键 + 等值聚簇**：单行，最便宜。
- **无分区键**：要么走二级索引（2i：全节点广播每个分区的本地探测，05 章判词），
  要么 `ALLOW FILTERING`（在协议层做"全表扫+客户端过滤"，只许交互式/小表）。

```sql
SELECT * FROM rides WHERE city='sf' AND year=2015 AND date > '2015-05-01'; -- 好
SELECT * FROM rides WHERE fare > 50 ALLOW FILTERING;   -- 交互式自杀，生产禁用 ⚠️
SELECT * FROM rides WHERE city IN ('sf','la') AND year=2015;  -- IN 仅限分区键前缀(2.x 后期放开部分) ⚠️
SELECT COUNT(*) FROM rides WHERE city='sf';  -- 扫该 city 全部分区，非 O(1)
```

限制清单（2.x ⚠️）：无 JOIN、无 GROUP BY（聚合语义缺失，仅 2.2 试验 DISTINCT ⚠️）、
无子查询、ORDER BY 只认聚簇序方向、LIKE 仅 2i 文本索引的 limited 支持。这些"缺失"不是
功能没做完，而是**分区模型的诚实**：跨分区聚合的代价不该藏在语法糖里——需要聚合时
答案在 12 章的 Spark/OLAP 侧。

## 4.4 BATCH 的正误用法

```sql
BEGIN BATCH
  INSERT INTO trips_by_city (city, id, ...) VALUES ('sf', ...);   -- 同分区 ✓
  INSERT INTO trips_by_date (date, id, ...) VALUES ('2015-05-01', ...); -- 另一分区但同分区内原子 ✓
  UPDATE summary SET n=n+1 WHERE city='sf';                       -- 第三个分区 ✗ 代价陡增
APPLY BATCH;
```

书中结论（⚠️ 转述）：BATCH 提供的是**单分区原子**（logged batch 跨分区靠 2PC，协调节点
故障可滞留，代价=写延迟翻倍起步）；默认 LOGGED，2.1 起 UNLOGGED/COUNTER 型 ⚠️。
"用 BATCH 提速"是最贵反模式——异步驱动的单行并发写永远更快。这条判词与
[../设计数据密集型应用/07-事务.md](../设计数据密集型应用/07-事务.md) 的"跨分区事务代价"通论互证。

## 4.5 DDL 与对象模型语句

- `CREATE INDEX IF NOT EXISTS ON rides(fare)`：2i 语法（模型限制见 05 章）；索引名不可选 ⚠️。
- `CREATE MATERIALIZED VIEW ... AS SELECT ... PRIMARY KEY ...`：2.1 实验 ⚠️——视图是**另一份
  复制的分区布局**，更新代价与修复牵连在演进节有当代判词。
- `ALTER TABLE ... WITH compaction = {'class':'TimeWindowCompactionStrategy', ...}`：表属性
  即运维参数（10 章挂点）；`bloom_filter_fp_chance`、`dclocal_read_repair_chance`（2.x 参数名 ⚠️，
  3.x 改名 `read_repair_chance` 族——升级迁移必踩的键名海沟）。
- `USE keyspace`、`DESCRIBE SCHEMA FULL`：cqlsh 导航。

## 4.6 与 SQL 的经验互译（系列读者向）

- 给 MySQL/PG 背景读者的桥：把 `PRIMARY KEY ((a), b, c)` 读作"按 a 哈希分片、片内按 b,c
  聚簇的索引组织表"；把"没有 UPDATE FROM ... WHERE 非键列"读作"分库分表中间件的硬约束"。
  本系列里分库分表的同一堵墙在 [../mysql/00-总览与阅读地图.md](../mysql/00-总览与阅读地图.md)
  的 `mysql/` 目录版语境出现过（✅ 盘上已验）。
- 反向提醒：SQL 里"加索引救慢查询"的直觉在这里=2i，但 2i 救的是**写放大和延迟**之外的东西，
  不救"跨分区大结果集"。

## 4.7 本章在全目录中的挂点

- 查询背后的物理路径 → [06-存储引擎与SSTable](06-存储引擎与SSTable.md)、
  [08-一致性与读写路径](08-一致性与读写路径.md)
- 建模决策如何决定语法自由度 → [05-数据建模](05-数据建模.md)
- 同题纵深 → [../Expert_Apache_Cassandra_Administration/06-CQL入门.md](../Expert_Apache_Cassandra_Administration/06-CQL入门.md)

## 核心概念速览（中英对照）

- **CQL** — Cassandra Query Language：SQL 外观的分区键约束语言，2.x 起唯一主接口。
- **分区键限定查询** — Partition-key-restricted query：性能合格的 WHERE 的最低门槛。
- **ALLOW FILTERING** — Allow filtering：显式签署"接受全扫+客户端过滤"的逃生阀。
- **Clustering 范围谓词** — Clustering range：聚簇列上的 >/>= 前缀连续范围才有序高效。
- **Logged batch** — Logged batch：跨分区 2PC 原子批，协调失败留悬挂日志。
- **Unlogged batch** — Unlogged batch：2.1+ 的无协调批，单分区原子性能友好 ⚠️。
- **IF NOT EXISTS / IF** — Conditional clause：LWT 入口，Paxos 代价（08 章）。
- **Secondary index** — 2i：全节点分区本地索引的广播查询形态。
- **Materialized view** — MV：复制式反范式分区，2.1 实验性 ⚠️。
- **fetch size / paging** — Paging：驱动侧 token 游标分页，cqlsh 自动续页。
- **WRITETIME/TTL 探针** — Introspection functions：查询列时间戳与剩余存活。
- **表属性 WITH/AND** — Table options：压实/缓存/复制/compaction 窗口的声明式旋钮。
- **token** — Token：分区键的哈希落点，`token()` 函数暴露环位置供范围查询。

## 最新演进与工业实践

（除注明 ✅ 外均 ⚠️ 转述；URL 均本会话实抓 ✅）

- **语法演进**：3.x/4.x 起支持非冻结集合元素级 DML、`WHERE IN` 对聚簇列/索引列的放宽、
  2.2→5.0 函数族扩容（json/text/time 转换、数学函数 5.0 新列，见
  https://cassandra.apache.org/doc/latest/cassandra/new/index.html 的 "New Mathematical CQL functions" 行）。
- **MV/2i 的当代判词**：4.0 起 SASI 默认禁用、**SAI 成为索引正道**（CEP-7
  https://cwiki.apache.org/confluence/display/CASSANDRA/CEP-7%3A+Storage+Attached+Index ，链接取自官方页
  正文 ✅）；MV 因修复/流式牵连在生产口碑仍谨慎 ⚠️，社区倾向"双写+外置反范式"。
- **LWT 补强**：4.x 起 LWT 写路径改进（Paxos 状态虚表化）⚠️；**6.0 Accord 将把"条件写"升级为
  可串行化事务**（https://cassandra.apache.org/doc/6.0/cassandra/new/index.html 的 ACID 行，预发布 ⚠️）。
- **聚合缺口的外部解**：GROUP BY/聚合下推交给物化路径——Spark connector 做 OLAP、
  CDC+流做实时聚合；与 [../bigdata/04-SparkSQL与结构化数据.md](../bigdata/04-SparkSQL与结构化数据.md)
  的用法衔接（盘上兄弟册）。
- **ALLOW FILTERING 现状**：官方文档仍保留该语法且警示语义不变；guardrails（4.x/5.0 "More
  guardrails" 行 ✅）可集群级封禁大分区/低效查询，把书中"口头纪律"变成可执行护栏。
