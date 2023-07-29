# SpringBoot实战

https://book.douban.com/subject/26857423/
知乎电子书

2016-9


JavaEE开发的颠覆者 Spring Boot实战  PDF清晰完整版.pdf

### 第2章　开发第一个应用程序


想要覆盖 Spring Boot 的自动配置，你所要做的仅仅是编写一个显式的配置。Spring Boot 会发现你的配置，随后降低自动配置的优先级，以你的配置为准。想弄明白这是如何实现的，让我们揭开 Spring Boot 自动配置的神秘面纱，看看它是如何运作的，以及它是怎么允许自己被覆盖的。

@ConditionalOnClass 注解后，你就应该知道 Classpath 里必须要有 @EnableWebSecurity 注解。 @ConditionalOnWebApplication 说明这必须是个 Web 应用程序。 @ConditionalOnMissingBean 注解才是我们的安全配置类代替 SpringBootWebSecurityConfiguration 的关键所在。

Spring Boot 应用程序有多种设置途径。Spring Boot 能从多种属性源获得属性，包括如下几处。

(1) 命令行参数

(2) java:comp/env 里的 JNDI 属性

(3) JVM 系统属性

(4) 操作系统环境变量

(5) 随机生成的带 random.* 前缀的属性（在设置其他属性时，可以引用它们，比如 ${random.long} ）

(6) 应用程序以外的 application.properties 或者 appliaction.yml 文件

(7) 打包在应用程序内的 application.properties 或者 appliaction.yml 文件

(8) 通过 @PropertySource 标注的属性源

(9) 默认属性这个列表按照优先级排序，也就是说，任何在高优先级属性源里设置的属性都会覆盖低优先级的相同属性。例如，命令行参数会覆盖其他属性源里的属性。

spring @Values注解是否生效？如何拍错？源码涉及到哪些类

actor还是啥，查看spring内部情况

Spring Boot 的 Actuator。它提供了很多生产级的特性，比如监控和度量 Spring Boot 应用程序。Actuator 的这些特性可以通过众多 REST 端点、远程 shell 和 JMX 获得。我们先来看看 Actuator 的 REST 端点，这种最为人所熟知的使用方式提供了最完整的功能。

spring-security-test

### 第3章　自定义配置





### 第4章　测试

sb启用springmvc项目





### 第5章　Groovy与Spring Boot CLI

5

### 第6章　在Spring Boot中使用Grails

6

### 第7章　深入Actuator

调试用的

### 第8章　部署Spring Boot应用程序

8

