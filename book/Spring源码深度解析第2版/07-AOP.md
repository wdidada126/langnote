# 第 7 章 AOP

> AOP 核心：切点（`Pointcut`）/通知（`Advice`）/切面（`Advisor`）、`ProxyFactory`、JDK 动态代理 vs CGLIB、`AnnotationAwareAspectJAutoProxyCreator`、织入时机。本书讲源码级代理创建。

## 一、核心精讲

### 7.1 🔧 两种代理
- **JDK 动态代理**：基于接口，`Proxy` + `InvocationHandler`（🔧 目标有接口时默认）；**CGLIB**：子类字节码增强（`MethodInterceptor`）（🔧 无接口或 `proxyTargetClass=true`；Spring 5.2+ 用 CGLIB 的 `Objenesis` 绕过构造；final 类/方法无法增强）。

### 7.2 织入时机
- `AnnotationAwareAspectJAutoProxyCreator` 是 `BeanPostProcessor`，在 `postProcessAfterInitialization` 里对匹配切点的 bean 生成代理（🔧 与第 5 章 createBean 衔接；这也解释了「自调用（this.xxx）不触发 AOP」——没走代理对象）。

### 7.3 通知类型
- `@Before`/`@After`/`@AfterReturning`/`@AfterThrowing`/`@Around`（🔧 `@Around` 最灵活，可控制是否执行目标；责任链是 `ReflectiveMethodInvocation` 递归）。

## 二、版本演进 / 论文 / 前沿

- 文献：Kiczales et al.《Aspect-Oriented Programming》(ECOOP'97)；AspectJ（Xerox PARC）；GoF 代理/装饰器模式（1994）。
- 工业界：Spring AOP（61k）、AspectJ（独立织入器，支持字段/构造器切点）；Micrometer/`@Transactional` 都基于 AOP。
- 开源 stars（2026-09）：spring-framework 61k / aspectj 关联.

## 三、常见误区

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "自调用触发 AOP" | 不触发，需走代理或 AopContext |
| 2 | "JDK 代理无限制" | 需接口；CGLIB 不能 final |
| 3 | "AOP 只在编译期" | Spring AOP 是运行期代理 |
