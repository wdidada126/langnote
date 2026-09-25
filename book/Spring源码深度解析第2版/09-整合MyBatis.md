# 第 9 章 整合 MyBatis

> `mybatis-spring` 桥接：`SqlSessionFactoryBean`（`FactoryBean`）、`SqlSessionTemplate`（线程安全代理）、`MapperFactoryBean`/`MapperScannerConfigurer`（接口生成代理注入 Spring）、事务交给 Spring（`SqlSession` 与 Spring 事务同步）。本章是「ORM 与 Spring 容器整合范式」的典型。

## 一、核心精讲

### 9.1 🔧 SqlSessionFactoryBean
- 实现 `FactoryBean<SqlSessionFactory>`：把 MyBatis 的 `SqlSessionFactory` 构建过程（XML/Configuration）纳入 Spring 生命周期（🔧 见第 5 章 FactoryBean；取工厂本身用 `&`）。

### 9.2 SqlSessionTemplate 的线程安全
- MyBatis 原生 `SqlSession` **非线程安全**；`SqlSessionTemplate` 用 JDK 动态代理，每次方法调用取当前线程绑定的 session（或新建后关闭）（🔧 与 Spring 事务同步：事务内复用同一 session 并延迟关闭，交给 Spring 提交/回滚）。

### 9.3 Mapper 接口注入
- `MapperFactoryBean` 用 MyBatis 的 `MapperProxy`（JDK 代理）把**接口**变成 bean；`MapperScannerConfigurer`（`BeanDefinitionRegistryPostProcessor`）批量扫描注册（🔧 与第 6 章的 `BeanFactoryPostProcessor` 呼应：这是「改定义」而非「改实例」）。

## 二、版本演进 / 论文 / 前沿

- 文献：MyBatis 官方文档；mybatis-spring；Spring Reference（ORM integration）。
- 工业界：MyBatis（stars 2026-09：17k）、MyBatis-Plus（国产增强，16k）、mybatis-spring-boot-starter。
- 开源 stars（2026-09）：mybatis 17k / mybatis-plus 16k.

## 三、常见误区

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "SqlSession 直接注入共享" | 非线程安全，用 SqlSessionTemplate |
| 2 | "Mapper 是类" | 接口，靠 MapperProxy 代理 |
| 3 | "MyBatis 自己管事务" | 交给 Spring 事务同步 |
