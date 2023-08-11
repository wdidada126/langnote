# Spring Boot


G:\source_code\spring-boot

spring boot 2.0.4 maven组织的，可以跳转

https://docs.spring.io/spring-boot/docs/2.3.x/api/

spring_boot.xlsx

spring-boot-2.7.11.jar!\META-INF\spring.factories
文件

##  jar文件

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

Classes

TaskExecutorBuilder

TaskSchedulerBuilder



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

