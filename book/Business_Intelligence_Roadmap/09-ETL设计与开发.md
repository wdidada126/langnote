# 09 ETL 设计与开发 — Extract/Transform/Load Design & Development（原书 Step 9 + Step 11）

> 章题与小节题 ✅ 取自 InformIT 官方目录页；本文件合并「ETL 设计（Step 9）」与「ETL 开发（Step 11）」
> （二者同一数据轨道的设计/实现两面）。ETL 是 BI 项目**工作量最大、最易超支**的一步。🔧 E2 为本机 DuckDB
> 演示，**非本书引擎/平台行为**。

## 9.1 三种装载：初始·历史·增量

✅ 官方小节「The Initial Load / The Historical Load / The Incremental Load」把装载切成三类，各有策略：

- **初始装载（Initial）**：首次建库灌入当前值快照——一次性、量大、可停机窗口执行。
- **历史装载（Historical）**：把历史数据回填以支撑趋势分析——分批复跑，须可**幂等**（重复跑不翻倍）。
- **增量装载（Incremental）**：日常只处理变化部分——BI 仓库上线后的常态，**最难做对**（变更捕获、水位、迟到数据）。

🔧 **实验 E2（DuckDB 幂等装载，非本书引擎行为）**：目标表 `tgt(k PK, v, upd)` 先初始装 1000 行（Σv=4,995,000）；
对一个含 500 新键 + 300 更新键的暂存批次用 `MERGE ... WHEN MATCHED UPDATE / WHEN NOT MATCHED INSERT`：
合并后 **1300 行、Σv=8,968,250、500 行被更新**；**重跑同一批次结果逐字节相同**（幂等）。对照朴素 `INSERT`
复跑同批 → **1800 行、仅 1300 个 distinct 键（500 重复爆炸）**。这就是「增量/历史装载必须幂等」的实证：
`MERGE/upsert` 是防重复的关键，朴素追加会破坏主键语义。脚本 `D:\develops\tmp\dbwave_w9_birmap\exp.py`。

## 9.2 抽取程序（Designing the Extract Programs）

✅：从源系统取数的设计——抽取方式（全量 vs 增量：时间戳/触发器/日志 CDC/快照比对）、抽取频率、
源系统负载隔离（勿在业务高峰直查生产库，常走只读副本）。源质量差（见 05 章 E4）在此放大成本。

## 9.3 转换程序（Designing the Transformation Programs）

✅ 官方小节「Source Data Problems / Data Transformations」：

- **源数据问题**：脏值、编码不一、缺失、重复、口径冲突——对应 Step 5 清洗规则。
- **数据转换**：清洗、标准化、码值映射、派生列、维度代理键生成、缓慢变化维（SCD）处理。转换规则以
  **《源到目标映射文档》**为唯一依据（下节）。

## 9.4 装载程序与过程流

✅ 官方小节「Designing the Load Programs / Referential Integrity / Indexing / Designing the ETL Process Flow /
The Source-to-Target Mapping Document / The ETL Process Flow Diagram / The Staging Area / Evaluating ETL Tools」：

- **装载 + 引用完整性 + 索引**：装载顺序须先维后事实以保外键；批量装载时常**先删索引、装完重建**（呼应
  08 章 E5：索引对装载是写放大成本）。
- **源到目标映射文档（STM）**：字段级映射 + 转换规则的**契约**，是 ETL 开发与验收的基准。
- **ETL 过程流图**：作业依赖 DAG；**暂存区（Staging Area）** 作为源与目标间缓冲区（Bronze 前身）。
- **评估 ETL 工具**：给出选型准则（连接性、转换能力、元数据交换、并行、运维）。
- **实现策略（Implementation Strategies / Preparing for the ETL Process）**：大爆炸 vs 渐进分域。

## 9.5 Step 11·ETL 开发

Step 11 是 Step 9 设计的**执行**：编码/配置 ETL 作业、单元与集成测试、对账（装载行数/校验和，如 E2 的 Σv）、
异常处理与重跑机制、并行调试。交付物为**可运行的 ETL 作业集 + 对账报告**。不做的风险：设计与实现脱节，
映射文档形同虚设，数据静默错漏。

## 9.6 活动·交付物·角色·不做之风险（两步并记）

- **交付物**：Step 9——STM 文档、过程流图、暂存区/装载顺序设计、工具选型；Step 11——可运行 ETL 作业、
  对账报告、重跑/异常机制。
- **角色**：ETL 工程师（核心团队）主做，DBA 保装载效率，元数据管理员登记操作元数据（07 章），SME 验口径。
- **不做的风险**：无 STM→口径随工程师理解漂移；非幂等装载→重复/漏数（E2 反例）；无对账→错误静默。

## 9.7 与 repo 其他书的联系

- **提取与哈希**：Data Vault 的 ETL 提取/哈希/装载专章——[../Data_Vault_2_0/11-数据提取与哈希.md](../Data_Vault_2_0/11-数据提取与哈希.md)、
  [../Data_Vault_2_0/12-装载DataVault.md](../Data_Vault_2_0/12-装载DataVault.md)。
- **集市装载**：[../Data_Vault_2_0/14-装载维度信息集市.md](../Data_Vault_2_0/14-装载维度信息集市.md)。
- **清洗上游**：转换规则源自 [05](05-数据分析与逻辑建模.md) 章；物理装载呼应 [08](08-数据库设计.md) 章 E5。
- **元数据下游**：装载即回写操作元数据 → [07](07-元数据仓库分析与设计.md) 章。波内兄弟 #142/#205：**只登记不链**。

## 9.8 原书口径 → 2026 话语对位（⚠️ 转述级）

| 本步术语 | 2026 常见对位 | 一句话差释义 |
| --- | --- | --- |
| 初始/历史/增量装载 | 全量 / 回填 / 增量微批+流 | 思想一致、频率更细 |
| 幂等装载 | MERGE upsert / 增量物化视图 | 🔧 E2 已成引擎原语 |
| 暂存区 Staging | Bronze 层 | 缓冲区升格为归档底座 |
| 转换程序 | dbt SQL 模型（ELT） | 引擎外→引擎内 |
| 源到目标映射 STM | 声明式模型 + 自动血缘 | 文档→代码 |
| 抽取 / CDC | 日志 CDC + 托管连接器 | 手工→生态化 |
| 装载对账 | 数据可观测性 | 静态核对→持续监控 |

## 9.9 阅读自测（附答案要点 ⚠️ 编者）

- **问：🔧 E2 的数字说明了什么？** 答：初载 1000（Σ=4,995,000）→ 合并后 1300（Σ=8,968,250、更新 500）且重跑**幂等**；朴素 INSERT 复跑则 1800 行/1300 distinct（500 重复爆炸）。
- **问：增量装载为何最难？** 答：变更捕获、水位管理、迟到数据三者叠加。
- **问：装载顺序为何先维后事实？** 答：保证事实表外键（引用完整性）。
- **问：批量装载为何常先删索引？** 答：减少写放大——呼应 🔧 E5 索引成本、08 章。
- **问：没有 STM 文档的风险？** 答：转换口径随工程师各自理解而漂移、验收无据。

## 9.10 步骤握手与本步边界（⚠️ 编者综合）

- **输入 ←**：Step 5 转换/清洗规则 + Step 8 目标库结构（STM 映射的唯一依据）。
- **输出 →**：可运行 ETL 作业 + 操作元数据（→ Step 7 目录、→ Step 12 应用供数）。
- **回写 ⟲**：每次装载刷新血缘/运行元数据，使元数据仓库不腐化（→ 07/10 章）。
- **边界**：设计（Step 9）与实现（Step 11）同轨；本文件不覆盖应用层展示（Step 12）。

## 9.11 一页速记（口诀）

- 一句话：**ETL 是 BI 里最大、最易超支、最该谈幂等的一步**。
- 三种装载：初始/历史/增量，增量最难（变更捕获+水位+迟到）。
- 🔧 E2 铁律：装载必须幂等，朴素追加=重复爆炸。

## 核心概念速览（中英对照）

- **初始 / 历史 / 增量装载** — Initial / Historical / Incremental Load：首灌快照 / 回填趋势 / 日常变更。
- **幂等装载** — Idempotent Load：重跑不翻倍（E2：MERGE 幂等 vs 朴素 INSERT 重复爆炸）。
- **抽取** — Extract：全量或增量取数（时间戳/CDC/快照比对），隔离源负载。
- **转换** — Transform：清洗/标准化/码映射/代理键/SCD。
- **源到目标映射文档** — Source-to-Target Mapping（STM）：字段级映射与规则的契约。
- **ETL 过程流图** — ETL Process Flow：作业依赖 DAG。
- **暂存区** — Staging Area：源与目标间缓冲（Bronze 层前身）。
- **先删后建索引** — Drop-Rebuild Indexing：批量装载减少写放大（呼应 08 章）。
- **对账** — Reconciliation：行数/校验和核对（如 E2 的 Σv）。
- **实现策略** — Implementation Strategies：大爆炸 vs 渐进分域。

## 最新演进与工业实践

2002→2026 对位（官方源 ⚠️ 转述 + URL 于 2026-10-02 验 200 ✅）：

- **ETL → ELT + 仓内转换**：抽取即落地、转换在引擎内做（dbt SQL 模型），「暂存区」升格为 **Bronze 层**、
  转换层即 **Silver**（对位 [../Analytics_Engineering_with_SQL_and_dbt/00-总览与阅读地图.md](../Analytics_Engineering_with_SQL_and_dbt/00-总览与阅读地图.md)）。
- **幂等 upsert → MERGE 原语 + 增量模型**：🔧 E2 的 `MERGE` 已成云仓/湖仓标配；**增量物化视图 / 微批** 把
  增量装载自动化（⚠️ `https://docs.databricks.com/aws/en/lakehouse/` ✅ 200）。
- **STM 文档 → 声明式模型 + 血缘**：字段映射内嵌在 dbt 模型里，血缘由运行期自动生成回元数据仓库（⚠️
  `https://docs.getdbt.com/docs/build/semantic-models` ✅ 200；对位 07 章 [../The_Enterprise_Data_Catalog_2e/00-总览与阅读地图.md](../The_Enterprise_Data_Catalog_2e/00-总览与阅读地图.md)）。
- **ETL 工具评估 → 采集生态（CDC/连接器）**：Debezium 式日志 CDC + 托管连接器替代传统抽取程序（联邦面
  ⚠️ `https://trino.io/docs/current/` ✅ 200）。
- **对账 → 数据可观测性**：行数/校验和的静态对账升级为**持续监控**（新鲜度/卷量/分布/schema 漂移）+ DataOps CI。
- **工业实践**：现代数据团队把本书「设计→实现→对账」固化为 **DataOps 流水线**：STM=模型契约、装载=带测试的
  dbt run、异常=自动告警与幂等重跑，正是 Step 9→11 的自动化终态。
