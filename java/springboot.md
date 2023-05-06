# Spring Boot


## ConditionalOnClass注解
@ConditionalOnClass(KafkaTemplate.class)


`@ConditionalOnClass` 是 Spring Boot 提供的一个条件注解，用于在特定的类存在时才加载一个 Bean 或配置类。具体来说，`@ConditionalOnClass` 的作用是检查当前 classpath 中是否存在指定的类，如果存在，则加载 Bean 或配置类，否则忽略加载。

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
