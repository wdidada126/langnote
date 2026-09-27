# 03 · 基础语句：DDL 与 DML（原书第 4 章）

> 对应原书 Ch4 *Basic Statements*（✅ 章题）。
> 实证 ✅：官方仓 `CHAPTER_04/code/chapter04.sql`（3.6KB 实抓）词频——`INSERT`×5、`GENERATED`×5、`IDENTITY`×5、`UPDATE`×2、`DELETE`×3：本章主线=建表/类型/约束+三类 DML，**IDENTITY 生成列是特色重点**。
> 勘误义务（✅ README Errata）：p92 例 5 "插入三条 categories 记录"应为**两条**；p93 例 7 文案应为 "title as C Language and description as Languages"。

## 1. 建表与数据类型（⚠️ 转述 + ✅ 文档锚点）

- 语法权威 ✅ https://www.postgresql.org/docs/current/sql-createtable.html ：列约束/表约束/分区表/CTAS 全谱。
- PG 类型宇宙（⚠️ 书内概览转述）：
  - 数值：integer/bigint/numeric(精度可控)；
  - 字符：text 为一等公民（varchar 无性能差 ⚠️）、citext 扩展大小写不敏感；
  - 时间：timestamp 与 **timestamptz**（书中立场：默认用带时区版 ⚠️）；
  - 结构型：数组、range、复合、json/jsonb（本章点名，深入见第 5 节 🔧）；
  - 网络/几何/UUID 等特种货架 ⚠️。
- 类型可扩展（`CREATE TYPE` 枚举/域/复合）——"PG 不做 schema 教条"的作者立场 ⚠️。
- DEFAULT/NOT NULL/CHECK/UNIQUE/PRIMARY KEY/FOREIGN KEY 六件套与表级 `CONSTRAINT name` 命名纪律 ⚠️+✅ sql-createtable。
- 约束增量两拍（⚠️+✅ 同页）：`ADD CONSTRAINT ... NOT VALID` 先立规不查旧账，`VALIDATE CONSTRAINT` 后台补课——大表在线变更的标准姿势（与 [07-触发器规则与分区.md](07-触发器规则与分区.md) 分区、Ch13 索引话题同构）。

## 2. 标识列：SERIAL 旧法 vs GENERATED 新法（本章高光 ✅）

- `SERIAL`＝隐式 sequence+DEFAULT 的语法糖（⚠️）；SQL 标准式 `GENERATED { ALWAYS | BY DEFAULT } AS IDENTITY` 为 PG 10+ 正统——chapter04.sql 的 IDENTITY×5 实证本书走标准线 ✅。
- 关键语义（⚠️+✅ sql-createtable.html "Identity Columns"）：
  - ALWAYS 拒手插（除非 `OVERRIDING SYSTEM VALUE`）、BY DEFAULT 可手插；
  - 与序列绑定可用 `ALTER TABLE ... ALTER COLUMN ... RESTART WITH` 拨表；
  - 迁移导入（第 4 节 COPY/第 19 章 pgLoader）时的覆盖开关。
- 概念坐标 🔧 见第 5 节实验表（AUTOINCREMENT/sequence/IDENTITY/GENERATED 四谱系）。

## 3. DML 三件套与 RETURNING（✅ 代码+✅ 文档）

- `INSERT ... VALUES|SELECT`（✅ https://www.postgresql.org/docs/current/sql-insert.html ）、`UPDATE ... FROM`（PG 方言联表更新，✅ https://www.postgresql.org/docs/current/sql-update.html ）、`DELETE`（✅ https://www.postgresql.org/docs/current/sql-delete.html ）。
- 三句同吃 `RETURNING`——书风：写后即读，省一次往返 ⚠️+✅。
- 书内实例 ✅（chapter04.sql 行 29-30 实抓）：

```sql
INSERT INTO posts (title,content,author,category)
VALUES ('Indexing PostgreSQL','Btree in PostgreSQL is....',1,1);
```

- 批量装载通道 `COPY`（✅ https://www.postgresql.org/docs/current/sql-copy.html ）：csv/binary/text 格式、`FROM STDIN` 与客户端 `\copy` 的权限差 ⚠️——Ch15 备份恢复复用此件。
- 事务点到即止（BEGIN/COMMIT/ROLLBACK），纵深全部留给 Ch11 → [08-安全权限与事务MVCC.md](08-安全权限与事务MVCC.md) ⚠️。

## 4. 视图与派生对象（本章收尾 ⚠️+✅）

- `CREATE VIEW`（✅ https://www.postgresql.org/docs/current/sql-createview.html ）：保存的查询而非数据——与物化视图的分界在 Ch11 后由 🔧 实验坐实（见 [08 号文件第 6 节](08-安全权限与事务MVCC.md)）。
- CTAS：`create table new_categories as select * from categories limit 0`（chapter5.sql 同款句式，✅ 实抓行 23——结构复制的土办法）；`LIKE INCLUDING ALL` 为更完整替身 ⚠️+✅ sql-createtable。

## 5. 🔧 类比实测 A：自动值/生成值四谱系（非 PostgreSQL 行为）

| 谱系 | SQLite 3.50.6 🔧 | DuckDB 1.5.5 🔧 | PostgreSQL 16 ⚠️+✅ |
|---|---|---|---|
| 自增 | rowid/AUTOINCREMENT | DEFAULT nextval | IDENTITY/SERIAL/序列 |
| 表达式列 | GENERATED VIRTUAL ✅ | **拒绝** STORED ✅ | STORED（18 起+VIRTUAL） |
| 更新守卫 | 报 `cannot UPDATE generated column "s"` | — | ALWAYS 拒写 |

实测记录（sq1.out / duck3.out）：

```text
sqlite> CREATE TABLE gc(a INT, b INT, s INT GENERATED ALWAYS AS (a*b) VIRTUAL);
sqlite> INSERT INTO gc(a,b) VALUES(3,4);  SELECT * FROM gc;   --> 3|4|12
sqlite> UPDATE gc SET s=9;  -- Error: cannot UPDATE generated column "s"

duckdb> CREATE SEQUENCE s;  SELECT nextval('s'), nextval('s'); --> [(1, 2)]
duckdb> CREATE TABLE g(a INT, b INT, s INT GENERATED ALWAYS AS (a*b) STORED);
        Invalid Input Error: Can not create a STORED generated column!
```

PG 对照口径 ⚠️+✅（sql-createtable）：GENERATED 列 PG 12 起仅 STORED，**PG 18 增加 VIRTUAL**（✅ https://www.postgresql.org/docs/release/18.0/ ）——有趣的是"虚拟列"SQLite 早就有、DuckDB 两样都拒。

## 6. 🔧 类比实测 B：JSON——jsonb 之外的两种做法（sq1.out / duck.out 🔧）

PG 双类型：`json` 保真文本重解析、`jsonb` 分解二进制可 GIN 索引、键序不保（✅ https://www.postgresql.org/docs/current/functions-json.html ）。对照：

```text
# SQLite：TEXT 列 + json1 函数族（编入内核）
sqlite> SELECT json_extract('{"a":[1,2,3]}','$.a[1]'), json_valid('nope');  --> 2|0
sqlite> CREATE TABLE j(id INT, doc TEXT CHECK(json_valid(doc)));
sqlite> SELECT id, json_extract(doc,'$.lang') FROM j WHERE json_extract(doc,'$.stars')>2;
        --> 1|plpgsql   2|sql

# DuckDB：JSON 是一等类型，箭头运算符内建
> SELECT doc->'$.lang', doc->>'$.lang' FROM j   --> ('"plpgsql"', 'plpgsql')
> SELECT typeof('{"a":[1,2,3]}'::JSON)          --> 'JSON'
```

三态结论 ⚠️：SQLite=弱类型+强函数+CHECK 自 guard；DuckDB=强类型+列存扩展（JSON↔STRUCT：`struct_extract('{"a":5}'::STRUCT(a INT),'a')→5` 🔧）；PG=双类型分工（保真 vs 加速）。**均非 PostgreSQL 行为**（PG 行以文档为据）。

## 7. 与其他册分工

- psql/导入自动化配方：[../PostgreSQL_16_Administration_Cookbook/02-表数据与psql自动化.md](../PostgreSQL_16_Administration_Cookbook/02-表数据与psql自动化.md)。
- JSON 类型内幕与索引：[../PostgreSQL_10_High_Performance_3e/08-数据访问路径与表设计取舍.md](../PostgreSQL_10_High_Performance_3e/08-数据访问路径与表设计取舍.md)。
- 模式设计理论后台：[../Database_Modeling_and_Design_5e/00-总览与阅读地图.md](../Database_Modeling_and_Design_5e/00-总览与阅读地图.md)。
- 进阶语句 → [04-高级语句_连接与递归查询.md](04-高级语句_连接与递归查询.md)。

## 核心概念速览（中英对照）

1. **标识列** — identity column：`GENERATED ALWAYS AS IDENTITY`，PG10+ 正统自增。
2. **序列** — sequence：IDENTITY/SERIAL 底下的计数器对象。
3. **生成列** — generated column：表达式列，STORED/VIRTUAL 两副面孔。
4. **外键** — foreign key：跨表完整性锚点。
5. **检查约束** — CHECK：行级谓词守门员。
6. **NOT VALID/VALIDATE** — 约束增量两拍：在线变更防长锁 ⚠️。
7. **UPDATE ... FROM** — PG 方言联表更新。
8. **RETURNING** — 写后即读子句。
9. **OVERRIDING SYSTEM VALUE** — 身份列覆盖开关：迁移导入放行道。
10. **CTAS** — CREATE TABLE AS：查询落表，DDL×DML 杂交。
11. **COPY** — 高速装载通道：csv/binary，与 pg_dump 分工。
12. **jsonb** — 分解二进制 JSON：索引与算子的载体。
13. **timestamptz** — 带时区时间戳：全书推荐默认。

## 最新演进与工业实践

- **PG 18 虚拟生成列** ✅（release 18.0 页）：`GENERATED ... VIRTUAL` 落地且可读时计算——本书 16 基线只有 STORED，新代码可直接面向 18 的语义。
- **IDENTITY 一统**：新代码禁 SERIAL 已是社区共识 ⚠️；迁移器（pgLoader ✅ https://api.github.com/repos/dimitri/pgloader ）自动映射 AUTO_INCREMENT→identity。
- **JSON 工业位势** ⚠️：jsonb 承担多租户属性/事件负载是 PG 侧常态；分析侧 JSON 由 DuckDB 直读（🔧 已证运算符），生产链路常见"PG jsonb → 湖内 Parquet/STRUCT"。
- **在线 DDL 姿势**：NOT VALID+VALIDATE、CONCURRENTLY 索引（Ch13 → [10-查询调优索引与性能.md](10-查询调优索引与性能.md)）、gh-ost 思想同源对照 [../Understanding_MySQL_Internals/00-总览与阅读地图.md](../Understanding_MySQL_Internals/00-总览与阅读地图.md) ⚠️。
