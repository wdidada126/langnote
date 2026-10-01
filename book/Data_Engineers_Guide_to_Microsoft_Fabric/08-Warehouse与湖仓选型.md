# 08 Warehouse 与湖仓选型 — The Data Engineer's Guide to Microsoft Fabric（⚠️ 主题重构章）

> ⚠️ 主题重构章（00 §5 口径）。对位书名中"分析与工程共用数据服务面"选型。机制 ✅ 转述
> fundamentals/decision-guide-lakehouse-warehouse（当日 200）；🔧 两组（E3 复用 + E7 新登）。
> 数仓方法论回链 Building_the_Data_Warehouse；波内 #146（多云数仓）只登记不链。

## 8.1 Fabric Warehouse 的物种：T-SQL 全功能仓跑在湖上

✅ 转述 `https://learn.microsoft.com/en-us/fabric/fundamentals/decision-guide-lakehouse-warehouse`：
Warehouse 提供**企业级 T-SQL 写路径 + 列存**，数据以开放格式驻留 OneLake——与 `03` 章
Lakehouse 的关系是"同一湖、两种服务面"：仓给分析师/ETL 工具熟悉的 SQL 方言与 ACID 写事务，
湖给 Spark 全表达力。给工程师的三档对象速记 ⚠️：

| 需求 | 对象 | 章内锚点 |
|---|---|---|
| SQL 重度、BI 服务、聚合层 | Warehouse | 本章 |
| Spark/多语言/流 | Lakehouse | 03/04 |
| 事务库只读副本 | Mirrored DB / SQL 端点 | 06 / 3.1 |

## 8.2 官方决策指南的重构（✅ 页 → ⚠️ 工程师口味）

当日 200 的决策指南按"谁写、谁读、什么工具"分岔；本册浓缩成四问（⚠️ 重构）：

1. **写方是谁？** 只有管道/笔记本 → 湖；SSIS/SQL Agent/dbt-sql 类 T-SQL 生态 → 仓。
2. **读方是谁？** 交互 BI/即席 SQL → 仓（直连体验 ⚠️）；ML/特征 → 湖（Spark 直读 ✅）。
3. **数据在哪落地？** 两者都落 OneLake（✅ 同湖是平台前提，不是选型变量）。
4. **成本怎么记？** 同一容量池不同 item 类型费率——数字回当日页（1.4 纪律 ✅ 页族在架）。

⚠️ 本书立场推定：湖仓**不是**二选一的宗教题，而是"同一份 Delta 的两种服务承诺"——与盘上
[../Practical_Lakehouse_Architecture/02-传统架构与现代数据平台.md](../Practical_Lakehouse_Architecture/02-传统架构与现代数据平台.md)
的通论同构，本册给厂商栈具象 ✅。

## 8.3 🔧 实验 E7：行存扫 vs 列存扫的形态差（非 Fabric 行为）

本机 SQLite 3.45.3 vs DuckDB 1.5.5（脚本 `exp.py`，2026-10-02 实测；结果集互验 count=32991 一致）：

```text
[E7] SQLite row-store aggregate-scan on 100k rows: 15.82 ms (count=32991);
     DuckDB columnar join+filter: 3.27 ms (count=32991 sum=2474274085.5) -- speedup x4.8
```

- 同一业务问题（事实×维表过滤聚合），列存+向量化引擎快 x4.8——**形态红利在 OLAP 谓词+投影窄表
  时兑现**；两引擎结果集一致是等价性证据 🔧。
- 映射到 Fabric：Warehouse 与湖 SQL 端点皆列存家族（⚠️），行存事务引擎不在分析面选型空间——
  所以"要不要仓"实际是 **T-SQL 生态位** 问题而非"要不要列存"问题（⚠️ 重构论点）。
- 类比缺口：本机 x4.8 不外推；分布键/索引策略/分区设计等真实仓工程全在本类比之外 ⚠️。

## 8.4 湖仓间的数据流动：抄表 vs 直连

✅ 域内页名实抓 + ⚠️ 转述的三条通道（数据工程师的路由决策）：

- **CTAS/CVS 抄表**：湖表→仓表物化复制（一致性快照语义，代价=双份存储+管道延迟）。
- **仓→湖回写**（`shortcuts to lakehouse` 类能力 ⚠️ 见 02 章谱系）：让仓的治理副本以 Delta 驻湖，
  湖侧消费者不再等待。
- **直连语义层**：BI 侧 Direct Lake 直读湖表——**不选仓的理由清单在增长** ⚠️（对位 #221 册
  [../Fundamentals_of_Microsoft_Fabric/08-语义模型DirectLake与Copilot.md](../Fundamentals_of_Microsoft_Fabric/08-语义模型DirectLake与Copilot.md)，
  本册不越界展开 BI 面）。

⚠️ 选型口诀：写路径决定对象（湖 or 仓），读路径尽量直连；只有当"复制的代价 < 服务的代价"才抄表。

## 8.5 数仓方法论的接缝：维度建模在 Fabric 的落点

回链系列祖谱（已验名实链）：
[../Building_the_Data_Warehouse/00-总览与阅读地图.md](../Building_the_Data_Warehouse/00-总览与阅读地图.md)
——Bill Inmon 的 CIF 把"仓=整合数据"定义为架构而非产品；Fabric 里"整合层"可由 Warehouse 表
或银/金层湖表承担，**方法论不因 SaaS 而豁免**：总线矩阵、一致性维度、缓慢变化维（SCD2 的
MERGE 实现见 `03` 章装载菜单与
[../Delta_Lake_Definitive_Guide/10-设计模式-CDC与SCD.md](../Delta_Lake_Definitive_Guide/10-设计模式-CDC与SCD.md)）。
Ralph Kimball 线在盘上的工具箱中译对照（盘上单文件册，实名已验）：
[../数据仓库工具箱.md](../数据仓库工具箱.md)、[../数据仓库工具箱3.md](../数据仓库工具箱3.md)。
波内对位登记（不链）：#146 多云数仓架构册——"Fabric 仓 vs 多云仓"选型树归它，本章只给租户内视角 ⚠️。

## 8.6 性能与成本的工程师常识（不抄死数字）

⚠️ 重构清单（机制有据：✅ 决策指南与 02 章 #221 同款纪律）：

1. 仓的统计信息/索引心智近似 SQL Server 家族（盘上谱系：
   [../Pro_SQL_Server_Internals/00-总览与阅读地图.md](../Pro_SQL_Server_Internals/00-总览与阅读地图.md)
   可深挖内核 ⚠️ 是否同源属推定，不当事实用）。
2. 与湖共池：大 ETL 抢同一容量 CU → 时段隔离/作业优先级是工程师自保手段（04 章池并发语义延伸 ⚠️）。
3. 分区/聚簇类物理设计两对象皆有对应物，参数一律当日页（🔧E3 的碎片账同样适用于仓表 ⚠️）。

## 8.7 🔧 补充账：E3 复用（维护经济性同构，非 Fabric 行为）

`03` 章 🔧E3（10 碎片→单文件：扫描 2.16→1.21 ms、整理费 47.44 ms、行数一致 True）在本章的复用点：
**湖仓两侧的"小文件税"同形**——选型题不豁免运维题（⚠️）。

## 8.8 与盘上诸书的联系

- 平台地图位姊妹章：[../Fundamentals_of_Microsoft_Fabric/05-Warehouse数仓引擎与选型.md](../Fundamentals_of_Microsoft_Fabric/05-Warehouse数仓引擎与选型.md)。
- 云仓三巨头对照（同岗位不同栈）：[../Snowflake_The_Definitive_Guide/00-总览与阅读地图.md](../Snowflake_The_Definitive_Guide/00-总览与阅读地图.md)、
  [../Amazon_Redshift_TDG/00-总览与阅读地图.md](../Amazon_Redshift_TDG/00-总览与阅读地图.md)、
  [../BigQuery_for_Data_Warehousing/00-总览与阅读地图.md](../BigQuery_for_Data_Warehousing/00-总览与阅读地图.md)；
  调优方法论迁移：[../Tuning_the_Snowflake_Data_Cloud/00-总览与阅读地图.md](../Tuning_the_Snowflake_Data_Cloud/00-总览与阅读地图.md)。
- 数据建模模式库：[../Data_Model_Patterns/00-总览与阅读地图.md](../Data_Model_Patterns/00-总览与阅读地图.md)、
  桥接实体化：[../Data_Vault_2_0/06-高级建模PIT与Bridge.md](../Data_Vault_2_0/06-高级建模PIT与Bridge.md)（盘上实名已验）。
- 波内登记：#219 Synapse 食谱（专用 SQL 池配方与本章选型题同源异构）、#146（波9 多云册，只登记）。

## 核心概念速览（中英对照）

- **同湖两面** — One Lake, Two Surfaces：湖与仓是同一 Delta 存储的两种服务承诺 ⚠️✅。
- **T-SQL 生态位** — T-SQL Niche：选仓的真实理由=写方/工具生态，不是"列存专属" ⚠️。
- **四问选型** — Four-Question Guide：写方/读方/落地/成本（8.2，重构自官方指南 ✅）。
- **抄表** — Materialize-to-Warehouse：一致性快照 vs 双份存储+延迟 ⚠️✅。
- **直连优先** — Direct-First：读路径尽量免复制；复制的代价<服务的代价才抄 ⚠️。
- **形态红利** — Columnar Bonus：窄投影+谓词场景兑现（🔧E7 x4.8，不外推）。
- **整合层** — Conformed Integration Layer：CIF 思想落 Fabric=银/金层或仓表，方法免疫 SaaS 化 ⚠️。
- **池共抢** — Shared Capacity Contention：ETL 与交互负载同池互噬，时段/优先级自保 ⚠️。
- **小文件税** — Fragmentation Tax（复用 E3）：选型不豁免运维 🔧✅。
- **保真副本** — Residency：仓/湖/镜像三对象同驻 OneLake，治理面因此统一（10 章回收）✅⚠️。

## 最新演进与工业实践

2024→2026（URL 均 2026-10-02 实测 200；⚠️ 转述）：

- **决策指南成体系化文档件**：`fundamentals/decision-guide-lakehouse-warehouse` 与
  `decision-guide-data-store`、`decision-guide-pipeline-dataflow-spark` 构成官方"选型三书"（✅ 域内
  清单实抓）——平台方主动接管选型叙事，是"书厂商化"的信号 ⚠️；本册立场：读官方骨架、练本机
  类比（🔧E7/E3）、租户内定稿。
- **旧链化石**：`/fabric/data-warehouse/overview` 实测 404、`get-started/licensing-model-fabric`
  实测 404（00 §9 禁引清单）——域重组与许可页迁移，2024 出版时点引文需全部重验。
- **工业实践画像** ⚠️（通识）：湖仓并存的成熟租户普遍收敛为"仓=面向业务 SQL 的发布层，
  湖=工程与 AI 的工作层"，与 8.2 四问一致；反例多为"为 BI 建了仓、工程链路仍在湖，两拨人
  对着同一指标吵架"——语义层治理问题，回链 #221 册 Direct Lake 章与其 08 章。
- **兄弟分工再登记**：#146（波9）多云视角的"云仓对位表"（含 Amazon_Redshift_TDG 在盘版本）
  是本章的扩展视角；波尾主代理总索引 Fabric 小节建议（00 §8）若采纳，本章即"厂商内选型"行锚。
