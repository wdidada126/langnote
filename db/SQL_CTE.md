# SQL_CTE

https://dev.mysql.com/doc/refman/8.0/en/with.html
https://www.postgresql.org/docs/current/queries-with.html
https://learn.microsoft.com/en-us/sql/t-sql/queries/with-common-table-expression-transact-sql?view=sql-server-ver17

问题1：MySQL 5.7支持with cte吗？

https://w3schools.tech/tutorial/sql/sql-common-table-expression

当然可以！下面是对 `WITH` 子句（Common Table Expression，CTE） 的全面、深入、系统性详解，涵盖其概念、语法、用途、执行机制、优化器行为、递归用法以及与相关结构的对比。

#  `WITH` 子句（Common Table Expression, CTE）概念详解

## 一、什么是 CTE？

CTE（Common Table Expression） 是 SQL 中一种用于定义临时命名结果集的结构，它只在当前查询执行期间存在，语法上使用 `WITH` 关键字引入。

>  CTE = 一个可重用的“内联视图”或“命名子查询”

### 核心特点：
- 仅在单个 `SELECT`、`INSERT`、`UPDATE` 或 `DELETE` 语句中有效
- 提高复杂查询的可读性和模块化
- 可以递归调用自身（用于树形结构等场景）
- 被现代数据库广泛支持（MySQL 8.0+、PostgreSQL、SQL Server、Oracle、SQLite 等）

## 二、基本语法

```sql
WITH cte_name [(column1, column2, ...)] AS (
    -- 查询语句（可以是 SELECT、INSERT 等返回结果的语句）
    SELECT ...
)
-- 主查询中引用 CTE
SELECT * FROM cte_name;
```

### 示例：简单 CTE

```sql
WITH sales_summary AS (
    SELECT 
        region,
        SUM(amount) AS total_sales,
        COUNT(*) AS order_count
    FROM sales
    GROUP BY region
)
SELECT 
    region, 
    total_sales 
FROM sales_summary
WHERE total_sales > 10000;
```

## 三、CTE 的主要用途

### 1.  提升可读性：分解复杂查询

将一个多层嵌套的子查询拆分为逻辑清晰的步骤。

####  嵌套子查询（难读）：
```sql
SELECT region, total_sales
FROM (
    SELECT region, SUM(amount) AS total_sales
    FROM (
        SELECT * FROM sales WHERE status = 'completed'
    ) t1
    GROUP BY region
) t2
WHERE total_sales > 10000;
```

####  使用 CTE（清晰）：
```sql
WITH filtered_sales AS (
    SELECT * FROM sales WHERE status = 'completed'
),
region_summary AS (
    SELECT region, SUM(amount) AS total_sales
    FROM filtered_sales
    GROUP BY region
)
SELECT region, total_sales
FROM region_summary
WHERE total_sales > 10000;
```

### 2.  递归查询（Recursive CTE）

用于处理层次结构数据，如组织架构、目录树、BOM（物料清单）、路径遍历等。

#### 语法结构：
```sql
WITH RECURSIVE cte_name AS (
    -- 非递归部分（锚点）
    SELECT ... FROM table WHERE condition
    UNION ALL
    -- 递归部分
    SELECT ... FROM table JOIN cte_name ON ...
)
SELECT * FROM cte_name;
```

#### 示例：组织架构树（员工-上级关系）

```sql
WITH RECURSIVE org_tree AS (
    -- 锚点：从 CEO 开始
    SELECT id, name, manager_id, 0 AS level
    FROM employees
    WHERE manager_id IS NULL

    UNION ALL

    -- 递归：逐层向下
    SELECT e.id, e.name, e.manager_id, ot.level + 1
    FROM employees e
    JOIN org_tree ot ON e.manager_id = ot.id
)
SELECT 
    REPEAT('  ', level) || name AS hierarchy,
    level
FROM org_tree;
```

输出示例：
```
CEO
  Manager A
    Employee 1
    Employee 2
  Manager B
    Employee 3
```

>  支持递归的数据库：PostgreSQL、SQL Server、Oracle、SQLite、MySQL 8.0+

### 3.  多次引用同一子查询

避免重复写相同的子查询逻辑。

```sql
WITH user_stats AS (
    SELECT 
        user_id,
        AVG(score) AS avg_score,
        COUNT(*) AS attempts
    FROM quiz_attempts
    GROUP BY user_id
)
SELECT 
    u.name,
    us.avg_score,
    us.attempts
FROM users u
JOIN user_stats us ON u.id = us.user_id
WHERE us.avg_score > 80

UNION ALL

SELECT 
    'Summary' AS name,
    AVG(avg_score),
    SUM(attempts)
FROM user_stats;
```

>  `user_stats` 被引用了两次，但只计算一次（如果被物化）

## 四、CTE 的执行机制（关键！）

###  1. CTE 不是物理表
- 它不是临时表，也不是物化视图
- 生命周期仅限于当前查询

###  2. 优化器会重写 CTE
这是你提到的核心点：

> “CTE 只是语法层面的结构，优化器会在执行前重写 SQL”

#### 优化器可能采取的策略：

| 策略 | 说明 |
|------|------|
| 内联展开（Inlining） | 将 CTE 内容直接插入主查询，像子查询一样处理（最常见） |
| 物化（Materialization） | 先执行 CTE，缓存结果，供后续引用（尤其是多次引用时） |
| 多次求值 | 每次引用都重新执行（某些数据库对简单 CTE 的处理方式） |

#### 示例：内联展开
原始 CTE：
```sql
WITH t AS (SELECT * FROM sales WHERE amount > 100)
SELECT * FROM t WHERE region = 'North';
```

优化器可能重写为：
```sql
SELECT * FROM (SELECT * FROM sales WHERE amount > 100) t
WHERE region = 'North';
```

甚至进一步优化为：
```sql
SELECT * FROM sales 
WHERE amount > 100 AND region = 'North';  -- 谓词下推
```

## 五、不同数据库的行为差异

| 数据库 | CTE 行为 | 控制物化 |
|--------|--------|----------|
| PostgreSQL | 默认可能物化，可用 `MATERIALIZED` / `NOT MATERIALIZED` 控制 |  |
| MySQL 8.0+ | 多数情况物化，复杂查询自动缓存 | （自动） |
| SQL Server | 通常内联，视为“命名子查询” | （可用 `OPTION` 提示） |
| Oracle | 可内联或物化，受优化器影响 | （可用 `INLINE` hint） |
| SQLite | 通常内联 |  |
| OceanBase / TiDB | 类似 MySQL，倾向于物化 |  |

## 六、CTE vs 子查询 vs 临时表

| 特性 | CTE | 子查询 | 临时表 |
|------|-----|--------|--------|
| 可读性 |  高（命名、模块化） |  低（嵌套深） |  高 |
| 可重用 |  可多次引用 |  每次需重写 |  可多次使用 |
| 性能 | 依赖优化器 | 通常内联 |  物理存储，可建索引 |
| 生命周期 | 当前查询 | 当前查询 | 当前会话或事务 |
| 递归支持 | （RECURSIVE） |  |  |
| 是否持久 |  |  | （会话级） |

## 七、使用建议与最佳实践

###  推荐使用CTE的场景：
- 复杂查询的逻辑分层
- 递归查询（树、图）
- 同一子查询被引用≥2次
- 团队协作，提高代码可维护性

###  注意事项：
- 不要假设CTE会“先执行”
- 不要依赖副作用（如日志插入）
- 关键性能SQL使用`EXPLAIN`查看执行计划
- 避免CTE中有副作用操作（如`INSERT ... RETURNING`在某些数据库中行为不确定）

## 八、高级技巧

### 1. 多个 CTE 连续定义
```sql
WITH
    step1 AS (SELECT ...),
    step2 AS (SELECT * FROM step1 WHERE ...),
    step3 AS (SELECT * FROM step2 JOIN ...)
SELECT * FROM step3;
```

### 2. CTE 与窗口函数结合
```sql
WITH ranked_sales AS (
    SELECT 
        product,
        amount,
        RANK() OVER (PARTITION BY category ORDER BY amount DESC) as rk
    FROM sales
)
SELECT product, amount
FROM ranked_sales
WHERE rk = 1;
```

##  总结
| 维度 | 说明 |
|------|------|
| 本质 | 语法层面的临时结果集，用于模块化 SQL |
| 执行 | 由优化器决定是否内联、物化或多次求值 |
| 优点 | 可读性强、支持递归、可重用 |
| 缺点 | 不保证执行顺序，性能依赖优化器 |
| 最佳实践 | 用于复杂查询分解，关键 SQL 查看执行计划 |

>  一句话总结：  
> CTE 是 SQL 的“函数式编程”思想体现——把复杂查询拆成可组合、可命名的小块，让代码更清晰，让优化器更聪明。

### mysql
#### mysql 5.7
不支持。

###  MySQL 5.7 不支持 `WITH` 子句（Common Table Expressions, CTE）。

###  正确答案：

- CTE（`WITH`）是从 MySQL 8.0 版本开始引入的。
- 如果你使用的是 MySQL 5.7 或更早版本，执行包含 `WITH` 的 SQL 语句会报语法错误，例如：

```sql
ERROR 1064 (42000): You have an error in your SQL syntax; 
check the manual that corresponds to your MySQL server version for the right syntax to use near 'WITH ...'
```

### 版本支持情况

| MySQL 版本 | 是否支持 CTE |
|-----------|---------------|
| MySQL 5.7 及以下 |  不支持 |
| MySQL 8.0+ |  支持（包括递归 CTE） |

>  CTE 功能在 MySQL 8.0.1（发布于 2018 年 4 月）中正式引入。

###  在 MySQL 5.7 中如何替代 CTE？

由于不支持 `WITH`，你可以使用以下方式来模拟 CTE 的功能：

#### 1. 使用派生表（子查询）

将 CTE 内容写成子查询嵌套在 `FROM` 中。

 示例：原本用 CTE

```sql
-- MySQL 8.0+ 写法（不适用于 5.7）
WITH sales_summary AS (
    SELECT region, SUM(amount) AS total
    FROM sales
    GROUP BY region
)
SELECT region, total FROM sales_summary WHERE total > 10000;
```

替代写法（适用于 MySQL 5.7）：

```sql
SELECT region, total
FROM (
    SELECT region, SUM(amount) AS total
    FROM sales
    GROUP BY region
) AS sales_summary
WHERE total > 10000;
```

#### 2. 使用临时表（Temporary Table）

如果子查询较复杂或需多次引用，可创建临时表。

```sql
-- 创建临时表
CREATE TEMPORARY TABLE sales_summary AS
SELECT region, SUM(amount) AS total
FROM sales
GROUP BY region;

-- 多次引用
SELECT region, total FROM sales_summary WHERE total > 10000;

-- 会话结束自动销毁，无需手动 DROP（也可显式删除）
-- DROP TEMPORARY TABLE sales_summary;
```

>  临时表只在当前会话有效，断开连接后自动删除。

#### 3. 使用视图（View）（适用于固定逻辑）

```sql
CREATE VIEW sales_summary AS
SELECT region, SUM(amount) AS total
FROM sales
GROUP BY region;

-- 使用
SELECT region, total FROM sales_summary WHERE total > 10000;
```

>  适合被多个查询复用的逻辑。

---

###  建议

- 如果你依赖 CTE 功能，建议升级到 MySQL 8.0+。
- 在 MySQL 5.7 中，优先使用子查询或临时表来实现等价逻辑。
- 避免在生产环境使用“模拟递归”的复杂存储过程，性能差且难维护。

###  总结

| 问题 | 回答 |
|------|------|
| MySQL 5.7 支持 `WITH` CTE 吗？ |  不支持 |
| CTE 从哪个版本开始支持？ |  MySQL 8.0.1 |
| 5.7 中如何替代？ | 使用子查询、临时表或视图 |
| 推荐做法 | 升级到 MySQL 8.0+ 以获得 CTE、窗口函数等现代 SQL 特性 |

