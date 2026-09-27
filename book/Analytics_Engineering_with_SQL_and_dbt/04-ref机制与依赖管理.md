# 04-ref机制与依赖管理

> **对应章节**: Ch4 — refs, sources, and Dependencies
> **核心命题**: `ref()` / `source()` 机制、DAG 自动构建、依赖图管理

---

## 4.1 ref() 的本质

### ref() 做了什么？

`{{ ref('model_name') }}` 在编译时被替换为目标引擎的**完整表引用**：

```
编译前:  SELECT * FROM {{ ref('stg_orders') }}
编译后:  SELECT * FROM analytics_dev.stg_orders   -- Snowflake 示例
```

| 职责 | 说明 |
|------|------|
| **名称→路径解析** | 将模型名映射到 schema.table |
| **依赖声明** | 告诉 dbt "本模型依赖 stg_orders" |
| **DAG 构建** | dbt 据此自动排序执行顺序 |
| **环境隔离** | dev/prod 自动切换 schema |

✅ `ref()` 是 dbt 的**核心抽象**——开发者只写逻辑名，dbt 负责物理寻址。

### ref() vs 硬编码表名

| 方式 | 可移植性 | 依赖追踪 | 环境切换 |
|------|---------|---------|---------|
| `{{ ref('x') }}` | ✅ 高 | ✅ 自动 | ✅ 自动 |
| `SELECT * FROM dev.x` | ❌ 硬编码 | ❌ 无 | ❌ 手动改 |

⚠️ 在 dbt 模型中**永远使用 ref()**，禁止硬编码表名。

---

## 4.2 source() 机制

### source() 与 ref() 的区别

```yaml
# models/schema.yml
sources:
  - name: jaffle_shop
    schema: raw_jaffle_shop
    tables:
      - name: orders
      - name: customers
```

```sql
-- 在模型中引用
SELECT * FROM {{ source('jaffle_shop', 'orders') }}
```

| 维度 | `ref()` | `source()` |
|------|---------|-----------|
| **指向** | 另一个 dbt 模型 | 仓库中的原始表 |
| **依赖** | 模型间依赖 | 无上游 dbt 依赖 |
| **新鲜度检查** | 不适用 | ✅ 支持 source freshness |
| **YAML 声明** | 不需要 | 需要在 sources.yml 声明 |

✅ `source()` 是 dbt 项目的**数据入口点**——所有外部数据通过 source 声明进入 DAG。

### Source Freshness（源数据新鲜度）

```yaml
sources:
  - name: jaffle_shop
    tables:
      - name: orders
        loaded_at_field: _etl_loaded_at
        freshness:
          warn_after: {count: 12, period: hour}
          error_after: {count: 24, period: hour}
```

```bash
dbt source freshness  # 检查源数据是否过期
```

✅ Source freshness 是数据质量的**第一道防线**——在变换前检查源数据是否及时到达。

---

## 4.3 DAG（有向无环图）

```
source('raw','orders') → stg_orders → int_orders → fact_orders → mart_summary
source('raw','customers') → stg_customers → dim_customers ──┘
```

| DAG 特性 | 说明 |
|---------|------|
| **有向** | 依赖方向单一：上游→下游 |
| **无环** | 不允许循环依赖 |
| **自动拓扑排序** | `dbt run` 按依赖顺序执行 |

✅ DAG 是 dbt 的**调度引擎**——开发者声明依赖，dbt 决定执行顺序。

⚠️ 隐式依赖（共享底层表但无 `ref()`）是危险的——dbt 无法追踪。

---

## 4.4 选择器语法

```bash
dbt run --select stg_orders+         # 模型 + 下游
dbt run --select +fact_orders        # 模型 + 上游
dbt run --select staging             # 某层
dbt run --select tag:nightly         # 按标签
dbt run --select marts --exclude v1  # 排除
```

✅ 选择器是 dbt **大规模项目的导航系统**。

---

## 4.5 🔧 DuckDB / SQLite 类比（ref 与 DAG 本地化）

| # | dbt 概念 | DuckDB 本地实现 | SQLite 本地实现 | 标注 |
|---|---------|----------------|----------------|------|
| 1 | `ref()` 名称解析 | `CREATE VIEW fact_orders AS SELECT * FROM stg_orders` — VIEW 链模拟 ref 传递 | 同：`CREATE VIEW` 链 | 🔧 非本书引擎行为 |
| 2 | DAG 执行排序 | 无自动 DAG，需手动按依赖顺序执行 `.read()` | 同：手动排序 `.read` | 🔧 非本书引擎行为 |
| 3 | `source()` 原始表 | `CREATE TABLE raw_orders AS SELECT * FROM read_csv_auto('raw.csv')` | `.import raw.csv raw_orders` | 🔧 非本书引擎行为 |
| 4 | Source freshness | `SELECT MAX(loaded_at) FROM raw_orders` 手动检查 | 同：`SELECT MAX(...)` | 🔧 非本书引擎行为 |
| 5 | 选择器 `+model+` | 无等价物，需手动追踪 VIEW 依赖 | 同 | 🔧 非本书引擎行为 |

> 🔧 以上均为**非本书引擎行为**——DAG 自动构建是 dbt 独有的编排能力。

---

## 4.6 依赖管理最佳实践

| 实践 | 原因 |
|------|------|
| 每个模型只 ref 直接上游 | 避免隐式依赖 |
| staging 层统一引用 source | 原始表变更只影响 staging |
| 避免跨层 ref（如 mart→staging） | 保持分层纪律 |
| 用 `dbt ls` 检查依赖图 | 发现意外依赖 |
| 定期清理废弃模型 | 减少 DAG 复杂度 |

⚠️ 常见反模式：**spaghetti DAG**——过多交叉依赖导致变更影响不可预测。

---

## 4.7 本章关键术语

| 英文 | 中文 | 定义 |
|------|------|------|
| ref() | 模型引用 | 引用另一个 dbt 模型的 Jinja 函数 |
| source() | 源数据引用 | 引用仓库原始表的 Jinja 函数 |
| DAG | 有向无环图 | dbt 自动构建的模型依赖图 |
| Node Selector | 节点选择器 | CLI 中精准选择运行范围的语法 |
| Source Freshness | 源数据新鲜度 | 检查源数据是否按时到达的机制 |
| Implicit Dependency | 隐式依赖 | 未通过 ref 声明的间接数据依赖 |

---

## 核心概念速览（中英对照）

| 中文概念 | English Term | 一句话定义 |
|---------|-------------|-----------|
| 模型引用 | ref() | dbt 中引用上游模型的核心函数，同时声明依赖关系 |
| 源数据引用 | source() | 指向仓库原始表的引用，支持新鲜度检查 |
| 有向无环图 | DAG (Directed Acyclic Graph) | dbt 根据 ref 自动构建的模型执行依赖图 |
| 拓扑排序 | Topological Sort | DAG 上线性化执行顺序的算法 |
| 节点选择器 | Node Selector | 通过 CLI 参数精准控制 dbt 运行范围 |
| 源数据新鲜度 | Source Freshness | 基于 loaded_at 字段检查源数据是否过期 |
| 隐式依赖 | Implicit Dependency | 未通过 ref 声明、dbt 无法追踪的数据依赖 |

---

## 最新演进与工业实践

| 时间 | 演进 | 影响 |
|------|------|------|
| 2022 | dbt-core 1.2 | ref() 支持同项目内模型引用 |
| 2023 | dbt-core 1.6 | 跨项目 ref 实验性支持（dbt Mesh 基础） |
| 2024 | dbt Mesh GA | `ref('project', 'model')` 正式稳定 |
| 2025 | dbt Mesh 2.0 | 跨项目组依赖可视化管理 |
| 2026 | dbt 2.0 路线图 | 可能的 DAG 性能优化、新选择器语法 |

> 📖 与 `../Unlocking_dbt/` 关联：
> - Unlocking_dbt Ch3 (Setting Up a dbt Project) → 项目结构中 ref/source 的详细配置
> - Unlocking_dbt Ch12 (dbt Mesh) → 跨项目 ref 的深度实践
>
> 📖 与 `../Data_Mesh/`（#201）关联：
> - #201 Ch3 (数据即产品) → dbt 项目即 domain team 的数据产品，ref 即产品间接口
> - #201 Ch7 (逻辑架构) → dbt Mesh 的跨项目 ref 是 Data Mesh 逻辑架构的技术实现
