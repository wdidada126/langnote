# 08 · 语义层：Direct Lake、语义模型与 Copilot（⚠️ 推定章：原书 TOC 未实抓，主题重构见 [00-总览与阅读地图.md](00-总览与阅读地图.md) 第二节）

消费端是"端到端"的终点。本章三件套：**语义模型（定义一次）→ Direct Lake（免导入直读湖）→ Copilot（自然语言前台）**。
官方简介第一条里的 Power BI 血统在这章兑现
（✅ 锚：https://learn.microsoft.com/en-us/fabric/fundamentals/direct-lake-overview 、
https://learn.microsoft.com/en-us/fabric/fundamentals/copilot-fabric-overview ，访问 2026-09-27）。

## 8.1 语义模型：报表界的"单一事实定义"

⚠️ 转述 + ✅ 概念锚：Fabric 的语义模型（semantic model，原"数据集"）承载度量值/DAX/关系，
是报表与 Copilot 的共同底座；一个模型多报表复用 = BI 界的 copy-of-one（与 01 章湖中心公理同构）。

治理含义（09 章挂钩）：语义模型权限 = 业务口径的最终裁决点；
对照 [../Understanding_Data_Governance/04-政策标准与规程.md](../Understanding_Data_Governance/04-政策标准与规程.md) 的"标准落地要执行器"论点。

## 8.2 Direct Lake：三模式谱系中的位置

✅ https://learn.microsoft.com/en-us/fabric/fundamentals/direct-lake-overview （访问 2026-09-27）：
Direct Lake 让报表**直接读取 OneLake 中的表**（Lakehouse/Warehouse 表），免导入、免查询转发。
与 Import（抽数进模型）、DirectQuery（查询打回源）构成三模式。

⚠️ 转述要点：

- 模式按表可混用（mixed mode）；
- 能力边界（源类型/转换支持矩阵）以当日页为准——本目录不复制快速变动的支持列表；
- 历史注脚 ✅：该特性文档由 Power BI 域迁入 Fabric fundamentals 域
  （旧 /power-bi/.../direct-lake 两候选路径 2026-09-27 实测 404，见 00 第七节禁引清单）。

## 8.3 🔧 EXP-5：免导入直读的"量纲直觉"（本机类比，非 Fabric 行为）

DuckDB 1.5.5 直查 8.18 MB Parquet（不建内表），2026-09-27 实测：

- 冷查询 **4.2 ms** / 热查询 **4.7 ms** / 全新连接 **3.9 ms**；
  （Windows OS 缓存把冷热差抹平了——诚实报告：这说明"直读性能"高度依赖缓存层，
  Fabric 的 Direct Lake 同样有自己的内存/缓存优化层 ⚠️。）
- 对照组：若先走 SQLite 导入再查，仅灌入就要 **5,331.7 ms**（EXP-4）。

结论（类比层）：**Direct Lake 的架构赌注 = 把一次性导入成本换成读路径持续优化**；
对高频重复查询，导入型仍可能赢在极致延迟（⚠️ 通识判断，无 Fabric 侧可比数字）。

## 8.4 报表、仪表盘与"数据应用"外延

⚠️ 转述：Report（含 DAX/可视化）、Dashboard、Paginated Report 等消费 item 与工作区/容量模型挂接
（✅ 概念锚 fundamentals/microsoft-fabric-overview 枢纽内枚举 + fundamentals/fabric-terminology 页，访问 2026-09-27）。
**数据应用（data app）** 使 Power BI 外应用可寄宿 Fabric——
对应 Data Mesh 的"数据产品要有消费面"（✅ 概念对照 [../Data_Mesh/10-数据产品设计-提供消费转换.md](../Data_Mesh/10-数据产品设计-提供消费转换.md)）。

## 8.5 Copilot：自然语言是语义模型的"第二 API"

✅ https://learn.microsoft.com/en-us/fabric/fundamentals/copilot-fabric-overview （访问 2026-09-27；旧 developer-center 路径 404）。
⚠️ 转述当日页口径：Copilot 横贯多体验（Notebook、Data Factory、仓库开发、Power BI），
以租户/区域与功能开关为前提；微软明示其输出可能不准确、需人工复核。

设计观点（⚠️ 本目录立场）：**Copilot 上限 ≈ 语义模型质量**——
口径混乱的租户里 AI 只会放大错误；与 10 章"治理先行"呼应，
与治理册质量章同构（[../Understanding_Data_Governance/07-数据质量.md](../Understanding_Data_Governance/07-数据质量.md)）。

## 8.6 消费面选型速查（评审用）

| 需求 | 推荐链 | 依据章 |
|---|---|---|
| 大表交互报表 | Lakehouse/Warehouse 表 → Direct Lake | 8.2/04/05 |
| 外部 BI 工具直连 | T-SQL 端点/REST（03 章 API 面） | 03/05 |
| 运营者自助问答 | Copilot on 语义模型 | 8.5 |
| 口径中心治理 | 一域一语义模型 + 目录登记 | 8.1/09 |
| 极低延迟单表 | Import 缓存模式仍合法 | 8.3 ⚠️ |

## 8.7 一个反例重构：Direct Lake 上的"隐形 Import"（⚠️ 案例重构）

报表团队用 Direct Lake 连大表，却在模型里堆计算列与隐式物化——
等价于把导入成本从"搬运"挪到了"每查询"，两头的坏都占了。
正解：变换下沉到 04/05/06 章写入层，模型只留度量与关系。
（此例为教学构造，非原书案例；机制依据 8.2 模式语义 ⚠️。）

## 8.8 本章收口

湖中心故事到消费端的闭环：
**同一份 Delta 文件，Spark 写它、T-SQL 查它、Direct Lake 把它变成报表、Copilot 把它翻译成人话**——
四层零搬运，这就是副标题 "End-to-End Analytics" 的完整句子。
任何一层需要"再拷一份"，都是架构异味信号。

## 8.9 三模式决策小抄（⚠️ 教学重构，综合 8.2/8.3/8.6）

| 问题 | 是 → | 否 → |
|---|---|---|
| 表已在 OneLake（湖/仓）？ | Direct Lake 首选 | 考虑 Import/DQ |
| 需要模型内复杂转换？ | 停下，下沉到写入层（8.7） | 继续 |
| 源系统能扛直查 QPS？ | DirectQuery 合法 | 别用 DQ 硬扛 |
| 离线/边缘可用性要求？ | Import 仍不可替代 | 默认不导入 |
| 新鲜度按分钟即可？ | 任一模式都可谈成本 | 先修管道再谈模式 |

用法：五问从上到下，第一个"否"出现处即改道点；全部走通则 Direct Lake 是缺省答案——这正是微软文档给湖表消费的第一推荐位（⚠️ 转述当日页倾向）。

## 核心概念速览（中英对照）

- **语义模型** — Semantic model：度量值/DAX/关系的统一定义载体（原数据集）。
- **Direct Lake** — Direct Lake：报表直读 OneLake 表、免导入免转发的混合模式。
- **导入模式** — Import mode：数据抽取进模型内存，延迟最优、新鲜度最差。
- **DirectQuery** — DirectQuery：查询实时打回源，新鲜度最优、延迟最差。
- **模式混用** — Mixed mode per table：同一模型按表选 Direct Lake/Import/DQ。
- **数据应用** — Data app：寄宿于 Fabric 的 Power BI 外应用形态。
- **Copilot** — Copilot：Fabric 各面的生成式 AI 助手族（受功能开关约束 ✅）。
- **DAX** — Data Analysis Expressions：语义模型度量语言。
- **分页报表** — Paginated report：像素级打印向报表。
- **口径裁决点** — Semantics ownership point：语义模型作为业务定义执行器的治理读法。
- **隐形 Import** — Hidden import（本目录用语 ⚠️）：Direct Lake 模型里堆转换导致导入成本变相复活的反模式。

## 最新演进与工业实践

- **Fabric IQ 把语义层再上推**（✅ https://learn.microsoft.com/en-us/fabric/iq/overview 实测 200，访问 2026-09-27）：
  IQ 文档枢纽 2026-09-27 存在于 Learn 一级目录，方向=语义/本体层统一多负载理解（⚠️ 概念边界以当日页为准；
  本册 2025-08 印刷版不可能覆盖）。读法：**Direct Lake 解决"数据不搬"，IQ 试图解决"含义不搬"**——
  与 Data Mesh 的"语义可供性"命题正面对撞（对照 [../Data_Mesh/09-按可供性设计数据产品.md](../Data_Mesh/09-按可供性设计数据产品.md)）。
- **AI 治理捆绑**：微软把 Copilot 数据驻留/租户边界写进产品条款（⚠️ 转述；
  治理评审以 09 章 + 当日安全文档为准，2026-09-27 未逐条核条款文本，诚实登记）。
- **旧文档路径失效潮**（✅ curl 2026-09-27）：power-bi 域 Direct Lake 两候选、fabric/developer-center Copilot 路径均 404——
  2024/2025 教程直链大面积失效，本目录已固化在 00 第七节禁引清单。
- **工业实践**：报表团队最常见迁移事故 = 把 Import 思维带进 Direct Lake（在模型里重做转换，8.7 反例）；
  正解是把变换下沉到写入层——该经验与 [../Google_BigQuery_TDG/00-总览与阅读地图.md](../Google_BigQuery_TDG/00-总览与阅读地图.md) 社区讨论的"ELT 优先"结论跨厂商一致（⚠️ 归纳）。
- 复习口令（⚠️ 教学构造）：**"一次定义、四层零搬、模型不搬数据"**——消费面三句箴。
