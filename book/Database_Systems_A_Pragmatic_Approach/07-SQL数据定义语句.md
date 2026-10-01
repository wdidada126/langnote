# 07 SQL 数据定义语句（原书第 11 章）

> 书目：《Database Systems: A Pragmatic Approach》，Elvis C. Foster & Shripad V. GodBole，Apress 2014，章 DOI `10.1007/978-1-4842-0877-9_11`（pp.177–218，42 页，SQL 部类最长章）。
> 证据级：章题/页码/DOI ✅；章首段 ✅ Springer 摘要逐字；语法细节 ⚠️ 依 Oracle 10g 文档语境转述；🔧 为 SQLite/DuckDB 实测，**非本书引擎（Oracle 10g）行为**。

## 1 本章定位与摘要逐字锚

Division 三开门章，且是全书法言立场的自供状（✅ 逐字）：

> "The main SQL definition statements in an Oracle 10G environment are shown in figure 11-1. These statements relate to the six basic types of database objects in Oracle — tables, indexes, views, constraints, synonyms, and sequences. Other more advanced types of database objects include databases, table-spaces, data-files, users, user profiles, functions, and procedures."

**六基本对象+高级对象十项**是本册 DDL 大纲的一手证据——注意它把"表空间/数据文件/用户/概要文件"也算 DDL 对象，这是 Oracle 世界观看数据定义的方式（物理与逻辑不分家），与 SQL 标准只谈 schema 对象构成鲜明对照。

## 2 内容主讲（基本六件套 ⚠️ 依摘要展开，语法按 2014 前后 Oracle 通行口径转述）

- **表 CREATE TABLE**：列定义+数据类型（VARCHAR2/NUMBER/DATE/…⚠️ 本册具体用哪些类型无逐字证据）、DEFAULT、列约束内联 vs 表约束分离写法。
- **约束 CONSTRAINT**：PK/FK/UNIQUE/CHECK/NOT NULL 的命名与启用/禁用（ch4 规则的 DDL 化）。
- **索引 CREATE INDEX**：B 树索引声明（✅ ch27 摘要背书"most DBMS suites implement them by default"）、UNIQUE 索引、正反向/组合键（细节 ⚠️）。
- **视图 CREATE VIEW**：预告 ch13 专章。
- **同义词 SYNONYM**：Oracle 特色别名层（公有/私有），标准 SQL 无对应物——本册最"方言"的一节（⚠️ 讲解深度无证据）。
- **序列 SEQUENCE**：计数器对象（`NEXTVAL/CURRVAL`），Oracle 10g 时代的自增方案（IDENTITY 列属 12c 后 ⚠️ 时间线注记）。
- **ALTER/DROP**：加列/改列/删对象与级联；**高级对象**：database/tablespace/datafile 存储骨架、user/profile 安全配额、function/procedure 存储过程预告（与 ch15"程序性局限"呼应）。

## 3 🔧 双引擎 DDL 对照实测（非本书行为）

| 概念（本书 Oracle 口径） | SQLite 3.45.3 | DuckDB 1.5.5 |
|---|---|---|
| 表+域约束 | 弱类型：`INTEGER` 列存 'abc' 成功（E1 `typeof`→text） | 强类型：`'x'`→INT32 报 ConversionException（E2） |
| PK/FK/UNIQUE/CHECK | 全支持；FK **默认关**须 `PRAGMA foreign_keys=ON`（E1） | 全支持且默认执法；列级 `did INTEGER REFERENCES dept(did)` 语法接受（E2） |
| 事后加 CHECK | 支持 ADD COLUMN 受限、约束须重建表 | **`ALTER TABLE … ADD CONSTRAINT CHECK` → `Not implemented Error`**（E2 实测） |
| 索引 | `CREATE INDEX idx_emp_did_sal ON emp(did,salary)`→EQP 立变 `SEARCH … USING INDEX (did=? AND salary>?)`；30 万行点查 **8.636ms→0.032ms（267.4×）**（E4） | 1.5.5 **接受 CREATE INDEX**（ART），DROP INDEX 正常；1M 行点查 1.29ms（带）/1.65ms（不带，行组 min-max 跳扫）——旧版"不支持索引"口径已过时（E4） |
| 同义词 | 无对象；用 ATTACH+别名替代（E8b） | 无对象；视图/MACRO 顶替 |
| 序列 | `AUTOINCREMENT`（ROWID 包装） | `SEQUENCE` 对象+`nextval`（本书两方言之外的现代折中） |

- ⚠️ 上表 Oracle 列为本书语境转述（10g 已不可实测），SQLite/DuckDB 列为工作区一手实测。
- 🔧 附加：DuckDB `duckdb_tables()/duckdb_columns()` 可把刚建的 DDL 结构回读成表（E6）——"DDL 写完即元数据"的目录学视角直通 ch14。

## 4 与本书其他章的接线

- ←ch4（规则→语法）、←ch3（类型=域草案）；→ch14（这些 DDL 全存进目录）、→ch17 附录（索引的实现=树）；ch16–19 概览章用同一批对象名对四产品各扫一遍（⚠️ 结构推断）。

## 5 对位阅读（实链，已验名）

- [../Using_SQLite/07-建表约束与Pragmas.md](../Using_SQLite/07-建表约束与Pragmas.md)：SQLite 侧 DDL+约束+PRAGMA 的专册展开（E1 的权威续读）。
- [../Pro_SQL_Server_Internals/01-数据页与数据存储内部结构.md](../Pro_SQL_Server_Internals/01-数据页与数据存储内部结构.md)：把"表空间/数据文件"翻成页/区/分配单元的内幕视角。
- [../Databases_Illuminated_4e/04-SQL基础-DDL与DML.md](../Databases_Illuminated_4e/04-SQL基础-DDL与DML.md)：同代教材 DDL 的紧凑版。
- [../Oracle_Essentials_5e/02-物理存储结构与表空间.md](../Oracle_Essentials_5e/02-物理存储结构与表空间.md)：本册"advanced objects"（tablespace/datafile）的现代 Oracle 深潜（波7 #44 册）。

## 6 教学与实操要点

1. 记 Oracle 六件套的顺序=使用密度：表>约束>索引>视图>序列>同义词——2026 除同义词衰微外全数成立。
2. DDL 三问自查：物理放哪（表空间/文件）、逻辑长啥（类型/约束）、怎么加速（索引）——本章 42 页无非这三问的展开。
3. 在 SQLite 项目里，"建表即约束"必须配套 `PRAGMA foreign_keys` 检查脚本（E1 血泪实测）；在 DuckDB/分析仓里，改表能力缺口（E2 ALTER 拒）决定 schema 演化策略。

## 7 深挖与自测

### 概念辨析十问
1. 六基本对象按"使用频率×方言浓度"排？——表/约束/索引高频低方言；同义词低频高方言（Oracle 独有）。
2. 约束"声明式"宣言在哪？——目录可查、可启停、可被优化器用（E6 可查性实证）。
3. PK 与 UNIQUE+NOT NULL 差在哪？——语义位：参照目标/集群倾向/优化器信任。
4. 索引是 DDL 还是性能策略？——语法属 DDL，决策属物理设计（ch17+PDD 书系回收）。
5. 序列何时不该用？——代理键需求可被 IDENTITY（Oracle 12c 后）/AUTOINCREMENT（🔧E2）覆盖时。
6. 同义词的现代等价物？——视图/CTE/搜索路径；未流传为通用对象。
7. 表空间进 DDL 的代价？——逻辑设计与物理放置纠缠；非 Oracle 世界普遍拒绝该切分。
8. ALTER 族真痛点？——加列易、改类型难、加约束有引擎直接不支持（DuckDB E2 Not implemented）。
9. DROP 与 TRUNCATE 分界？——对象消亡 vs 内容清空保结构（本册辨析与否 ⚠️ 未取证）。
10. 存储函数进 DDL 章说明什么？——"对象"世界观：代码也是被定义被授权的对象（ch13/15 回收）。

### 常见误区六条
- DDL 写完即生效——SQLite FK 需 PRAGMA（E1）；定义与执法两层。
- VARCHAR 万能——业务域约束在应用层重写一遍=没建模。
- 索引多多益善——写放大+统计陈旧；E4 教"先量测后建"。
- 结构变更走手工脚本——无迁移框架=目录与代码漂移（2026 用 Flyway/dbt 类）。
- 序列当业务号段——跳号/分段/合规规则要专门设计，勿挤引擎计数器。
- 背完 Oracle 六件套不换方言视角——四概览的"同标不同实"才是本章目的。

### 🔧 加餐：两引擎 DDL 备忘（非本书行为）
- SQLite：表=ROWID 王国（INTEGER PRIMARY KEY 别名）；一切对象元数据同居 sqlite_master（E6）。
- DuckDB：DECIMAL 保标度/列级 REFERENCES 可写/CREATE INDEX 已可用（1.5.5，E4）——文档口径按版本读。

### 一分钟版
- 42 页只答三问：放哪（存储）、长啥（类型约束）、怎么快（索引）。
- Oracle 六件套+高级十项=2014 企业 DBA 的 DDL 世界观切片。
- 带走技能：任何 DDL 先问"这引擎执行吗"（E1/E2 双课）。

## 8 术语快卡与跨书对位

| 术语 | EN | 一句话定位 |
|---|---|---|
| CREATE TABLE | 基本 DDL | 建表：列+域+约束一次声明 |
| 列级/表级约束 | Column/Table Constraint | 同一规则两种挂载点 |
| 域断言 | Domain Assertion | CREATE DOMAIN 上的检查（本书点名 MySQL 不支持） |
| 索引 | INDEX | 加速读、拖慢写，2026 仍成立 |
| ALTER | 变更表结构 | 加列易、改型难 |
| CASCADE | 级联 | DROP/删除沿外码传导 |

**跨书对位（盘上已验证目录）**：
- 参 [Fundamentals of Database Indexing]：索引纵深（盘上目录名以终检为准，此处只登记不链）。
- 🔧：E1/E2 在 SQLite/DuckDB 实测建表约束与索引行为，非本书引擎行为。

**速测**：合上书，用一句话向同事讲清本册最难的概念；讲不清就回到 §7 误区清单重读。

## 核心概念速览（中英对照）

| 中文 | English | 一句话 |
|---|---|---|
| 数据定义语言 | Data Definition Language (DDL) | 定义/修改/删除对象 |
| 数据库对象六件套 | tables/indexes/views/constraints/synonyms/sequences | ✅ 摘要逐字的 Oracle 基本对象 |
| 表空间/数据文件 | tablespace/datafile | Oracle 存储骨架入 DDL |
| 序列 | sequence | 引擎级计数器对象 |
| 同义词 | synonym | 对象别名（Oracle 特色） |
| 命名约束 | named constraint | 便于后管（禁用/启用/查目录） |
| ALTER/DROP | alter/drop | 演化与拆毁 |
| ART 索引 | ART adaptive radix tree | 🔧DuckDB 1.5.5 实测可建（非本书） |

## 最新演进与工业实践

- **Oracle 线**：10g（本书）→ 12c 的 IDENTITY 列取代序列惯用法、19c 长期支持、23ai 收敛——✅ https://docs.oracle.com/en/database/oracle/oracle-database/（200 验真）；存储对象 DDL 家族依旧。
- **声明式 schema 演化**：Iceberg/Delta 的 schema evolution + hidden partitioning 把"ALTER TABLE"的痛迁移到表格式层——盘上 [../Data_Lakehouse_in_Action/04-存储层对象存储文件格式与分区.md](../Data_Lakehouse_in_Action/04-存储层对象存储文件格式与分区.md) 续读。
- **分析引擎补索引课**：DuckDB 1.5.5 从"无 CREATE INDEX"到"接受 CREATE INDEX"（E4 实测）恰是 2022→2026 版本间的事实漂移样本——文档口径要按版本读：✅ https://duckdb.org/docs/stable/sql/statements/create_index.html（200）。
- ⚠️ MySQL 8.4/SQL Server 2025 的 DDL 差异（INSTANT 加列、JSON 列、向量类型）超出本册视野：✅ https://dev.mysql.com/doc/refman/8.4/en/ 与 https://learn.microsoft.com/en-us/sql/sql-server/（均 200）。
