# 05 BigQuery SQL 进阶：分区表、外表、通配符与视图（BigQuery SQL Advanced）

> 对应原书 **Ch.5 "BigQuery SQL Advanced"**（章题与 13 个节题 ✅ QQ 阅读电子版实抓）。
> 正文为**精读重构**，非原书文本；机制描述「官方文档转述 ⚠️」；`docs.cloud.google.cn` URL 2026-10-02 亲测 200（✅）。
> 含 🔧 类比实验 T2（hive 伪分区裁剪）与 T6（免装载直读 CSV，**均非 BigQuery 行为**）。

## 本章在本书中的位置

Ch.4 教你把问题问出来，Ch.5 教你**别让问题把钱和耐心烧光**：分区表控扫描量、外部表省装载工序、通配符表吃时间序列、视图固化口径、UDF 二次登场、嵌套记录正面攻坚。这是全书从"会查"到"会设计"的门槛章，也是本书与 TDG 性能章（[../Google_BigQuery_TDG/07-性能与成本优化.md](../Google_BigQuery_TDG/07-性能与成本优化.md)）重叠度最高、可以互相替换阅读的一章。

## 5.1 分区表（Partition tables 四节：GUI/SDK/查询/项目实践）

- 2017 形态（书中原状 ⚠️ 转述）：**一天一区的装饰性分区**——`tables$20170401` 分区装饰符（partition decorator）手动写进查询，配 `bq mk --time_partitioning_type=DAY`（Ch.2 命令面复用）；GUI 建表向导里勾一个 "Day partitioning" 就算教完。
- 书中价值主张（重构）：日志/事件类**时间序列表必分区**——"查询带 _PARTITIONTIME 谓词 = 扫描量除以天数"，与 Ch.4 🔧 T1 的"列裁剪省钱"并列为**行裁剪省钱**。
- 关键语法对账：书里 `_PARTITIONTIME` 伪列今天仍是 ingestion 分区的兼容入口，但官方主推**分区列（require partition filter 可选）**（⚠️ 转述；✅ https://docs.cloud.google.cn/bigquery/docs/partitioned-tables）。
- 5.1.4 "Using partition tables in your projects"：作者给了月报场景（每天追加、查单月）——今天读作"分区+聚簇"组合拳的第一拍（聚类 CLUSTERED BY 是书后 2018 年补的能力 ⚠️）。

### 🔧 T2：分区裁剪直觉（DuckDB，非 BigQuery）

```python
con.sql("COPY (SELECT * FROM events) TO 'hp' (FORMAT parquet, PARTITION_BY (yr), OVERWRITE)")
con.sql("EXPLAIN SELECT count(*) FROM 'hp/*/*.parquet' WHERE yr=5")
# 计划节点实测:  File Filters: (yr = 5)   → 10 个年度目录只打开 1 个, 命中 200,000/2,000,000 行
```

目录即分区的引擎会**把谓词下推到文件枚举层**；BigQuery 的 ingestion 分区做的是同构的事（把分区谓词映射到块元数据），但**机制细节、计费口径、必填谓词约束完全不同**——类比止于"谓词进计划才有裁剪"这一条（⚠️）。

## 5.2 外部数据源直查（Querying external data sources 两节）

- 书中流程（⚠️ 转述）：Console/API 定义**表结构挂在 GCS 路径上**（CSV/JSON/ORC/Avro 当日可选面有限），然后当普通表 SELECT；定位是"探索期免装载 + 冷数据不占仓内存储"。
- 书里诚实的坑单：外表查询**慢且重复计费**（每次重解析文件），建议只做抽样探索与装载前预览。
- 今日对照：外部表家族扩到 **BigQuery Omni/Dremio 时代的多源面**、**对象表（读非结构化文件集合）**、**BigLake 表**、**Iceberg 托管表（2025 ⚠️ 转述）**（✅ https://docs.cloud.google.cn/bigquery/docs/external-data-cloud-storage、object-table-introduction https://docs.cloud.google.cn/bigquery/docs/object-table-introduction）。

### 🔧 T6：免装载直查直觉（DuckDB，非 BigQuery）

```python
con.sql("SELECT city, sum(val) s FROM read_csv('ext.csv') GROUP BY 1 ORDER BY 2 DESC LIMIT 2")
# 5 万行 CSV 零装载, 首查 0.067s 出聚合
```

"文件即表"的体验一致，但 BigQuery 外表的**并发上限、单查询文件数限、元数据缓存**等平台约束在此类比中一律不存在（⚠️ 非 BigQuery 行为）。

## 5.3 通配符表（Wildcard tables）

- 解决"日表森林"问题：`events_*` + `_TABLE_SUFFIX BETWEEN '20170101' AND '20170131'` 一条查询跨月（书中原题重现：每日导出表 vs 分区的选型讨论 ⚠️）。
- 与分区表的裁决（作者观点重构）：**能用分区就别造日表**；通配符是既成事实的救赎。今天新增 UNION BY NAME 列自动对齐、`_TABLE_NAME` 元列（⚠️ 转述；✅ https://docs.cloud.google.cn/bigquery/docs/querying-wildcard-tables）。

## 5.4 UDF 与视图（User-defined functions / Views）

- UDF 在 Ch.3 教语法，这里教**用法**：把业务口径（账龄分段、州名标准化）封成函数复用——视图则把"每张报表的 WHERE"固化（⚠️ 转述）。
- 书中视图观（重构）：**视图不落数据、每次全算**→ 高频重视图=高频重扫描。这一节是物化视图广告位的史前史（2020 GA：✅ https://docs.cloud.google.cn/bigquery/docs/materialized-views-intro；书里每个"重口径视图"今天先问一句"能不能物化"）。
- Standard 视图支持参数化 TVF/逻辑视图为书后能力（⚠️ 转述；✅ views https://docs.cloud.google.cn/bigquery/docs/views）。

## 5.5 嵌套与重复记录攻坚（Querying nested and repeated records）

- 2017 最难节（书中自认）：Legacy 语法下的 RECORD 展平三连——`OMIT RECORD IF`（Ch.4 化石）、`NEST/FLATTEN`、逗号连接 `FROM t, t.repeated_field` 隐式展开。
- Standard 现代写法（本笔记替换重述 ⚠️）：`CROSS JOIN UNNEST(items) AS item`、点号路径 `st.city`、数组函数 `OFFSET/ORDINAL`（✅ https://docs.cloud.google.cn/bigquery/docs/reference/standard-sql/arrays）——🔧 T4（03 章）已给同构直觉。
- 作者的忠告（重构）：嵌套是为"保留事件上下文免 JOIN"设计的，**过度嵌套的代价在分析端偿还**；denormalize 与嵌套是钟摆。

## 5.6 迷你项目：一张点击流表的进阶四连（串起本章全部节题）

```bash
# ① 建日分区表（5.1；书时代还要手挂装饰符，今天一条命令）
bq mk --time_partitioning_type=DAY --schema click.txt proj.logs.clicks
# ② 装载一周（Ch.2 技能回收；再让两天新数据留在 GCS 当外表——5.2 场景）
bq load proj.logs.clicks gs://bucket/clicks_2017*.csv click.txt
bq mk --external_table_definition=gs://bucket/clicks_2018*.csv=CURRENT_SCHEMA.clicks_ext
# ③ 固化口径三连（5.4）：UDF 规范化 URL、视图封周报、通配符兼容旧日表森林
bq query --use_legacy_sql=false '''
CREATE OR REPLACE VIEW proj.logs.weekly AS
SELECT DATE(_PARTITIONTIME) d, COUNTIF(event="click") clicks
FROM `proj.logs.clicks`
WHERE _PARTITIONTIME BETWEEN TIMESTAMP("2017-01-01") AND TIMESTAMP("2017-01-07")
GROUP BY 1'''
# ④ 成本复核：先 dry run 带谓词版与裸 SELECT * 版，对比 estimatedBytesProcessed
bq query --dry_run 'SELECT * FROM `proj.logs.clicks`' | grep bytes
```

- 四步各踩一章眼：分区谓词命中与否、外表/内表同构查询、视图零物化成本、dry run 刹车——**面试官问"分区有什么用"，请拿第④步的两个字节数回答**；
- 嵌套侧补第五步（5.5）：若事件带 `items ARRAY<STRUCT>`，把 COUNTIF 换成 `CROSS JOIN UNNEST(items)` 再聚合——🔧 T4（03 章）即此步的 DuckDB 替身。

## 5.7 本节题的"还在用/已作古"清单（2026-10-02 逐条对链）

| 书中节题 | 今天 | 锚点 |
| --- | --- | --- |
| Creating partition table using GUI/SDK | ✅ 概念在、界面与旗标升级 | partitioned-tables ✅ |
| Querying external data sources | ✅ 家族化（外表/对象表/BigLake） | external-data/object-table ✅ |
| Wildcard tables | ✅ 仍 GA，转历史数据读取用 | querying-wildcard-tables ✅ |
| UDF / Views | ✅ +新增 TVF/物化/参数化 | user-defined-functions/views ✅ |
| Nested and repeated | ✅ UNNEST 路线彻底标准化 | arrays ✅ |
| partition decorator 手写法 | ⚠️ 被分区列+必选谓词取代 | ⚠️ 转述 |

## 阅读策略与坑

1. 本章五节可归一诀：**"裁剪（分区/通配符谓词）→ 固化（视图/UDF）→ 展平（UNNEST）"**；
2. 每节都埋着成本钩子——练例必开 `--dry_run` 看字节差（Ch.2 技能回收）；
3. 书中 GUI 截图步骤（分区建表向导）与今日界面差异大，**以 CLI + 文档链为准**（✅ 各节 URL）；
4. 与兄弟册互读：治理视角看 [../BigQuery_for_Data_Warehousing/05-仓库养护与查询开发.md](../BigQuery_for_Data_Warehousing/05-仓库养护与查询开发.md)，架构机制看 TDG 06/07 章。

## 核心概念速览（中英对照）

| 中文 | 英文 | 一句话 |
| --- | --- | --- |
| 分区装饰符 | partition decorator table$YYYYMMDD | 2017 手动时代语法 |
|  ingestion 时间分区 | ingestion-time partitioning (_PARTITIONTIME) | 系统列伪分区 |
| 分区列 | partition column | 现代替代，可强制谓词 |
| 行裁剪 | partition pruning | 谓词进计划=少读天 |
| 外部表 | federated/external query | GCS 文件免装载直查 |
| 对象表 | object table | 非结构化文件集合当表 |
| 通配符表 | wildcard table (`t_*` + _TABLE_SUFFIX) | 日表森林一查询 |
| 视图 | view | 固化口径不落数据 |
| 物化视图 | materialized view | 书后时代的重视图解 |
| 表值函数 | TVF | 参数化视图近亲 |
| 嵌套记录 | RECORD/STRUCT, REPEATED/ARRAY | 一表多子行 |
| 展开连接 | CROSS JOIN UNNEST | 现代展平主语法 |

## 最新演进与工业实践

- **分区进化树**：装饰符（书中）→ 原生 ingestion 分区 → 业务列分区 + **require filter** → 声明式分区（函数/分组列）→ **自动分区（2025 ⚠️）**（✅ partitioned-tables 页）；聚类表（CLUSTERED BY，2018）整条线本书未赶上。
- **时间旅行补位**：误删/误改表 7 天可回（✅ https://docs.cloud.google.cn/bigquery/docs/time-travel），书中"先 bq cp 备份再 DML"土仪式退役。
- **外表矩阵**：外部表支持列级权限、BigLake 跨云、托管 Iceberg（⚠️ 转述）；T6 式"直读探索"今天官方形态是 **Data Previews/serverless 编排预览**（⚠️）。
- **通配符退场中**：分区表普及后，日表森林模式在绿地项目基本消失，通配符转成历史数据读取工具（⚠️ 通识）。
- 工业实践：现代建模规范把本章浓缩为**"新表必分区、热表加聚簇、口径进视图、重视图物化、嵌套浅尝辄止"**五条 checklist（⚠️ 转述）；成本护栏（max_bytes_billed、custom roles 限扫描）见 BQDW 02 号章文件与 TDG 07。
