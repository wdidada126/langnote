# 06 · Snapshots

> Ch 6 pp 213–242 | DOI: 10.1007/979-8-8688-1844-8_6

---

## 学习目标

- 理解 Snapshot 实现 SCD Type 2 的原理
- 掌握 `check` 与 `timestamp` 两种策略
- 配置 `dbt_valid_from` / `dbt_valid_to` / `dbt_scd_id`
- 了解 Snapshot 在生产环境中的最佳实践

---

## 6.1 Snapshot 概念

Snapshot 捕获源表随时间的变化，生成带有效时间区间的历史记录。

```
源表当前状态:
| id | status  |
|----|---------|
| 1  | active  |

Snapshot 历史:
| id | status  | dbt_valid_from | dbt_valid_to | dbt_scd_id |
|----|---------|----------------|--------------|------------|
| 1  | pending | 2024-01-01     | 2024-06-01   | abc123     |
| 1  | active  | 2024-06-01     | NULL         | def456     |
```

> ✅ `dbt_valid_to IS NULL` 表示当前有效行。

---

## 6.2 Timestamp 策略

```sql
-- snapshots/orders_snapshot.sql
{% snapshot orders_snapshot %}
{{
    config(
        target_schema='snapshots',
        unique_key='order_id',
        strategy='timestamp',
        updated_at='updated_at'
    )
}}
SELECT * FROM {{ source('jaffle_shop', 'orders') }}
{% endsnapshot %}
```

- 依赖源表中的 `updated_at` 时间戳列
- 当 `updated_at` 大于上次快照时间时，记录新行

---

## 6.3 Check 策略

```sql
{% snapshot customers_snapshot %}
{{
    config(
        target_schema='snapshots',
        unique_key='customer_id',
        strategy='check',
        check_cols=['status', 'email']
    )
}}
SELECT * FROM {{ source('jaffle_shop', 'customers') }}
{% endsnapshot %}
```

- 比较指定列的值是否变化
- 不依赖时间戳列，但需要全行扫描对比

---

## 6.4 策略对比

| 维度 | Timestamp | Check |
|------|-----------|-------|
| 依赖列 | `updated_at` 时间戳 | 任意业务列 |
| 性能 | 高 (仅查新增) | 低 (需全量对比) |
| 准确性 | 依赖源表更新时间 | 精确到列级 |
| 适用场景 | 源表有可靠时间戳 | 源表无时间戳 |

> ⚠️ 优先使用 timestamp 策略，check 策略在大数据量下性能较差。

---

## 6.5 Snapshot 元数据列

| 列名 | 类型 | 说明 |
|------|------|------|
| `dbt_scd_id` | varchar | 快照行唯一标识 (hash) |
| `dbt_valid_from` | timestamp | 有效区间起始 |
| `dbt_valid_to` | timestamp/null | 有效区间结束 (NULL=当前) |
| `dbt_updated_at` | timestamp | 快照执行时间 |

---

## 6.6 查询快照

```sql
-- 查询当前有效记录
SELECT * FROM orders_snapshot WHERE dbt_valid_to IS NULL;

-- 查询某时间点的历史状态
SELECT * FROM orders_snapshot
WHERE '2024-06-15' BETWEEN dbt_valid_from AND COALESCE(dbt_valid_to, '9999-12-31');
```

---

## 6.7 Snapshot 配置

```yaml
# dbt_project.yml
snapshots:
  my_project:
    +target_schema: snapshots
    +strategy: timestamp
    +unique_key: id
    +updated_at: updated_at
    +invalidate_hard_deletes: true   # 标记软删除
```

> ⚠️ `invalidate_hard_deletes` (v1.0+) 将源表中已删除的行标记 `dbt_valid_to = snapshot时间`。

---

## 6.8 运行 Snapshot

```bash
dbt snapshot                    # 执行所有 snapshot
dbt snapshot --select orders_snapshot   # 单个
```

---

## 🔧 6.9 DuckDB / SQLite 类比

> 以下类比使用 DuckDB/SQLite 概念辅助理解，**非本书引擎行为**。

| # | dbt 概念 | DuckDB 类比 | SQLite 类比 |
|---|---------|-------------|-------------|
| 1 | SCD Type 2 快照 | DuckDB 手动 `INSERT` + 有效区间列 | SQLite 手动 `INSERT` + 有效区间列 |
| 2 | timestamp 策略 | DuckDB `MERGE` + `updated_at` 对比 | SQLite `INSERT OR REPLACE` + 时间对比 |
| 3 | check 策略 | DuckDB 全表 `EXCEPT` 差异检测 | SQLite `EXCEPT` 差异检测 |
| 4 | invalidate_hard_deletes | DuckDB `LEFT JOIN` + `IS NULL` 标记删除 | SQLite `LEFT JOIN` + `IS NULL` |

---

## 核心概念速览（中英对照）

| 中文 | English | 一句话 |
|------|---------|--------|
| 快照 | Snapshot | 捕获源表历史变化 |
| 缓慢变化维度 | SCD Type 2 | 新增行记录维度变化 |
| 时间戳策略 | Timestamp Strategy | 依赖 updated_at 检测变化 |
| 检查策略 | Check Strategy | 对比指定列值检测变化 |
| 有效区间 | Valid From / To | 标记行的时间有效性 |
| 硬删除标记 | Invalidate Hard Deletes | 追踪源表中被删除的行 |

---

## 最新演进与工业实践

- **dbt v1.8+ Snapshot 重构**: 引入 `dbt-snowflake` 原生 MERGE 优化 ⚠️ [docs.getdbt.com/docs/build/snapshots](https://docs.getdbt.com/docs/build/snapshots)
- **Fusion 引擎对 snapshot 的加速**: 大表 MERGE 操作性能提升 ⚠️ [getdbt.com/blog/dbt-core-v1-11-is-ga](https://www.getdbt.com/blog/dbt-core-v1-11-is-ga)
- **硬删除追踪增强**: v1.9+ 对 `invalidate_hard_deletes` 的适配器支持更统一
- **替代方案**: 对于需要完整 CDC 的场景，考虑 Debezium/Fivetran 等 EL 工具直接生成 SCD2 表
