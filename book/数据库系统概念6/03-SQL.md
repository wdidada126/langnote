# 第 3 章 SQL（基础）

> SQL 入门：DDL（`CREATE TABLE`/类型/完整性约束）、DML（`SELECT/FROM/WHERE`、`INSERT/UPDATE/DELETE`）、字符串/集合运算、聚合函数、`GROUP BY`/`HAVING`、`ORDER BY`、嵌套子查询。

## 一、核心精讲

### 3.1 🔧 查询语义顺序（易混）
- 书写顺序 `SELECT ... FROM ... WHERE ... GROUP BY ... HAVING ... ORDER BY`；**逻辑执行顺序**是 `FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY`（🔧 这解释了为什么 `WHERE` 不能用 `SELECT` 的别名，而 `ORDER BY` 可以）。

### 3.2 聚合与分组
- `COUNT/SUM/AVG/MIN/MAX`；`GROUP BY` 分组；`HAVING` 过滤**分组**（🔧 `WHERE` 过滤行、`HAVING` 过滤组；聚合忽略 NULL，`COUNT(*)` 除外）。

### 3.3 子查询
- 标量子查询、`IN`/`NOT IN`、`EXISTS`/`NOT EXISTS`、相关子查询（🔧 `NOT IN` 遇 NULL 会返回空集——经典陷阱，用 `NOT EXISTS` 更安全）。

## 二、版本演进 / 论文 / 前沿

- 论文/标准：SQL-86/92/99/2003/2011/2016/2023 标准；Chamberlin-Boyce SEQUEL（1974）。
- 工业界：PostgreSQL、MySQL；方言差异（🔧 如 `LIMIT` vs `TOP`/`ROWNUM`）。

## 三、常见误区

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "WHERE 能用 SELECT 别名" | 不能，ORDER BY 可以 |
| 2 | "NOT IN 安全" | 遇 NULL 空集，用 NOT EXISTS |
| 3 | "聚合含 NULL 计数" | 除 COUNT(*) 外忽略 NULL |
