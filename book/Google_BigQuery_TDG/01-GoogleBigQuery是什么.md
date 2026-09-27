# 01 Google BigQuery是什么（原书第 1 章 · Introduction to BigQuery）

> 章首注：原书页区间 ⚠️ 推定 p.1–24；本章证据密度最高——**二级目录为中译本目录实抓 ✅**（读书网照录），
> 配套代码 `01_intro/queries.txt`、`all_code.txt` ✅ 实抓（本文引用处标"配套仓库"）。全部机制转述标 ⚠️。

## 本章地图（✅ = 中译本目录实抓的小节；⚠️ = 依官方文档主题推定的展开顺序）

| 小节 | 主题 | 证据 |
| --- | --- | --- |
| 数据处理架构 | 数仓/报表/即席分析在数据栈中的位置 | ✅ 目录实抓 |
| 关系数据库管理系统 | 传统 RDBMS 数仓为何在 PB 级失速 | ✅ 目录实抓 |
| MapReduce 框架 | Google 第一代大规模批处理及其延迟局限 | ✅ 目录实抓 |
| BigQuery：Serverless、分布式 SQL 引擎 | 本书对 BigQuery 的定义句 | ✅ 目录实抓 |
| 使用 BigQuery：从数据集中获得洞察 | citibike 骑行 + 天气关联分析主线案例 | ✅ 目录实抓 + 配套仓库 |
| ETL、EL 和 ELT | 装载范式的三分与云仓语境下的迁移 | ✅ 目录实抓 |
| 强大的分析能力 / 易于管理 | SQL 面 + 无运维面 | ✅ 目录实抓 |
| BigQuery 起源 | Dremel 论文（VLDB 2010）→ 商业化 | ✅ 目录实抓 |
| 计算和存储分离 / 存储和网络基础设施 / 存储托管 | Colossus 与高速网络底座 | ✅ 目录实抓（细节 ⚠️ 转述） |
| 与 Google Cloud Platform 集成 / 安全与合规 | GCP IAM/网络/审计一体 | ✅ 目录实抓 |

## 核心精讲

### 1. 一句话定位与其代价（⚠️ 转述 + ✅ URL）

BigQuery 是 Google Cloud 的**全托管 serverless 分析型数仓**：存算分离、按用量计费、SQL 原生、
扩展透明。官方概览 ✅（https://docs.cloud.google.com/bigquery/docs/introduction ，cn 镜像 2026-09-27 验 200）：
"fully managed, petabyte-scale, cost-effective analytics data warehouse"。
对读者的直接后果：**你优化的是"如何少扫数据"，不是"如何调服务器"**——这决定了 06/07 两章的全部世界观。

### 2. 从 RDBMS 与 MapReduce 的失败面切入（⚠️ 转述）

- 传统 MPP/RDBMS 数仓：schema、索引、物化视图、分区都要人肉经营，扩容≈重采购。
- MapReduce：能扩，但**每问一次写一遍盘**，交互式分析（秒级响应）不可能。
- Dremel 论文给出的第三条路：列式压缩存储 + 短查询向量化执行 + 树状扇出聚合，
  跑在 Colossus 共享存储上。精读条目见 [../../paper/doi_10.14778_1920841.1920886/00-精读笔记.md](../../paper/doi_10.14778_1920841.1920886/00-精读笔记.md)，论文索引 [../../db/db.md](../../db/db.md)。
  对照 Hadoop 系同期演进：[../bigdata/10-计算引擎的演进.md](../bigdata/10-计算引擎的演进.md)。

### 3. 主线案例：雨天人少骑车吗？（✅ 配套仓库 01_intro/all_code.txt 实抓）

原书第一章就带读者在公共数据集上跑真分析，配套仓库原文（`bigquery-public-data.new_york_citibike.citibike_trips`
与 `ghcn_d.ghcnd_2016` 天气表做 CTE 关联，节选）：

```sql
WITH bicycle_rentals AS (
  SELECT COUNT(starttime) AS num_trips, EXTRACT(DATE FROM starttime) AS trip_date
  FROM `bigquery-public-data.new_york_citibike.citibike_trips`
  GROUP BY trip_date
), rainy_days AS (
  SELECT date, (MAX(prcp) > 5) AS rainy
  FROM (SELECT wx.date AS date,
               IF(wx.element = 'PRCP', wx.value/10, NULL) AS prcp
        FROM `bigquery-public-data.ghcn_d.ghcnd_2016` AS wx
        WHERE wx.id = 'USW00094728')
  GROUP BY date
)
SELECT ROUND(AVG(bk.num_trips)) AS num_trips, wx.rainy
FROM bicycle_rentals AS bk JOIN rainy_days AS wx ON wx.date = bk.trip_date
GROUP BY wx.rainy
```

> 输出（✅ 配套仓库注释记录的样例结果）：晴天日均约 39107 单、雨天约 32052 单。
> 要点：**引用公共数据集不需要账号、不导数据**——"ELT 里 T 在仓内、数据先搬进来再建模"的范式演示（配套仓库 `04_load` 承接）。

### 4. ETL / EL / ELT（✅ 目录实抓，⚠️ 概念转述）

| 范式 | 变形/清洗发生地 | 云仓后果 |
| --- | --- | --- |
| ETL | 入库前管道内 | 管道复杂、原始数据可能丢失 |
| EL | 不转换，直接堆 | 湖变泥潭（repo 数据治理线吐槽点，见 [../Data_Mesh/00-总览与阅读地图.md](../Data_Mesh/00-总览与阅读地图.md)） |
| ELT | 仓内 SQL 按需变形 | BigQuery 主推姿势：先装载、后用视图/脚本加工 |

### 5. 底座三件套（⚠️ 转述，官方无源码级承诺）

计算存储分离（存储 Colossus / 计算槽位池）、网络基础设施（原书提"40Gb 网络与专用路由"级别描述）、
存储托管（列式、自动压缩编码、用户不可见物理布局）。与 Snowflake 三层架构对读：
[../Snowflake_The_Definitive_Guide/02-架构与虚拟仓库.md](../Snowflake_The_Definitive_Guide/02-架构与虚拟仓库.md)；
开源对照：[../Trino_The_Definitive_Guide_2e/04-Trino架构.md](../Trino_The_Definitive_Guide_2e/04-Trino架构.md)、
[../Presto实战/04-Presto的架构.md](../Presto实战/04-Presto的架构.md)。

## 常见误区（⚠️ 转述口径）

| 误区 | 事实 |
| --- | --- |
| "BigQuery 要建索引/分区表才能快" | 全表扫描即基线能力；速度靠列存+裁剪，分区/聚簇是**可选优化**（07 章） |
| "像 MySQL 一样有连接池/长事务" | 作业制（job）模型，DML 事务性有窗口限制（08/09 章） |
| "serverless=不计费" | 按需/槽位两模式都在为字节与秒付费（07 章） |
| "数据必须先在 GCS" | 支持本地/Sheet/Bucket/Bigtable/跨云多种入口（04 章） |

## 与其他章、其他书联系

- 本章的"起源/底座"在 [06-BigQuery架构.md](06-BigQuery架构.md) 展开；"SQL 面"从 [02-基础查询语法.md](02-基础查询语法.md) 开始；"装载面"接 [04-将数据加载到BigQuery.md](04-将数据加载到BigQuery.md)。
- 数仓在决策支持谱系中的位置：[../Building_the_Data_Warehouse/00-总览与阅读地图.md](../Building_the_Data_Warehouse/00-总览与阅读地图.md)（Inmon 派 vs 云仓派对照）。
- 并行/分布式底座通识：[../数据库系统概念6/18-并行数据库.md](../数据库系统概念6/18-并行数据库.md)、[../数据库系统概念6/19-分布式数据库.md](../数据库系统概念6/19-分布式数据库.md)、[../设计数据密集型应用/00-总览与阅读地图.md](../设计数据密集型应用/00-总览与阅读地图.md)。
- 云仓兄弟：[../Snowflake_The_Definitive_Guide/01-开始上手.md](../Snowflake_The_Definitive_Guide/01-开始上手.md)（同为"第一课"的镜像体例）；同波 `Amazon_Redshift_TDG`、`Advanced_Snowflake` **仅登记不链**（见 00 互链表）。

## 核心概念速览（中英对照）

| 术语 | English | 释义 |
| --- | --- | --- |
| 无服务器数仓 | serverless data warehouse | 用户不预置/不管理任何计算集群的分析仓库 |
| 存算分离 | disaggregated storage and compute | 存储与计算独立扩缩，各自成池 |
| 列式存储 | columnar storage | 按列物理布局+压缩编码，分析只读所需列 |
| 数据仓库 | data warehouse | 面向分析的结构化数据中央库（vs 交易库） |
| 即席查询 | ad-hoc query | 未预定义的交互式分析查询 |
| ELT | extract-load-transform | 先装载后在仓内转换的管道范式 |
| Dremel | Dremel | BigQuery 引擎的学术前身，VLDB 2010 论文 |
| Colossus | Colossus | GFS 后继的 Google 分布式存储底座 |
| 公共数据集 | public datasets | `bigquery-public-data` 项目下免申请可查的数据集 |
| 项目 | project | GCP 资源与计费边界，BigQuery 表按项目-数据集-表三级寻址 |
| 作业 | job | BigQuery 执行单元（查询/装载/导出/复制），异步+轮询 |
| 槽位 | slot | BigQuery 的计算并行度计量单位（07 章主场） |
| 多租户 | multi-tenancy | 共享物理池、逻辑隔离（安全面见 10 章） |

## 最新演进与工业实践

到 2026 年，"第 1 章是什么"的答案已被官方扩容（以下事实均出自 2026-09-27 实抓的官方版本说明，✅ cn 镜像 200）：

- **平台叙事从"数仓"改为"AI-ready data platform / 数据云"**：BigQuery 概览页（✅ docs.cloud.google.com/bigquery/docs/introduction）现把 Gemini 对话式分析（conversational analytics，2026-07 支持 `AI.AGG` 函数、HIPAA 合规）列为一级能力。
- **版本/商务分层**：Enterprise / Standard 等 editions 成为计费与能力矩阵的骨架（版本说明 2026 条目以 editions 区分可用性 ✅）；免费侧有沙盒（✅ docs.cloud.google.com/bigquery/docs/sandbox：绑定信用卡前的无额度试跑）。
- **多模态分析进第 1 章射程**：图查询可视化（2026-04 ✅）、向量搜索/混合检索（`VECTOR_SEARCH` hybrid 模式 2026-07 GA ✅）、地理空间延续——原书"强大分析能力"一节在 2026 被显著改写。
- **开放化**：Apache Iceberg 托管表持续补强（2026-07 分区/多语句事务/advanced runtime GA ✅），BigLake 已并入 "Google Cloud Lakehouse" 品牌（2026 ✅），跨云经 BigQuery Omni 与 lakehouse connections（✅ docs.cloud.google.com/bigquery/docs/omni-introduction）。原书 2019 语境下"闭源托管存储"的第一章叙事，2026 已变成"托管+开放格式双轨"。
- 工业实践：三巨头对读建议以本册 06/07 + [../Snowflake_The_Definitive_Guide/12-数据云工作负载.md](../Snowflake_The_Definitive_Guide/12-数据云工作负载.md) 为基准（Redshift 侧待同波 #178 落盘后由主代理回填对链）。
