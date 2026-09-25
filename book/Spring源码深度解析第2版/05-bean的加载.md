# 第 5 章 bean 的加载

> `getBean` → `doGetBean` → `createBean`：单例三级缓存、**循环依赖**、`FactoryBean`、依赖注入（`populateBean`）、初始化（`initializeBean`）、`BeanPostProcessor`。本章是全书最核心章。

## 一、核心精讲

### 5.1 🔧 三级缓存与循环依赖
- `singletonObjects`（成品）/ `earlySingletonObjects`（早期引用）/ `singletonFactories`（`ObjectFactory`）（🔧 三级缓存解决**单例 setter/字段注入**的循环依赖；**构造器注入**循环依赖无法解决，抛 `BeanCurrentlyInCreationException`）。

### 5.2 createBean 流程
- `createBeanInstance`（构造/工厂方法）→ `populateBean`（属性注入，含 `@Autowired` 的 `AutowiredAnnotationBeanPostProcessor`）→ `initializeBean`（`Aware` 回调 → `BeanPostProcessor.before` → `InitializingBean`/`init-method` → `after`）（🔧 AOP 代理通常在 `postProcessAfterInitialization` 生成）。

### 5.3 FactoryBean
- `getObject()` 产真正的 bean；取 FactoryBean 本身要加 `&` 前缀（`getBean("&xxx")`）（🔧 MyBatis `SqlSessionFactoryBean`、早期 `ProxyFactoryBean` 都用它）。

## 二、版本演进 / 论文 / 前沿

- 文献：Spring Reference（Bean Scopes / Dependencies）；`AbstractBeanFactory#doGetBean` 源码。
- 工业界：Spring Framework；循环依赖在 Spring Boot 2.6+ 默认**禁止**（`spring.main.allow-circular-references=false`）（🔧 倡导重构而非依赖容器兜底）。
- 开源 stars（2026-09）：spring-framework 61k.

## 三、常见误区

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "循环依赖都能解决" | 构造器注入不行 |
| 2 | "getBean(&x) 取产品" | & 取 FactoryBean 本身 |
| 3 | "Boot 默认允许循环依赖" | 2.6+ 默认禁止 |
