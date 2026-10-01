# 10 系统目录与 SQL 的局限（原书第 14–15 章）

> 书目：《Database Systems: A Pragmatic Approach》，Elvis C. Foster & Shripad V. GodBole，Apress 2014，章 DOI `…_14`（pp.279–289）/ `…_15`（pp.291–297）。
> 证据级：章题/页码/DOI ✅；两章首段 ✅ 摘要逐字；展开 ⚠️ 重构；🔧 为 SQLite/DuckDB 实测，**非本书引擎（Oracle 10g）行为**。

## 1 本章定位

Division 三收尾双章：ch14 揭"DBMS 的账本"（系统目录/数据字典），ch15 泼"语言的冷水"（SQL 局限）。两首段逐字（✅）：

> ch14: "Every reputable DBMS contains a system catalog (also called the data dictionary) of some form. This has been alluded to several times earlier in the course. This chapter discusses this very important component of the database system. The chapter proceeds under the…"
> ch15: "As can be seen from chapters 11 14, SQL is a very powerful programming language, ideally suited for the management of databases. However, like all languages, SQL has limitations. This chapter briefly examines some of these limitations. The chapter proceeds as…"

ch15 的"chapters 11–14"字样一手确证 **Division 三=ch11–14 四章**（DDL/DML/视图安全/目录），本册 SQL 部类边界就此钉死（✅ 推断升级）。

## 2 ch14 内容主讲（⚠️ 目录学教材口径重构）

- **目录里存什么**：表/列/类型/约束/视图定义/索引/权限/统计信息的元数据——"DBMS 里所有 DDL 的最终归宿"。
- **怎么查**：Oracle 数据字典视图（`USER_TABLES/USER_TAB_COLUMNS/…` 风格，⚠️ 本册具体列举无逐字证据）+ 只读纪律（字典由引擎自维护，DBA 不手写）。
- **目录与三模式架构**：概念/外部视图的定义都登记于此——ch2 数据独立性论述的物证层。
- **自举问题**（目录描述自身）：一句带过的课堂彩蛋。

## 3 ch15 内容主讲（⚠️ 局限清单重构，锚="like all languages"）

- **程序性短板**：SQL 非通用语言——循环/分支/变量需游标或过程语言（Oracle PL/SQL；本册 ch11 已把 function/procedure 列为高级对象，此处回收 ⚠️）。
- **集合与顺序的裂缝**：bag 语义与关系集合语义的差（DISTINCT/EXCEPT 手动补）；ORDER BY 破坏关系无序性。
- **NULL 与三值逻辑**：`=NULL` 不成立、聚合中 NULL 蒸发、NOT IN 子查询遇 NULL 全空——最经典的 SQL 局限（与 ch8"须始终铭记"呼应 ⚠️）。
- **表达力缺口**：递归查询在 SQL:1999 前不可写（Oracle 靠 CONNECT BY 方言）；图/层次遍历的笨拙。
- **schema 演化与对象/复杂类型**：改结构之痛+嵌套集合支持之弱——直接为 ch22/23 分布式与对象章开门。

## 4 🔧 目录与局限的实测化（非本书行为）

- **目录可查性对照（E6）**：SQLite=`sqlite_master`（type/name/sql 三列，视图 DDL 原文逐字在册）+`PRAGMA table_info(emp)` 出四列+`PRAGMA index_list(t)` 出 `(0,'ix',0,'c',0)`（origin='c' 即 created）；DuckDB=`duckdb_tables()`/`duckdb_views()`/`duckdb_columns()`（列含 `is_nullable`）/`duckdb_functions()` 计数 **2948**。三种世界三种字典：SQLite 极简一表、DuckDB 现代多视图、Oracle 字典视图家族（⚠️ 转述）。
- **自举现场（E6）**：`sqlite_master` 自身不列在 `sqlite_master`（临时库）——"目录描述自己"的直接体感样本。
- **写保护彩蛋（E6c）**：`PRAGMA writable_schema`→0：默认锁死目录直写，开它=自毁程序启动器——工程口径的最佳反面教材。
- **局限逐条实测**：递归（SQL:1999）——`WITH RECURSIVE` 在 SQLite 3.45.3 可造 50 万行（E7），验证"现代开源引擎已补齐 ch15 抱怨"；NULL 三值——`WHERE i=NULL` 恒假、`IS NULL` 唯一解（E1/E4 查询中顺手可复现）；过程性——E8b 双引擎 ATTACH+触发器混合演示"引擎外补程序性"。

## 5 对位阅读（实链，已验名）

- [../Oracle_Essentials_5e/05-数据字典与动态性能视图.md](../Oracle_Essentials_5e/05-数据字典与动态性能视图.md)：本册 ch14 的正统 Oracle 深化（波7 #44 册，字典视图家族实貌）。
- [../Pro_SQL_Server_Internals/03-统计信息.md](../Pro_SQL_Server_Internals/03-统计信息.md)：目录中"统计信息"一格的内幕放大（E4 sqlite_stat1 的对照豪华版）。
- [../SQL_and_Relational_Theory/06-NULL与三值逻辑3VL.md](../SQL_and_Relational_Theory/06-NULL与三值逻辑3VL.md)：ch15 NULL 段的严格化（含 42/2/Placeholder 语义）；其 09 补 bag/DISTINCT 纠偏。
- [../Using_SQLite/07-建表约束与Pragmas.md](../Using_SQLite/07-建表约束与Pragmas.md)：PRAGMA=SQLite 目录接口的设计语境。

## 6 教学与实操要点

1. "会查目录"是本章唯一必须带走的手艺：Oracle `ALL_TAB_COLUMNS`、PG/MySQL `information_schema`、SQLite `sqlite_master`、DuckDB `duckdb_columns()`——四套入口一个概念。
2. ch15 的局限清单在今天要加一条**新局限**：SQL 无原生版本化/血缘表达（审计靠外物）——用本册框架自然生长出的 2026 注脚。
3. 递归 CTE 教学模板=E7 造数（`WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i+1 …)`），50 行内讲完"SQL 图灵不完备但够用"。

## 7 深挖与自测

### 概念辨析十问
1. 目录为什么"由 DBMS 自维护"？——DDL 落笔即目录改写；人直写=一致性灾难（🔧writable_schema 默认 0，E6c）。
2. 字典 vs 目录是两物吗？——同物异名（✅ 摘要并名 data dictionary）；Oracle 习惯"字典+视图家族"。
3. 目录里最少存哪三类？——对象定义（表/列/视图）、约束与索引、统计信息（+权限）。
4. 统计信息何时"骗"优化器？——陈旧直方图；E4 的 ANALYZE→sqlite_stat1 '3 2 1' 即喂食仪式。
5. ch15 的第一条局限？——程序性：循环/分支/异常外求（游标/PL/宿主语言）。
6. 递归缺口的解药时间线？——SQL:1999 递归 CTE；Oracle 更早方言 CONNECT BY（⚠️ 转述）；🔧E7 实测可用。
7. NULL 系局限一句话？——三值逻辑污染比较/聚合/NOT IN 三处（E3/E7 顺手可复现）。
8. bag 语义带来什么工程债？——DISTINCT 税+重复行审计+键不自动（回收 ch2/3）。
9. 模式演化之痛指什么？——ALTER 受限/迁移窗口/兼容读写并存（🔧E2 的 ADD CONSTRAINT 拒是切片）。
10. 2026 该给局限清单加哪条？——版本化/血缘/时态语义在 SQL 内无第一等表达。

### 常见误区六条
- 把目录当摆设——排障第一步永远是查目录（表定义/索引是否存在/统计是否新鲜）。
- 手写 INSERT 进系统表——多数引擎禁止或危险（SQLite 需 writable_schema=1，反面教材）。
- 以为视图定义改了依赖自动安全——需重查权限面（回收 ch13）。
- SQL 局限=性能差——局限是表达力维度；性能属物理设计（ch17/19 语境）。
- 有了递归 CTE 就全能——复杂过程仍应上宿主语言（本册"像所有语言"框架）。
- 忽略目录的方言面——四引擎入口各名（E6/§2 ⚠️ 转述），可移植的是概念不是表名。

### 🔧 加餐：目录四入口速记（非本书行为）
- SQLite：sqlite_master 单表+PRAGMA table_info/index_list（E6）。
- DuckDB：duckdb_tables()/views()/columns()/functions()=2948（E6/E6e）。
- 概念统一：对象×列×约束×统计四栏，谁家都一样。

### 一分钟版
- ch14=账本（目录），ch15=冷水（局限）；一热一冷收束 Division 三。
- 带走手艺：四套目录入口+NULL/递归/bag 三件局限警觉。

## 8 术语快卡与跨书对位

| 术语 | EN | 一句话定位 |
|---|---|---|
| 系统目录 | System Catalog | 引擎自带的"关于自己的表" |
| INFORMATION_SCHEMA | 标准信息模式 | SQL 标准目录视图 |
| 嵌入式 SQL | Embedded SQL | 宿主语言内写 SQL（本书用 Delphi） |
| 动态 SQL | Dynamic SQL | 运行期拼串执行——注入温床 |
| 游标 | Cursor | 逐行消费结果集的旧接口 |
| 三值逻辑 | Three-Valued Logic | TRUE/FALSE/UNKNOWN 与 NULL 共舞 |

**跨书对位（盘上已验证目录）**：
- 参 [DuckDB_in_Action]：现代引擎同样靠目录+扩展点组织自身。
**速测**：合上书，解释 NOT IN 遇 NULL 为何整体落空。

**速测**：合上书，用一句话向同事讲清本册最难的概念；讲不清就回到 §7 误区清单重读。

**快验证问答（补）**

- Q：表与列的定义存哪？A：系统目录表里的行。
- Q：SQL 注入的根治？A：参数化/预编译，而非转义。
- Q：SQL 缺什么才非图灵完备？A：通用递归与循环控制，需宿主语言补。

## 核心概念速览（中英对照）

| 中文 | English | 一句话 |
|---|---|---|
| 系统目录/数据字典 | system catalog / data dictionary | 元数据的元数据库（✅ 摘要并名） |
| 元数据 | metadata | 描述数据的数据 |
| 自举 | bootstrapping | 目录如何描述自己 |
| 统计信息 | statistics | 优化器的眼睛（sqlite_stat1/DBMS 直方图） |
| 三值逻辑 | three-valued logic (3VL) | NULL 使真值多出 Unknown |
| 过程性缺口 | procedural gap | 循环/分支要外求（游标/PL） |
| 递归查询 | recursive query | SQL:1999 后 CTE 可写（🔧实测） |
| bag 语义 | bag semantics | 重复行/ORDER BY 的病根之一 |

## 最新演进与工业实践

- **字典→目录服务→元数据平台**：information_schema/pg_catalog 之外，2026 的"系统目录"外扩为开放元数据（Iceberg REST Catalog）+数据目录产品——盘上续读 [../Data_Engineers_Guide_to_Microsoft_Fabric](../Data_Engineers_Guide_to_Microsoft_Fabric/00-总览与阅读地图.md) 所在治理线（波9 #191 册）与 [../The_Data_Lakehouse/08-数据湖仓中的数据集成.md](../The_Data_Lakehouse/08-数据湖仓中的数据集成.md)（grep 验名）。
- **NULL 语义的终局**：SQL:2023 仍未"治好"3VL，工业答案转向类型系统（半类型/Option 类型）与质量框架（大交换断言）——ch15 那条局限常青。
- ✅ 现代字典入口双锚：https://www.postgresql.org/docs/current/sql-createschema.html（200）与 https://www.sqlite.org/lang_createview.html（200）。
- 🔧 一句话复现本章全部目录断言：`SELECT * FROM sqlite_master` / `SELECT * FROM duckdb_columns()`（3.45.3/1.5.5，非本书引擎）。
