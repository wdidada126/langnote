# 06 Mirroring 近实时复制 — The Data Engineer's Guide to Microsoft Fabric（⚠️ 主题重构章）

> ⚠️ 主题域重构章（00 §5 口径）：对位书名中"事务库到分析面"的持续同步面。机制事实 ✅ 来自
> learn.microsoft.com/fabric/mirroring 域当日 200 页与文件清单实抓；🔧E5 为本机类比（非 Fabric）。

## 6.1 Mirroring 的物种定位：把"链接服务"升维成"镜像库"

✅ 转述 `https://learn.microsoft.com/en-us/fabric/mirroring/overview`（当日 200）：Mirroring 对
SQL Server / Azure SQL（库与托管实例）/ Cosmos DB / PostgreSQL / MySQL 等源建立**持续同步的
Fabric 内只读副本**——副本以 Delta 表（湖侧）和/或 T-SQL 可查形态存在，引擎自动完成初始种子
（seed）、CDC 流式应用与断线恢复。对照谱系：Synapse/ADF 时代的"链接服务（Azure Synapse Link）"
是其前世 ⚠️（✅ 域内 `azure-cosmos-db-migrate-synapse-link` 页名实抓，谱系有据）。

与 `05` 章三岔路的关系（⚠️ 重构的边界表）：

| 维度 | Copy job/Dataflow（05 章） | Mirroring（本章） |
|---|---|---|
| 触发 | 排程/手动批 | 常驻流式 |
| 延迟 | 分钟~天 | 秒~分钟 ⚠️（当日页为 SLA 权威） |
| 删除语义 | 盲区（水位看不见 DELETE） | 捕获（CDC 本质）✅ |
| 源侧负担 | 查询拉取 | 一次快照+变更日志订阅 ✅ |
| 目标 | 你指定的任意表 | 镜像库整体结构 ✅ |

## 6.2 初始种子与自动 reseed：镜像的"生死流程"

✅ 域内页名实抓：`azure-sql-database-automatic-reseed`、`sql-server-configure-automatic-reseed`
等——**种子**（初始全量快照）可能因源端结构漂移、日志断档、权限变更而失败，平台提供自动
reseed：检测到不可续传时自动重打快照而非人工重建。工程师该配置的三件事（⚠️ 重构，机制页 ✅ 在架）：

1. 源侧先决条件：CDC/变更捕获的启用与日志保留窗口——**日志保留期短于最长可容忍停机**是
   reseed 频发的头号根因 ⚠️（社区共识+✅ `*-limitations` 页族在架）。
2. 镜像范围与命名：整库镜像会带进垃圾表；范围裁剪是治理不是偷懒（⚠️ 编者语）。
3. 成本预期：seeding 是全量数据移动，会同时消耗源库 IO 与目标容量——reseed 不是免费按钮 ⚠️。

## 6.3 SQL 端点镜像（Enterprise 线）与只读副本边界

✅ `mirroring/overview` 导航域含 SQL database mirroring（Fabric 内建 SQL 数据库的镜像形态，
企业级读扩展）⚠️ 转述级：主库→镜像库的持续复制用于**读缩放与隔离**，与"事务库→湖"的
Lakehouse mirroring 目标不同。边界共识（⚠️）：所有镜像面**不可写**——镜像是分析入口不是
应用数据面；要回写请走事件/管道（`05/07` 章）。

## 6.4 🔧 实验 E5：镜像语义的最小模型（非 Fabric 行为）

本机 SQLite→DuckDB（脚本 `exp.py`，2026-10-02 实测）：把 `05` 章留下的 100,002 行源库
`inc.db` 经 ATTACH 映射进 DuckDB 并物化镜像表——

```text
[E5] ATTACH sqlite=57.68 ms; COPY->mirror table=43.24 ms;
     mirrored rows=100002 sum=7500076887.0 (mirror reads identical to source => verification passed)
```

- 两段式成本：ATTACH（≈种子/建链）与物化（≈首刷）分开计时——对应真实镜像的
  "seed→catch-up→steady" 三段生命周期 ⚠️。
- 行数与聚合值双核对 = 镜像验收断言（`rowcount identical + sum match`），5.5 节"三件套"的
  镜像版。
- 本模型是**一次性快照**，不含持续应用：真实 Mirroring 的差异化价值恰在"稳态增量应用+断线
  续传"，本机无法类比其日志订阅机制（⚠️ 缺口如实登记，不假装有数）。

## 6.5 镜像之上的消费形态

⚠️ 重构+✅ 机制页支撑：镜像表落湖后进入 `03` 章生命周期（SQL 分析端点读、笔记本加工、BI 直连）；
镜像域专页族（`azure-cosmos-db-lakehouse-notebooks`、`azure-sql-database-tutorial` 等教程/限制/
故障排除三件套页名实抓 ✅）说明官方按"源类型 × 教程/限制/排障"矩阵组织文档——数据工程师的
runbook 应同构组织 ⚠️。

## 6.6 什么时候不该用 Mirroring（⚠️ 编者反模式清单）

1. **超大低频档案库**：常驻流的成本换不来收益，用 `05` 章 Copy job 季刷。
2. **需要转换后再入库的源**：镜像保真=脏数据也保真；清洗面放湖内侧（银层，`09` 章），别在源侧求干净。
3. **合规禁止变更日志出域的场景**：CDC 订阅即数据出域，先过治理评审（`10` 章回收）。
4. **日志保留窗口极短的遗留库**：任何停机窗口都会触发 reseed 风暴（6.2 条 1）——先修源侧配置再谈镜像。
5. **源库 DBA 未签核就开整库镜像**：镜像的"便利"对源端是真实负载（6.4 成本曲线的镜像版 ⚠️），
   范围裁剪（Scoping）不仅是治理问题，更是邻里关系。

补一条正向判据 ⚠️：Mirroring 的**净收益 = 免建的三样东西**——CDC 管道、水位表、对账脚本
（05/09 章各自的手工作业在此归零）；三样都不用建的平台场景，镜像只是多余的常驻流。
验收动作固化（🔧E5 模式）：每次 reseed 后跑一遍"行数+聚合"双核对，绿灯才解除变更冻结 ⚠️ 流程建议。

## 6.7 与盘上诸书的联系

- 姊妹章：[../Fundamentals_of_Microsoft_Fabric/06-数据集成三件套.md](../Fundamentals_of_Microsoft_Fabric/06-数据集成三件套.md)
  （三件套含 Mirroring 的地图位）。
- CDC/变更流机制正主（开放格式形态）：
  [../Delta_Lake_Definitive_Guide/10-设计模式-CDC与SCD.md](../Delta_Lake_Definitive_Guide/10-设计模式-CDC与SCD.md)
  与 [../Delta_Lake_Definitive_Guide/07-高级特性-DV与CDF.md](../Delta_Lake_Definitive_Guide/07-高级特性-DV与CDF.md)——
  CDF（change data feed）与本章"变更流应用"同一语义场 ✅ 章内已有浅讲，读本书不懂时去那里补机制。
- 复制语义理论：[../Streaming_Systems/06-流和表.md](../Streaming_Systems/06-流和表.md)
  （日志订阅/流表二象性——镜像=把源表持续物化为副本表的通用底座）。
- 事务→分析谱系纵深：[../PostgreSQL数据库内核分析.md](../PostgreSQL数据库内核分析.md)（盘上单文件册，实链核验通过：
  源端事务引擎（WAL/逻辑复制）机制视角，与本章问题同构，厂商栈不同 ⚠️ 对照读）。
- 波内登记：#220（Mirroring 食谱纵深，挂点=6.2/6.5）、#219（Synapse 链接服务旧谱系，挂点=6.1 前世段）。

## 核心概念速览（中英对照）

- **镜像库** — Mirrored Database：源库在 Fabric 内的持续同步只读副本，Delta/T-SQL 双形态 ✅。
- **种子** — Seed：初始全量快照；seed→catch-up→steady 三段生命周期 ✅⚠️。
- **自动重播** — Automatic Reseed：不可续传时自动重打快照；日志保留期是头号触发器 ✅⚠️。
- **变更捕获** — CDC Capture：镜像的语义心脏，删除与更新不再盲区 ✅（对照 05 章水位）。
- **只读边界** — Read-only Surface：镜像不可回写，回写走事件/管道 ⚠️✅。
- **源负担曲线** — Source Load Profile：一次快照+日志订阅 vs 反复拉取（6.1 表）✅⚠️。
- **范围裁剪** — Scoping：镜像整库/部分表的治理决策，垃圾表也有成本 ⚠️。
- **验收断言** — Verification：行数+聚合双核对（🔧E5），镜像 runbook 的固定条目 ⚠️。
- **矩阵文档法** — Matrix Docs：源类型×教程/限制/排障的官方组织式（6.5）✅。
- **前世** — Synapse Link Lineage：链接服务→Mirroring 的谱系迁移线 ✅页名实抓。

## 最新演进与工业实践

2024→2026（URL/页名 2026-10-02 实测 ✅；⚠️ 为推断）：

- **源矩阵扩张**：当日 mirroring 域文件清单实抓 ✅ 显示 SQL Server/Azure SQL（DB+MI）/Cosmos
  DB-NoSQL/PostgreSQL/MySQL 全线各有教程+限制+排障专页，另有 `fabric-database-mirroring`、
  `azure-database-postgresql-how-to-data-security` 等安全/内镜像页——2024 出版时点的源支持表
  今读必然过期，引用当日重验（00 §9 纪律）。
- **旧路径化石登记**：`/fabric/database-mirroring/overview` 已不可达、`/fabric/mirroring/overview`
  为现行（波5 #221 与本册双验）——文档域改名本身记录了产品从"库镜像特性"到"独立工作负载"的升格 ⚠️。
- **工业实践画像** ⚠️（通识）：镜像落地的三大运维件=源侧日志保留审计、reseed 告警订阅、
  镜像延迟监控（源时间 vs 应用位点差）；与 🔧E4/E5 的"水位/两段账"模型同构，可在 SQLite/DuckDB
  原型上先练手再上平台。
- **与治理面接缝**：镜像=跨边界数据流动， Purview 敏感标签继承与审计（`10` 章）在其上运行
  （✅ governance 域页族在架）；合规团队对"哪些表被镜像"应有目录级可见性（⚠️ 编者建议，
  呼应 #190 目录册的主动元数据语境）。
