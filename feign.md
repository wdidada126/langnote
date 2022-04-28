# feign

tutorials\feign

一个Java接口


import feign.Headers;
import feign.Param;
import feign.RequestLine;

http协议
get路径参数
http body
form-data
urlencoded
raw
bin



Feign、OpenFeign及SpringCloud Feign的区别

Feign是Spring Cloud组件中一个轻量级RESTful的HTTP服务客户端，Feign内置了Ribbon，用来做客户端负载均衡，去调用服务注册中心的服务。Feign的使用方式是：使用Feign的注解定义接口，调用接口，就可以调用服务注册中心的服务。

由于 Netflix 公司不再维护feign，feign由社区维护，feign更名为 openfeign，并且项目迁移到新的仓库。后续版本仅使用“io.github.openfeign”，推荐使用该依赖。

spring-cloud-openfeign是基于openfeign进行包装，集成了SpringMVC的注解等方便SpringBoot项目开发的一个组件。

Spring Cloud OpenFeign简介
Spring Cloud OpenFeign是一个声明式的HTTP客户端，它简化了HTTP客户端的开发，使编写Web服务的客户端变得更容易。使用Spring Cloud OpenFeign，只需要创建一个接口并注解，就能很容易地调用各服务提供的HTTP接口。Spring Cloud OpenFeign基于OpenFeign实现，它除了提供声明式的 HTTP客户端外，还整合了Spring Cloud Hystrix，能够轻松实现熔断器模型。

测试的例子

https://gitee.com/edidada/openfeigndemo

https://gitee.com/edidada/springboothttpserver
