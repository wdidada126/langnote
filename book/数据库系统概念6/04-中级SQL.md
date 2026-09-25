# 第 4 章 中级 SQL

> 连接（`JOIN` 各类型/`USING`/`NATURAL`）、视图（`CREATE VIEW`、可更新视图/物化视图）、完整性约束（`NOT NULL`/`UNIQUE`/`CHECK`/`FOREIGN KEY ... REFERENCES`）、授权（`GRANT`/`REVOKE`/角色）、嵌入式 SQL、事务的初步引入。

## 一、核心精讲

### 4.1 🔧 连接类型
- `INNER JOIN`（内连接）、`LEFT/RIGHT/FULL OUTER JOIN`（外连接，保留未匹配侧补 NULL）、`CROSS JOIN`、`NATURAL JOIN`（🔧 `NATURAL JOIN` 自动按同名列连接，易因同名列变化导致语义突变，**生产慎用**）。

### 4.2 视图
- 视图是**虚拟表**（不存数据，查询时展开）；`WITH CHECK OPTION` 约束更新；**物化视图**才真正存数据（🔧 视图用于安全（隐藏列）/简化复杂查询；更新受限——含聚合/DISTINCT 的视图通常不可更新）。

### 4.3 完整性
- `CHECK`（行级/表级约束）、`UNIQUE`、`FOREIGN KEY ... ON DELETE CASCADE/SET NULL`（🔧 外键约束由 DBMS 检查，比应用层可靠）。

### 4.4 授权
- `GRANT SELECT ON t TO role`；`REVOKE`；角色聚合权限（🔧 最小权限原则）。

## 二、版本演进 / 论文 / 前沿

- 标准：SQL-92 引入 `JOIN` 语法；SQL:1999 引入触发器/递归查询。
- 工业界：物化视图（Oracle/PG）；行级安全 RLS（PG）。

## 三、常见误区

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "NATURAL JOIN 安全" | 同名列变化语义突变，慎用 |
| 2 | "视图存数据" | 虚拟；物化视图才存 |
| 3 | "约束放应用层" | 应放 DBMS 保一致 |
