# 04 将数据加载到BigQuery（原书第 4 章 · Loading Data into BigQuery）

> 章首注：原书页区间 ⚠️ 推定 p.105–144；一级章题 ✅ 目录实抓；**本章二级小节 ⚠️ 推定**——
> 按配套代码 `04_load/` ✅ 实抓文件族（load_from_local.sh / load_from_gcs.sh / load_external_gcs.sh /
> setup_data_transfer.sh / dataflow.ipynb / bigtable/ / college_scorecard.csv.gz / schema.json / query_temp_table.sh）
> 与官方 loading-data / write-api 文档页组织。

## 本章地图（⚠️ 推定结构，锚点为 ✅ 配套文件）

| 组 | 小节主题 | 锚点 |
| --- | --- | --- |
| 批量装载 | bq load（本地/GCS）、压缩与通配 URI、schema 探测与修正 | ✅ load_*.sh |
| 作业与并行 | LOAD 作业、写入离散性、批量上限（⚠️ 50 次/表/日） | ⚠️ |
| 外部表 | 挂 GCS/Bigtable 就地查、格式（CSV/JSON/Parquet/ORC） | ✅ load_external_gcs.sh |
| 流式 | Tabledata insertAll（2019 主角）→ Streaming insert 约束 | ⚠️ |
| 管道 | Dataflow/Beam 落库、Data Transfer Service 托管拉取 | ✅ dataflow.ipynb、setup_data_transfer.sh |
| 模式演化 | schema.json 手订 vs autodetect、字段放宽/收紧 | ✅ schema.json |
| 校验与清洗 | 装载后 SELECT 体检、脏值 CAST 策略 | ✅ queries.txt |

## 核心精讲

### 1. 三条装载正路（⚠️ 转述 + ✅ 配套脚本）

| 路径 | 载体 | 适用 |
| --- | --- | --- |
| `bq load` / LOAD 作业 | 本地文件、GCS（含 `*.gz`、通配 `sales_20*`） | 批量、冷启动 |
| 外部表 | GCS/Bigtable 对象**不搬家**直查 | 湖式访问、低频数据 |
| insertAll / Storage Write API | 行级 JSON / Arrow 二进制流 | 近实时管道 |

✅ 配套仓库 `04_load/college_scorecard.csv.gz + schema.json + load_from_gcs.sh` 完整演示" gz CSV → 显式 schema → LOAD 作业"，
并配 `college_scorecard` 查询族（✅ queries.txt 实抓：`CAST(SAT_AVG AS FLOAT64) > 1300` 式的装载后体检——
"先 STRING 装下再 CAST 过滤"是原书刻意示范的容错装载姿势）。

### 2. 通配 URI 与装载原子性（⚠️ 转述 + 🔧 类比）

`bq load 'proj:ds.tbl' 'gs://bucket/logs_*.csv.gz' schema.json` 一次吞多文件；失败文件进 bad file 统计。
🔧 **DuckDB 1.5.5 无 BigQuery 语义可比的部分**（通配装载原子性属托管作业面，本机不可测 ⚠️），
但"glob 多文件→并集视图"的查询侧近似本册 [06-BigQuery架构.md](06-BigQuery架构.md) 的 T6 实验已给（union_by_name）。

### 3. 流式约束与"2019 时代的痛"（⚠️ 转述）

insertAll 的配额（批次大小/频率/缓冲可见延迟）、恰好一次语义缺失（2019 无 Streaming Buffer 概念 ⚠️ 演进见下节）——
原书给出的处方是"高频小批改微批+Dataflow"。配套 `dataflow.ipynb` ✅ 即 Beam→BQ 落库的 Colab 演示；
Bigtable 外部表/导出（✅ `04_load/bigtable/`）承接"操作型库→分析库"的旁路。

### 4. Data Transfer Service（✅ 配套 setup_data_transfer.sh）

托管的 SaaS 拉取（GitHub/Ads/Sheets/Salesforce 等）⚠️：定时、幂等、坏数据容忍由平台管。
配套仓库另有 Google Sheets 直灌样例（✅ `sheets_data.csv` 与 README 更新文章"Loading complex CSV files
into BigQuery using Google Sheets" ✅ URL 见云博客，2026-09 未逐条 curl 复核 → 引用只到题 ⚠️）。

### 5. 模式演化纪律（⚠️ 转述）

- 字段可**放宽**（NULLABLE 化、新增字段、REPEATED→ARRAY 同构）不可随意收紧；
- autodetect 只用于探索，生产必配显式 schema（✅ 配套 schema.json 的存在即原书立场）；
- 与 09 章呼应：ML 特征 schema 漂移是 BQML 训练事故主因。

### 6. 装载后校验 SQL 模式（✅ 配套仓库 queries.txt）

配套仓库 `04_load/queries.txt`（✅ 实抓）给出一组装载后体检 SQL：

```sql
-- 配套仓库风格示意（非原书文本）
-- 空值率检查
SELECT COUNT(*) AS total, COUNTIF(col IS NULL) AS nulls,
       COUNTIF(col IS NULL) / COUNT(*) AS null_rate
FROM dataset.loaded_table;

-- 类型边界检查
SELECT MIN(CAST(amount AS FLOAT64)) AS min_amt,
       MAX(CAST(amount AS FLOAT64)) AS max_amt
FROM dataset.loaded_table;
```

⚠️ 装载后体检是**数据质量第一道防线**——在 MERGE/物化之前拦截脏数据。
03 章的 `SAFE_CAST` 在此场景的用法：先全 STRING 入场（✅ 配套示范），查询期用 `SAFE_CAST` 过滤转换失败行。

## 常见误区（⚠️ 转述）

| 误区 | 事实 |
| --- | --- |
| 外部表=导入 | 外部表每次查询都重读源，费用按扫描计；高频用请物化（CTAS） |
| 装载会去重 | LOAD/流式都不管重复；幂等靠 DELETE+INSERT/MERGE（08 章） |
| gz 解压再传 | 直接装 `.gz`（✅ 配套就是 gz），引擎侧解压 |
| 流式立即可见 | 缓冲可见延迟存在；对账用分区落库或 Write API（⚠️ 2026 已大幅收敛，见下节） |
| CSV 全用 STRING 是偷懒 | ✅ 配套示范：先全 STRING 入场 + 查询期 CAST 是**反脏数据模式**的正解之一 |

## 与其他章、其他书联系

- 装载后性能/成本 → [07-性能与成本优化.md](07-性能与成本优化.md)；MERGE/事务性修正 → [08-高级查询.md](08-高级查询.md)。
- 流式接入全谱系（Kafka/PubSub/反压）：[../bigdata/08-消息中间件与数据接入.md](../bigdata/08-消息中间件与数据接入.md)、
  [../bigdata/07-实时计算与流式架构.md](../bigdata/07-实时计算与流式架构.md)；管道工程观：[../bigdata/12-数据质量与工程实践.md](../bigdata/12-数据质量与工程实践.md)。
- 湖仓直读对照（Delta/Iceberg 外部表同源思想）：[../Delta_Lake_Definitive_Guide/00-总览与阅读地图.md](../Delta_Lake_Definitive_Guide/00-总览与阅读地图.md)（该目录在盘 ✅，若波尾改名由主代理修链）。
- 云仓对读：Snowflake 装载宇宙（COPY INTO/Snowpipe）[../Snowflake_The_Definitive_Guide/06-数据加载与卸载.md](../Snowflake_The_Definitive_Guide/06-数据加载与卸载.md)；Trino/Presto 连接器视角 [../Trino_The_Definitive_Guide_2e/06-连接器.md](../Trino_The_Definitive_Guide_2e/06-连接器.md)、[../Presto实战/06-连接器.md](../Presto实战/06-连接器.md)。
- 文件格式层原理补课：[../bigdata/09-存储与文件格式.md](../bigdata/09-存储与文件格式.md)、[../数据库系统概念6/10-存储和文件结构.md](../数据库系统概念6/10-存储和文件结构.md)。

## 核心概念速览（中英对照）

| 术语 | English | 释义 |
| --- | --- | --- |
| 装载作业 | load job | 异步批量导入单元（bq load/LOAD 语句/API） |
| GCS | Google Cloud Storage | 对象存储，批量装载主通道 |
| 通配 URI | wildcard URI | `*.csv.gz` 式多文件一次装载 |
| 外部表 | external table | 指向 GCS/Bigtable 的零拷贝查询视图 |
| 模式自动探测 | schema autodetect | 采样推断列型，仅限探索使用 |
| 显式模式 | explicit schema | 生产装载纪律：schema.json 先行 |
| 流式插入 | streaming insert (insertAll) | 行级 JSON 近实时入口（2019 主角） |
| 缓冲期 | streaming buffer | 流式数据可见前的暂存层（⚠️ 术语转述） |
| Dataflow | Cloud Dataflow | 托管 Beam 执行器，ETL 主力 |
| Beam | Apache Beam | 统一批/流编程模型 |
| DTS | Data Transfer Service | SaaS/云存储定时拉取托管 |
| 坏文件 | bad file | 装载中被拒记录的去向，配额告警对象 |
| CTAS | CREATE TABLE AS SELECT | 外部表物化/结果固化的常用句 |

## 最新演进与工业实践

- **Storage Write API 取代 insertAll 成流式正解**（✅ docs.cloud.google.com/bigquery/docs/write-api，cn 镜像 200）：
  Arrow 二进制、exactly-once 流、低延迟可见；官方 loading-data 总览页 ✅（.../docs/loading-data）。
- **Iceberg 托管表 = 装载目标开始"开放化"**：2026-07-13 版本说明（✅ 实抓）宣布 Apache Iceberg 托管表的
  表分区、多语句事务、advanced runtime 全 GA；BigLake 品牌并入 "Google Cloud Lakehouse"（✅ 实抓），
  装载/直读的边界进一步糊化——原书"外部表 vs 托管表"二分在 2026 已是光谱。
- **跨云装载/直查**：BigQuery Omni + lakehouse connections（✅ .../docs/omni-introduction；2026 版说明新增
  AWS Glue 直查条目 ✅）、SAP BDC 经 Iceberg REST Catalog 双向互通（✅ 实抓）——"接入"从 GCP 内题变成多云题。
- **管道即 SQL**：Dataform 托管 SQL 管道（✅ 配套仓库 README 更新文章 ✅ 原文 URL）、BigQuery 侧
  "Data Engineering Agent" 2026 GA（✅ 实抓）：自然语言搭管道，本章的脚本族正被 agent 编排。
- 工业实践：批+流双写的幂等收敛靠"分区覆盖 + MERGE"（08 章），对读湖仓线同题方案
  [../Apache_Paimon_Streaming_Lakehouse/00-总览与阅读地图.md](../Apache_Paimon_Streaming_Lakehouse/00-总览与阅读地图.md)（盘上 ✅）。
