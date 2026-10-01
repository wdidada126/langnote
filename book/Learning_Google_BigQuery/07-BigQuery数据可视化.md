# 07 BigQuery 数据可视化：Data Studio、Tableau 与 R（Visualizing BigQuery Data）

> 对应原书 **Ch.7 "Visualizing BigQuery Data"**（章题与 13 个节题 ✅ QQ 阅读电子版实抓）。
> 正文为**精读重构**，非原书文本；机制描述「官方文档转述 ⚠️」；`docs.cloud.google.cn` 镜像对 Looker Studio 相关页 2026-10-02 实测 404，本章 URL 相应按 ⚠️ 处理（✅ 面复用 00 池）。
> 本章无 🔧 实验。

## 本章在本书中的位置

"interactive analysis" 的收口章：查出来的数字要能看、能讲。作者先花三节**不谈工具**谈可视化认知（为什么重要/摘要统计的危险/让可视化为你工作），再给三工具横评——免费但浅的 Data Studio、方便但贵的 Tableau、灵活但陡的 R。2017 年这个横评至今仍有讨论价值，只是三件棋子的名字和位置全换了（见文末演进节），阅读时要持续做名称翻译。

## 7.1 认知先行（Why is data visualization important? / The danger of summary statistics / Making data visualization work for you）

- 书中压箱案例（重构自 Anscombe's quartet 一脉 ⚠️）：**同一组均值/方差可以对应形态迥异的四张散点图**——作者用一句话版安斯康姆梗劝读者"先画图再下结论"；
- 三档读者画像（重构）：给老板看→单页仪表；给自己探索→即时散点/直方；给公众讲→叙事地图。工具选型围绕画像转，不围绕功能清单转——本章方法论含金量最高的一段。
- 与 Ch.4 的暗线：`count/avg` 是摘要统计的糖衣，可视化是解毒剂。

## 7.2 Google Data Studio：免费基本款（Simple yet basic，六节）

- 书中流程（⚠️ 转述）：Data Studio 建报告 → 连接器选 BigQuery（走 GCP 凭据）→ 选表 → 字段建模（维度/度量）→ 拖组件：时间轴、表格、**散点图**（making a scatterplot 节）、**地图**（making a map 节，地理字段自动识别经纬度/国家码）。
- "Other features" 节：过滤器控件、按查看者限数据行（行级权限的雏形）、社区可视化雏形期。
- 作者判词（重构）：**零成本零运维，适合内部自服务**；天花板在交互深度与像素级排版。
- 2026 翻译：Data Studio → **Looker Studio**（2022-10 更名，免费/Pro 双轨 ⚠️ 转述；镜像 looker-studio 文档页 404，不给 ✅ 链），BigQuery 连接器变成"亲生"级别，原生查询参数、Blend 数据混合等书中缺位能力已补（⚠️）。

1. Compose Query 界面三件套之外的第一站：查询结果区的 "Open in → Data Studio" 一键跳转（书里当作生态亲和力卖点 ⚠️ 转述）；
2. 免费档的隐性代价：无版本管理、无行级审计，团队化使用要升 Pro/走 Looker（2017 语境判词，2026 依旧成立只是名词换了 ⚠️）；
3. 地图组件依赖字段角色标注——回到 Ch.3 清洗（国家码大小写/别名），工具链在此闭环。

## 7.3 Tableau：方便但要钱（Simple, fairly flexible, but with a cost，三节）

- 书中路径：Tableau Desktop 的 **Google BigQuery 连接器**（当年第三方包 → 内置的过渡期）→ Live/Extract 两模式 → 地图层（map charts）与**词云**（word cloud，需装扩展或手写计算字段，书里给了 regex 分词的 Table Calc ⚠️）。
- 两模式对比是本章真正的技术点（重构）：**Live=把 SQL 下推 BQ 每次真查真付费；Extract=快照本地免重复扫描但会过期**——作者用 Ch.4 的扫描计费直觉做了选型表，这正是 🔧 T1/T5（04 章）在 BI 端的续集。
- 判词（重构）：分析师体验最好，License 成本与网关配置是摩擦项。
- 现状：BigQuery 官方 **Tableau 连接器（OAuth/服务账号认证）**久已内置于 Tableau；Extract 之外新增基于 BigQuery 物化视图的加速面（⚠️ 转述；✅ https://docs.cloud.google.cn/bigquery/docs/materialized-views-intro）。

## 7.4 R：灵活但陡（Complex but with considerable flexibility）

- 书中栈：R + **bigrquery** 包（`bq_project_query`）→ ggplot2 出图 → 地图/分布可视化；作者态度（重构）：R 是"把分析叙事完整代码化"的唯一选项，代价是全员 R 技能税。
- 与 Ch.6 Python 节互为镜像：同一查询落表动作，两语言两生态——2017 年少见地把 Python/R 并置教学，今天看是 BQML 时代伏笔（TDG 09 章收口 ⚠️ 概念见 ✅ https://docs.cloud.google.cn/bigquery/docs/bqml-introduction）。
- 现状：bigrquery/dbplyr 后端成熟、**dbplot、tidymodels 远程训练接 BQML** 为书后世界（⚠️ 转述）。

## 7.5 三工具裁决矩阵（书中观点重构 + 2026 校订）

| 维度 | Data Studio(→Looker) | Tableau | R |
| --- | --- | --- | --- |
| 成本 | 免费 | License 贵 | 免费(人力贵) |
| 上手 | 小时级 | 天级 | 周级 |
| 交互深度 | 浅 | 深 | 无限(代码) |
| 与 BQ 血缘 | 亲生 | 一等公民连接器 | 社区包 |
| 治理面 | 权限沿用 GCP | 独立 Server 体系 | 无 |
| 2026 位置 | 内部报表默认 | 分析专业户 | 统计/ML 叙事 |

## 7.6 一张图的两种建法（书中 2017 步骤 vs 2026 重构步骤）

**书中路线（Data Studio，Making a scatterplot 节，⚠️ 转述重构）**：

1. report.google.com 新建空白报告 → 数据源向导选 BigQuery；
2. 弹出 Google 账号授权 → 选项目 → 选表（可直接粘 SQL 当自定义查询）；
3. 字段面板把 `gestation_weeks` 拖为 X（维度）、`weight_pounds` 均值拖为 Y（度量）；
4. 散点组件入画布 → 右侧样式面板加聚合色 → 右上共享按钮出链接。

**2026 等价路线（Looker Studio，⚠️ 通识转述）**：

1. Looker Studio 资源库内置 **BigQuery(Standard SQL) 连接器**，OAuth/服务账号双认证；
2. 选表后进入"字段建模"页，维度/度量+聚合默认与书中一致；
3. 散点/地图组件同源；新增：查询参数联动、混合数据源、页面级行过滤（RLS）；
4. 分享面从"链接可见"进化到 Workspace 域内审计 + Pro 版 API 编程接口（⚠️）。

- 两代步骤一一对照后可以确认：**作者教的"心智步骤"一步没死，死的只是菜单路径**——这正是本目录"读 Packt 老册的正确姿势"示例；
- 地图节同构复核：书中"国家码字段自动识别"今天对应 geo 角色标注，仍需先过 Ch.3 清洗（大小写/别名坑原样保留）。

## 7.7 数据可视化在云仓三册中的分工

- 本册：工具横评与建图手感（本章全部内容）；
- TDG：把可视化归入"数据消费"一角，主力在查询与 API（[../Google_BigQuery_TDG/05-使用BigQuery进行开发.md](../Google_BigQuery_TDG/05-使用BigQuery进行开发.md)）；
- BQDW：报表工程化——权限、调度、成本护栏三件套（[../BigQuery_for_Data_Warehousing/09-报表仪表板与DataStudio.md](../BigQuery_for_Data_Warehousing/09-报表仪表板与DataStudio.md)）；
- 三册连读结论（本笔记裁决）：**工具会改名，"摘要统计有害论 + 三档读者画像"永不过期**——7.1 那三节是本章真正的传家宝；
- 若只允许读一节：读 7.1.2（摘要统计的危险）——它是全部 BI 治理文档里最难被替代品取代的一段（⚠️ 观点注记）。

## 阅读策略与坑

1. 7.1 值得整节精读——它是全书少见的"反工具崇拜"文本；
2. 三工具的手把手步骤全部过期（界面代际差），**只带走 Live/Extract 权衡与连接器认证模型**；
3. 词云/地图这类"炫技图"作者自己也吐槽（Ansbury/红鲱鱼警告在 7.1 回收 ⚠️）；
4. 本章没有的第四个选项：Notebook（BQ 原生 notebook 2023 ⚠️）——读 TDG 05 章补齐开发者可视化面。

## 7.8 可视化的账单面（7.3 Live 模式的成本显微镜）

- 一次仪表板刷新的账单解剖（重构自书 7.3 两模式讨论）：**页面上 N 个组件 × 每次重查 = N 条 SQL 打进 BQ**；5 人开会同屏刷新，Live 模式瞬间放大成 5N 条查询（⚠️ 算术示意）；
- 四道传统刹车（书中与社区合流）：Extract 快照、聚合层预计算（Ch.5 视图/汇总表）、结果缓存（2018 年后的官方层 ✅ 概念转述）、限速刷新（Data Studio 缓存设置页 ⚠️）；
- 2026 对照：性能层级/预留槽位下账单形态从"次数×字节"变成"槽位×时间"，但**"BI 是隐藏查询发生器"**的系统性判断反而更强——仪表板治理（查 who/when/what via information_schema + 系统分析套件 ⚠️）已是标配工序；
- 一句收尾（呼应 04 章 T5）：**给老板的仪表盘越漂亮，给 CFO 的账单越需要会讲**——本章真正没教的是这件事，读 BQDW 02/09 章补上。

## 7.9 本章毕业标准（三件半事）

- 能默画"报表→连接器→BQ"三段箭头并标出每段的认证与计费归属；
- 能用 7.1 三档读者画像给任意需求选工具（并说清 7.5 矩阵里至少两个维度的代价）；
- 能复述 Live/Extract 权衡并给出四道刹车中任意两道（7.8）；
- 半件：知道本章界面截图全部作废、概念全部存活——这是读一切老工具书的心法开关。

## 核心概念速览（中英对照）

| 中文 | 英文 | 一句话 |
| --- | --- | --- |
| 摘要统计陷阱 | danger of summary statistics | 均值相同图形可迥异 |
| 自服务报表 | self-service reporting | Data Studio 定位 |
| 连接器 | connector | BI 工具进 BQ 的闸门 |
| 实时模式 | live query | 每次真查真计费 |
| 抽取模式 | extract | 快照本地防重复扫描 |
| 数据混合 | data blend | 跨源拼报表 |
| 行级限看 | row-level restriction for viewers | 权限雏形 |
| 地理字段 | geo field | 自动识别生成地图 |
| 词云 | word cloud | regex 分词计算字段 |
| R 客户端 | bigrquery | tidyverse 进 BQ 的门 |
| 叙事代码化 | analysis as code | R 路线的哲学卖点 |
| 品牌更名 | Data Studio → Looker Studio | 2022-10 翻译层 |

## 最新演进与工业实践

- **工具谱系重排**：Looker Studio（更名+全家桶化，与 Looker 语义层并轨 ⚠️）、**BigQuery 原生可视化**（查询页直出图 + Notebook + Exploring data 界面 ⚠️）、Omni 时代第三方 BI 矩阵；书中"三选一"变成"分层并用"。
- **成本端反转**：Live 查询在性能层级/Editions 下从"按字节心疼"变为"按预留槽位吃并发"，Extract 的价值主张从省钱转向离线稳定（⚠️ 转述；✅ https://docs.cloud.google.cn/bigquery/docs/slots）。
- **语义层回归**：LookML/metrics 层把"7.1 给老板看什么"从工具问题升级为治理问题；盘上 BI 语境互读 [../BigQuery_for_Data_Warehousing/09-报表仪表板与DataStudio.md](../BigQuery_for_Data_Warehousing/09-报表仪表板与DataStudio.md)（BQDW 的 DataStudio 章正是本书本章的 2020 校订版）。
- 工业实践：现代 BI 栈共识=**报表轻工具、口径重仓库**——聚合逻辑沉到视图/物化模型层，BI 端只拖维度；书中连接器两侧的手写 SQL 已迁入版本库（⚠️ 通识转述）。
