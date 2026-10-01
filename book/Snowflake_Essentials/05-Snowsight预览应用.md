# 05 Web 界面：Snowsight 预览应用（Snowflake Web Interface: Preview App / Snowsight）

> 原书章：Ch.5 "Snowflake Web Interface: Preview App (Snowsight)"（pp.75–113），DOI `10.1007/978-1-4842-7316-6_5` ✅（Crossref 章级寄存实证）。
> 口径：页码区间一手实证；成书期 Snowsight 尚名 "Preview App"，本章以「成书期描述 ⚠️ + 2026 现行文档 ✅」双轨写，现行机制均以官方文档转述 ⚠️ + URL 锚定。

## 阅读目标

1. 记住 Snowsight 相对 Classic 的四个产品决策（卡片化/项目化/仪表盘/管理信息架构）。
2. 能在 2026 现行 UI 中完成本章全部教学动作（worksheet、数据浏览、装载向导、仓库管理）。
3. 理解"预览转正"对本书的杀伤半径：Ch.4 整章作废、本章骨架存活。

## 1. 成书期定位（章题即史料）

- 章题原文 "Preview App (Snowsight)" 是**一手的年代学证据**（✅ Crossref 题名）：2021-12 时 Snowsight 未 GA。
- 39 页（pp.75–113）超过 Classic 章（35 页）——作者团已预判重心转移，本册实际是**最早系统介绍 Snowsight 的出版物之一**（⚠️ 出版史评述）。
- 登录入口当时为 `https://app.snowflake.com` 形态（⚠️ 考古），现统一到账户域名（见 04 章对照）。

## 2. 四大工作区（成书期骨架 → 2026 演进）

| 成书期模块 | 2026 对应（✅ ui-snowsight 系列） | 说明 |
| --- | --- | --- |
| Projects（共享工作表） | **Worksheets / Workspaces** | 私有+共享工作表统一，✅ https://docs.snowflake.com/en/user-guide/ui-snowsight-worksheets |
| Dashboards（卡片） | **Notebooks + Dashboards** | 新增 Notebook 单元（SQL/Python/Markdown 混排）⚠️ |
| Data（浏览器） | **Data**（Explorer + Query History + Loads） | ✅ https://docs.snowflake.com/en/user-guide/ui-snowsight-data |
| Admin | **Admin**（Users/Roles/Warehouses/Cost） | 成本页后随 Horizon 扩为 Budgets，✅ https://docs.snowflake.com/en/user-guide/budgets |

- 设计逻辑差异（⚠️ 转述）：Classic=按 DBA 对象摆货架；Snowsight=按任务流摆卡片（分析者旅程：找数→查询→可视化→共享）。

## 3. 本章教学动作的 2026 复现清单

1. **建工作表并跑样例查询**：Data→Explorer 搜表 → 右键 "Query & Inspect" → 生成 SQL → Save to worksheet（✅ ui-snowsight-worksheets）。
2. **可视化**：结果区 "Create → Chart" 存成 Dashboard 卡片（✅ ui-snowsight-dashboards 主题，经索引登记）。
3. **装载**：Data→Tables→"Load" 打开向导，含自动推断 schema（INFER_SCHEMA 的 UI 化，✅ https://docs.snowflake.com/en/user-guide/data-load-schema-evolution）。
4. **管理仓库**：Admin→Warehouses 起停/挂起分钟/尺码——与 10 章参数面板同一事实源（⚠️）。
5. **看活动**：Admin/Share 页与 Query Profile 入口——Tuning 册剖析器章的官方载体（✅ https://docs.snowflake.com/en/user-guide/ui-snowsight-activity）。

## 4. 🔧 无实测声明与替代直觉

- Snowsight 是浏览器产品，本环境无法起账户实测 → 全章 ⚠️/✅ 口径，无 🔧 类比（类比组分配在 03/09/10/11/12/13 章，见 00 汇总）。
- 概念类比留给引擎层（03 章裁剪、10 章算力）；UI 层"以官方文档 + 现行截图为唯一依据"。

## 5. 章内易错与疑问

- **易错 1**：旧资料里的 "Projects" 在现行 UI 已更名/并入——搜不到别疑心权限（✅ worksheets 页）。
- **易错 2**：Snowsight 权限仍由角色决定（Ch.7），UI 换血没有改变 RBAC 模型——"界面找不到"九成是授权问题（⚠️）。
- **疑问**：为什么本册把两套界面各写 35–40 页、TDG 只写 Snowsight？答：出版窗口错位半年（04 章联系表），也提示入门册修订频率应高于概念册——工业界"教程保质期"经验由此而来。

## 扩展深读点：四工作区任务流评级与 FAQ

### 教学动作→现行入口→熟练度评级（自测用）

| 动作（本章原文任务） | 2026 现行入口（✅） | 评级标准 |
| --- | --- | --- |
| 跑一条查询 | Worksheets + Cmd+Enter | 盲操作 <30s |
| 采样浏览一张表 | Data→表页 "Query & Inspect"/Preview | 能用过滤器二次下钻 |
| 装载一个 CSV | Table 页 Load 向导+格式预览 | 能说清它封装了哪两条命令（Ch.12） |
| 建图并分享 | Results→Create Chart→Dashboard/Link | 会设分享权限（Ch.7 角色） |
| 起停/改仓库 | Admin→Warehouses | 理解每旋钮对应 ALTER 参数（Ch.10） |
| 查一次慢查询 | Activity→Query Profile | 能指认扫描/本层/交换耗时段（Tuning 册入门） |
| 看账单与用量 | Admin→Cost/Budgets | 能按角色/标签拆分（Ch.6 后代） |

### FAQ

- **Q1 找不到某旧功能先查什么？** A：先权限（角色缺 USAGE/MONITOR），后名称（Projects→Worksheets 类换代），最后才疑文档。
- **Q2 Snowsight 会不会重演 Classic 的"整章作废"？** A：UI 永在漂移，但本目录的对策是**以 ✅ 文档主题名而非截图**为锚——迁移对位表（04 章）的"SQL 层常数"原则同样适用未来。
- **Q3 界面学习的时间预算应该是多少？** A：入门阶段 UI≤总学时 15%，其余给 SQL/权限/成本——2022 年两章 UI 共 74 页、今日仍有效的部分不足三成，比例即教训。

## 新旧词表对照卡（读 2022 材料随身用）

| 成书期词面（本册/同期博客） | 2026 现行词面（✅） | 备注 |
| --- | --- | --- |
| Preview App | Snowsight（无后缀） | 章题即年代证据 |
| Projects | Worksheets / Workspaces | 私有/共享合并 |
| Data Product（Snowsight 旧义） | Listings / Collaboration | 并入协作体系（308 实证） |
| Preview 侧栏 Data 树 | Data（Explorer/Query History/Loads 三组） | 三组分域是后成的 |
| Cards 收藏 | Cards/Dashboards 族 | 语义未变壳变 |
| Admin→Account Management | Admin 组织视图+Account Manager 整合 | 旧专页 404 |
| Warehouse 悬浮菜单 | Warehouses 列表+更多操作 | 参数面同构 |

- 读法建议：本章与 04 章交替对读（每读一段旧界面就回本表找新家），比线性刷完更省力——两章的表格互为索引是本目录的重排意图。

- **Q4 本目录里 04 和 05 谁先读？** A：教学顺序随原书（04→05），实操顺序倒过来（05 起步、04 作词典）——两章互为对方注脚的编排是本目录的刻意设计。
- **Q5 为什么自测清单要设"熟练度"列？** A：UI 学习成果难以笔试自证——以"能否盲操作/能否说出背后命令"两级自评，防止界面章退化成截图记忆。
- **Q6 词表两册（04 对位表+05 词表）会不会又过时？** A：会——所以两张表都以 ✅ 现行文档页为最终裁判，表本身只是迁移期的临时桥梁；这正呼应"界面叙事寿命最短"的全书教训。

## 与其他书的联系

| 对照 | 说明 |
| --- | --- |
| [04-经典控制台.md](04-经典控制台.md) | 被替代者；两章合读=UI 迁移史 |
| [../Snowflake_The_Definitive_Guide/11-Snowsight可视化.md](../Snowflake_The_Definitive_Guide/11-Snowsight可视化.md) | 同年代 TDG 的 Snowsight 单章成熟版 |
| [../Tuning_the_Snowflake_Data_Cloud/03-查询剖析器.md](../Tuning_the_Snowflake_Data_Cloud/03-查询剖析器.md) | Query Profile 所在界面在其处为调优主场景 |
| [../Advanced_Snowflake/12-Cortex与AI数据云.md](../Advanced_Snowflake/12-Cortex与AI数据云.md) | ⚠️ 降级册：Snowsight 上 AI 面板（Cortex/Copilot）的推定深潜 |
| [14-数据共享与市场.md](14-数据共享与市场.md) | Marketplace/Exchange 浏览体验全部长在 Snowsight 内 |

## 章末自测

1. "Preview App" 章题告诉我们关于成书年代的什么事实？
2. Classic→Snowsight 的导航哲学差异一句话是什么？
3. Query & Inspect、Load Data、Create Chart 三个入口各自的服务对象？
4. 用户在 Snowsight 找不到某功能，先查什么、后查什么？
5. 在"教学动作评级表"中给自己 D3–D4 两项定级，并说明证据。
6. 新旧词表与 04 迁移对位表各自解决哪一类误读？为何互为镜像？

## 核心概念速览（中英对照）

| 中文 | 英文 | 一句话定义 |
| --- | --- | --- |
| Snowsight | Snowsight | 现行唯一官方 Web 界面 |
| 工作表/工作区 | Worksheet / Workspace | SQL 编辑与共享单元 |
| 笔记本 | Notebook | SQL/Python/Markdown 混排文档 |
| 数据探索器 | Data Explorer | 库/schema/表树形浏览与采样 |
| 卡片/仪表盘 | Card / Dashboard | 轻量可视化与聚合视图 |
| 查询剖析 | Query Profile | 执行计划与耗时分解视图 |
| 活动监控 | Activity | 查询/登录/变更历史页 |

## 最新演进与工业实践

- **转正与一统（2022→2026）**：Snowsight 2022 GA；Classic 退役后成为唯一界面——本章章题限定词 "Preview" 已成历史，阅读时自动脑内替换（✅ 文档全线下沉 ui-snowsight-* 系列，索引 https://docs.snowflake.com/en/user-guide/ui-snowsight）。
- **AI 面板叠加（2023→）**：Copilot（SQL 辅助）、Cortex Analyst（自然语言问数）、 notebooks 内 Python/Snowpark 单元——界面从"查询工具"膨胀为"数据工作台"（✅ https://docs.snowflake.com/en/guides-overview-ai-features）。
- **治理面扩张**：Admin 区新增 Budgets/Alerts（成本熔断）、Trust Center（合规文档库）（✅ https://docs.snowflake.com/en/user-guide/budgets）。
- **工业实践**：团队标准操作=共享 Workspaces + Git 仓库存 notebook（✅ https://docs.snowflake.com/en/user-guide/account-replication-git-repositories 同族主题）；本册 39 页 UI 教程 Today 折合 3–4 小时文档阅读——但"任务流导航"设计思想仍是新人上手主线。
