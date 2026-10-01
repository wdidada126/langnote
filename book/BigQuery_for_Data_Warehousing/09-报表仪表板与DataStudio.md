# 09 报表仪表板与 Data Studio

> 对应原书 **Ch.16 Reporting（pp.355–378）**、**Ch.17 Dashboards and Visualization（pp.379–400）**、**Ch.18 Google Data Studio（pp.401–416）**（章题/页码：Crossref DOI _16 / _17 / _18，✅ 实抓）。
> 正文为精读重构；机制为官方文档/公开资料转述（⚠️）；Part V 消费侧三章合一档（00 有逐章映射表）。

## 一句话主题

仓库的钱要花在「被看」上：第 16 章讲**报表**（可重复、可审计的固定产出），第 17 章讲**仪表板**（交互下钻的实时面貌），第 18 章给一个免费工具（Data Studio）的落地教程。三章构成消费侧全景，也是作者「数据决策日常化」信念的兑现层（Ch.1 立项动机的镜像）。

## Ch.16 Reporting：报表生产线

### 16.1 报表分类与义务（重构）

- 三类：**运营报表**（日报/周报，定时投递，容忍度低）、**分析报表**（专题深挖，一次性）、**合规报表**（审计/财务，改动要走变更流程——与 Ch.15 消费者合同同轨，见 [08-数据治理与长期适应.md](08-数据治理与长期适应.md)）；
- 报表工程四要素：口径唯一（指标定义进语义层/视图层，禁止各报表自写聚合）、数据时点标注（as-of 时间显式印在页脚）、刷新 SLA（对接 Ch.10 值守）、退役机制（无人看的报表是最大的治理负债，作者建议季度访问审计下线）；
- 载体谱系：Sheets/Excel 连接器（业务侧最爱、IT 侧最怕——口径漂移通道）、邮件 PDF、嵌入式报表 API（把报表织进业务应用是本章技术高点，⚠️ 2020 转述）。

### 16.2 给报表写 SQL 的手艺（回收 Ch.9）

- 聚合先行：面向报表建**汇总层表/物化视图**（按需模式下扫描费直接减半以上，E5 类比见 [07-云日志与BigQuery进阶.md](07-云日志与BigQuery进阶.md)）；
- 行列透视：`PIVOT/UNPIVOT`（2020 后陆续 SQL 化 ⚠️ 版本注，此前用 CASE+聚合手写）；同环比窗口模板（`LAG/SUM OVER` 帧控制）；
- 口径测试：每张报表级视图配「指标对账断言」（合计=明细和、空值率阈值），装载链尾自动跑——测试文化是报表公信力的地基（Ch.3 质量基线的消费端延伸）。

## Ch.17 Dashboards and Visualization：仪表板设计

### 17.1 仪表板 ≠ 报表（作者辨析，重构）

- 交互三权：下钻（drill）、筛选（filter联动）、跳转（跨页上下文传递）——报表是「读完即止」，仪表板是「越点越深」；
- 信息设计纪律（转述社区共识）：一屏一问题、先总后分、异常色语义一致、同比基线常驻；作者点名反模式：**饼图堆满 + 无基线的折线 + 十色热力**——「好看的仪表盘是数据民主化的假象」；
- 性能契约：仪表板直连大表=并发扫描费黑洞；三层解法（汇总层供数 / 抽取缓存 / BI Engine 类内存加速——2020 时点 BI Engine 为独立 SKU，⚠️ 转述）；每图查询预算制是 Ch.4 成本三角在消费侧的投影。

### 17.2 工具选型地图（2020 口径，⚠️ 转述）

- Google 自家双轨：**Data Studio（免费轻）vs Looker（重语义建模，LookML）**——选型轴=「业务自助度 vs 口径强制度」；
- 第三方连接器：Tableau/Power BI/Qlik 经 JDBC/原生连接器读 BQ；Grafana 走 SQL 数据源插件承接运维域；
- 选型三问（重构）：消费者会不会写 SQL？口径是否需要平台级强制？加速层的钱谁出？——三问答完工具自然选定，作者反对「先买工具再找用例」。

## Ch.18 Google Data Studio：免费工具落地教程

### 18.1 产品形态（⚠️ 2020 转述）

- 浏览器端报表拼装：连接 BigQuery/Sheets/Billing 等官方连接器，SQL 自定义字段+数据 blends（多源横向拼接）；
- 直连语义：每图一次查询打回 BQ（新鲜度=实时，代价=扫描费与并发配额，与 Ch.17 性能契约对冲）；抽取加速（BigQuery 侧缓存/汇总表兜底）；
- 共享治理：链接即读（组织域控制）、查看者不需仓库权限的凭证透传模式（连接器 owner 承担权限与账单——作者提醒这是**隐性成本集中点**，需登记进 Ch.4 事后归因）。

### 18.2 实操路径重构（发布到告警一条龙）

1. 建汇总层视图（含口径断言）→ 2. Data Studio 连接器指向视图（不指裸表，权限与成本双收口）→ 3. 页面信息设计按 17.1 清单自检 → 4. 嵌入企业门户/邮件订阅 → 5. 异常值配「数据驱动告警」（阈值组件或回流 Ch.12 Monitoring webhook）——**报表发现问题、仓库解释问题、管道修正问题**的闭环在此章完成最后一段（Ch.5–7→Ch.9→Ch.12 全链回收）。

## 附：报表配方与评审卡（自拟教学示意，⚠️ 非原书内容）

- **同环比口径模板**（报表层视图，收编 16.2）：

```sql
CREATE OR REPLACE VIEW rpt.sales_daily AS
SELECT d, sales,
  SAFE_DIVIDE(sales - LAG(sales, 7)  OVER (ORDER BY d), LAG(sales, 7)  OVER (ORDER BY d)) AS wow,
  SAFE_DIVIDE(sales - LAG(sales, 28) OVER (ORDER BY d), LAG(sales, 28) OVER (ORDER BY d)) AS mtd_yoy_proxy,
  SUM(sales) OVER (ORDER BY d ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS ma7
FROM agg.sales_by_day;   -- 汇总层供数（17.1 性能契约第一层）
```

- **报表级质量断言**（口径测试样例）：`ASSERT (SELECT ABS(sum_sales - (SELECT s FROM detail)) < 0.01) AS 'reconcile'` 思路——断言失败即阻断调度（Ch.6 依赖冻结联动）；每张消费级视图至少一条「合计=明细和」+一条「空值率阈值」；
- **仪表板评审卡**（上线前打勾，重构）：□ 一屏一问题已声明；□ 每图标注数据来源视图与 as-of 时点；□ 每图查询预算（估算字节×刷新频次×并发）经财务签认；□ 下钻层有分区谓词；□ 异常色语义与全站一致；□ 三个月无人访问则进退役队列——评审卡归档进 Ch.14 目录台账；
- 凭证透传的账本治理（18.1 隐性成本的收口配方）：为所有 BI 连接器的服务账号单独立项目/单独标签，账单侧一眼看清「看报表花了多少仓内钱」；消费者侧显示真实查询者则要求连接器支持 On-Behalf-Of 模式（各 BI 实现不一 ⚠️）；
- Data Studio 时代的遗产清单（供老册读者对表）：社区连接器市场、`ML.ANNOTATE` 式计算字段、blend 的 join 键爆炸警告——这些概念在 Looker Studio 时代换了名字但没换物理（见演进节）；
- 思考题（5 道）：T1 为什么「连接器只指视图」能同时收口权限与成本？T2 直连模式与抽取模式在合规审计上的取证差异？T3 语义层缺位时，两份周报打架的第一根因链？T4 BI Engine 类加速的钱应由消费方还是平台方出（用 Ch.4 归因工具论证）？T5 给「周活跃消费者数」设计一条 INFORMATION_SCHEMA 上的统计 SQL。

## 系列互链

- 同书纵向：SQL 手艺 [05-仓库养护与查询开发.md](05-仓库养护与查询开发.md)；成本投影 [02-数据盘点与成本管控.md](02-数据盘点与成本管控.md)；告警联动 [07-云日志与BigQuery进阶.md](07-云日志与BigQuery进阶.md)；口径治理 [08-数据治理与长期适应.md](08-数据治理与长期适应.md)。
- 他书横向：语义层/指标层的现代工程化（dbt metrics、指标中台）对位 [../Analytics_Engineering_with_SQL_and_dbt/00-总览与阅读地图.md](../Analytics_Engineering_with_SQL_and_dbt/00-总览与阅读地图.md)；运营分析/实时看板谱系（RTA 主题）登记见 [00-总览与阅读地图.md](00-总览与阅读地图.md) 互链表（同波 #157/#199 只登记不链）。

## 核心概念速览（中英对照）

- **运营报表** — Operational Report：定时定量投递、低容错的例行产出。
- **口径唯一** — Single Definition：指标定义收敛于语义层/视图层的纪律。
- **as-of 时点** — As-of Timestamp：报表数据截止时刻的显式标注义务。
- **语义层** — Semantic Layer：业务指标与物理列之间的映射与治理层。
- **报表退役** — Report Retirement：按访问审计下线无人看报表的季度动作。
- **下钻** — Drill-down：从汇总值点击进入明细维度的交互权。
- **抽取加速** — Extract/Acceleration：以缓存/内存层换仪表板并发与延迟。
- **BI Engine** — BI Engine：BigQuery 配套内存加速 SKU（2020 独立售卖）。
- **Data Blending** — Blending：多数据源在可视化层横向拼接的技术与风险。
- **凭证透传** — Credential Pass-through：连接器以 owner 身份代查、查看者免直权的共享模式。
- **数据驱动告警** — Data-driven Alert：以报表阈值触发监控动作的逆向闭环。
- **LookML** — LookML：Looker 的声明式语义建模语言，口径强制度代表。

## 最新演进与工业实践

- **Data Studio 之死与 Looker Studio 之名（2022–2026）**：Data Studio 于 2022-11 更名 Looker Studio（免费层）并长出 Looker Studio Pro/Connector 生态——18 章教程的产品名整体进入历史（⚠️ 转述；canonical 文档 `cloud.google.com/looker-studio/docs` 与本波中国侧镜像 `docs.cloud.google.cn/looker-studio/docs/introduction` 实测 404，不给 ✅ 链，缺口如实登记）。Looker 语义模型在 2023 后与 BigQuery 深化整合（Warehouse Performance Analysis、Gemini 辅助 LookML ⚠️）。
- **消费侧新面**：Notebook（BigQuery Enterprise Notebook/Jupyter 托管）与 AutoML 面板把「探索性可视化」从 BI 工具分流（衔接 [10-BigQueryML与Jupyter公共数据集.md](10-BigQueryML与Jupyter公共数据集.md)）；对话式取数（NL2SQL/Gemini in BigQuery，2024–2025 ⚠️）正在改写 17.2「消费者会不会写 SQL」的选型轴。
- **工业实践（2024–2026）**：指标平台（metrics layer：dbt Semantic Layer/Snowflake Semantic Views 等）把 16.1「口径唯一」升格为跨工具合约；仪表板查询预算与加速层成本进入 FinOps 报表；「报表访问审计→自动退役」成为 SaaS 化数仓产品标配功能。
- **不变项**：17.1 的信息设计纪律与「一屏一问题」跨代有效；18.2 的「连接器只指视图不指裸表」仍是权限/成本双收口的第一实践。
