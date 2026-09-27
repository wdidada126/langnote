# 02-SQL数据建模

> **对应章节**: Ch2 — SQL for Data Modeling
> **核心命题**: 用 SQL 实现维度建模——CTE、窗口函数、星型模型构建

---

## 2.1 SQL 在分析工程中的角色

### SQL 的三重身份

| 身份 | 说明 | 示例 |
|------|------|------|
| **查询语言** | 从仓库提取数据 | `SELECT * FROM orders WHERE ...` |
| **建模语言** | 定义数据变换逻辑 | `CREATE VIEW mart_orders AS ...` |
| **工程语言** | 可组合、可测试的代码单元 | dbt model = 一个 SQL 文件 |

✅ 分析工程的核心洞察：**SQL 不只是查询语言，它是数据建模的工程语言**。

---

## 2.2 CTE（Common Table Expressions）

### CTE 作为建模基石

dbt 模型的核心模式是 **CTE 链**——每个 `WITH` 块引用 `ref()` 或 `source()`：

```sql
WITH orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
),
customer_orders AS (
    SELECT customer_id, MIN(order_date) AS first_order,
           MAX(order_date) AS most_recent, COUNT(*) AS num_orders
    FROM orders GROUP BY 1
)
SELECT c.*, co.first_order, co.most_recent, co.num_orders
FROM {{ ref('stg_customers') }} c
LEFT JOIN customer_orders co ON c.customer_id = co.customer_id
```

✅ CTE 的价值：**将复杂查询分解为命名步骤**，每步可独立理解和测试。

### CTE vs 子查询 vs 临时表

| 方式 | 可读性 | 可复用 | dbt 兼容 |
|------|--------|--------|---------|
| CTE | ✅ 高 | 同查询内 | ✅ |
| 子查询 | ⚠️ 嵌套深时差 | 不可 | ✅ |
| 临时表 | ✅ 中 | 跨查询 | ⚠️ 不推荐 |

---

## 2.3 窗口函数在建模中的应用

### 常用窗口函数分类

| 类别 | 函数 | 建模用途 |
|------|------|---------|
| **排名** | `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()` | 去重、Top-N |
| **聚合** | `SUM() OVER()`, `COUNT() OVER()` | 运行总计、占比 |
| **偏移** | `LAG()`, `LEAD()` | 同比/环比计算 |
| **首尾** | `FIRST_VALUE()`, `LAST_VALUE()` | 状态变化检测 |

### 窗口函数实战：SCD Type 2

```sql
-- 检测客户地址变更（SCD Type 2 模式）
WITH ranked AS (
    SELECT
        customer_id,
        address,
        updated_at,
        LAG(address) OVER (PARTITION BY customer_id ORDER BY updated_at) AS prev_address,
        ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY updated_at) AS rn
    FROM {{ source('raw', 'customer_updates') }}
)
SELECT
    customer_id,
    address,
    updated_at AS valid_from,
    LEAD(updated_at) OVER (PARTITION BY customer_id ORDER BY updated_at) AS valid_to,
    CASE WHEN prev_address IS DISTINCT FROM address OR rn = 1
         THEN TRUE ELSE FALSE END AS is_new_record
FROM ranked
WHERE prev_address IS DISTINCT FROM address OR rn = 1
```

✅ 窗口函数是 dbt 模型中实现**缓慢变化维度（SCD）**的关键工具。

---

## 2.4 星型模型构建

### 事实表 + 维度表

```sql
-- fact_orders.sql
SELECT o.order_id, o.order_date, o.customer_id, o.product_id,
       oi.quantity, oi.unit_price,
       oi.quantity * oi.unit_price AS gross_amount
FROM {{ ref('stg_orders') }} o
JOIN {{ ref('stg_order_items') }} oi ON o.order_id = oi.order_id

-- dim_customers.sql
SELECT customer_id, first_name, last_name, email, created_at
FROM {{ ref('stg_customers') }}
```

✅ **星型模型 = 事实表（度量）+ 维度表（上下文）**，是 dbt 模型层的核心设计模式。

---

## 2.5 🔧 DuckDB / SQLite 类比（SQL 建模本地化）

| # | dbt/云仓库概念 | DuckDB 本地实现 | SQLite 本地实现 | 标注 |
|---|--------------|----------------|----------------|------|
| 1 | `ref()` 模型依赖链 | `CREATE VIEW model_b AS SELECT * FROM model_a` — VIEW 链模拟 ref 传递 | 同：`CREATE VIEW` 链 | 🔧 非本书引擎行为 |
| 2 | CTE 分层建模 | DuckDB 支持完整 CTE 语法，含递归 CTE | SQLite 3.8.3+ 支持 CTE，递归需显式声明 | 🔧 非本书引擎行为 |
| 3 | 窗口函数 SCD | DuckDB 完整支持窗口函数，含 `IGNORE NULLS` | SQLite 3.25+ 支持窗口函数 | 🔧 非本书引擎行为 |
| 4 | 星型模型 JOIN | DuckDB 自动优化列存 JOIN（向量化执行） | SQLite 行存，大表 JOIN 性能差 | 🔧 非本书引擎行为 |
| 5 | 质量检查 SQL | `SELECT COUNT(*) ... HAVING COUNT(*)>1` 完全兼容 | 同：标准 SQL 兼容 | 🔧 非本书引擎行为 |

> 🔧 以上均为**非本书引擎行为**——本书以 Snowflake/BigQuery/Redshift 为目标引擎。

---

## 2.6 性能考量

### SQL 建模性能最佳实践

| 实践 | 原因 |
|------|------|
| 尽早过滤 | `WHERE` 在 `JOIN` 之前减少数据量 |
| 避免 `SELECT *` | 列存仓库按列读取，只选需要的列 |
| CTE 物化时机 | 复杂 CTE 可考虑临时表（dbt 中用 intermediate 层） |
| 分区感知 | 查询带分区列的过滤条件 |
| 避免笛卡尔积 | 确保 JOIN 条件完整 |

⚠️ 不同仓库的优化器差异很大——Snowflake 的 CTE 会物化，BigQuery 的 CTE 会内联展开。

---

## 2.7 本章关键术语

| 英文 | 中文 | 定义 |
|------|------|------|
| CTE | 公共表表达式 | `WITH ... AS` 命名的临时结果集 |
| Window Function | 窗口函数 | 在分区内跨行计算的 SQL 函数 |
| Star Schema | 星型模型 | 事实表 + 维度表的建模模式 |
| Fact Table | 事实表 | 记录业务事件度量的表 |
| Dimension Table | 维度表 | 描述业务实体上下文的表 |
| SCD | 缓慢变化维度 | 处理维度数据随时间变化的策略 |
| Conformed Dimension | 一致性维度 | 跨多个事实表共享的维度 |

---

## 核心概念速览（中英对照）

| 中文概念 | English Term | 一句话定义 |
|---------|-------------|-----------|
| 公共表表达式 | Common Table Expression (CTE) | 用 WITH 子句定义的命名临时结果集 |
| 窗口函数 | Window Function | 在行分区上执行聚合/排名而不折叠行的函数 |
| 星型模型 | Star Schema | 以事实表为中心、维度表直接关联的建模模式 |
| 缓慢变化维度 | Slowly Changing Dimension (SCD) | 处理维度属性随时间变化的策略（Type 1/2/3） |
| 一致性维度 | Conformed Dimension | 跨多个事实表/数据产品共享的标准维度 |
| 分层建模 | Layered Modeling | Staging → Intermediate → Mart 的模型组织方式 |

---

## 最新演进与工业实践

| 时间 | 演进 | 影响 |
|------|------|------|
| 2022 | 本书出版 | CTE-first 建模风格成为 dbt 社区标准 |
| 2023 | DuckDB 0.8+ | 窗口函数性能大幅提升，本地建模成为可能 |
| 2024 | One Big Table 趋势 | 部分团队从星型转向 OBT，减少 JOIN |
| 2025 | AI SQL 生成 | Copilot 辅助 CTE 编写，但建模设计仍需人工 |
| 2026 | 列存格式演进 | Iceberg v3 + DuckDB 原生读取，模糊仓库/湖仓边界 |

> 📖 与 `../Data_Lakehouse_in_Action/`（#136）关联：
> - #136 Ch2 的分层模式 ↔ 本节 Staging → Intermediate → Mart
> - #136 的 Iceberg 表格式 ↔ dbt 外部表的底层存储选项
