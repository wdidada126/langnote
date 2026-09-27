# 08 · Hooks

> Ch 8 pp 283–306 | DOI: 10.1007/979-8-8688-1844-8_8

---

## 学习目标

- 理解 dbt Hooks 的执行时机与类型
- 掌握 `pre-hook` 和 `post-hook` 的配置方式
- 学会使用 Hooks 进行权限管理、日志记录、性能优化
- 了解 Hooks 的限制与最佳实践

---

## 8.1 Hooks 概述

Hooks 是在 dbt 模型执行前后自动运行的 SQL 语句。

| Hook 类型 | 执行时机 | 典型用途 |
|-----------|---------|---------|
| `pre-hook` | 模型 SQL 执行前 | 创建临时表、删除旧数据 |
| `post-hook` | 模型 SQL 执行后 | 授权、创建索引、记录日志 |
| `on-run-start` | `dbt run` 开始时 | 会话级设置 |
| `on-run-end` | `dbt run` 结束时 | 全局授权、清理 |

---

## 8.2 Pre-hook 与 Post-hook

### 模型级配置

```sql
{{ config(
    materialized='table',
    pre_hook="DELETE FROM {{ this }} WHERE order_date < '2020-01-01'",
    post_hook="GRANT SELECT ON {{ this }} TO ROLE ANALYST"
) }}
SELECT ...
```

### 项目级配置

```yaml
# dbt_project.yml
models:
  my_project:
    marts:
      +post-hook:
        - "GRANT SELECT ON {{ this }} TO ROLE READONLY"
        - "COMMENT ON TABLE {{ this }} IS 'dbt managed'"
```

---

## 8.3 on-run-start / on-run-end

```yaml
# dbt_project.yml
on-run-start:
  - "SET timezone = 'UTC'"
  - "SELECT 'dbt run started at ' || current_timestamp"

on-run-end:
  - "GRANT USAGE ON SCHEMA {{ target.schema }} TO ROLE ANALYST"
  - "{{ grant_select_to_roles() }}"   # 调用自定义宏
```

> ✅ `on-run-end` 中的 `{{ this }}` 不可用（因为此时没有"当前模型"上下文）。

---

## 8.4 常见 Hook 模式

### 权限管理

```sql
-- macros/grant_select.sql
{% macro grant_select_to_roles() %}
    {% if target.name == 'prod' %}
        GRANT SELECT ON {{ this }} TO ROLE analyst;
        GRANT SELECT ON {{ this }} TO ROLE bi_tool;
    {% endif %}
{% endmacro %}
```

### 增量前清理

```sql
{{ config(
    materialized='incremental',
    pre_hook="DELETE FROM {{ this }} WHERE load_date >= current_date - 1"
) }}
```

### 日志与审计

```yaml
on-run-end:
  - >
    INSERT INTO audit.dbt_run_log (run_at, target, schema, row_count)
    SELECT current_timestamp, '{{ target.name }}', '{{ target.schema }}', COUNT(*)
    FROM {{ this }}
```

---

## 8.5 Hook 执行顺序

```
1. on-run-start (整个 dbt run 开始时)
2. 对每个模型:
   a. pre-hook
   b. 模型 SQL 执行
   c. post-hook
3. on-run-end (整个 dbt run 结束时)
```

> ⚠️ Hook 中的 SQL 直接发送到仓库执行，不经过 Jinja 编译（除了 `{{ this }}` 等 dbt 上下文变量）。

---

## 8.6 Hook 限制

- ❌ Hook 中不能使用 `ref()` 或 `source()`
- ❌ Hook 不能返回结果集
- ⚠️ 多语句 Hook 需使用分号分隔
- ⚠️ 不同适配器的 SQL 方言差异需在 Hook 中自行处理

---

## 8.7 Hook vs Operations

dbt 的 `operations` 是一种特殊的模型类型，用于执行不产出表的 SQL:

```sql
-- models/operations/grant_permissions.sql
{{ config(materialized='operation') }}
{% if execute %}
    GRANT SELECT ON ALL TABLES IN SCHEMA {{ target.schema }} TO ROLE analyst;
{% endif %}
```

> ✅ `operation` 类型在 `on-run-end` 阶段执行，适合全局权限管理。

---

## 🔧 8.8 DuckDB / SQLite 类比

> 以下类比使用 DuckDB/SQLite 概念辅助理解，**非本书引擎行为**。

| # | dbt 概念 | DuckDB 类比 | SQLite 类比 |
|---|---------|-------------|-------------|
| 1 | pre-hook (执行前 SQL) | DuckDB 事务内 `DELETE` 前置清理 | SQLite `BEFORE` 触发器 |
| 2 | post-hook (执行后 SQL) | DuckDB 事务后 `GRANT` / `ANALYZE` | SQLite `AFTER` 触发器 |
| 3 | on-run-start (全局初始化) | DuckDB `PRAGMA` 会话设置 | SQLite `PRAGMA` 会话设置 |
| 4 | on-run-end (全局收尾) | DuckDB 脚本末尾批量授权 | SQLite `.output` 日志导出 |

---

## 核心概念速览（中英对照）

| 中文 | English | 一句话 |
|------|---------|--------|
| 前钩子 | Pre-hook | 模型执行前运行的 SQL |
| 后钩子 | Post-hook | 模型执行后运行的 SQL |
| 全局开始钩 | on-run-start | dbt run 启动时执行 |
| 全局结束钩 | on-run-end | dbt run 结束时执行 |
| 操作模型 | Operation | 不产出表的特殊模型 |
| 权限授予 | Grant / Revoke | Hook 常见用途 |

---

## 最新演进与工业实践

- **dbt v1.8+ Hook 上下文增强**: `on-run-end` 可访问 `model` 对象获取更多信息 ⚠️ [docs.getdbt.com/docs/build/hooks](https://docs.getdbt.com/docs/build/hooks)
- **dbt Mesh 中的 Hook**: 跨项目场景下 `on-run-end` 的执行范围需要特别注意
- **Fusion 引擎**: Hook 执行在 Fusion 中保持顺序不变，但整体 run 时间缩短
- **替代方案**: 对于复杂权限管理，考虑使用 Terraform/仓库原生 RBAC 替代 Hook
