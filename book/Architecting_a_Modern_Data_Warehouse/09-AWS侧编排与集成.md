# 09 AWS 侧编排与集成 — Data Orchestration Techniques C 段（原书第 5 章之 AWS 半边，章级 ✅）

> 段归属 ⚠️ 推定（Ch5 双云并写）。机制 ⚠️ 转述 + ✅ URL（docs.aws.amazon.com 域，2026-10-02 验 200）；
> 云服务不可本机实测；🔧G5 复引为 python 模拟，**非 AWS 平台行为**。
> 波内辨析：AWS 单云数据架构纵深归 #147《Modern Data Architecture on AWS》（同波只登记不链，00 §5）；
> 本册仅取「多云拼件」视角；Redshift 引擎面让位盘上两册（对位联动见 03 章）。

## 9.1 Step Functions：状态机正统（⚠️+✅）

✅ https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html。转述要点 ⚠️：
标准/快速两工作流型（至少一次 vs 恰好一次语义倾向）、ASL JSON 状态语言、
重试/捕获/补偿为一等构造——7.3 三公理里「重试+补偿显式化」在 AWS 侧的原生落点；
服务集成面直达 Glue/Lambda/Athena/EMR——「编排器只发令牌，执行在数据侧云内」的
教科书实现（7.1 三平面 AWS 版）。

## 9.2 Glue：目录+ETL+工作流三合一（⚠️+✅）

- 概览 ✅ https://docs.aws.amazon.com/glue/latest/dg/what-is-glue.html：无服务器连接/转换平台，
  Spark 引擎托管（波6 实证 pyspark 本机不可装——引擎侧一律 ⚠️，禁 🔧 冒充）；
- 目录 ✅ https://docs.aws.amazon.com/glue/latest/dg/catalog-and-crawler.html：爬取器生成表元数据——
  04 章三条件之「目录」的 AWS 实体（10 章三角候选之一）；
- Glue Workflows：触发器+条件+活动——AWS 侧的轻量 DAG 门面，与 Step Functions 的分工
  （管道内步骤 vs 全局控制流）为通说 ⚠️；
- Glue 连接/开发端点：网络孔位对 ADF 自托管 IR 的最近邻（8.5 端点表右列，⚠️）。

## 9.3 摄入族：DMS·零 ETL·流式（⚠️+✅）

- **DMS** ✅ https://docs.aws.amazon.com/dms/latest/userguide/Welcome.html：同构/异构迁移+CDC——
  02 章摄入层主件；
- **零 ETL**（⚠️ 概念转述；盘上配方实证链 [../Amazon_Redshift_Cookbook_2e/10-ZeroETL与LakeFormation统一授权.md](../Amazon_Redshift_Cookbook_2e/10-ZeroETL与LakeFormation统一授权.md)）：
  Aurora/DynamoDB/Kinesis→Redshift 托管复制——「先湖后仓」教条的短路件（04 章演进同条）；
- **流式三件套** Kinesis/MSK/Lambda（⚠️ 名目转述，专页本次未逐条验真——登记）：
  事件触发面（7.2 事件端）的 AWS 执行体；运营口径：事件只携带指针，重数据走 S3 路径
  （7.1 旁路护栏在 AWS 的纪律化）。

## 9.4 🔧 复引 E-G5：AWS 语义下的依赖与重试（非 AWS 行为）

07 章 G5 实验（5 作业、validate 注入失败、终序 extract>validate>transform>quality>publish、
尝试 6 次/122ms）在此给 AWS 读法 ⚠️：Step Functions 的 Retry（退避+jitter）对应尝试数增长、
Catch 对应补偿支路、`Path` 并行+`Join` 对应 quality/publish 双依赖边；Glue Workflow 的
条件触发对应「失败阻塞下游」默认行为。**云上重试是计费事件**（状态转换计费 ⚠️）——
🔧 里 122ms 的廉价重试在账单上是另一回事（07 章 7.5 计费纪律的 AWS 侧注脚）。

## 9.5 Athena/Redshift 的编排接口角色（⚠️+✅，对位表联动）

- Athena ✅ https://docs.aws.amazon.com/athena/latest/ug/what-is.html：联邦查询面的编排端——
  作为 Step Functions 服务集成活动被调度，低频探查场景即 🔧G1 联邦税的 AWS 侧账单化
  （按扫描字节计费，08 章 8.4 同构结论）；
- Redshift ✅ https://docs.aws.amazon.com/redshift/latest/mgmt/welcome.html：Data Share/工作负载管理
  由 03 章对位表管辖；编排视角只留两接口：**Data API**（无驱动 SQL 通道，Step Functions/Lambda
  的落点 ⚠️）与**事件通知**（COPY/分析作业完成事件回总线 ⚠️）。

## 9.6 双云编排对照速查（⚠️ 重构，8/9 两章收口）

| 职能 | Azure 件（08） | AWS 件（09） | 中立件 |
|---|---|---|---|
| 全局控制流 | ADF 管道+触发器 | Step Functions 标准工作流 | Databricks Jobs（两云同 API，⚠️✅AZ6） |
| 数据搬运 | ADF Copy/数据流 | Glue Job/DMS | DataX 类自研（⚠️ 书外注） |
| 目录 | Purview Data Map ✅AZ3 | Glue Catalog ✅AWS10 | Unity Catalog（⚠️ 三角第三方，10 章） |
| 探查面 | Synapse serverless ⚠️ | Athena ✅AWS3 | Trino（盘上实链 04 章） |
| 生产仓面 | Synapse 专用池 ✅AZ8 | Redshift ✅AWS1 | Snowflake（盘上两册） |
| 事件总线 | Event Grid ⚠️ | EventBridge/SNS ⚠️ | — |

结论（⚠️ 推定书中倾向）：两云件**按职能成对采购、按域择主**，6.4 域注册表裁决归属；
跨云边一律走「令牌+指针」纪律（7.1/9.3）。

## 9.7 本章学习检查点（⚠️ 推定）

1. Step Functions 的 Retry/Catch/Join 三构造各对应 🔧G5 的哪个观测值；
2. 说出「Glue Workflow 管管道内、Step Functions 管全局」划界的失效场景（重 DAG 全在 Glue 系内时）；
3. 9.6 表任选一列，写出其「中立件替代」对身份/计费/技能栈三项的连锁影响。

## 9.8 AWS 对象速查（⚠️ 转述 ✅AWS4/AWS2/AWS9/AWS3 域）

| 对象 | 一句话 | 本册挂点 |
|---|---|---|
| Standard/Express 工作流 | 全局控制流两档：可靠 vs 高频轻量 | 9.1/🔧G5 |
| ASL | 管道的状态机方言 | 7.4 即代码 |
| Glue Job | 托管 Spark 转换载体 | 9.2（引擎本机不可装 ⚠️） |
| Crawler | 目录进件器 | 10.2 Glue 角 |
| Workflow | 湖内轻 DAG | 9.2 分工线 |
| DMS 任务 | 异构迁移+CDC | 9.3 摄入主件 |
| Athena 工作分组 | 查询隔离+用量控制 | 9.5（名目 ⚠️） |

## 9.9 AWS 侧误读四条（⚠️ 编者注）

1. 「Glue≈ADF 的 AWS 版」——Glue 重心在目录+湖上计算，ADF 在搬运+全局触发（9.6 行分工）；
2. 「Step Functions 编排一切」——重搬运沉到 Glue/DMS，状态机只发令牌（7.1 军规重申）；
3. 「零 ETL 消灭管道」——短路件只覆盖指定源型，跨云边仍需合同（9.3/11.5 最小切片）；
4. 「Athena 慢」——慢的是账单形状不是引擎（🔧G1；缓存/物化频率纪律是解药，12.5 同构）。
五条之外补一条编者注 ⚠️：本章所有平台名目以 00 §8 验 200 清单为引用上限，未列者一律 ⚠️ 面。

## 9.10 读后回环三问（自测 ⚠️）

1. 你司全局控制流现在是「双大脑」吗（Step Functions 与 Glue Workflow 互为上游）？
   有——按 7.7 军规一行裁掉一个（⚠️ 实践高发题）；
2. DMS 与零 ETL 的边界：哪些源在「指定源型」名单外？名单外的合同谁签（9.3/11.5）；
3. 把 🔧G5 的 6/5 尝试比换成你司 Step Functions 的重试放大率：现在监控的是完成率还是尝试率？

## 核心概念速览（中英对照）

| 中文 | 英文 | 一句话 |
|---|---|---|
| Step Functions | AWS Step Functions | 托管状态机编排：ASL/标准与快速工作流（✅AWS4） |
| Glue | AWS Glue | 目录+无服务器 ETL+工作流三合一（✅AWS2） |
| 爬取器 | Crawler | 采样生成表元数据的目录进件器（✅AWS10） |
| DMS | Database Migration Service | 同/异构迁移与 CDC 托管件（✅AWS9） |
| 零 ETL | Zero-ETL | 源库直落仓的托管复制族（⚠️ 9.3） |
| Athena | Amazon Athena | 湖上按扫描计费的联邦 SQL 面（✅AWS3） |
| Data API | Redshift Data API | 无驱动程序化 SQL 通道（⚠️ 9.5） |
| 服务集成 | Service Integration | 编排器直达执行服务的令牌式调用（9.1） |
| 退避重试 | Exponential Backoff with Jitter | 平台化重试策略的标准形（9.4） |
| 职能成对 | Paired Capability Procurement | 9.6 结论：按职能对表、按域裁决 |

## 最新演进与工业实践

- **DMS Serverless 与零 ETL 扩容**（2024–，⚠️ 时间转述；✅ https://docs.aws.amazon.com/dms/latest/userguide/Welcome.html）：9.3 摄入族的运维面继续变薄，本册成书快照中仍占篇幅的自建 Glue 调度模式在 2026 工业口径里多已收敛为托管件（盘上 [../Amazon_Redshift_TDG/09-迁移到AmazonRedshift.md](../Amazon_Redshift_TDG/09-迁移到AmazonRedshift.md) 的迁移工具链同批更新）。
- **Step Functions 表达力补课**（⚠️ 转述；✅AWS4 现行文档树含测试/可观测分支）：状态机测试与分布式映射能力落地后，🔧G5 级自制模拟的「教学脚手架」属性增强、生产必要性下降——编排范式章（07）与本章的分工因此更清晰：07 管公理、09 管平台实现。
- **Glue 向「Iceberg 托管维护面」倾斜**（2024–2026 ⚠️；✅ https://docs.aws.amazon.com/glue/latest/dg/catalog-and-crawler.html 现行口径含表格式支持叙述）：05 章「表契约上移」趋势的 AWS 侧执行者——目录服务开始代管小文件合并/孤儿清理，medallion 运维成本进一步平台化。
- **MWAA/Composer 与 Airflow 资产的共存策略**（⚠️ 通说；本次未单独验真专页，登记为 ⚠️ 面）：既有 Airflow 代码库的大企业常见选择是「托管 Airflow 跑域内 DAG、Step Functions 跑全局控制流」——9.6 表在「存量 Airflow」权重下增加一行历史包袱注记（盘上对位 [../Amazon_Redshift_Cookbook_2e/05-ETL编排_Airflow与StepFunctions.md](../Amazon_Redshift_Cookbook_2e/05-ETL编排_Airflow与StepFunctions.md)）。
