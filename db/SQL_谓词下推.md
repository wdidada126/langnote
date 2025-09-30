# SQL_谓词下推

你的说法 “SQL `WITH` 只是语法层面的实现，而优化器会在执行前重写你的 SQL” —— 非常正确，而且触及了现代数据库查询优化的核心机制。
下面我们来深入解析这句话的含义，并说明 `WITH`（即 Common Table Expression, CTE）在实际执行中是如何被处理的。

##  一、`WITH` 是语法糖吗？

是的，从执行角度看，`WITH` 本质上是一种“语法层面”的结构，它提供了一种更清晰、模块化的方式来组织复杂查询，但数据库优化器并不会“原样执行”它。

### 示例：
```sql
WITH sales_summary AS (
    SELECT region, SUM(amount) AS total_sales
    FROM sales
    GROUP BY region
)
SELECT region, total_sales
FROM sales_summary
WHERE total_sales > 10000;
```

这个 `WITH` 子句看起来像是先执行 `sales_summary` 并生成一个临时结果集，但实际上：

>  数据库优化器会将其“内联”（inline）并重写为等价的子查询或直接融入执行计划。

##  二、优化器如何重写 `WITH`？

优化器会根据成本模型决定如何处理 CTE。常见策略有：

### 1. 内联展开（Inlining）——最常见
优化器将 CTE 内容直接插入主查询，变成：

```sql
SELECT region, total_sales
FROM (
    SELECT region, SUM(amount) AS total_sales
    FROM sales
    GROUP BY region
) AS sales_summary
WHERE total_sales > 10000;
```

 这样可以与其他部分进行联合优化（如谓词下推、连接顺序调整等）。

###  好处：
- 可以进行 谓词下推（Predicate Pushdown）
- 可以与外部查询做 连接重排序
- 利用统计信息做更优的执行计划

### 2. 物化（Materialization）——某些情况

在以下场景中，CTE 可能被物化（即先执行并缓存结果）：

- CTE 被多次引用
- 使用了递归 CTE（如树形结构查询）
- 数据库明确支持 `MATERIALIZED` 关键字（如 PostgreSQL 12+）

#### PostgreSQL 示例：
```sql
WITH sales_summary AS MATERIALIZED (
    SELECT region, SUM(amount) ...
)
...
```

> 如果不强制，PostgreSQL 也可能自动选择是否物化。

### 3. 非物化 + 多次求值
某些数据库（如早期 MySQL）对 CTE 的处理是“非物化且每次引用都重新计算”，这可能导致性能问题。

```sql
WITH expensive_cte AS (
    SELECT * FROM huge_table WHERE ...
)
SELECT * FROM expensive_cte a, expensive_cte b WHERE ...;
```

如果不物化，上面的 `huge_table` 查询会被执行 两次！

##  三、不同数据库的行为差异

| 数据库 | CTE 默认行为 | 是否可控制物化 |
|--------|---------------|----------------|
| PostgreSQL | 通常内联，可选择 `MATERIALIZED` / `NOT MATERIALIZED` |  是 |
| MySQL 8.0+ | 通常物化（尤其是复杂查询） |  否（自动决定） |
| Oracle | 可内联或物化，由优化器决定 |  可用 `INLINE` 提示 |
| SQL Server | 通常内联（视为视图） |  可用 `OPTION (QUERYTRACEON 9481)` 等控制 |
| SQLite | 通常内联 |  否 |
| OceanBase / TiDB | 类似 MySQL，多数情况物化 |  自动 |

## ⚙️ 四、优化器重写的实际意义

### 1. `WITH` 不保证执行顺序
你不能假设 `WITH` 中的查询会“先执行”。

### 2. 不能依赖副作用
例如：
```sql
WITH log_step AS (
    INSERT INTO audit_log VALUES ('start') RETURNING *
)
SELECT * FROM some_table;
```
 执行顺序可能被优化器打乱，日志插入可能延迟或并行执行。

### 3. 性能不一定更好
- 简单的 `WITH` 可能不如直接写子查询高效（如果被多次求值）
- 但复杂的逻辑用 `WITH` 更易读，且优化器能更好分析

##  五、什么时候该用 `WITH`？

| 场景 | 推荐使用 `WITH` |
|------|-----------------|
|  复杂查询分解 | 将大查询拆成多个逻辑步骤 |
|  递归查询 | 树形结构、组织架构遍历 |
|  多次引用同一子查询 | 避免重复写 |
|  提高可读性 | 团队协作、维护性优先 |
|  与窗口函数结合 | 先聚合再排序过滤 |

##  六、什么时候要小心？

| 场景 | 注意事项 |
|------|----------|
|  性能敏感场景 | 查看执行计划，确认是否被物化或重复执行 |
|  大结果集 CTE | 可能占用大量内存或临时空间 |
|  误以为“临时表” | CTE 不是临时表，生命周期仅限当前查询 |

##  七、如何验证优化器行为？

使用 `EXPLAIN` 查看执行计划：

```sql
EXPLAIN
WITH ...
SELECT ...
```

观察：
- 是否有“Materialize”节点？
- CTE 是否被展开为子查询？
- 扫描次数是否合理？

##  总结

| 说法 | 正确性 | 说明 |
|------|--------|------|
| “`WITH` 只是语法层面的实现” |  正确 | 它是逻辑组织工具，不是物理执行单元 |
| “优化器会在执行前重写 SQL” |  正确 | 优化器会内联、物化、重排序，生成最优执行计划 |
| “CTE 一定先执行” |  错误 | 执行顺序由优化器决定 |
| “CTE 性能一定差” |  错误 | 现代数据库优化得很好，可读性收益远大于微小性能损失 |

>  最佳实践：  
> 用 `WITH` 提升代码可读性和可维护性，相信优化器，但关键 SQL 一定要用 `EXPLAIN` 验证执行计划。

