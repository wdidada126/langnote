# 04 · Sources and Seeds

> Ch 4 pp 135–154 | DOI: 10.1007/979-8-8688-1844-8_4

---

## 学习目标

- 掌握 `sources.yml` 声明外部数据源的方法
- 理解 `source()` 宏与 `ref()` 的区别
- 学会使用 seeds 加载静态 CSV 数据
- 配置 source freshness 检查

---

## 4.1 Sources 声明

在 `models/` 目录下创建 `sources.yml`（或 `_sources.yml`）:

```yaml
version: 2

sources:
  - name: jaffle_shop        # 源系统名
    database: RAW             # 仓库中的 database
    schema: jaffle_shop_raw   # 仓库中的 schema
    description: "Jaffle Shop 原始数据"
    tables:
      - name: orders
        description: "订单表"
        columns:
          - name: id
            description: "主键"
          - name: user_id
            description: "客户 FK"
          - name: order_date
          - name: status
      - name: customers
        description: "客户表"
```

> ✅ source 声明不会创建任何数据库对象，仅是元数据注册。

---

## 4.2 在模型中引用 source

```sql
-- models/staging/stg_orders.sql
SELECT
    id AS order_id,
    user_id AS customer_id,
    order_date,
    status
FROM {{ source('jaffle_shop', 'orders') }}
```

编译后:
```sql
SELECT ... FROM RAW.jaffle_shop_raw.orders
```

### source() vs ref()

| 维度 | `source()` | `ref()` |
|------|-----------|---------|
| 引用对象 | 外部原始表 | dbt 内部模型 |
| 依赖关系 | 不建立 DAG 边 | 建立 DAG 边 |
| 用途 | 数据入口 | 模型间关联 |

---

## 4.3 Source Freshness

```yaml
sources:
  - name: jaffle_shop
    freshness:
      warn_after: {count: 12, period: hour}
      error_after: {count: 24, period: hour}
    loaded_at_field: _etl_loaded_at
    tables:
      - name: orders
      - name: customers
        freshness:
          warn_after: {count: 6, period: hour}
```

```bash
dbt source freshness    # 检查所有 source 新鲜度
```

> ✅ freshness 检查通过 `SELECT MAX(loaded_at_field)` 与阈值对比。

---

## 4.4 Seeds

Seeds 是存放在 `seeds/` 目录下的 CSV 文件，dbt 将其加载到仓库中。

```
seeds/
├── country_codes.csv
└── marketing_channels.csv
```

```bash
dbt seed          # 将 CSV 加载到仓库
dbt seed --full-refresh   # 全量重新加载
```

### 在模型中引用 seed

```sql
SELECT * FROM {{ ref('country_codes') }}
```

> ⚠️ seed 使用 `ref()` 而非 `source()`，因为 seed 是 dbt 管理的对象。

---

## 4.5 Seed 配置

```yaml
# dbt_project.yml
seeds:
  my_project:
    +column_types:
      id: integer
      country_code: varchar(2)
    marketing_channels:
      +schema: marketing   # 覆盖默认 schema
```

---

## 4.6 Source 与 Seed 的选择

| 场景 | 推荐方式 |
|------|---------|
| 外部系统持续灌入的数据 | Source |
| 小型静态查找表 (< 几万行) | Seed |
| 需要 freshness 监控 | Source |
| 手动维护的配置/映射表 | Seed |

---

## 4.7 Source 配置进阶

```yaml
sources:
  - name: jaffle_shop
    quoting:
      database: false
      schema: false
      identifier: false
    overrides: null    # dbt Mesh 中用于覆盖上游 source
```

> ⚠️ `overrides` 是 dbt Mesh 特性，详见 Ch 12。

---

## 🔧 4.8 DuckDB / SQLite 类比

> 以下类比使用 DuckDB/SQLite 概念辅助理解，**非本书引擎行为**。

| # | dbt 概念 | DuckDB 类比 | SQLite 类比 |
|---|---------|-------------|-------------|
| 1 | source 声明 (元数据注册) | DuckDB `INFORMATION_SCHEMA` 查询外部表 | SQLite `sqlite_master` 注册表 |
| 2 | source freshness 检查 | DuckDB `MAX(timestamp)` 查询 | SQLite `MAX()` 聚合检查 |
| 3 | seed (CSV→表) | DuckDB `COPY FROM 'file.csv'` | SQLite `.import file.csv` |
| 4 | seed column_types 配置 | DuckDB `CAST` 显式类型转换 | SQLite `typeof()` + 手动转换 |

---

## 核心概念速览（中英对照）

| 中文 | English | 一句话 |
|------|---------|--------|
| 数据源声明 | Source Definition | 注册外部原始表的元数据 |
| 源新鲜度 | Source Freshness | 监控数据是否按时到达 |
| 种子数据 | Seed | CSV 文件加载到仓库 |
| 加载时间字段 | loaded_at_field | freshness 检查的时间戳列 |
| 列类型覆盖 | Column Types Override | 控制 seed 列的数据类型 |

---

## 最新演进与工业实践

- **dbt Fusion 引擎**: source freshness 检查在 Fusion 中并行执行，大项目速度提升显著 ⚠️ [docs.getdbt.com/docs/dbt-versions/2025-release-notes](https://docs.getdbt.com/docs/dbt-versions/2025-release-notes)
- **Discovery API 查询 source 元数据**: 通过 GraphQL 获取 source 级血缘 ⚠️ [docs.getdbt.com/docs/dbt-cloud/using-dbt-cloud/cloud-discovery-api](https://docs.getdbt.com/docs/dbt-cloud/using-dbt-cloud/cloud-discovery-api)
- **dbt Mesh source overrides**: 跨项目场景下下游项目可覆盖上游 source 定义
- **动态 source 路径**: 通过 `env_var()` 实现多环境 source 切换
