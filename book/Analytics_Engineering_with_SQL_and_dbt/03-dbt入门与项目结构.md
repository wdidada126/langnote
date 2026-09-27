# 03-dbt入门与项目结构

> **对应章节**: Ch3 — Introduction to dbt
> **核心命题**: dbt 架构、项目结构、CLI 工作流、Jinja 模板基础

---

## 3.1 dbt 是什么？

```
dbt = SQL 编译器 + 依赖引擎 + 测试框架 + 文档生成器
```

| 功能 | 说明 | 类比 |
|------|------|------|
| **SQL 编译** | Jinja + SQL → 可执行 SQL | 模板引擎（Jinja2） |
| **依赖管理** | `ref()` 自动构建 DAG | 构建工具（Make/CMake） |
| **测试框架** | YAML 声明式数据质量测试 | 单元测试框架（pytest） |
| **文档生成** | 自动生成模型文档网站 | 代码文档（Javadoc/Sphinx） |

✅ dbt 的本质：**把 SQL 从脚本提升为工程化的代码项目**。

### dbt-core vs dbt Cloud

| 维度 | dbt-core (OSS) | dbt Cloud |
|------|---------------|-----------|
| **部署** | 本地/自建 | SaaS |
| **调度** | 需外部（Airflow） | 内置 |
| **IDE** | 本地编辑器 | 浏览器 |
| **费用** | 免费 | 按席位收费 |

⚠️ 2026 年 dbt Cloud 已成为主流选择。

---

## 3.2 安装与环境

```bash
pip install dbt-core dbt-duckdb   # 🔧 DuckDB 适配器用于本地学习
```

```yaml
# profiles.yml — my_project 连接 DuckDB 本地库
my_project:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: './analytics.duckdb'
```

⚠️ pip 安装可能因依赖冲突失败；若无法安装，通过 [docs.getdbt.com](https://docs.getdbt.com) ✅ 在线学习概念。
> 🔧 dbt-duckdb 是社区适配器，**非本书引擎行为**。

---

## 3.3 项目结构

```
my_dbt_project/
├── dbt_project.yml      # 项目配置（名称、版本、模型路径）
├── profiles.yml         # 连接配置（通常在 ~/.dbt/）
├── packages.yml         # 依赖包声明
├── models/              # SQL 模型（staging/ intermediate/ marts/）
├── tests/               # 自定义数据测试
├── macros/              # Jinja 宏（可复用 SQL 片段）
├── seeds/               # CSV 种子数据
├── snapshots/           # SCD Type 2 快照
└── target/              # 编译产物（自动生成）
```

✅ **目录即分层**——dbt 项目的目录结构直接映射数据建模的分层架构。

---

## 3.4 dbt_project.yml 核心配置

```yaml
name: 'analytics'
version: '1.0.0'
config-version: 2
profile: 'analytics'

models:
  analytics:
    staging:
      +materialized: view
    intermediate:
      +materialized: ephemeral
    marts:
      +materialized: table
```

✅ `+materialized` 的层级配置是 dbt **约定优于配置**的典范。

---

## 3.5 第一个 dbt 模型

```sql
-- models/staging/stg_orders.sql
WITH source AS (
    SELECT * FROM {{ source('jaffle_shop', 'orders') }}
),
renamed AS (
    SELECT id AS order_id, user_id AS customer_id, order_date, status
    FROM source
)
SELECT * FROM renamed
```

| 语法 | 说明 |
|------|------|
| `{{ source('schema', 'table') }}` | 引用源数据（原始表） |
| `{{ ref('model_name') }}` | 引用另一个 dbt 模型 |

✅ `{{ ref() }}` 和 `{{ source() }}` 是 dbt 的**两大核心引用机制**。

---

## 3.6 CLI 核心命令

| 命令 | 功能 | 常用参数 |
|------|------|---------|
| `dbt init` | 初始化新项目 | `--adapter` |
| `dbt run` | 执行模型变换 | `--select`, `--models` |
| `dbt test` | 运行数据测试 | `--select` |
| `dbt compile` | 编译 Jinja → SQL | |
| `dbt docs generate/serve` | 生成/预览文档 | |
| `dbt seed/snapshot/debug` | 种子/快照/调试 | |

✅ `dbt run` + `dbt test` 是日常开发的核心循环。

---

## 3.7 Jinja 模板基础

dbt 使用 Jinja 将 SQL 转化为**可编程的数据逻辑**：

```sql
{% set payment_methods = ['credit_card', 'coupon', 'bank_transfer'] %}
SELECT order_id,
    {% for method in payment_methods %}
    SUM(CASE WHEN payment_method = '{{ method }}' THEN amount ELSE 0 END) AS {{ method }}_amount
    {% if not loop.last %},{% endif %}
    {% endfor %}
FROM {{ ref('stg_payments') }} GROUP BY 1
```

| 结构 | 语法 | 用途 |
|------|------|------|
| 变量 | `{% set x = ... %}` | 定义可复用值 |
| 循环 | `{% for x in list %}` | 动态生成 SQL 列 |
| 条件 | `{% if condition %}` | 条件性包含 SQL |
| 宏 | `{% macro name(args) %}` | 可复用 SQL 函数 |

⚠️ Jinja 过度使用会降低 SQL 可读性——保持简洁。

---

## 3.8 🔧 DuckDB / SQLite 类比（dbt 项目本地化）

| # | dbt 概念 | DuckDB 本地实现 | SQLite 本地实现 | 标注 |
|---|---------|----------------|----------------|------|
| 1 | dbt 项目 = 多 SQL 文件 | 多个 `.sql` + DuckDB `.read()` 逐文件执行 | `sqlite3 db < model.sql` | 🔧 非本书引擎行为 |
| 2 | `dbt run` | 手动 `duckdb -c ".read('model.sql')"` | `sqlite3 db < model.sql` | 🔧 非本书引擎行为 |
| 3 | `dbt compile` | 无 Jinja 引擎，需手动展开模板 | 同 | 🔧 非本书引擎行为 |
| 4 | `dbt seed` | `CREATE TABLE AS SELECT * FROM read_csv_auto('seed.csv')` | `.import seed.csv table` | 🔧 非本书引擎行为 |

> 🔧 以上均为**非本书引擎行为**。

---

## 核心概念速览（中英对照）

| 中文概念 | English Term | 一句话定义 |
|---------|-------------|-----------|
| dbt 模型 | dbt Model | 一个 SELECT 语句的 .sql 文件，dbt 将其编译并执行 |
| Jinja 模板 | Jinja Template | 嵌入 SQL 中的 Python 风格模板语法 |
| 项目配置 | dbt_project.yml | 定义项目名称、路径、物化策略的配置文件 |
| 连接配置 | profiles.yml | 定义数据库连接参数的配置文件 |
| 源数据引用 | Source Reference | `{{ source() }}` 指向仓库中的原始表 |
| 模型引用 | Model Reference | `{{ ref() }}` 指向另一个 dbt 模型 |
| 约定优于配置 | Convention over Configuration | 目录结构即分层策略的设计哲学 |

---

## 最新演进与工业实践

| 时间 | 演进 | 影响 |
|------|------|------|
| 2022 | dbt-core 1.2 | 本书出版时的版本 |
| 2023 | dbt-core 1.5+ | Python models 支持 |
| 2024 | dbt-core 1.7 | dbt Mesh、跨项目 ref 稳定 |
| 2025 | dbt-core 1.9 | Unit Testing GA |
| 2026 | dbt 2.0 路线图 | 新包管理器、性能重写 |

> 📖 与 `../Data_Governance_Elsevier/`（#186）关联：
> - #186 的治理框架 → dbt 项目结构是治理的**代码化实现**
> - #186 的元数据管理 → dbt `schema.yml` 是模型级元数据载体
