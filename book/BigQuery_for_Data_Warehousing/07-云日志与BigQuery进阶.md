# 07 云日志与 BigQuery 进阶

> 对应原书 **Ch.12 Cloud Logging（pp.253–269）**、**Ch.13 Advanced BigQuery（pp.273–303）**（章题/页码：Crossref DOI _12 / _13，✅ 实抓）。
> 正文为精读重构；机制为官方文档转述（⚠️）；章内二级小图为按章题与公开目录的**推定重构**（⚠️，一级章题与页码为 ✅）。

## 一句话主题

第 12 章把「仓库自己产生的日志」也变成仓库里的数据——观测数据的自举；第 13 章是全书技术纵深章：嵌套建模、布局调优、系统视图与高级 SQL 的合集。读完这两章，读者从「会用 BigQuery」进入「运营 BigQuery」。

## Ch.12 Cloud Logging：观测数据自举

### 12.1 日志入仓的路径（⚠️ 转述）

- Cloud Logging（时名 Stackdriver Logging）经 **sink（接收器）导出 BigQuery 数据集**：日志按接收器自动建**每日新表**（非分区表按日切表）——这与 Ch.9 通配表语法（`tables_*` + `_TABLE_SUFFIX`）天然咬合，是通配表在 2020 仍不可替代的头号场景（见 [05-仓库养护与查询开发.md](05-仓库养护与查询开发.md)）；
- 两类与仓库直接相关的日志流：**审计日志**（Admin/Data Access，谁动了哪张表）与**平台遥测**（作业统计、配额告警）；后者在 INFORMATION_SCHEMA 有更结构化的等价物，作者建议两路都做：日志管「人」，信息模式管「作业」；
- 治理钩子：日志表本身的保留期、访问最小化（审计日志是敏感资产）——Ch.14 权限章回收（见 [08-数据治理与长期适应.md](08-数据治理与长期适应.md)）。

### 12.2 用法清单（重构自本章叙事）

1. **成本审计 SQL**：按用户/标签聚合 job 扫描字节，月报给财务（Ch.4 事后闸的数据源，见 [02-数据盘点与成本管控.md](02-数据盘点与成本管控.md)）；
2. **SLA 看板**：装载作业完成时间序列 → 环比异常告警（Ch.10 值守三件套的仪表化）；
3. **安全取证**：敏感表访问链回放（principal × table × time 透视）；
4. **指标下沉**：Monitoring 告警 webhook → Ch.11 函数 → 仓内告警事实表——告警本身也可被 SQL 复盘；
- 反身提醒（作者式幽默，重构）：**别用按需计费的仓库全日扫自己的日志**——日志表必上分区/生命周期，否则观测成本吃掉观测收益。

## Ch.13 Advanced BigQuery：技术纵深合集

### 13.1 嵌套数据建模（本章重头，⚠️ 转述）

- `ARRAY<STRUCT>` 把「一对多」装进一行：订单+明细行内数组，一次扫描完成聚合，免 join 爆炸——代价是 UNNEST 语法心智与「数组元素不是行」的语义断层；
- 建模判据（重构）：数组元素**从不单独作查询主体**时内嵌划算；需要独立权限/独立生命周期时拆表；嵌套深度与数组大小有硬配额（⚠️ 100 层/重复列规模上限类限制，数字以官方页为准）；
- 与文档数据库的和解：BigQuery 的 STRUCT/ARRAY 让「关系派」与「文档派」在同一张表共存——方法论对位 [../Building_the_Data_Warehouse/00-总览与阅读地图.md](../Building_the_Data_Warehouse/00-总览与阅读地图.md)（星型教条的云端松动，盘上已验名）。

### 13.2 布局调优矩阵（分区×聚簇×过滤，⚠️ 转述）

- 分区列选择：高基数时间列、查询谓词习惯与之对齐（范围过滤 vs 等值过滤决定分区粒度 DAY/MONTH）——✅ https://docs.cloud.google.cn/bigquery/docs/partitioned-tables（镜像 200）；
- 聚类列选择：**等值过滤高选择性列在前**（客户 ID 优于状态码）、最多四列（2020 上限）、列序即剪枝序——✅ https://docs.cloud.google.cn/bigquery/docs/clustered-tables（镜像 200）；
- 组合效应：分区裁天、聚簇裁块、列裁剪裁宽——三刀齐下才是 TB 表单日查询的可接受剖面；验证通道：dry-run 字节数对比 + `EXPLAIN`（⚠️ 2020 为 statistics plan 预览口径）；
- 已聚簇表的再聚簇：对存量分区 `UPDATE ... WHERE false`/重建迁移的运维手艺（Ch.8 影子表技法的特例，见 [05-仓库养护与查询开发.md](05-仓库养护与查询开发.md)）。

### 13.3 系统视图与元编程（重构）

- INFORMATION_SCHEMA 家族（表/列/分区元数据 + JOBS 作业史）：**用 SQL 运营仓库**的技术底座——12 章的成本审计 SQL 正跑在这层上；region 化视图命名从 2020 至今多次变体（⚠️ 演进注）；
- 脚本与过程化：临时表/表变量/控制流把多步作业封成单脚本；UDF/TVF 的复用经济学（Ch.9 展开，此处补治理维度：版本化与依赖登记）；
- 物化视图：对高频聚合的预计算+自动改写命中——按需模式下「以一次昂贵重算换千百次免费命中」（✅ https://docs.cloud.google.cn/bigquery/docs/materialized-views-intro 镜像 200）；
- 性能最佳实践总入口 ✅ https://docs.cloud.google.cn/bigquery/docs/best-practices-performance-overview（镜像 200）。

## 🔧 概念类比（非 BigQuery 平台行为）

**E4 热冷分档（SQLite 3.45.3，月度分文件+按需 ATTACH）**：

```
E4 仅热档查询=4.2ms | 加挂冷档后联合=2.6ms rows=120000 → 热冷分离=按需触达，冷档不被查则零IO
```

- 两个独立 DB 文件模拟热/冷档：不 ATTACH 冷档时其 60000 行对查询完全不可见（零 IO）——类比 BigQuery 长期存储折扣与分区生命周期的「冷数据自动降权」心智。⚠️ BQ 分层是**平台自动按修改龄降单价**、无文件挂载动作，本组仅类比「冷档默认远离计算路径」。

**E5 物化复用（DuckDB 1.5.5，预聚合表 vs 每次重扫）**：

```
E5 物化表=1.9ms vs 全量重聚合=13ms 一致=True → BQ 物化视图/结果缓存的扫描费省法类比
```

- 同一聚合：预计算物化表比 300MB Parquet 全量重聚合快约 7 倍且结果一致——类比物化视图/结果缓存「一次写、多次免扫」的成本结构。⚠️ BQ 物化视图有自动增量刷新与查询改写（本类比无），结论不外推。方法：`CREATE TABLE mv AS ... GROUP BY` 对照即时聚合，perf_counter 计时。

## 附：日志与进阶练习配方（自拟教学示意，⚠️ 非原书内容）

- **通配表日志查询样板**（sink 按日建表形态，语法 ⚠️ 转述）：

```sql
SELECT timestamp, protos_payload.methodName, resource.labels.table_id
FROM `ds.bq_audit_cloud*`                     -- 通配：吞掉全部日志日表
WHERE _TABLE_SUFFIX BETWEEN '20200101' AND '20200131'
  AND protos_payload.methodName = 'google.cloud.bigquery.v2.JobInsert'
LIMIT 1000;                                    -- 日志表必带窗+必带限（12.1 反身提醒）
```

- **聚簇键选择工作表**（13.2 的操作化，重构）：取近 30 日该表查询日志 → 统计各列在 WHERE 中的**等值出现率** × **列基数** → 前四名列序即候选聚簇序 → 影子表重建 → dry-run 前后字节对比留档进变更单——一条完整的「布局优化闭环工单」；
- **INFORMATION_SCHEMA 三连**（region 化命名 ⚠️ 以当期文档为准）：

```sql
-- 谁在烧钱
SELECT job_creator_email, SUM(total_bytes_processed) b
FROM region_us.ds.INFORMATION_SCHEMA.JOBS
WHERE creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
GROUP BY 1 ORDER BY 2 DESC LIMIT 10;
-- 僵尸表 / 无分区谓词作业：同表族改条件即可（05 号巡检三件同源）
```

- 观测自举的反身测试清单：日志表自身有无分区/窗口过期？成本审计 SQL 的扫描量是否小于它省下的钱？告警链路端到端演练（注入一条假审计记录）季度做过吗？——三问全否的仓库，12 章等于白读；
- 进阶阅读梯度建议：先吃透 13.1 嵌套（改变建模观）→ 再练 13.2 布局（改变账单观）→ 最后玩 13.3 元编程（改变运维观）；顺序反了会先把仓库「运营」成一个没有数据的空目录；
- 思考题（5 道）：T1 日志按日建表与分区表两代形态下，通配语法与分区谓词各自边界？T2 ARRAY<STRUCT> 内嵌明细 vs 拆表，权限粒度差在哪？T3 聚簇列序 (customer_id, date) 与 (date, customer_id) 的剪枝效果差如何解释？T4 E4/E5 两组 🔧 类比各能外推到什么程度、不能外推什么？T5 审计日志的敏感性高于业务数据吗？给出治理判据。

## 系列互链

- 同书纵向：嵌套/通配语法细节 [05-仓库养护与查询开发.md](05-仓库养护与查询开发.md)；布局调优的账单兑现 [02-数据盘点与成本管控.md](02-数据盘点与成本管控.md)；日志资产的保护 [08-数据治理与长期适应.md](08-数据治理与长期适应.md)。
- 他书横向：元数据自举（系统视图运营仓库）与 Data Fabric 的活性元数据同题，对位 [../Data_Fabric_Architectures/00-总览与阅读地图.md](../Data_Fabric_Architectures/00-总览与阅读地图.md)；调优通识谱系 [../Database_Tuning/00-总览与阅读地图.md](../Database_Tuning/00-总览与阅读地图.md)（盘上均已验名）。

## 附二：进阶误区五条（重构速查，⚠️ 非原书内容）

- 误区1「聚簇列越多越好」：四列封顶且写侧有重组代价，两列高选择性胜过四列凑数；
- 误区2「分区粒度越细越省」：小时分区×小表=元数据开销反超扫描节省，分区是为大表设计的；
- 误区3「ARRAY 嵌套是银弹」：元素级权限与元素级生命周期需求一来就得拆表（13.1 判据的反向应用）；
- 误区4「信息模式视图=免费」：JOBS 视图本身按查询计费，巡检 SQL 也要带时间窗；
- 误区5「观测体系一次建成」：日志/指标/断言三层各留季度评审位，否则第一条永远是「先不管」。

## 核心概念速览（中英对照）

- **日志接收器** — Log Sink：把 Cloud Logging 流导出到 BigQuery 的管道对象。
- **按日建表** — Daily Log Tables：日志入仓的默认物理形态，通配表语法的主要客户。
- **审计日志** — Audit Log：Admin/Data Access 两类行为留痕，安全取证底账。
- **嵌套列** — Nested Column：ARRAY/STRUCT 型列，一行装一对多。
- **UNNEST 语义断层** — Unnest Gap：数组元素非行、需展开才进关系算子的认知坎。
- **聚簇列序** — Cluster Column Order：最多四列的等值过滤优先级排列，即剪枝序。
- **分区粒度** — Partition Granularity：DAY/MONTH/HOUR 或整数范围分区的时间刻度选择。
- **INFORMATION_SCHEMA** — Info Schema：以 SQL 查询仓库元数据与作业史的系统视图族。
- **物化视图** — Materialized View：预计算聚合+查询改写的扫描费豁免器。
- **影子再聚簇** — Recluster via Copy：存量表补聚类需重建搬运的运维技法。
- **观测自举** — Observability Bootstrap：仓库日志回到仓库自身被 SQL 复盘。
- **统计计划** — Statistics/Explain：查询物理剖面的预估输出，调优验证入口。

## 最新演进与工业实践

- **日志入仓形态换代（2022–2024）**：Cloud Logging 的 Log Analytics 池（2023）与「BigQuery 路由到分区表」路线逐步替代按日建表旧模式；Live tail/日志预览改善运维体验 ⚠️（canonical 页本环境不可直连，机制转述）。通配表场景收缩为历史兼容层。
- **进阶能力矩阵扩张**：表快照（SNAPSHOT，2022）、`LOAD DATA`/`EXPORT DATA` 语句化、ML/dist 推理（✅ https://docs.cloud.google.cn/bigquery/docs/vector-search 镜像 200 为向量检索文档入口，属 Ch.19 线的延伸）——2020 本章的「高级」清单到 2026 已是平台基线。
- **系统视图演进**：INFORMATION_SCHEMA 全面 region 参数化并新增 reservations/editions 视图族（⚠️ 转述），「用 SQL 运营仓库」从技巧升格为官方运维面。
- **工业实践（2024–2026）**：成熟组织把 13 章三刀剖面（分区/聚簇/列裁剪）做成**表级 SLI**（新表上线必须声明分区策略与聚簇键评审记录）；观测数据本身进湖仓分层（日志类热查 30 天、冷档对象存储）成为降本主战场之一，路线对位 [../Data_Lakehouse_in_Action/00-总览与阅读地图.md](../Data_Lakehouse_in_Action/00-总览与阅读地图.md)。
