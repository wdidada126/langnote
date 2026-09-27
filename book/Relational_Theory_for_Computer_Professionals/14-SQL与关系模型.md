# 第 14 章　SQL 与关系模型（SQL and the Relational Model ⚠️ 回译）

> 译本 p177–182｜小节（✅ 实抓）：14.1 概述 / 14.2 SQL 与关系模型的不同点 / 14.3 练习 / 14.4 答案。
> 这是全书的**结账章**：前 13 章逐项讲过的偏离在这里合成一张清单，并回答第 1 章就提出的那个问题——「SQL 是关系型语言吗？」
> 作者的判定口径始终没变：**「关系型」不是「有表」，而是「用户接口是否真正实现关系模型」**（第 1 章）。

## 本章地图

| 偏离的层次 | 条目数 | 代表证据（🔧 = 本目录实测，编号见 `demos.txt` 的 D 系列 / `ch13_out.txt` 的 A 系列） | 可否在不换语言的前提下修好 |
| --- | --- | --- | --- |
| 头（heading）层 | 3 | D2、D10f（列有序）；A6（可空性不是头的声明成分） | 部分可修（禁 `SELECT *`、要求显式 NOT NULL） |
| 体（body）/ 元组层 | 4 | D1（重复行）、D1c/D3c（隐藏身份）、D10d（非原子单元）、D4d/D6（无零度关系） | **可修而未修**（DISTINCT 是开关，不是默认） |
| 值 / 变量层次 | 2 | D10e（比较要绕）、A14（逐行更新） | 不可修：语法地基 |
| 算子层次 | 6 | D5b/D5c/D5d/D5e、D4d、12 章 EXTEND/映像 | 部分可补语法（DuckDB 已有 SEMI/ANTI JOIN） |
| 逻辑 / NULL 层次 | 4 | D8c/D8e/D8f、A7、A12 | 不可修：改了就不是 SQL |
| 约束层次 | 6 | A1–A4、A8、A9、A11、A18、D7f | 可修：断言/DOMAIN 标准都写过 |
| 序与展示层次 | 3 | D10、D10b、D10c | 应彻底分层，不该进语言 |

## 核心精讲

### 1. 14.1 概述：判据只有一条，误用有十种

作者在这一章把「SQL 到底有多关系型」从情绪问题变成分层清单。判据（第 1 章）：**看用户接口，不看内部实现**——存储引擎怎么排行、要不要堆文件，都与"关系型"无关；能观察到的语义违反模型，才是违反模型。

一个常被忽略的事实是：**「完全实现 SQL」从来不是全有全无**。✅ 一手取证（本目录抓取 ISO/IEC 9075:1992 公开文本，https://www.contrib.andrew.cmu.edu/~shadow/sql/sql1992.txt ，`curl` 200，50794 行）——其 Clause 23「Conformance」23.2「Claims of conformance」原文（第 42911–42923 行）：

```
23.2  Claims of conformance
Claims of conformance to this International Standard shall state:
1) Which level of conformance is claimed:
   a) Full SQL (The complete database language specified in this International Standard.)
   b) Intermediate SQL (Intermediate SQL is a subset of Full SQL as specified in the Leveling Rules.)
   c) Entry SQL (Entry SQL is a subset of Intermediate SQL as specified in the Leveling Rules.)
```

也就是说，标准自己就把"实现到哪一档"写进了合规声明：一个只支持 Entry SQL 的产品照样可以自称符合 SQL。⚠️ 后续版本（SQL:1999 之后的 Core/Enhanced 分档、SQL:2016/2023 的符合性口径）未在本目录一手核实，只作方向说明。

推论：讨论「SQL 关系吗」的正确问法不是「是/否」，而是**「哪几条偏离是我正在用的这一款产品的」**——这正是 14.2 清单的用法。

### 2. 14.2 偏离总清单（本目录的重构版，按层次合并）

| # | SQL 的现实 | 模型的要求 | 实测证据 🔧 | 修补状况 |
| --- | --- | --- | --- | --- |
| 1 | 表允许完全相同的两行 | 关系是元组**集合** | D1：`COUNT(*)` → `[(3,)]`；D1b `DISTINCT` → 2 行 | 未修（袋语义是刻意选择） |
| 2 | 头是**有序**列表，按位置匹配 | 头是属性集合 | D2：`UNION ALL` 把 `A(x,y)` 与 `B(y,x)` 并成 `[(1,2),(3,4)]`，列名 `['x','y']`；D10f 换列序得不同"表" | 未修（`*`、`NATURAL JOIN` 依赖名字，其余依赖位置，规则混用） |
| 3 | 每行有隐藏物理标识 | 元组无身份，只有值 | D1c：`rowid` 让两条相同行可区分；D3c：`WITHOUT ROWID` 表 `SELECT rowid` → `no such column: rowid` | 可绕（`WITHOUT ROWID`），但默认仍给 |
| 4 | 单元可放多个值（字符串列表 / JSON） | 1NF：单元恰好一个值 | D10d：`json_each` 把 `'["Paris","Rome"]'` 摊成 2 行才能查 | SQL:2016 JSON 路线＝承认问题并以嵌套化解（→ 第 15 章附录 D） |
| 5 | 没有零度关系（0 属性 0/1 元组） | `TABLE_DEE` / `TABLE_DUM` 是关系 | D4d：`Π_{}` 只能近似成 `COUNT` → `[(1,)]` / `[(0,)]`；D6：`SELECT 1` 仍带列名 `expr_0` | 缺位（→ 附录 B） |
| 6 | 值与变量不分（"表"两义） | 关系是值，relvar 是变量 | D10e：判断两个表相等要写双向 `EXCEPT` 计数 → `[(1,)]`；模型里就是 `r1 = r2` | 不可修（同一套语法既指当前值又指变量） |
| 7 | 更新是逐行原地修改 | 赋值是**整体替换**一个值 | A14：失败的 `DELETE` 整语句回滚（父 4 行、子 1 行都在），但成功路径仍是一行一行改 | 不可修；第 7 章替换语义在 SQL 里靠"语句级原子性"近似 |
| 8 | `MATCHING` 只有谓词形式，不是算子 | 结果应是可继续操作的关系 | D5b/D5c：`EXISTS`/`NOT EXISTS` → `[(S1,20,Paris),(S2,10,Rome)]` / `[(S3,40,Athens)]` | DuckDB 已语法化 `SEMI/ANTI JOIN`（✅ https://duckdb.org/docs/sql/query_syntax/select ） |
| 9 | 没有除法 | `r ÷ s` 是一等算子 | D5d：双重否定 + `DISTINCT` → `[('S4',)]`；D5e：漏 `DISTINCT` → 三行 `S4` | 未补（只能靠窗口/聚集绕） |
| 10 | `EXTEND` 降级为 SELECT 列表位置 | 派生列产生新关系，可上移复用 | 第 12 章：表达式不能出现在 `WHERE`/`GROUP BY`（求值顺序，11.8） | 产品各自给别名扩展，互不兼容 |
| 11 | 没有映像关系（子关系不是值） | 聚集作用在**子关系**上 | 第 12 章：空组聚集 `MIN/SUM` → `None`；`AVG` 不可组合 | 窗口函数补了计算，没补"值" |
| 12 | 3VL：互补谓词不划分关系 | 谓词二值，`p ∨ ¬p` 恒真 | D8c：全表 4 行、`ST = 20` 2 行、`NOT (ST = 20)` 1 行 ⇒ **2+1 < 4**；D8e 补 `OR ST IS NULL` 才是补集 | 不可修（`NULL` 的语义定义就是它） |
| 13 | `NOT` ≠ 集合差 | 差是补集运算 | D8f：`DELETE ... WHERE ST <> 20` 后 `NULL` 行留下 → `[('A',20,'Rome'),('B',None,'Rome'),('C',20,None)]` | 需纪律：比较旁必写 `IS NULL` 分支 |
| 14 | `CHECK` 遇 UNKNOWN 直接放过 | 约束要么成立要么不成立 | A7：`CHECK (V > 0)` 插入 `NULL` 成功、插入 `-1` 才报 `CHECK constraint failed` | 与 12 条同根；必须再写 `NOT NULL`（A6） |
| 15 | 外码含 NULL 即跳过检查 | 包含依赖逐元组成立 | A12：`('S1',NULL)`、`(NULL,'P1')`、`('S9',NULL)` 全被接受，只有 `('S9','P9')` 被拒 | 标准给了 `MATCH FULL/PARTIAL`（✅ sql1992.txt 19530 行 `<match type> ::= FULL | PARTIAL`），产品少实现 |
| 16 | 候选码不平等、码非必需 | 每个关系至少有一个码，码间无主次 | A11：`pragma_index_list('S')` → `[('sqlite_autoindex_S_1','pk',0)]`；D7f：`CREATE TABLE no_key(A,B)` 合法且可存重复行 | 不可修：SQL 里没有"码"这个概念，只有 PK/UNIQUE |
| 17 | 参照完整性依赖会话开关 | 模型的定义性成分不可关 | A1：`PRAGMA foreign_keys` → `[(0,)]`；A2 脏行入库；A3 开启后旧脏行仍在；A4 只能事后 `foreign_key_check` → `[('SP_off',1,'S',0)]` | 产品默认值问题，可修（新 SQLite 发行版可编译期默认开） |
| 18 | 没有断言 | 数据库级约束是一等声明 | A9：`CREATE ASSERTION ...` → `near "ASSERTION": syntax error`；✅ 但标准文本里 `<assertion definition> ::= CREATE ASSERTION <constraint name> <assertion check> [ <constraint attributes> ]`（sql1992.txt 22913 行） | 标准有、产品砍（→ 第 6/13 章）；PostgreSQL 至今未实现 |
| 19 | `CHECK` 禁子查询（比标准更严） | 谓词可引用任意关系 | A8：`subqueries prohibited in CHECK constraints`；✅ 标准侧只禁止「可能不确定」的查询：`6) The <search condition> shall not generally contain a <query specification> or a <query expression> that is possibly non-deterministic.`（sql1992.txt 第 20053–20055 行，`<check constraint definition>` 的语法规则） | 产品自缚，比标准还窄 |
| 20 | 没有域（类型 + 约束的可复用单元） | 类型公设（第 7 章） | 🔧 `CREATE DOMAIN ...` → `near "DOMAIN": syntax error`；A5：`INTEGER` 列里存进 `('abc', 3.14, NULL, 42)`，`typeof` 分别为 text/real/null/integer | PostgreSQL 实现了 `DOMAIN`；SQL 的声明类型普遍只是 affinity（🔧 A5、A12 的 `ARRAY` 假列） |
| 21 | 序被当成结果的一部分 | 关系无序 | D10：无 `ORDER BY` 时顺序是实现细节；D10b：`LIMIT 2` 无 `ORDER BY` → 非确定；D10c：SQLite 允许 `GROUP BY` 后裸列 → `[('S1','P1',2),...]` | 「展示层」问题，应从语言里剥离 |
| 22 | `GROUP BY` 与聚集绑在语法里而不是算子上 | 分类汇总 = 按属性集产生映像 + 对子关系聚集 | 第 5/12 章；🔧 `COUNT(*) FILTER (WHERE ...)` 与 `CASE` 写法一致 → `[('Athens',1),('Paris',2),('Rome',0)]` | SQL:2003 后逐步补齐语法，语义层次未变 |
| 23 | 视图写入的检查（`WITH CHECK OPTION`）与 `ALTER TABLE ADD CONSTRAINT` 普遍缺席 | 约束与定义同层次 | 🔧 两条都 `syntax error`（本目录 ch13b 实测：`near "WITH": syntax error`、`near "CONSTRAINT": syntax error`）；`CREATE VIEW ... WITH CHECK OPTION`（✅ sql1992.txt 50182 行）确在标准里 | 产品差异大（PostgreSQL/MySQL 支持，SQLite 不支持） |
| 24 | 相等随列而变（`COLLATE`） | 类型自带秩序与相等 | A20：同一行里 `WHERE A='S1'` → 1 行、`WHERE B='S1'` → 0 行 | 属"类型该有而 SQL 放在列上"的一族 |
| 25 | `ORDER BY` / `LIMIT` 直接作用于表 | 展示不是代数 | D10/D10b | 应属游标/接口层 |

### 3. 五个"能不能"的自检（把清单变成用法）

1. **能不能造出重复元组？** 能 ⇒ 不是关系（D1）。判据：任何"行数"结论都必须先说清 `DISTINCT` 口径。
2. **能不能观察列的顺序？** 能 ⇒ 头不是集合（D2、`UNION ALL` 不报名字冲突）。判据：接口层禁用 `SELECT *`。
3. **能不能对结果再用算子？** 只有包进子查询/CTE 才能 ⇒ 闭包不完整（第 4 章）。
4. **`NOT p` 是不是补集？** 有 NULL 就不是（D8c/D8e/D8f）。判据：写取反时同时决定 NULL 的归属。
5. **有没有不依赖会话开关的约束？** 没有 ⇒ 参照完整性不存在（A1–A4）。

这五条能答对，本章清单就可以不看；答不对，说明用的仍是"有表即关系型"的错觉（第 1 章的反面）。

### 4. 作者的结论与它常被误读的地方

⚠️ 依作者一贯立场转述（本节为其论证结构的重构，非原文）：**SQL 是关系完备的（能表达全部关系代数可表达的东西），但不是关系型的（其语义不是模型语义）。** 二者常被混为一谈——第 4 章的闭包与第 11 章的算子对应已经说明，关系完备性只保证"算得出"，不保证"算出来的东西还是关系、还能继续算"。

因此本章不是"SQL 批判"，而是**风险清单**：清单里每条偏离都对应一类具体故障——重复行对应错误的 `COUNT/AVG`；列序对应错误的 `UNION`；NULL 对应漏删漏查；断言缺失对应规则散落到应用层；外键开关对应静默脏数据。工程上真正省钱的不是换语言，而是**把每条偏离变成一条编码纪律**。

## 常见误区

| 误区 | 纠正 |
| --- | --- |
| 「SQL 有 bug 才不关系型」 | 重复行、列序、3VL、值/变量不分是**设计选择**，不是缺陷（清单 #1/#2/#6/#12） |
| 「关系完备 = 关系模型相容」 | 前者只保证表达能力，后者要求语义与类型系统（→ 第 4/7 章） |
| 「产品不支持 ASSERTION，所以是标准的锅」 | 反了：标准里 `<assertion definition>` 有正式语法（✅ sql1992.txt），是产品没实现 |
| 「SQLite 禁 CHECK 子查询 = 标准禁」 | 标准只禁"可能不确定"的查询（✅ 规则 6 原文）；SQLite 一刀切（🔧 A8） |
| 「有 PRIMARY KEY 就说明引擎承认码」 | 🔧 A11/D7f：只有 PK + autoindex + 隐藏 rowid，且无码也可建表 |
| 「`EXCEPT ALL`/`INTERSECT ALL` 已经让 SQL 支持袋语义了」 | 🔧 本目录实测 SQLite 3.45.3：`EXCEPT ALL` → `near "ALL": syntax error`（清单外的一条产品差异） |
| 「第 14 章是总结，可以先读它」 | 可以，但**清单没有说服力**：证据在前 13 章，尤其 02/04/06/11/12/13 |
| 「读完这章就懂关系模型了」 | 模型公设、类型产生器、`TABLE_DUM`/`TABLE_DEE` 与关系演算在第 7 章和附录（→ [15-附录TutorialD dum与dee集合论与关系演算.md](15-附录TutorialD dum与dee集合论与关系演算.md)） |

## 与其他章 / 其他书的联系

- 偏离逐项的出处：值/变量与头体 → [02-关系和关系变量.md](02-关系和关系变量.md)、[10-SQL基本表.md](10-SQL基本表.md)；算子与闭包 → [04-关系运算符Ⅰ.md](04-关系运算符Ⅰ.md)、[05-关系运算符Ⅱ.md](05-关系运算符Ⅱ.md)、[11-SQL操作符Ⅰ.md](11-SQL操作符Ⅰ.md)、[12-SQL运算符Ⅱ.md](12-SQL运算符Ⅱ.md)；NULL/3VL → [06-约束和断言.md](06-约束和断言.md)；公设与类型 → [07-关系模型.md](07-关系模型.md)；约束家族 → [13-SQL约束.md](13-SQL约束.md)；`DUM`/`DEE` 与演算 → [15-附录TutorialD dum与dee集合论与关系演算.md](15-附录TutorialD dum与dee集合论与关系演算.md)。
- 同一位作者把这份清单**做成可操作处方**的那一本（Date 第 1 本，SQL 视角）：[../SQL_and_Relational_Theory/13-全书常见误区与关系论清单.md](../SQL_and_Relational_Theory/13-全书常见误区与关系论清单.md)，NULL/3VL 深论 [../SQL_and_Relational_Theory/06-NULL与三值逻辑3VL.md](../SQL_and_Relational_Theory/06-NULL与三值逻辑3VL.md)、重复行处方 [../SQL_and_Relational_Theory/09-重复行DISTINCT与集合语义.md](../SQL_and_Relational_Theory/09-重复行DISTINCT与集合语义.md)、代数与封闭性 [../SQL_and_Relational_Theory/02-关系代数与封闭性.md](../SQL_and_Relational_Theory/02-关系代数与封闭性.md)。
- 学院口径（把 SQL 当"标准语言"讲，不列偏离清单）：[../数据库系统概念6/03-SQL.md](../数据库系统概念6/03-SQL.md)、[../数据库系统概念6/02-关系模型介绍.md](../数据库系统概念6/02-关系模型介绍.md)、[../数据库系统概念6/06-形式化关系查询语言.md](../数据库系统概念6/06-形式化关系查询语言.md)。
- 实现为什么会这样（偏离多半是存储/执行层的投影）：[../Database_Internals/01-简介与概览.md](../Database_Internals/01-简介与概览.md)、[../mysql/04-记录在页中如何存储.md](../mysql/04-记录在页中如何存储.md)、[../BuildYourOwnDatabaseFromScratch.md](../BuildYourOwnDatabaseFromScratch.md)。
- 非关系模型的对照（图模型不靠外码连接）：[../Graph_Databases_2e/00-总览与阅读地图.md](../Graph_Databases_2e/00-总览与阅读地图.md)。
- 深浅分工：清单里每一条「在真实引擎上代价多大」属实务书层——同波 [#23 `Cost_Based_Oracle_Fundamentals`](../Cost_Based_Oracle_Fundamentals/00-总览与阅读地图.md)（已落盘）；「按模型怎么设计才不会撞上这些偏离」属方法论层——同波 [#8 `Database_Design_and_Relational_Theory`](../Database_Design_and_Relational_Theory/00-总览与阅读地图.md)。

## 核心概念速览（中英对照）

- **偏离清单** — deviation list：把"SQL 不够关系型"从口号变成可核对的条目表（14.2）
- **关系完备 vs 模型相容** — relationally complete vs relational：能算出所有代数结果 ≠ 语义遵循模型
- **接口判据** — user interface test：判"关系型"只看用户可观察的语义（第 1 章）
- **袋语义** — bag semantics：允许重复行，SQL 与模型的第一处分野 🔧 D1
- **头的有序性** — ordered heading：列位置可观察，`UNION` 按位置匹配 🔧 D2
- **值/变量不分** — no value/variable distinction：同一个"表"既指当前值又指变量 🔧 D10e
- **闭包破裂** — broken closure：结果不能直接参与下一个算子（→ 第 4 章）
- **三值逻辑代价** — cost of 3VL：`p` 与 `NOT p` 不再划分关系 🔧 D8c
- **零度关系缺席** — absence of zero-degree relation：无 `TABLE_DEE`/`TABLE_DUM` 🔧 D4d/D6
- **约束的可关性** — switchable constraints：FK 依赖会话开关 ⇒ 事实上不存在 🔧 A1
- **断言缺席** — missing assertions：跨关系规则只能靠触发器/外部检测 🔧 A9/A10
- **域缺席 / affinity 冒充类型** — no domains：声明类型只是存储倾向 🔧 A5
- **展示层污染** — presentation in the language：`ORDER BY`/`LIMIT` 被当成关系操作 🔧 D10
- **合规分级** — conformance tiers（Entry/Intermediate/Full）：标准自己允许部分实现 ✅ sql1992.txt

## 最新演进与工业实践

- **标准侧（2016 → 2023）**：SQL:2016 起补 JSON 与属性图查询（PGQ），SQL:2023 把 JSON 表函数正规化（⚠️ 转述，未取得正式文本）。方向很清楚——**修补的是"非原子单元"和"嵌套"这一族（清单 #4），没有一条触碰 #1/#2/#6/#12**：袋语义、列序、值/变量不分、3VL 至今原样保留。本书 2012 年的清单因此仍然有效。
- **产品侧的分化（本目录可实测的只有 SQLite）**：清单 #17/#18/#19/#20/#23 的落地程度差异极大——PostgreSQL 有 `DOMAIN`、`WITH CHECK OPTION`、`EXCLUDE`；MySQL 8.0.16+ 强制 `CHECK`；SQLite 全都没有但给了部分唯一索引与 `DEFERRABLE`（🔧 A15/A18）。⚠️ Oracle/DB2/SQL Server 的断言与域支持未在本目录核实，只作转述性说明。
- **新派引擎把清单当"需求单"**：DuckDB 支持 `SEMI`/`ANTI JOIN` 语法、`LIST/STRUCT` 显式嵌套类型、`ASOF JOIN`（✅ https://duckdb.org/docs/sql/query_syntax/select ）；其取舍等于承认 #4（嵌套）比 #1（重复行）更值得支持——它同样保留袋语义。关系代数正统路线的当代实现仍是 Tutorial D/Rel 一系（→ [15-附录TutorialD dum与dee集合论与关系演算.md](15-附录TutorialD dum与dee集合论与关系演算.md)）。
- **工业实践的三条硬纪律（每条对应清单一项）**：① 接口层禁止 `SELECT *` 与按位置消费结果（#2）；② 任何"取反"查询显式处理 `NULL`（#12/#13，🔧 D8e 是唯一正确写法）；③ 外键/约束在每个连接初始化时显式开启并纳入测试断言（#17，🔧 A1/A4）。
- **一键复现**：本章表格里的 D 系列证据可由 `D:\develops\tmp\dbwave_rtcp\rg_sqlite_demo.py` 一次跑完（输出 `demos.txt`），A 系列由 `ch13_extra.py` 跑完（输出 `ch13_out.txt`）；标准原文取证为同目录 `sql1992.txt`（本次 `curl` 200 实抓，50794 行）。**repo 内零构建产物。**
- **深浅分工回顾**：本目录（#12）= 清单与判据；[../SQL_and_Relational_Theory/00-总览与阅读地图.md](../SQL_and_Relational_Theory/00-总览与阅读地图.md) = 每条偏离在 SQL 里怎么写才对；同波 [#8 `Database_Design_and_Relational_Theory`](../Database_Design_and_Relational_Theory/00-总览与阅读地图.md) = 怎么设计才不会撞上清单；[#23](../Cost_Based_Oracle_Fundamentals/00-总览与阅读地图.md)/[#45](../Efficient_MySQL_Performance/00-总览与阅读地图.md)/[#87](../Using_SQLite/00-总览与阅读地图.md) = 真实引擎上的代价与运维（均已落盘，波尾闭环）。
