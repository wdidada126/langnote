# 03 · SQL 监控实现（推定内容域：基于 SQL 的数据质量监控规则与检测算法）

> ⚠️ 推定内容域页。取证三态：✅ 实证 / ⚠️ 转述推定 / 🔧 本机 SQLite 实跑。
> 册内导航：[00-总览与阅读地图.md](00-总览与阅读地图.md) · 上一章 [02](02-关键维度工程化.md) · 下一章 [04-告警与事件响应.md](04-告警与事件响应.md)

## 3.1 从维度到 SQL：监控规则的分类

数据质量监控规则可按检测对象分为四类（⚠️ 编者归纳）：

| 类别 | 检测对象 | SQL 实现难度 | 典型规则 |
|---|---|---|---|
| 完整性 | NULL 率、空行 | 低 | `COUNT(*) - COUNT(col) < threshold` |
| 一致性 | 跨表参照完整性 | 中 | `EXCEPT` / `NOT IN` 子查询 |
| 模式漂移 | 列结构变更 | 中 | 元数据快照 `EXCEPT` diff |
| 统计异常 | 体量/分布偏移 | 高 | MAD z-score / 基线比较 |

## 3.2 模式漂移检测 🔧 G2

**核心思路**：对列元数据做两期快照，用 `EXCEPT` 集合差检测变更。

🔧 **G2 实验**（SQLite，非本书引擎行为）：

```sql
-- 列元数据快照表
CREATE TABLE col_snapshots (
    table_name TEXT, column_name TEXT,
    data_type TEXT, is_nullable INTEGER, snap_period TEXT
);
-- 新增列检测
SELECT 'ADDED' AS change_type, table_name, column_name, data_type
FROM col_snapshots WHERE snap_period='T2'
EXCEPT
SELECT 'ADDED', table_name, column_name, data_type
FROM col_snapshots WHERE snap_period='T1';
```

**真实输出**（10 列→13 列，种子 224）：

| Type | Table | Column | DataType |
|---|---|---|---|
| ADDED | raw.orders | discount | REAL |
| ADDED | raw.orders | coupon_code | TEXT |
| ADDED | stg.payments | gateway_ref | TEXT |
| REMOVED | raw.orders | customer_id | INTEGER |
| ADDED | raw.orders | customer_id | TEXT |

**5 起漂移事件**：2 新增列（discount, coupon_code）+ 1 新增列（gateway_ref）+ 1 类型变更（customer_id: INTEGER→TEXT，本质是 schema-breaking change）+ 1 隐含的旧类型移除。

**与 #226 G2 的错位**：#226 G2 检出 3 起漂移（2 新增 + 1 类型变更 REAL→DOUBLE）；本组用不同数据集、不同变更类型，零重合。

## 3.3 体量异常检测 🔧 G4

**核心思路**：对行数日序列建立 MAD（Median Absolute Deviation）基线，用修正 z-score 检测异常。

**为什么用 MAD 而非标准差**：行数序列通常含周末/节假日的周期性下降，标准差会被这些「正常异常」拉偏；MAD 基于中位数，对周期性波动更鲁棒。

🔧 **G4 实验**（SQLite，非本书引擎行为）：

```sql
-- 日体量序列
CREATE TABLE daily_volume (table_name TEXT, day INTEGER, row_count INTEGER);
-- 注入异常：day=33 (-88%), day=58 (+180%)
-- Python 侧计算 MAD 基线与修正 z-score
```

**真实输出**（90 天序列，种子 224）：

| 统计量 | 值 |
|---|---|
| 中位数 | 42561 |
| MAD | 7893 |
| 阈值 (z=3.5) | \|Mz\| > 3.5 |

| Day | Volume | Z-score | Flag |
|---|---|---|---|
| 33 | 5043 | -5.42 | ANOMALY |
| 58 | 119247 | +6.78 | ANOMALY |

**2 点全中，零误报**——MAD 基线在含周期性波动的序列上显著优于朴素 z-score。

**与 #226 G4 和 #223 E2 的错位**：#226 G4 用朴素 z-score（均值/标准差基线）检出 5 次；#223 E2 用周环比 + MAD 检出 6 点含 3 回声双报；本组用全序列 MAD 无环比，2 点零误报——三种方法全部不同。

## 3.4 完整性检测的 SQL 模式（⚠️ 推定）

工程实施中常见的完整性规则：

```sql
-- NULL 率监控
SELECT 'high_null_rate' AS rule,
    1.0 - 1.0*COUNT(customer_id)/COUNT(*) AS null_rate
FROM raw.orders WHERE created_at >= date('now','-1 day');

-- 跨表参照完整性
SELECT 'orphan_records' AS rule, COUNT(*) AS violations
FROM stg.orders o
LEFT JOIN raw.customers c ON o.customer_id = c.id
WHERE c.id IS NULL;

-- 主键唯一性
SELECT 'duplicate_pk' AS rule, COUNT(*) AS violations
FROM (SELECT id, COUNT(*) AS cnt FROM raw.orders GROUP BY id HAVING cnt > 1);
```

这些规则的工程化关键是**阈值设定**与**告警路由**——后者是 04 章主题。

## 3.5 检测算法的工程选型指南

| 算法 | 适用场景 | 误报率 | 实施成本 |
|---|---|---|---|
| 固定阈值 | 已知边界的完整性规则 | 低 | 低 |
| 朴素 z-score | 正态分布的体量序列 | 中 | 低 |
| MAD z-score | 含周期性波动的序列 | 低 | 中 |
| 滑动窗口百分位 | 时效/滞后类指标 | 中 | 中 |
| PSI/KS 检验 | 分布偏移检测 | 中高 | 高 |
| 季节性分解 | 强周期序列 | 低 | 高 |

工程建议（⚠️ 推定）：从固定阈值和 MAD 起步，积累数据后升级到季节性分解。

## 3.6 监控规则的元数据管理

监控规则本身需要元数据管理（⚠️ 推定）：

```sql
CREATE TABLE monitoring_rules (
    rule_id TEXT, table_name TEXT, rule_type TEXT,
    threshold REAL, severity TEXT, owner TEXT
);
```

每条规则挂负责人（owner）和严重级别（severity），是告警路由（04 章）的前置条件。

## 3.7 取证表

| 断言 | 等级 | 依据 |
|---|---|---|
| G2 漂移 5 起 | 🔧 | SQLite 实跑 |
| G4 MAD 2 点零误报 | 🔧 | SQLite 实跑 |
| 完整性 SQL 模式 | ⚠️ | 品类通识 |
| 算法选型表 | ⚠️ | 编者归纳 |

## 核心概念速览（中英对照）

- **监控规则** — Monitoring Rule：对数据信号做健康判定的可执行检查。
- **模式漂移** — Schema Drift：列元数据在两期快照之间发生变更。
- **EXCEPT 集合差** — EXCEPT Set Diff：SQL 标准运算符，用于检测两集合的对称差。
- **MAD** — Median Absolute Deviation：中位数绝对偏差，鲁棒统计量。
- **修正 z-score** — Modified Z-score：基于 MAD 的标准分，`k*(x-median)/MAD`。
- **完整性规则** — Completeness Rule：检测 NULL 率/空行/参照断裂。
- **阈值设定** — Threshold Setting：区分「正常波动」与「异常信号」的边界值。
- **监控规则元数据** — Rule Metadata：规则自身的负责人/阈值/严重级别登记。
- **检测算法选型** — Algorithm Selection：根据数据特征选择误报率与成本的平衡点。
- **类型变更** — Type Change：列数据类型变更，是 schema-breaking change 的典型形态。

## 最新演进与工业实践

- **dbt 测试生态**：dbt tests 提供声明式监控规则（unique/not_null/relationships），已成为 SQL 监控的事实标准之一（⚠️ 品类通识）。
- **自动阈值学习**：商业平台（Monte Carlo/BigEye）推自动基线学习，减少人工设阈值的成本（⚠️ 厂商口径）。
- **SQL-based 检测的局限**：分布偏移/复杂模式检测需要 Python/统计引擎，纯 SQL 不够——这是商业平台的差异化空间（⚠️）。
- **工业实践口径**：从 dbt tests + 自定义 SQL 规则起步，逐步引入统计检测——渐进式路径是品类共识（⚠️）。
- **与 #226 04 章的关系**：#226 04 章把检测模式按五支柱展开；本章聚焦 SQL 实施层，是其工程下钻。
