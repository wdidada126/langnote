# 05 · Models

> Ch 5 pp 155–211 | DOI: 10.1007/979-8-8688-1844-8_5

---

## 学习目标

- 掌握 dbt 模型的四种物化方式及其适用场景
- 理解 `ref()` 函数构建 DAG 依赖
- 配置模型的 materialized / schema / tags 等属性
- 掌握增量模型 (incremental) 的策略与 `is_incremental()` 宏

---

## 5.1 物化方式总览

| 物化 | 仓库行为 | 适用场景 | 性能 |
|------|---------|---------|------|
| view | 创建视图 | staging / intermediate | 查询时计算 |
| table | 创建物理表 | marts / 频繁查询 | 预计算 |
| incremental | 增量合并 | 大数据量追加 | 仅处理新数据 |
| ephemeral | 不创建对象，CTE 注入 | 小型复用逻辑 | 编译时内联 |

> ✅ 物化可在 `dbt_project.yml`、模型 config block、或 schema.yml 中配置。

---

## 5.2 模型配置层级

```sql
-- 模型文件顶部 config block
{{ config(materialized='table', tags=['finance']) }}
SELECT ...
```

```yaml
# dbt_project.yml (项目级)
models:
  my_project:
    marts:
      +materialized: table
      +tags: ['marts']
```

```yaml
# schema.yml (模型级)
models:
  - name: fct_orders
    config:
      materialized: table
      tags: ['finance', 'orders']
```

> ✅ 优先级: 模型 config block > schema.yml > dbt_project.yml > 默认值

---

## 5.3 ref() 与依赖管理

```sql
SELECT * FROM {{ ref('stg_orders') }}
```

- `ref()` 做两件事: (1) 解析为完整表名 (2) 建立 DAG 依赖边
- dbt 编译器根据 `ref()` 自动推导执行顺序
- 支持同项目内任意模型间引用

---

## 5.4 增量模型深入

```sql
{{ config(materialized='incremental', unique_key='order_id') }}

SELECT
    order_id,
    customer_id,
    order_date,
    amount
FROM {{ source('jaffle_shop', 'orders') }}

{% if is_incremental() %}
WHERE order_date > (SELECT MAX(order_date) FROM {{ this }})
{% endif %}
```

### 增量策略

| 策略 | 行为 | 需要 unique_key |
|------|------|----------------|
| append (默认) | 直接 INSERT | 否 |
| merge | MERGE/UPSERT | 是 |
| delete+insert | 先删后插 | 是 |

> ⚠️ `unique_key` 可以是单列或列表 (v1.5+)，也支持复合键。

---

## 5.5 on_schema_change 配置

```sql
{{ config(
    materialized='incremental',
    unique_key='id',
    on_schema_change='sync_all_columns'
) }}
```

| 值 | 行为 |
|----|------|
| `ignore` | 不处理 schema 变化 (默认) |
| `append_new_columns` | 仅追加新列 |
| `sync_all_columns` | 同步新增/删除/类型变更 |
| `fail` | schema 变化时报错 |

---

## 5.6 模型别名与 Schema

```sql
{{ config(alias='customers_dim', schema='analytics') }}
```

- `alias`: 控制仓库中的实际表名
- `schema`: 覆盖 dbt_project.yml 中的 schema 映射

---

## 5.7 禁用模型

```yaml
# schema.yml
models:
  - name: deprecated_model
    config:
      enabled: false
```

> ✅ 禁用后 dbt 不会编译或执行该模型，但代码保留在仓库中。

---

## 5.8 批量运行与选择

```bash
dbt run --models stg_orders            # 单个模型
dbt run --models tag:finance           # 按 tag
dbt run --models +fct_orders           # 模型及其上游
dbt run --models fct_orders+           # 模型及其下游
dbt run --models +fct_orders+          # 上下游全部
dbt run --select staging.*             # 按目录
```

---

## 🔧 5.9 DuckDB / SQLite 类比

> 以下类比使用 DuckDB/SQLite 概念辅助理解，**非本书引擎行为**。

| # | dbt 概念 | DuckDB 类比 | SQLite 类比 |
|---|---------|-------------|-------------|
| 1 | view 物化 | DuckDB `CREATE VIEW` | SQLite `CREATE VIEW` |
| 2 | table 物化 | DuckDB `CREATE TABLE AS SELECT` | SQLite `CREATE TABLE AS SELECT` |
| 3 | incremental merge | DuckDB `MERGE INTO` (v1.9+) | SQLite `INSERT OR REPLACE` |
| 4 | ephemeral (CTE 注入) | DuckDB 嵌套 CTE | SQLite 嵌套 CTE |

---

## 核心概念速览（中英对照）

| 中文 | English | 一句话 |
|------|---------|--------|
| 物化方式 | Materialization | 模型在仓库中的存储策略 |
| 增量模型 | Incremental Model | 仅处理新增/变更数据 |
| 唯一键 | Unique Key | 增量 merge 的去重依据 |
| Schema 变更 | on_schema_change | 增量模型列结构变化时的处理 |
| 依赖引用 | ref() | 模型间引用并建立 DAG |
| 别名 | Alias | 仓库中的实际表名 |

---

## 最新演进与工业实践

- **dbt v1.8+ 增量模型重构**: 引入 `incremental_predicates` 和 `batch_size` 配置 ⚠️ [docs.getdbt.com/docs/build/incremental-models](https://docs.getdbt.com/docs/build/incremental-models)
- **dbt Fusion 引擎**: 增量 merge 在 Fusion 中利用列式优化，大表性能提升 ⚠️ [getdbt.com/blog/dbt-core-v1-11-is-ga](https://www.getdbt.com/blog/dbt-core-v1-11-is-ga)
- **Microbatch 策略** (v1.9+): 新的 `microbatch` 增量策略，按时间批次处理
- **`this` 对象增强**: 在增量查询中 `{{ this }}` 支持更多适配器
