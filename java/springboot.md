# Spring Boot


springboot 命令行运行
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





<<<<<<< HEAD
#### Connection to a JNDI DataSource
=======
### Connection to a JNDI DataSource
>>>>>>> afe522da082020e5ece0b75c43067644b2edb768

If you deploy your Spring Boot application to an Application Server, you might want to configure and manage your DataSource by using your Application Server’s built-in features and access it by using JNDI.

```shell
spring.datasource.jndi-name=java:jboss/datasources/customers
```

<<<<<<< HEAD






B站视频

写SpringBoot starter
=======
>>>>>>> afe522da082020e5ece0b75c43067644b2edb768
