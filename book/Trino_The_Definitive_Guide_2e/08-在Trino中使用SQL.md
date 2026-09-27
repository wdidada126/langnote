# 第 8 章 在Trino中使用SQL（Using SQL with Trino ⚠️ 英题推定）

> 对应原书第二部分第 8 章。二级节标题 ✅ 实抓自 [oreilly.com.cn 官方页](http://www.oreilly.com.cn/index.php?func=book&isbn=978-7-111-73160-3)。SQL 为教学示意。

## 本章地图

| 节 | 内容 | 一句话结论 |
| --- | --- | --- |
| 8.1 Trino语句 | 语句总览：SHOW/DESCRIBE/EXPLAIN + DDL + DML 全家福 | 手册式章节，抓住「SHOW→DESCRIBE→SELECT」动线 |
| 8.2 Trino系统表 | `system.runtime.*`/`system.metadata.*`：引擎内省 | 监控与排错的 SQL 入口（12 章复用） |
| 8.3 catalog | CREATE/DROP/SHOW CATALOGS 与 connector 绑定 | catalog 生命周期 ≈ 配置文件生命周期 |
| 8.4 schema | CREATE/DROP SCHEMA 映射对端命名空间 | 能否建 schema 取决于 connector |
| 8.5 information schema | SQL 标准元数据视图 | 跨源元数据的「最小公分母」 |
| 8.6 表 | CREATE/DROP/ALTER/**CTAS**/INSERT | DDL 能力 = connector 能力（06 章呼应） |
| 8.7 视图 | CREATE VIEW：保存的查询，非物化 | 与 MV 的区别一表讲清 |
| 8.8 会话信息和配置 | SHOW/SET SESSION、事务提示 | 会话是调优的第一接触面 |
| 8.9 数据类型 | 标量+复合（ARRAY/MAP/ROW）+半结构化（JSON 线 ⚠️ 392 无原生 JSON 类型） | 复合类型是 Trino SQL 表达力高地 |
| 8.10 SELECT语句基础 | FROM/WHERE/投影/别名 | — |
| 8.11 WHERE子句 | 谓词与 Sargable 形态影响下推 | 写法决定性能（4.6 兑现处） |
| 8.12 GROUP BY和HAVING子句 | 聚合 + grouping sets 预告 | 部分聚合/下推行为看 04 章 |
| 8.13 ORDER BY子句和LIMIT子句 | TopN 与分页 | 全局排序是单点合并，慎大 |
| 8.14 JOIN语句 | INNER/LEFT/RIGHT/FULL/CROSS + USING/ON | join 顺序靠 CBO 与统计（4.8） |
| 8.15 UNION、INTERSECT和EXCEPT子句 | 集合三兄弟（ALL/DISTINCT） | 与 UNION 混写注意优先级 |
| 8.16 分组操作 | CUBE/ROLLUP/GROUPING SETS | OLAP 立方体的 SQL 化（配数仓书） |
| 8.17 WITH子句 | CTE：可读性 + 物化语义提醒 | CTE 默认不物化，重复引用重复算 |
| 8.18 子查询 | 标量/IN/EXISTS 与去关联 | 去关联失败 = 嵌套循环灾难 |
| 8.19 从表中删除数据 | DELETE/TRUNCATE/DROP 与 connector 支持度 | 「湖上的删除」是表格式特权（06 章） |
| 8.20 小结 | — | 方言熟了就进 09 章函数宇宙 |

## 核心精讲

### 1. 内省三件套与系统表（8.1/8.2）

```sql
-- 教学示意：先看看这个引擎能告诉我什么
SHOW CATALOGS; SHOW SCHEMAS FROM hive; SHOW TABLES FROM tpch.tiny;
DESCRIBE lineitem;
-- 系统表：运行时与元数据两族
SELECT query, state, elapsed_time FROM system.runtime.queries;  -- 现名/列以 483 为准 ⚠️
SELECT * FROM system.metadata.catalogs;
SELECT * FROM system.runtime.nodes;
```

系统表是「引擎自观」的 API：Web UI（3.5）与 JMX connector（6.7）之外的第三条内省通道，12 章排障剧本全靠它。

### 2. 类型系统（8.9）：与周边方言的三处高频差异

| 差异点 | Trino | 参照系 |
| --- | --- | --- |
| 字符串 | `VARCHAR(n)` 可无 n；无 CHAR 语义包袱 | MySQL/Pg 对比 ⚠️ |
| 整型 | 无 INT32 默认（INTEGER/VARCHAR 转换严格） | Hive BIGINT 惯性 |
| 时间 | `TIMESTAMP(p)` 带精度/`WITH time zone` | 湖上时区坑第一来源 |
| 复合 | ARRAY/MAP/ROW 一等公民，配 09 章解嵌套 | 与 PG 数组/JSONB 气质不同 |
| JSON | 392 书稿无原生 JSON 类型（json 函数 + VARCHAR）；483 已引入 JSON 数据类型（✅ 近版演进，具体引入版本 ⚠️ 未逐版核） | 半结构化路线与表格式书对照 |

### 3. 查询写作即性能（8.10–8.18 的性能面）

- **WHERE 可下推形态**：`col = const`、`col IN (...)`、`col BETWEEN` 是 sargable；把列包进函数（`date_trunc('day',ts)=...`）当场摧毁下推与分区裁剪（Hive/Iceberg 的分区谓词同理，06 章）。
- **JOIN**：写 `ON` 等值、过滤放对位置（LEFT JOIN 的右表条件进 ON 还是 WHERE，结果不同）；大表 join 前先 `EXPLAIN (TYPE DISTRIBUTED)` 看分发（4.7）。
- **ORDER BY + LIMIT**：触发 TopN 下推/合并优化；无 LIMIT 的全排序把终 stage 压到单点。
- **CTE（WITH）**：Trino 默认把 CTE **内联展开**（可重复引用≠物化一次），需要物化就 CTAS 或 MV（06 章）；此语义与 PostgreSQL（物化 CTE）相反，跨库老手最常翻车处。
- **去关联**：`WHERE EXISTS (SELECT ... WHERE ...)` 会被解关联成半连接；子查询出现 `LIMIT` 等阻止解关联的形态时退化为相关执行（⚠️ 版本相关，以 EXPLAIN 为准）。

### 4. 视图与物化视图的边界（8.7 vs 06 章）

`CREATE VIEW` = 命名查询（每次现算）；`CREATE MATERIALIZED VIEW` = 预计算存储 + 定时 REFRESH + 优化器改写命中（06 章 §1 的机制）。判断公式：**重复聚合且能容忍刷新窗口 → MV；只是逻辑复用/权限裁剪 → VIEW**。

### 5. 删除的三种重量（8.19）

`DROP TABLE`（结构+数据，connector 权限内）、`TRUNCATE`（保结构清空，支持面窄）、`DELETE FROM ... WHERE`（行级，Iceberg/Delta 类 v2 格式才优雅，Hive 表在 392 时点受 ACID 表限制 ⚠️ 书稿口径；483 的 MERGE/DELETE 语义按各 connector 页 ✅ [sql/create-table-as.html](https://trino.io/docs/current/sql/create-table-as.html) 同族语法页群）。湖上「删除」的真实成本 = 写侧格式机制，见 [../Apache_Iceberg活用入門/00-总览与阅读地图.md](../Apache_Iceberg活用入門/00-总览与阅读地图.md)。

### 6. 语句族速查（8.1 总览的压缩表）

| 族 | 代表语句 | connector 依赖度 |
| --- | --- | --- |
| 内省 | SHOW */DESCRIBE/EXPLAIN | 低（引擎自答） |
| 元数据 | CREATE/DROP CATALOG*、SCHEMA | 中（能建否看插件） |
| 表 DDL | CREATE TABLE/CTAS/ALTER/DROP | **高**（写能力总开关） |
| DML | INSERT/UPDATE/DELETE/MERGE/TRUNCATE | **最高**（行级操作≈表格式特权） |
| 查询 | SELECT 全家桶（8.10–8.18） | 低 |
| 会话 | USE/SET SESSION/RESET | 无 |
| 事务提示 | START/COMMIT TRANSACTION | 特殊（引擎无常规事务）* |

*具体语义与可支持度 ⚠️ 以 483 各 SQL 语法页现文为准——本表的价值是「依赖度分级」，不是背语句清单。

## 常见误区

- 拿 MySQL 习惯写 `SELECT ... FROM t LIMIT 10` 的「快」预期：分布式 Trino 的 LIMIT 仍需各分片先扫。
- `GROUP BY` 引用列别名/位置的行为差异 ⚠️ 跨库迁移期以报错信息为准。
- information_schema 扫全库超时：它可能逐 catalog 现拉元数据（4.2），生产元数据查询加过滤（`table_schema=`）。
- 以为视图能加速：见上节判断公式。
- DELETE 在不支持行删的 connector 上报「not supported」后回退「DROP+重建」：大表场景先想 Iceberg。

## 与其他章/其他书的联系

- 本章语句的性能解释全在 [04-Trino架构.md](04-Trino架构.md)；函数宇宙在 [09-高级SQL特性.md](09-高级SQL特性.md)；MV 机制在 [06-连接器.md](06-连接器.md)。
- SQL 方言迁移与标准差异的姊妹阅读：[../SQL系列·总索引.md](../SQL系列·总索引.md)（如 SQL 反模式/语言艺术类笔记）；分组操作的立方体理论在 [../数据仓库与OLAP实践教程.md](../数据仓库与OLAP实践教程.md)。
- Spark SQL 语法对照（CTE/JOIN hints 差异）：[../bigdata/04-SparkSQL与结构化数据.md](../bigdata/04-SparkSQL与结构化数据.md)。

## 核心概念速览（中英对照）

1. **SHOW/DESCRIBE 族** — introspection statements：元数据查看的最小动词集。
2. **系统表** — system tables：`system.runtime`/`system.metadata` 引擎内省表。
3. **information schema** — 标准信息模式：跨源元数据的最小公分母视图族。
4. **CTAS** — CREATE TABLE AS SELECT：8.6 的语句形态（语义见 06 章）。
5. **视图** — view：保存的查询，不预计算。
6. **物化视图** — materialized view：预计算 + 改写命中 + REFRESH。
7. **会话属性** — session property：查询行为调参的 SQL 面入口。
8. **复合类型** — array/map/row：一等公民的嵌套值模型。
9. **Sargable 谓词** — sargable predicate：列裸用、可下推的谓词形态。
10. **TopN** — ORDER BY + LIMIT：部分排序优化形态。
11. **Grouping sets** — 分组集：CUBE/ROLLUP/GROUPING SETS 族。
12. **公共表表达式** — CTE (WITH)：内联展开为默认语义的命名子查询。
13. **去关联** — decorrelation：EXISTS/IN 子查询改半连接改写。
14. **TRUNCATE/DELETE** — DML 删数据：connector 支持度分层（行删看格式）。
15. **方言差异** — dialect quirks：Trino vs Hive/MySQL/Pg 的语法语义错位清单。

## 最新演进与工业实践

- **语法面扩张（392→483）**：JSON 数据类型与函数线、MERGE 支持面、`EXPLAIN` 选项、时区与精度语义持续小步演进；官方语法页群随 483 发布 ✅（如 [explain.html](https://trino.io/docs/current/sql/explain.html)）。
- **SQL 标准兼容度**是 Trino 对外的一贯卖点（官方文档/博客口径 ✅ [overview](https://trino.io/docs/current/overview.html) 与 blog feed 历史条目）；2024–2026 的 release notes 高频出现语法修正与标准对齐项（✅ release-483 索引可回溯 ⚠️ 逐条未读）。
- **工业实践**：湖仓 SQL 工作台（dbt-trino、各类 IDE/notebook 经 JDBC）把本章语句变成日常——与 [../数据仓库与OLAP实践教程.md](../数据仓库与OLAP实践教程.md) 的「查询即资产」治理观合流；CTE 不物化导致的重复扫描在 BI 工具生成 SQL 里是常见慢因（工程口径 ⚠️）。
