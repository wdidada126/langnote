# 02 开始使用 Amazon Redshift（Chapter 2: Getting Started with Amazon Redshift ⚠️ 英题推定）

> 精读重构笔记，非原书文本。Redshift 不可本机实测：架构/计费描述一律 ⚠️ 转述 + 官方文档 ✅ URL（URL 均经本机 curl 状态码核验，2026-09）。

## 1. 本章骨架（✅ 译文实抓）

- 2.1 Amazon Redshift 架构概述
- 2.2 开始使用 Amazon Redshift 无服务器（创建 Serverless 数仓）
- 2.3 示例数据（激活示例数据模型 + 查询编辑器查询）
- 2.4 何时使用预置集群？（创建预置集群）
- 2.5 估算成本：托管存储 / Serverless 计算（基本容量 RPU、高/频繁使用）/ 预留计算
- 2.6 AWS 账户管理（ Organizations 口径 ⚠️ 转述）
- 2.7 连接：私有/公有 VPC 与安全访问、密码存储、临时凭证、联合用户、SAML/本地 IdP、Data API、查询编辑器 V2（三种登录态）、QuickSight BI、JDBC/ODBC
- 2.8 总结

## 2. 架构概述（⚠️ 转述，全书技术底座）

Redshift = **MPP（massively parallel processing）列存数仓**，源于 ParAccel 授权（2012 发布，⚠️ 史实转述）：
- 经典拓扑：**1 leader 节点（编译/分发计划，不存用户数据）+ N compute 节点（存储+执行）**；
- 表按 **DISTSTYLE** 切片到 compute 节点，块粒度 1MB、**无索引、靠区域映射（min/max）**定位（Ch3/Ch5 展开）；
- 演进三段：DS2 → DC2（本地 NVMe，dense compute）→ **RA3**（本地热层 RMS + 云端 managed storage 冷层，存储计算解耦）→ **Serverless**（连集群概念都收掉：namespace + workgroup + RPU 容量，基础默认 8 RPU/可 5–512 ⚠️ 数字以官方页为准）。
- RA3 定价表"截至 2023"（ra3.large/xl/16xl/48xl/lustre-48xl 的 RMS/vCPU 配比，✅ 译文表 2-1 实抓 ⚠️ 数值细节未回核英文）。

对比记忆锚（对位表见 00 §4）：Snowflake 把"集群"抽象成虚拟仓库（[../Snowflake_The_Definitive_Guide/02-架构与虚拟仓库.md](../Snowflake_The_Definitive_Guide/02-架构与虚拟仓库.md)）；Redshift 抽象得更慢一步——预置集群概念保留至今，Serverless 是新腿。

## 3. Serverless vs 预置：本书决策口径（⚠️ 转述）

- Serverless 适合：波动负载、新建仓库、不想管节点/参数组；按 RPU-秒计费 + 托管存储 GB；
- 预置适合：稳定大负载 + 预留实例折扣、需要节点级定制（如 lustre 缓存盘）、既有 DC2 迁移缓冲；
- 书中给出 RPU 单价换算例（8 RPU 基准下 $/hour 数量级演算 ✅ 译文实抓，现价 ⚠️ 以 price list 为准）；
- 高/频繁使用两个成本小节的要点：**base 容量常开贵**，善用 autoscaling 上限与 workgroup 暂停。

## 4. 连接与认证全景（本章另一半篇幅，⚠️ 转述归纳）

| 路径 | 凭证形态 | 备注 |
|---|---|---|
| 查询编辑器 V2 | 浏览器直连（会话/临时凭证/db 用户） | 免装客户端，带 SAML 支持 |
| Data API | HTTPS + Secrets Manager/IAM | Serverless 友好，无驱动 |
| JDBC/ODBC | db user 或 **temp credentials（GetClusterCredentials）** |  BI 工具标配 |
| 联合身份 | IAM → SAML 断言（IdP/本地 IdP） | 企业 SSO 主线 |
| 网络 | VPC 私有子网 + ENI/安全组；Public access 开关 | ⚠️ 网络细节转述 |

🔧 类比（**非 Redshift 行为**）：本机 DuckDB 1.5.5 演示"临时凭证≠库权限"的概念分层——DuckDB 进程内 `ATTACH ':memory:'` 任意名用户都能建库，而 Redshift 是 IAM（云侧门卡）→ db user（库内户口）→ GRANT（对象钥匙）三层串联；类比止步于"身份与会话解耦"这一点（Ch8 继续）。

## 5. 示例数据主线开场（✅ 译文实抓）

本章起全书复用**学生信息学习分析数据集**（edtech AaaS 商案例）：激活 AWS 示例数据库→查询编辑器 V2 跑首批 SQL→Ch3 拿它建模、Ch6 拿它训练、Ch7 拿它共享。TDG 惯用"一书一案例"手法。

## 6. 成本小节的可迁移心智（⚠️ 转述）

- 托管存储计费与 Spectrum 查询量是两条正交曲线（湖上扫描另收，Ch4）；
- 预留（RI）锁 1/3 年换折扣，Serverless 无 RI——**弹性与折扣不可兼得**是 2023-2026 云仓共同格局；
- 与 Snowflake credits 心智差异：Redshift 账单可拆到"RPU×时长×workgroup"，FinOps 归因粒度更细（⚠️ 转述两家定价页）。对位：[../Snowflake_The_Definitive_Guide/08-账户成本管理.md](../Snowflake_The_Definitive_Guide/08-账户成本管理.md)。

## 7. 疑点与缺口

- RA3/Spectrum 计费单价 2026 已多轮调价，正文数字仅作 2023-2024 快照 ⚠️；
- 查询编辑器 V2 与 Snowsight 的功能差集（版本管理/计划器可视化）未逐条回核英文原文 ⚠️；
- 官方文档旧页（如 c_high_level_architecture.html）实测 302→根：AWS 2025-2026 文档改版，本册仅引仍 200 的页面（✅ curl 取证）。

## 8. Serverless 对象模型速记卡（⚠️ 转述归纳）

| 对象 | 类比预置世界 | 作用 |
|---|---|---|
| namespace | 集群的"库+权限"壳 | 定义数据库、用户、datashare 身份边界 |
| workgroup | 集群本体（算力入口） | 绑 subnet/security group、定 base/上限 RPU、挂参数组 |
| base capacity | min 节点数 | 常开成本主体；闲置可按策略自动暂停 ⚠️ |
| autoscaling 上限 | 弹性 max | 高峰自动加 RPU 到此封顶 |
| 示例数据库 | sample data | 本书学生数据集入口（✅ 2.3 实抓） |

预置世界对象对照：cluster/parameter group/子网组/security group 仍在（✅ 2.4 小节实抓）；两世界的参数组与 WLM 差异见 Ch5。

## 9. 动手清单复述（⚠️ 转述控制台路径，不含任何本机可跑含义）

1. 建 namespace → 建 workgroup（VPC 私有子网 + 安全组放行入站端口 5439 ⚠️ 默认端口转述）；
2. 激活示例数据 → 查询编辑器 V2 用临时凭证登录 → 跑通首条 SELECT；
3. 建 db user + 组，配 IAM DB 认证或 Secrets Manager 托管；
4. QuickSight 连接 warehouse → 首图；
5. 读账单页：RPU-小时 × base+autoscale 曲线、托管存储 GB、Spectrum 扫描 GB 三条目各自归因。

## 10. 选型速答（⚠️ 本书口径转述）

- Q：新项目？——Serverless 起步（免管节点/参数），除非有确定性大负载+RI 折扣需求；
- Q：已有 DC2 大集群？——评估 RA3 迁移（Ch9 路径），不要原地续命太久：托管存储/并发扩展红利都绑在 RA3+ 上（⚠️ 转述）；
- Q：连接方式选择？——浏览器 V2 做探索，JDBC/ODBC 给 BI 工具，Data API 给无服务器函数，temp credentials 给自动化脚本（Ch8 治理其风险面）。

## 10b. 首日语故障速查（⚠️ 归纳帮读，非原文）

- 连不上：安全组入站/公网访问开关 → 子网路由 → 名称解析（DNS 伏笔，Ch9 亦提）；
- 连上被拒：db user 不存在 vs IAM 映射缺失——两条认证链分开排；
- V2 登进但无库：示例数据未激活 / namespace 选错（Serverless 双身份心智）；
- SELECT 报权限：新集群 public schema 宽松度问题 ⚠️，Ch8 收口；
- 首查慢：冷缓存+统计未建，RA3 从托管存储拉数据属正常（⚠️ 转述）。

- 对位阅读：Snowflake 同题章节 [../Snowflake_The_Definitive_Guide/02-架构与虚拟仓库.md](../Snowflake_The_Definitive_Guide/02-架构与虚拟仓库.md)、[../Snowflake_The_Definitive_Guide/01-开始上手.md](../Snowflake_The_Definitive_Guide/01-开始上手.md)；开源 MPP 观感校准用 [../DuckDB_in_Action/03-执行SQL查询.md](../DuckDB_in_Action/03-执行SQL查询.md)（单机列存执行剖面，🔧 可跑）。
- 端口与网络备忘（⚠️ 转述）：Redshift 默认监听 5439（PG 系 5432 的变体），入站规则、VPC 端点（PrivateLink）、代理出口三类网络形态在书中各给一段——本章"连接"小节真正的厚度在网络侧而非驱动侧；
- 计费演算方法可迁移：书中"8 RPU=$0.001/秒级"换算例（✅ 译文实抓）示范的是**把 RPU 单价折到查询成本**的 FinOps 基本功，换任何云仓都成立（对位 credits/slot 单价折算）；
- 阅读提醒：2.1 架构概述只给"leader+compute"骨架，RA3 的 managed storage 细节散见 Ch2/Ch5——初读建议在 §2 卡片处做全书汇总笔记，二读再拆。

## 核心概念速览（中英对照）

- MPP — massively parallel processing：多机并行扫描/聚合的数仓执行范式
- leader 节点 — leader node：编译计划并分发，不存用户表数据（⚠️ 转述）
- 计算节点 — compute node：存切片并执行 fragment 的工作进程宿主
- RA3 节点 — RA3 node：本地 RMS 热层 + managed storage 冷层的解耦机型
- DC2 — dense compute 2：全本地盘机型，稳定大负载仍可用
- 托管存储 — managed storage：RA3/Serverless 的 S3 系底层存储层（⚠️ 实现转述）
- Serverless workgroup/namespace — 工作群/命名空间：算力入口与库身份解耦的两个对象
- RPU — Redshift Processing Unit：Serverless 计量单位（约等于一份固定算力）
- 预留实例 — reserved instance：预置集群的 1/3 年期折扣契约
- 临时凭证 — temporary credentials：GetClusterCredentials/GetCredentialsForDatabase 换短时 db 会话
- 联合身份 — federated/IAM DB auth：IAM/SAML 直通库内用户，免密管理
- Data API — 数据 API：HTTPS 型 SQL 执行接口，Lambda/无驱动场景
- 查询编辑器 V2 — query editor V2：浏览器端 SQL IDE（对位 Snowsight）
- VPC/ENI — 私有网络挂载点：仓库落 VPC，安全组管进出（⚠️ 转述）
- Secrets Manager 集成 — 托管口令轮换：db 密码出库入 KMS 域，自动化脚本标配（⚠️ 转述）
- 基础容量 — base capacity：workgroup 常开 RPU 下限，成本主体（§8 卡）
- 示例数据集 — sample data：激活即得学生数据集入口（✅ 2.3 实抓）
- 自动暂停/恢复 — auto suspend & resume：闲置挂起换成本，恢复延迟换首查（§8 卡 ⚠️）

## 最新演进与工业实践

- Serverless 现状（2026）：GA（2022-07）后已成 AWS 默认推荐形态；RPU 范围扩容、自动暂停恢复、跨区湖查询等持续加码（⚠️ 转述自 AWS 公开文档线；✅ 概念页 https://docs.aws.amazon.com/redshift/latest/mgmt/serverless-whatis.html curl 200；容量语义见 https://docs.aws.amazon.com/redshift/latest/mgmt/serverless-capacity.html curl 200）。
- 认证侧演进：IAM DB 认证与 Secrets Manager 托管轮换成为合规基线；SSO 全链路（Identity Center→workgroup）2024+ 文档重写（⚠️ 转述）。
- 工业实践：新仓库默认 Serverless + 每部门一 workgroup 做成本归因；存量 DC2 走 RA3 迁移（快照恢复）仍是 2024-2025 常见项目（⚠️ 社区经验转述，无一手数字）。
- 对位阅读：Snowflake 同题章节 [../Snowflake_The_Definitive_Guide/02-架构与虚拟仓库.md](../Snowflake_The_Definitive_Guide/02-架构与虚拟仓库.md)、[../Snowflake_The_Definitive_Guide/01-开始上手.md](../Snowflake_The_Definitive_Guide/01-开始上手.md)；开源 MPP 观感校准用 [../DuckDB_in_Action/03-执行SQL查询.md](../DuckDB_in_Action/03-执行SQL查询.md)（单机列存执行剖面，🔧 可跑）。
