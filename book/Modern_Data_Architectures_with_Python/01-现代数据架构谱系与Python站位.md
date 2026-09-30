# 01 · 现代数据架构谱系与 Python 站位

> ⚠️ 主题重构章（原书目录取证不可得，见 [00-总览与阅读地图.md](00-总览与阅读地图.md) §2）。
> 本章为全书的概念基座：架构谱系是什么、Python 在每一层实际干了什么。
> 三态标注：✅ 实证｜⚠️ 转述/推定｜🔧 本机实测（见 00 §6 复现指引）。

## 1. 为什么"架构"成了数据工程的第一个词

数据技术故障里很大一块不是代码 bug，而是**架构错配**：用运维数据库的心智做分析负载，
或用批处理的心智做近实时需求。所谓"现代数据架构"（Modern Data Architecture），是把
2010s 以来陆续出现的形态——数据湖、云数仓、湖仓（Lakehouse）、网格（Mesh）、编织
（Fabric）、平台化（如 Microsoft Fabric 类 SaaS）——按**问题分工**摆成一张可讲解剖图。
本书（⚠️ 存在性存疑册，按名册主题「Python + 现代数据架构」重构）的独特价值在于：
它假设你不是平台售前，而是**要亲手用 Python 把这些层拼起来的人**。

- 谱系三巨头分工（本册 00 §4 有全表）：湖仓答"**存储与表语义**"（一份数据既供 BI 又供 ML）；
  网格答"**组织与所有权**"（数据产品、域自治、联邦治理）；编织答"**集成与自动化**"
  （主动元数据驱动的移动/变换/富化）。三者不互斥，工业界常叠放。
  对读：[../Data_Lakehouse_in_Action/00-总览与阅读地图.md](../Data_Lakehouse_in_Action/00-总览与阅读地图.md)、
  [../Data_Mesh/00-总览与阅读地图.md](../Data_Mesh/00-总览与阅读地图.md)、
  [../Principles_of_Data_Fabric/00-总览与阅读地图.md](../Principles_of_Data_Fabric/00-总览与阅读地图.md)。
- 平台流派把三件一体打包卖（Fabric/Snowflake+Dynamic Tables/Databricks+UC），
  代码流派用开源件拼装（DuckDB/dbt/Airflow/Iceberg）。本册站**代码流派**视角，
  每个架构词都翻译成"几行 Python + 几段 SQL 的哪个模式"。

## 2. 四代数仓形态速谱（谱系前史）

1. **第一代：关系数仓 + ETL**（Inmon/Kimball 时代）。星型模型、夜间批、ETL 工具
   （Informatica 系）。Python 尚不存在于此图。对读 repo：
   [../Building_the_Data_Warehouse/00-总览与阅读地图.md](../Building_the_Data_Warehouse/00-总览与阅读地图.md)（若盘上未建目则以此名指代规划位——写前已验：该目录 ✅ 存在）。
2. **第二代：大数据湖 + MapReduce**。Hadoop 把"schema-on-read"变成默认，成本降、
   治理差，湖变沼泽。
3. **第三代：云数仓 + ELT**。存储计算分离、按量计费，变换回到 SQL（dbt 兴起），
   摄取工具（Fivetran 系）吃掉 EL 半程。Redshift/BigQuery/Snowflake 三巨头谱见 repo
   波 4 各册（本册不重复；⚠️ 云仓不可本机实测，一律转述）。
4. **第四代（进行时）：湖仓一体 + 开放表格式 + 治理平面**。Iceberg/Delta/Hudi 给对象
   存储装上 ACID/快照/schema 演进；Mesh 给组织装上产品契约；Fabric 给元数据装上
   自动化。本册 07/08/09 章各对一层。

## 3. Lambda 与 Kappa：批流之争的两种宪法

- **Lambda**：批层（真相）+ 速度层（近似）+ 服务层（合并查询）。正确性靠批层重算兜底，
  代价是**同一逻辑写两遍**（批一份、流一份），两套代码漂移是经典事故源。
- **Kappa**：一切皆日志流，重放代替重算（Kafka + 流处理器）。把"批"降格为"流的特例"，
  逻辑只写一遍，代价是历史重放成本与状态管理复杂度（⚠️ 转述；本册无 Kafka 可测）。
- Python 站位：无论哪种宪法，**编排与胶水层**都是 Python 的（Airflow/Dagster/Prefect
  以 Python 定义 DAG；流处理侧 Faust/Bytstream 属小众 ⚠️）。工程上最常见的落点是
  "微批"：调度器按分钟级拉增量，用 02 章的水位线+MERGE 幂等摄取，语义上逼近流。
  与分布式系列的接口：流式原理归 `../../db/db.md` 论文线与 repo 流处理册（本目录
  不链空，故此处仅指路径不冒链未验文件）。

## 4. Python 在架构解剖图上的五块肌肉

| 架构层 | Python 的实际职务 | 本册章节 | 类比可测件 |
| --- | --- | --- | --- |
| 摄取/管道 | 连接器胶水、微批调度、幂等装载 | 02 | 🔧E1（DuckDB ATTACH sqlite + MERGE） |
| 变换建模 | pandas/DuckDB SQL 做仓内/湖内变换 | 02/07 | DuckDB 直查 pandas 帧 |
| 质量 | 规则即代码、断言即测试 | 04 | 🔧E2（SQL 规则引擎 vs CHECK） |
| 元数据/血缘 | 目录采集器、解析器抽线 | 05/06 | 🔧E3/E4（指纹漂移、sqlglot） |
| 治理落地 | 把政策写成可执行的闸门 | 09 | 三件拼装的最小闭环 |

注意**没有的一块**：Python 不是高吞吐流处理的主流引擎（那是 JVM/Rust 的腹地 ⚠️ 工程
共识）。承认这条边界，才谈得上"用对 Python"：它赢在**表达架构决策的成本**——
一个边表、一套规则 DSL、一个目录 schema，几百行就能落地并被团队演化。

## 5. "架构即数据"的反身性

现代架构的一个自反特征：架构组件本身（管道、规则、血缘）都要用**数据**来表达和存储。
- dbt 把变换建模成 manifest JSON（对读 [../Analytics_Engineering_with_SQL_and_dbt/00-总览与阅读地图.md](../Analytics_Engineering_with_SQL_and_dbt/00-总览与阅读地图.md)）；
- OpenLineage 把执行事件标准化成 JSON schema（✅ https://openlineage.io/ ）；
- 本册 🔧E3/E4 手工复现了这个思想：元数据目录与血缘边表就是两张普通 SQLite 表，
  递归 CTE 一查就是上游闭包——**治理平面的最小可行体不需要任何平台**。
这也是本册与治理线（[../Understanding_Data_Governance/00-总览与阅读地图.md](../Understanding_Data_Governance/00-总览与阅读地图.md)）
的接口：治理册讲"该有什么制度"，本册讲"制度落成的第一个代码原型长什么样"。

## 6. 反模式清单（本章小结）

1. **平台名词驱动选型**：先信 Mesh/Fabric 口号再找问题，多半买回一堆没人用的控制台。
2. **两遍逻辑无对账**：Lambda 双实现但没有任何一致性测试（04 章的质量规则本该同时挂批流两侧）。
3. **元数据靠人肉 wiki**：不与管道共执行、无指纹比对（🔧E3 演示了漂移检出的 20 行替代）。
4. **血缘只在 BI 截图里**：不存边表、不可查询（🔧E4 演示 SQL 解析→边表→递归追溯）。
5. **把 Python 用到它不擅长的位置**：超高吞吐流上硬用 Python（见 §4 边界）。

## 7. 自检问答（读毕应有答案）

1. 湖仓/网格/编织各自回答的问题是哪一句话？（存储与表语义 / 所有权与产品 / 集成与自动化）
2. Lambda 的第一事故源是什么，Kappa 用什么换掉它、又付出了什么？
   （双实现漂移；重放换重算，代价是状态与历史回放成本）
3. "架构即数据"在本册的三个落点？（dbt manifest、OpenLineage 事件、🔧E3/E4 目录与边表）
4. Python 在架构图上的五块肌肉与一块禁区？（02/04/05/06/09 对位；禁区=高吞吐流主体）
5. 为什么说"先能手撕，再谈平台"？（§3 差距表与 09 章采购判断力论）

## 核心概念速览（中英对照）

1. **现代数据架构** — Modern Data Architecture：湖仓+表格式+治理平面构成的当代平台骨架总称。
2. **湖仓** — Lakehouse：对象存储上以开放表格式提供 ACID/时间旅行的统一分析层。
3. **Schema-on-read** — 读时建模：湖的默认心智，写入不校验、读取才解释（沼泽之源）。
4. **Lambda 架构** — Lambda Architecture：批层+速度层+服务层三件套，以批重算保正确。
5. **Kappa 架构** — Kappa Architecture：一切皆日志流，重放即重算，逻辑单实现。
6. **微批** — Micro-batch：分钟级调度的增量摄取，工程上逼近流语义的常见折中。
7. **ELT** — Extract-Load-Transform：先装载后在引擎内变换，云数仓时代的主流方向。
8. **数据即产品** — Data as a Product：Mesh 的核心口号，域对外提供有契约的资产。
9. **主动元数据** — Active Metadata：驱动自动化（血缘/质量/编排）而非仅供浏览的元数据。
10. **架构即数据** — Architecture-as-data：管道/血缘/规则以普通表+可查询形式存储。
11. **编排器** — Orchestrator：以代码（常为 Python）定义 DAG 的调度层（Airflow/Dagster）。
12. **存储计算分离** — Disaggregated Storage/Compute：云数仓的经济学根基，按量伸缩的前提。
13. **联邦治理** — Federated Governance：政策集中定义、域内自主执行（09 章闸门化的对象）。

## 最新演进与工业实践

- **编排三件套现状（2024–2026）**：Airflow 3.x 重构 DAG 解析与 UI（⚠️ 转述，未逐条核实发布注）；
  Dagster/Prefect 以 Python 装饰器把"资产/任务"建模得更类型化（⚠️ 转述）。本册 🔧E1 的
  水位线+MERGE 与任一派都兼容：编排层只是把这些函数按 DAG 摆好。
- **DuckDB 成为"架构内的 Python 进程"**：1.0（2024-06）以来 sqlite 扩展、MERGE INTO、
  ATTACH 多库使其可客串管道枢纽与联邦枢纽；扩展与语法文档 ✅
  https://duckdb.org/docs/stable/extensions/overview 、✅ https://duckdb.org/docs/stable/sql/statements/merge_into.html ；
  发布线 ✅ https://github.com/duckdb/duckdb/releases （🔧E1/E5 即此路线的本机实证）。
- **湖仓收敛到 Iceberg 事实标准**：REST Catalog（apache/iceberg-architecture-rest）+ pyiceberg
  使 Python 首次成为一等公民客户端，✅ https://iceberg.apache.org/spec/ （2026-10-01 curl 200）。
  Delta/Hudi 活跃但新投资明显向 Iceberg 聚拢（⚠️ 转述自社区共识，无硬统计可引）。
- **Fabric 平台化对冲**：Microsoft Fabric 把 OneLake/元数据/治理打包成租户级 SaaS，
  对读 [../Fundamentals_of_Microsoft_Fabric/00-总览与阅读地图.md](../Fundamentals_of_Microsoft_Fabric/00-总览与阅读地图.md)；
  开源代码流派与本册立场一致：**先能手撕，再谈平台**。
- **工业界对"谱系叠放"的实际处置**：多数公司 2024–2026 的落地形态=湖仓(存储)+
  网格(组织,常常只取其所有权语义)+平台 SaaS(部分组件)，Fabric 作为方法论较少独立存在
  （⚠️ 转述；本册拒绝引用任何无法核实的调研百分比）。
