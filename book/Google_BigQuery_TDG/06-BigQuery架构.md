# 06 BigQuery架构（原书第 6 章 · BigQuery Architecture）

> 章首注：原书页区间 ⚠️ 推定 p.181–224；一级章题 ✅ 目录实抓；**本章二级小节 ⚠️ 推定**——Google 从未公开 BigQuery
> 完整架构论文，本目录按"Dremel 论文 + 官方文档可证部分 + 配套 `06_arch/all_code.txt` ✅ 实抓证据（REST jobs.insert 报文、
> `completedParallelInputs` 探针、london_bicycles/yellow_taxi 作业例）"三层组织，凡机制细节一律 ⚠️ 转述。

## 本章地图（⚠️ 推定结构）

| 组 | 小节主题 | 证据层 |
| --- | --- | --- |
| 宏观 | 前端服务/作业调度/槽位执行池/Colossus 存储 四层 ⚠️ | Dremel 论文谱系 + 官方文档 |
| 存储 | 列式+压缩编码、分片(shard)、自动均衡；用户无索引可建 | ⚠️ |
| 执行 | 树状扇出(leaf→intermediate→root)、Dremel 模型、shuffle | Dremel 论文 ✅（[../../paper/doi_10.14778_1920841.1920886/00-精读笔记.md](../../paper/doi_10.14778_1920841.1920886/00-精读笔记.md)） |
| 作业内省 | `completedParallelInputs` 看并行输入完成度；dryRun 估字节 | ✅ 配套 all_code.txt 实抓 |
| 数据组织 | 分区/聚簇/通配表三件套（裁剪的抓手，07 章消费） | ✅ URL（下节） |
| 多租户与隔离 | 槽位分池、按项目配额、网络隔离 | ⚠️ |
| 与 GCP 底座 | Colossus/高速网络（01 章"起源"的工程化收口） | ⚠️ |

## 核心精讲

### 1. 作业=一切的最小真相（✅ 配套 06_arch/all_code.txt）

配套仓库贴出的**真实 REST 报文**（✅ 实抓，Authorization 已脱敏）：

```http
POST /bigquery/v2/projects/<proj>/jobs HTTP/1.1
Host: www.googleapis.com
Content-Type: application/json
{'configuration': {'query': {'query': 'SELECT 17'}}}
```

连 `SELECT 17` 也走 jobs.insert 异步作业——**没有"连接"，只有作业**；
`bq --format=prettyjson show -j <job_id> | grep completedParallelInputs`（✅ 同款实抓）是 2019 版
"执行计划可视化"的全部家当，对应今天控制台进度条与 2026 的查询热力图（🔗 05 章演进节）。

### 2. 四层宏观与"无索引"的底气（⚠️ 转述）

前端（鉴权/编译/缓存）→ 调度（槽位分配）→ 执行（Dremel 式扇出聚合）→ 存储（Colossus 列存分片）。
扫描快靠：列裁剪 + 压缩块跳过 + 分片并行，而非 B-tree（教科书索引观对照
[../数据库系统概念6/11-索引与散列.md](../数据库系统概念6/11-索引与散列.md)、处理观
[../数据库系统概念6/12-查询处理.md](../数据库系统概念6/12-查询处理.md)、并行观
[../数据库系统概念6/18-并行数据库.md](../数据库系统概念6/18-并行数据库.md)）。
DDIA 的存算分离与云原生数据库一章（[../设计数据密集型应用/00-总览与阅读地图.md](../设计数据密集型应用/00-总览与阅读地图.md)）可作第三方框架 ⚠️。

### 3. 数据组织三件套（✅ 官方页 2026-09-27 实抓 200）

| 机制 | 语义 | URL（canonical，cn 镜像已验） |
| --- | --- | --- |
| 分区表 | 按时间列/日期表达式或**整数区间(2023+ ⚠️)** 切块，裁剪第一杠杆 | docs.cloud.google.com/bigquery/docs/partitioned-tables |
| 聚簇 | 分区内按≤N 列物理排序，匹配谓词才收敛扫描 | docs.cloud.google.com/bigquery/docs/clustered-tables |
| 通配表 | `dataset.sales_*` 跨表/跨分区 UNION + `_TABLE_SUFFIX` 伪列 | docs.cloud.google.com/bigquery/docs/wildcard-tables |

🔧 **通配表/glob 类比（DuckDB 1.5.5，非 BigQuery 行为）**：造两个年度分表文件后——

```sql
SELECT * FROM read_parquet('mf/sales_*.parquet', union_by_name=1) ORDER BY dt;
-- ✅ (202001,100),(202002,200) —— glob≈通配表，union_by_name≈模式漂移容忍
SELECT regexp_extract(filename,'sales_(\d+)',1) AS suffix, sales
FROM read_parquet('mf/sales_*.parquet', filename=1);
-- ✅ ('202001',100),('202002',200) —— filename 伪列 ≙ BQ 的 _TABLE_SUFFIX
```

DuckDB 的 `filename=1` 证明"从文件路径物色分片标签"是通配表语义的最小内核；BigQuery 的
`_TABLE_SUFFIX` 常量折叠还参与**裁剪**（⚠️），这层成本效应本机不可测。

### 4. 裁剪的本地可感版：hive 分区 vs 内存表（🔧 计时，非 BigQuery 行为）

2,000,000 行表按 `yr` 写 hive 分区 parquet（实测生成 21,376 个文件 ⚠️ 分区过碎的反面教材）：

```
内存表 WHERE yr=2019        → (991,)  耗时 0.002s
hive 分区 parquet 同查询     → (991,)  耗时 0.495s
```

🔧 读法：**裁剪省的是"扫描字节"，但文件碎片与网络/打开成本会吃掉收益**——这正是 BQ 用"托管大文件+元数据
统计"而非用户自管小文件的原因（⚠️ 转述其分层文件管理；对读 [../bigdata/09-存储与文件格式.md](../bigdata/09-存储与文件格式.md)
小文件之痛，同一条工程定律）。

### 5. 三巨头架构对位（⚠️ 转述归纳）

| 维度 | BigQuery | Snowflake（✅ 盘上笔记） | Trino（✅ 盘上笔记） |
| --- | --- | --- | --- |
| 计算单元 | slot（自动分配/预留） | virtual warehouse（用户显式 sizing） | worker 集群（自运维） |
| 存储 | Colossus 内列存（闭源）+2026 Iceberg 托管 | 内部微分区（闭源） | 无（连接器读开放格式） |
| 弹性 | 无预置 serverless | 秒级启停仓库 | 静态扩缩 |
| 计费观 | 字节 or 槽位 | credits | 自建成本 |
  对读入口：[../Snowflake_The_Definitive_Guide/02-架构与虚拟仓库.md](../Snowflake_The_Definitive_Guide/02-架构与虚拟仓库.md)、
[../Trino_The_Definitive_Guide_2e/04-Trino架构.md](../Trino_The_Definitive_Guide_2e/04-Trino架构.md)、
[../Presto实战/04-Presto的架构.md](../Presto实战/04-Presto的架构.md)。同波 `Amazon_Redshift_TDG` **登记不链**（00 互链表）。

## 常见误区（⚠️ 转述）

| 误区 | 事实 |
| --- | --- |
| 能建索引/能选磁盘类型 | 均不存在；只有分区/聚簇两个抓手 |
| 分区数随便加 | 每表分区/聚簇列数有上限；碎分区劣化（🔧 T9 精神） |
| 通配表=视图免费 | 每次展开扫全部匹配表，除非 `_TABLE_SUFFIX` 能折叠 |
| slot 是"核" | slot≈并行度抽象单位，不承诺 vCPU 等价（⚠️ slots 页口径） |
| 架构论文=实现文档 | Dremel 2010 是精神源头，产品内部多年重写（⚠️ 无公开逐版本对齐） |

## 与其他章、其他书联系

- 裁剪/物化视图/槽位的消费端全在 [07-性能与成本优化.md](07-性能与成本优化.md)；`SELECT 17` 式脚本化 → [08-高级查询.md](08-高级查询.md)。
- 历史快照读（Time Travel）机制在 [08-高级查询.md](08-高级查询.md)；快照/克隆 vs Snowflake：
  [../Snowflake_The_Definitive_Guide/07-数据保护与恢复.md](../Snowflake_The_Definitive_Guide/07-数据保护与恢复.md)。
- 论文线总表：[../../db/db.md](../../db/db.md)（Dremel 条目 ✅）。
- 分布式底座词汇表：[../数据库系统概念6/19-分布式数据库.md](../数据库系统概念6/19-分布式数据库.md)。

## 核心概念速览（中英对照）

| 术语 | English | 释义 |
| --- | --- | --- |
| 作业 | job | 一切 SQL/装载/复制的异步执行单元（✅ REST 报文实抓） |
| Dremel | Dremel | 树状扇出交互式分析引擎，BigQuery 执行模型源头 |
| Colossus | Colossus | GFS 后继分布式存储层，BigQuery 的地基（⚠️） |
| 槽位 | slot | 并行度与计费的抽象单元，可预留可按需 |
| 前端服务 | frontend | 鉴权/编译/缓存命中的入口层（⚠️ 转述） |
| 分区表 | partitioned table | 按时间/区间切块的裁剪单位 |
| 聚簇 | clustering | 分区内多列物理排序，谓词匹配即少扫 |
| 通配表 | wildcard table | `tbl_*` UNION 视图 + `_TABLE_SUFFIX` 伪列 |
| 并行输入完成度 | completedParallelInputs | ✅ 配套实抓的作业进度探针 |
| dry run | dryRun | 只估不跑，字节预算第一工具 |
| 无聚簇索引 | no user index | 列存+扫描引擎，索引概念让位于裁剪 |
| 结果缓存 | results cache | 前端层命中即免费（07 章计费相关） |
| 分层存储 | tiered storage（近线/冷线 ⚠️） | 2019 原书语境为自动列存；2026 已产品化多存储类（见演进） |

## 最新演进与工业实践

- **执行面 2026**（均 ✅ 版本说明 2026-09-27 实抓）：查询文本热力图（query text heatmap）把"哪段 SQL 吃槽位"
  可视化进执行图；Iceberg 托管表 advanced runtime/多语句事务/分区 2026-07-13 GA——**架构章第一次有了"开放格式也在
  托管执行面内"的新分支**（✅ docs.cloud.google.com/bigquery/docs/iceberg-tables）。
- **资源面**：fluid scaling——预留槽位秒级计费、无最小时长的自动扩缩 2026-06-03 GA（✅ docs.cloud.google.com/bigquery/docs/slots）；
  组织级策略可约束 reservation/capacity commitment 操作（Preview ✅）——本章"槽位"叙事在 2026 已长成
  "editions+预留+承诺+自动扩缩"四件套。
- **存储类分层**：近线/冷线存储类把"分层存储"从形容词变 SKU（⚠️ 术语以官方 storage 类文档为准，本册不引未验 URL）。
- **图/向量入引擎**：graph 查询执行与可视化 2026-04（✅）、向量检索 GA 系（03/09 章各取一面）——
  架构章的"SQL 引擎"定语在 2026 扩为"多模态分析引擎"。
- 工业实践：三云对位表建议与 [../Snowflake_The_Definitive_Guide/09-查询性能分析与优化.md](../Snowflake_The_Definitive_Guide/09-查询性能分析与优化.md)
  联读；Redshift 栏待同波 #178 落盘由主代理回填（00 互链义务表 A）。
