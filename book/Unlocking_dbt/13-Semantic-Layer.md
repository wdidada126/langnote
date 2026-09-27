# 13 · Semantic Layer

> Ch 13 pp 437–461 | DOI: 10.1007/979-8-8688-1844-8_13

---

## 学习目标

- 理解 Semantic Layer 的定位与价值
- 掌握 Metrics 和 Dimensions 的定义方式
- 了解 dbt Semantic Layer 与 BI 工具的集成
- 理解从 SQL 指标到语义层的演进路径

---

## 13.1 什么是 Semantic Layer

Semantic Layer 是在数据仓库之上、BI 工具之下的抽象层，统一定义业务指标和维度。

```
[Warehouse Models (dbt)]
        ↓
[Semantic Layer: Metrics + Dimensions]
        ↓
[BI Tools: Tableau / Looker / dbt Semantic Layer API]
```

> ✅ 核心价值: 指标定义一处维护，多工具消费——避免每个 BI 报表各自计算。

---

## 13.2 Metrics 定义

### 在 schema.yml 中定义 (旧方式)

```yaml
metrics:
  - name: total_revenue
    label: "Total Revenue"
    type: sum
    type_params:
      measure: revenue
    description: "所有已完成订单的总收入"
    filters:
      - !sql "{{ Dimension('order_status__status') }} = 'completed'"
```

### 在 semantic_models.yml 中定义 (新方式 v1.6+)

```yaml
semantic_models:
  - name: orders
    description: "订单语义模型"
    model: ref('fct_orders')
    defaults:
      agg_time_dimension: order_date
    entities:
      - name: order_id
        type: primary
      - name: customer_id
        type: foreign
    dimensions:
      - name: order_date
        type: time
        type_params:
          time_granularity: day
      - name: status
        type: categorical
    measures:
      - name: revenue
        agg: sum
        expr: amount
      - name: order_count
        agg: count_distinct
        expr: order_id

metrics:
  - name: total_revenue
    label: "Total Revenue"
    type: simple
    type_params:
      measure: revenue
  - name: avg_order_value
    label: "Average Order Value"
    type: derived
    type_params:
      expr: total_revenue / order_count
      metrics:
        - name: total_revenue
        - name: order_count
```

---

## 13.3 Semantic Model 组件

| 组件 | 说明 | 示例 |
|------|------|------|
| Entity | 业务实体 (主键/外键) | order_id, customer_id |
| Dimension | 可过滤/分组的属性 | order_date, status, region |
| Measure | 可聚合的基础度量 | revenue (sum), order_count (count) |
| Metric | 面向消费者的指标 | total_revenue, avg_order_value |

---

## 13.4 Metric 类型

| 类型 | 说明 | 示例 |
|------|------|------|
| simple | 直接聚合一个 measure | total_revenue = sum(revenue) |
| derived | 基于其他 metric 计算 | avg_order_value = revenue / orders |
| cumulative | 累计值 | running_total_revenue |
| ratio | 两个 metric 的比值 | conversion_rate |

---

## 13.5 dbt Semantic Layer API

```graphql
# GraphQL 查询
{
  metrics(
    input: {
      metrics: [{name: "total_revenue"}]
      groupBy: [{name: "metric_time"}, {name: "region"}]
      where: [{expression: "{{ Dimension('orders__status') }} = 'completed'"}]
    }
  ) {
    data { metricTime region totalRevenue }
  }
}
```

---

## 13.6 BI 工具集成

| 工具 | 集成方式 |
|------|---------|
| Tableau | dbt Semantic Layer 连接器 |
| Google Looker | 原生 dbt Semantic Layer 集成 |
| dbt Cloud | 内置 Metrics Explorer |
| Google Sheets | dbt Semantic Layer 插件 |

> ✅ 用户可在 BI 工具中发现和拖放 dbt 定义的指标，无需手写 SQL。

---

## 13.7 Metrics Explorer (dbt Cloud)

dbt Cloud 内置 Metrics Explorer: 指标浏览与搜索、可视化构建查询、时间范围选择、维度下钻、导出结果。

---

## 13.8 Semantic Layer 最佳实践

- ✅ 指标定义从 SQL 模型解耦——不要在 BI 工具中硬编码
- ✅ 使用 measure 作为原子聚合，metric 作为组合
- ✅ 为每个 metric 提供清晰的 label 和 description
- ✅ 使用 derived metric 处理复合指标
- ⚠️ semantic model 的 entity 必须与底层模型的主键一致

---

## 🔧 13.9 DuckDB / SQLite 类比

> 以下类比使用 DuckDB/SQLite 概念辅助理解，**非本书引擎行为**。

| # | dbt 概念 | DuckDB 类比 | SQLite 类比 |
|---|---------|-------------|-------------|
| 1 | measure | 聚合函数 `SUM()` / `COUNT()` | 聚合函数 `SUM()` / `COUNT()` |
| 2 | metric | 无指标层（需 SQL 手动定义） | 无指标层 |
| 3 | Semantic Layer API | 无 API（需外部服务） | 无 API |
| 4 | Metrics Explorer | 无可视化（需 BI 工具） | 无可视化 |

---

## 核心概念速览（中英对照）

| 中文 | English | 一句话 |
|------|---------|--------|
| 语义层 | Semantic Layer | 业务指标的抽象定义层 |
| 度量 | Measure | 基础聚合 (sum/count/avg) |
| 指标 | Metric | 面向消费者的业务指标 |
| 实体 | Entity | 主键/外键业务实体 |
| 维度 | Dimension | 可过滤/分组的属性 |
| 派生指标 | Derived Metric | 基于其他指标计算 |

---

## 最新演进与工业实践

- **dbt Semantic Layer GA** (v1.6+): MetricFlow 引擎正式集成到 dbt Core ⚠️ [docs.getdbt.com/docs/build/about-metricflow](https://docs.getdbt.com/docs/build/about-metricflow)
- **Metrics Explorer 增强** (2025): 支持更多可视化和导出格式
- **MCP Server 集成**: AI Agent 可通过 MCP 查询语义层指标 ⚠️ [docs.getdbt.com/docs/dbt-cloud/using-dbt-cloud/cloud-discovery-api](https://docs.getdbt.com/docs/dbt-cloud/using-dbt-cloud/cloud-discovery-api)
- **Fusion 引擎**: MetricFlow 查询优化，复杂指标查询性能提升 ⚠️ [getdbt.com/blog/dbt-core-v1-11-is-ga](https://www.getdbt.com/blog/dbt-core-v1-11-is-ga)
- **Headless BI 趋势**: Semantic Layer 作为 "Headless BI" 正在成为行业标准架构模式
