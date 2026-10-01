# 06 湖上 ETL 与大规模处理 — Lake ETL & Large-Scale Processing（⚠️ 主题重构章）

> 章题为 ⚠️ 主题重构（[00](00-总览与阅读地图.md) §3）；Glue/EMR/Lambda 机制 = 官方文档转述 ⚠️ +
> ✅ URL；🔧 类比**非 AWS 行为**。

## 6.1 ETL 还是 ELT：湖上语境下这是个假两难

⚠️ 重构口径：着陆即原始格式（ELT 的 Load 先行），转换后置但**必须物化为分层表**
（bronze→silver→gold，即 05 章 §5.7 与 04 章 §4.7 的会师）。争论焦点不在字母顺序，
在「转换逻辑的**运行时**放哪、**契约**放哪」：运行时可选 Glue/EMR/Lambda/Athena CTAS，
契约永远在目录与表格式里 ⚠️。

## 6.2 Glue 平台三面（✅ `glue/latest/dg/what-is-glue.html`，⚠️ 转述）

- **Spark 运行时（jobs）**：托管 PySpark/Scala 容器，DPU 计量；连接/脚本/触发在 jobs 面。
- **Python Shell jobs**：boto 编排轻量转换——「Glue 不是只有 Spark」是成本课第一页 ⚠️。
- **Interactive/Notebook + workflows**：开发面与触发依赖面（workflows 图论并入 10 章）。
转换原语：DynamicFrame（容错记录单元 + applyMapping/ResolveChoice 三板斧 ⚠️）vs 直接
Spark DataFrame——**脏数据策略决定抽象层选择** ⚠️。

## 6.3 EMR：开源引擎的托管运行面

✅ `emr/latest/ManagementGuide/emr-what-is-emr.html`（⚠️ 转述）：托管 Hadoop/Spark/Hive/
Presto 集群；与 Glue 的分界不是「谁更托管」而是**引擎自由度与调参面**：需要特定 Spark
版本/Hive UDF/第三方 jar → EMR；纯 ETL 且无版本癖 → Glue ⚠️。Instance Fleet/托管伸缩、
EMR on EKS（⚠️ 概念登记，EKS 页本轮未验证不引 URL）。

## 6.4 Lambda 在 ETL 谱系里的合法位置

✅ `lambda/latest/dg/welcome.html`（⚠️ 转述）：限时限内存的函数面 ⇒ 只做「小、快、事件驱动」
的转换：解包/转码/校验/路由。超过分钟级或 GB 级内存需求就是**放错层**（该去 Glue Shell/
Firehose 内联，04 章 §4.3）⚠️。

## 6.5 转换的分层模板（medallion ⚠️ 通识重构）

- **Silver 三件事**：去重（按业务键+位点取最新）、类型规整（契约 cast 而非猜测）、
  迟到治理（事件时间分窗落分区，05 章分区键在此兑现）。
- **Gold 三件事**：聚合口径、维度退化、面向消费域的物化视图/汇总表。
- **反压设计** ⚠️：全量重算 vs 增量合并的分水岭在「分区数×日增速」——超过就走增量
  （merge/upsert 语义交表格式，12 章；Hudi/Iceberg 纵深链 04 章演进节已给 ✅ 在盘册）。

## 6.6 🔧 类比锚（**非 AWS 行为**）

- 6.5 的 silver 去重直觉可用 DuckDB 一句 `QUALIFY row_number() OVER(PARTITION BY k ORDER BY
  ts DESC)=1` 在本地 120 万行上秒级验证（tmp `exp.py` E2 数据集同源复用，改写即得）——
  **注意本机是无成本模型的单文件场景**，湖上该步的真实成本=扫描+重写双份（05 章 §5.3 恒等式）。
- 🔧E2（05 章）在 ETL 侧的镜像：增量转换的谓词若能落在分区列，Glue/Athena 的读放大与
  本地「1/12 文件」同构；谓词落在非分区列则是全量重扫——**转换切分跟着分区键走**是
  两章共用的唯一硬规则 ⚠️。

## 6.7 规模故障手册（⚠️ 通识清单）

小文件爆炸（写侧高频提交 → compaction 计划，S3 Tables 化后托管 ⚠️）、热点键（加盐/两阶段
聚合）、倾斜 join（广播小表/热点分离）、失败重跑不幂等（回到 03 章 §3.7 清单提交契约）——
每一条的「发现」归 10 章观测、「治疗」归本章运行时选择 ⚠️。

## 6.8 与仓内转换的分工线

Redshift 内 COPY+SQL 转换（07 章）承接「进仓后」的逻辑；湖侧 Glue 承接「进仓前」的逻辑。
2024+ Zero-ETL 模糊了边界（数据先到仓再到湖/反向 ⚠️，✅ `glue/latest/dg/glue-zero-etl.html`），
但**重聚合放仓、重清洗放湖**的成本直觉仍成立（13 章给算账法）⚠️。盘上仓侧纵深：
[../Amazon_Redshift_Cookbook_2e/03-表设计与装载转换配方.md](../Amazon_Redshift_Cookbook_2e/03-表设计与装载转换配方.md)
（✅ ls 验名在盘）。

## 6.9 引擎选择小抄（⚠️ 重构，6.2–6.4 的可打印版）

| 特征 | 选 | 口诀 |
| --- | --- | --- |
| 分钟级小转换、无重计算 | Lambda/Shell | 胶水不上火（6.4） |
| 标准清洗+目录联动 | Glue Spark | 契约在目录（6.1） |
| 特定引擎版本/UDF/第三方件 | EMR | 自由度买单（6.3） |
| 纯 SQL 可表达、消费即转换 | Athena/Redshift CTAS | 少一个运行时（6.8） |

## 6.10 一次真实形状的转换推演（⚠️ 重构示例，非书中案例）

银层去重日任务：着陆 200 分区×12MB/日，DMS 文件含重放副本。步骤：①谓词只取当日
分区（🔧E2 的 1/12 直觉外推）；②`row_number` 去重（6.6 第一锚）；③按业务域写回
gold 增量分区（05 章键设计）；④失败=整分区重跑（03 §3.7 提交契约使重跑幂等）；
⑤metrics 上报运行时长+输入字节（13.2 归因）。**每一步的可失败性都在前章埋过单**——
本章是把 03–05 章的债在运行时结清的总账房 ⚠️。

## 6.11 转换层复盘四问（⚠️ 重构自测）

1. 你的转换代码进 git 了吗？dry-run 于采样数据进 CI 了吗？（6.10 演进纪律条）
2. 每条管线能一句话说出「增量边界」吗？（6.5 反压设计的分水岭题）
3. 小文件、热点、倾斜、重跑四张单，哪张在你家周报里长期缺席？（6.7 手册对号）
4. 仓内/湖侧分工线画过没有？没画则 6.8 的「重聚合放仓、重清洗放湖」默认失效 ⚠️。

**一句话收束** ⚠️：转换引擎会换代、运行时会更迭，唯有
「契约在目录、债务在小文件、复算在分区边界」三句话像物理定律一样稳定——
本章全部旋钮都是围绕这三句的减震器 ⚠️（重构句）。

## 核心概念速览（中英对照）

| 中文 | 英文 | 一句话 |
| --- | --- | --- |
| 动态帧 | DynamicFrame | 带自解释与容错语义的记录集 |
| 映射/裁决 | applyMapping / ResolveChoice | Glue 两板斧：改名变形、拆歧义列 |
| DPU | Data Processing Unit | Glue 算力计量元 |
| 中介层 | Silver Layer | 清洗去重后的可信原料 |
| 金层 | Gold Layer | 面向消费域的成品 |
| 增量合并 | Upsert / Merge | 按业务键覆写的新旧裁决 |
| 数据倾斜 | Skew | 热点键打断并行假设 |
| 小文件问题 | Small File Problem | 高提交率的物理债 |
| 重放幂等 | Replay Idempotency | 失败重试不改结果的能力 |
| 运行时选择 | Runtime Selection | 契约不变、引擎换刀 |

## 最新演进与工业实践

2022→2026（✅ URL 200；⚠️ 转述）：

- **Glue 的「平台化」**：数据目录血缘、worksflows、以及新版作业作者体验持续向
  「一站式 ETL 平台」收敛（✅ `glue/latest/dg/what-is-glue.html` 现行页体系）；但 dbt/
  SQL-first 阵营把 gold 层逻辑搬出 Glue 脚本——**Glue 退守「连接器+搬运工」** ⚠️，
  盘上对位 [../Analytics_Engineering_with_SQL_and_dbt/00-总览与阅读地图.md](../Analytics_Engineering_with_SQL_and_dbt/00-总览与阅读地图.md)（✅ ls 在盘）。
- **S3 Tables 吃掉 compaction 运维** ✅（03/05 章已述）：6.7 手册第一条从「你的日程」变成
  「产品的默认值」⚠️。
- **EMR 的 Serverless 化分支** ⚠️：预算式 Spark 作业（免集群）与托管 Flink（11 章）
  共同压缩「长驻 EMR 集群」的适用面。
- **工业实践**：转换逻辑的版本化（git+CI 跑 dry-run 于采样数据）已是准入门槛；
  「脚本在控制台里裸奔」的 Glue jobs 在审计中按事故隐患计 ⚠️ 通识——重构章虽无法引用
  原书章序，但此纪律与本册「契约在目录」的 6.1 结论互锁。
