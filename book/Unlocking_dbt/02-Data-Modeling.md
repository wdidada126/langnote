# 02 · Data Modeling

> Ch 2 pp 45–96 | DOI: 10.1007/979-8-8688-1844-8_2

---

## 学习目标

- 掌握维度建模 (Dimensional Modeling) 在 dbt 中的应用
- 理解 ODS → Staging → Intermediate → Marts 分层架构
- 区分星型模型 (Star Schema) 与雪花模型 (Snowflake Schema)
- 了解 Data Vault 与 One Big Table 等替代范式

---

## 2.1 数据建模范式概览

| 范式 | 核心思想 | dbt 适用场景 |
|------|---------|-------------|
| 维度建模 (Kimball) | 事实表 + 维度表 | 标准 marts 层 |
| Data Vault | Hub + Link + Satellite | 审计要求高的场景 |
| One Big Table (OBT) | 宽表反范式 | BI 自助分析 |
| Activity Schema | 活动为中心 | 事件驱动分析 |

> ✅ 本书主推 **Kimball 维度建模 + 分层架构**，这是 dbt 社区最主流的实践。

---

## 2.2 dbt 分层架构

```
[Sources]
    ↓
[Staging]        ← 1:1 映射源表，轻量清洗
    ↓
[Intermediate]   ← 复杂逻辑拆解，复用桥梁
    ↓
[Marts]          ← 业务消费层，面向 BI/DS
```

### 各层职责

- **Staging**: 类型转换、重命名列、过滤无效行；每个 source table 对应一个 staging model
- **Intermediate**: 拆解复杂逻辑、聚合到合适粒度、跨 marts 复用
- **Marts**: 按业务域组织 (customers, orders, products)；面向终端消费者

---

## 2.3 星型模型在 dbt 中的实现

```sql
-- dim_customers.sql (marts/dim_customers.sql)
SELECT
    customer_id,
    customer_name,
    region,
    segment,
    first_order_date,
    most_recent_order_date,
    lifetime_value
FROM {{ ref('stg_customers') }}
LEFT JOIN {{ ref('int_customer_metrics') }} USING (customer_id)
```

```sql
-- fct_orders.sql (marts/fct_orders.sql)
SELECT
    order_id,
    customer_id,        -- FK → dim_customers
    order_date,
    amount,
    status
FROM {{ ref('stg_orders') }}
```

---

## 🔧 2.4 DuckDB / SQLite 类比

> 以下类比使用 DuckDB/SQLite 概念辅助理解，**非本书引擎行为**。

| # | dbt 概念 | DuckDB 类比 | SQLite 类比 |
|---|---------|-------------|-------------|
| 1 | 分层物化 (staging→marts) | DuckDB 多 schema 分层 (`staging.`, `marts.`) | SQLite 多 database 分层 |
| 2 | ref() 构建依赖 DAG | DuckDB 视图链自动解析依赖顺序 | SQLite 视图依赖图 |
| 3 | 增量模型 (incremental) | DuckDB `INSERT OR REPLACE` + 合并逻辑 | SQLite `INSERT OR REPLACE` |
| 4 | 星型模型 join | DuckDB 列式存储高效 hash join | SQLite 行式 nested loop join |

---

## 2.5 缓慢变化维度 (SCD)

| 类型 | 策略 | dbt 实现 |
|------|------|---------|
| SCD Type 1 | 覆盖 | 直接 UPDATE / MERGE |
| SCD Type 2 | 新增行 | dbt **Snapshots** (Ch 6) |
| SCD Type 3 | 新增列 | 手动 ALTER TABLE |

> ✅ dbt Snapshots 是 SCD Type 2 的声明式实现，详见 Ch 06。

---

## 2.6 粒度与一致性

- **声明粒度**: 每个 model 必须在注释中声明粒度 (grain)
- **避免混合粒度**: 一个 model 不应同时包含不同粒度的数据
- **一致性维度**: 跨 marts 共享维度表，保证 join 一致

---

## 2.7 命名约定

| 层 | 前缀 | 示例 |
|----|------|------|
| Staging | `stg_` | `stg_orders`, `stg_customers` |
| Intermediate | `int_` | `int_order_items` |
| Marts (事实) | `fct_` | `fct_orders` |
| Marts (维度) | `dim_` | `dim_customers` |

---

## 核心概念速览（中英对照）

| 中文 | English | 一句话 |
|------|---------|--------|
| 维度建模 | Dimensional Modeling | Kimball 事实+维度 |
| 分层架构 | Layered Architecture | staging → intermediate → marts |
| 星型模型 | Star Schema | 事实表居中，维度表环绕 |
| 缓慢变化维度 | Slowly Changing Dimension (SCD) | 处理维度属性变化 |
| 粒度 | Grain | 一行数据代表什么 |
| 一致性维度 | Conformed Dimension | 跨主题域共享 |

---

## 最新演进与工业实践

- **dbt Mesh 对建模的影响**: 跨项目共享 marts 层模型，团队各自拥有独立 dbt 项目 ⚠️ 详见 Ch 12
- **Semantic Layer 与建模**: 指标定义从 SQL 模型解耦到语义层 (Ch 13)
- **dbt Fusion 引擎**: 编译和执行分离，大项目编译速度提升显著 ⚠️ [getdbt.com/blog/dbt-core-v1-11-is-ga](https://www.getdbt.com/blog/dbt-core-v1-11-is-ga)
- **AI 辅助建模**: dbt Cloud Copilot 可辅助生成 staging model SQL
