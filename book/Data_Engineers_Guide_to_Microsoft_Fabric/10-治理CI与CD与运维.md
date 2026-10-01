# 10 治理、CI/CD 与运维 — The Data Engineer's Guide to Microsoft Fabric（⚠️ 主题重构章）

> ⚠️ 主题重构章（00 §5 口径），对位原书尾部的治理/DevOps/运维纵深。机制取证双通道：
> ✅ 当日 200 页（governance/security 域 4 页，00 §9 台账）+ ✅ fabric-docs 目录清单实抓
> （GitHub API 取证通道：governance/security/fundamentals/admin 域文件名，存
> `D:\develops\tmp\dbwave_w9_degfab\dir_*.json`）。🔧 复用 E6/E5。盘上治理学科正主实链回链。

## 10.1 平台治理面全景（✅ 页 → 支柱表）

✅ `governance/governance-compliance-overview`、`governance/onelake-catalog-overview`、
`governance/lineage`、`security/security-overview`（当日 200，00 §9）给出官方支柱划分；
浓缩成工程师视角四支柱（⚠️ 重构）：

| 支柱 | 平台件 | 本册挂点 |
|---|---|---|
| 发现与元数据 | OneLake Catalog | 本章 10.2 |
| 血缘与责任 | lineage + item ownership | 10.2/10.3 |
| 分类与防护 | 标签/敏感度标签/DLP/保护策略 | 10.2 |
| 发布与运行 | git 集成/部署管道/监控中心/容量 | 10.4/10.5 |

⚠️ 结构性论断：Fabric 的治理是**单湖长出来的元数据面**——OneLake 命名空间统一（02 章）是
血缘/目录/策略得以内置的前提；代价是治理词表由平台定义，导出即失效（对照 10.7 开放目录两册）。

## 10.2 OneLake Catalog：目录、血缘、标签与认可

✅ 域内清单实抓的页名族（内容未逐页转述 ⚠️）：

- 目录三件套：`onelake-catalog-overview`（200 实测）、`onelake-catalog-explore`、
  `onelake-catalog-govern`、`onelake-catalog-item-details`、`onelake-catalog-capacities`。
- 血缘：`governance/lineage`（200 实测）——item 级血缘平台自带；03 章表维护历史、05 章
  ADF 同步任务、09 章管道段都会汇进这条河 ⚠️ 汇流细节属推定。
- 自定义标签：`tags-define`、`tags-apply`（✅ 实抓）——轻量人肉元数据，成本在纪律不在工具 ⚠️。
- 敏感度标签重炮（Purview 系）：`microsoft-purview-fabric`、`mandatory-label-policy`、
  `domain-default-sensitivity-label`、`protection-policies-overview/create`、
  `data-loss-prevention-configure/monitor/respond`、标签继承 `service-security-sensitivity-label-*`
  一族（✅ 文件名实抓，十余页——治理文档面膨胀本身是信号 ⚠️）。
- 认可：`endorsement-overview`（✅ 实抓）——certify/promote 把"可信"做成人工流程位。
- 外分边界：`external-data-sharing-overview`（✅ 实抓）——共享是治理最后一公里 ⚠️。

## 10.3 工作区、角色与 item 所有权

✅ fundamentals 域实抓：`workspaces`、`roles-workspaces`、`give-access-workspaces`、
`create-items-in-workspaces`；`item-ownership`（01 章已引 ✅）。⚠️ 工程师推论（一图四用）：

**工作区 = 权限边界 = git 文件夹边界（10.4）= 监控粒度（workspace-monitoring）**——
把工作区设计当微服务边界设计来做，是 Fabric 治理的第一块骨 ⚠️（编者语）。

`domains` / `domains-best-practices`（✅ 实抓）给"主题域"概念位——与 Data Mesh 的域词面
同源、语义不同款（00 §3 已登记编织≠产品辨析，此处再钉一枚：域≠去中心化 ⚠️）。

## 10.4 Git 集成与部署管道（ALM 面）

✅ 清单实抓的文件族证明 item 全家桶进入"仓库同步+管道部署"轨道（页名逐列）：
`git-deployment-pipelines`、`environment-git-and-deployment-pipeline`、
`lakehouse-git-deployment-pipelines`、`notebook-source-control-deployment`、
`spark-job-definition-source-control`、`dataflow-gen2-cicd-and-git-integration`、
`git-eventstream`、`git-kql-queryset`、`git-eventhouse-kql-database`、
`git-integration-admin-settings`（admin 开关位）。

⚠️ 机制推定（不当代页事实用）：**两段式**——① workspace↔Git 双向 sync（覆盖清单当日页
为准，格式=平台自定义 item 文件夹，非裸 SQL/代码 ⚠️ 这是评审体验的痛点）；② deployment
pipeline 做环境推进（dev→test→prod，发布门可挂审批/标签策略）。

数据工程师纪律（⚠️ 编者清单）：管道 JSON、notebook、DDL 全部进评审；**热修复绕管道=治理债**，
其利息在下一次"环境不一致"事故里支付；04 章 spark-job-definition 的 source-control 页名
（✅ 实抓）说明作业定义已可仓库化——这正是"作业即代码"的平台落点。

开源对照实链：[../Analytics_Engineering_with_SQL_and_dbt/00-总览与阅读地图.md](../Analytics_Engineering_with_SQL_and_dbt/00-总览与阅读地图.md)、
[../Unlocking_dbt/00-总览与阅读地图.md](../Unlocking_dbt/00-总览与阅读地图.md)——dbt 的
model+test+docs 是 SQL-only 世界的同一诉求（版本化数据逻辑）⚠️。

## 10.5 监控中心与容量（运维面）

✅ admin 域实抓：`monitoring-hub` 主页+`monitoring-hub-capacity`/`-jobs`/`-alerts`/
`-agents` 子页、`capacity-settings`、`monitoring-workspace`；✅ fundamentals 实抓：
`workspace-monitoring-overview`、`enable-workspace-monitoring`；✅ 200 实测：
`spark-monitoring-overview`（04 章已引）。

⚠️ 角色推定：monitoring-hub 是"平台内长的运维控制台"，替代开源栈 Airflow UI+Grafana+
告警拼装组合；容量（CU）是唯一横贯所有 item 的稀缺资源——**ETL 与交互负载同池互噬**
（04/08 章已两次挂号），容量告警阈值+时段隔离是自保两件套 ⚠️。计费/费率数字一律当日页
（1.4 纪律 ✅，不抄死）。

🔧 复用账（非 Fabric 行为，2026-10-02 实测）：

```text
[E6] events ingested=60000; retention-delete 35.89 ms -> remaining=13545; 2-day tail-window count=3870
[E5] ATTACH sqlite=57.68 ms; COPY->mirror table=43.24 ms; mirrored rows=100002 sum=7500076887.0
```

- E6 → 留存清理是运维日历的**第一动作**（07 章 KQL 保留策略的本机账）；
- E5 → "行数+聚合双核对"验收断言进每个镜像/管道的 runbook，绿灯才算运维完成。

## 10.6 治理与运维巡检清单（⚠️ 编者交付）

1. 新 item 三问：owner 是谁（ownership 页 ✅）、工作区对不对（10.3）、标签打过没有。
2. 血缘周检：断链（手工临时管道）是头号污染源——lineage 上看不到的链路=治理盲区 ⚠️。
3. 部署管道演练：季度做一次 dev→prod 全量重放，验证"环境即代码"没烂。
4. 容量水位：CU 峰值/告警阈值月度回顾（monitoring-hub-capacity 位 ✅ 页名）。
5. 保留策略审计：E6 账——无保留期的事件/日志表是下一场存储账单事故。
6. 孤儿巡检：无 owner、无血缘下游、30 天零访问的 item 走 `tutorial-lakehouse-clean-up` 式清退
  （✅ 页名在 09 章表）。
7. 标签/DLP 抽查：mandatory-label 策略命中率为零=大家绕过或数据真不敏感 ⚠️，两者都要查。
8. 访问重审：give-access 单向门要配双向历（季度 revoke 扫一遍 ✅ 页名在位）。

## 10.7 与盘上诸书的联系

- 治理学科正主：[../Understanding_Data_Governance/00-总览与阅读地图.md](../Understanding_Data_Governance/00-总览与阅读地图.md)、
  [../The_Enterprise_Data_Catalog_2e/00-总览与阅读地图.md](../The_Enterprise_Data_Catalog_2e/00-总览与阅读地图.md)
  ——后者同时是本册 **0642 号段判定的先例出处**（00 §2 首行反链已挂）。
- 开放目录治理对照（封闭 vs 开放两面）：
  [../Data_Governance_with_Unity_Catalog/00-总览与阅读地图.md](../Data_Governance_with_Unity_Catalog/00-总览与阅读地图.md)、
  [../Apache_Polaris_TDG/00-总览与阅读地图.md](../Apache_Polaris_TDG/00-总览与阅读地图.md)——
  Unity/Polaris 把 catalog 做成独立系统，Fabric 把 catalog 长进湖里；迁移时治理词表不随行 ⚠️。
- 可观测纵深（"跑没跑成"vs"值不值得信"，09 章分工）：
  [../Fundamentals_of_Data_Observability/00-总览与阅读地图.md](../Fundamentals_of_Data_Observability/00-总览与阅读地图.md)、
  [../Data_Observability_for_Data_Engineering/00-总览与阅读地图.md](../Data_Observability_for_Data_Engineering/00-总览与阅读地图.md)。
- 产品全景姊妹册：[../Fundamentals_of_Microsoft_Fabric/00-总览与阅读地图.md](../Fundamentals_of_Microsoft_Fabric/00-总览与阅读地图.md)。
- 本册闭环：10 章回收 02（同湖前提）、05（ADF 血缘汇流）、07（留存）、08（同池互噬）的
  治理伏笔——全书终章即"账本清零章" ⚠️。
- 波内登记（不链）：#218 入门册（治理浅位）、#219 Synapse 迁移册（旧治理面谱系）、
  #220 食谱册（策略逐场景配方）；Fabric 同波诸册互链义务见 00 §8。

## 核心概念速览（中英对照）

- **目录即湖面** — Catalog-as-Lake-Surface：OneLake Catalog 是元数据主入口，发现/治理/
  容量三页皆其投影 ✅⚠️。
- **血缘汇流** — Lineage Confluence：表维护、同步任务、管道段汇入 item 级血缘 ✅页/⚠️细节。
- **标签双轨** — Two-Track Classification：自定义 tag（轻）与敏感度标签（Purview 重炮）
  成本与约束力不同级 ✅实抓/⚠️。
- **认可位** — Endorsement：certify/promote 把"可信"制度化，人是流程的门 ⚠️✅。
- **一图四用** — Workspace as Boundary：权限/git/监控/部署共用工作区边界，设计当架构做 ⚠️。
- **两段式 ALM** — Sync + Deploy：仓库同步与环境推进分立；覆盖清单当日页为准 ⚠️✅页名。
- **仓库格式税** — Item-Format Tax：平台自定义 item 文件夹格式，diff/评审体验非裸代码 ⚠️。
- **治理即元数据面** — Governance-as-Metadata：单湖前提换内置治理，导出即失效 ⚠️。
- **监控中心** — Monitoring Hub：容量/作业/告警统一运维台（✅ 页名族实抓）。
- **容量互噬** — CU Contention：ETL 与交互同池争抢，阈值告警+时段隔离自保 ⚠️。

## 最新演进与工业实践

2024→2026（取证 2026-10-02；台账 00 §9 + dir_*.json 实抓清单）：

- **治理文档面急剧膨胀**：governance 域清单实抓 50+ 页（标签继承、DLP 三步、保护策略、
  metadata-scanning 自动化 `metadata-scanning-overview/run` ✅），2024 出版时的"治理一章"
  已长成平台级子系统 ⚠️——本册以支柱表（10.1）消化，拒绝逐页转述。
- **hub 页叙事迁移**：`/fabric/governance/overview` 实测 404（00 §9 禁引清单），现行入口
  =`onelake-catalog-overview`+`governance-compliance-overview` 双页——引 2024 二手博客必踩坑。
- **ALM 全家桶化**：git 同步页族从 notebook 扩到 eventstream/kql queryset/eventhouse
  （✅ 实抓）——实时件也进仓库轨道，10.4 的"作业即代码"边界持续外推。
- **工业实践画像** ⚠️（通识）：成熟租户收敛为"标签先行（默认标签策略）+ 部署管道带审批、
  热修复零旁路 + 容量告警日历化"；常见失败模式=lineage 追不上手工临时表，孤儿 item 沉积
  （10.6 巡检第 6 条的存在理由）。
- **取证缺口再提醒（波尾人工项）**：本册作者（Chris Teon 推定）与实版印刷 ISBN 在取证日
  仍未定谳（00 §2/§4 全案）；治理/监控面的机制细节大量停在"✅ 页名实抓、⚠️ 内容未逐页
  转述"层——后续持书勘误时优先回填 10.2/10.4 两节。
