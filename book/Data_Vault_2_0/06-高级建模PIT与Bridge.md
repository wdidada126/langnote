# 第 6 章 高级建模：PIT、Bridge、Reference（Advanced Data Vault Modeling）

> 目录取证：章题与 6.1 Point-in-Time Tables / 6.2 Bridge Tables / 6.3 Reference Tables ✅ 实抓自 Elsevier 官方 TOC。正文为精读重构；🔧 部分为本机 DuckDB 1.5.5 实测。

## 1. 本章定位：给三型装上「时间机器」和「展开器」

三型把「事实+历史」存了下来，但直接消费会痛：取「2015-01-10 该客户的等级」要手写多表时态 JOIN。本章三个结构各司其职：

- **PIT（Point-in-Time，时点表）**：任意时刻视图的物化/半物化——「时间机器」；
- **Bridge（桥接表）**：多对多结构（层级、组合、分摊）的展开器；
- **Reference（引用表）**：值域/码表，三型纪律的唯一豁免区。

## 2. 6.1 Point-in-Time 表（✅）

**定义**：`PIT_客户 = (hk_customer, load_dts)` × 若干颗卫星在 load_dts 时刻的「当前有效值」并排展平。构建法（书中/社区两代做法）：

1. 手工时态 JOIN：对每颗卫星取「不晚于 t 的最新一行」（2015 年在 SQL Server 上要写相关子查询或窗口函数，本章示例即此路线，⚠️ 原书 SQL 风格未逐条核）；
2. 物化 PIT（加载增量维护）vs 视图 PIT（读时计算）——与第 14 章「集市物化 vs 虚拟化」同一权衡。

🔧 实测（DuckDB 1.5.5）：DuckDB 的 **ASOF JOIN** 原生给出 PIT 语义——

```sql
SELECT b.bk, b.bdate, s.tier AS tier_asof_booking
FROM bookings b
ASOF JOIN sat_cust s
  ON s.hk = md5(b.cust) AND s.recsrc='CRM' AND s.ldts <= CAST(b.bdate AS TIMESTAMP);
-- 实测输出：B1→VIP(2015-01-10)  B2→STD(2015-02-10)  B3→VIP(2015-06-10, 早于07-01改PLAT)
```

三笔订单各自取到「下单时点」的等级，改级（VIP→PLAT，2015-07-01）不污染历史——PIT 的教学本质一行可证。2015 年本书要在 RDBMS 上手写窗口函数；今天 ASOF/time-travel 是引擎原语（DuckDB/Databricks `TIMESTAMP AS OF`/Snowflake Time Travel），PIT 正从「建模构件」退居「可移植视图」。

**PIT 的第二用途**（与第 14.5 节呼应）：数据质量审计——对账「报表答案当时用的哪版数据」，追溯争议口径。

## 3. 6.2 Bridge 表（✅）

**适用场景**：维度层级/组合关系在星型两端都要展开时——组织树滚总、持股穿透、机票 BOM 成本分摊。

- 结构：`Bridge(父键, 子键, 权重/深度, 有效区间)`；权重用于**可加性分摊**（1.0 的父指标按 0.6/0.4 分给子节点），纯滚总则权重恒 1。
- 与 Link 的分工：Bridge 是**集市层的展开结构**（信息出口侧），Link 是**Vault 层的关系本体**（事实侧）；Bridge 通常由 Link+PIT 生成，而非替代 Link。
- 经典陷阱：桥接双计（同一事实既在父又在子被 SUM）——必须带权重或在查询端 `WHERE depth=1`；层级历史变更必须由 PIT 决定「按哪个时点的树滚总」（时点快照 vs 历史归属两种口径），⚠️ 书中对该二选一的具体论述未核。

## 4. 6.3 Reference 表（✅）

- **定义**：值域/码表/枚举——等级、币种、舱位、状态机。允许直接以业务码为键（不必哈希、不建 Hub），是 Vault 内**唯一**非三型规范化豁免。
- **何时 Hub 何时 Reference**：会携带属性史、参与业务关系 → Hub；纯查表翻译 → Reference。
- **多源码值同化**：`R_LEVEL(等级码)` 挂 Satellite 式映射或用 same-as 语义把 CRM 的 `A` 与 ERP 的 `1` 归到同一标准值（第 13.7 标准化的落点之一）。
- 装载规则（第 12.2 专节）：Reference 表可以 UPDATE（它不是事实，是**字典**）——这是理解 Vault「不可变性边界」的关键反例。

## 5. 三结构与消费端的关系图

```text
Raw/Business Vault ──(HK+时态契约)──► PIT(hk, load_dts, 展平属性们)
                                  └─► Bridge(父,子,权重,区间)   ─► 信息集市星型（第7/14章）
Reference 表 ◄─ 键值翻译/码标准 ──┘
```

第 14 章的「虚拟化集市」= 直接把 PIT/Bridge 当维表和桥用；「物化集市」= 把 PIT/Bridge 展开成物理星型。本章只造机器，14 章决定卖整机还是卖散件。

## 5. PIT 的 2015 年写法 vs 引擎原语写法（同一语义三代方言）

```sql
-- ① 窗口函数折叠（书中年代的主战场：SQL Server/Oracle 手工件）
-- ① 相关子查询取「不晚于时点的最新行」（书中年代主战场：SQL Server/Oracle 手工件）
SELECT d.as_of, s.hk, s.name, s.tier
FROM pit_driver d                      -- (as_of, hk) 驱动集
JOIN sat_cust s ON s.hk = d.hk
 AND s.ldts = (SELECT MAX(s2.ldts) FROM sat_cust s2
               WHERE s2.hk = s.hk AND s2.ldts <= d.as_of);
-- ② ASOF JOIN（🔧 本目录 DuckDB 1.5.5 实测式，见 §2）
FROM bookings b ASOF JOIN sat_cust s ON s.hk=md5(b.cust) AND s.ldts<=CAST(b.bdate AS TIMESTAMP)
-- ③ 引擎时间旅行（Snowflake/Delta: SELECT ... AT/AS OF ... 配合 PIT 视图）——转述⚠️未实测
```

物化策略三分：全量物化（查询最快、每批重算）/增量维护（新 as-of 行才写，装载框架复杂度高一档）/纯视图（零存储、把成本推给每次读）。选择函数=读频×时点基数×引擎成本，与第 14 章物化/虚拟抉择同题。

## 6. Bridge 两例（重构演示）

**组织滚总（纯层级，权重恒 1）**：

```text
BRG_ORG(parent_org, child_org, depth, eff_from, eff_to)
  总部→A部→A1组   (depth 1/2)
查询「任意节点及其全部子孙的销售额」：
  SELECT p.parent_org, SUM(f.amount) FROM BRG_ORG p
  JOIN sales f ON f.org=p.child_org GROUP BY p.parent_org;   -- 权重全 1 时父=子和，无双计
```

**持股穿透（带权重，可加性分摊）**：`BRG_HOLD(comp, sub, weight=持股比例, eff区间)`；滚总时 `SUM(amount*weight)`，否则重复计入。「按哪个时点的树/股比」→ Bridge 外再包 PIT 选择（6.1×6.2 的组合件，也是 14.3 虚拟化的典型原料）。

## 7. Reference 表速写

```sql
CREATE TABLE R_CUST_TIER (tier_code_std VARCHAR PRIMARY KEY, tier_desc VARCHAR, sort_order INT);
CREATE TABLE R_CUST_TIER_SOURCE_MAP (tier_code_std, src_code, record_source, eff_from, eff_to);
-- 多源映射行本身带时态：源系统改码表时，历史翻译依然可复原
```

判据回顾：**会参与关系/带属性史 → Hub+卫星；纯翻译 → Reference；介于两者之间（如产品规格码）→ 倾向 Hub（宁滥勿缺在码表上同样成立，因为降级 Reference 后再升 Hub 要迁移所有 JOIN）。**（后半句为本目录经验口径 ⚠️）

## 8. FAQ

- **Q：PIT 和 SCD2 维表何者为准？** PIT 是骨干侧契约（可重算），集市 SCD2 是其物化投影；两派冲突时以 PIT 重算校验（14.5 的追溯能力来源）。
- **Q：Bridge 能不能干脆塞进维表（把层级拉平成列）？** 深度固定且浅（≤4）可拉平；深度漂移/多父（网状持股）必须 Bridge——Kimball 的层级处理与本节同一判断（对照 [../数据仓库工具箱3.md](../数据仓库工具箱3.md) 层级维度节）。
- **Q：哨兵值 9999-12-31 时区/精度坑？** 是——统一 UTC、统一 DATE/TIMESTAMP 类型、生成器模板里固化，别手写（湖仓引擎对 9999 年的支持不一，⚠️ 转述自社区踩坑帖）。

## 核心概念速览（中英对照）

- **时点表** — Point-in-Time (PIT) Table：卫星们「任意时刻当前值」的展平结构。
- **桥接表** — Bridge Table：多对多/层级结构的展开器，可带权重。
- **引用表** — Reference Table：值域字典，Vault 内非三型豁免区。
- **滚总** — Roll-up：沿层级向上聚合。
- **权重分摊** — Allocation Weight：父子间指标分配比例，防双计。
- **双计陷阱** — Double Counting：父子同时计入同一事实。
- **快照口径 vs 追溯口径** — Snapshot vs Retro-spective Attribution：层级/关系按发生时或按当前归属。
- **闭区间/开集** — Closed/Open Interval：PIT 时间轴两端语义（哨兵 9999-12-31）。
- **虚拟化集市** — Virtualized Mart：PIT/Bridge 直供 BI 不落星型。
- **物化** — Materialization：查询结果落成物理表。
- **可加性** — Additivity：事实能否跨维求和，桥接权重的前提。
- **ASOF JOIN** — As-of Join：按「不晚于时刻」匹配最近的时态行，DuckDB 原生。
- **时间旅行** — Time Travel：引擎级历史时点查询（Snowflake/Delta）。
- **码值同化** — Code Harmonization：多源枚举归一到标准值域。

## 最新演进与工业实践

- **PIT 的引擎化**：本目录实测的 DuckDB `ASOF JOIN`（1.5.5 🔧）与 Databricks/Snowflake 的 time travel + 流式快照读，让书中手工 PIT 的 SQL 复杂度大幅缩水；但 PIT 作为「可移植、可版本化的业务时点契约」仍保留在 dbt 模型层——AutomateDV 与 datavault4dbt 都把 PIT 作为一等公民宏/模板（https://github.com/Datavault-UK/automate-dv 、https://github.com/ScalefreeCOM/datavault4dbt ）。
- **dbtvault 的 PIT 表模式**：原 dbtvault（AutomateDV 前身）文档即以「PIT + Bridge = 集市虚拟层」为架构图核心，与本章叙事完全一致（历史文档站点已停更，⚠️ 现以 automate-dv.com 文档为准）。
- **Reference 表的当代形态**：小维表（static reference data）在湖仓侧有专门研究——C-Store/DSM 论文线对「广播小表」的处理可参 [../../db/db.md](../../db/db.md) 论文索引中列式/MPP 分支（⚠️ 系笔记类比，非本书引用）；工程上即 dbt 的 `static`/种子（seeds）机制。
- **语义层对 Bridge 的替代？**：2024–2026 指标语义层（dbt Semantic Layer、Cube、MetricFlow）让「层级滚总/分摊」部分转移到指标定义层，Bridge 退守到「非可加穿透」场景。观点梳理，无单一权威出处 ⚠️。
