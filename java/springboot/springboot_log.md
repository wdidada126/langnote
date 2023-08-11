# springboot_log

默认使用
spring-boot-starter-logging
对应slf4j + logback

如果要使用log4j2
spring-boot-starter-log4j2


Spring Boot使用Logback作为默认的日志框架，因此配置日志需要对Logback进行配置。

在Spring Boot中，可以通过在`application.properties`或`application.yml`文件中配置日志属性来控制日志输出。以下是一个示例`application.properties`文件，其中包含一些常见的日志配置属性：

```properties
# 日志级别配置
logging.level.root=INFO
logging.level.com.example=DEBUG

# 控制台输出配置
logging.pattern.console=%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n
logging.console.enabled=true

# 文件输出配置
logging.file.name=myapp.log
logging.file.path=/var/log/myapp
logging.pattern.file=%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n
logging.file.max-size=10MB
logging.file.max-history=7
```

在上面的示例中，`logging.level.root`属性设置了根日志记录器的日志级别为`INFO`，而`logging.level.com.example`属性设置了名为`com.example`的日志记录器的日志级别为`DEBUG`。可以根据自己的需要修改这些值。

`logging.pattern.console`属性和`logging.pattern.file`属性分别控制控制台输出和文件输出的日志格式。可以使用特定的格式化符号来定义自己的日志格式，例如`%d{HH:mm:ss.SSS}`表示输出日志的时间，`%thread`表示输出日志的线程名称，`%-5level`表示输出日志的级别，`%logger{36}`表示输出日志的记录器名称（最多显示36个字符），`%msg%n`表示输出日志的消息和换行符。

`logging.console.enabled`属性设置是否启用控制台输出。

`logging.file.name`属性和`logging.file.path`属性分别设置输出日志文件的名称和目录。`logging.file.max-size`属性和`logging.file.max-history`属性分别设置日志文件的最大大小和最大历史版本数。

除了在`application.properties`或`application.yml`文件中配置日志属性外，还可以通过编程方式配置日志。例如，可以使用`LoggerFactory`类获取日志记录器，并设置日志级别和输出格式等属性。


### spring-boot-starter-logging项目如何使用logback打印日志

logback-spring.xml

### 使用slf4j+logback
去掉spring-jcl


        <!--common-logging替换成slf4j-->
        <dependency>
            <groupId>org.slf4j</groupId>
            <artifactId>jcl-over-slf4j</artifactId>
            <version>1.7.25</version>
        </dependency>


application.properties设置

spring.profiles.active=dev

logback-spring.xml



springboot项目，如何读取 logback-spring.xml配置文件


springboot项目读取 logback-spring.xml配置文件的方法如下：
- 在 pom.xml 文件中添加 spring-boot-starter-web 依赖，它包含了 spring-boot-starter-logging 依赖，该依赖内容就是 Spring Boot 默认的日志框架 Logback+SLF4J²³。
- 在 application.properties 或 application.yml 文件中使用 logging.config 属性来指定 logback-spring.xml 配置文件的位置，可以是绝对路径或相对路径³⁴⁵。
- 在 logback-spring.xml 文件中，可以使用 <springProperty> 标签来引用 application.properties 或 application.yml 文件中的变量，如日志路径、日志级别等¹²⁵。
- 在 logback-spring.xml 文件中，可以使用 <springProfile> 标签来根据 Spring Boot 的 profile 功能来切换不同的日志配置²。
(1) logback整合Springboot及logback-spring.xml配置说明 - CSDN博客. https://blog.csdn.net/shanvlang/article/details/120196979.
(2) Spring Boot读取外部的 logback.xml 配置文件 - CSDN博客. https://blog.csdn.net/WC3312245110/article/details/121008564.
(3) SpringBoot项目在logback.xml中读取配置中的日志路径问题. https://blog.csdn.net/weimenglala/article/details/106164011.
(4) SpringBoot在logback.xml中读取application.properties中配置的日志路径 - 繁华一瞬间 - 博客园. https://www.cnblogs.com/xingfudexu/p/10374639.html.
(5) Spring Boot笔记-logback-spring.xml获取application.properties中的变量. https://bing.com/search?q=springboot%e9%a1%b9%e7%9b%ae%ef%bc%8c%e5%a6%82%e4%bd%95%e8%af%bb%e5%8f%96+logback-spring.xml%e9%85%8d%e7%bd%ae%e6%96%87%e4%bb%b6.



备注

logging.config配置项

LoggingApplicationListener的   public static final String CONFIG_PROPERTY = "logging.config";








```shell

============================
CONDITIONS EVALUATION REPORT
============================


Positive matches:
-----------------

   AuditAutoConfiguration#auditListener matched:
      - @ConditionalOnMissingBean (types: org.springframework.boot.actuate.audit.listener.AbstractAuditListener; SearchStrategy: all) did not find any beans (OnBeanCondition)

Negative matches:
-----------------

   ActiveMQAutoConfiguration:
      Did not match:
         - @ConditionalOnClass did not find required classes 'javax.jms.ConnectionFactory', 'org.apache.activemq.ActiveMQConnectionFactory' (OnClassCondition)

```

CONDITIONS EVALUATION REPORT的作用如下：

- CONDITIONS EVALUATION REPORT是一个条件评估报告，用于显示 Spring Boot 应用在启动时匹配的自动配置类和条件¹²³。
- CONDITIONS EVALUATION REPORT可以帮助开发者了解 Spring Boot 应用的配置情况，以及为什么某些自动配置类被激活或排除¹²³。
- CONDITIONS EVALUATION REPORT默认在日志级别为 DEBUG 时打印，如果不想看到这些信息，可以在配置文件中设置 logging.level.org.springframework.boot.autoconfigure 为 INFO 或 ERROR¹²⁴。


### 源代码分包解析

https://docs.spring.io/spring-boot/docs/2.3.x/api/



org.springframework.boot.logging包自动注入spring ioc容器的类有哪些，源码中在哪个类方法中注入的

org.springframework.boot.logging包中自动注入Spring IoC容器的主要类有:

1. LoggingApplicationListener

这个类会在Spring ApplicationContext创建后自动调用,它会设置日志系统,并将日志配置环境信息打印到控制台。

它是通过org.springframework.context.event.EventListener注解自动注册的:

@EventListener(ApplicationStartedEvent.class)
public void onApplicationStartedEvent(ApplicationStartedEvent event) {
  // 日志初始化代码
}

2. LoggingSystem

这个类封装了日志系统的初始化逻辑,它会被LoggingApplicationListener自动注入使用。

它通过@Component注解自动注册:

@Component
public class LoggingSystem {
  // 日志系统初始化代码
}  

org.springframework.boot.context.logging.LoggingApplicationListener#onApplicationStartingEvent   调用LoggingSystem beforeInitialize()



3. LogFile

这个类代表日志文件,也通过@Component注册。

其他一些辅助类如LogLevel、LoggingConverter等也都是通过@Component自动注册的。

所以综上,org.springframework.boot.logging包通过@Component、@EventListener等注解实现了组件的自动注册,使得日志模块可以自动集成到Spring Boot应用中,这也是Spring Boot自动配置的核心方式之一。



org.springframework.boot.context.logging.LoggingApplicationListener#initialize

配置







spring boot log配置项？



Spring Boot中提供了丰富的日志配置项,可以通过application.properties或application.yml进行设置。

常见的日志配置项包括:

- logging.file - 设置日志文件的名称,如logging.file=app.log

- logging.path - 设置日志文件的路径,如logging.path=/var/log

- logging.pattern.console - 设置控制台日志的格式 pattern

- logging.pattern.file - 设置文件日志的格式 pattern

- logging.level - 设置日志级别,可以针对路径或Logger名称,如logging.level.root=WARN

- logging.charset - 设置日志的编码,如logging.charset=UTF-8 

- logging.max-size - 设置日志文件的最大大小,如logging.max-size=10MB

- logging.max-history - 设置最大归档日志文件数,如logging.max-history=30

此外,Spring Boot也支持更详细的自定义日志配置:

- logging.config - 指定日志配置文件位置

- logging.exception-conversion-word - 设置日志打印异常时的转换词,如logging.exception-conversion-word=%wEx

- logging.redis.channel - 设置Redis日志记录通道

- logging.logstash.* - 设置Logstash配置

- logging.logback.* - 设置Logback配置

- logging.log4j2.* - 设置Log4j2配置

通过这些配置,Spring Boot为日志提供了自动配置的同时,也给予了用户更大的自定义空间。





### org.springframework.boot.logging

| org.springframework.boot.logging | 类型     | 说明                              |
| -------------------------------- | -------- | --------------------------------- |
| AbstractLoggingSystem            |          |                                   |
| AbstractLoggingSystem.LogLevels  |          |                                   |
| DeferredLog                      |          |                                   |
| LogFile                          |          | 重要 有配置项 logging.file.name等 |
| LoggerConfiguration              |          |                                   |
| LoggerConfigurationComparator    | 私有类   |                                   |
| LoggerGroup                      | final    | implements Iterable<LoggerGroup>  |
| LoggerGroups                     |          |                                   |
| LoggingInitializationContext     | context  |                                   |
| LoggingSystem                    | abstract | 重要 见上面 子类JavaLoggingSystem |
| LoggingSystemProperties          |          | 有属性 Environment environment    |
| Slf4JLoggingSystem               | abstract |                                   |
|                                  |          |                                   |
| LogLevel                         |          |                                   |

LogLevel 在LoggerConfiguration中用

LoggerConfiguration在JavaLoggingSystem 中用



LoggingSystem (org.springframework.boot.logging)
    AbstractLoggingSystem (org.springframework.boot.logging)
        JavaLoggingSystem (org.springframework.boot.logging.java)
        Slf4JLoggingSystem (org.springframework.boot.logging)
            Log4J2LoggingSystem (org.springframework.boot.logging.log4j2)
            LogbackLoggingSystem (org.springframework.boot.logging.logback)



### org.springframework.boot.logging.java

| org.springframework.boot.logging.java | 类型 | 说明                            |
| ------------------------------------- | ---- | ------------------------------- |
| JavaLoggingSystem                     |      |                                 |
| SimpleFormatter                       |      | 继承java.util.logging.Formatter |

JavaLoggingSystem是子类



有配置文件



logging.properties



```shell
handlers =java.util.logging.ConsoleHandler
```



### org.springframework.boot.logging.log4j2

| org.springframework.boot.logging.log4j2     | 类型 | 说明 |
| ------------------------------------------- | ---- | ---- |
| ColorConverter                              |      |      |
| ExtendedWhitespaceThrowablePatternConverter |      |      |
| Log4J2LoggingSystem                         |      |      |
| SpringBootConfigurationFactory              |      |      |
| WhitespaceThrowablePatternConverter         |      |      |


### org.springframework.boot.logging.logback 

| org.springframework.boot.logging.logback  | 类型 | 说明                              |
| ----------------------------------------- | ---- | --------------------------------- |
| ColorConverter                            |      | CompositeConverter<ILoggingEvent> |
| DebugLogbackConfigurator                  |      |                                   |
| DefaultLogbackConfiguration               |      |                                   |
| ExtendedWhitespaceThrowableProxyConverter |      |                                   |
| LogbackConfigurator                       |      |                                   |
| LogbackConfigurator.ShutdownHandler       |      |                                   |
| LogbackLoggingSystem                      |      |                                   |
| WhitespaceThrowableProxyConverter         |      |                                   |

