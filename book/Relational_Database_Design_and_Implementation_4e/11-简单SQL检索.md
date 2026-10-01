# 11-简单SQL检索（Part IV 导言 p.321 ✅；Ch16 Simple SQL Retrieval, pp.323–354 ✅）

> 三态：✅ 书页 TOC/Crossref 页码实抓 · ⚠️ 转述/推定展开 · 🔧 本机 SQLite/DuckDB 实测（**非本书示范行为**）。
> Part IV（交互式 SQL 操纵关系库）开场章，32 页：SELECT 骨架的列选择、行选择、排序与 NULL 三值逻辑。教材把「投影/选择」代数词汇（Ch6）在此正式换成 SQL 词汇——这是全书「理论→操作」落差最集中的一章，值得逐段对表。

## 一、精读札记（官方二级小节 ✅ 逐条）

- **Revisiting the Sample Data** —— Rare Books 例库回场：代数章的手写表达式在此获得 SELECT 翻译。
- **Choosing Columns** —— SELECT 列清单=π 的近似；「近似」指缺 DISTINCT 时的多重集语义（Ch6 §2.1 再袭）。
- **Ordering the Result Table** —— ORDER BY 与「行序无关」公理的合宪性谈判：只为呈现排序。
- **Choosing Rows** —— WHERE=σ；谓词组合（AND/OR/NOT）与 BETWEEN/IN/LIKE 语法糖。
- **Nulls and Retrieval: Three-Valued Logic** —— TRUE/FALSE/UNKNOWN 三值；IS NULL 唯一合法判等；「NOT(x) 仍未知」的滤行陷阱。

## 二、主题深读

### 2.1 三值逻辑是本章的真正考点
WHERE 只放行 TRUE 行：UNKNOWN 与 FALSE 同遭淘汰，于是
- `WHERE col <> 5` 漏掉 NULL 行（<>5 为 UNKNOWN）；
- `WHERE NOT (col = 5)` 同样漏 NULL——「负查询不闭全」。
🔧 E6 镜像实验（demos.txt）：`AVG(temp_c)`=-41.0（跳过 NULL，4 值均摊）vs `SUM(temp_c)/5`=-32.8（NULL 不参与 SUM、分母手工 5）——聚合语义也受三值逻辑管辖，E6 的-41 还演示了「NULL 无害、错误值有毒」的对照（-274 一值拖垮均值 21 度）。
### 2.2 Codd Rule 3 的兑现度检查
Ch9 Rule 3 要求 NULL 被「系统化对待」；现实方言矩阵（🔧 本机）：
- SQLite：`=NULL` 返回 NULL（非报错）、`NULLS FIRST/LAST` 需版本支持 ⚠️；
- DuckDB 1.5.5：`NULLS` 保留字曾致列名撞车（盘上 [../DuckDB_Up_and_Running/00-总览与阅读地图.md](../DuckDB_Up_and_Running/00-总览与阅读地图.md) 波2实测有案 ✅），排序含 NULL 行为与标准一致 ⚠️。
教学结论：Rule 3 的「系统化」在 2026 仍是**方言差异清单**，本章的 NULL 小节应扩成矩阵表。
### 2.3 LIKE 的通配符工程边界
书内 LIKE 讲模式匹配；现场痛点是大小写折叠方言（PostgreSQL LIKE 大小写敏感 vs MySQL 不敏感，SQLite TEXT 比较按 BINARY——E6 的 'new york ' 检索演示：`city LIKE '%york%'` 能命中、`city='new york'` 不能命中，尾空格陷阱与 2.4 呼应）。
### 2.4 呈现序与存储序的分离纪律
ORDER BY 的「合宪性」在 E5 计划实测里看得见：SQLite 无 ORDER BY 的行序=扫描序，加 `dept,sal` 复合索引后行序改变而计划变 SEARCH（demos.txt E5）——「结果序必须显式声明」的教训有机器证词。

### 2.5 SELECT 五子句 × 代数四动词（回指 05 的兑现面）
Ch16 小节结构（✅ Choosing Columns / Ordering the Result Table / Choosing Rows / Nulls and Retrieval）正是代数三件套的 SQL 身位：Project→SELECT 列清单、Restrict→WHERE、呈现序→ORDER BY（模型外动作，2.4）。书后时代加两件：DISTINCT（回集合论域，05 §2.6 的税）、LIMIT/OFFSET（书内小节清单无分页 ✅——分页是应用动作，2026 补件 ⚠️）。收口题：本章每条例题改写为代数式；写不出或写出即错的，都是 05 章的欠账。

### 2.6 三值逻辑真值表（本章核心资产，本册重排）

| 运算 | T | F | U |
|---|---|---|---|
| AND | T/F/U | F/F/F | U/F/U |
| OR | T/T/T | F/F/U | T/U/U |
| NOT | F | T | U |

消费端三规则：WHERE 只取 TRUE 列（U 被丢）、CHECK 约束只拦 FALSE 列（U 放行——NULL 绕过完整性是 E2/FK 执法矩阵的反面半张，🔧 载体注非本书示范）、CASE WHEN 取首个 TRUE 分支。「Nulls and Retrieval」（✅ 节题）=Codd Rule 3 的兑现现场，2.2 的 Rule 3 检查表与本表合读，NULL 线闭环。

### 2.7 检索谓词的方言小抄（⚠️ 综合+✅ 文档账）
LIKE 的 %/_/ESCAPE 三件套、SQLite 方言的 GLOB、标准的 SIMILAR TO 残余、DuckDB 的 regexp_* 族——四方言一家时先记各家的（⚠️ 通识清单；SQLite 官方文档面在 00 取证链 ✅ 内，未逐页重验者以本行纪律自约）。BETWEEN 含两端是 2026 通例，但其「对称闭区间」史前怪谈（低>高时的行为分化）⚠️ 已随旧引擎退场。IN 值表 vs EXISTS 是 12 章相关子查询的前置分岔。本章 32 页（✅ 323–354）的陷阱密度与页面难度成反比——**最简单的章藏着最贵的 NULL 税**。

### 2.8 全链首课义务（评注）
文件 11 是本盘上 SQL 实操链的起点：13 的聚合账与 17 的 E6 质量标本都长在本章 WHERE/ORDER 纪律上。自检=Ch16 五节（✅）每条例题在 Rare Books 复现库（05 §2.8 剧本，🔧 非本书示范）跑通。

## 三、原书 → 2026 对位

| 书内论点 (2016) | 2026 现状 |
|---|---|
| NULL 三值逻辑教学 | 不变+加剧：LEFT JOIN 产 NULL、JSON 路径缺键产 NULL、外层查询 WHERE 吞行成事故 Top 来源 |
| BETWEEN/IN/LIKE 糖 | IN 大列表被 JOIN 值表/半连接改写取代；LIKE 前缀匹配走索引下推 |
| 交互式即席查询 | notebook SQL/dbt 即席层；SELECT 教学价值不减 |
| 纸面查询练习 | 断言测试（dbt tests）把「答案正确」变成可执行件 |

## 四、阅读自测
1. `WHERE rating IS NULL` 与 `WHERE NOT (rating IS NOT NULL)` 等价吗？用三值表推。
2. `<>` 漏 NULL 事故如何用 COALESCE 或显式 `OR col IS NULL` 修复？
3. E6 里 AVG=-41 的算式分解（四值/跳 NULL）现场写出。
4. SQLite 的 BINARY 比较让 LIKE 与 = 在 'NY'/'ny ' 上各是什么结果？
5. 「ORDER BY 仅为呈现」的公理依据与 E5 计划证据各一句。

## 五、互链
- 上游：05（π/σ 代数原形）、09（例库 DDL）、10（案例数据）。
- 下游：12（连接检索）、13（聚合分组）、14（把常用 SELECT 命名成视图/CTE）。
- 谱系：[../SQL_and_Relational_Theory/00-总览与阅读地图.md](../SQL_and_Relational_Theory/00-总览与阅读地图.md)（NULL/排序违约批注库）、[../Using_SQLite/00-总览与阅读地图.md](../Using_SQLite/00-总览与阅读地图.md)（🔧 载体册）、[../Databases_Illuminated_4e/00-总览与阅读地图.md](../Databases_Illuminated_4e/00-总览与阅读地图.md)。

## 核心概念速览（中英对照）
| 中文 | 英文 | 出处/一句话 |
|---|---|---|
| 选择列 | choosing columns (SELECT list) | Ch16 π 的 SQL 形 |
| 选择行 | choosing rows (WHERE) | Ch16 σ 的 SQL 形 |
| 排序 | ordering (ORDER BY) | Ch16 呈现层特权 |
| 空值 | NULL | Ch16/Rule 3 系统化对象 |
| 三值逻辑 | three-valued logic | Ch16 TRUE/FALSE/UNKNOWN |
| 模式匹配 | LIKE pattern matching | Ch16 通配谓词 |
| 区间谓词 | BETWEEN | Ch16 语法糖 |
| 列表谓词 | IN | Ch16 语法糖 |
| 大小写折叠 | case folding | 2.3 方言痛点 |
| 多重集语义 | bag semantics | 2.1 DISTINCT 缺省面 |
| 聚合语义 | aggregate semantics | E6 AVG/SUM 的 NULL 纪律 |
| 五子句映射 | clause-verb map | §2.5 SELECT↔代数 |
| 分页补课 | LIMIT/OFFSET | §2.5 书外义务 ⚠️ |
| 真值九格 | 3VL table | §2.6 重排资产 |
| WHERE 取真列 | WHERE TRUE-only | §2.6 U 被丢 |
| CHECK 拦假列 | CHECK FALSE-only | §2.6 NULL 绕法 |
| CASE 首真支 | CASE first-true | §2.6 消费端三规则 |
| 通配三件套 | LIKE %/_/ESCAPE | §2.7 谓词小抄 |
| GLOB 方言 | GLOB | §2.7 SQLite 特有 |
| SIMILAR TO | SIMILAR TO | §2.7 标准残余 |
| 正则分家 | regex per dialect | §2.7 ⚠️ 综合 |
| 区间对称史 | BETWEEN symmetry | §2.7 旧引擎分化 ⚠️ |
| IN 与 EXISTS 分岔 | IN/EXISTS fork | §2.7 前置 12 |
| 呈现序纪律 | display vs storage | §2.4 复习 |
| NULL 排序面 | NULL ordering | ⚠️ 方言分歧面 |
| 简单章高税 | easy-chapter tax | §2.7 反比论 |
| 五节全跑 | five-section run | §2.8 毕业判据 |
| 例库重访 | revisiting the sample data | ✅ Ch16 首节 |
| 选列选行 | choosing columns/rows | ✅ 两节题=投影选择 SQL 身 |

## 最新演进与工业实践
- 三值逻辑的当代事故面集中在「外层 JOIN+WHERE 谓词」组合（LEFT JOIN 后 WHERE b.x=5 静默降级为内连接）——本章若出 2026 增补版，应把该模式列为头号陷阱（⚠️ 工程通说，对位见盘上 BigQuery/数仓册的反连接章）。
- SQLite/DuckDB 双载体可复现本章全部小节（🔧 E6/E5 片段）；DuckDB 文档站约束/类型页实查在线 ✅（见 08 文件 URL 账），SELECT 语义无特殊页面——方言差异集中在排序 NULL 位置与字符串折叠，教学时以本目录矩阵为准。
- 查询断言化：dbt/Great Expectations 把「这道题的答案」变 growth check（行数/值域/NULL 率），Ch16 的自测题在工业里即默认测试套件成员（与 17/19 文件演进节合读）。
- 「简单」是教材修辞（✅ 章题）：32 页里三值逻辑与 LIKE 语义占真正事故预算（§2.6/2.7）。
- 真值表+三消费端=全册 NULL 总阀门；12/13/17 从本表放款（回顾登记）。
- 🔧 E6 联动（非本书示范）：聚合口径差（-41.0 vs -32.8）本埋 13 算（demos 账）。
- 谓词小抄维护义务：⚠️ 条以 2026-10 文档口径为账——诚实纪律（§2.7）。
- 代数↔SQL 互写（§2.5）是 05 留题在 11 交卷——两文件合读完整。
- 毕业判据：五节（✅）每节一题手跑+九格真值表默写。
- LIMIT/OFFSET 补件（⚠️）姿势：排序稳定先行，分页才有意义。
- 「WHERE 只取 TRUE」值一次事故复盘：NOT(col<>'x') 与 col='x' 在 NULL 行不等价（⚠️）。
- Rule 3 检查（§2.2）续账：引擎侧系统化合格、应用侧语义化欠账——永久考点。
- 呈现序即 API 契约（§2.4）：无 ORDER BY 的排序断言=测试不稳定源（⚠️ 工程律）。
- LIKE 前缀可索引性是 11→14 隐藏接缝：中缀 %=全扫（⚠️ 载体常识）。
- 谓词写法跟引擎、语义纪律跟标准——三分家合读判据（§2.7）。
- 本章在 NoSQL 线位置：查询谓词是最先被「再 SQL 化」的一族（18 回指）。
- 首课义务（§2.8）：13/17 标本以本章 WHERE 语法为地基。
- 课堂复用：E1 宽表加 WHERE IS NULL 即占位行检测器（02/11 联动；非本书示范）。
- 与 12 接力：单表谓词→多表装配；「全部」触发词移交 12 §2.3。
- 方言小抄不冒充实测账：未跑项全部 ⚠️——全册纪律同标。
