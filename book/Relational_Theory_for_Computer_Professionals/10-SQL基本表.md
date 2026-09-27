# 第 10 章　SQL 基本表（SQL Base Tables ⚠️ 回译）

> 译本 p129–138｜小节（✅ 实抓）：10.1 发展历史 / 10.2 基本概念 / 10.3 表的特性 / 10.4 修改表 / 10.5 等值比较 / 10.6 定义表 / 10.7 SQL 系统与程序系统 / 10.8 练习 / 10.9 答案。
> 第三部分（SQL，第 10–14 章）开篇：从这里开始，作者把前九章建立的坐标系拿来**逐项对照 SQL**。写法从" Tutorial D 讲模型"切换为"SQL 讲偏离"。

## 本章地图

| 小节 | 内容 | 结论 |
| --- | --- | --- |
| 10.1 发展历史 | SEQUEL → IBM SQL/System R → ANSI X3.135-1986 / ISO 9075:1987 → SQL-92 → SQL:1999 → SQL:2003/2008/2011/2016（⚠️ 版本清单按通行口径） | SQL 的历史是"实现先于标准、标准追赶实现"的历史 |
| 10.2 基本概念 | 表/列/行、目录（catalog）与模式（schema）、基本表 vs 派生表 vs 视图 | SQL 的概念体系是**两层**（值/变量不分），与模型的"关系值 + relvar"两层不同构 |
| 10.3 表的特性 | 五条：可空、重复行、列有序、行无序但**可被 ORDER BY 观测**、单元只能一个值 | 五条里除最后一条，其余都是偏离 |
| 10.4 修改表 | INSERT / UPDATE / DELETE 逐行、默认值、`INSERT ... SELECT` | 逐行更新意味着"中途状态"合法存在 ⇒ 与第 7.5 的替换语义冲突 |
| 10.5 等值比较 | `=` 在 SQL 里是 3VL 谓词；行（元组）比较与 `IS NOT DISTINCT FROM` | 相等不是等价：两行都含 NULL 时 `=` 不为真，"看起来相同"却不相等 |
| 10.6 定义表 | CREATE TABLE 的约束子句（PK/UNIQUE/FK/CHECK）与域缺失 | 约束是**可选附加物**；产品默认关闭/不实现关键项（🔧） |
| 10.7 SQL 系统与程序系统 | 视图、授权、存储过程把哪些规则留在数据库里 | 判据同第 3 章：一份事实在系统里被表达几次 |

## 核心精讲

### 1. 历史小账（10.1）

⚠️ 转述（标准号与年份采用通行书目口径，本目录未能逐条对到 ISO 页面）：SQL 起源于 IBM Research 的 SEQUEL（1974）与 System R 实现，1986 年成为 ANSI 标准（X3.135-1986）、1987 年成为 ISO 9075；随后 SQL-92（增 NATURAL JOIN、CHECK 约束、断言）、SQL:1999（引入 SQL/O、递归查询、触发器、`GROUPING SETS`）、SQL:2003（窗口函数）、SQL:2008（`TRUNCATE`、INSTEAD OF 触发器完善）、SQL:2011（时序/应用周期）、SQL:2016（JSON）、SQL:2023（JSON 能力扩展、属性图 PGQ）。本书成书于 2012 年，覆盖到 SQL:2008/2011 一代的偏离，与第 14 章清单一致。

一条历史事实对读本书很有用：**标准里的 NULL/3VL 是继承自实现（System R）而非来自关系模型**。作者对此的处理不是骂，而是把 3VL 的真值表逐格写清（第 11 章），让读者知道每一格的后果。

### 2. 表的五条特性（10.3）—— 本章的靶心

| SQL 表的特性 | 关系的要求 | 偏离后果（可实测/已在书内实测） |
| --- | --- | --- |
| 允许重复行 | 集合，无重复元组 | 同一"事实"存两遍；`COUNT(*)` 不再等于基数 → 🔧 D1 |
| 列有序（第 1 列、第 2 列） | 头是属性的**集合** | `UNION`/`*`/按位置取列都能观察顺序 → 🔧 D2、D10f |
| 行物理有序可变 | 元组无序 | 无 `ORDER BY` 的结果不稳定；`LIMIT` 非确定 → 🔧 D10、D10b |
| 单元可有多个值（NULL / 逗号串 / JSON） | 1NF：单元一个值 | 需要字符串解析或 `json_each` → 🔧 D10d |
| 可空（每个列都可空） | 是否可空是**头的成分**，必须显式声明 | 约束/谓词处处带 3VL → 第 13 章 |

前四条正是第 1 章"接口是否关系型"判据的可操作检验项。作者给 SQL 表下的定义大致是：**表是带位置信息的、允许重复的、单元可能不原子的关系近似**。

### 3. 🔧 实测：位置、顺序、非确定（SQLite 3.45.3，方法见 00）

```sql
-- D1/D1c：重复行 + 隐藏身份
INSERT INTO S_dup VALUES ('S1','Paris'),('S1','Paris'),('S2','Rome');
SELECT COUNT(*) FROM S_dup;      -- -> [(3,)]
SELECT rowid, * FROM S_dup;      -- -> [(1,'S1','Paris'),(2,'S1','Paris'),(3,'S2','Rome')]

-- D2：UNION 按位置对齐，属性名不参与
WITH A(x,y) AS (VALUES (1,2)), B(y,x) AS (VALUES (3,4))
SELECT * FROM A UNION ALL SELECT * FROM B;      -- -> [(1, 2), (3, 4)]

-- D10/D10b：行序与 LIMIT 的非确定性
SELECT SN, STATUS FROM S;                       -- 顺序随扫描方式变
SELECT * FROM SP LIMIT 2;                       -- -> [('S1','P1',300),('S1','P2',200)]

-- D10f：交换列序仍是"同一关系"，但下游按位置取列会炸
SELECT SN, CITY FROM S ORDER BY SN;             -- -> [('S1','Paris'),...]
SELECT CITY, SN FROM S ORDER BY SN;             -- -> [('Paris','S1'),...]
```

第 4 组对照特别值得记住：**模型层面两行查询完全等价**（同一关系、同一元组集），SQL 层面它们是两个不同的结果集结构。凡是"按位置取列"的代码，都把这条等价关系变成了兼容性事故。

### 4. 等值比较（10.5）：SQL 的 `=` 是 3VL 谓词

- `NULL = NULL` → UNKNOWN；`NULL <> 3` → UNKNOWN；只有 `IS NULL` 是探测器（第 11 章展开真值表）；
- 行比较 `(a,b) = (c,d)` 是逐列 `=` 后 AND，**任一格 NULL 即 UNKNOWN**；
- 因此"两行看起来一样"不等于"两行相等"：`IS NOT DISTINCT FROM`（标准 SQL，PostgreSQL/DuckDB 支持 ⚠️ 转述）才是"带 NULL 的相等"。🔧 SQLite 3.45.3 的对应物是 `IS`：`SELECT (NULL IS NULL), (1 IS NULL), (1 IS 1)` → `[(1, 0, 1)]`（实测）；而袋语义的差集运算符 **SQLite 不支持**（🔧 `SELECT 1 EXCEPT ALL SELECT 1` → `near "ALL": syntax error`）。

🔧 本目录实测的两条相关后果（第 8/11 章也用）：

```sql
SELECT (NULL = 3), (NULL <> 3), (NULL IS NULL), (NULL = NULL);   -- -> [(None, None, 1, None)]
SELECT COUNT(*) FROM T8 WHERE ST = 20;      -- -> 2
SELECT COUNT(*) FROM T8 WHERE NOT (ST=20);  -- -> 1，两者相加 ≠ 总数 4
```

### 5. 定义表与约束（10.6）

`CREATE TABLE` 能声明：`NOT NULL`、`UNIQUE`、`PRIMARY KEY`、`CHECK`、`FOREIGN KEY ... REFERENCES ... [MATCH SIMPLE|PARTIAL|FULL] [ON DELETE ...]`。作者的对照点：

- 关系模型的**码是类型的一部分**，SQL 的码是表定义里的一个可选子句；
- 标准有 `CREATE DOMAIN`（域约束）但产品支持参差；SQL 的列类型 ≠ 域（无精化谓词，除非写 CHECK）；
- 外键的 MATCH 三种类型是给"可空外码"擦屁股的（🔧 第 6 章已实测 CHECK 不能带子查询，所以任何"部分唯一/条件依赖"也无处声明）。

### 6. SQL 系统与程序系统（10.7）

1.4 与 3.6 做过两次这个对照，这里是 SQL 版：SQL 允许把规则放进数据库的槽位有四个（约束、断言〔标准有/产品无〕、视图 + `WITH CHECK OPTION`、触发器/存储过程），实际项目通常只用后两个 ⇒ 后两个是过程式的 ⇒ 回到程序系统。作者的判断 ⚠️ 重构：**一个 SQL 数据库越依赖存储过程承载业务规则，它就越接近"带 SQL 接口的文件服务器"**。

## 常见误区

| 误区 | 纠正 |
| --- | --- |
| 「表就是关系，只是实现粗糙些」 | 位置可观察、重复合法、单元非原子这三条都是**语义**差异，不只是粗糙 |
| 「不写 ORDER BY 结果也是稳定的，实测没出问题」 | 稳定性是实现副产品（索引/统计变化即变）；🔧 D10b 的 `LIMIT` 是最容易踩的坑 |
| 「`SELECT *` 方便又安全」 | 它把列序变成契约（🔧 D10f）；接口层必须列名显式 |
| 「两个 NULL 不相等只是古怪，不影响业务」 | 它同时破坏相等性、聚合定义域、外键匹配、行比较（第 11/13 章逐个看） |
| 「标准一直在修这些问题」 | 2016/2023 修的是 JSON/PGQ/窗口；重复行与 3VL 一条未动（第 14 章清单） |
| 「有存储过程就是数据库系统在管规则」 | 过程式规则仍是程序系统；判据是"声明式约束表达了几次事实" |

## 与其他章 / 其他书的联系

- 本章五条偏离的完整版（含聚合、外连接、ORDER BY）：[14-SQL与关系模型.md](14-SQL与关系模型.md)。
- 子句级对照（σ π ∪ − ρ ⋈ 的 SQL 形态与陷阱）：[11-SQL操作符Ⅰ.md](11-SQL操作符Ⅰ.md)；MATCHING/EXTEND/SUMMARIZE 的缺位：[12-SQL运算符Ⅱ.md](12-SQL运算符Ⅱ.md)。
- 3VL 与"取反"的工程排雷版：[../SQL_and_Relational_Theory/06-NULL与三值逻辑3VL.md](../SQL_and_Relational_Theory/06-NULL与三值逻辑3VL.md)、[../SQL_and_Relational_Theory/09-重复行DISTINCT与集合语义.md](../SQL_and_Relational_Theory/09-重复行DISTINCT与集合语义.md)；那本 03 章（为什么没有重复元组）与本章 10.3 是同一主题的两种写法：本直给模型判据，那本给 SQL 处方。
- 可空性作为头的成分：[../SQL_and_Relational_Theory/07-缺失值的真实语义-42与2与Placeholder.md](../SQL_and_Relational_Theory/07-缺失值的真实语义-42与2与Placeholder.md)（两类缺失值与 Placeholder，对 10.3 第 5 行）。
- 学院教材的 SQL 语法全集（不作偏离评判）：[../数据库系统概念6/03-SQL.md](../数据库系统概念6/03-SQL.md)、[../数据库系统概念6/04-中级SQL.md](../数据库系统概念6/04-中级SQL.md)。
- 真实产品里的"位置"从哪来（列 ID、行头）：[../mysql/04-记录在页中如何存储.md](../mysql/04-记录在页中如何存储.md)、[../mysql/09-表级别的操作.md](../mysql/09-表级别的操作.md)。
- [#87 `Using_SQLite`](../Using_SQLite/00-总览与阅读地图.md)（已落盘；同一引擎的行为手册，本直全部 🔧 的产品侧解释在那里）；[#23](../Cost_Based_Oracle_Fundamentals/00-总览与阅读地图.md)/[#45](../Efficient_MySQL_Performance/00-总览与阅读地图.md)（性能视角下的 `SELECT *`/索引可见列）。

## 核心概念速览（中英对照）

- **基本表** — base table：SQL 中对应 relvar 的构造（但值/变量不分、可含重复行）
- **派生表 / 相关子查询** — derived table：FROM 里的子查询，是"临时表"而非关系值
- **目录 / 模式** — catalog / schema：SQL 的元数据层次；模型层只关心关系与其类型
- **列有序** — ordinality of columns：SQL 的头是有序列表，可被 `UNION`/`*`/位置取列观察
- **重复行** — duplicate rows：SQL 表的默认许可，与关系定义冲突
- **单元非原子** — non-atomic cell：逗号串/JSON 塞一格，靠解析函数还原 🔧 D10d
- **可空性** — nullability：SQL 里每列默认可空；模型里它属于头的显式成分
- **行比较** — row comparison：`(a,b)=(c,d)` 逐列 AND，遇 NULL 即 UNKNOWN
- **`IS NOT DISTINCT FROM`** — null-safe equality：把 UNKNOWN 折成真假的"相等"（⚠️ 产品支持不一）
- **MATCH SIMPLE / PARTIAL / FULL** — 外码匹配类型：为可空外码准备的三种规定
- **`CREATE ASSERTION`** — 断言 DDL：SQL:1999 有、产品几乎无（🔧 SQLite 语法错误）
- **SQL 系统 vs 程序系统** — 判据：业务规则以声明式约束表达，还是以过程式代码表达 N 次

## 最新演进与工业实践

- **SQL:2016/2023 与本章五条偏离（⚠️ 转述）**：这两轮修订增加了 JSON 类型/函数（SQL:2016 起，SQL:2023 扩展构造与表函数）与属性图查询 PGQ，并持续加窗口/有序聚合能力；**重复行、NULL/3VL、列序可观察、单元可非原子这四条完全没动**。也就是说本章的偏离清单在 2026 年仍然成立。标准条目页无法在线核实（iso.org 返回 403），此处只给标准号口径。
- **产品在"可空性显式化"上的反向进展**（🔧/文档）：SQLite 严格到近乎放任（affinity），PostgreSQL 提供域/生成列/表达式索引/`NOT NULL` 的强制与 `NOT VALID` 约束的渐进启用，DuckDB 走"类型强、约束弱"路线（PRIMARY KEY/UNIQUE 更多服务于导入语义）。PostgreSQL 约束文档：https://www.postgresql.org/docs/current/ddl-constraints.html ✅；DuckDB SELECT 语法：https://duckdb.org/docs/sql/query_syntax/select ✅
- **`SELECT *` 的现代事故面**：列式扫描/向量化引擎（DuckDB/ClickHouse/Parquet 谓词下推）让"取哪些列"直接决定 I/O，`SELECT *` 的代价从"多几列网络"变成"扫描整个文件族"。⚠️ 转述（本目录未测）。
- **NULL 安全比较的实际可用集**（🔧 本目录实测口径）：SQLite 用 `IS` / `IS NOT` 做 NULL 安全比较（`a IS b` 在两边都 NULL 时为真），PostgreSQL/DuckDB 支持 `IS NOT DISTINCT FROM`；MySQL 用 `<=>`。⚠️ 除 SQLite 外未实测。
- **深浅分工**：本章是"用模型看 SQL"的第一遍；**具体怎么在 SQL 里绕开这些坑**（DISTINCT/显式列名/COUNT 处理/EXCEPT 写法）在 [../SQL_and_Relational_Theory/](../SQL_and_Relational_Theory/00-总览与阅读地图.md)；**产品实现为什么这样**在 [#87](../Using_SQLite/00-总览与阅读地图.md)（已落盘）与 [../mysql/mysql是怎样运行的.md](../mysql/mysql是怎样运行的.md)。
