# 09 MPP 平台迁移到 Synapse — MPP Platform Migration to Synapse（原书第 9 章）

> 章题 ✅ Packt 官方 ColorImages PDF 文本层实抓；**官方仓库无 chapter 9 代码文件夹**
> （✅ 仓库树实查，登记缺口）——配方级小节 ⚠️ 按章题语义 + Learn 迁移文档域 + README
> 软件清单点名 **Azure Synapse Pathway**（✅ 实抓）组织。机制 = Learn 转述 ⚠️ + ✅ URL
> （2026-10-02 `curl -sI` 200）；Azure 不可实测 ⚠️；🔧 引用全册实验做类比，**非平台行为**。

## 9.1 迁移对象：同业 MPP 数仓群

✅ `azure/synapse-analytics/migration-guides/migrate-to-synapse-analytics-guide` ⚠️ 转述：
官方迁移指南按源平台分线——**Teradata / Netezza / Oracle**（各线三步：设计性能→
ETL 装载→安全访问，✅ 三线的 `1-design-performance-migration` 页均 200 验真），加上
SQL Server 系（专用池本家方言最近）。章题「MPP Platform」即指这类对等架构迁移：
分布表→分布表、存储过程→存储过程，**不是**异构重写。

| 源 | 概念对位（⚠️ 转述迁移指南） | 已验 ✅ 页 |
| --- | --- | --- |
| Teradata | 主值索引/PI 分布 ↔ HASH 分布键；AMP 并行 ↔ 分布切片 | teradata/1-design-performance-migration |
| Netezza | 表空间/哈希分布 ↔ 分布+分区；SLED 一体机 ↔ 弹性 DWU | netezza/1-design-performance-migration |
| Oracle | 分区/并行查询选项 ↔ 分区+资源类；PL/SQL ↔ T-SQL 方言差 | oracle/1-design-performance-migration |
| SQL Server | T-SQL 近亲，方言差最小；列存索引经验可平移 | （总指南覆盖，专页 404 登记） |

## 9.2 迁移流水线：评估→转换→搬迁→验证（⚠️ 重构口径）

1. **资产盘点**：对象/ETL 脚本/BI 报表清单化——治理面先行（08 章衔接 ⚠️）；
2. **语法转换**：**Synapse Pathway**（README 软件清单 ✅ 点名）做源方言→T-SQL/ARM 的
   机器转换（评估+转换报告），人工兜底残差 ⚠️；
3. **数据搬迁**：一次性大批装载走 01 章路径（导出→对象存储→COPY/CTAS），增量水位
   切流走 02 章管道 ⚠️；
4. **双跑验证**：行数/校验和/KPI 三对齐（total gross 型对账脚本——07 章仓库文件呼应 ⚠️）；
5. **性能追平**：按 03 章顺序「分布键→统计→索引→档位」重做布局，**源平台索引/ hint
   不可照搬** ⚠️。
- POC 方法学 ✅ `guidance/proof-of-concept-playbook-dedicated-sql-pool`（官方演练手册）。

## 9.3 方言与语义陷阱清单（⚠️ 编者归纳，对位三线指南）

- 分布语义：源平台「无分布」概念（Oracle 单实例 RAC）→ 必须重做 3.3 三选一决策，
  这是 MPP 迁移**第一课**；🔧E2 的 2.2× 共置红利/惩罚（SQLite 分片实测，非 Synapse）
  即键选错的量级代价；
- 日期/字符串函数族差异（TERADATA 风格 `DATE '...'`、格式化掩码）⚠️；
- 存储过程事务边界与并发限制（专用池事务面 ✅ toc 实抓 `sql/develop-transactions`）⚠️；
- 统计重建：迁移后全表 `UPDATE STATISTICS` 再放流量（03 章 3.5 呼应 ⚠️）。

## 9.4 SQL Server 谱系辨析对位（名册硬义务的正文落点）

专用 SQL 池 = SQL Server 方言 + PDW/APS 血统的云化 MPP（✅
`sql-data-warehouse/sql-data-warehouse-reference-tsql-system-views` 系统视图谱系）。
从 SQL Server 迁来是「换供给不换内核心智」，从第三方 MPP 迁来是「补分布心智」——
本册对盘上 SQL Server 谱系册的三档引用口径：

| 盘上册 | 状态 | 本册引用方式 |
| --- | --- | --- |
| [../Pro_SQL_Server_Internals/00-总览与阅读地图.md](../Pro_SQL_Server_Internals/00-总览与阅读地图.md) | 在盘 ✅ | 实链：索引/分配结构内幕 ↔ 3.4 |
| [../SQL_Server_2008_Internals/00-总览与阅读地图.md](../SQL_Server_2008_Internals/00-总览与阅读地图.md) | 在盘 ✅ | 实链：SQLOS/存储史前史（PDW 同期代） |
| [../SQL_Server_2012_Internals/00-总览与阅读地图.md](../SQL_Server_2012_Internals/00-总览与阅读地图.md) | 在盘 ✅ | 实链：列存索引内幕（CCI 本地原型） |
| [../SQL_Server_2022_Administration_Inside_Out/00-总览与阅读地图.md](../SQL_Server_2022_Administration_Inside_Out/00-总览与阅读地图.md) | 在盘但**降级册**（名册名 `SQL_Server_2022_Inside_Out` 实名不存在；其 00 已实读：号合法、记录查无、章目录 ⚠️ 主题重构、作者不具名） | **辨析登记 + 带 ⚠️ 等级实链**：其 09 章 IQP/调优 ↔ 本册 03；其 04 章备份升级 ↔ 本章迁移叙事 |

**辨析结论**：两册视角互补不重叠——#71 讲「本地实例怎么管」，本册讲「云上配方怎么做」；
概念冲突时以 Learn 文档为最终准绳（本册 53 条 URL 全验 ✅）。

## 9.5 迁移项目检查单（编者归纳 ⚠️）

1. Pathway 转换报告残差率 < 阈值？人工改写清单进版本库？
2. 每张事实表重做过分布键决策（🔧E2 直觉 + Distribution Advisor ✅ `sql/distribution-advisor`）？
3. 双跑对账含边界日期/闰秒/字符集用例？
4. 回退窗口与冻结期公告？
5. 治理/密钥/网络在目标端先就位（08 章）再迁数据？

## 9.6 与 repo 其他章/册的联系

- 迁移目标形态 → [01-数据装载方法选型与落地.md](01-数据装载方法选型与落地.md)、
  [03-多节点最优处理与专用池调优.md](03-多节点最优处理与专用池调优.md)；
- 切流编排 → [02-数据管道与转换编排.md](02-数据管道与转换编排.md)；
- 报表对账 → [07-PB级可视化报表与物化视图.md](07-PB级可视化报表与物化视图.md)；
- 云仓互鉴（跨波实链 ✅ 验名）：[../Amazon_Redshift_TDG/00-总览与阅读地图.md](../Amazon_Redshift_TDG/00-总览与阅读地图.md)（RA3 迁移面）、[../Snowflake_The_Definitive_Guide/00-总览与阅读地图.md](../Snowflake_The_Definitive_Guide/00-总览与阅读地图.md)；
- 湖仓终局视角：[../Practical_Lakehouse_Architecture/00-总览与阅读地图.md](../Practical_Lakehouse_Architecture/00-总览与阅读地图.md)；
- **波内兄弟只登记不链**：#217《Beginning Azure Synapse Analytics》（Apress 2021，Crossref
  章条目实抓旁证在案）——其「数仓→湖仓过渡」叙事与本册 09 章同题异构（入门向 vs 配方向），
  波尾主代理闭双向挂点。

## 9.7 迁移时间线模板（⚠️ 编者归纳，对位 9.2 五段）

| 周次 | 里程碑 | 本章/他章工件 |
| --- | --- | --- |
| W1–2 | 资产盘点+转换评估 | Pathway 报告（9.2 步 2）；目录盘点（08 章） |
| W3–4 | 目标端基线：分布/分区设计评审 | 3.3/3.4 决策单；Distribution Advisor |
| W5–6 | 语法转换+残差人工改写进版本库 | 9.3 陷阱清单逐项销号 |
| W7–8 | 全量搬迁+首装体检 | 01 章 1.8 闭环 + 1.6 体检单 |
| W9–10 | 双跑对账（行数/校验和/KPI） | 9.2 步 4；total gross 型对账（07 章） |
| W11 | 切流+回退窗口值守 | 9.5 项 4/5 |
| W12 | 复盘：性能追平报告+成本核算 | 03 章 3.8 顺序复查；E1 扩展税心智 |

模板用法：每周次挂一条「否决权条件」（如 W9 对账不平即回退），迁移项目从
「勇气驱动」变「闸门驱动」⚠️ 编者归纳。

## 核心概念速览（中英对照）

- **MPP→MPP 迁移** — 对等架构搬迁：分布心智补课为主、方言转换为辅 ⚠️。
- **Synapse Pathway** — 评估+机器转换工具（README 点名 ✅），残差人工兜底 ⚠️。
- **三线迁移指南** — Teradata/Netezza/Oracle 官方分线文档 ⚠️（✅ 三页 200）。
- **双跑对账** — Parallel run validation：行数/校验和/KPI 三级对齐 ⚠️ 编者归纳。
- **分布键重决策** — Redistribute-by-design：源平台无此概念者必做（🔧E2）⚠️。
- **POC 演练手册** — Proof-of-concept playbook：官方方法学 ✅ proof-of-concept-playbook-dedicated-sql-pool。
- **降级册引用纪律** — Evidence-graded citation：#71 带 ⚠️ 等级引用，冲突以 Learn 为准（编者口径）。
- **回退预案** — Rollback window：迁移项目的否决权条款 ⚠️ 编者归纳。

## 最新演进与工业实践

2022→2026（URL 均 ✅ 200；状态 ⚠️ 转述）：

- **迁移终点转向 Fabric**：官方现行主路径是「Synapse 专用池 → Fabric 数据仓库」再迁移
  （✅ `fabric/data-warehouse/migration-synapse-dedicated-sql-pool-warehouse` 专页 200）——
  本册的「入 Synapse」配方与「出 Synapse」通道并存，规划时先定终态 ⚠️；
  原 `sql-data-warehouse-migrate-from-sql-server` 专页 404（缺口登记）。
- **Pathway 面演进**：转换目标扩展（含 Fabric 工件）、评估报告模板化 ⚠️；
  第三方 MPP 下线潮（Netezza 式一体机退坡）让「存量迁移」成为 2024–2026 常态项目型态 ⚠️。
- **工业实践**：迁移项目治理化——资产盘点复用 08 章目录、对账脚本进 CI、双跑窗口写进
  变更管理；「先布局后档位」（03 章 3.8）在迁移语境权重更高，因为源平台经验常诱导
  照搬索引（🔧E1 扩展税提醒：升档不能救坏布局）。
- 🔧 数字口径：本章引用 E2（34.2ms vs 73.8ms）为 SQLite 分片实测，仅证分布决策代价
  量级，**非 Synapse/源平台行为**。
