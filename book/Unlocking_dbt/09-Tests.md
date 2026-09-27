# 09 · Tests

> Ch 9 pp 307–338 | DOI: 10.1007/979-8-8688-1844-8_9

---

## 学习目标

- 掌握 dbt 的三种测试类型: schema test / data test / unit test
- 配置通用测试 (generic tests) 与自定义测试
- 理解测试严重性 (severity) 与阻断策略
- 掌握测试驱动开发 (TDD) 在 dbt 中的实践

---

## 9.1 测试类型总览

| 类型 | 定义位置 | 行为 | 示例 |
|------|---------|------|------|
| Schema (Generic) Test | schema.yml | 自动生成 SQL 检查 | not_null, unique |
| Data (Singular) Test | tests/ 目录 | 自定义 SQL 查询 | 业务规则校验 |
| Unit Test | schema.yml + fixtures | 模拟输入验证逻辑 | 复杂转换验证 |

> ✅ dbt v1.8+ 正式引入 Unit Test，此前仅有 schema + data 两类。

---

## 9.2 Schema Tests (Generic Tests)

```yaml
# models/schema.yml
models:
  - name: fct_orders
    columns:
      - name: order_id
        tests:
          - unique
          - not_null
      - name: amount
        tests:
          - accepted_values:
              values: ['pending', 'completed', 'cancelled']
      - name: customer_id
        tests:
          - relationships:
              to: ref('dim_customers')
              field: customer_id
```

内置 Generic Tests: `unique` (列值唯一) | `not_null` (无 NULL) | `accepted_values` (允许值列表) | `relationships` (外键完整性)

---

## 9.3 自定义 Generic Test

```sql
-- macros/test_positive_value.sql
{% test positive_value(model, column_name) %}
SELECT * FROM {{ model }} WHERE {{ column_name }} < 0
{% endtest %}
```

使用:
```yaml
columns:
  - name: amount
    tests:
      - positive_value
```

---

## 9.4 Data Tests (Singular Tests)

```sql
-- tests/assert_order_totals_match.sql
SELECT
    order_id,
    SUM(amount) AS order_total,
    (SELECT SUM(payment_amount) FROM {{ ref('stg_payments') }} p
     WHERE p.order_id = o.order_id) AS payment_total
FROM {{ ref('fct_orders') }} o
GROUP BY 1
HAVING order_total != payment_total
```

```bash
dbt test --select test_type:singular
```

> ✅ Singular test 返回任何行即视为失败。

---

## 9.5 Unit Tests (v1.8+)

```yaml
models:
  - name: fct_orders
    unit_tests:
      - name: test_order_amount_calculation
        model: fct_orders
        given:
          - input: ref('stg_orders')
            rows:
              - {order_id: 1, amount: 100, status: 'completed'}
              - {order_id: 2, amount: 200, status: 'pending'}
          - input: ref('stg_customers')
            rows:
              - {customer_id: 1, name: 'Alice'}
        expect:
          rows:
            - {order_id: 1, amount: 100, customer_name: 'Alice'}
            - {order_id: 2, amount: 200, customer_name: null}
```

```bash
dbt test --select test_type:unit
```

---

## 9.6 测试配置

```yaml
models:
  - name: fct_orders
    columns:
      - name: order_id
        tests:
          - unique:
              severity: error    # 失败时阻断 (默认)
              config:
                where: "order_date > '2024-01-01'"
          - not_null:
              severity: warn     # 失败时仅警告
```

| severity | 行为 |
|----------|------|
| `error` | 测试失败 → 非零退出码 |
| `warn` | 测试失败 → 仅警告 |

---

## 9.7 测试运行与选择

```bash
dbt test                              # 所有测试
dbt test --models fct_orders          # 特定模型
dbt test --select test_type:generic   # 仅 generic tests
dbt test --exclude tag:deprecated     # 排除特定 tag
```

---

## 9.8 测试最佳实践

- ✅ 主键列必须有 `unique` + `not_null` 测试
- ✅ 外键列使用 `relationships` 测试
- ✅ 状态/类型列使用 `accepted_values` 测试
- ✅ 关键业务规则用 singular test 覆盖
- ⚠️ 避免过多 warn 级别测试导致"测试疲劳"
- 🔧 DuckDB 类比: `ASSERT` 语句类似 dbt 测试的 fail-fast 行为

---

## 🔧 9.9 DuckDB / SQLite 类比

> 以下类比使用 DuckDB/SQLite 概念辅助理解，**非本书引擎行为**。

| # | dbt 概念 | DuckDB 类比 | SQLite 类比 |
|---|---------|-------------|-------------|
| 1 | unique 测试 | `COUNT(*) != COUNT(DISTINCT col)` | 同 |
| 2 | not_null 测试 | `WHERE col IS NULL` 检查 | 同 |
| 3 | relationships 测试 | `LEFT JOIN ... WHERE right.id IS NULL` | 同 |
| 4 | unit test | `VALUES` 子句构造测试数据 | `VALUES` 子句 |

---

## 核心概念速览（中英对照）

| 中文 | English | 一句话 |
|------|---------|--------|
| 通用测试 | Generic (Schema) Test | schema.yml 中声明的标准测试 |
| 单一测试 | Singular (Data) Test | 自定义 SQL 的业务规则测试 |
| 单元测试 | Unit Test | 模拟输入验证模型逻辑 |
| 严重性 | Severity | error 阻断 / warn 仅告警 |
| 测试驱动开发 | TDD | 先写测试再写模型 |
| 测试选择 | Test Selection | 按类型/模型/tag 筛选 |

---

## 最新演进与工业实践

- **Unit Test 持续增强** (v1.9+): 支持更多输入格式和 mock 能力 ⚠️ [docs.getdbt.com/docs/build/unit-tests](https://docs.getdbt.com/docs/build/unit-tests)
- **dbt_expectations 包**: 提供 50+ 预置测试 (正则、分布、时序等)
- **Fusion 引擎**: 测试执行并行化，大项目测试时间缩短 ⚠️ [getdbt.com/blog/dbt-core-v1-11-is-ga](https://www.getdbt.com/blog/dbt-core-v1-11-is-ga)
- **CI/CD 集成**: dbt Cloud CI Job 自动运行 slim CI 测试 (仅测试受影响的模型)
