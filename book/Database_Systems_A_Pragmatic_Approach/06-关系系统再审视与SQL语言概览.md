# 06 关系系统再审视与 SQL 语言概览（原书第 9–10 章）

> 书目：《Database Systems: A Pragmatic Approach》，Elvis C. Foster & Shripad V. GodBole，Apress 2014，章 DOI `…_9`（pp.163–168）/ `…_10`（pp.171–175）。
> 证据级：章题/页码/DOI ✅ Crossref 一手；两章首段 ✅ Springer 摘要逐字；展开 ⚠️ 重构；🔧 为 SQLite/DuckDB 实测类比，**非本书引擎行为**。

## 1 本章定位

两枚"过场枢纽章"（各 5–6 页）：ch9 给关系模型一段理论收官陈词，ch10 把接力棒交给 SQL——本书由此进入篇幅最重的 Division 三（SQL 实操，Oracle 10g 方言，✅ ch11/16 摘要互证）。

## 2 ch9 内容主讲：Relational System — a Closer Look

首段逐字（✅）：

> "We have covered much ground in our study of database systems. We have also established the importance of the relational model and its significant contribution to the field of database systems. We now pause to conduct a more enlightened discussion of this contribution…"（截断）

⚠️ 重构（6 页体量决定其为评论式短文）：

- **关系模型贡献清单**：数据-程序分离（对 ch2 数据独立性的回收）、声明式语言、数学可优化性（ch5/7 的回收）。
- **局限的预告**：对复杂对象/递归查询的先天不便——为 ch15《Some Limitations of SQL》和 ch23《Object Databases》留出接缝（✅ ch15 摘要确证"然而像所有语言一样，SQL 有局限"的框架）。
- 可能的"从模型到产品"过渡段（引出 SQL 诸实现）。

## 3 ch10 内容主讲：Overview of SQL

首段逐字（✅）：

> "The Structured Query Language (SQL) has become the universal language of choice for DBMS products. A study of this language is therefore imperative for the student of computer science or computer information systems. This and the next few chapters will help you…"（截断）

⚠️ 重构 + 常识时间线（教材惯例）：

- **谱系**：Codd 关系模型（1970）→ IBM SEQUEL（Chamberlin/Boyce 一脉，1970s 初）→ SQL-86/89（ANSI/ISO）、SQL:1992、SQL:1999（对象/递归）、SQL:2003/2008（窗口）——本书印刷止于 SQL:2008 时代口径。
- **三分部类**：DDL（→ch11）/DML（→ch12）/DCL+控制语句（→ch13/14 语境），以及"SQL 非纯粹关系代数语言"的提醒（bag 语义、ORDER BY 破序）。
- **方言声明**：本册实现基于 Oracle 10g（✅ ch11/ch16 摘要），差异点到 ch16–19 概览回收（⚠️ 组织推断）。

## 4 🔧/⚠️ 实测与类比

- **方言差异现场（非本书引擎）**：E1——SQLite `INSERT 'abc' INTO INTEGER 列` 照收（`typeof`→'text'）；E2——DuckDB 同款直接 `ConversionException`；Oracle 系（本书主线 ⚠️）会报类型错——"同一 SQL 三种答案"是 ch10"方言"论最便宜的教学道具。
- **bag vs set**（E3）：`SELECT count(*), count(DISTINCT did)` 双计数演示 SQL 默认不集化；DISTINCT/EXCEPT 是"回到关系代数"的语法桥。
- **ORDER BY 破序**（E4 EQP 输出）：`SCAN→SEARCH USING INDEX` 计划变化不改结果序承诺——索引序≠输出序，本册 ch17 附录 B 树的工程回声。

## 5 对位阅读（实链，已验名）

- [../Databases_Illuminated_4e/04-SQL基础-DDL与DML.md](../Databases_Illuminated_4e/04-SQL基础-DDL与DML.md)：同代教材把本册 ch10–12 合并压缩的对照。
- [../SQL_and_Relational_Theory/12-语言教程TutorialDees与SQL对照.md](../SQL_and_Relational_Theory/12-语言教程TutorialDees与SQL对照.md)：另一种"先理论后 SQL"的激进版编排。
- [../Using_SQLite/01-SQLite概述.md](../Using_SQLite/01-SQLite概述.md)：嵌入式方言视角（本书无此产品，2026 必读补位）。
- [../Database_Tuning/01-基本原则.md](../Database_Tuning/01-基本原则.md)：把"SQL 是性能的黑箱"翻成 tunable 世界观。

## 6 教学与实操要点

1. ch9/10 合读法：前者的"贡献/局限"清单直接当后者的 SQL 特性检查表用。
2. 给同学讲清三层：**模型（关系代数/演算）—语言（SQL 标准）—产品（Oracle/…）**——本书 29 章有一半在为这三层的归属吵架提供素材。
3. 标准年代感自查：2014 教材停在 SQL:2008；今天任何主流引擎实际支持面≈SQL:1999+SQL:2003 窗口+SQL:2016 子集，2026 新事是 SQL:2023 属性图（本书世界观无法想象 ⚠️）。

## 7 深挖与自测

### 概念辨析十问
1. ch9 贡献清单与 ch15 局限清单什么关系？——同一枚硬币：声明式收益 vs 程序性代价。
2. SQL 是关系语言吗？——不纯：bag 语义+ORDER BY+方言扩展；"关系化子集"才对应代数。
3. SEQUEL 与 SQL 字母梗背后哪家机构？——IBM 原型期（教材通史口径 ⚠️）。
4. "universal language of choice"（✅ 摘要）的 2026 反例？——DataFrame API/文档 DSL；但即席分析面 SQL 仍胜。
5. DDL/DML/DCL 三分之外谁管事务？——习惯单列 TCL（本册未标 ⚠️ 术语惯例）。
6. 方言差异最大的一层？——类型系统与 DDL 扩展对象（同义词/表空间，ch11 实证）。
7. 教材为何强调 SQL 非程序语言？——图灵不完备（无原生循环/过程）；补丁=游标/PL/递归 CTE。
8. 标准化时间线 2014 讲到哪？——引用口径至 SQL:2008 一代；SQL:1999 递归/类型是常考界碑。
9. "先模型后语言"的教学顺序价值？——见 `SELECT *` 条件反射问"这是关系吗"。
10. Division 三=ch11–14 的证据？——ch15 摘要 "chapters 11 14" 逐字（10 号已钉）。

### 常见误区六条
- 把 SQL 标准当产品手册——骨架在标准，血肉全在方言。
- 认为 ORDER BY+LIMIT 到处同义——Oracle 10g 用 ROWNUM 分页（⚠️ 代差典型）。
- 用 SELECT DISTINCT 修 JOIN 扇出——治标（重复）掩盖键缺失（治本）。
- 忽视 EXPLAIN 文本不可移植——概念可迁移，语法各引擎独有。
- 把窗口函数当"高级货"——2003 已入标准、开源双引擎皆可用（E3）；不会才是落后。
- PL/SQL 混进 SQL 讲——过程语言扩展；"能 SQL 不 PL"是分层原则。

### 🔧 加餐：三问三跑（30 秒，非本书行为）
- 域去哪了：E1 typeof vs E2 ConversionException。
- 集合去哪了：E3 count(*) vs count(DISTINCT did)。
- 序在哪：E4 SCAN→SEARCH 不改 ORDER 承诺。

### 一分钟版
- ch9=理论收官陈词，ch10=语言交接仪式。
- 记住三层：模型—标准语言—产品方言，本书把三层钉死在 Oracle 10g 上授课。
- Division 三由此启程（ch11–14）。

## 8 术语快卡与跨书对位

| 术语 | EN | 一句话定位 |
|---|---|---|
| ISAM | Indexed Sequential Access Method | 索引顺序访问：关系模型之前的世界 |
| 层次模型 | Hierarchical Model | 树状父子链接，IMS 血统 |
| 网状模型 | Network Model | 记录互连成网，CODASYL 血统 |
| SQL 三层 | SQL Sublanguages | DDL/DML/DCL 分工（第 11–13 章） |
| SELECT 骨架 | SELECT-FROM-WHERE | 查询的基本形 |

**跨书对位（盘上已验证目录）**：
- 参 [Databases Illuminated 4e](../Databases_Illuminated_4e/00-总览与阅读地图.md)：旧模型史叙述可互校。
**速测**：合上书，说出 SQL 赢过关系代数实现的两条工程理由。

**速测**：合上书，用一句话向同事讲清本册最难的概念；讲不清就回到 §7 误区清单重读。

**快验证问答（补）**

- Q：ISAM 的根本痛点？A：访问路径写死，查询方式一变就重建。
- Q：层次/网状为何败于多对多？A：路径单一，被迫复制数据或手工挂指针。
- Q：SQL 声明的是什么？A：要什么，而不是怎么取。

## 核心概念速览（中英对照）

| 中文 | English | 一句话 |
|---|---|---|
| 数据独立性 | data independence | 关系模型头号贡献（ch2 伏笔回收） |
| 声明式语言 | declarative language | 说 what 不说 how |
| SEQUEL→SQL | SEQUEL to SQL | IBM 1970s 起源线 |
| DDL/DML/DCL | data definition/manipulation/control language | SQL 三分部类 |
| 方言 | dialect | 标准与产品之间的鸿沟（本册=Oracle 10g） |
| bag 语义 | bag/list semantics | SQL 默认不集化 |
| SQL 标准化年代 | SQL-86/89/92/99/2003/2008/2016 | 时间线即教材边界 |

## 最新演进与工业实践

- **SQL 标准的 2026 现场**：ISO/IEC 9075 系列推进到 SQL:2023（属性图查询 LPG/MG）——"universal language"论断依然成立但战场移到云仓（Snowflake/BigQuery/Databricks 各自方言化），✅ 概念锚点 https://docs.snowflake.com/en/user-guide/intro-key-concepts（200 验真）。
- **开源双雄补位**：本书无 PostgreSQL 专章；2026 学院/工业默认第三极，✅ https://www.postgresql.org/docs/current/sql-createschema.html（200）。
- **嵌入式 SQL 的逆袭**：SQLite/DuckDB 让"DBMS 产品"一词从服务端独占变为进程内可选——E1/E2 那组"同一 SQL 三种答案"实验正是这场变迁的最小标本。
- 盘上纵深的读法：SQL 内核视角 [../Database_Internals/01-简介与概览.md](../Database_Internals/01-简介与概览.md)；调优世界观 [../Database_Tuning/02-调优内核.md](../Database_Tuning/02-调优内核.md)。
