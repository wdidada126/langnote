# 03 · Executing SQL queries（执行 SQL 查询）

> 覆盖原书第 3 章。目录来源：✅ Manning 官方 TOC 实抓。本章是全书的 SQL 地基：DDL/DML 常规操作 + **DuckDB 方言扩展**——后者的"爽点语法"大多已反哺其他引擎。

## 内容规格（小节地图，✅ 实抓）

- **3.1 A quick SQL recap**：假设你懂 SELECT/WHERE/JOIN/GROUP BY，本章直接进 DuckDB 特色。
- **3.2 Analyzing energy production**：全章贯穿案例——欧 Stat 能源统计 CSV：下载→建 schema→查询。
- **3.3 DDL**：3.3.1 CREATE TABLE（含 `AS SELECT` CTAS）；3.3.2 ALTER TABLE（RENAME/ADD/DROP COLUMN，列存友好）；3.3.3 CREATE VIEW（含 `CREATE OR REPLACE`、宏 `CREATE MACRO`）；3.3.4 DESCRIBE / SUMMARIZE（免 information_schema 的快速体检）。
- **3.4 DML**：3.4.1 INSERT（直插/`INSERT BY NAME`/`INSERT AS`）；3.4.2 Merging data（`INSERT ... ON CONFLICT` UPSERT、UPDATE FROM、`MERGE INTO` 1.x 后）；3.4.3 DELETE/UPDATE；3.4.4 SELECT 全家桶（多表 UPDATE `FROM` 子查询等）。
- **3.5 DuckDB-specific extensions**：3.5.1 SELECT 星号三件套（`* EXCLUDE (col)`、`* REPLACE (expr AS col)`、`* RETURNING`）；3.5.2 按名插入；3.5.3 别名随处可用（GROUP BY 别名/序号、ORDER BY 投影别名）；3.5.4 `GROUP BY ALL` / `ORDER BY ALL`；3.5.5 抽样（`USING SAMPLE n ROWS` / `TABLESAMPLE`）；3.5.6 函数可选命名参数（`func(x, opt := 1)`）。

## 核心技术清单

- 类型系统：DECIMAL 默认、`LIST`/`STRUCT`/`MAP`/`ENUM` 一等公民、无隐式炸裂的宽松 CAST。
- CTAS + `SELECT * FROM 'file.csv'` 一步建表（"schema 从数据来"）。
- 半结构化字面量：`{'a':1}` STRUCT、`[1,2,3]` LIST、`map{'k':v}`；访问 `s.x` / `l[1]`（1 基）。
- 宏体系：`CREATE MACRO`(标量/表宏) + `CREATE TABLE MACRO` + 参数化视图。
- UPSERT 三件套：ON CONFLICT DO UPDATE / UPDATE ... FROM / MERGE INTO。
- 事务：`BEGIN/COMMIT`，默认自动提交；隔离级别 SERIALIZABLE（快照隔离实现）。
- `SUMMARIZE t` 秒出 null 率/min/max/mean——EDA 第一命令。

## 🔧 实测（1.5.5，语法逐条点验）

```sql
CREATE TABLE sales AS SELECT i AS id,(i%10) AS region,(i%50) AS product,random()*100 AS amount
FROM range(100000) tbl(i);            -- CTAS 10 万行瞬时
```

| 语法 | 结果 |
| --- | --- |
| `SELECT region, sum(amount) FROM sales GROUP BY ALL` | ✅ 自动补非聚合列 |
| `SELECT * EXCLUDE (amount) FROM sales` | ✅（REPLACE/RETURNING 同族） |
| `SELECT COLUMNS('region\|product') ...` 正则列选择 | ✅ |
| `SELECT id%7 AS k, count(*) FROM sales GROUP BY k` | ✅ 别名进 GROUP BY |
| `INSERT INTO t2 BY NAME (SELECT region AS name FROM sales)` | ✅ 按列名对齐 |
| `SELECT count(*) FROM sales USING SAMPLE 1000 ROWS` | ✅ 返回恰 1000 行 |
| `... TABLESAMPLE 1 PERCENT` | ⚠️ 计数返回 0（语义与预期 1%≈1000 不符，Bernoulli 小样本波动/解析口径待深究——抽样结果**先 count 验证再用**） |
| `PREPARE p AS SELECT ?::INT + 1; EXECUTE p(41)` | ✅ 42 |
| `CREATE TYPE mood AS ENUM(...); SELECT 'ok'::mood` | ✅ |
| `SELECT {'a':1,'b':2} AS m, m['a']` | ✅ MAP；STRUCT 同层引用 `s.x` ❌（要外层 SELECT 再引，见陷阱） |
| `SELECT sum(*) FROM (VALUES (1),(2))` | ❌ 必须 `sum(column1)`——`sum(*)` 不是合法写法 |
| `FROM sales SELECT count(*)`（FROM 前置） | ✅ 方言糖 |

## 易错点与陷阱

- **STRUCT 别名同层引用**：`SELECT {'x':1} AS s, s.x` 在 1.5.5 报 Binder Error——同层投影不能互相引用，需包一层子查询。
- **列序陷阱**：`INSERT INTO t SELECT ...` 位置对齐而非名字——数据错位无报错，**生产一律 `INSERT BY NAME`**。
- **DECIMAL 默认**：整数除法 `3/2=1.5`（≠ PG 的 1）、`INT` 自动升宽；聚合出 `Decimal` 对象在 Python 端要做 float 转换。
- **UPDATE 无 FROM 的写法差异**：`UPDATE a SET x=b.x FROM b WHERE ...` 的 SET 里不能出现表前缀（1.x 某版本语法收紧，⚠️ 以文档为准）。
- 别名在 `WHERE` 里仍不可用（标准限制），GROUP BY/ORDER BY 才放开——别想当然。
- `GROUP BY ALL` 遇到常量列也分组，结果行数可能超预期；导报表前先 count。
- 1.x 的 `SAMPLE n PERCENT` 老写法在部分版本直接 Parser Error（本目录 04 章实测撞上过），CI 升级要回归。

## 核心概念速览（中英对照）

- **CTAS** — CREATE TABLE AS：从查询结果建表/填表一步到位。
- **按名插入** — INSERT BY NAME：按列名匹配而非位置。
- **GROUP BY ALL** — 自动分组：非聚合表达式全部进 GROUP BY。
- **星号投影修饰** — star modifiers：EXCLUDE/REPLACE/RENAME 对 `*` 做减法/替换。
- **COLUMNS 正则** — column globbing：`COLUMNS('re')` 动态选列。
- **宏** — Macro：标量/表级参数化表达式对象。
- **UPSERT** — INSERT ON CONFLICT：冲突则更新。
- **MERGE INTO** — 合并语句：WHEN MATCHED/NOT MATCHED 分流（⚠️ 成书后 GA）。
- **DESCRIBE/SUMMARIZE** — 表结构/数据速览语句。
- **命名参数** — named arguments：`f(x, side := 'left')` 可选参写法。
- **ENUM 类型** — 枚举：省空间、可排序字典。

## 最新演进与工业实践

- **方言的"逆流"**：`GROUP BY ALL`、星号三件套、QUALIFY 已被 Snowflake/Databricks/BigQuery(dry run)/ClickHouse 陆续抄录；DuckDB 事实上成为"分析方言试验田"（社区共识，⚠️ 无单一权威链接）。
- **MERGE INTO 稳定化**：1.4/1.5 线中 UPSERT 语义已覆盖 DELETE/INSERT/UPDATE 全支（官方文档路径以 https://duckdb.org/docs/stable/clients/overview ✅ 为入口；成书时仅 ON CONFLICT+UPDATE FROM）。
- **1.x 类型演进**：v1.3 起新增半结构化 `VARIANT`（自动混型 JSON 列）——解决 03 章 STRUCT 推断翻车史（GitHub release notes ✅ v1.3.0/2025-05-21）。
- **与 dbt 的方言层**：dbt-duckdb 把 `adapter` 行为钉在 DuckDB 方言上；版本升级时的方言漂移是 dbt 项目回归重点（见 08 章文件）。
