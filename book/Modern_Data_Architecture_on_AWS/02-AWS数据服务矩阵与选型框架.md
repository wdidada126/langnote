# 02 AWS 数据服务矩阵与选型框架 — The AWS Analytics Service Matrix（⚠️ 主题重构章）

> 章题为 ⚠️ 主题重构（[00](00-总览与阅读地图.md) §3）；服务定位描述 = 官方文档转述 ⚠️ +
> ✅ URL（2026-10-02 逐条 200，清单见 00 §7）；不可实测，🔧 类比**非 AWS 行为**。

## 2.1 一张矩阵看全槽位

| 槽位 | 服务 | 一句话定位（⚠️ 转述官方 what-is 口径） | ✅ 锚页 |
| --- | --- | --- | --- |
| 对象底座 | S3 | 无限规模的对象存储，一切分析服务的公分母 | `AmazonS3/latest/userguide/Welcome.html` |
| 流缓冲 | Kinesis Data Streams | 分片式追加日志，毫秒级多消费者 | `streams/latest/dev/introduction.html` |
| 托管投递 | Kinesis Data Firehose | 免运维的「流→湖/仓」管道 | `firehose/latest/dev/what-is-this-service.html` |
| 消息骨干 | MSK | 托管 Kafka，兼容开源生态 | `msk/latest/developerguide/what-is-msk.html` |
| 变更捕获 | DMS | 异构库间 CDC 复制 | `dms/latest/userguide/Welcome.html` |
| 目录/ETL | Glue | 托管目录 + 无服务器 ETL 平台 | `glue/latest/dg/what-is-glue.html` |
| 集群计算 | EMR | 托管 Hadoop/Spark 生态 | `emr/latest/ManagementGuide/emr-what-is-emr.html` |
| 轻计算 | Lambda | 事件函数，转换胶水 | `lambda/latest/dg/welcome.html` |
| 交互查询 | Athena | 湖上按扫描计费的 serverless SQL | `athena/latest/ug/what-is.html` |
| 云仓 | Redshift | MPP 数仓（预置/Serverless 双形态） | `redshift/latest/mgmt/welcome.html` |
| BI | QuickSight | 云端 BI 与嵌入式分析 | `quick/latest/userguide/what-is.html` |
| ML | SageMaker | 建模-训练-部署全链 | `sagemaker/latest/dg/whatis.html` |
| 权限 | Lake Formation | 湖上集中细粒度授权 | `lake-formation/latest/dg/what-is-lake-formation.html` |
| 域目录 | DataZone | 数据产品/域治理门户 | `datazone/latest/userguide/what-is-datazone.html` |
| 编排 | Step Functions / MWAA | 状态机 DAG / 托管 Airflow | `step-functions/latest/dg/welcome.html`、`mwaa/latest/userguide/what-is-mwaa.html` |
| 事件 | EventBridge | 规则路由的事件总线 | `eventbridge/latest/userguide/eb-event-bus.html` |
| 流计算 | Managed Flink | 开源 Flink 托管运行面 | `managed-flink/latest/java/what-is.html` |

（S3 路径订正登记：QuickSight 旧路径 `quicksight/latest/user/welcome.html` 301 迁移至
`quick/…`，00 §7 已录——引用前验链是本波纪律。）

## 2.2 选型四问（⚠️ 方法论重构）

1. **延迟预算是什么？** 秒内→KDS+Flink；分钟→Firehose/EventBridge+Lambda；小时/天→Glue/EMR 批。
   延迟每降一个量级，运维面与单价都跳档——先给 SLA 再给架构图。
2. **数据形态是什么？** 强 schema 事务源→DMS/Zero-ETL 直入仓；半结构化日志→湖优先（schema-on-read）；
   高吞吐事件流且生态已有 Kafka→MSK 而非 KDS（兼容性换一点性能上限 ⚠️）。
3. **团队技能货币是什么？** SQL 团队→Athena/Redshift 为主的 ELT；Python/Spark 团队→Glue/EMR；
   工具错配的管线没人维护，比服务选型错误更致命 ⚠️ 通识判断。
4. **成本模型匹配负载形态？** 稀疏即席→按扫描计费（Athena）；稳定高频→按容量预留（Redshift RI 语义 ⚠️）；
   脉冲→Serverless 弹性（13 章展开）。

## 2.3 三大典型组合

- **Lake-first**：源→Firehose/MSK→S3→Glue（转换）→Athena/Redshift Spectrum 消费。
  特征：先便宜地存一切，查询面后补；目录与权限（05/09）是成败手。
- **Warehouse-first**：源→DMS→Redshift→QuickSight。特征：治理天然（都在仓内 ACL），
  但非结构化与 ML 侧翼要另起炉灶 ⚠️。
- **Hybrid 湖仓**：01 章五段式全用上，以开放表格式为共同地面（12 章）。2022 年后 AWS 叙事
  明显向此收敛（S3 Tables/Zero-ETL 两枚落点 ✅，见 01 章演进节）。

## 2.4 集成面：箭头从哪里接

⚠️ 转述各页：Glue Catalog 是 Athena/Redshift Spectrum/EMR/Firehose 投递目标的**公共元数据面**
（✅ `glue/latest/dg/what-is-glue.html`）；Lake Formation 直接改写这一面的权限语义（✅
`lake-formation/latest/dg/access-control-overview.html`）；Firehose 以 S3/Redshift/ES 为托管终点
（✅ `firehose/latest/dev/what-is-this-service.html`）。工程推论：**目录=总线**，任何「服务 A 查
服务 B 数据」的问题先问「目录里有没有对方的表」⚠️。

## 2.5 托管 vs 自建（开源兼容）光谱

| 光谱位 | 例 | 换来什么 | 付出什么 |
| --- | --- | --- | --- |
| 全托管 serverless | Athena/Glue/Firehose | 零集群运维、按量 | 冷启动/配额/黑盒调优面小 ⚠️ |
| 托管集群 | Redshift 预置/EMR/MSK | 可调内核参数、稳态成本可测 | 版本与容量责任回到你 ⚠️ |
| 自建在 EC2 | Spark on EC2 | 极限自由 | 一切自己扛——仅当托管面确不满足 |

EMR 的存在本身说明 AWS 承认光谱中段需求（✅ `emr/latest/ManagementGuide/emr-what-is-emr.html`
把「运行开源框架」写成一级目标 ⚠️）。

## 2.6 🔧 类比锚（非 AWS 行为）

- 🔧E3 预告：本机用 DuckDB `information_schema` 一次目录查询 13.11ms 取回列结构、零数据扫描——
  「元数据面独立于数据面」直觉即 2.4 的最小模型（DuckDB 无网络面无鉴权，离 Glue 差整个控制面）。
- 2.2 之问 1 的直觉可用 🔧E4（04 章主场）校准：同一份「追加日志」，游标式增量读 2 万+条仅 2.0ms，
  全量重放则按行线性——**延迟档位差是架构给的，不是查询优化给的**。

## 2.7 反「服务清单式架构」声明

矩阵不是菜单。架构产物的合格线：每个箭头能回答「延迟预算/重放语义/权限传递/成本归因」四问；
答不出就删箭头。本册其后 11 章可视为对四问的逐层展开 ⚠️（重构叙事）。

## 2.8 选型答辩模板（⚠️ 重构，把 2.2/2.7 落成可填的表）

| 槽位 | 候选 | 延迟答 | 形态答 | 技能答 | 成本答 | 结论/契约 |
| --- | --- | --- | --- | --- | --- | --- |
| 摄入-订单库 | DMS / Zero-ETL / 应用双写 | | | | | |
| 交互查询 | Athena / Redshift / Flink 服务层 | | | | | |
| 转换-gold | Glue Spark / Glue Shell / EMR / SQL | | | | | |

填法 ⚠️：一行一次真实评审，**空着的格子=还没想清楚的格子**；「结论」列必须能改天
被单独推翻而不牵连相邻行（层独立性，01 章 §1.2 的落地形态）。

## 2.9 本章常见追问三则（⚠️ 重构）

- 「为什么不全 Serverless？」——2.5 光谱：稳态高频负载把弹性溢价白付三年（13.1 公理的
  镜像推论）；Serverless 是计费模型不是道德立场 ⚠️。
- 「能不能不用 Glue Catalog？」——能，但你将同时失去 Athena/EMR/Spectrum 的公共读面
  （2.4「目录=总线」的反证）；换目录=换总线，属架构级手术 ⚠️。
- 「OpenSearch/Neptune 等为何缺席 2.1？」——超出「数据架构」重构范围即登记不展开 ⚠️：
  矩阵章的纪律恰恰是**知道哪些盒子不摆上桌**。

## 核心概念速览（中英对照）

| 中文 | 英文 | 一句话 |
| --- | --- | --- |
| 服务矩阵 | Service Matrix | 槽位×候选的选型表 |
| 变更数据捕获 | Change Data Capture (CDC) | 从事务日志复制增量 |
| 分片日志 | Shard Log | 流服务的有序追加单元 |
| 按扫描计费 | Pay-per-scan | 查询成本=读字节定价 |
| 无服务器 | Serverless | 容量抽象到请求粒度 |
| 元数据总线 | Metadata Plane | 目录作为服务间公共面 |
| 延迟预算 | Latency Budget | 从 SLA 反推档位 |
| 数据产品 | Data Product | 域视角的对外契约单元 |
| ELT vs ETL | Extract-Load-Transform | 转换发生在目的地之后 |
| 托管光谱 | Managed Spectrum | 自由度与运维责任的连续统 |

## 最新演进与工业实践

2022→2026（✅ URL 全 200；⚠️ 转述）：

- **矩阵重心从「新增服务」转向「删箭头」**：Glue Zero-ETL（✅ `glue/latest/dg/glue-zero-etl.html`）
  把 DMS+批搬运两条箭头折叠为托管连线；S3 Tables（✅ `s3/latest/userguide/s3-tables.html`）把
  湖表维护（压缩/快照过期）从 ETL 箭头里吸走——选型四问的「箭头数量」维度在系统性下降。
- **Flink 升为流计算正主**：KDA（Spark Streaming 血统）淡出、Managed Flink 页 ✅ 存续，
  与盘上 [../Building_Real_Time_Analytics_Systems/00-总览与阅读地图.md](../Building_Real_Time_Analytics_Systems/00-总览与阅读地图.md) 的流批一体叙事合流。
- **目录面出现第三方竞争**：开放元数据/目录项目（盘上
  [../Apache_Polaris_TDG/00-总览与阅读地图.md](../Apache_Polaris_TDG/00-总览与阅读地图.md)，若名不符则按
  ls 实名订正）分流 Glue Catalog 的「唯一总线」地位 ⚠️——但 AWS 系消费服务默认仍读 Glue。
- **工业实践**：架构评审模板（Analytics Lens ✅ 六支柱）+ 四问四答（2.2/2.7）已成为跨云通用的
  数据平台准入检查表；#146 多云册主题（波内登记不链）正把此检查表推向 Azure/GCP 对偶面。
