# feign

SpringCloud原理之feign.md


Spring Boot提供了一种非常方便的方式来使用Feign来实现RESTful服务之间的通信。

以下是使用Spring Boot配置Feign的步骤：

1.添加Feign依赖项
在Maven项目中，您需要添加以下依赖项：

<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-openfeign</artifactId>
</dependency>



2.启用Feign
在Spring Boot应用程序中启用Feign，您需要使用@EnableFeignClients注释：
@SpringBootApplication
@EnableFeignClients
public class MyApp {
   // ...
}
3.创建Feign客户端接口
创建一个接口，用于定义Feign客户端。该接口应该包含对远程服务的所有请求，以及所需的任何参数。例如：

@FeignClient(name = "my-service")
public interface MyServiceClient {
    @GetMapping("/users/{userId}")
    User getUserById(@PathVariable("userId") Long userId);
}


Spring Boot提供了一种非常方便的方式来使用Feign来实现RESTful服务之间的通信。

以下是使用Spring Boot配置Feign的步骤：

1.添加Feign依赖项
在Maven项目中，您需要添加以下依赖项：

php
Copy code
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-openfeign</artifactId>
</dependency>
2.启用Feign
在Spring Boot应用程序中启用Feign，您需要使用@EnableFeignClients注释：

less
Copy code
@SpringBootApplication
@EnableFeignClients
public class MyApp {
   // ...
}
3.创建Feign客户端接口
创建一个接口，用于定义Feign客户端。该接口应该包含对远程服务的所有请求，以及所需的任何参数。例如：

less
Copy code
@FeignClient(name = "my-service")
public interface MyServiceClient {
    @GetMapping("/users/{userId}")
    User getUserById(@PathVariable("userId") Long userId);
}
4.使用Feign客户端
使用Feign客户端非常简单，只需将其注入到您的代码中即可：



@Service
public class MyService {
    private final MyServiceClient client;

    public MyService(MyServiceClient client) {
        this.client = client;
    }

    public User getUserById(Long userId) {
        return client.getUserById(userId);
    }
}



5.配置Feign客户端
您可以通过创建Feign配置类来配置Feign客户端的行为。例如，您可以使用以下配置来启用Feign的日志记录：



@Configuration
public class FeignConfig {
    @Bean
    Logger.Level feignLoggerLevel() {
        return Logger.Level.FULL;
    }
}


以上是使用Spring Boot配置Feign的基本步骤。根据您的具体需求，您可能需要进行其他配置来满足您的需求。







### feign body中自动填充参数

{
        head:{}
        body:{}
}

head部分自动填充


16:11:16.408 [main] INFO  org.springframework.cloud.openfeign.FeignClientFactoryBean : [378] - For '' URL not provided. Will try picking an instance via load-balancing. 
16:11:17.046 [main] INFO  org.springframework.cloud.openfeign.FeignClientFactoryBean : [378] - For '' URL not provided. Will try picking an instance via load-balancing.


### ribbon
spring cloud feign添加ribbon
1、引入pom依赖

2、设置负载ip列表
loadblanceclient2.ribbon.listOfServers=http://localhost:9001, http://localhost:9002

3、设置注解的name或value
@FeignClient(value = "loadblanceclient2"
        ,configuration = {LoadBlanceRequestInterceptor.class}
)



spring cloud feign打印日志 没有生效

打印日志，暂时用插值器替换
feign 插值器
FeignException
FeignClient使用@RequestLine注解, 而未配置feign自带契约Contract时, @Headers不会起作用, 而且启动项目会报错:
Method xxx not annotated with HTTP method type (ex. GET, POST)
https://blog.csdn.net/hkk666123/article/details/113964715



tutorials\feign

一个Java接口


import feign.Headers;
import feign.Param;
import feign.RequestLine;

http协议
get 路径参数
http body
form-data
urlencoded
raw
bin



io.github.openfeign



Feign、OpenFeign及SpringCloud Feign的区别

Feign是Spring Cloud组件中一个轻量级RESTful的HTTP服务客户端，Feign内置了Ribbon，用来做客户端负载均衡，去调用服务注册中心的服务。Feign的使用方式是：使用Feign的注解定义接口，调用接口，就可以调用服务注册中心的服务。

由于 Netflix 公司不再维护feign，feign由社区维护，feign更名为 openfeign，并且项目迁移到新的仓库。后续版本仅使用“io.github.openfeign”，推荐使用该依赖。

spring-cloud-openfeign是基于openfeign进行包装，集成了SpringMVC的注解等方便SpringBoot项目开发的一个组件。

Spring Cloud OpenFeign简介
Spring Cloud OpenFeign是一个声明式的HTTP客户端，它简化了HTTP客户端的开发，使编写Web服务的客户端变得更容易。使用Spring Cloud OpenFeign，只需要创建一个接口并注解，就能很容易地调用各服务提供的HTTP接口。Spring Cloud OpenFeign基于OpenFeign实现，它除了提供声明式的 HTTP客户端外，还整合了Spring Cloud Hystrix，能够轻松实现熔断器模型。

测试的例子

https://gitee.com/edidada/openfeigndemo

https://gitee.com/edidada/springboothttpserver


https://github.com/OpenFeign/feign


doc
https://github.com/spring-cloud/spring-cloud-openfeign

https://cloud.spring.io/spring-cloud-openfeign/reference/html/


org.springframework.beans.factory.UnsatisfiedDependencyException: Error creating bean with name 'com.example.openfeigndemo.StoreClientTest': Unsatisfied dependency expressed through field 'storeClient'; nested exception is org.springframework.beans.factory.BeanCreationException: Error creating bean with name 'com.example.openfeigndemo.httprpc.StoreClient': Unexpected exception during bean creation; nested exception is java.lang.IllegalStateException: No Feign Client for loadBalancing defined. Did you forget to include spring-cloud-starter-netflix-ribbon or spring-cloud-starter-loadbalancer?


README_feign.md


github.com/openfeign/feign-form


POST 传输文件

openfeign_form_README.md

