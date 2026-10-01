# 09 Synapse Link — Synapse Link（原书第 9 章，pp.201–223）

> 章题与页区间 ✅ Crossref 存款记录实抓（DOI 后缀 `_9`，pp.201–223）；章内小节 ⚠️ 推定（无公开样章），
> 按 learn.microsoft.com Synapse Link 文档域组织。云服务不可实测，机制一律「⚠️ 转述 + ✅ URL
> （2026-10-02 验 200）」；本章含 🔧 类比实验一组（E4，**非 Synapse 引擎/平台行为**）。

## 9.1 本章在全书中的位置

第 9 章把 01 章「新鲜度」度量产品化：Synapse Link 不是一条管道，而是一族**旁路复制通道**——源系统
（Azure SQL DB / SQL Server 2022 / Cosmos DB / Dataverse）自动把行数据（快照）与变更流（增量）
投递到湖（+可选仓），分析引擎零 ETL 直接消费 ⚠️ ✅ `synapse-link/sql-synapse-link-overview`。
它与 07 章管道构成「推拉互补」，是副题「数仓→湖仓」过渡中最能被低估的一翼。

## 9.2 机理：快照 + 变更日志的持续合并

- 关系型 Link（Azure SQL DB/SQL Server 2022）：在源侧生成**列存快照+增量变更文件**直写目标存储，
  Synapse 侧暴露为可直接 SQL/Spark 查询的表；主库不受分析查询冲击 ⚠️ ✅
  `synapse-link/sql-database-synapse-link`、`synapse-link/sql-server-2022-synapse-link`；
- Cosmos DB Link：走**变更流（change feed）+ 分析存储（columnstore, TTL 关）** 双路，无需
  Copy Activity/ETL ✅ `synapse-link/how-to-connect-synapse-link-cosmos-db`；仓侧 Serverless 亦可
  联邦查询分析存储 ✅ `sql/query-cosmos-db-analytical-store`；
- 一致性/延迟口径 ⚠️ 转述：秒到分钟级「近实时」，非严格一致读；故障转移等边界行为有官方已知问题清单 ✅
  `synapse-link/synapse-link-for-sql-known-issues`（工程必读页）。

## 9.3 🔧E4：用 SQLite 触发器复刻「快照+增量」的最小骨架（非 Synapse 引擎/平台行为）

OLTP 表 `orders` 上挂 AFTER INSERT/UPDATE 触发器，把变更落入 `orders_cdc` 追加日志，分析聚合只读
日志侧的「最新像」——原始输出：

```text
E4 CDC capture log (trigger-forced, OLTP untouched):
    (1, 'I', 1, 'Acme', 100.0, 'new')
    (2, 'I', 2, 'Beta', 50.0, 'new')
    (3, 'U', 1, 'Acme', 110.0, 'paid')
    (4, 'I', 3, 'Acme', 75.0, 'new')
E4v2 latest-snapshot aggregate from CDC stream: [('Acme', 185.0), ('Beta', 50.0)]
```

- 读法：`Acme=100+(-100+110)+75` 的「最新值合并」在日志侧完成——这正是 Link 的形态学：**写路径
  只追日志，读路径自己做快照合并**。真实 Synapse Link 用列存快照文件+行版本增量替代触发器方案
  （源库负担远低于本实验的 trigger 同步开销 ⚠️ 转述）；本实验只为把「快照+delta 何时值得」的直觉
  建起来（对照盘上 CDC 纵深：Hudi/Iceberg 目录的增量表章节，在盘 ✅）。
- 边界诚实：SQLite 无法演示分区/事务可见性/自动 schema 演化——那些是托管通道的价值所在 ⚠️。

## 9.4 消费侧：湖上 Delta + 仓内双栖

- Link 落地形态是**Delta（Parquet+事务日志）表**：Spark 直接查询 ✅
  `synapse-link/how-to-query-analytical-store-spark`（Cosmos 路线同页族）；专用池可经外部表继续吃
  05 章三要素红利 ⚠️；
- 监控：Link 是工作区一等资源，有独立管理面与指标 ✅（域内 `synapse-link/` 监控页族，本册引用面
  2026-10-02 验 200 者见 §9.2）；
- 与管道的选择函数 ⚠️ 推定处方：**源系统可控且要「零作业」→ Link；跨异构源/需变换整形/审批编排 →
  管道**；两者在「装载 SLA 与源库隔离度」上互换。

## 9.5 Dataverse/Power Platform Link（书中一段 ⚠️ 组织）

- Dataverse 表经「同步到 Synapse 的导出」进入湖，CRM 分析场景零管道 ⚠️；2026 口径该链路目标端
  已是 Fabric：官方页「Link your Dataverse environment to Microsoft Fabric」✅
  https://learn.microsoft.com/en-us/power-apps/maker/data-platform/azure-synapse-link-view-in-fabric
  （本册验 200；该页标题仍保留 Azure-Synapse-Link 旧名，即历史脉络证据 ⚠️）。

## 9.6 常见误区

1. **「Link 取代 CDC 管道」**——严格窗口合并、跨源 join、数据质量闸门仍属编排面（07 章）⚠️。
2. **「近实时=实时一致」**——快照+增量的合并语义不保证跨表同一时点 ⚠️（known-issues 页有边界清单 ✅）。
3. **「源库从此免费」**——生成列存快照与变更文件仍耗源侧 IO/CPU，容量评估要做（对位盘上
   [../Practical_Lakehouse_Architecture/00-总览与阅读地图.md](../Practical_Lakehouse_Architecture/00-总览与阅读地图.md)
   的源库隔离讨论 ⚠️）。
4. **「Link 表无需治理」**——湖侧表若不做 Gold 加工，会把 OLTP 结构变更直接暴露给 BI——schema
   漂移治理仍是人的事 ⚠️。

## 9.7 四通道能力对照表（⚠️ 推定组织；通道文档面 ✅ 本册已验）

| 通道 | 源侧要求 | 落地形态 | 消费面 | 典型边界 |
| --- | --- | --- | --- | --- |
| Azure SQL DB Link | 托管实例+区域配对 | 快照+增量（Parquet/Delta 族） | Serverless/Spark/专用池外表 | 故障转移需重配 ⚠️ known-issues |
| SQL Server 2022 Link | on-prem 2022 + Azure 侧组件 | 同上形态 | 同上 | 版本硬门槛 ⚠️ |
| Cosmos DB Link | 容器开变更流/分析存储 | 分析存储列存副本 | Spark connector/Serverless | TTL/分区热点 ⚠️ |
| Dataverse 导出 | 环境管理员授权 | 同步表至 Synapse/Fabric | SQL/BI 直查 | 表集选择粒度 ⚠️ |

- 对照用法：先查「源侧要求」列决定可行性，再用「典型边界」列估运维负债；消费面一列全部回指
  05/06 章引擎，不再有第四种算力 ⚠️ 推定。
- 本表为编者综合（非书页逐字）；四通道官方入口分别 ✅ `synapse-link/sql-database-synapse-link`、
  `synapse-link/sql-server-2022-synapse-link`、`synapse-link/how-to-connect-synapse-link-cosmos-db`、
  power-apps 页（§9.5 全 URL）。

## 核心概念速览（中英对照）

- **Synapse Link** — 零 ETL 旁路通道族：Azure SQL DB/SQL Server 2022/Cosmos/Dataverse→湖(+仓) ✅。
- **快照+增量** — Snapshot + Delta：初始列存快照叠加持续变更流，读侧合并出「最新像」（🔧E4 类比）。
- **变更流** — Change Feed：Cosmos DB 的有序变更日志，Link 的增量输入 ✅。
- **分析存储** — Analytical Store：Cosmos 容器上的列存副本（与 OLTP RU 隔离）✅。
- **近实时** — Near-Real-Time：秒~分钟级新鲜度目标，非强一致读 ⚠️。
- **已知问题清单** — Known Issues：故障转移/大事务/类型边界的行为备案页 ✅（工程必读）。
- **Delta 落地** — Delta on Landing：Link 目标形态为可 Spark/SQL 双消费的湖表 ⚠️。
- **推拉互补** — Push(Pipelines)/Pull(Link)：07/09 章的通道选型函数（§9.4）。
- **源库隔离** — Source Isolation：分析流量不打扰生产库——Link 的存在理由（01 章新鲜度轴）。
- **Dataverse 导出** — Dataverse Export：CRM→湖仓的托管 Link 线路 ✅ power-apps 页。

## 最新演进与工业实践

2021→2026（URL 均 2026-10-02 验证 ✅ 200；描述 ⚠️ 转述）：

- **Fabric Mirroring 是 Link 的现役形态**：Azure SQL（含 MI）/Cosmos/Dataverse/Snowflake 等到 OneLake
  的镜像通道 ✅ https://learn.microsoft.com/en-us/fabric/mirroring/explore、
  https://learn.microsoft.com/en-us/fabric/mirroring/azure-sql-managed-instance（本册验 200）——
  概念谱系「快照+增量+源库隔离」原样继承，目标存储从 ADLS 换 OneLake ⚠️。
- **旧连接器 slug 勘误**：2021 代 `synapse-link/connectors/what-is-synapse-link-sql-pool` 等 connectors
  子树已 404，现役为 `synapse-link/sql-synapse-link-overview` 等平铺页（登记
  [00](00-总览与阅读地图.md) §2）。
- **湖仓增量语义的行业对照**：Link/Mirroring 解决「OLTP→湖」的托管增量；开放表格式（Hudi upsert/
  clustering、Iceberg CDC 布局、Paimon LSM 流式湖仓）承接「湖内」增量——盘上四册可纵深：
  [../Apache_Hudi_Definitive_Guide/00-总览与阅读地图.md](../Apache_Hudi_Definitive_Guide/00-总览与阅读地图.md)、
  [../Apache_Paimon_Streaming_Lakehouse/00-总览与阅读地图.md](../Apache_Paimon_Streaming_Lakehouse/00-总览与阅读地图.md)
  （均在盘 ✅，02 章已登记）。
- **工业实践**：零 ETL 通道在 2024+ 成为各云标配（同类：Databricks Auto CDC、Snowflake Zero-ETL
  到 Redshift 等 ⚠️ 口径）；本书 9.4 的「推拉互补」升级为「**托管镜像优先，管道兜异源**」的默认序 ⚠️。
- **架构对位**：0→1 建「仓外分析通道」的决策框架见盘上
  [../Practical_Lakehouse_Architecture/00-总览与阅读地图.md](../Practical_Lakehouse_Architecture/00-总览与阅读地图.md)
  （波规点名对位，实链 ✅）。
