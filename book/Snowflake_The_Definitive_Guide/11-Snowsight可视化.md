# 11 · Snowsight 数据可视化（Ch11: Visualizing Data in Snowsight，✅ 章题实抓）

> 原书第 11 章（约 p.347–371，页码锚点来自配套仓库 Chapter11.sql 注释 ✅ 实抓）。
> 全书唯一"以 Web UI 为主、SQL 为辅"的章：官方配套 SQL 里明说
> "There are some examples / instructions that refer to the Snowsight Web UI … including screenshots"（实抓 ✅）。
> UI 操作细节无法本机实测 → 转述 + ⚠️ 口径。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 11.1 | Snowsight 定位：控制台 + 工作台 + 轻量 BI 三合一 | 从 Classic Console 统一到 Snowsight 是 2021–2022 的事 |
| 11.2 | 工作表（Worksheets）：多语句编辑器、上下文四件套、草稿/共享 | 本章练习主战场（p.347 建 "Chapter11 Visualization" 工作表 ✅） |
| 11.3 | 结果集操作：表格视图、抽样、下载、行列统计 | `LIMIT` vs `SAMPLE` 的取数姿势（p.352–353 实抓） |
| 11.4 | 图表：柱/线/饼/散点/热力等图表库，X/Y 轴与聚合配置 | 查询即图表：图表是结果集的投影 |
| 11.5 | 仪表盘（Dashboards）：多图表页、参数化、可共享 | 从"一次查询"到"可复用报表" |
| 11.6 | 边界：Snowsight 内置可视化 vs 外部 BI（Tableau/PowerBI 等） | 内置适合探查与轻量看板，企业报表仍靠外部 BI ⚠️ |
| 11.7 | 治理视角：可视化消费的仍是虚拟仓库算力 | 图表刷新的账单在成本章结账（第 8 章） |

## 核心精讲

### 1. 上下文与取数（书中 SQL 实抓 ✅，逐句）
```sql
// p.349 实抓：本章全程 SYSADMIN + 示例库
USE ROLE SYSADMIN;
USE DATABASE SNOWFLAKE_SAMPLE_DATA;
USE SCHEMA TPCDS_SF100TCL;

SELECT * FROM STORE_SALES LIMIT 100;                      -- p.352：前 100 行
SELECT * FROM STORE_SALES SAMPLE (100 ROWS);              -- p.353：随机 100 行
SELECT * FROM STORE_SALES TABLESAMPLE SYSTEM (0.015);     -- p.353：按 1.5% 概率抽行
SELECT * FROM CATALOG_RETURNS LIMIT 5000000;              -- p.354：大结果集实验
SELECT * FROM CATALOG_RETURNS LIMIT 9999;                 -- p.354：贴着上限取
```
- `SAMPLE (n ROWS)` 与 `TABLESAMPLE SYSTEM (p)` 是同一构造的两种写法
  （官方：https://docs.snowflake.com/en/sql-reference/constructs/sample ✅200）；
  随机抽样看数据分布、`LIMIT` 看头部样本——探查语义完全不同（对照第 4 章 AT(OFFSET)）。
- p.354 两个 `LIMIT` 一对照，指向的是 **Snowsight 结果页/下载的行数上限**这一 UI 行为：
  超大结果在网页端会被截断/分批，全量导出应走 `COPY INTO <location>`（UNLOAD，第 6 章）。
  具体上限数值随版本变化 → ⚠️ 不写死，以官方 UI 文档为准：
  https://docs.snowflake.com/en/user-guide/ui-snowsight ✅200。
- 本地不可实测，但抽样思想可在 DuckDB 复刻（本地代理实验，非 Snowflake 实测）：
  `SELECT * FROM 'tpch.parquet' TABLESAMPLE SYSTEM (1.5);`

### 2. 工作表：SQL 工作台三件套
转述 ⚠️（https://docs.snowflake.com/en/user-guide/ui-snowsight-worksheets ✅200）：
- **多标签/多语句**：一个工作表可含多条语句，选择性执行；结果逐语句分页。
- **上下文条**：UI 上的 Role/Warehouse/Database/Schema 选择器 = 第 1 章 `USE …` 四件套的图形化，
  两者会互相改写——看截图前先确认上下文（本章 p.347 prep work 强调 SYSADMIN + COMPUTE_WH ✅）。
- **共享与权限**：工作表可按角色共享（view/run），本质仍是第 5 章 RBAC 的延伸；
  消费者跑在**自己的仓库**上，账单归执行者。
- `SNOWFLAKE_SAMPLE_DATA`（TPCDS_SF100TCL、TPCH_SF100 等）是免装载的公共演示数据，
  只读、跨区域共享而来（第 10 章 live share 的官方示例 ✅ 口径转述）。

### 3. 图表与仪表盘（书中为截图练习 ⚠️）
- 图表 = 对**当前查询结果集**的可视化投影：选图表类型 → 指定 X 轴列/Y 轴列/聚合/分组，
  不需要预建模（官方：https://docs.snowflake.com/en/user-guide/ui-snowsight-dashboards ✅200）。
- 仪表盘把多个图表组件排成一页，支持**参数（filters）**联动多个查询，
  并可像工作表一样按角色共享。
- 适合的场景：探查、运维看板、给业务方"最小可用报表"。
  不适合的：复杂交叉表、像素级排版、嵌入式门户——那是外部 BI 与 Streamlit 的地盘（见演进节）。

### 4. 可视化的成本与治理钩子
- 每次刷新图表/仪表盘都触发真实查询 → 消耗 credit（第 8 章）；
  仪表盘"定时刷新"若配在 XLARGE 仓库上就是烧钱器 ⚠️。
- 结果缓存（`USE_CACHED_RESULT`）让重复图表近乎免费（第 9/12 章实验用过同一开关 ✅ 实抓于 ch12）。
- 行列级安全在可视化下依然生效：图表只渲染查询返回的数据， masking/row policy 上游已裁（第 5 章）。

## 常见误区

| 误区 | 事实（转述 ⚠️） |
| --- | --- |
| "Snowsight 图表能替代 BI" | 探查/轻看板可以，企业级语义层与排版仍归外部 BI |
| "网页下载能拿到全部行" | 结果页/下载有行数与大小上限，全量要 UNLOAD 到 stage |
| "SAMPLE 和 LIMIT 一样" | LIMIT 是确定的头部行，SAMPLE 是随机样本（分布探查必须用后者） |
| "仪表盘刷新不花钱" | 刷新=重跑查询=烧 credit；缓存命中才便宜 |
| "共享工作表=共享数据" | 共享的是查询定义/看板，数据权限仍按查看者的角色与仓库判定 |
| "示例库是公共免费午餐" | SNOWFLAKE_SAMPLE_DATA 只读且查询照收算力费（数据免费、计算不免费） |

## 与其他章、其他书的联系

- 上下文四件套与 Snowsight 初印象 → [01-开始上手.md](01-开始上手.md)；结果页/下载与 UNLOAD → [06-数据加载与卸载.md](06-数据加载与卸载.md)。
- 缓存与结果复用 → [09-查询性能分析与优化.md](09-查询性能分析与优化.md)；仪表盘成本归因 → [08-账户成本管理.md](08-账户成本管理.md)。
- 示例库的跨区共享机制 → [10-安全数据共享.md](10-安全数据共享.md)。
- BI/多维视角的通识底图：[../数据仓库工具箱3.md](../数据仓库工具箱3.md)（Kimball 线）、
  [../数据库系统概念6/20-数据仓库与数据挖掘.md](../数据库系统概念6/20-数据仓库与数据挖掘.md)。
- 湖仓侧"谁来做分析层"的同题讨论：[../The_Data_Lakehouse/09-湖仓中的分析.md](../The_Data_Lakehouse/09-湖仓中的分析.md)。

## 核心概念速览（中英对照）

1. **Snowsight** — Snowflake 统一 Web 控制台：管理 + 开发 + 轻量 BI。
2. **工作表** — worksheet：多语句 SQL 编辑器，带角色/仓库/库/表上下文条。
3. **上下文四件套** — role / warehouse / database / schema context：UI 选择器与 `USE` 语句同义。
4. **结果集上限** — result page/download limits：网页端截断行为，全量导出走 UNLOAD ⚠️。
5. **随机抽样** — SAMPLE (n ROWS) / TABLESAMPLE SYSTEM (p)：分布探查取数法。
6. **图表** — charts：对查询结果集的可视化投影（X/Y 列 + 聚合）。
7. **仪表盘** — dashboards：多图表组件页 + 参数联动 + 角色共享。
8. **示例数据库** — sample databases：TPCH/TPCDS 只读公共库，算照计费。
9. **结果缓存** — result caching：重复查询免算力通道（`USE_CACHED_RESULT`）。
10. **嵌入式分析** — embedded analytics：把查询/看板嵌入外部应用（API/iframe ⚠️）。
11. **数据探查** — data profiling：抽样+统计先看数据形状再建模。

## 最新演进与工业实践

**可视化与应用面 2024–2026（URL 均 2026-09 curl 验证 200）：**

- **Snowsight 持续扩张**：工作表（https://docs.snowflake.com/en/user-guide/ui-snowsight-worksheets）、
  仪表盘（https://docs.snowflake.com/en/user-guide/ui-snowsight-dashboards）已成为默认管理面，
  Classic Console 退役；控制台整体文档 https://docs.snowflake.com/en/user-guide/ui-snowsight。
- **Streamlit in Snowflake**：用 Python 写数据应用、托管在账户内（官方：
  https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit ✅200）——
  书出版时为 preview ⚠️，现已是"比仪表盘更进一步的内部应用"标准答案。
- **AI 辅助分析**：Cortex 系把"问数"搬进 UI——Cortex AISQL（SQL 内调 LLM 函数，
  https://docs.snowflake.com/en/user-guide/snowflake-cortex/aisql ✅）、Cortex Agents
  （https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-agents ✅）、
  Snowflake Intelligence（对话式取数/洞察界面，
  https://docs.snowflake.com/en/user-guide/snowflake-cortex/snowflake-intelligence ✅）。
- **Summit 2025 公告**（自适应计算、Snowflake Intelligence 等）：
  https://www.snowflake.com/en/blog/announcements-snowflake-summit-2025/ ✅200。
- **工业实践**：2024–2026 团队常见分层——探查用工作表 + SAMPLE、内部轻看板用仪表盘、
  内部应用用 Streamlit、企业报表仍用外部 BI 直连（转述 ⚠️）；
  对照开放栈同题：[../The_Data_Lakehouse/09-湖仓中的分析.md](../The_Data_Lakehouse/09-湖仓中的分析.md)。
- ⚠️ 升级书稿须修正：本章截图级 UI 步骤时效性最差；行数上限、图表类型清单均以官方 UI 文档为准。

**文献与文档**
- 官方配套仓库 Chapter11.sql（章题、p.347–354 锚点、SAMPLE/LIMIT 语句、UI 练习声明 ✅ 实抓）
- Snowflake Docs — ui-snowsight / worksheets / dashboards / sample / about-streamlit / cortex 三件套 / Summit 2025 博客（上文 ✅200）
