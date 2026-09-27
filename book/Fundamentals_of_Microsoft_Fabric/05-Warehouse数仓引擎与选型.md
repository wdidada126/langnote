# 05 · Warehouse：数仓引擎与湖仓选型（⚠️ 推定章：原书 TOC 未实抓，主题重构见 [00-总览与阅读地图.md](00-总览与阅读地图.md) 第二节）

Fabric Data Warehouse = 容量内托管的 T-SQL 云数仓 item
（✅ https://learn.microsoft.com/en-us/fabric/data-warehouse/data-warehousing ，访问 2026-09-27）。
本章两条线：**引擎侧它是什么** ＋ **选型侧它何时该赢过 Lakehouse**（后者有官方决策专页可锚，罕见地不用 ⚠️ 猜）。

## 5.1 引擎画像：完整 T-SQL 事务引擎 + 列存

可锚要点（✅ 同页与域内子页 hrefs 实抓，访问 2026-09-27；⚠️ 细节深度转述）：

- 完整 DDL/DML 事务语义；聚集列存索引为默认物理形态；
- 存储过程、时间增量表（变更审计）等企业件在文档域内有条目（⚠️ 逐项能力以当日页为准）；
- 域内直挂 `guidelines-warehouse-performance`、`migration-assistant`、
  `migration-synapse-dedicated-sql-pool-warehouse` 等页——产品意图明确：**承接 Synapse 专用 SQL 池存量**。

## 5.2 与湖仓的"同底座不同引擎"关系

关键辨析（✅ 双页互证，2026-09-27）：
Warehouse 的表也**落进 OneLake 的 Delta Parquet**
（https://learn.microsoft.com/en-us/fabric/onelake/sql-analytics-endpoint-onelake-security 讨论两侧安全面）。
即：同一文件格式层上——

- Warehouse 提供"原生 T-SQL 写 + 索引优化"；
- Lakehouse SQL 端点提供"Spark 写 + T-SQL 读"。

**选型问题从"存哪"变成"谁是写入方主责"**——这是副标题级别的设计决策，官方为此给专页（5.3）。

## 5.3 官方决策指南要点转述

✅ https://learn.microsoft.com/en-us/fabric/fundamentals/decision-guide-lakehouse-warehouse （访问 2026-09-27，专页存在）。
⚠️ 转述其决策轴（口径以当日页为准）：

1. 团队技能：Spark/Python 重 → 湖；T-SQL/DBA 重 → 仓；
2. 事务强度：高频 MERGE/行级更新 → 仓；
3. 负载形态：半结构化与 ML 特征工程 → 湖；高并发报表混合读 → 两侧皆可（Direct Lake 拉平差距，08 章）；
4. 细粒度安全（行级安全/动态掩码类策略）→ 优先仓（⚠️ 两侧能力对照页未逐一实抓，登记缺口）。

## 5.4 🔧 EXP-4：行存导入 vs 列存直查的代价量纲（本机类比，非 Fabric 行为）

SQLite 3.45.3（行存代表）vs DuckDB 1.5.5（列存代表），1,000,000 行，2026-09-27：

- SQLite 逐行灌入：**5,331.7 ms**，落盘 **39.44 MB**；
  同数据 Parquet 仅 8.18 MB——列存+编码压缩约 **4.8 倍**；
- 全表聚合 count+avg：SQLite **138.3 ms** vs DuckDB **2.59 ms**（**≈53 倍**，结果同为 avg 714.21）。

读数：**导入型仓库把扫描成本付在每次查询，列存把这笔钱换成一次性编码成本**。
Fabric Warehouse 的列存索引属后一阵营，但其在容量 CU 上的真实并发/隔离数字 ⚠️ 不可本机等价。
方法与版本：exp.py，声明"非 Fabric 行为"。

## 5.5 与云仓三巨头的对位（盘上已验收册三角）

| 维度 | Fabric Warehouse | 参照册（✅ 盘上在册） |
|---|---|---|
| 扩缩计费 | 共享容量 CU（01 章） | [../Advanced_Snowflake/00-总览与阅读地图.md](../Advanced_Snowflake/00-总览与阅读地图.md)、[../Snowflake_The_Definitive_Guide/00-总览与阅读地图.md](../Snowflake_The_Definitive_Guide/00-总览与阅读地图.md) |
| 方言 | T-SQL 全家 | [../Google_BigQuery_TDG/00-总览与阅读地图.md](../Google_BigQuery_TDG/00-总览与阅读地图.md)、[../Amazon_Redshift_TDG/00-总览与阅读地图.md](../Amazon_Redshift_TDG/00-总览与阅读地图.md) |
| 存算分离程度 | 湖化存储（Delta 露出） | 三家存储更封闭（⚠️ 归一化为本目录观点） |
| 方法论祖谱 | Inmon/Kimball 落地新载体 | [../Building_the_Data_Warehouse/00-总览与阅读地图.md](../Building_the_Data_Warehouse/00-总览与阅读地图.md)、其 [11-关系模型与多维模型.md](../Building_the_Data_Warehouse/11-关系模型与多维模型.md) |

## 5.6 迁移面：Synapse 专用池与 SQL DB 的"接盘"路径

✅ 枢纽页 hrefs 含 `migration-synapse-dedicated-sql-pool-methods`、`migration-assistant`、`create-warehouse`（访问 2026-09-27）。
⚠️ 转述产品信号：微软明示 Synapse 专用 SQL 池向 Fabric Warehouse 收敛的迁移工具链。
DBA 读者的 T-SQL 纵深在盘上属单文件/资料层（如 book 根 `55349_TSQLFundamentals2012.zip`，⚠️ 非笔记册不作内容主张），
正式书目谱系见 [../数据库系列·总索引.md](../数据库系列·总索引.md)。

## 5.7 仓的"三张性能牌"（评审话术，⚠️ 转述+🔧 类比）

1. **列存索引**：扫描型聚合的根优化（🔧 EXP-4 的 53 倍即此方向的单机影子）；
2. **统计信息与计划**：T-SQL 引擎传统艺能，迁移 Synapse 资产时重点回归测试对象（⚠️）；
3. **分布/并发**：在 Fabric 里被"容量 CU + 工作负载引擎调度"抽象接管，用户不再管分布键——
   与 Redshift DISTKEY/SORTKEY 显式时代告别（对照 [../Amazon_Redshift_TDG/00-总览与阅读地图.md](../Amazon_Redshift_TDG/00-总览与阅读地图.md)）。

## 5.8 本章收口：选型题的"三句话判据"

1. 写入方是工程师+ML 管道 → Lakehouse；写入方是 DBA+应用事务 → Warehouse；
2. 高并发小查询+细粒度安全 → Warehouse；
3. 拿不准 → 先湖后仓用端点/Shortcut 补读，**别让存储格式替团队技能做决定**（⚠️ 教学判据，非原书/官方原文）。

## 5.9 湖 vs 仓 一张对照表收束（评审打印件，⚠️ 综合前文）

| 维度 | Lakehouse | Warehouse | 出处 |
|---|---|---|---|
| 写方主责 | Spark/管道工程师 | DBA/T-SQL 团队 | 5.3 |
| 事务高频 MERGE | 勉强 | 原生强项 | 5.3 |
| 文件可读性（退出成本） | Delta 露出，外部引擎可直读 | 亦落 Delta 但工具链以仓为先 | 5.2/4.1 |
| 细粒度安全（RLS/DDM 类） | 端点面受限（⚠️ 以当日页为准） | 主场 | 5.3 |
| ML 特征/半结构 | 主场 | 配角 | 5.3 |
| 小文件敏感度 | 高（🔧 EXP-2） | 低（引擎内整理） | 4.3/5.4 |
| 高并发点查+聚合混合 | 端点可用 | 列存主场（🔧 EXP-4 方向） | 5.4/5.7 |
| Direct Lake 消费 | ✅ 一等 | ✅ 一等 | 8.2 |

判据总结：前两列"是/否"多数情况下已替你做决定；剩下 20% 的争议案例，
用 5.8 第 3 句——**让写入方技能定引擎，别让存储格式绑架组织**。

## 核心概念速览（中英对照）

- **Fabric 数据仓库** — Fabric Data Warehouse：容量内托管 T-SQL 数仓 item。
- **聚集列存索引** — Clustered columnstore index：仓表默认物理形态，扫描型负载之根。
- **决策指南** — Decision guide (lakehouse vs warehouse)：官方两形态选型专页 ✅。
- **写入主责** — Write-side ownership：本目录判据：按主写入方选引擎。
- **端点对照** — SQL analytics endpoint vs warehouse：湖读脸 vs 仓原生脸。
- **迁移助手** — Migration assistant：Synapse/SQL DB 资产转入仓的工具面（✅ 页在链）。
- **时间增量表** — Temporal tables：行级变更审计的 T-SQL 机制（⚠️ 转述存在性）。
- **存算湖化** — Lake-backed storage：仓表亦以 Delta 落 OneLake 的架构事实。
- **共享容量** — Shared capacity：仓与全家桶同池 CU 计费的约束源。
- **细粒度安全** — Fine-grained security（RLS/DDM）：仓侧权限策略卖点之一（⚠️）。
- **性能指南** — Warehouse performance guidelines：域内专页存在（✅ hrefs 实抓，2026-09-27）。

## 最新演进与工业实践

- **OneWarehouse 方向**（⚠️ 转述 2024–2025 大会叙事）：微软曾宣示"湖仓一体到单一仓库"融合路线；
  2026-09-27 核查 `data-warehouse/one-warehouse`、`/fabric/one-warehouse/overview` 两候选路径均 **404**——
  **功能叙事与文档落地不同步，禁引旧名直链**，以 data-warehousing 枢纽页为准（00 第七节清单在案）。
- **仓的 AI 面**：Copilot 系能力散见发布节奏（⚠️ 未锚定仓专属子页；唯一可 ✅ 的引用面是
  https://learn.microsoft.com/en-us/fabric/fundamentals/copilot-fabric-overview ，访问 2026-09-27，08 章展开）。
- **容量演进**：F SKU 谱系、暂停/恢复与细粒度配额（✅ buy-capacity/scale-capacity，2026-09-27）；
  与 Snowflake 自动挂起语义的差距在收窄（⚠️ 对比判断，非可锚事实）。
- **工业实践**：Synapse 存量向 Fabric 迁移是微软渠道主推剧本（✅ 三条 migration 页即产品意图证据）；
  数仓方法论层需求依然刚硬——[../Building_the_Data_Warehouse/12-高级话题与企业信息工厂.md](../Building_the_Data_Warehouse/12-高级话题与企业信息工厂.md) 的 EIF 批判视角适合作"全家桶热情"的解药。
- 🔧 类比边界再声明：5.4 的 53 倍是**单机无并发**数字；云仓价值在并发隔离与弹性，本机不可模拟——该结论 ⚠️ 转述自各家文档口径。
