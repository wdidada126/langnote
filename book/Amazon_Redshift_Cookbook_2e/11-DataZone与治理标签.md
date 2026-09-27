# 11 DataZone 与治理标签（2e Ch11）

> 取证强度：✅ 强（官方 2E 仓 Chapter11 实抓：`datazone_domain_CFN.yaml`（DataZone 域栈）、`SampleCustomContext.json`（自定义上下文样例）、`sales_data.sql`（业务演示数据）、`chapter_11_CFN.yaml`）。章题为主题命名（⚠️ 官方章题未获，00 §2-6），但"DataZone+自定义上下文"两件代码把治理章身份钉死（✅）。
> 三态：✅ URL/命令实证｜⚠️ 转述推定｜🔧 类比（**非 Redshift 行为，方言已按 DuckDB 改写**）。

## 1. 本章定位

数据进仓（3/4）、动起来（5）、算得快（7/8）、分得出去（9/10）之后，2e 新增的重头：**治理产品化**。Amazon DataZone=企业级数据集市（域 domain/项目/目录/订阅），把"数据产品"从口号落成工作流；**自定义上下文（custom contexts）**=目录上的自定义标签维度（业务术语/数据所有者/敏感级），让发现与治理贴业务语言（⚠️ 概念转述+✅ 文件对应）。

## 2. 配方地图

| 配方 | 机制 | 取证 |
|---|---|---|
| 起域 | DataZone domain CFN（域+团队+数据项目） | ✅ yaml 实抓；语义 ⚠️ |
| 资产上架 | 订阅 Redshift datashare/Glue 表为"数据产品"进目录 | ⚠️ 转述（与 ch9/10 汇流；✅ 盘上 TDG 07 含 DataZone 段） |
| 自定义上下文 | `SampleCustomContext.json` 定义的标签树经 API/控制台注入目录 | ✅ JSON 文件实抓；API 细节 ⚠️ |
| 业务数据演示 | sales_data.sql：建 schema/插销售域样本，供目录检索与授权演练 | ✅ 文件名+SQL 形态实抓 |
| 治理闭环 | 发现→理解→订阅→审计（DataZone 生命周期） | ⚠️ 转述 |

## 3. 深潜一：DataZone 在治理栈里的位置（⚠️ 转述+✅ 盘上互证）

- 下层的 LF（→10）管"能不能读"，上层 DataZone 管"该不该给你、以什么产品名义、留什么审计"；中间 Glue Catalog 是技术元数据总线；
- DataZone 是 AWS 对 **data mesh**（域所有权、数据即产品、自助平台、联邦治理）的产品化应答——四原则逐条映射：domain=领域所有权；订阅工作流=数据即产品交付面；脚手架项目=自助平台；治理关卡=联邦治理（⚠️ 架构学对照，全篇理论出处 ✅ 盘上 [../Data_Mesh/02-领域所有权原则.md](../Data_Mesh/02-领域所有权原则.md)–05 三原则章）；
- 与第三方目录（Collibra/Atlas 谱系）的关系：DataZone=云服务内闭环目录，2024 语境主打"原生零集成成本"（⚠️）。

## 4. 深潜二：自定义上下文的两副面孔（✅ 文件+⚠️ 语义）

1. **分类面**：给资产挂业务分类（客户域/财务域/…），检索与浏览按上下文聚合——`SampleCustomContext.json` 即此树形定义样例（✅ 文件名与 JSON 语义）；
2. **策略面**：治理动作（审批链/保留期）可绑定上下文而非裸对象——上下文=策略的锚点（⚠️ 转述，具体规则能力以官方页为准）；
3. 反模式警告：标签爆炸（人人建维度）与"有标签无消费者"（不接审批/检索）是目录治理的两大死法（⚠️ 工程惯例）。

## 5. 🔧 类比：给表挂"业务标签树"并强制拦截（本机真实跑过）

DuckDB 1.5.5 无标签子系统——类比降级为**标签关联表+SQL 关卡**演示（custom_context_demo.py，输出 custom_context_demo_out.txt，存 tmp/dbwave_w5_rscb/；**非 Redshift 行为，方言已按 DuckDB 改写**）：`asset_tag(object_id, context, value)` 承载标签树（owner/sensitivity/steward 三上下文共 29 行，含批量打标 20 对象）；"注册关卡"=`INSERT INTO registry SELECT ? WHERE EXISTS(该对象有 owner 标签)`——对 3 个候选对象仅放行 1 个（`sales.orders` 有 owner 标签入册，`ods.ssn`/`tmp.load_1` 无 owner 被拦，registry 终值 1 行）；按 `context='sensitivity' AND value='PII'` 反查命中 5 对象。抽象迁移：**"上下文=一等元数据+策略锚点"在最小实现里就是一张带 EXISTS 约束的关联表**，DataZone 只是把它做成了带 UI 与审批链的服务（⚠️ 真产品语义以官方文档为凭；本例诚实登记：未做真触发器，拦截发生在写入语句的 WHERE 而非引擎强制）。

## 6. 常见坑与最佳实践（⚠️ 转述+✅ 锚）

1. 域拓扑=组织设计：按数据域而非 IT 层建域，照抄部门树必返工（⚠️→Data Mesh 原则一）；
2. 上架前先定 SLA/所有权/脱敏层（→10 视图脱敏；✅ 盘上 TDG 08 DDM 段），"裸表上架"是治理债的复利机器；
3. 自定义上下文先窄后宽：起步 ≤5 个维度，每季度按使用率退役零命中维度（⚠️）；
4. DataZone 授权与 LF/仓内 RBAC 三张皮：审批通过但 LF 忘配=经典 403 排障链（→10 §6-1）；
5. 目录审计留痕（谁订阅了什么）接入 CloudWatch——合规问询时目录即证据（⚠️；✅ https://docs.aws.amazon.com/redshift/latest/mgmt/db-auditing.html 同址 200 的仓内一侧）。

## 7. 系列互链

- 架构学总仓：[../Data_Mesh/00-总览与阅读地图.md](../Data_Mesh/00-总览与阅读地图.md)（四原则与本章一一对位）、逻辑架构卷 [../Data_Mesh/07-逻辑架构.md](../Data_Mesh/07-逻辑架构.md)；
- 概念版 AWS 面：[../Amazon_Redshift_TDG/07-数据共享的合作.md](../Amazon_Redshift_TDG/07-数据共享的合作.md)（DataZone 段）；
- 目录工程通识（谱系/采集/血缘）：[../The_Enterprise_Data_Catalog_2e/00-总览与阅读地图.md](../The_Enterprise_Data_Catalog_2e/00-总览与阅读地图.md)；
- SF 治理对照：[../Advanced_Snowflake/10-治理与安全进阶.md](../Advanced_Snowflake/10-治理与安全进阶.md)。

## 核心概念速览（中英对照）

- 域 — domain：DataZone 的治理与成员边界单元
- 数据项目 — data project：域内的资产与权限工作组
- 资产/目录 — asset/catalog：上架的数据产品条目
- 订阅 — subscription：消费者申请→审批→获权的交付流
- 自定义上下文 — custom contexts：目录树之上的业务标签维度（本章 ✅ 文件主角）
- 数据产品 — data product：含 SLA/所有权/接口的可交付数据单元
- 联邦治理 — federated governance：域自治+全局策略的折中（mesh 原则四）
- 数据即产品 — data as a product：mesh 原则二在 DataZone 的工作流化
- 标签爆炸 — taxonomy sprawl：无治理的元数据反模式
- 三张皮 — RBAC/LF/DataZone：权限三层脱节的排障高发区
- 治理关卡 — governance gate：订阅链上的审批点
- 上架 — publish/asset curation：资产进目录的完整动作

## 最新演进与工业实践

- **DataZone 主站叙事更迭（2024→2026）**：AWS 目录/治理面在 2025+ 持续重组（统一目录类新服务上位、DataZone 功能线滚动调整），本章代码为 2024 快照，读者落地前以 aws 主站现状复核（⚠️ 转述；✅ https://aws.amazon.com/redshift/ 200 实测 2026-09-28，DataZone/docs 专页本册未逐一取锚——诚实登记缺口，不引 302/未知页）。
- **上下文→AI 元数据**：业务标签树喂给自然语言问数/生成 SQL 的检索层，是 2025+ 目录工程与 LLM 汇流的主战场（⚠️ 转述；对照盘上目录册 [../The_Enterprise_Data_Catalog_2e/00-总览与阅读地图.md](../The_Enterprise_Data_Catalog_2e/00-总览与阅读地图.md) 的主动元数据线）。
- **工业实践**：中小团队 2026 常以"Glue Catalog+标签+仓内 RBAC"平替 DataZone 全家桶——先跑通再平台化（⚠️ 转述）；治理即代码（标签/策略进 git）与本章 CFN 精神同构（✅ 文件形态）。
- **取证提醒**：本章为 2e 全新章（1e 无对应 ✅ 00 §5 表）——读它是读"Packt 眼中 2024 治理答案"，时效敏感。
