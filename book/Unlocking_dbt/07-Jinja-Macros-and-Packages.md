# 07 · Jinja, Macros, and Packages

> Ch 7 pp 243–282 | DOI: 10.1007/979-8-8688-1844-8_7

---

## 学习目标

- 掌握 Jinja 模板语言在 dbt 中的核心用法
- 编写和复用宏 (Macros)
- 理解 dbt 包生态系统与常用包
- 掌握 `dbt_utils` 等社区包的实用功能

---

## 7.1 Jinja 基础

Jinja 是 Python 模板引擎，dbt 用它实现 SQL 的动态生成。

### 变量与控制流

```sql
-- 变量
{{ var('payment_methods', ['credit_card', 'bank_transfer']) }}

-- 条件
{% if target.name == 'prod' %}
WHERE created_at >= '2020-01-01'
{% else %}
WHERE created_at >= current_date - interval '30 days'
{% endif %}

-- 循环
{% for method in var('payment_methods') %}
    SUM(CASE WHEN payment_method = '{{ method }}' THEN amount ELSE 0 END)
        AS {{ method }}_amount
    {% if not loop.last %},{% endif %}
{% endfor %}
```

---

## 7.2 宏 (Macros)

宏是 Jinja 中可复用的 SQL 片段，类似函数。

```sql
-- macros/cents_to_dollars.sql
{% macro cents_to_dollars(column_name, precision=2) %}
    ({{ column_name }} / 100)::numeric(16, {{ precision }})
{% endmacro %}
```

使用:
```sql
SELECT order_id, {{ cents_to_dollars('amount') }} AS amount_dollars
FROM {{ ref('stg_orders') }}
```

### 宏的存放与命名

- 放在 `macros/` 目录下，文件名即宏包名
- 跨包宏: `{{ dbt_utils.star(ref('my_model')) }}`

---

## 7.3 常用内置 Jinja 对象

| 对象 | 说明 | 示例 |
|------|------|------|
| `ref()` | 引用模型 | `{{ ref('stg_orders') }}` |
| `source()` | 引用源表 | `{{ source('raw', 'orders') }}` |
| `config()` | 模型配置 | `{{ config(materialized='table') }}` |
| `this` / `target` | 当前模型/target | `{{ this }}`, `{{ target.name }}` |
| `var()` / `env_var()` | 项目/环境变量 | `{{ var('my_var') }}` |
| `modules` | Python 模块 | `{{ modules.datetime.date.today() }}` |

---

## 7.4 生成器 (Generators)

```sql
-- macros/staging.sql
{% macro generate_staging_model(source_name, table_name) %}
SELECT
    {% set cols = adapter.get_columns_in_relation(source(source_name, table_name)) %}
    {% for col in cols %}
        {{ col.name }}{{ "," if not loop.last }}
    {% endfor %}
FROM {{ source(source_name, table_name) }}
{% endmacro %}
```

---

## 7.5 dbt 包生态

| 包名 | 用途 |
|------|------|
| `dbt-labs/dbt_utils` | 通用宏与测试 (star, group_by, pivot) |
| `calogica/dbt_expectations` | 数据质量测试 (正则、分布、时序) |
| `dbt-labs/codegen` | 自动生成 schema.yml 和 staging SQL |
| `dbt-labs/dbt_external_tables` | 管理外部表 (S3, GCS) |

### packages.yml

```yaml
packages:
  - package: dbt-labs/dbt_utils
    version: "1.1.1"
  - package: dbt-labs/codegen
    version: "0.12.1"
```

```bash
dbt deps    # 安装到 dbt_packages/
```

---

## 7.6 dbt_utils 精选宏

```sql
-- star(): 选择所有列 (可排除/重命名)
SELECT {{ dbt_utils.star(ref('stg_orders'), except=['_etl_id']) }}
FROM {{ ref('stg_orders') }}

-- group_by(): 按列分组
SELECT status, COUNT(*)
FROM {{ ref('stg_orders') }}
{{ dbt_utils.group_by(1) }}

-- surrogate_key(): 生成复合主键 hash
SELECT {{ dbt_utils.surrogate_key(['order_id', 'product_id']) }} AS sk
```

---

## 7.7 自定义测试宏

```sql
-- macros/test_positive_value.sql
{% test positive_value(model, column_name) %}
SELECT * FROM {{ model }} WHERE {{ column_name }} < 0
{% endtest %}
```

在 schema.yml 中使用:
```yaml
models:
  - name: fct_orders
    columns:
      - name: amount
        tests:
          - positive_value
```

---

## 🔧 7.8 DuckDB / SQLite 类比

> 以下类比使用 DuckDB/SQLite 概念辅助理解，**非本书引擎行为**。

| # | dbt 概念 | DuckDB 类比 | SQLite 类比 |
|---|---------|-------------|-------------|
| 1 | Jinja 宏 | 无对应（需外部脚本生成 SQL） | 无对应 |
| 2 | dbt_utils.star() | `SELECT * EXCLUDE (...)` (v0.9+) | 需手动列举列 |
| 3 | surrogate_key() | `MD5(col1 \|\| col2)` | `MD5(col1 \|\| col2)` (需扩展) |
| 4 | packages.yml | 无包管理（需手动下载扩展） | 扩展需手动 `.load` |

---

## 核心概念速览（中英对照）

| 中文 | English | 一句话 |
|------|---------|--------|
| 宏 | Macro | 可复用的 SQL 模板函数 |
| Jinja 模板 | Jinja Templating | SQL 动态生成引擎 |
| 包 | Package | 可复用的宏/测试集合 |
| 项目变量 | var() | 运行时可配置的变量 |
| 生成器 | Generator | 动态生成 SQL 片段的宏 |
| 依赖管理 | dbt deps | 安装 packages.yml 中的包 |

---

## 最新演进与工业实践

- **dbt v1.9+ 宏作用域增强**: 包中的宏可通过 `dispatch` 机制按适配器覆盖 ⚠️ [docs.getdbt.com/docs/build/packages](https://docs.getdbt.com/docs/build/packages)
- **dbt_utils 持续更新**: v1.3+ 新增 `safe_cast`、`date_spine` 等宏
- **AI 辅助宏生成**: dbt Cloud Copilot 可根据描述生成宏代码
- **Fusion 引擎**: Jinja 编译速度在 Fusion 中大幅提升，大项目受益明显 ⚠️ [getdbt.com/blog/dbt-core-v1-11-is-ga](https://www.getdbt.com/blog/dbt-core-v1-11-is-ga)
