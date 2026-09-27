# 11 · Iceberg 托管表与开放格式互操作（⚠️ 推定主题章）

> **性质声明**：推定主题重构（[00](00-总览与阅读地图.md)）。机制=官方文档转述（⚠️）+✅URL；
> Iceberg 不可本机连测（沿用前波口径：DuckDB iceberg 扩展"可装不可查"，本册不再重复该类比）。
> TDG 对位：[../Snowflake_The_Definitive_Guide/12-数据云工作负载.md](../Snowflake_The_Definitive_Guide/12-数据云工作负载.md)（湖仓负载入门面）。

## 本章地图

| 节 | 内容 | 一句话结论 |
| --- | --- | --- |
| 11.1 | 两条路线：直读/写外部 Iceberg vs Snowflake 托管 Iceberg | "用你的格式"与"替你看格式"的分工 |
| 11.2 | catalog-linked database：目录主权回收 | 目录成为治理与互操作的锚 |
| 11.3 | 托管表的能力面：聚簇/复制/优化 | 闭源红利逐步注入开放表 ⚠️ |
| 11.4 | Open Catalog / Polaris 线 | 目录产品化对位 |
| 11.5 | v3/删除向量等格式演进（2026 快照） | 与前波笔记对表 |
| 11.6 | 选型矩阵：微分区 vs Iceberg 托管 | 迁出自由度 vs 托管省力度 |

## 核心精讲

### 1. 形态学（转述 ⚠️，✅ 页组齐备）
- **Iceberg 表总览**：✅ https://docs.snowflake.com/en/user-guide/tables-iceberg
- **Snowflake 托管表（create-iceberg-table 语法线）**：✅ https://docs.snowflake.com/en/sql-reference/sql/create-iceberg-table
  ——Snowflake 写并提交 Iceberg 元数据，客户引擎可直读云存储：格式开放、优化托管。
- **catalog-linked database（CLD）**：✅ https://docs.snowflake.com/en/user-guide/tables-iceberg-catalog-linked-database
  ——账户绑定外部目录（Glue/Polaris/Snowflake Open Catalog 等），目录成为跨引擎一致治理锚点。
- **Open Catalog 同步**：✅ https://docs.snowflake.com/en/user-guide/tables-iceberg-open-catalog-sync

### 2. 外部引擎视角（转述 ⚠️）
经 Horizon 目录授权后，Spark/Fabric/Trino 等外部引擎可读写（写支持范围逐步扩张 ⚠️）：
✅ https://docs.snowflake.com/en/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon 、
✅ https://docs.snowflake.com/en/user-guide/tables-iceberg-query-using-microsoft-fabric 、
✅ https://docs.snowflake.com/en/user-guide/externally-managed-iceberg-tables-access-horizon-irc
治理策略穿透在第 10 章已展开——**本章是"格式的互操作面"，10 章是"策略的强制面"**，同页两面。

### 3. 复制与容灾视角（转述 ⚠️）
托管 Iceberg 表纳入原生复制/failover 体系：
✅ https://docs.snowflake.com/en/user-guide/tables-iceberg-replication （对读第 12.6/01 章容灾线，
✅ https://docs.snowflake.com/en/user-guide/account-replication-intro 、
✅ https://docs.snowflake.com/en/user-guide/database-failover-config 、
✅ https://docs.snowflake.com/en/user-guide/database-replication-failover）。

### 4. 能力灌注清单（⚠️ 逐项以页内为准，不虚构函数名）
| 能力 | 微分区原生表 | Iceberg 托管表（2026 口径） |
| --- | --- | --- |
| 值域裁剪 | ✅ 默认 | ⚠️ 依赖分区+元数据，逐步增强 |
| 聚簇类优化 | ✅ 自动聚簇 | ⚠️ 文档线出现排序/优化类能力，命名未逐条核实 |
| Time Travel | ✅ | ⚠️ 快照=格式原生语义 |
| 零复制克隆 | ✅ | ⚠️ 部分（以页内为准） |
| 治理穿透 | ✅ | ✅ Horizon 线（10 章） |
| 外部引擎直读 | ✗ | ✅ 本质卖点 |
（左列基础语义对读 TDG-07/TDG-09；右列本表全部 ⚠️，除已 ✅ 的 URL 支撑项。）

### 5. 与前波三册 Iceberg 笔记的接缝
Iceberg 格式机制（快照/清单/分区演化/删除向量）不在本册重讲——直接进正典：
[../Apache_Iceberg活用入門/03-隐藏分区与分区演化.md](../Apache_Iceberg活用入門/03-隐藏分区与分区演化.md)、
[../Apache_Iceberg活用入門/08-表维护操作.md](../Apache_Iceberg活用入門/08-表维护操作.md)、
[../Use_Iceberg_with_Spark/04-时间旅行与元数据表.md](../Use_Iceberg_with_Spark/04-时间旅行与元数据表.md)、
[../Engineering_Lakehouses_with_Open_Table_Formats/09-Catalog与互操作.md](../Engineering_Lakehouses_with_Open_Table_Formats/09-Catalog与互操作.md)、
[../Apache_Paimon_Streaming_Lakehouse/00-总览与阅读地图.md](../Apache_Paimon_Streaming_Lakehouse/00-总览与阅读地图.md)。

### 6. 一页决策备忘骨架（方法论 ⚠️）
选型四问：① 谁读这份数据（仅本仓 or 跨引擎）？② 谁写（Snowflake or 双流写入）？
③ 第 4 章三件武器的收益是否可放弃（见 11.4 矩阵）？④ 目录主权归谁（11.1 CLD vs 自建）？
只有①②同时"跨"时才值得付托管表的能力折价——其余场景"双层架构"（核心微分区+共享层 Iceberg）
是 2026 社区主流答案 ⚠️（转述）。

## 常见误区

| 误区 | 事实（转述 ⚠️） |
| --- | --- |
| "用了 Iceberg 就逃出供应商" | 托管优化/治理越深，**目录与安全模型**的黏性越高 |
| "直读=零成本" | 缺值域/统计红利时，外部表账单常以慢查询形态偿还 |
| "CLD 只是换个 catalog 地址" | 它是主权模型变更：提交者、权限与审计路径都重排 |
| "格式版本自动追新" | v3/删除向量等需平台侧 GA 节奏（11.6），文档 release-notes 是唯一裁判 |

## 与其他章、其他书的联系

- 治理强制面 → [10-治理与安全进阶.md](10-治理与安全进阶.md)；容灾 → [01-计算模型与弹性深潜.md](01-计算模型与弹性深潜.md)（复制语义在 10.5/11.3）；
  聚簇对照 → [04-聚簇与搜索优化.md](04-聚簇与搜索优化.md)；账单对照 → [02-成本模型与计费内核.md](02-成本模型与计费内核.md)。
- 湖仓总纲对读：[../The_Data_Lakehouse/00-总览与阅读地图.md](../The_Data_Lakehouse/00-总览与阅读地图.md)、
  [../Practical_Lakehouse_Architecture/00-总览与阅读地图.md](../Practical_Lakehouse_Architecture/00-总览与阅读地图.md)、
  [../Delta_Lake_Definitive_Guide/12-Delta-Sharing.md](../Delta_Lake_Definitive_Guide/12-Delta-Sharing.md)。
- 【登记·同波不链】BigQuery Iceberg 外部表、Redshift→S3 Tables 路线对照，波尾挂两兄弟目录。

## 本章自测（3 分钟）

1. 同一张高频点查表从微分区迁到 Iceberg 托管表，第 4 章三件武器（聚簇/搜索优化/MV）哪些
   还确定可用？不确定项去哪个页面找答案？
2. CLD 与"把 Glue 表挂成 Iceberg 表直接查"的本质区别是**谁提交元数据**——据此解释审计边界变化。
3. 外部 Spark 引擎经 Horizon 读写时，第 10 章哪几层策略仍在强制？哪几层大概率失守？

## 核心概念速览（中英对照）

1. **托管 Iceberg 表** — Snowflake-managed Iceberg table：平台写开放格式+托管优化。
2. **catalog-linked database** — CLD：账户绑定外部目录的数据库形态。
3. **Horizon Catalog** — Snowflake 托管目录：治理随 REST 访问强制（10 章）。
4. **Open Catalog/Polaris 线** — 开源目录对位：格式主权的第三极。
5. **删除向量** — deletion vectors：v3 高效 MoR 删除形态（前波 ✅ 已证 GA 页）。
6. **快照** — snapshot：Iceberg 原生时间旅行单位，≈Time Travel 的开放版。
7. **直读** — direct read：外部引擎绕过 Snowflake 计算读云存储。
8. **能力灌注** — managed 特性向开放表迁移的过程（本册 ⚠️ 矩阵）。
9. **格式版本博弈** — spec v-next vs 平台 GA 节奏：选型时间差风险。
10. **黏性再分配** — 数据黏性从私有文件转向目录/权限体系。
11. **互操作面** — 本章主题词：与 10 章"强制面"对偶。
12. **微分区对照** — 闭源布局引擎：本册 3/4 章主角，选型矩阵左列。

## 最新演进与工业实践

**2024–2026（URL 均 2026-09-27 curl -L 实测 200 ✅）：**

- **Iceberg v3 + 删除向量 GA**（2026-05-07 ✅ https://docs.snowflake.com/en/release-notes/2026/other/2026-05-07-iceberg-v3-ga ，
  前波验证本波复核命中）：开放表侧"布局/删除"两大补课到位，对读
  [../Apache_Iceberg活用入門/08-表维护操作.md](../Apache_Iceberg活用入門/08-表维护操作.md)。
- **Horizon/CLD 文档线成建制**：tables-iceberg* 相关页 67 条 ✅（索引计数），"目录即边界"成为
  官方互操作叙事主轴；外部引擎读写矩阵持续扩张 ⚠️（以页内为准）。
- **托管表进复制体系**（✅ tables-iceberg-replication）：DR 白皮书级场景补齐。
- **工业实践 ⚠️（转述）**：2025+ 参考架构默认"核心热数据微分区 + 共享/跨云层 Iceberg 托管"双层；
  迁出演练（表格式导出可行性）写进采购条款成为新趋势。

**文献与文档**：tables-iceberg / create-iceberg-table / tables-iceberg-catalog-linked-database /
tables-iceberg-open-catalog-sync / tables-iceberg-replication / tables-iceberg-access-using-external-query-engine-snowflake-horizon /
tables-iceberg-query-using-microsoft-fabric / externally-managed-iceberg-tables-access-horizon-irc /
iceberg-v3-ga release note / account-replication-intro / database-failover-config / database-replication-failover（✅200）。
