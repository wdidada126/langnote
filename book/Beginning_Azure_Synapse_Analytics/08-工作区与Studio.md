# 08 工作区与 Studio — Synapse Workspace and Studio（原书第 8 章，pp.175–199）

> 章题与页区间 ✅ Crossref 存款记录实抓（DOI 后缀 `_8`，pp.175–199）；章内小节 ⚠️ 推定（无公开样章），
> 按 learn.microsoft.com 工作区/安全/监控文档域组织。云服务不可实测，机制一律「⚠️ 转述 + ✅ URL
> （2026-10-02 验 200）」；本章无 🔧 组（五组分布于 02/05/09 章，见 [00](00-总览与阅读地图.md) §6）。

## 8.1 本章在全书中的位置

第 8 章从「用户使用面」重新切一刀：工作区（Workspace）是资源合同，Studio 是人机界面。04 章给了架构
横截面，本章给的是**每天打开浏览器后看到的东西**——Data/Notebooks/Data Pipelines/Monitor/Manage 各
hub、Power BI 集成、安全与网络选项、以及把一切资产纳入版本控制的 Git 线。

## 8.2 工作区：一个 ARM 资源的捆绑合同

- 创建即捆绑：资源组 + 默认 ADLS Gen2 存储 + 受管身份（workspace managed identity）+ 计费锚点 ⚠️
  ✅ `get-started-create-workspace`、`quickstart-create-workspace`；
- 池是工作区的子资源：专用池/Serverless/Spark 池各有独立启停与计量（05/06 章回收）✅ `overview-what-is`；
- 命名与域名事实 ⚠️ 转述：工作区派生 SQL 端点（`xxx.sql.azuresynapse.net` 形态）——连接串文档 ✅
  `sql-data-warehouse/sql-data-warehouse-connection-strings`；SSMS/sqlcmd 等生态经 TDS 接入 ✅
  `sql/connect-overview`（同族页）。

## 8.3 Studio：多引擎体验的统一入口

- 六大 hub（2021 代）⚠️ 组织：Data（湖+仓资产目录）、Spark/Data 笔记本、Data Pipelines、Monitor、
  Manage、Power BI/Data Hub；
- **Knowledge store**：对湖内文档建索引供 SQL 检索（Preview 工件）✅ `get-started-knowledge-center`
  ——本章最能体现「分析面继续外扩」的小样本；
- 内建开发体验：笔记本/脚本编辑/草稿-发布双态（管道与笔记本）⚠️；
- 监控中心：Active queries/管道运行/Spark 会话一屏，跨引擎事故时间线的起点 ✅ `get-started-monitor`、
  `monitoring/how-to-monitor-sql-requests`。

## 8.4 安全与网络（与 04 章横切层同图放大）

- 双层 RBAC：Azure RBAC 管控制面（建池/删工作区），**Synapse RBAC** 管数据面（执行 Spark/发布管道/
  读写库表）✅ `security/synapse-workspace-synapse-rbac`、`security/synapse-workspace-access-control-overview`；
- 身份：AAD/Entra 为根，SQL 侧用户建模式落库（外部用户从托管身份映射）⚠️（白皮书线 ✅
  `guidance/security-white-paper-authentication` 域内）；
- 网络三态：公网上限+IP 防火墙 / 专用链接+托管专用终点 / **受控虚拟网络**（全托管私有出站）⚠️
  ✅ `security/synapse-workspace-managed-vnet`、`security/synapse-workspace-ip-firewall` 域内页；
- 数据出口防渗漏（data exfiltration protection）与 CMK 加密 ⚠️（✅ `security/workspaces-encryption` 域、
  `security/workspace-data-exfiltration-protection`——本册引用面 2026-10-02 全验 200）。

## 8.5 DevOps 线：Git 集成与发布

- 工作区绑定 Azure DevOps/GitHub 仓库→分支协作、草稿/协作分支模型、ARM 模板导出发布 ✅
  `cicd/source-control`（07 章三件套在本章获得仓库学细节）；
- 发布粒度 ⚠️ 推定：管道/笔记本/触发器为模板单元，池参数与链接服务用 release 参数重绑——
  「开发订阅→生产订阅」的跨环境纪律与 ADF 同源。

## 8.6 Power BI 与可视化直连

- 工作区一键绑定 Power BI 工作区；专用池/Serverless 结果可存为 Power BI 数据集（导入/DirectQuery
  两路）⚠️ ✅ `get-started-visualize-power-bi`；
- 语义资产分层：仓视图=最低公分母语义层，BI 度量层在 Power BI 侧——本书角色三分（01 章 §1.7）在
  工具上的落点 ⚠️ 推定组织。

## 8.7 常见误区

1. **「Studio=SSMS 上位替代」**——Studio 管编排与混合资产，重型 T-SQL 开发/执行计划深看仍回 SSMS
   （05 章配套）⚠️。
2. **「工作区 RBAC 配好了就安全」**——数据面权限（SQL 用户/存储 ACL/受管身份三角）缺一即漏 ⚠️。
3. **「Knowledge store 是全文检索标配」**——2021 Preview 工件，2026 已由其他形态承接（见演进节）⚠️。
4. **「托管 VNet 只是开关」**——它改变出站拓扑与成本面（IR/私有终点流量），评审要前置 ⚠️。

## 8.8 工作区上线检查清单（工程视角 ⚠️ 推定组织，引用面见 §8.2–8.5）

**网络与安全**
- [ ] 公网/受控 VNet 已评审并固化（✅ `security/synapse-workspace-managed-vnet`、`security/synapse-workspace-ip-firewall`）
- [ ] 私有链接+托管专用终点覆盖存储/SQL/Cosmos 依赖（防意外出站）
- [ ] Synapse RBAC 角色映射到岗位表（分析师/工程师/科学家三类起步）✅ `security/synapse-workspace-synapse-rbac`
- [ ] CMK/加密与出口防渗漏选项显式决策（合规驱动则默认拒绝出站）✅ `security/workspaces-encryption`、
      `security/workspace-data-exfiltration-protection`

**资产与命名**
- [ ] 湖目录分层规范落文件（bronze/silver/gold + 环境前缀），Studio Data hub 可见即可治理
- [ ] 池命名含容量档与 SLA 级（prod-dw-gen2-500 风格示例 ⚠️ 示意非推荐值）
- [ ] 笔记本/管道草稿与发布分支纪律在 Git 绑定后第一次提交前讲清 ✅ `cicd/source-control`

**可观测**
- [ ] Monitoring Hub 三面指标（SQL/Spark/管道）有告警订阅（Azure Monitor 动作组）✅ `get-started-monitor`
- [ ] 查询标签制度启用（成本归因到团队/项目 ✅ `sql-data-warehouse/sql-data-warehouse-develop-label`
      域内机制——本册按存在性引用）
- [ ] 每月一次监控评审例会（复盘模板对位 10 章 ✅ `guidance/implementation-success-perform-monitoring-review`）

- 清单逻辑：8.2 的资源合同 + 8.4 的安全双层 + 8.5 的发布三件套，逐项变成可勾选的上线门槛 ⚠️ 推定。

## 核心概念速览（中英对照）

- **Synapse 工作区** — Workspace：捆绑存储/池/身份/计费的 ARM 资源单元 ✅ get-started-create-workspace。
- **受管身份** — Managed Identity：工作区访问存储/密钥的免密代理身份 ⚠️。
- **Synapse RBAC** — 数据面角色：跨 Spark/管道/元数据的细粒度授权，与 Azure RBAC 双层并存 ✅。
- **Studio hubs** — Data/Notebooks/Pipelines/Monitor/Manage：浏览器端的五类工作场 ⚠️。
- **Knowledge store** — 知识存储：对湖文档建索引供 SQL 检索的 2021 Preview 工件 ✅ knowledge-center。
- **监控中心** — Monitoring Hub：跨引擎作业时间线与事故追溯入口 ✅ get-started-monitor。
- **受控虚拟网络** — Managed VNet：全托管私有出站的网络最高档 ✅ synapse-workspace-managed-vnet。
- **专用链接** — Private Link： Studio 与数据服务的最小暴露面接入 ✅ access-control-overview 域。
- **草稿/发布双态** — Draft/Committed：Git 绑定下的资产生命周期（管道/笔记本）✅ cicd/source-control。
- **BI 直连绑定** — Power BI Linkage：数据集保存与 DirectQuery 到 SQL 端点的可视化桥 ✅。

## 最新演进与工业实践

2021→2026（URL 均 2026-10-02 验证 ✅ 200；描述 ⚠️ 转述）：

- **Studio 血统进入 Fabric**：Fabric 的工作区+Items 模型（湖仓/仓库/笔记本/管道/事件中心同舱）是
  Synapse Studio hub 模型的直系后代；试用入口 ✅ https://learn.microsoft.com/en-us/fabric/get-started/fabric-trial；
  本章的「一个浏览器五种活」体验在 2026 由 Fabric 门户复刻 ⚠️。
- **Knowledge store 已收编/退役 ⚠️**：Synapse 文档域内页 ✅ `get-started-knowledge-center` 仍在线，
  但该能力未进入 Fabric 主线（2026 口径下全文/事件检索走其他项）——按历史工件读 ⚠️ 转述。
- **安全文档域现状**：RBAC 总览 ✅
  https://learn.microsoft.com/en-us/azure/synapse-analytics/security/synapse-workspace-synapse-rbac、
  安全白皮书入口 ✅ https://learn.microsoft.com/en-us/azure/synapse-analytics/guidance/security-white-paper-introduction
  （2026-10-02 验 200）；Fabric 侧对应物为工作区角色+OneLake 安全 ACL ⚠️（盘上
  [../Fundamentals_of_Microsoft_Fabric/00-总览与阅读地图.md](../Fundamentals_of_Microsoft_Fabric/00-总览与阅读地图.md)
  治理章有对位，#221 不同书三角辨析见 [00](00-总览与阅读地图.md) §4）。
- **旧 slug 勘误**：2021 代 `quickstart-create-workspace` 之外的部分工具页（如
  `monitoring-working-party-arcade` 监控「工作派对」教程）已 404（登记
  [00](00-总览与阅读地图.md) §2）；照抄旧链接的运维手册需全量重验。
- **工业实践**：2026 年新建微软侧分析平台的团队默认从 Fabric 工作区起步，Synapse 工作区进入「存量
  运维+迁移评估」状态 ⚠️；本章的双层 RBAC/网络三态/Git 三件套仍是理解 Fabric 权限模型的必要先修 ⚠️。
- **波9 收束互挂**：Fabric 工作区新形态见 [00](../Microsoft_Fabric_Data_Factory_Playbook/00-总览与阅读地图.md)（管道面）与 [00](../Learn_Microsoft_Fabric/00-总览与阅读地图.md)（治理章）对位 ⚠️。
