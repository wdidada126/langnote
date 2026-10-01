# 03 Oracle 数据仓库导论 — Introduction to Oracle Data Warehousing（原书第 3 章，pp.53–74）

> 章题/页区间/小节题名 ✅ 出版社目录扫描件（Contents x）。本章是 Part I 的收束章：把「BI 版图」落到
> 「Oracle Database 作为仓库平台」的事实清单，并给出**自研 vs 打包**的路线裁决。Oracle 侧机制为
> ⚠️ 文档转述（现行 19c/23ai 口径 + 10g 历史口径分别标注），本机不可实测。

## 3.1 Oracle 数据仓库基础（p.54）

- ⚠️ 转述（现行文档口径，✅ https://docs.oracle.com/en/database/oracle/oracle-database/19/dwhsg/index.html ）：
  19c 仓库指南第 1 章把仓库定义为「面向主题、集成、非易失、时变」的分析型数据集合，并给出三种
  架构形态：基本型 / 带暂存区（staging）型 / 暂存区 + 数据集市型 ⚠️。这三形态正是本章 3.2/3.3 的骨架。
- OLTP 与仓库的分裂（⚠️ 指南 1.2 主题）：负载谱系不同 ⇒ 模式设计、索引策略、并发与装载窗口全部不同；
  本书在 2007 年就把这一点写成「同一 DBA 团队要同时会两套算术」。
- ⚠️ 编者归纳：本章不教建模（那是 ch.5），它教的是**平台事实**：Oracle 提供哪些仓库原语
  （分区、物化视图、并行、位图索引、直接路径装载、OLAP 分析视图），以及它们各自的授权归属
  （分区/OLAP/压缩属选件 ⚠️，与 ch.4 的成本小节、ch.8 的管理选项小节呼应）。

## 3.2 Oracle 数据库分析与模式考量（p.55）

目录把本节放在「基础」之下作为最大块（✅ p.55–63，跨 9 页），⚠️ 按现行指南主题可归纳为五条清单：

1. **模式与属主**：仓库对象的属主规划、暂存 Schema 与分析 Schema 分离（对应指南 1.4.2/1.4.3 架构）；
2. **表与约束**：信任声明语义下的 RELY 约束、NOVALIDATE 组合，让优化器信任约束而不付校验代价 ⚠️
   （指南 4.2.2.3 主题）；
3. **索引策略**：位图索引与位图连接索引承担低基数列，B 树留给高基数（指南 4.1 主题；机理纵深见
   [../Cost_Based_Oracle_Fundamentals/08-位图索引.md](../Cost_Based_Oracle_Fundamentals/08-位图索引.md)）；
4. **分区与物化视图**：分区首先是**管理工具**（装载窗口/备份粒度），性能收益是第二性的 ⚠️
   （指南 3.2.1.2、5–8 章主题，本册 07/09 展开）；
5. **统计信息与查询变换**：仓库的谓词组合复杂，统计与直方图决定星型转换是否发生 ⚠️
   （CBOF [07-直方图](../Cost_Based_Oracle_Fundamentals/07-直方图.md)、[09-查询变换](../Cost_Based_Oracle_Fundamentals/09-查询变换.md)）。

- 🔧 概念类比（**非 Oracle 行为**）：DuckDB 里 5M 行事实表 + 3 张维表的星型查询（日期区间 + 品类 +
  渠道三谓词）实测 **13.3ms**，同表全扫 3.1ms ⇒ join 与谓词选择才是成本主体；改打「月×品类」预聚合表
  （6000 行）后查询 **1.27ms**（≈10× 快，建表 66ms）。这就是 3.2 第 3/4 条的算术直觉来源（00 §9 E1/E1b/c）。

## 3.3 管理基于 Oracle 的数据仓库（p.64）

- ⚠️ 转述：本节（✅ p.64–69）落在日常管理面：装载窗口、统计信息维护、物化视图刷新调度、
  备份与恢复粒度、容量增长跟踪。这些主题在 ch.8（Grid Control）与 ch.9（调优）被正式展开，
  本章只做清单式预告。
- ⚠️ 编者归纳：本章把「管理」放在「选型」之前是有意的——**先确认运维能承接，再决定架构复杂度**；
  这与 ch.10 的「人员配置与风险」形成同一价值观。

## 3.4 从哪里开始（p.70）：三条路线

目录给出三条起点（✅）：**Oracle/PeopleSoft EPM**（p.71）、**Oracle/Siebel Business Analytics
Applications**（p.73）、**Choosing Completely Custom**（p.74）。

| 路线（✅） | 页 | 适用判断（⚠️ 编者归纳） | 代价 |
| --- | --- | --- | --- |
| PeopleSoft EPM | 71 | 财务/人力/项目管理口径为主，源系统即 PeopleSoft 家族 | 语义受产品预置约束 ⚠️ |
| Siebel Business Analytics Applications | 73 | CRM/销售分析口径，源为 Siebel | 行业包版本耦合 ⚠️ |
| Completely Custom | 74 | 跨源、跨主题、需自有竞争口径 | 全栈自担：ETL/元数据/工具/运维（Part II 全部内容） |

- ⚠️ 转述：这条决策线的判据在书中被表述为「业务口径是否已被打包应用覆盖」——若覆盖，买；
  若不覆盖或需自有语义，自建，并进入 Part II 的工程清单。
- 与 ch.1 的呼应：2.5 的「够不够」裁决在这里第二次出现，说明本书的方法论是**两级裁决**
  （应用内 BI 够不够 → 打包分析应用够不够 → 才谈自建）。

## 3.5 与 repo 其他书的联系

- 导游册对位：[../Oracle_Essentials_5e/07-数据仓库基础与体系结构.md](../Oracle_Essentials_5e/07-数据仓库基础与体系结构.md)
  （⚠️ 重构章，同为「平台事实清单」视角）、[../Oracle_Essentials_5e/08-仓库实施分区物化视图与装载.md](../Oracle_Essentials_5e/08-仓库实施分区物化视图与装载.md)。
- 成本模型纵深：[../Cost_Based_Oracle_Fundamentals/00-总览与阅读地图.md](../Cost_Based_Oracle_Fundamentals/00-总览与阅读地图.md)
  （Lewis，本册 3.2 第 5 条的机理解释全在那边）。
- 方法论：[../Building_the_Data_Warehouse/02-数据仓库环境.md](../Building_the_Data_Warehouse/02-数据仓库环境.md)、
  [../数据仓库工具箱.md](../数据仓库工具箱.md)、[../Physical_Database_Design/12-数据仓库OLAP与反范式化.md](../Physical_Database_Design/12-数据仓库OLAP与反范式化.md)。
- 云仓对照（同题不同答案）：[../Tuning_the_Snowflake_Data_Cloud/04-微分区.md](../Tuning_the_Snowflake_Data_Cloud/04-微分区.md)
  （托管平台把 3.2 的清单变成默认行为）、[../Amazon_Redshift_TDG/00-总览与阅读地图.md](../Amazon_Redshift_TDG/00-总览与阅读地图.md)。
- 波内兄弟 #142/#143/#145/#168：只登记不链（[00 §8](00-总览与阅读地图.md)）。

- 波内互证：#204（同题 Oracle BI 食谱，Heaton，Packt 2012）与本册的三叉辨析见
  [00 §5](00-总览与阅读地图.md)；本册 05/07 承接本章清单的展开面。

## 3.6 编者注记：把平台清单变成检查表

- ⚠️ 编者归纳（方法性收束）：3.2 的五条平台事实可直接改写成仓库立项/巡检检查表，
  每条给「问什么 / 失败信号」两列：
  1. **属主与 Schema 分离**——问「暂存层与分析层各是谁的表」；失败信号=报表直打业务源表；
  2. **约束策略**——问「RELY/NOVALIDATE 用了没有」；失败信号=装载窗口里含全表校验；
  3. **索引策略**——问「低基数列上是位图还是 B 树」；🔧 E7（77.3→85.9ms）即失败信号的可复现演示；
  4. **分区与物化视图**——问「分区键是管理粒度还是性能噱头」；失败信号=从不做交换装载、
     从不按分区刷新汇总；
  5. **统计与查询变换**——问「装载后统计作业的时点」；失败信号=星型转换不发生时无人能解释。
- 用法 ⚠️ 编者归纳：季度 DBA 例会上过一遍，把「平台事实」维持成「平台现状」；
  本章作为导论章的交付物，就是这张表加上 3.4 的两级裁决。

## 核心概念速览（中英对照）

- **仓库四特征** — Subject-Oriented / Integrated / Non-Volatile / Time-Variant：19c 指南沿用的经典定义 ⚠️（✅ dwhsg）。
- **暂存区** — Staging Area：装载前的落地与清洗区，架构形态二的标志（✅ 指南 1.4.2 主题）。
- **RELY 约束** — RELY Constraint：向优化器声明可信但不强制校验的约束，仓库专用手法 ⚠️。
- **NOVALIDATE** — 不校验装载：加约束不回头校验历史数据，缩短装载窗口 ⚠️。
- **位图/位图连接索引** — Bitmap / Bitmap Join Index：低基数列与星型查询的索引答案 ⚠️（🔧 E7 反例）。
- **分区即管理工具** — Partitioning for Manageability：先谈窗口与备份粒度，再谈裁剪收益 ⚠️。
- **选件授权** — Option Licensing：分区/OLAP/压缩等属额外选件，选型即预算（与 ch.4/ch.8 呼应）⚠️。
- **PeopleSoft EPM 路线** — 打包绩效与财务分析起点（✅ p.71）。
- **Siebel BA 路线** — 打包客户分析起点（✅ p.73）。
- **完全自研路线** — Completely Custom：跨源跨主题时的默认选择，代价是全栈自担（✅ p.74）。
- **两级裁决** — Two-Stage Sufficiency Check：应用内 BI → 打包应用 → 自建（本书方法论骨架）⚠️ 编者归纳。

## 最新演进与工业实践

2007 → 2026 对位（⚠️ 转述 + ✅ URL）：

- **仓库原语的默认化**：19c/23ai 指南把星型转换、物化视图查询重写、PCT 刷新、近似查询处理
  （Approximate Query Processing / Approximate Top-N）、In-Memory 表达式列为标准武器 ⚠️
  （✅ https://docs.oracle.com/en/database/oracle/oracle-database/19/dwhsg/index.html 、
  https://docs.oracle.com/en/database/oracle/oracle-database/19/inmem/ ）；2007 需要 DBA 手工装配的东西，
  今天多数有开关或自动（自动 DOP、自动索引仅云版 ⚠️）。
- **Autonomous Data Warehouse → ATP/ADB-S**：本章「平台事实清单」的当代版本是自治库：自动内存/索引/
  并行与弹性伸缩（✅ https://docs.oracle.com/en/cloud/paas/autonomous-database/ 、
  https://docs.oracle.com/en/cloud/paas/autonomous-database/serverless/adbsb/ ）⚠️。
- **打包分析应用的替代**：PeopleSoft EPM / Siebel BA Applications 的后继是 **Oracle Fusion Cloud 内建分析 +
  FAW 行业数据应用**（✅ https://www.oracle.com/analytics/ ）⚠️；「买 vs 自建」两级裁决仍然成立，
  只是「买」的一侧从安装包变成了云订阅。
- **湖仓第三选项**：2026 的路线表里多了「开放表格式 + 多引擎」这一列（Iceberg/Delta + Spark/Trino），
  与本章 3.4 三路线并列 ⚠️ 编者归纳，对照
  [../Data_Lakehouse_in_Action/00-总览与阅读地图.md](../Data_Lakehouse_in_Action/00-总览与阅读地图.md)、
  [../Architecting_an_Apache_Iceberg_Lakehouse/00-总览与阅读地图.md](../Architecting_an_Apache_Iceberg_Lakehouse/00-总览与阅读地图.md)。
- **工业实践** ⚠️ 评价性转述：Oracle 仓库栈在 2026 的典型形态是「ADB-S 承载核心集市 + OCI Data Integration
  做管道 + OAC 做前端 + 湖仓承载非结构化/ML」，与本章「先平台后建模」的顺序一致。
- **本机教学** 🔧：E1/E1b（13.3ms → 1.27ms）演示「预聚合 = 一个数量级」，是讲 3.2 索引/物化视图动机的
  最低成本实验；DuckDB 无位图索引、无查询重写，**非 Oracle 行为**。
