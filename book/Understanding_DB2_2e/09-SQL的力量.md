# 09 SQL 的力量（原书第 9 章 Leveraging the Power of SQL ✅ 题逐字）

> 本章为精读重构：SQL 语法行为「⚠️ 转述」；语源史叙述以公开技术史共识为据（不贴未验证 DOI）。这是全目录"历史感"最重的一章。

## 章图与图描述（视觉向开场）

- **图 9-A「SQL 能力分层金字塔」**（描述）：塔基=CRUD/连接/子查询，塔身=聚合/GROUPING SETS/OLAP 窗口，塔尖=CTE/递归/MERGE/SQL PL——原书用逐层配例的方式讲"你以为你会的 SQL 只到塔基"。
- **图 9-B「JOIN 韦恩图族」**（描述）：内连接/左外/全外/交叉/自连接五图并排，每图下配一行示例结果表；"ON 与 WHERE 在外连接下的语义差"用高亮框单列。
- **图 9-C「递归 CTE 展开示意」**（描述）：员工-经理组织树 + WITH RECURSIVE 的"种子/递归/合并"三段流水线小图——本章技术含量的封面图。
- **图 9-D「结果集对比截图」**（描述）：同一需求"朴素写法 vs 窗口函数写法"两网格截图并排，行数一致但列多了 RANK/ROWNUMBER——"少写自连接"的收益可视化。

## 原书章骨架 → 本文件对位（⚠️ 推定主题域）

| 推定主题域 | 本文件小节 |
| --- | --- |
| 查询基础与连接全家 | 精讲 1 |
| 子查询家族 | 精讲 2 |
| CTE 与递归 | 精讲 3 |
| 聚合进阶/OLAP 窗口 | 精讲 4 |
| MERGE 与 DML 组合拳 | 精讲 5 |
| SQL PL 程序性扩展 | 精讲 6 |
| 语源史与标准影响 | 精讲 7 |

## 核心精讲

### 1. 连接全家福（⚠️ 转述）
INNER/LEFT/RIGHT/FULL/CROSS/自连接；显式 JOIN 语法优先于逗号老式（优化器等价、人读不等价）；外连接的 ON 谓词保留"补 NULL 行"，WHERE 再过滤会把外连接打回内连接——SQL 圈千年老坑，各厂同坑。

### 2. 子查询家族（⚠️ 转述）
标量/行表/EXISTS 半连接、相关子查询与 LATERAL 前夜语境（⚠️ 9.5 无 LATERAL 口径）；IN (大列表) 的谓词展开成本账在 [15](15-性能与问题诊断.md) 优化器语境回收。

### 3. CTE / 递归查询：DB2 的招牌贡献（⚠️ 转述+史实）
WITH 公用表表达式与 WITH RECURSIVE 由 IBM 研究院在 System R 后续产品线上率先落地（DB2 V8 世代表述为"CTE/递归查询先行者"——社区/作者谱系常引，标准 SQL:1999 收录 ⚠️ 年代口径以通史为据），组织树/闭包/图遍历一函数打通；本目录理论对位：[../数据库系统概念6.md](../数据库系统概念6.md) 递归查询章 + 盘上专文 [../../db/SQL_CTE.md](../../db/SQL_CTE.md)（repo 论文线既有条目，✅ 存在）。

### 4. 聚合进阶与 OLAP 窗口（⚠️ 转述）
GROUP BY/HAVING 之上：**GROUPING SETS/CUBE/ROLLUP**（同为 IBM 系先行、后入标准的多维聚合）；窗口函数族 ROW_NUMBER/RANK/DENSE_RANK/OLAP 聚合+OVER(PARTITION BY/ORDER BY/ROWS|RANGE)、框架子句——报表 SQL 的发动机；FETCH FIRST n ROWS ONLY 的极限语义（无 ORDER 时行不定 ⚠️）。

### 5. MERGE：一条语句的 UPSERT（⚠️ 转述）
USING 源表 WHEN MATCHED THEN UPDATE/INSERT 的分流语义；数仓装载与快照对账的主力（联动本目录 E1 统计/对账语境的 🔧 思维，见 [12](12-并发锁与数据维护.md)）。MERGE 亦是 DB2 首倡、SQL:2003 采纳的语法之一（⚠️ 年代口径通史）。

### 6. SQL PL：库内程序性（⚠️ 转述）
CREATE PROCEDURE/FUNCTION/TRIGGER 用 SQL PL 复合语句（BEGIN...END、LOOP、SIGNAL）——DB2 的 SQL 例程语言被社区认为是 PL/SQL 之外"过程化扩展入标准"（SQL/PSM）的主要源头之一（⚠️ 谱系表述取通史口径）；调用面 CALL/SELECT 函数列。

### 7. 语源史小结：为什么这章值得单独写
CTE/递归、GROUPING SETS、MERGE、SQL/PSM 四条线都指向同一现象：**标准 SQL 的许多"新语法"是 DB2 先跑几年再收编**。盘上论文线入口 [../../db/db.md](../../db/db.md)、System R/SQL 史话可回扣 [../Database_Design_and_Relational_Theory/00-总览与阅读地图.md](../Database_Design_and_Relational_Theory/00-总览与阅读地图.md) 的关系理论语境（异侧面）。

## 常见误区

1. "窗口函数=分析型专属"——去重/分页/TopN 在 OLTP 同样高频（DB2 用 ROW_NUMBER 破 LIMIT 缺失时代的老技巧）。
2. "MERGE 就是 UPDATE+INSERT"——单语句原子+幂等设计意图完全不同（装载对账语境）。
3. "外连接条件放哪都行"——ON/WHERE 语义差是经典事故（精讲 1）。
4. "递归 CTE 当循环写"——终止条件与展开深度失控，各厂同坑（SQLite 的 WITH RECURSIVE 行为见 🔧 声明）。

【微讲堂】本章四件套一屏（示意，⚠️ DB2 语法口径转述）：

```text
WITH RECURSIVE tree AS (种子: 顶层行 UNION ALL 递归: JOIN 父子)
SELECT ... FROM tree GROUP BY GROUPING SETS ((a),(a,b),());
MERGE INTO tgt USING src ON k=k
  WHEN MATCHED THEN UPDATE ... WHEN NOT MATCHED THEN INSERT ...;
SELECT *, RANK() OVER (PARTITION BY dept ORDER BY sal DESC) rk FROM emp;
```

## 🔧 类比说明（语法面通用演示挂 12 章）
SQL 语法的"能跑验证"分散两处：CTE/窗口/MERGE 变体在 SQLite 3.45.3 可跑（SQLite 无原生 MERGE，用 INSERT OR + UPSERT 子句对照——**非 DB2 语法**）；对账类实验并入 [12](12-并发锁与数据维护.md) 的 E1/E3。本章不另设实验防重复计数。

## 与其他章/其他笔记的联系

- 上游：对象与约束 → [07](07-数据库对象.md)；下游：谓词与访问路径 → [15](15-性能与问题诊断.md)；MQT 改写依赖聚合形态 → [07](07-数据库对象.md)/[15](15-性能与问题诊断.md)。
- 异厂对照：连接优化的跨厂通识 → [../Cost_Based_Oracle_Fundamentals/10-连接基数估算.md](../Cost_Based_Oracle_Fundamentals/10-连接基数估算.md)、连接算法三章群（11–13）；MySQL 侧子查询 → [../Understanding_MySQL_Internals/09-解析器与优化器.md](../Understanding_MySQL_Internals/09-解析器与优化器.md)；SQL 通识 → [../SQL沉思录.md](../SQL沉思录.md)、[../SQL经典实例.md](../SQL经典实例.md)（盘上单文件 ✅）。

## 章末自查（对位原书复习题的"看图作答"法）

1. 外连接 ON/WHERE 语义差举一个反例结果。
2. 递归 CTE 三段式（种子/递归/合并）各写一句。
3. RANK/DENSE_RANK/ROW_NUMBER 在并列值上的分叉？
4. MERGE 的 WHEN 两支覆盖什么装载场景？
5. GROUPING SETS 与 CUBE/ROLLUP 的包含关系？
6. 本章四条"DB2 先行"语法线与标准收编年份口径？
7. SQL PL 与社区"过程化 SQL"的谱系关系一句。

## 语源速查表（⚠️ 年代取通史口径）

| 语法 | DB2 先行落地 | 标准收编 | 今天谁都有 |
| --- | --- | --- | --- |
| CTE/递归 | V8 世代 | SQL:1999 | PG/SQL Server/SQLite/DuckDB |
| GROUPING SETS | 9 世代 | SQL:2003 谱系 | 主流厂 |
| MERGE | V8 世代 | SQL:2003 | 多数（SQLite 用 UPSERT 变体） |
| SQL/PSM | SQL PL | 标准 PSM | 各厂方言例程 |

## 本章黑话三句

- "打塔基" = 只会 CRUD；"上塔身" = 窗口/多维聚合。
- "分流" = MERGE 的 MATCHED 语义。
- "展开" = 递归 CTE 的迭代过程。

## 核心概念速览（中英对照）

1. **CTE** — Common Table Expression: WITH 引入的命名结果集。
2. **递归 CTE** — Recursive Query: 种子+递归+合并的树/闭包写法。
3. **GROUPING SETS** — 多分组集聚合: CUBE/ROLLUP 的一般式。
4. **窗口函数** — OLAP Windowing: OVER(PARTITION/ORDER/FRAME)。
5. **RANK/DENSE_RANK/ROW_NUMBER** — 排名三兄弟: 并裂名次/不并裂/顺号。
6. **MERGE** — 合并语句: MATCHED/NOT MATCHED 分流 upsert。
7. **FETCH FIRST** — 极限语义: n 行截断（无排序则不确定序）。
8. **相关子查询** — Correlated Subquery: 引用外层行的内查询。
9. **EXISTS 半连接** — 存在性判断: 短路式返回。
10. **SQL PL** — SQL Procedural Language: 库内过程化例程语言。
11. **SIGNAL** — 显式告警: SQL PL 中抛条件/异常。
12. **INSTEAD OF** — 视图写路由: 与 07 章对象面呼应。
13. **SQL/PSM** — Persistent Stored Modules: 标准程序化 SQL（DB2 系源头之一 ⚠️）。
14. **LATERAL** — 侧向连接: 9.5 无、后代 SQL 标准补的位（对照记忆）。

## 最新演进与工业实践

- **标准反哺**：本章"DB2 先行→标准收编"的语法今天全部是跨厂通用词：WITH RECURSIVE/GROUPING SETS/MERGE 在 PostgreSQL、SQL Server、Oracle（23ai 起原生 MERGE/逻辑表）与 DuckDB/SQLite 各有落地——方言对照可跑实验（SQLite 3.45.3 原生支持 WITH RECURSIVE/窗口，**非 DB2 行为**）。
- **Db2 11.5 语法增量**：聚簇/列组织、JSON 函数族（SQL/JSON）、临时表与上下文增强（⚠️ 转述；入口 https://www.ibm.com/docs/en/db2 curl 200 ✅）；pureXML 一脉见 [10](10-pureXML.md)。
- **半结构化合流**：SQL:2023 把 JSON 算子收编（ISO 口径 ⚠️ 只记会议/年份不贴 DOI——本环境 Crossref 对标准文书无寄存），与 DB2 当年"XML 原生"叙事形成 20 年呼应；跨格式对照 → [../PostgreSQL技术内幕_查询优化深度探索.md](../PostgreSQL技术内幕_查询优化深度探索.md) 的谓词面（盘上单文件）。
- **工程实践（2024–2026）**：ELT 工具（dbt 等）把 MERGE/窗口写进模板——本章语法是"分析工程化"的底层原语 → [../Unlocking_dbt/00-总览与阅读地图.md](../Unlocking_dbt/00-总览与阅读地图.md)。
- **读法**：把这章当作"SQL 通史的一条主线"来读：你会的每一条"现代 SQL"，多半在 2004–2008 的 DB2 手册里已经印过。
