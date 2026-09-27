# 10 · Documentation

> Ch 10 pp 339–379 | DOI: 10.1007/979-8-8688-1844-8_10

---

## 学习目标

- 掌握 dbt 文档自动生成机制
- 编写 schema.yml 中的描述与元数据
- 使用 `dbt docs generate` 生成文档站点
- 理解 Discovery API 查询文档元数据

---

## 10.1 文档即代码

dbt 将文档嵌入代码中，通过 YAML 描述模型、列、测试:

```yaml
# models/marts/schema.yml
version: 2
models:
  - name: fct_orders
    description: "订单事实表，每行代表一笔订单"
    docs:
      show: true
    config:
      tags: ['finance', 'orders']
    columns:
      - name: order_id
        description: "订单唯一标识"
        tests:
          - unique
          - not_null
      - name: customer_id
        description: "客户 FK → dim_customers"
        meta:
          business_owner: "Sales Team"
      - name: amount
        description: "订单金额 (美元)"
      - name: status
        description: "订单状态"
```

> ✅ 文档与代码同仓库，保证同步更新。

---

## 10.2 文档生成与浏览

```bash
dbt docs generate     # 编译文档到 target/
dbt docs serve        # 启动本地 HTTP 服务器
dbt docs serve --port 8081   # 指定端口
```

生成的文档站点包含: 模型列表与描述、列级文档与测试状态、**Lineage DAG** (血缘图)、SQL 源码查看、依赖关系图。

---

## 10.3 Lineage 血缘图

dbt 自动根据 `ref()` / `source()` 生成血缘 DAG:

```
[source: jaffle_shop.orders]
        ↓
[stg_orders]
        ↓
[fct_orders]  →  [dim_customers]
        ↓
[BI Tool / Semantic Layer]
```

> ✅ 血缘图是 dbt 文档的核心价值——自动维护，无需手动绘制。

---

## 10.4 自定义文档页面

```markdown
<!-- models/marts/docs.md -->
{% docs fct_orders %}
## 订单事实表

每行代表一笔客户订单。

### 粒度
一行 = 一笔订单

### 关键业务规则
- amount 为最终支付金额 (已扣除折扣)
- status 字段反映最新状态
{% enddocs %}

{% docs fct_orders__order_id %}
订单唯一标识，由源系统生成。
{% enddocs %}
```

在 schema.yml 中引用:
```yaml
models:
  - name: fct_orders
    description: "{{ doc('fct_orders') }}"
    columns:
      - name: order_id
        description: "{{ doc('fct_orders__order_id') }}"
```

---

## 10.5 元数据 (meta)

```yaml
columns:
  - name: amount
    meta:
      business_owner: "Finance Team"
      sla: "P99 < 5min"
      data_steward: "Alice"
```

`meta` 字段不影响 dbt 行为，仅存储额外元数据。可通过 Discovery API 查询，也可在自定义宏中读取。

---

## 10.6 文档站点配置

```yaml
# dbt_project.yml
models:
  my_project:
    +docs:
      show: true           # 是否在文档中显示
      node_color: '#FF0000'  # DAG 图中的颜色
```

---

## 10.7 dbt Cloud 文档

dbt Cloud 自动托管文档站点: 每次生产 run 后自动更新，支持搜索、过滤，集成 Slack 通知，Discovery API 提供编程访问。

---

## 10.8 Discovery API

```graphql
# GraphQL 查询示例
{
  models(jobId: 12345) {
    name
    description
    columns { name description type }
  }
}
```

> ✅ Discovery API 是构建自定义数据目录 (data catalog) 的基础。

---

## 🔧 10.9 DuckDB / SQLite 类比

> 以下类比使用 DuckDB/SQLite 概念辅助理解，**非本书引擎行为**。

| # | dbt 概念 | DuckDB 类比 | SQLite 类比 |
|---|---------|-------------|-------------|
| 1 | 自动血缘图 | 无自动血缘（需外部工具） | 无血缘功能 |
| 2 | schema.yml 文档 | `COMMENT ON` 注释 | 无列注释（仅表注释） |
| 3 | docs generate 站点 | 无对应（需外部文档工具） | 无对应 |
| 4 | Discovery API | 无 API（需自建） | 无 API |

---

## 核心概念速览（中英对照）

| 中文 | English | 一句话 |
|------|---------|--------|
| 文档即代码 | Documentation as Code | YAML + Markdown 嵌入代码 |
| 血缘图 | Lineage Graph | 自动生成的依赖 DAG |
| 文档站点 | Docs Site | 可浏览的 HTML 文档 |
| 元数据 | Meta | 自定义业务元数据字段 |
| 发现 API | Discovery API | GraphQL 接口查询 dbt 元数据 |
| 文档块 | Docs Block | Markdown 文档片段复用 |

---

## 最新演进与工业实践

- **Discovery API v2** (2025): 新增 model versions、exposures 查询 ⚠️ [docs.getdbt.com/docs/dbt-cloud/using-dbt-cloud/cloud-discovery-api](https://docs.getdbt.com/docs/dbt-cloud/using-dbt-cloud/cloud-discovery-api)
- **dbt MCP Server** (2025-10 GA): AI Agent 可通过 MCP 协议查询 dbt 文档和血缘
- **Fusion 引擎**: 文档生成速度提升，大项目从分钟级降到秒级 ⚠️ [getdbt.com/blog/dbt-core-v1-11-is-ga](https://www.getdbt.com/blog/dbt-core-v1-11-is-ga)
- **自定义数据目录**: 基于 Discovery API 构建内部 data catalog (如 DataHub, Amundsen 集成)
