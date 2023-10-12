# Spring Boot

SpringBoot从配置文件中获取属性的四种方法
https://wenku.baidu.com/view/de957e73ae02de80d4d8d15abe23482fb5da0252.html

java代码 Boolean 默认 false
bool 没有默认值

Integer
int 

任何Java框架 都可以用spring boot启动，兼容层

/** fastJson 配置信息 **/
@Bean
public HttpMessageConverters fastJsonConfig(){

    //新建fast-json转换器
    FastJsonHttpMessageConverter converter = new FastJsonHttpMessageConverter();

    //fast-json 配置信息
    FastJsonConfig config = new FastJsonConfig();
    config.setDateFormat("yyyy-MM-dd HH:mm:ss");
    converter.setFastJsonConfig(config);

    //设置响应的 Content-Type
    converter.setSupportedMediaTypes(Arrays.asList(new MediaType[]{MediaType.APPLICATION_JSON, MediaType.APPLICATION_JSON_UTF8}));
    return new HttpMessageConverters(converter);
}


SpringBoot使用fastJson作为json解析框架
https://www.bbsmax.com/A/kmzLk0aKdG/

https://docs.spring.io/spring-boot/docs/2.7.14/reference/html/using.html#using.devtools.property-defaults


https://docs.spring.io/spring-boot/docs/2.7.14/reference/pdf/spring-boot-reference.pdf

windows电脑上有spring-boot-reference.pdf
## springboot官方文档笔记

## Chapter 7. Core Features
### 7.1. SpringApplication
#### 7.1.4. Customizing SpringApplication

7.1.1. Startup Failure
org.springframework.boot.diagnostics.FailureAnalyzers
FailureAnalyzers子类

org.springframework.boot.autoconfigure.logging.ConditionEvaluationReportLoggingListener

java -jar myproject-0.0.1-SNAPSHOT.jar --debug

7.1.2. Lazy Initialization

spring.main.lazy-initialization=true

7.1.3. Customizing the Banner

org.springframework.boot.loader.JarLauncher

7.1.4. Customizing SpringApplication
  application.setBannerMode(Banner.Mode.OFF);

7.1.5. Fluent Builder API

```java
new SpringApplicationBuilder()
  .sources(Parent.class)
  .child(Application.class)
  .bannerMode(Banner.Mode.OFF)
  .run(args);
```

7.1.6. Application Availability

ApplicationAvailability
org.springframework.boot.availability.ApplicationAvailability

CommandLineRunner
ApplicationRunner

7.1.7. Application Events and Listeners
ContextRefreshedEvent

META-INF/spring.factories

ApplicationStartingEvent
ApplicationEnvironmentPreparedEvent
ApplicationContextInitializedEvent
ApplicationPreparedEvent
ApplicationStartedEvent
AvailabilityChangeEvent
ApplicationReadyEvent
AvailabilityChangeEvent
ApplicationFailedEvent


7.1.8. Web Environment

AnnotationConfigServletWebServerApplicationContext
AnnotationConfigReactiveWebServerApplicationContext
AnnotationConfigApplicationContext

7.1.9. Accessing Application Arguments

org.springframework.boot.ApplicationArguments

7.1.10. Using the ApplicationRunner or CommandLineRunner

CommandLineRunner ApplicationRunner

7.1.11. Application Exit

org.springframework.boot.ExitCodeGenerator

7.1.12. Admin Features

7.1.13. Application Startup tracking

ApplicationStartup

BufferingApplicationStartup

org.springframework.boot.context.metrics.buffering.BufferingApplicationStartup
FlightRecorderApplicationStartup

7.2. Externalized Configuration

@Value注解获取Environment对象的值

@ConfigurationProperties 使用
PropertySource

变量的顺序

7.2.1. Accessing Command Line Properties
7.2.2. JSON Application Properties
7.2.3. External Application Properties
7.2.4. Encrypting Properties
7.2.5. Working With YAML
7.2.6. Configuring Random Values
7.2.7. Configuring System Environment Properties
7.2.8. Type-safe Configuration Properties

7.3. Profiles
7.3.1. Adding Active Profiles
7.3.2. Profile Groups

7.3.3. Programmatically Setting Profiles

ConfigurableEnvironment

7.3.4. Profile-specific Configuration Files

@ConfigurationProperties

7.4. Logging

7.4.9. Logback Extensions

logback-spring.xml
7.5. Internationalization

messages.properties


MessageSource

7.6. JSON

7.6.1. Jackson

7.6.2. Gson
GsonBuilderCustomizer


7.6.3. JSON-B

Jsonb

7.7. Task Execution and Scheduling

ThreadPoolTaskExecutor
org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor

AsyncTaskExecutor


AsyncConfigurer

TaskExecutorBuilder

ThreadPoolTaskScheduler
TaskSchedulerBuilder
@EnableScheduling

spring.task.scheduling namespace


7.8. Testing

jar包 spring-boot-test  spring-boot test-autoconfigure

spring-boot-starter-test

7.8.1. Test Scope Dependencies


The spring-boot-starter-test “Starter” (in the test scope) contains the following provided libraries:
• JUnit 5: The de-facto standard for unit testing Java applications.
• Spring Test & Spring Boot Test: Utilities and integration test support for Spring Boot
applications.
• AssertJ: A fluent assertion library.
• Hamcrest: A library of matcher objects (also known as constraints or predicates).
• Mockito: A Java mocking framework.
• JSONassert: An assertion library for JSON.
• JsonPath: XPath for JSON.

7.8.2. Testing Spring Applications

7.9. Creating Your Own Auto-configuration

7.9.1. Understanding Auto-configured Beans
@AutoConfiguration
@Configuration
@Conditional
@ConditionalOnClass
@ConditionalOnMissingBean

META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports

7.9.2. Locating Auto-configuration Candidates

META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports


@AutoConfiguration
@AutoConfigureBefore @AutoConfigureAfter

WebMvcAutoConfiguration

@AutoConfigureOrder

7.9.3. Condition Annotations

• Class Conditions
• Bean Conditions
• Property Conditions
• Resource Conditions
• Web Application Conditions
• SpEL Expression Conditions


7.9.4. Testing your Auto-configuration
7.9.5. Creating Your Own Starter


7.10. Kotlin Support

7.11. What to Read Next

Chapter 8. Web
8.1. Servlet Web Applications
8.1.1. The “Spring Web MVC Framework”
8.1.2. JAX-RS and Jersey
8.1.3. Embedded Servlet Container Support

8.2. Reactive Web Applications

8.2.1. The “Spring WebFlux Framework”
8.2.2. Embedded Reactive Server Support
8.2.3. Reactive Server Resources Configuration

8.3. Graceful Shutdown


8.4. Spring Security


8.4.1. MVC Security
8.4.2. WebFlux Security
8.4.3. OAuth2

8.4.4. SAML 2.0

8.5. Spring Session
8.6. Spring for GraphQL
8.6.1. GraphQL Schema
8.6.2. GraphQL RuntimeWiring
8.6.3. Querydsl and QueryByExample Repositories Support
8.6.4. Transports
8.6.5. Exception Handling
8.6.6. GraphiQL and Schema printer
8.7. Spring HATEOAS

8.8. What to Read Next

数据技术
消息系统

data technologies,
messaging systems

Chapter 9. Data
9.1. SQL Database
9.1.1. Configure a DataSource
9.1.2. Using JdbcTemplate
9.1.3. JPA and Spring Data JPA
9.1.4. Spring Data JDBC
9.1.5. Using H2’s Web Console
9.1.6. Using jOOQ
9.1.7. Using R2DBC


9.2. Working with NoSQL Technologies
9.2.1. Redis
9.2.2. MongoDB
9.2.3. Neo4j
9.2.4. Solr
9.2.5. Elasticsearch
9.2.6. Cassandra
9.2.8. LDAP
9.2.9. InfluxDB
9.3. What to Read Nex
Chapter 10. Messaging
10.1. JMS
javax.jms.ConnectionFactory
javax.jms.Connection
10.1.1. ActiveMQ Support
10.1.2. ActiveMQ Artemis Support
spring-boot-starter-artemis
org.apache.activemq:artemis-jmsserver
10.1.3. Using a JNDI ConnectionFactory
java:/JmsXA and java:/XAConnectionFactory
10.1.4. Sending a Message

JmsMessagingTemplate
DestinationResolver
MessageConverter

10.1.5. Receiving a Message

@JmsListener
JmsListenerContainerFactory
DestinationResolver  MessageConverter  javax.jms.ExceptionListener
JtaTransactionManager
@Transactional
JmsListenerContainerFactory

DefaultJmsListenerContainerFactoryConfigurer

10.2. AMQP

10.2.1. RabbitMQ Support

10.2.2. Sending a Message

10.2.3. Sending a Message To A Stream

10.2.4. Receiving a Message
10.3. Apache Kafka Support
10.3.1. Sending a Message
10.3.2. Receiving a Message
10.3.3. Kafka Streams

10.3.4. Additional Kafka Properties
10.3.5. Testing with Embedded Kafka

10.4. RSocket

10.4.1. RSocket Strategies Auto-configuration
10.4.2. RSocket server Auto-configuration
10.4.3. Spring Messaging RSocket support
10.4.4. Calling RSocket Services with RSocketRequester

10.5. Spring Integration
10.6. WebSockets
10.7. What to Read Next

Chapter 11. IO
11.1. Caching
11.1.1. Supported Cache Providers

1. Generic
2. JCache (JSR-107) (EhCache 3, Hazelcast, Infinispan, and others)
3. EhCache 2.x
377
4. Hazelcast
5. Infinispan
6. Couchbase
7. Redis
8. Caffeine
9. Cache2k
10. Simple
11.2. Hazelcast

11.3. Quartz Scheduler

11.4. Sending Email
11.5. Validation
11.6. Calling REST Services
11.6.1. RestTemplate
11.6.2. WebClient
11.7. Web Services
11.7.1. Calling Web Services with WebServiceTemplate

11.8. Distributed Transactions With JTA
11.8.1. Using an Atomikos Transaction Manager
11.8.2. Using a Java EE Managed Transaction Manager
11.8.3. Mixing XA and Non-XA JMS Connections

11.8.4. Supporting an Alternative Embedded Transaction Manager

Chapter 12. Container Images

12.1. Efficient Container Images
12.1.1. Unpacking the Executable JAR
java org.springframework.boot.loader.JarLauncher
java -cp BOOT-INF/classes:BOOT-INF/lib/* com.example.MyApplication


12.1.2. Layering Docker Images
12.2. Dockerfiles
12.3. Cloud Native Buildpacks


Chapter 13. Production-ready Features
13.1. Enabling Production-ready Features
13.2. Endpoints
13.2.1. Enabling Endpoints

13.2.2. Exposing Endpoints
13.2.3. Security
13.2.4. Configuring Endpoints
13.2.5. Hypermedia for Actuator Web Endpoints
13.2.6. CORS Support
13.2.7. Implementing Custom Endpoints
13.2.8. Health Information
13.2.9. Kubernetes Probes
13.2.10. Application Information

spring-boot-starter-json

JsonSerializer 
JsonDeserializer

@JsonComponent

KeyDeserializer




13.3. Monitoring and Management Over HTTP
13.3.1. Customizing the Management Endpoint Paths 
13.3.2. Customizing the Management Server Port
13.3.3. Configuring Management-specific SSL 
13.3.4. Customizing the Management Server Address 
13.3.5. Disabling HTTP Endpoints
13.4. Monitoring and Management over JMX
13.4.1. Customizing MBean Names 
13.4.2. Disabling JMX Endpoints
13.4.3. Using Jolokia for JMX over HTTP 
Customizing Jolokia 
Disabling Jolokia
13.5. Loggers
13.5.1. Configure a Logger
13.6. Metrics 
13.6.1. Getting started
13.6.2. Supported Monitoring Systems
AppOptics 
Atlas
Datadog
Dynatrace
Elastic
Ganglia
Graphite
Humio
Influx
JMX
KairosDB 
New Relic
Prometheus
SignalFx
Simple
Stackdriver
StatsD
Wavefront
13.6.3. Supported Metrics and Meters
JVM Metrics
System Metrics
Application Startup Metrics
Logger Metrics
Task Execution and Scheduling Metrics
Spring MVC Metrics
Spring WebFlux Metrics
Jersey Server Metrics
HTTP Client Metrics
Tomcat Metrics
Cache Metrics
Spring GraphQL Metrics 
DataSource Metrics
Hibernate Metrics 
Spring Data Repository Metrics
RabbitMQ Metrics
Spring Integration Metrics
Kafka Metrics
MongoDB Metrics 
Jetty Metrics
@Timed Annotation Support
Redis Metrics
13.6.4. Registering Custom Metrics
13.6.5. Customizing Individual Metrics
Common Tags
Per-meter Properties
13.6.6. Metrics Endpoint
13.7. Auditing
13.7.1. Custom Auditing
13.8. HTTP Tracing
13.8.1. Custom HTTP tracing
13.9. Process Monitoring
13.9.1. Extending Configuration
13.9.2. Programmatically Enabling Process Monitoring
13.10. Cloud Foundry Support
13.10.1. Disabling Extended Cloud Foundry Actuator Support
13.10.2. Cloud Foundry Self-signed Certificates
13.10.3. Custom Context Path
13.11. What to Read Next
14. Deploying Spring Boot Applications
14.1. Deploying to the Cloud
14.1.1. Cloud Foundry
Binding to Services
14.1.2. Kubernetes
Kubernetes Container Lifecycle
14.1.3. Heroku
14.1.4. OpenShift
14.1.5. Amazon Web Services (AWS) 
AWS Elastic Beanstalk
Summary
14.1.6. CloudCaptain and Amazon Web Services
14.1.7. Azure
14.1.8. Google Cloud
14.2. Installing Spring Boot Applications
14.2.1. Supported Operating Systems
14.2.2. Unix/Linux Services
Installation as an init.d Service (System V)
Installation as a systemd Service
Customizing the Startup Script
14.2.3. Microsoft Windows Services
14.3. What to Read Next
15. Spring Boot CLI
15.1. Installing the CLI
15.2. Using the CLI
15.2.1. Running Applications With the CLI
Deduced “grab” Dependencies
Deduced “grab” Coordinates
Default Import Statements
Automatic Main Method
Custom Dependency Management 
15.2.2. Applications With Multiple Source Files
15.2.3. Packaging Your Application
15.2.4. Initialize a New Project 
15.2.5. Using the Embedded Shell
15.2.6. Adding Extensions to the CLI
15.3. Developing Applications With the Groovy Beans DSL
15.4. Configuring the CLI With settings.xml
15.5. What to Read Next 
16. Build Tool Plugins 
16.1. Spring Boot Maven Plugin
16.2. Spring Boot Gradle Plugin
16.3. Spring Boot AntLib Module
16.3.1. Spring Boot Ant Tasks
Using the “exejar” Task
Examples 
16.3.2. Using the “findmainclass” Task
Examples
16.4. Supporting Other Build Systems
16.4.1. Repackaging Archives
16.4.2. Nested Libraries
16.4.3. Finding a Main Class 
16.4.4. Example Repackage Implementation 
16.5. What to Read Next 
17. “How-to” Guides 
17.1. Spring Boot Application
17.1.1. Create Your Own FailureAnalyzer
17.1.2. Troubleshoot Auto-configuration
17.1.3. Customize the Environment or ApplicationContext Before It Starts
17.1.4. Build an ApplicationContext Hierarchy (Adding a Parent or Root Context)
17.1.5. Create a Non-web Application
17.2. Properties and Configuration
17.2.1. Automatically Expand Properties at Build Time
Automatic Property Expansion Using Maven
Automatic Property Expansion Using Gradle
17.2.2. Externalize the Configuration of SpringApplication
17.2.3. Change the Location of External Properties of an Application
17.2.4. Use ‘Short’ Command Line Arguments
17.2.5. Use YAML for External Properties
17.2.6. Set the Active Spring Profiles
17.2.7. Set the Default Profile Name
17.2.8. Change Configuration Depending on the Environment
17.2.9. Discover Built-in Options for External Properties
17.3. Embedded Web Servers
17.3.1. Use Another Web Server
17.3.2. Disabling the Web Server
17.3.3. Change the HTTP Port
17.3.4. Use a Random Unassigned HTTP Port
17.3.5. Discover the HTTP Port at Runtime
17.3.6. Enable HTTP Response Compression
17.3.7. Configure SSL
17.3.8. Configure HTTP/2
HTTP/2 With Tomcat
HTTP/2 With Jetty
HTTP/2 With Reactor Netty
HTTP/2 With Undertow
17.3.9. Configure the Web Server
17.3.10. Add a Servlet, Filter, or Listener to an Application
Add a Servlet, Filter, or Listener by Using a Spring Bean
Add Servlets, Filters, and Listeners by Using Classpath Scanning
17.3.11. Configure Access Logging
17.3.12. Running Behind a Front-end Proxy Server
Customize Tomcat’s Proxy Configuration
17.3.13. Enable Multiple Connectors with Tomcat 
17.3.14. Use Tomcat’s LegacyCookieProcessor 
17.3.15. Enable Tomcat’s MBean Registry
17.3.16. Enable Multiple Listeners with Undertow 
17.3.17. Create WebSocket Endpoints Using @ServerEndpoint 
17.4. Spring MVC 
17.4.1. Write a JSON REST Service
17.4.2. Write an XML REST Service
17.4.3. Customize the Jackson ObjectMapper
17.4.4. Customize the @ResponseBody Rendering
17.4.5. Handling Multipart File Uploads
17.4.6. Switch Off the Spring MVC DispatcherServlet 
17.4.7. Switch off the Default MVC Configuration
17.4.8. Customize ViewResolvers
17.5. Jersey
17.5.1. Secure Jersey endpoints with Spring Security
17.5.2. Use Jersey Alongside Another Web Framework
17.6. HTTP Clients
17.6.1. Configure RestTemplate to Use a Proxy
17.6.2. Configure the TcpClient used by a Reactor Netty-based WebClient 
17.7. Logging
17.7.1. Configure Logback for Logging
Configure Logback for File-only Output
17.7.2. Configure Log4j for Logging
Use YAML or JSON to Configure Log4j 2
Use Composite Configuration to Configure Log4j 2
17.8. Data Access
17.8.1. Configure a Custom DataSource
17.8.2. Configure Two DataSources
17.8.3. Use Spring Data Repositories
17.8.4. Separate @Entity Definitions from Spring Configuration
17.8.5. Configure JPA Properties
17.8.6. Configure Hibernate Naming Strategy
17.8.7. Configure Hibernate Second-Level Caching
17.8.8. Use Dependency Injection in Hibernate Components
17.8.9. Use a Custom EntityManagerFactory
17.8.10. Using Multiple EntityManagerFactories
17.8.11. Use a Traditional persistence.xml File
17.8.12. Use Spring Data JPA and Mongo Repositories
17.8.13. Customize Spring Data’s Web Support
17.8.14. Expose Spring Data Repositories as REST Endpoint
17.8.15. Configure a Component that is Used by JPA
17.8.16. Configure jOOQ with Two DataSources
17.9. Database Initialization
17.9.1. Initialize a Database Using JPA
17.9.2. Initialize a Database Using Hibernate
17.9.3. Initialize a Database Using Basic SQL Scripts
17.9.4. Initialize a Spring Batch Database
17.9.5. Use a Higher-level Database Migration Tool
Execute Flyway Database Migrations on Startup
Execute Liquibase Database Migrations on Startup
17.9.6. Depend Upon an Initialized Database
Detect a Database Initializer
Detect a Bean That Depends On Database Initialization
17.10. NoSQL
17.10.1. Use Jedis Instead of Lettuce
17.11. Messaging
17.11.1. Disable Transacted JMS Session
17.12. Batch Applications
17.12.1. Specifying a Batch Data Source
17.12.2. Running Spring Batch Jobs on Startup
17.12.3. Running From the Command Line
17.12.4. Storing the Job Repository
17.13. Actuator
17.13.1. Change the HTTP Port or Address of the Actuator Endpoints
17.13.2. Customize the ‘whitelabel’ Error Page
17.13.3. Sanitize Sensitive Values
Customizing Sanitization
17.13.4. Map Health Indicators to Micrometer Metrics
17.14. Security
17.14.1. Switch off the Spring Boot Security Configuration
17.14.2. Change the UserDetailsService and Add User Accounts
17.14.3. Enable HTTPS When Running behind a Proxy Server
17.15. Hot Swapping
17.15.1. Reload Static Content
17.15.2. Reload Templates without Restarting the Container
Thymeleaf Templates
FreeMarker Templates
Groovy Templates
17.15.3. Fast Application Restarts
17.15.4. Reload Java Classes without Restarting the Container
17.16. Testing
17.16.1. Testing With Spring Security
17.16.2. Use Testcontainers for Integration Testing
17.16.3. Structure @Configuration classes for inclusion in slice tests
17.17. Build
17.17.1. Generate Build Information
17.17.2. Generate Git Information
17.17.3. Customize Dependency Versions
17.17.4. Create an Executable JAR with Maven
17.17.5. Use a Spring Boot Application as a Dependency
17.17.6. Extract Specific Libraries When an Executable Jar Runs
17.17.7. Create a Non-executable JAR with Exclusions
17.17.8. Remote Debug a Spring Boot Application Started with Maven
17.17.9. Build an Executable Archive From Ant without Using spring-boot-antlib
17.18. Traditional Deployment
17.18.1. Create a Deployable War File
17.18.2. Convert an Existing Application to Spring Boot
17.18.3. Deploying a WAR to WebLogic




G:\source_code\spring-boot

spring boot 2.0.4 maven组织的，可以跳转

https://docs.spring.io/spring-boot/docs/2.3.x/api/

spring_boot.xlsx

spring-boot-2.7.11.jar!\META-INF\spring.factories
文件

## jar文件

- spring-boot
- spring-boot-autoconfigure
- spring-boot-starter  没有java文件
- spring-boot-starter-amqp  没有java文件
- spring-boot-starter-logging  没有java文件
- spring-boot-starter-test  没有java文件
- spring-boot-starter-validation  没有java文件
- spring-boot-test
- spring-boot-test-autoconfigure








从你提供的信息看,这些Spring Boot starter依赖项确实不包含Java源代码文件:
- spring-boot-starter: 这是核心的启动器,提供了自动配置的支持、日志和YAML。它不包含任何Java代码。
- spring-boot-starter-amqp: 提供了对Spring AMQP和RabbitMQ的自动配置。其代码在spring-amqp项目中。
- spring-boot-starter-logging: 提供了日志(Logback, Log4J2)的自动配置。其代码在spring-boot项目中。
- spring-boot-starter-test: 提供了测试支持,包含JUnit、Hamcrest、Mockito等。其代码在spring-boot项目中。
- spring-boot-starter-validation: 提供了Bean Validation(Hibernate Validator)的自动配置。其代码在hibernate-validator项目中。
这些启动器的作用是提供自动配置,减少手动设置的代码量。实际的功能实现代码存在于它们所依赖的其他项目中,而不是在启动器里面。这使得启动器能保持精简和专注于自动配置的目的。我们在使用Spring Boot时通常需要同时引入这些启动器依赖,它们会一起启用Spring Boot应用所需的常见功能。

AnnotationConfigServletWebApplicationContext
AnnotationConfigServletWebServerApplicationContext  区别 都是spring-boot包里面的

AnnotationConfigServletWebApplicationContext 和 AnnotationConfigServletWebServerApplicationContext 都是 Spring Framework 应用程序上下文，用于支持基于注解的 Spring Web 应用程序。

它们的主要区别在于应用程序运行的环境不同：

AnnotationConfigServletWebApplicationContext 用于 Web 应用程序运行在 Servlet 容器中的情况。它是基于 AnnotationConfigApplicationContext 实现的，但还添加了一些支持 Spring Web 应用程序的特定功能，例如处理 Web 请求和响应、处理静态资源等。它适用于通过 WAR 包部署的 Spring Web 应用程序。
AnnotationConfigServletWebServerApplicationContext 用于 Web 应用程序运行在嵌入式 Servlet 容器中的情况。它是基于 AnnotationConfigApplicationContext 实现的，但还添加了一些支持嵌入式 Servlet 容器的特定功能，例如创建和配置嵌入式 Servlet 容器、处理静态资源等。它适用于使用嵌入式 Tomcat、Jetty 或 Undertow 等容器运行的 Spring Web 应用程序。
因此，当您使用 Spring 框架开发 Web 应用程序时，您可以根据应用程序的部署方式来选择使用哪种应用程序上下文。如果您的应用程序将部署在 Servlet 容器中，您应该使用 AnnotationConfigServletWebApplicationContext；如果您的应用程序将嵌入在一个 Servlet 容器中，您应该使用 AnnotationConfigServletWebServerApplicationContext。


## ConditionalOnClass注解
@ConditionalOnClass(KafkaTemplate.class)


`@ConditionalOnClass` 是 Spring Boot 提供的一个条件注解，用于在特定的类存在时才加载一个 Bean 或配置类。具体来说，`@ConditionalOnClass` 的作用是检查当前 classpath 中是否存在指定的类，如果存在，则加载Bean或配置类，否则忽略加载。

`@ConditionalOnClass` 注解的使用方法如下：

```
@Configuration
@ConditionalOnClass(name = "com.example.MyClass")
public class MyConfiguration {
    @Bean
    public MyBean myBean() {
        return new MyBean();
    }
}
```
在这个例子中，我们定义了一个名为 `MyConfiguration` 的配置类，并使用 `@ConditionalOnClass` 注解指定了一个名为 `com.example.MyClass` 的类。这意味着，只有当 classpath 中存在 `com.example.MyClass` 类时，才会加载该配置类，并创建一个名为 `myBean()` 的 Bean。
需要注意的是，`@ConditionalOnClass` 注解只检查 classpath 中是否存在指定的类，而不会检查该类是否可以实例化或是否可用。因此，如果你的应用程序需要使用某个类，但该类不一定存在或可用，你应该使用更加复杂的条件注解来控制 Bean 的加载行为，例如 `@ConditionalOnMissingClass` 或 `@ConditionalOnExpression`。
总之，`@ConditionalOnClass` 注解是 Spring Boot 提供的一个条件注解，用于在特定的类存在时才加载一个 Bean 或配置类。使用该注解可以避免因缺少某个依赖而导致应用程序启动失败的问题。



`@ConditionalOnMissingBean` 是 Spring Boot 提供的一个条件注解，用于在当前上下文中不存在指定的 Bean 时才加载一个 Bean 或配置类。具体来说，`@ConditionalOnMissingBean` 的作用是检查当前上下文中是否已经存在指定名称或类型的 Bean，如果不存在，则加载 Bean 或配置类，否则忽略加载。
`@ConditionalOnMissingBean` 注解的使用方法如下：

```
@Configuration
public class MyConfiguration {
    @Bean
    @ConditionalOnMissingBean
    public MyBean myBean() {
        return new MyBean();
    }
}
```

在这个例子中，我们定义了一个名为 `MyConfiguration` 的配置类，并使用 `@ConditionalOnMissingBean` 注解表示只有在当前上下文中不存在类型为 `MyBean` 的 Bean 时，才会创建一个名为 `myBean()` 的 Bean。
需要注意的是，`@ConditionalOnMissingBean` 注解只检查当前上下文中是否已经存在指定名称或类型的 Bean，并不检查该 Bean 是否可以实例化或是否可用。因此，如果你的应用程序需要使用某个 Bean，但该 Bean 不一定存在或可用，你应该使用更加复杂的条件注解来控制 Bean 的加载行为，例如 `@ConditionalOnBean` 或 `@ConditionalOnExpression`。
总之，`@ConditionalOnMissingBean` 注解是 Spring Boot 提供的一个条件注解，用于在当前上下文中不存在指定的 Bean 时才加载一个 Bean 或配置类。使用该注解可以避免因重复定义 Bean 而导致应用程序启动失败的问题，并且可以在不影响现有 Bean 的情况下添加新的 Bean。

`@ConditionalOnMissingClass` 是 Spring Boot 提供的一个条件注解，用于在 classpath 中不存在指定的类时才加载一个 Bean 或配置类。具体来说，`@ConditionalOnMissingClass` 的作用是检查当前 classpath 中是否存在指定的类，如果不存在，则加载 Bean 或配置类，否则忽略加载。
`@ConditionalOnMissingClass` 注解的使用方法如下：

```
@Configuration
@ConditionalOnMissingClass("com.example.MyClass")
public class MyConfiguration {
    @Bean
    public MyBean myBean() {
        return new MyBean();
    }
}
```

在这个例子中，我们定义了一个名为 `MyConfiguration` 的配置类，并使用 `@ConditionalOnMissingClass` 注解指定了一个名为 `com.example.MyClass` 的类。这意味着，只有当 classpath 中不存在 `com.example.MyClass` 类时，才会加载该配置类，并创建一个名为 `myBean()` 的 Bean。
需要注意的是，`@ConditionalOnMissingClass` 注解只检查 classpath 中是否存在指定的类，而不会检查该类是否可以实例化或是否可用。因此，如果你的应用程序需要使用某个类，但该类不一定存在或可用，你应该使用更加复杂的条件注解来控制 Bean 的加载行为，例如 `@ConditionalOnClass` 或 `@ConditionalOnExpression`。
总之，`@ConditionalOnMissingClass` 注解是 Spring Boot 提供的一个条件注解，用于在 classpath 中不存在指定的类时才加载一个 Bean 或配置类。使用该注解可以避免因缺少某个依赖而导致应用程序启动失败的问题。

### SpringBootApplication注解
包括ComponentScan注解

Spring Boot 默认使用 Logback 作为日志框架

使用log4j2
https://developer.aliyun.com/article/757562


使用logback
https://www.jianshu.com/p/3a9e32d9d347

springboot 命令行运行
需要配置maven插件
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>

### spring-boot-maven-plugin
build-info：生成项目的构建信息文件 build-info.properties
repackage：这个是默认 goal，在 mvn package 执行之后，这个命令再次打包生成可执行的 jar，同时将 mvn package 生成的 jar 重命名为 *.origin
run：这个可以用来运行 Spring Boot 应用
start：这个在 mvn integration-test 阶段，进行 Spring Boot 应用生命周期的管理
stop：这个在 mvn integration-test 阶段，进行 Spring Boot 应用生命周期的管理


mvn package
java -jar

Spring Boot
配置mybatis

mybatis有三样 mybatis.xml Java接口 xxxMapper.xml文件
Application 上配置 @MapperSacn() 配置Java接口报名
application.yml 配置两个 一个是jdbc url 一个是xxxMapper.xml文件位置



Springboot中的@EnableAsync和@Async的作用和基本用法

https://blog.csdn.net/qq_38796327/article/details/90599867

### nosql

spring-boot-starter-data-solr

### Caching

Generic
JCache (JSR-107) (EhCache 3, Hazelcast, Infinispan, and others)
EhCache 2.x
Hazelcast
Infinispan
Couchbase
Redis
Caffeine
Simple


### jms


#### RestTemplate


#### WebClient
webflux类
Calling REST Services with WebClient

#### Validation JSR-303 Bean Validation 1.1 javax.validation @Validated
https://docs.spring.io/spring-boot/docs/2.1.11.RELEASE/reference/html/boot-features-validation.html

#### Logging

### WebClient
webflux类
Calling REST Services with WebClient

## Validation JSR-303 Bean Validation 1.1 javax.validation @Validated
https://docs.spring.io/spring-boot/docs/2.1.11.RELEASE/reference/html/boot-features-validation.html

## Logging

https://docs.spring.io/spring-boot/docs/2.1.11.RELEASE/reference/html/boot-features-logging.html

[Spring Boot干货系列：（十二）Spring Boot使用单元测试](http://tengj.top/2017/12/28/springboot12/)


org.springframework.context.annotation.AnnotationConfigApplicationContext

SpringBoot，没有commons log，会报错

SpringBoot
Spring依赖apache commons logging

在springboot中 ，也是使用的slf4j + logback?


http://blog.didispace.com/books/spring-boot-reference/IV.%20Spring%20Boot%20features/35.2%20Using%20a%20Bitronix%20transaction%20manager.html





### Connection to a JNDI DataSource

If you deploy your Spring Boot application to an Application Server, you might want to configure and manage your DataSource by using your Application Server’s built-in features and access it by using JNDI.

```shell
spring.datasource.jndi-name=java:jboss/datasources/customers
```







B站视频

写SpringBoot starter
## 源代码分包详解v2.3.4


### springboot 



https://docs.spring.io/spring-boot/docs/2.3.x/api/

|  org.springframework.boot    |  类型    | 笔记     |
| ---- | ---- | ---- |
|   SpringApplication   |      |      |
|      |      |      |
|      |      |      |



| org.springframework.boot.                  | 类型 | 笔记 |
| ------------------------------------------ | ---- | ---- |
| Interfaces                                 |      |      |
| ApplicationArguments                       |      | 实现类DefaultApplicationArguments     |
| ApplicationRunner                          |      |      |
| Banner                                     |      |      |
| CommandLineRunner                          |      |      |
| ExitCodeExceptionMapper                    |      |      |
| ExitCodeGenerator                          |      |      |
| LazyInitializationExcludeFilter            |      |      |
| SpringApplicationRunListener               |      |      |
| SpringBootExceptionReporter                |      |      |
|                                            |      |      |
| Classes                                    |      |      |
|                                            |      |      |
| DefaultApplicationArguments                |      |  实现了ApplicationArguments接口    |
| ExitCodeEvent                              |      |      |
| ImageBanner                                |      |      |
| LazyInitializationBeanFactoryPostProcessor |      |      |
| ResourceBanner                             |      |      |
| SpringApplication                          |      |      |
| SpringBootVersion                          |      |      |
|                                            |      |      |
| Enums                                      |      |      |
|                                            |      |      |
| Banner.Mode                                |      |      |
| ImageBanner.PixelMode                      |      |      |
| WebApplicationType                         |      |      |
|                                            |      |      |
| Annotation Types                           |      |      |
|                                            |      |      |
| SpringBootConfiguration                    |      |      |

Banner接口的实现类
SpringBootBanner (org.springframework.boot)
PrintedBanner in SpringApplicationBannerPrinter (org.springframework.boot)
Banners in SpringApplicationBannerPrinter (org.springframework.boot)
ResourceBanner (org.springframework.boot)
ImageBanner (org.springframework.boot)


SpringApplication有main函数，会启动两个Context

在 Spring Boot 框架中，`org.springframework.boot.LazyInitializationExcludeFilter` 类是用于指定不应懒加载的类的过滤器。懒加载（Lazy Initialization）是一种性能优化技术，它可以推迟对象的加载和初始化，直到实际需要的时候再进行。
在 Spring Boot 2.2 版本及之后，Spring Boot 引入了 "懒加载排除过滤器"，该过滤器允许您定义哪些类不应该被懒加载。这可以防止某些类的懒加载，以确保它们在应用程序启动时立即初始化，而不需要等到第一次使用时才初始化。
`LazyInitializationExcludeFilter` 类的主要作用是指定那些应该在应用程序启动时立即初始化的类，以避免在后续的请求或操作中引起懒加载导致的延迟。这对于某些特定场景很有用，例如避免在关键路径上的延迟。
您可以在 Spring Boot 的配置文件中使用 `spring.jpa.properties` 来指定这个过滤器。例如：

```properties
spring.jpa.properties.hibernate.bytecode.use_reflection_optimizer=false
spring.jpa.properties.org.springframework.boot.LazyInitializationExcludeFilter=com.example.MyClass1,com.example.MyClass2
```
上述配置中，`com.example.MyClass1` 和 `com.example.MyClass2` 是指定在启动时不应该进行懒加载的类。
请注意，确保在使用这个过滤器时明确理解您的应用程序需求，以便不会出现不必要的性能问题。


ApplicationRunner CommandLineRunner

自定义类实现ApplicationRunner，注入spring ioc容器，获取ApplicationArguments参数，ApplicationArguments对象的参数是哪儿来的  命令行中赋值的

要将自定义类实现 `ApplicationRunner` 并注入到 Spring IOC 容器中，你可以按照以下步骤进行操作：

1. 创建自定义类并实现 `ApplicationRunner` 接口：

   ````java
   import org.springframework.boot.ApplicationArguments;
   import org.springframework.boot.ApplicationRunner;
   import org.springframework.stereotype.Component;
   
   @Component
   public class MyApplicationRunner implements ApplicationRunner {
   
       @Override
       public void run(ApplicationArguments args) throws Exception {
           // 执行逻辑，使用 args 获取命令行参数
           String[] sourceArgs = args.getSourceArgs();
           // ...
       }
   }
   ```

   在上述示例中，我们创建了一个名为 `MyApplicationRunner` 的自定义类，并实现了 `ApplicationRunner` 接口。在 `run()` 方法中，你可以编写你的逻辑，通过 `args` 参数获取命令行参数。

   ````
   
   ````

1. 将自定义类注入到 Spring IOC 容器中：

   确保在你的 Spring Boot 项目中使用了组件扫描（`@ComponentScan`）或显式配置类（`@Configuration`）来启用自动扫描和注册组件的功能。这样，Spring Boot 将会自动扫描 `MyApplicationRunner` 类，并将其实例化为一个 Bean。

   如果你的自定义类不在主应用程序的包或子包中，你可能需要使用 `@ComponentScan` 注解来指定要扫描的包或类。

   ````java
   import org.springframework.boot.SpringApplication;
   import org.springframework.boot.autoconfigure.SpringBootApplication;
   
   @SpringBootApplication
   public class MyApplication {
       public static void main(String[] args) {
           SpringApplication.run(MyApplication.class, args);
       }
   }
   ```

   在主应用程序类中使用 `@SpringBootApplication` 注解标记你的应用程序类，并确保使用了 `SpringApplication.run()` 方法来启动应用程序。

   ````
   
   ````

1. 获取命令行参数：

   在 `MyApplicationRunner` 类的 `run()` 方法中，你可以使用 `args` 参数来获取命令行参数。`ApplicationArguments` 对象提供了多个方法来访问命令行参数，如 `getSourceArgs()` 返回一个字符串数组，包含原始的命令行参数。

   ````java
   @Override
   public void run(ApplicationArguments args) throws Exception {
       String[] sourceArgs = args.getSourceArgs();
       // ...
   }
   ```

   在上述示例中，我们使用 `getSourceArgs()` 方法获取原始的命令行参数，并将其保存在 `sourceArgs` 字符串数组中。

   ````
   `ApplicationArguments` 对象的参数是通过 Spring Boot 的启动类 `SpringApplication` 在启动过程中解析和收集的。它可以包含来自命令行的参数、配置文件中的参数等。
   请注意，在 Spring Boot 应用程序中，你也可以使用 `@Value` 注解来直接注入单个命令行参数，而不必实现 `ApplicationRunner` 接口。这种方式适用于获取单个参数的情况，例如 `java -jar myapp.jar --my.param=value` 中的 `--my.param=value`。
   总结起来，你可以创建一个实现 `ApplicationRunner` 接口的自定义类，并将其注入到 Spring IOC 容器中。通过 `ApplicationArguments` 对象，你可以获取 Spring Boot 应用程序启动时传递的命令行参数。
   ````

`ApplicationRunner` 和 `CommandLineRunner` 都是在 Spring Boot 应用程序启动时执行一些逻辑的接口，它们有以下区别：

1. **参数类型不同**：

   - `ApplicationRunner` 的 `run()` 方法接收一个 `ApplicationArguments` 对象作为参数，该对象提供了对应用程序启动时传递的命令行参数的访问。
   - `CommandLineRunner` 的 `run()` 方法接收一个 `String` 数组作为参数，该数组表示应用程序启动时传递的命令行参数。

1. **命令行参数的处理方式不同**：

   - `ApplicationRunner` 的 `ApplicationArguments` 对象提供了更丰富的命令行参数处理方法，如 `getOptionValues()`、`getOptionNames()`、`getNonOptionArgs()` 等，可以更灵活地访问和解析命令行参数。
   - `CommandLineRunner` 的 `String` 数组参数直接表示原始的命令行参数，你需要自行解析和处理这些参数。

1. **扩展性不同**：

   - `ApplicationRunner` 接口提供了更高级的扩展能力，因为它可以访问更多关于命令行参数的信息，并提供了更多方法来处理这些参数。
   - `CommandLineRunner` 接口的参数简单明了，适合处理简单的命令行参数情况。

在实际使用中，你可以根据具体的需求选择使用 `ApplicationRunner` 还是 `CommandLineRunner`。如果你需要更丰富的命令行参数处理能力，或者需要在应用程序启动时执行一些复杂的逻辑，那么 `ApplicationRunner` 可能更适合。而对于简单的命令行参数处理或逻辑执行，`CommandLineRunner` 也是一个很好的选择。

需要注意的是，你可以同时使用多个 `ApplicationRunner` 或 `CommandLineRunner` 实现类，它们将按照注册的顺序依次执行。
### org.springframework.boot.admin

| org.springframework.boot.admin        | 类型 | 笔记 |
| ------------------------------------- | ---- | ---- |
| Interfaces                            |      |      |
|                                       |      |      |
| SpringApplicationAdminMXBean          |      |      |
|                                       |      |      |
| Classes                               |      |      |
|                                       |      |      |
| SpringApplicationAdminMXBeanRegistrar |      |      |

### org.springframework.boot.ansi

| org.springframework.boot.ansi         | 类型 | 笔记 |
| ------------------------------------- | ---- | ---- |
| Interfaces                            |      |      |
|                                       |      |      |
| SpringApplicationAdminMXBean          |      |      |
|                                       |      |      |
| Classes                               |      |      |
|                                       |      |      |
| SpringApplicationAdminMXBeanRegistrar |      |      |


### org.springframework.boot.availability
| org.springframework.boot.availability | 类型 | 笔记 |
| ------------------------------------- | ---- | ---- |
| Interfaces                            |      |      |
|                                       |      |      |
| ApplicationAvailability               |      |      |
| AvailabilityState                     |      |      |
|                                       |      |      |
| Classes                               |      |      |
|                                       |      |      |
| ApplicationAvailabilityBean           |      |      |
| AvailabilityChangeEvent               |      |      |
|                                       |      |      |
| Enums                                 |      |      |
|                                       |      |      |
| LivenessState                         |      |      |
| ReadinessState                        |      |      |


### org.springframework.boot.builder

| org.springframework.boot.builder                             | 类型 | 笔记 |
| ------------------------------------------------------------ | ---- | ---- |
| ParentContextApplicationContextInitializer                   |      |      |
| ParentContextApplicationContextInitializer.ParentContextAvailableEvent |      |      |
| ParentContextCloserApplicationListener                       |      |      |
| ParentContextCloserApplicationListener.ContextCloserListener |      |      |
| SpringApplicationBuilder                                     |      |      |


### org.springframework.boot.cloud

| org.springframework.boot.cloud           | 类型 | 笔记 |
| ---------------------------------------- | ---- | ---- |
| Classes                                  |      |      |
|                                          |      |      |
| CloudFoundryVcapEnvironmentPostProcessor |      |      |
|                                          |      |      |
| Enums                                    |      |      |
|                                          |      |      |
| CloudPlatform                            |      |      |



### org.springframework.boot.context
| org.springframework.boot.context                             | 类型 | 笔记 |
| ------------------------------------------------------------ | ---- | ---- |
| Interfaces                                                   |      |      |
| ConfigurationWarningsApplicationContextInitializer.Check     |      |      |
|                                                              |      |      |
| Classes                                                      |      |      |
|                                                              |      |      |
| ApplicationPidFileWriter                                     |      |      |
| ConfigurationWarningsApplicationContextInitializer           |      |      |
| ConfigurationWarningsApplicationContextInitializer.ComponentScanPackageCheck |      |      |
| ConfigurationWarningsApplicationContextInitializer.ConfigurationWarningsPostProcessor |      |      |
| ContextIdApplicationContextInitializer                       |      |      |
| FileEncodingApplicationListener                              |      |      |
| TypeExcludeFilter                                            |      |      |



#### org.springframework.boot.context.annotation

| org.springframework.boot.context.annotation | 类型 | 笔记 |
| ------------------------------------------- | ---- | ---- |
| Interfaces                                  |      |      |
| DeterminableImports                         |      |      |
|                                             |      |      |
| Classes                                     |      |      |
|                                             |      |      |
| Configurations                              |      |      |
| UserConfigurations                          |      |      |



### org.springframework.boot.config
| org.springframework.boot.config         | 类型 | 笔记 |
| --------------------------------------- | ---- | ---- |
| Classes                                 |      |      |
| AnsiOutputApplicationListener           |      |      |
| ConfigFileApplicationListener           |      |      |
| DelegatingApplicationContextInitializer |      |      |
| DelegatingApplicationListener           |      |      |


#### org.springframework.boot.bind


| org.springframework.boot.bind           | 类型 | 笔记 |
| --------------------------------------- | ---- | ---- |
| Interfaces                              |      |      |
| BindConstructorProvider                 |      |      |
| BindContext                             |      |      |
| BindHandler                             |      |      |
| PlaceholdersResolver                    |      |      |
|                                         |      |      |
| Classes                                 |      |      |
|                                         |      |      |
| AbstractBindHandler                     |      |      |
| Bindable                                |      |      |
| Binder                                  |      |      |
| BindResult                              |      |      |
| BoundPropertiesTrackingBindHandler      |      |      |
| DataObjectPropertyName                  |      |      |
| PropertySourcesPlaceholdersResolver     |      |      |
|                                         |      |      |
| Exceptions                              |      |      |
|                                         |      |      |
| BindException                           |      |      |
| UnboundConfigurationPropertiesException |      |      |
|                                         |      |      |
| Annotation Types                        |      |      |
|                                         |      |      |
| DefaultValue                            |      |      |


#### org.springframework.boot.context

##### org.springframework.boot.context.event

| org.springframework.boot.context.event | 类型 | 笔记 |
| -------------------------------------- | ---- | ---- |
| Classes                                |      |      |
| ApplicationContextInitializedEvent     |      |      |
| ApplicationEnvironmentPreparedEvent    |      |      |
| ApplicationFailedEvent                 |      |      |
| ApplicationPreparedEvent               |      |      |
| ApplicationReadyEvent                  |      |      |
| ApplicationStartedEvent                |      |      |
| ApplicationStartingEvent               |      |      |
| EventPublishingRunListener             |      |      |
| SpringApplicationEvent                 |      |      |



#####  org.springframework.boot.context.logging


| org.springframework.boot.context.logging | 类型 | 笔记 |
| ---------------------------------------- | ---- | ---- |
| Classes                                  |      |      |
| ClasspathLoggingApplicationListener      |      |      |
| LoggingApplicationListener               |      |      |


LoggingApplicationListener初始化日志



##### org.springframework.boot.context.properties

| org.springframework.boot.context.properties | 类型 | 笔记 |
| ------------------------------------------- | ---- | ---- |
| Interfaces                                  |      |      |
| ConfigurationPropertiesBindHandlerAdvisor   |      |      |
| PropertyMapper.SourceOperator               |      |      |
|                                             |      |      |
| Classes                                     |      |      |
|                                             |      |      |
| BoundConfigurationProperties                |      |      |
| ConfigurationBeanFactoryMetadata            |      |      |
| ConfigurationPropertiesBean                 |      |      |
| ConfigurationPropertiesBindingPostProcessor |      |      |
| PropertyMapper                              |      |      |
| PropertyMapper.Source                       |      |      |
|                                             |      |      |
| Enums                                       |      |      |
|                                             |      |      |
| ConfigurationPropertiesBean.BindMethod      |      |      |
|                                             |      |      |
| Exceptions                                  |      |      |
|                                             |      |      |
| ConfigurationPropertiesBindException        |      |      |
|                                             |      |      |
| Annotation Types                            |      |      |
|                                             |      |      |
| ConfigurationProperties                     |      |      |
| ConfigurationPropertiesBinding              |      |      |
| ConfigurationPropertiesScan                 |      |      |
| ConstructorBinding                          |      |      |
| DeprecatedConfigurationProperty             |      |      |
| EnableConfigurationProperties               |      |      |
| NestedConfigurationProperty                 |      |      |



###### org.springframework.boot.context.properties.bind.handler


| org.springframework.boot.context.properties.bind.handler | 类型 | 笔记 |
| -------------------------------------------------------- | ---- | ---- |
| Classes                                                  |      |      |
| IgnoreErrorsBindHandler                                  |      |      |
| IgnoreTopLevelConverterNotFoundBindHandler               |      |      |
| NoUnboundElementsBindHandler                             |      |      |

###### org.springframework.boot.context.properties.bind.validation

| org.springframework.boot.context.properties.bind.validation | 类型 | 笔记 |
| ----------------------------------------------------------- | ---- | ---- |
| Classes                                                     |      |      |
| ValidationBindHandler                                       |      |      |
| ValidationErrors                                            |      |      |
|                                                             |      |      |
| Exceptions                                                  |      |      |
|                                                             |      |      |
| BindValidationException                                     |      |      |

#### org.springframework.boot.convert

| org.springframework.boot.convert | 类型 | 笔记 |
| -------------------------------- | ---- | ---- |
| Classes                          |      |      |
| ApplicationConversionService     |      |      |
|                                  |      |      |
| Enums                            |      |      |
|                                  |      |      |
| DurationStyle                    |      |      |
| PeriodStyle                      |      |      |
|                                  |      |      |
| Annotation Types                 |      |      |
|                                  |      |      |
| DataSizeUnit                     |      |      |
| Delimiter                        |      |      |
| DurationFormat                   |      |      |
| DurationUnit                     |      |      |
| PeriodFormat                     |      |      |
| PeriodUnit                       |      |      |



#### org.springframework.boot.diagnostics


| org.springframework.boot.diagnostics | 类型 | 笔记 |
| ------------------------------------ | ---- | ---- |
| Interfaces                           |      |      |
| FailureAnalysisReporter              |      |      |
| FailureAnalyzer                      |      |      |
|                                      |      |      |
| Classes                              |      |      |
|                                      |      |      |
| AbstractFailureAnalyzer              |      |      |
| FailureAnalysis                      |      |      |
| LoggingFailureAnalysisReporter       |      |      |



##### org.springframework.boot.diagnostics.analyzer


| org.springframework.boot.diagnostics.analyzer | 类型 | 笔记 |
| --------------------------------------------- | ---- | ---- |
| Classes                                       |      |      |
| AbstractInjectionFailureAnalyzer              |      |      |
| BeanNotOfRequiredTypeFailureAnalyzer          |      |      |


#### org.springframework.boot.env


|                                                              | 类型 | 说明 |      |      |      |      |
| ------------------------------------------------------------ | ---- | ---- | ---- | ---- | ---- | ---- |
| Interfaces                                                   |      |      |      |      |      |      |
| EnvironmentPostProcessor                                     |      |      |      |      |      |      |
| PropertySourceLoader                                         |      |      |      |      |      |      |
|                                                              |      |      |      |      |      |      |
| Classes                                                      |      |      |      |      |      |      |
|                                                              |      |      |      |      |      |      |
| OriginTrackedMapPropertySource                               |      |      |      |      |      |      |
| PropertiesPropertySourceLoader                               |      |      |      |      |      |      |
| RandomValuePropertySource                                    |      |      |      |      |      |      |
| SpringApplicationJsonEnvironmentPostProcessor                |      |      |      |      |      |      |
| SystemEnvironmentPropertySourceEnvironmentPostProcessor      |      |      |      |      |      |      |
| SystemEnvironmentPropertySourceEnvironmentPostProcessor.OriginAwareSystemEnvironmentPropertySource |      |      |      |      |      |      |
| YamlPropertySourceLoader                                     |      |      |      |      |      |      |





#### org.springframework.boot.info


|                      | 类型 | 笔记 |
| -------------------- | ---- | ---- |
| Classes              |      |      |
| BuildProperties      |      |      |
| GitProperties        |      |      |
| InfoProperties       |      |      |
| InfoProperties.Entry |      |      |


#### org.springframework.boot.jackson

|                        | 类型 | 笔记 |
| ---------------------- | ---- | ---- |
| Classes                |      |      |
| JsonComponentModule    |      |      |
| JsonObjectDeserializer |      |      |
| JsonObjectSerializer   |      |      |
|                        |      |      |
| Enums                  |      |      |
|                        |      |      |
| JsonComponent.Scope    |      |      |
|                        |      |      |
| Annotation Types       |      |      |
|                        |      |      |
| JsonComponent          |      |      |



#### org.springframework.boot.jdbc


|                               | 类型 | 笔记 |
| ----------------------------- | ---- | ---- |
| Interfaces                    |      |      |
| SchemaManagementProvider      |      |      |
| XADataSourceWrapper           |      |      |
|                               |      |      |
| Classes                       |      |      |
|                               |      |      |
| AbstractDataSourceInitializer |      |      |
| DataSourceBuilder             |      |      |
| DataSourceUnwrapper           |      |      |
|                               |      |      |
| Enums                         |      |      |
|                               |      |      |
| DatabaseDriver                |      |      |
| DataSourceInitializationMode  |      |      |
| EmbeddedDatabaseConnection    |      |      |
| SchemaManagement              |      |      |



##### org.springframework.boot.jdbc.metadata


|                                         | 类型 | 笔记 |
| --------------------------------------- | ---- | ---- |
| Interfaces                              |      |      |
| DataSourcePoolMetadata                  |      |      |
| DataSourcePoolMetadataProvider          |      |      |
|                                         |      |      |
| Classes                                 |      |      |
|                                         |      |      |
| AbstractDataSourcePoolMetadata          |      |      |
| CommonsDbcp2DataSourcePoolMetadata      |      |      |
| CompositeDataSourcePoolMetadataProvider |      |      |
| HikariDataSourcePoolMetadata            |      |      |
| TomcatDataSourcePoolMetadata            |      |      |

#### org.springframework.boot.jms

|  | 类型 | 笔记 |
|----------------------------|----------------------------|----------------------------|
| XAConnectionFactoryWrapper |  |  |



#### org.springframework.boot.json

|                    | 类型 | 笔记 |
| ------------------ | ---- | ---- |
| Interfaces         |      |      |
| JsonParser         |      |      |
|                    |      |      |
| Classes            |      |      |
|                    |      |      |
| AbstractJsonParser |      |      |
| BasicJsonParser    |      |      |
| GsonJsonParser     |      |      |
| JacksonJsonParser  |      |      |
| JsonParserFactory  |      |      |
| YamlJsonParser     |      |      |
|                    |      |      |
| Exceptions         |      |      |
|                    |      |      |
| JsonParseException |      |      |

#### org.springframework.boot.jta

##### org.springframework.boot.jta.atomikos





| org.springframework.boot.jta.atomikos     | 类型 | 笔记 |
| ----------------------------------------- | ---- | ---- |
| Classes                                   |      |      |
| AtomikosConnectionFactoryBean             |      |      |
| AtomikosDataSourceBean                    |      |      |
| AtomikosDependsOnBeanFactoryPostProcessor |      |      |
| AtomikosProperties                        |      |      |
| AtomikosProperties.Recovery               |      |      |
| AtomikosXAConnectionFactoryWrapper        |      |      |
| AtomikosXADataSourceWrapper               |      |      |



#### org.springframework.boot.liquibase

|                                                             | 类型 | 笔记 |
| ----------------------------------------------------------- | ---- | ---- |
| Classes                                                     |      |      |
| LiquibaseServiceLocatorApplicationListener                  |      |      |
| LiquibaseServiceLocatorApplicationListener.LiquibasePresent |      |      |
| SpringPackageScanClassResolver                              |      |      |

#### org.springframework.boot.logging



| org.springframework.boot.logging |      |      |
| -------------------------------- | ---- | ---- |
|                                  |      |      |
|                                  |      |      |
|                                  |      |      |



#### org.springframework.boot.origin

| org.springframework.boot.origin | 类型 | 笔记 |
| ------------------------------- | ---- | ---- |
| Interfaces                      |      |      |
| Origin                          |      |      |
| OriginLookup                    |      |      |
| OriginProvider                  |      |      |
|                                 |      |      |
| Classes                         |      |      |
|                                 |      |      |
| OriginTrackedValue              |      |      |
| PropertySourceOrigin            |      |      |
| SystemEnvironmentOrigin         |      |      |
| TextResourceOrigin              |      |      |
| TextResourceOrigin.Location     |      |      |



####  org.springframework.boot.reactor

| org.springframework.boot.reactor | 类型 | 笔记 |
|------------------------------------|------------------------------------|------------------------------------|
| DebugAgentEnvironmentPostProcessor |  |  |





#### org.springframework.boot.rsocket

org.springframework.boot.rsocket.context

org.springframework.boot.rsocket.messaging

org.springframework.boot.rsocket.netty

org.springframework.boot.rsocket.server





#### org.springframework.boot.security



org.springframework.boot.security.reactive

org.springframework.boot.security.servlet



#### org.springframework.boot.system



ApplicationHome

ApplicationPid

ApplicationTemp

SystemProperties

Enums

JavaVersion



#### org.springframework.boot.task



TaskExecutorCustomizer
TaskSchedulerCustomizer

TaskExecutorBuilder
TaskSchedulerBuilder

官方文档
7.7. Task Execution and Scheduling


#### org.springframework.boot.type



org.springframework.boot.type.classreading

Classes

ConcurrentReferenceCachingMetadataReaderFactor





#### org.springframework.boot.util



LambdaSafe

LambdaSafe.Callback

LambdaSafe.Callbacks

LambdaSafe.InvocationResult

LambdaSafe.LambdaSafeCallback



#### org.springframework.boot.validation



MessageInterpolatorFactory



#### org.springframework.boot.web

#####  org.springframework.boot.web.client



| org.springframework.boot.web.client | 类型 | 内容 |
| ----------------------------------- | ---- | ---- |
| Interfaces                          |      |      |
| RestTemplateCustomizer              |      |      |
| RestTemplateRequestCustomizer       |      |      |
|                                     |      |      |
| Classes                             |      |      |
|                                     |      |      |
| ClientHttpRequestFactorySupplier    |      |      |
| RestTemplateBuilder                 |      |      |
| RootUriTemplateHandler              |      |      |

##### org.springframework.boot.web.codec



| org.springframework.boot.web.codec | 类型 |      |
| ---------------------------------- | ---- | ---- |
| Interfaces                         |      |      |
| CodecCustomizer                    |      |      |



#### org.springframework.boot.context



| org.springframework.boot.context            | 类型 |      |
| ------------------------------------------- | ---- | ---- |
| Interfaces                                  |      |      |
| ConfigurableWebServerApplicationContext     |      |      |
| WebServerApplicationContext                 |      |      |
|                                             |      |      |
| Classes                                     |      |      |
|                                             |      |      |
| ServerPortInfoApplicationContextInitializer |      |      |
| WebServerInitializedEvent                   |      |      |
| WebServerPortFileWriter                     |      |      |



#### org.springframework.boot.reactor





| org.springframework.boot.reactor       | 类型 |      |
| -------------------------------------- | ---- | ---- |
| Interfaces                             |      |      |
| ConfigurableJettyWebServerFactory      |      |      |
| JettyServerCustomizer                  |      |      |
|                                        |      |      |
| Classes                                |      |      |
|                                        |      |      |
| JettyReactiveWebServerFactory          |      |      |
| JettyServletWebServerFactory           |      |      |
| JettyWebServer                         |      |      |
| ServletContextInitializerConfiguration |      |      |

#### org.springframework.boot.web
##### org.springframework.boot.web.embedded
###### org.springframework.boot.web.embedded.netty



| org.springframework.boot.web.embedded.netty | 类型 |      |
| ------------------------------------------- | ---- | ---- |
| Interfaces                                  |      |      |
| NettyRouteProvider                          |      |      |
| NettyServerCustomizer                       |      |      |
|                                             |      |      |
| Classes                                     |      |      |
|                                             |      |      |
| NettyReactiveWebServerFactory               |      |      |
| NettyWebServer                              |      |      |
| SslServerCustomizer                         |      |      |



###### org.springframework.boot.web.embedded.tomcat



| org.springframework.boot.web.embedded.tomcat | 类型 |      |
| -------------------------------------------- | ---- | ---- |
| Interfaces                                   |      |      |
| ConfigurableTomcatWebServerFactory           |      |      |
| TomcatConnectorCustomizer                    |      |      |
| TomcatContextCustomizer                      |      |      |
| TomcatProtocolHandlerCustomizer              |      |      |
|                                              |      |      |
| Classes                                      |      |      |
|                                              |      |      |
| TomcatEmbeddedWebappClassLoader              |      |      |
| TomcatReactiveWebServerFactory               |      |      |
| TomcatServletWebServerFactory                |      |      |
| TomcatWebServer                              |      |      |
|                                              |      |      |
| Exceptions                                   |      |      |
|                                              |      |      |
| ConnectorStartFailedException                |      |      |



###### org.springframework.boot.web.embedded.undertow



| org.springframework.boot.web.embedded.undertow | 类型 |      |
| ---------------------------------------------- | ---- | ---- |
| Interfaces                                     |      |      |
| ConfigurableUndertowWebServerFactory           |      |      |
| HttpHandlerFactory                             |      |      |
| UndertowBuilderCustomizer                      |      |      |
| UndertowDeploymentInfoCustomizer               |      |      |
|                                                |      |      |
| Classes                                        |      |      |
|                                                |      |      |
| UndertowReactiveWebServerFactory               |      |      |
| UndertowServletWebServer                       |      |      |
| UndertowServletWebServerFactory                |      |      |
| UndertowWebServer                              |      |      |



#### org.springframework.boot.web.reactive

##### org.springframework.boot.web.reactive.error



| org.springframework.boot.web.reactive.error | 类型 |      |
| ------------------------------------------- | ---- | ---- |
| Interfaces                                  |      |      |
| ErrorAttributes                             |      |      |
| ErrorWebExceptionHandler                    |      |      |
|                                             |      |      |
| Classes                                     |      |      |
|                                             |      |      |
| DefaultErrorAttributes                      |      |      |



##### org.springframework.boot.web.reactive.context



| org.springframework.boot.web.reactive.context       | 类型 |      |
| --------------------------------------------------- | ---- | ---- |
| Interfaces                                          |      |      |
| ConfigurableReactiveWebApplicationContext           |      |      |
| ConfigurableReactiveWebEnvironment                  |      |      |
| ReactiveWebApplicationContext                       |      |      |
|                                                     |      |      |
| Classes                                             |      |      |
|                                                     |      |      |
| AnnotationConfigReactiveWebApplicationContext       |      |      |
| AnnotationConfigReactiveWebServerApplicationContext |      |      |
| GenericReactiveWebApplicationContext                |      |      |
| ReactiveWebServerApplicationContext                 |      |      |
| ReactiveWebServerInitializedEvent                   |      |      |
| StandardReactiveWebEnvironment                      |      |      |



####  org.springframework.boot.web.server



| org.springframework.boot.web.server         | 类型 |      |
| ------------------------------------------- | ---- | ---- |
| Interfaces                                  |      |      |
| ConfigurableWebServerFactory                |      |      |
| ErrorPageRegistrar                          |      |      |
| ErrorPageRegistry                           |      |      |
| GracefulShutdownCallback                    |      |      |
| SslStoreProvider                            |      |      |
| WebServer                                   |      |      |
| WebServerFactory                            |      |      |
| WebServerFactoryCustomizer                  |      |      |
|                                             |      |      |
| Classes                                     |      |      |
|                                             |      |      |
| AbstractConfigurableWebServerFactory        |      |      |
| Compression                                 |      |      |
| ErrorPage                                   |      |      |
| ErrorPageRegistrarBeanPostProcessor         |      |      |
| Http2                                       |      |      |
| MimeMappings                                |      |      |
| MimeMappings.Mapping                        |      |      |
| Ssl                                         |      |      |
| SslConfigurationValidator                   |      |      |
| WebServerFactoryCustomizerBeanPostProcessor |      |      |
|                                             |      |      |
| Enums                                       |      |      |
|                                             |      |      |
| GracefulShutdownResult                      |      |      |
| Shutdown                                    |      |      |
| Ssl.ClientAuth                              |      |      |
|                                             |      |      |
| Exceptions                                  |      |      |
|                                             |      |      |
| PortInUseException                          |      |      |
| WebServerException                          |      |      |
|                                             |      |      |
| Annotation Types                            |      |      |
|                                             |      |      |
| LocalServerPort                             |      |      |



####  org.springframework.boot.web.servlet





| org.springframework.boot.web.servlet                   | 类型 |      |
| ------------------------------------------------------ | ---- | ---- |
| Interfaces                                             |      |      |
| ServletContextInitializer                              |      |      |
| ServletContextInitializerBeans.RegistrationBeanAdapter |      |      |
|                                                        |      |      |
| Classes                                                |      |      |
|                                                        |      |      |
| AbstractFilterRegistrationBean                         |      |      |
| DelegatingFilterProxyRegistrationBean                  |      |      |
| DynamicRegistrationBean                                |      |      |
| FilterRegistrationBean                                 |      |      |
| MultipartConfigFactory                                 |      |      |
| RegistrationBean                                       |      |      |
| ServletContextInitializerBeans                         |      |      |
| ServletListenerRegistrationBean                        |      |      |
| ServletRegistrationBean                                |      |      |
|                                                        |      |      |
| Enums                                                  |      |      |
|                                                        |      |      |
| DispatcherType                                         |      |      |
|                                                        |      |      |
| Annotation Types                                       |      |      |
|                                                        |      |      |
| ServletComponentScan                                   |      |      |



##### org.springframework.boot.web.servlet.context





| org.springframework.boot.web.servlet.context                 | 类型 |      |
| ------------------------------------------------------------ | ---- | ---- |
| AnnotationConfigServletWebApplicationContext                 |      |      |
| AnnotationConfigServletWebServerApplicationContext           |      |      |
| ServletWebServerApplicationContext                           |      |      |
| ServletWebServerApplicationContext.ExistingWebApplicationScopes |      |      |
| ServletWebServerInitializedEvent                             |      |      |
| WebApplicationContextServletContextAwareProcessor            |      |      |
| XmlServletWebServerApplicationContext                        |      |      |



##### org.springframework.boot.web.servlet.error



| org.springframework.boot.web.servlet.error | 类型 |      |
| ------------------------------------------ | ---- | ---- |
| Interfaces                                 |      |      |
| ErrorAttributes                            |      |      |
| ErrorController                            |      |      |
|                                            |      |      |
| Classes                                    |      |      |
|                                            |      |      |
| DefaultErrorAttributes                     |      |      |





##### org.springframework.boot.web.servlet.filter





| org.springframework.boot.web.servlet.filter | 类型 |      |
| ------------------------------------------- | ---- | ---- |
| Interfaces                                  |      |      |
|                                             |      |      |
| OrderedFilter                               |      |      |
|                                             |      |      |
| Classes                                     |      |      |
|                                             |      |      |
| ApplicationContextHeaderFilter              |      |      |
| OrderedCharacterEncodingFilter              |      |      |
| OrderedFormContentFilter                    |      |      |
| OrderedHiddenHttpMethodFilter               |      |      |
| OrderedRequestContextFilter                 |      |      |



##### org.springframework.boot.web.servlet.server





| org.springframework.boot.web.servlet.server | 类型 |      |
| ------------------------------------------- | ---- | ---- |
| Interfaces                                  |      |      |
| ConfigurableServletWebServerFactory         |      |      |
| ServletWebServerFactory                     |      |      |
|                                             |      |      |
| Classes                                     |      |      |
|                                             |      |      |
| AbstractServletWebServerFactory             |      |      |
| Encoding                                    |      |      |
| Jsp                                         |      |      |
| Session                                     |      |      |
| Session.Cookie                              |      |      |
|                                             |      |      |
| Enums                                       |      |      |
|                                             |      |      |
| Encoding.Type                               |      |      |
| Session.SessionTrackingMode                 |      |      |



##### org.springframework.boot.web.servlet.support



| org.springframework.boot.web.servlet.support | 类型 |      |
| -------------------------------------------- | ---- | ---- |
|                                              |      |      |
| ErrorPageFilter                              |      |      |
| ServletContextApplicationContextInitializer  |      |      |
| SpringBootServletInitializer                 |      |      |



##### org.springframework.boot.web.servlet.view



| org.springframework.boot.web.servlet.view | 类型 |      |
| ----------------------------------------- | ---- | ---- |
|                                           |      |      |
| MustacheView                              |      |      |
| MustacheViewResolver                      |      |      |



#### org.springframework.boot.web.reactive.result.view





| org.springframework.boot.web.reactive.result.view | 类型 |      |
| ------------------------------------------------- | ---- | ---- |
|                                                   |      |      |
| MustacheView                                      |      |      |
| MustacheViewResolver                              |      |      |



#### org.springframework.boot.web.reactive.server



ConfigurableReactiveWebServerFactory

ReactiveWebServerFactory

Classes

AbstractReactiveWebServerFactory



#### org.springframework.boot.web.server



|                                             |      |      |
| ------------------------------------------- | ---- | ---- |
| ConfigurableWebServerFactory                |      |      |
| ErrorPageRegistrar                          |      |      |
| ErrorPageRegistry                           |      |      |
| GracefulShutdownCallback                    |      |      |
| SslStoreProvider                            |      |      |
| WebServer                                   |      |      |
| WebServerFactory                            |      |      |
| WebServerFactoryCustomizer                  |      |      |
|                                             |      |      |
| Classes                                     |      |      |
|                                             |      |      |
| AbstractConfigurableWebServerFactory        |      |      |
| Compression                                 |      |      |
| ErrorPage                                   |      |      |
| ErrorPageRegistrarBeanPostProcessor         |      |      |
| Http2                                       |      |      |
| MimeMappings                                |      |      |
| MimeMappings.Mapping                        |      |      |
| Ssl                                         |      |      |
| SslConfigurationValidator                   |      |      |
| WebServerFactoryCustomizerBeanPostProcessor |      |      |
|                                             |      |      |
| Enums                                       |      |      |
|                                             |      |      |
| GracefulShutdownResult                      |      |      |
| Shutdown                                    |      |      |
| Ssl.ClientAuth                              |      |      |
|                                             |      |      |
| Exceptions                                  |      |      |
|                                             |      |      |
| PortInUseException                          |      |      |
| WebServerException                          |      |      |
|                                             |      |      |
| Annotation Types                            |      |      |
|                                             |      |      |
| LocalServerPort                             |      |      |



#### org.springframework.boot.web.servlet



| Interfaces                                             |      |      |
| ------------------------------------------------------ | ---- | ---- |
|                                                        |      |      |
| ServletContextInitializer                              |      |      |
| ServletContextInitializerBeans.RegistrationBeanAdapter |      |      |
|                                                        |      |      |
| Classes                                                |      |      |
|                                                        |      |      |
| AbstractFilterRegistrationBean                         |      |      |
| DelegatingFilterProxyRegistrationBean                  |      |      |
| DynamicRegistrationBean                                |      |      |
| FilterRegistrationBean                                 |      |      |
| MultipartConfigFactory                                 |      |      |
| RegistrationBean                                       |      |      |
| ServletContextInitializerBeans                         |      |      |
| ServletListenerRegistrationBean                        |      |      |
| ServletRegistrationBean                                |      |      |
|                                                        |      |      |
| Enums                                                  |      |      |
|                                                        |      |      |
| DispatcherType                                         |      |      |
|                                                        |      |      |
| Annotation Types                                       |      |      |
|                                                        |      |      |
| ServletComponentScan                                   |      |      |



#### org.springframework.boot.web.servlet.context

|                                                              |      |      |
| ------------------------------------------------------------ | ---- | ---- |
| AnnotationConfigServletWebApplicationContext                 |      |      |
| AnnotationConfigServletWebServerApplicationContext           |      |      |
| ServletWebServerApplicationContext                           |      |      |
| ServletWebServerApplicationContext.ExistingWebApplicationScopes |      |      |
| ServletWebServerInitializedEvent                             |      |      |
| WebApplicationContextServletContextAwareProcessor            |      |      |
| XmlServletWebServerApplicationContext                        |      |      |

#### org.springframework.boot.web.servlet.error



ErrorAttributes

ErrorController

Classes

DefaultErrorAttributes



#### org.springframework.boot.web.servlet.filter

|                                |      |      |
| ------------------------------ | ---- | ---- |
| OrderedFilter                  |      |      |
|                                |      |      |
| Classes                        |      |      |
|                                |      |      |
| ApplicationContextHeaderFilter |      |      |
| OrderedCharacterEncodingFilter |      |      |
| OrderedFormContentFilter       |      |      |
| OrderedHiddenHttpMethodFilter  |      |      |
| OrderedRequestContextFilter    |      |      |



#### org.springframework.boot.web.servlet.server

|                                     |      |      |
| ----------------------------------- | ---- | ---- |
| ConfigurableServletWebServerFactory |      |      |
| ServletWebServerFactory             |      |      |
|                                     |      |      |
| Classes                             |      |      |
|                                     |      |      |
| AbstractServletWebServerFactory     |      |      |
| Encoding                            |      |      |
| Jsp                                 |      |      |
| Session                             |      |      |
| Session.Cookie                      |      |      |
|                                     |      |      |
| Enums                               |      |      |
|                                     |      |      |
| Encoding.Type                       |      |      |
| Session.SessionTrackingMode         |      |      |

#### org.springframework.boot.web.servlet.support

ErrorPageFilter

ServletContextApplicationContextInitializer

SpringBootServletInitializer

#### org.springframework.boot.web.servlet.view



MustacheView

MustacheViewResolver



#### org.springframework.boot.webservices.client



WebServiceTemplateCustomizer

Classes

HttpWebServiceMessageSenderBuilder

WebServiceTemplateBuilder




| 库       |      |      |
| -------- | ---- | ---- |
| druid    |      |      |
| retrofit |      |      |
| mybatis  |      |      |
| dubbo    |      |      |



<dependency>
    <groupId>org.apache.dubbo</groupId>
    <artifactId>dubbo-spring-boot-starter</artifactId>
</dependency>



<dependency>
    <groupId>com.alibaba</groupId>
    <artifactId>druid-spring-boot-starter</artifactId>
    <version>${druid.version}</version>
</dependency>





<dependency>
  <groupId>com.github.lianjiatech</groupId>
  <artifactId>retrofit-spring-boot-starter</artifactId>
  <version>${retrofit-spring-boot-starter.version}</version>
</dependency>



<dependency>
    <groupId>org.mybatis.spring.boot</groupId>
    <artifactId>mybatis-spring-boot-starter</artifactId>
    <version>${mybatis-spring-boot-starter.version}</version>
</dependency>



kafka



Kafka Spring Boot Starter 的 Maven 坐标为：

```xml
<dependency>
    <groupId>org.springframework.kafka</groupId>
    <artifactId>spring-kafka</artifactId>
    <version>${spring-kafka.version}</version>
</dependency>
```

其中，`${spring-kafka.version}` 是 Kafka Spring Boot Starter 的版本号，你需要将它替换为你要使用的版本号。你可以在 Maven 的 `pom.xml` 文件中添加以上依赖，然后使用 Maven 或其他构建工具进行项目构建。

需要注意的是，Kafka Spring Boot Starter 依赖于 Spring Boot 和 Kafka，因此你需要同时引入 Spring Boot 和 Kafka 的依赖，例如：

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter</artifactId>
    <version>${spring-boot.version}</version>
</dependency>
<dependency>
    <groupId>org.apache.kafka</groupId>
    <artifactId>kafka-clients</artifactId>
    <version>${kafka.version}</version>
</dependency>
```



其中，`${spring-boot.version}` 和 `${kafka.version}` 分别是 Spring Boot 和 Kafka 的版本号，你需要将它们替换为你要使用的版本号。

在引入以上依赖后，你可以在 Spring Boot 的配置文件中配置 Kafka，例如：

```properties
spring.kafka.bootstrap-servers=localhost:9092

# 配置消费者
spring.kafka.consumer.group-id=my-group
spring.kafka.consumer.auto-offset-reset=earliest
spring.kafka.consumer.enable-auto-commit=false

# 配置生产者
spring.kafka.producer.acks=all
spring.kafka.producer.retries=0
spring.kafka.producer.batch-size=16384
spring.kafka.producer.buffer-memory=33554432
```

这样，你就可以通过 `spring.kafka.*` 配置项来配置 Kafka，例如配置 Kafka 的地址、消费者的 Group ID、消费者的消费模式、生产者的参数等。然后在代码中通过 `@Autowired` 注解来注入 Kafka 的 `KafkaTemplate` 对象，例如：

```java
import org.springframework.kafka.core.KafkaTemplate;

@RestController
public class UserController {
    
    @Autowired
    private KafkaTemplate<String, String> kafkaTemplate;
    
    // ...
}
```

这样，你就可以通过 `kafkaTemplate` 来发送消息到 Kafka 以及接收来自 Kafka 的消息。

spring官方支持



```java
import org.springframework.kafka.core.KafkaTemplate;

@RestController
public class UserController {
    
    @Autowired
    private KafkaTemplate<String, String> kafkaTemplate;
    
    // ...
}
```





rocketmq



redis

<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-redis</artifactId>
</dependency>

RedisTemplate





mongodb

rabbitmq



web springboot



<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
    <version>${spring-boot.version}</version>
</dependency>



test

<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-test</artifactId>
    <scope>test</scope>
</dependency>



logging



<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-logging</artifactId>
  <version>2.3.4.RELEASE</version>
  <scope>compile</scope>
</dependency>





json



<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-json</artifactId>
  <version>2.3.4.RELEASE</version>
  <scope>compile</scope>
</dependency>



tomcat



<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-tomcat</artifactId>
  <version>2.3.4.RELEASE</version>
  <scope>compile</scope>
</dependency>

