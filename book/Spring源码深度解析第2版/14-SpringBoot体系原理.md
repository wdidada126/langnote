# 第 14 章 Spring Boot 体系原理

> Spring Boot 三大魔法：**自动配置**（`@EnableAutoConfiguration` + `spring.factories` + `@Conditional`）、**起步依赖**（starter）、**内嵌容器/Actuator**；`SpringApplication.run` 流程。本书收尾章，是从 Spring 到 Boot 的桥梁。

## 一、核心精讲

### 14.1 🔧 自动配置三要素
- `META-INF/spring.factories`（Boot 2.x）/ `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`（Boot 3.x）列出配置类；`@ConditionalOnClass`/`@ConditionalOnMissingBean`/`@ConditionalOnProperty` 等条件装配（🔧 「约定优于配置」：classpath 有某类就自动配，用户自定义 bean 则让位 `@ConditionalOnMissingBean`）。

### 14.2 SpringApplication.run 流程
- 创建 `ApplicationContext`（按 classpath 推断 Servlet/Reactive）→ 加载 `ApplicationContextInitializer`/`ApplicationListener` → `refresh()`（见第 6 章）→ `ApplicationRunner`/`CommandLineRunner`（🔧 Boot 把 Spring 容器的启动「产品化」了）。

### 14.3 起步依赖
- `spring-boot-starter-xxx` 只是一组**依赖聚合 POM**（🔧 不含代码；真正生效的是对应 autoconfigure 模块）。

## 二、版本演进 / 论文 / 前沿

- 文献：Spring Boot Reference；`@Conditional` 机制；Spring Boot 3 → Jakarta EE + **AOT/GraalVM Native**。
- 工业界：spring-boot（stars 2026-09：73k）；`spring-boot-autoconfigure`；Micrometer（4.8k）Actuator 指标。
- 前沿：Boot 3.2+ `spring.threads.virtual.enabled=true` 用**虚拟线程**处理请求（🔧 与并发系列呼应：Tomcat/Netty 请求线程变虚拟线程）。

## 三、常见误区

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "starter 里有代码" | 只是依赖聚合 POM |
| 2 | "自动配置不可覆盖" | 自定义 bean 优先（@ConditionalOnMissingBean） |
| 3 | "Boot 3 仍用 javax.*" | 已迁移 jakarta.* |
