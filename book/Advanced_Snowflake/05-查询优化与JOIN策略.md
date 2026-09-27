# 05 · 查询优化与 JOIN 策略（⚠️ 推定主题章，任务书 ★ 关键词）

> **性质声明**：推定主题重构（[00](00-总览与阅读地图.md)）。机制=官方文档转述（⚠️）+✅URL；
> 🔧 JOIN 类比用 DuckDB 1.5.5（**非 Snowflake 行为**，Snowflake 执行器细节不可连测）。
> TDG 对位：[../Snowflake_The_Definitive_Guide/09-查询性能分析与优化.md](../Snowflake_The_Definitive_Guide/09-查询性能分析与优化.md) §4。

## 本章地图

| 节 | 内容 | 一句话结论 |
| --- | --- | --- |
| 5.1 | 优化器输入面：统计+值域+无分桶 | "看不见分布"时人怎么帮忙 |
| 5.2 | 诊断三件套：EXPLAIN/Query Profile/历史视图 | 计划是假设，Profile 是证词 |
| 5.3 | JOIN 形态学：广播/分区/shuffle 的云上变体 | Snowflake 用全集群 hash：build 侧选择是核心 |
| 5.4 | 倾斜与放大：数据倾斜 vs 重复键放大 | 行数变化是最诚实的诊断信号 |
| 5.5 | 半连接/反连接惯用法 | EXISTS/NOT IN/QUALIFY 的成本语义 |
| 5.6 | 谓词卫生：SARGable、隐式转换、函数包裹 | 裁剪失效三大杀手 |
| 5.7 | QAS 与仓库外溢 | 优化到头后用弹性兜底 |
| 5.8 | 🔧 类比：小维哈希 join vs 重复键放大 | 3ms vs 5ms、27400 vs 2750 行 |

## 核心精讲

### 1. 优化器的信任链（转述 ⚠️）
列统计（自动维护，AUTO_ANALYZE）+微分区值域共同喂给代价模型；**没有用户级分布统计**（无分桶/
分区声明），所以人的介入方式是：布局（3/4 章）、谓词形态（5.6）、以及**用 Profile 复核计划假设**。
✅ https://docs.snowflake.com/en/user-guide/tables-clustering-micropartitions （统计供给侧，第 3 章已证）

### 2. 诊断三件套（转述 ⚠️）
- `EXPLAIN`：编译期计划（行数/代价是估算值）；
- **Query Profile（Snowsight）**：运行时逐节点真实统计（rows produced、fan-out、内存/磁盘溢出
  标记），问题行高亮；✅ https://docs.snowflake.com/en/user-guide/ui-snowsight-activity
- `QUERY_HISTORY`/`QUERY_HISTORY_BY_SESSION` + `QUERY_ATTEMPTS` 等账户视图定位 TOP 消耗。
  ✅ https://docs.snowflake.com/en/sql-reference/account-usage/warehouse_metering_history （计量侧对偶）
MySQL 肌肉记忆迁移：[../mysql/15-EXPLAIN详解.md](../mysql/15-EXPLAIN详解.md)、
[../mysql/16-optimizer-trace.md](../mysql/16-optimizer-trace.md)。教科书：
[../数据库系统概念6/12-查询处理.md](../数据库系统概念6/12-查询处理.md)、
[../数据库系统概念6/13-查询优化.md](../数据库系统概念6/13-查询优化.md)。

### 3. JOIN 策略在"全集群共享存储"下的形态（转述 ⚠️）
所有节点可见全部微分区 → 传统 MPP 的"DISTKEY 共置避免 shuffle"问题被平台接管；人侧残留下三题：
1. **build/probe 侧**：小维表应先到——`WHERE` 谓词早过滤（本引擎对过滤后行数的估计依赖统计质量）；
2. **JOIN 键的裁剪友好度**：键列聚簇/搜索优化决定两侧扫描量（✅ search-optimization/join-queries，
  第 4 章已证 200）；
3. **形态选择**：等值 hash、`QUALIFY ROW_NUMBER()` 去重、`LEFT ANTI`（官方惯用反连接写法 ⚠️）。
参考 SQL 惯用法（教学示意，非书中原文）：
```sql
SELECT /*+ */ t.* FROM trades t
LEFT ANTI JOIN cancels c ON t.id = c.id          -- 反连接：未成交集合
WHERE t.dt = '2026-09-27';
```

### 4. 倾斜与放大（转述 ⚠️ + 🔧直觉）
- **重复键放大**：维表 JOIN 键不唯一 → 结果行数 fan-out（Profile 中 rows produced 激增即此病）；
- **值倾斜**：单值热点使某节点超载（多集群救不了单查询 → 键盐/两阶段聚合是 SQL 侧解法 ⚠️）。

### 5. 🔧 本地镜像实验（DuckDB 1.5.5，**非 Snowflake 行为**）
4,000,000 行 fact（cust_id∈[0,1000)）分别 JOIN：
(a) 1,000 行唯一键维表；(b) 50 行、每键重复约 17 次的"放大维表"（`i%3`），两侧同谓词 `d_days<5`：
| 场景 | 用时（🔧） | 结果行数 |
| --- | --- | --- |
| 小维哈希 join | **3 ms** | 27,400 |
| 重复键放大 | **5 ms** | **2,750（1/10 行却更慢）** |
EXPLAIN 显示 `HASH_JOIN` 且过滤在扫描侧完成（build 侧被裁小的机制演示）。读法：**行数不是 JOIN
成本的可靠代理，键的重复度才是**——这正是 Query Profile 里 fan-out 检查的原型。
（脚本 E4。）

### 6. 谓词卫生清单（转述 ⚠️）
列上避免：函数包裹（`TO_DATE(col)>…`→改常量侧）、隐式类型转换（VARCHAR 键 JOIN BIGINT 键）、
`LIKE '%x%'`（改用搜索优化或第 6 章变体）。每条都会把第 3 章的裁剪打回全扫。

### 7. QAS 兜底（转述 ⚠️）
优化穷尽后的突发尖峰交给 Query Acceleration Service（外溢共享算力，按秒计费、可设上限）。
✅ https://docs.snowflake.com/en/user-guide/query-acceleration-service
✅ https://docs.snowflake.com/en/user-guide/performance-explorer

## 常见误区

| 误区 | 事实（转述 ⚠️） |
| --- | --- |
| "EXPLAIN 好看就收工" | 估卡可能全错，必须用运行时 Profile 复核 |
| "JOIN 慢就加大仓库" | 先查放大与键裁剪，尺寸救不了坏计划 |
| "维表小就不用管" | 小而不唯一=放大源；小且热点=单查询长尾 |
| "NOT IN 子查询没坑" | NULL 语义陷阱+反连接形态差异，优先 LEFT ANTI/NOT EXISTS |
| "统计是黑话" | 列统计与值域是估卡与裁剪的共同供给，AUTO_ANALYZE 别关 |

## 与其他章、其他书的联系

- 上游：布局与索引侧杠杆 → [03-微分区与裁剪引擎.md](03-微分区与裁剪引擎.md)、[04-聚簇与搜索优化.md](04-聚簇与搜索优化.md)；
  下游：优化→账单裁决 → [02-成本模型与计费内核.md](02-成本模型与计费内核.md)；
  半结构化上的 JOIN → [06-VARIANT与半结构化数据.md](06-VARIANT与半结构化数据.md)。
- 入门对读：TDG-09 §4/§6。
- 谱系对照：Trino 的 JOIN 分布策略（co-partitioning/broadcast 显式控制）→
  [../Trino_The_Definitive_Guide_2e/00-总览与阅读地图.md](../Trino_The_Definitive_Guide_2e/00-总览与阅读地图.md)
  ——"平台接管 vs 人肉声明"的另一极；执行算子通识 → [../Database_Internals/00-总览与阅读地图.md](../Database_Internals/00-总览与阅读地图.md)。
- 【登记·同波不链】Redshift DISTSTYLE/DISTKEY JOIN 共置深对照，波尾挂 `Amazon_Redshift_TDG`。

## 核心概念速览（中英对照）

1. **执行计划** — EXPLAIN：编译期假设（估卡/估行），仅供起点。
2. **查询画像** — Query Profile：运行时节点级真实统计，诊断主证据。
3. **行数放大** — fan-out：JOIN 键重复导致 rows produced 激增。
4. **构建侧** — build side：hash join 中先被物化的一侧，越小越好。
5. **反连接** — LEFT ANTI JOIN：官方惯用"未匹配集合"形态，优于 NOT IN+NULL 陷阱。
6. **QUALIFY** — 窗口结果过滤子句：去重取最新的标准件。
7. **SARGable** — 可参数化搜索谓词：裁剪能用的谓词形态。
8. **隐式转换** — implicit cast：类型不匹配键 JOIN 的裁剪杀手。
9. **值倾斜** — data skew：热点单值使并行度失效。
10. **查询加速服务** — QAS：突发外溢算力兜底（第 2 章计费联动）。
11. **查询历史视图** — QUERY_HISTORY：TOP 消耗与归因的数据源。
12. **哈希连接** — hash join（🔧类比物）：DuckDB EXPLAIN 中观测到的形态，非 Snowflake 实证。

## 最新演进与工业实践

**2024–2026（URL 均 2026-09-27 curl -L 实测 200 ✅）：**

- **观测面升级**：Performance Explorer/CoCo 把"JOIN 画像/倾斜体检"产品化
  （✅ performance-explorer、analyze-workload-performance-coco），替代社区自写 ACCOUNT_USAGE 脚本的趋势。
- **执行引擎持续演进**：官方工程博客列近年改进（自适应并行/计划形状），细节以页内为准
  ✅ https://www.snowflake.com/en/engineering-blog/sql-performance-improvements-2026/ （前波 TDG-09 已验证；本波复核沿用其口径 ⚠️）。
- **JOIN 键搜索优化**（✅ search-optimization/join-queries）代表 2025+ "索引补课 SQL 性能"的官方路线。
- **工业实践 ⚠️（转述）**：查询评审清单三问——裁剪命中了吗/放大发生了吗/倾斜存在吗——
  对应本章三节；压测纪律 `USE_CACHED_RESULT=FALSE`（TDG-12 实抓惯例）仍是社区基线。
- 🔧 复现：E4 实验可作为"fan-out 诊断"内训素材（明确声明 DuckDB 类比）。

**文献与文档**：ui-snowsight-activity / query-acceleration-service / performance-explorer /
warehouse_metering_history / search-optimization/join-queries / engineering-blog SQL 性能页（✅200）；
🔧 experiments.py E4。
