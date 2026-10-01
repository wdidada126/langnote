# 04 BigQuery SQL 基础与 DML（BigQuery SQL Basic）

> 对应原书 **Ch.4 "BigQuery SQL Basic"**（章题与 28 个节题 ✅ QQ 阅读电子版实抓）。
> 正文为**精读重构**，非原书文本；机制描述「官方文档转述 ⚠️」；`docs.cloud.google.cn` URL 2026-10-02 亲测 200（✅）。
> 含 🔧 类比实验 T1/T1b/T1c/T5（DuckDB 列裁剪与扫描计费算术，**非 BigQuery 行为**）。

## 本章在本书中的位置

全书篇幅最大的一章（28 节），从 Compose Query 界面一路讲到 INSERT/UPDATE 手工改数——作者的"交互式分析"副题（A beginner's guide to mining massive datasets through **interactive analysis** ✅ 题名页原文）在本章落地：不建管道、不开 API，就在查询框里把数据问穿。本章也是 Legacy SQL 语法密度最高的一章（WITHIN、OMIT RECORD IF 两个化石节），学它 simultaneously 学一份"方言考古"。

## 4.1 界面、错误与查询类型（The BigQuery interface / Error checking / Types of queries / Querying public data）

- 查询双模式：**Interactive（即时，1000 并发上限量级）与 Batch（排队，默认 20 并行）**——书中以配额表讲解（⚠️ 数字过期，概念仍在；✅ https://docs.cloud.google.cn/bigquery/docs/introduction）。
- 错误检查教学法：作者故意写错 FROM 的项目名让读者看报错文本——"404 table not found 先查限定名，403 先查权限，reason: stopReason 看配额"（重构）。
- 查公共数据集贯穿全章：每条语法都用 `publicdata.samples.natality`（百年婴儿出生数据，本书明星表 ⚠️ 该数据集仍在 ✅ sample-tables 页口径另述）。

## 4.2 基础语法巡礼（Basic SQL syntax → DISTINCT 九节）

SELECT/FROM/WHERE/GROUP BY/ORDER BY/HAVING 各一节 + 表限定名 + DISTINCT。书中最有价值的两点（重构）：

1. **子句执行顺序 ≠ 书写顺序**：WHERE 先于聚合、HAVING 后于聚合、SELECT 别名在 Legacy 不能进 WHERE——作者用报错截图教这条，Ch.4 的"错误检查"呼应；
2. **表限定三段名** `project.dataset.table`；查公共数据集是**四段**（首段固定 publicdata/含点号需反引号），书里给了 `FROM [publicdata:samples.natality]` 的 Legacy 表引用格式——**方括号+冒号是 Legacy 专属化石**，Standard 用反引号点号。

## 4.3 BigQuery 特色函数与两个化石（SQL functions / WITHIN / OMIT RECORD IF / ROLLUP）

- `WITHIN`：Legacy 里对嵌套记录做 `CONTAINS ... WITHIN` 匹配——Standard 时代由 `IN UNNEST(...)` 全面取代（⚠️ 转述；数组语法见 https://docs.cloud.google.cn/bigquery/docs/reference/standard-sql/arrays）。
- `OMIT RECORD IF`：查询级"从嵌套表剔除不匹配子行"——Standard 无同义关键字，用半连接/数组过滤重写；今天两者均只存活在遗留文档里（✅ legacy 页 https://docs.cloud.google.cn/bigquery/docs/reference/standard-sql/legacy-sql 标注已弃用）。
- `ROLLUP`：书里当聚合糖讲解；Standard SQL 补齐 ROLLUP/CUBE/GROUPING SETS 是书后之事（⚠️ 转述）。
- 五型 JOIN（Inner/Left/Right/Full/Cross）+ `UNION / UNION ALL / UNION DISTINCT` 三态：书中特别标注 **BQ 的 UNION DISTINCT 需显式写**（多数方言裸 UNION 即去重）——这条到 2026 仍是 Standard SQL 行为（⚠️ 转述）。

## 4.4 手改数据（Adding your own data in BigQuery 五节：Creating/Inserting/Updating/Resetting/Deleting）

- 2017 现实（书中原状，⚠️ 转述）：DML 刚发布，本节"先 CREATE TABLE/INSERT VALUES，后 UPDATE/DELETE"是全书最早的正经建表例题；**Legacy 表不能 DML**、分区裁剪不当=整表重写照计费三连警告。
- 作者告诫（重构）：UPDATE 一条=重写整表（当时无行级更新），交互式改数用于修错，不用于当 OLTP——"别把仓库当交易库"。
- 今日对照：DML 全 GA、**MERGE**、近实时更新与 Change Data Capture 让"重写焦虑"大幅缓解（⚠️ 转述；✅ time-travel https://docs.cloud.google.cn/bigquery/docs/time-travel 兜底误改）。

## 4.5 🔧 列式与"按扫描字节计费"本机直觉（T1/T5，DuckDB 1.5.5，非 BigQuery 行为）

BigQuery 不可本机测，但**"计费=扫描字节≈读了哪些列"**可以在列式引擎上建立体感：

```python
# 200万行×10列 parquet（含两个 md5 字符串列）
con.sql("SELECT count(uid) FROM 'ev.parquet'").fetchall()           # 单列: 0.002s
con.sql("SELECT count(name||s1||s2) FROM 'ev.parquet'").fetchall()  # 全列字符串: 0.070s → 36.6x
con.sql("SELECT sum(total_compressed_size) FROM parquet_metadata('ev.parquet')")          # 159.2MB
con.sql("... WHERE path_in_schema='uid'")                                              # 8.01MB → 5.0%
```

- 读数：**同一张表，查询成本可以差 20 倍**——列数决定字节数，字节数决定账单（T5 用 "$5/TB" 算术模型套上表：SELECT * ≈ $0.0008，只读两列 ≈ $0.0001，19MB）。
- **边界声明**：这是列式存储通用直觉类比；BigQuery 的计费口径（压缩前逻辑字节 vs 分区裁剪后字节、缓存命中不重计等细则）**均非 DuckDB 行为**，以官方定价文档转述 ⚠️（镜像 pricing 页 404，不给 ✅ 链）。
- 书中同款建议（"少 SELECT *、先 LIMIT 探索"）在 🔧 实验里得到与引擎无关的机制学支持。

## 4.6 明星例题逐行讲：natality 上的六连问（重构自书节序）

```sql
# 0) Legacy 表引用（书中原貌，Standard 请换反引号）
FROM [publicdata:samples.natality]
```

1. **问总量**：`SELECT COUNT(1) FROM ...` ——界面右下角即刻显示"该查询扫描 ≈57MB"（⚠️ 书中量级口径），dry run 感性的第一滴；
2. **问分组**：`SELECT source_year, COUNT(1) GROUP BY 1`——GROUP BY 位置简写是 BQ 特色（书里强调 ⚠️）；
3. **问过滤**：`WHERE is_male AND gestation_weeks > 40`——布尔列可直接进 WHERE，`IS TRUE` 更稳（NULL 三值坑回收 Ch.3）；
4. **问口径**：`HAVING COUNT(1) > 100000`——书写序/执行序第四课；
5. **问排名**：窗口函数书里本章未讲（留给Further reading 外），2026 补一句 `RANK() OVER (PARTITION BY ... ORDER BY ...)` 才是本报告正解（⚠️）；
6. **问落表**：`CREATE TABLE demo.yearly AS SELECT ... GROUP BY source_year`——DML 五节的收官动作，也是 Ch.6 destinationTable 的 SQL 镜像。

六连问走完，Ch.4 的每个节题都在某一步露过脸——这是本书"交互式分析"的最小完整循环。

## 4.7 扫描成本三句话（4.5 🔧 实验的口径总结）

1. **列少则廉**：T1 实测列组合可致 36.6× 差（DuckDB 数据，机制同构 ⚠️）；
2. **行裁更狠**：分区谓词把"天"约掉（Ch.5 T2 续集）；
3. **先算后跑**：dry run/maximum_bytes_billed 是随身刹车（Ch.2 回收）。

三句话对应 BigQuery 控制台的三个入口：查询编辑器的估算条（⚠️ 界面物）、bq --dry_run（✅ CLI 文档）、作业配额（⚠️ 转述）——工具三代，物理量一个：**bytes scanned**。

## 阅读策略与坑

1. 语法巡礼节快读，把两处 Legacy 化石（4.3）读成"考古笔记"，其余全部以 Standard 语法重练一遍（Ch.2 的 `bq query --use_legacy_sql=false` 是练功房）；
2. JOIN 章节注意 BQ 特色：**Cross join 与无 ON 的 join 会爆炸扫描量**，先想清楚再按运行键 ⚠️；
3. DML 五节的成本警告今天仍成立一半——重写粒度变了但"小改大单"直觉不变；
4. 本章与 TDG 册第 2/3 章互替性强（[../Google_BigQuery_TDG/02-基础查询语法.md](../Google_BigQuery_TDG/02-基础查询语法.md)），两册合读可去掉本册的方言陈旧部分。

## 4.8 JOIN 解剖室（五型连接的成本与语义双注）

```sql
SELECT a.id, b.city
FROM `demo.orders` a
LEFT JOIN `demo.customers` b ON a.cid = b.cid   -- 左表保全：b 缺行补 NULL
```

- 书中五型各配一张文氏图 + 一条 natality 自连接例题（重构）；真正要带走的是三条 BigQuery 特色（⚠️ 转述，✅ query-syntax 页对照）：
  1. **INNER 可省 ON 退化成交叉积**——其他方言会拦，BQ 不拦只烧钱；
  2. **FULL OUTER 当年性能最差**，作者建议双 LEFT+UNION 绕行——今天优化器成熟，绕法反成可读性负资产（⚠️）；
  3. **嵌套字段不能直接当 JOIN 键**，先 UNNEST 摊平（Ch.5 回收）——2017/2026 同坑；
- `UNION ALL` 优先于去重版是全书贯穿的写法纪律：去重=额外一次全量 shuffle（🔧 直觉：任何引擎同然，数字各引擎不同 ⚠️）；
- 自连接例题（同年州际比较）是窗口函数缺席年代的土办法——学语义，别学姿势。

## 核心概念速览（中英对照）

| 中文 | 英文 | 一句话 |
| --- | --- | --- |
| 交互式/批查询 | interactive vs batch query | 并发额度两条道 |
| 表限定名 | fully qualified table name | project.dataset.table 三段 |
| Legacy 表引用 | [project:dataset.table] | 方括号冒号化石语法 |
| 聚合链 | GROUP BY/HAVING/ROLLUP | 书写序≠执行序 |
| 嵌套过滤 | WITHIN / OMIT RECORD IF | Legacy 双化石，Standard 重写 |
| 数组展开 | IN UNNEST(...) | WITHIN 的现代替代 |
| 五型连接 | inner/left/right/full/cross join | cross 是扫描量陷阱 |
| 并集三态 | UNION ALL / UNION DISTINCT | 去重必须显式写 |
| 数据操纵 | DML: INSERT/UPDATE/DELETE/MERGE | 2017 新贵，当年重写整表 |
| 扫描计费 | bytes scanned billing | 列裁剪=账单瘦身 |
| 试运行 | dry run | 运行前先算字节 |
| 出生样本表 | publicdata.samples.natality | 全章例题公共舞台 |

## 最新演进与工业实践

- **方言统一**：Legacy SQL 已于约 2024-06-30 停止服务（⚠️ 转述），本章 4.3 两个化石节成为纯考古；新文档全按 Standard 写（✅ query-syntax https://docs.cloud.google.cn/bigquery/docs/reference/standard-sql/query-syntax）。
- **DML/事务化**：MERGE、行级安全策略、**近实时 CDC 导出**、事务表（2024，⚠️ 转述）——4.4 的"别当 OLTP"告诫被产品边界逐条松动，但数仓反模式定性不变。
- **计费模型换代**：槽位制（slots ✅ https://docs.cloud.google.cn/bigquery/docs/slots）+ Editions/性能层级使"按扫描字节"不再是唯一计费叙事（⚠️ 转述）；🔧 T1 的列裁剪省钱直觉在按量面仍成立，在预留面转为"省槽位时间"。
- **缓存与物化**：结果缓存、**物化视图**（✅ https://docs.cloud.google.cn/bigquery/docs/materialized-views-intro）替代书中"手工汇总表"土法。
- 工业实践：交互式分析今天的主战场是 **SQL Workbench 文件化 + Git 版本管理 + PR 里 dry-run 审扫描量**；"SELECT * 不上生产"写进代码规范（⚠️ 通识转述）。
