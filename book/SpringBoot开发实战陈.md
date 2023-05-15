# SpringBoot开发实战

知乎读书上有电子版

2018年的书
代码不是java的是grovvy的
https://book.douban.com/subject/30320873/

https://weread.qq.com/web/bookDetail/a6d32030715dbcb6a6d9015


第Ⅰ部分　Spring Boot框架基础
第1章　Spring Boot简介 2

第2章　快速开始HelloWorld 13


第3章　深入理解Spring Boot自动配置 23
重点

条件化Bean


在 Spring Boot 中，`@Conditional` 注解用于根据条件决定是否创建一个 Bean 或者是否加载一个配置类。Spring Boot 中提供了多个预定义的 `@Conditional` 注解，下面是这些注解的列表：

- `@ConditionalOnBean`：当容器中存在指定的 Bean 时，才会创建当前 Bean。
- `@ConditionalOnClass`：当类路径下存在指定的类时，才会创建当前 Bean。
- `@ConditionalOnExpression`：当指定的 SpEL 表达式计算结果为 true 时，才会创建当前 Bean。
- `@ConditionalOnJava`：当运行环境的 Java 版本符合指定条件时，才会创建当前 Bean。
- `@ConditionalOnJndi`：当 JNDI 中存在指定的资源时，才会创建当前 Bean。
- `@ConditionalOnMissingBean`：当容器中不存在指定的 Bean 时，才会创建当前 Bean。
- `@ConditionalOnMissingClass`：当类路径下不存在指定的类时，才会创建当前 Bean。
- `@ConditionalOnNotWebApplication`：当当前应用程序不是 Web 应用程序时，才会创建当前 Bean。
- `@ConditionalOnProperty`：当指定的配置属性存在且值符合指定条件时，才会创建当前 Bean。
- `@ConditionalOnResource`：当类路径下存在指定的资源时，才会创建当前 Bean。
- `@ConditionalOnSingleCandidate`：当容器中存在唯一的符合类型的 Bean 时，才会创建当前 Bean。
- `@ConditionalOnWebApplication`：当当前应用程序是 Web 应用程序时，才会创建当前 Bean。

这些注解可以单独使用，也可以组合使用，以实现更复杂的条件判断。在 Spring Boot 中，通过使用 `@Conditional` 注解，可以根据不同的条件来动态地创建和加载 Bean，从而实现更加灵活和可配置的应用程序。

第Ⅱ部分　Spring Boot项目综合实战
第4章　Spring Boot集成MyBatis数据库层开发 42

第5章　Spring Boot集成JPA数据库层开发 79

第6章　Spring Boot Gradle插件应用开发 110



第7章　使用Spring MVC开发Web应用 129
第8章　Spring Boot自定义Web MVC配置 146
第9章　Spring Boot中的AOP编程 170
第10章　Spring Boot集成Spring Security安全开发 193
第11章　Spring Boot集成React.js开发前后端分离项目 226

第12章　任务调度与邮件服务开发 236


第13章　Spring Boot集成WebFlux开发响应式Web应用 255

第14章　Spring Boot缓存 263



第15章　使用Spring Session集成Redis实现Session共享 273

第16章　使用Zuul开发API Gateway 286

第17章　Spring Boot日志 295

第Ⅲ部分　Spring Boot系统监控、测试与运维
第18章　Spring Boot应用的监控：Actuator与Admin 308

第19章　Spring Boot应用的测试 340



第20章　Spring Boot应用Docker化 348
