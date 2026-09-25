# 第 8 章 数据库连接 JDBC

> Spring JDBC 封装：`JdbcTemplate`（模板方法 + 回调）、`DataSource`、连接获取（`DataSourceUtils`/事务绑定）、异常转换（`SQLExceptionTranslator`）、`NamedParameterJdbcTemplate`。本章讲「Spring 如何消除 JDBC 样板代码」。

## 一、核心精讲

### 8.1 🔧 模板方法 + 回调
- `JdbcTemplate` 固定流程（获取连接 → 创建 Statement → 执行 → 处理 `ResultSet` → 释放 → 异常转换），变化部分由回调（`PreparedStatementCreator`/`RowMapper`/`ResultSetExtractor`）注入（🔧 GoF 模板方法模式；消除了 try-catch-finally 样板）。

### 8.2 连接与事务绑定
- 无事务时直接向 `DataSource` 取；有事务时 `DataSourceUtils` 会复用 **事务绑定在当前线程** 的连接（🔧 靠 `TransactionSynchronizationManager` 的 `ThreadLocal`；这就是 Spring 事务内多次 DB 访问用同一连接的原因，见第 10 章）。

### 8.3 异常转换
- `SQLErrorCodeSQLExceptionTranslator` 把各厂商 `SQLException`（错误码/`SQLState`）转成 Spring 统一的 `DataAccessException` 体系（🔧 与具体数据库解耦；注意与并发系列的 `ThreadLocal` 泄漏同源风险——但这里由框架管理）。

## 二、版本演进 / 论文 / 前沿

- 文献：GoF 模板方法（1994）；Spring Reference（Data Access）；JDBC 规范（JSR 221）。
- 工业界：HikariCP（连接池首选，stars 2026-09：17k）、spring-jdbc、R2DBC（响应式关系型）。
- 开源 stars（2026-09）：spring-framework 61k / HikariCP 17k.

## 三、常见误区

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "自己写 JDBC 样板" | 用 JdbcTemplate |
| 2 | "事务内多次 DB 用不同连接" | 复用线程绑定连接 |
| 3 | "SQLException 直接抛" | 转 DataAccessException |
