# guice

Google开源的一个依赖注入类库，相比于Spring IoC来说更小更快。Elasticsearch大量使用了Guice，本文简单的介绍下Guice的基本概念和使用方式。

https://tech.souyunku.com/?p=13133

Guice是Google推出的一个轻量级的依赖注入框架,其GitHub项目地址是:

https://github.com/google/guice

这个项目包含了Guice的完整源码以及文档、示例等资源。

主要内容包括:

- guice - 核心库源代码
- extensions - Guice扩展模块代码
- doc - 参考文档
- examples - 示例程序 
- benchmarks - 性能测试
- contributors - 贡献者指南

在README中对Guice进行了简明的介绍。

最新版本为5.1.0,采用Apache 2.0协议开源。

项目地址:https://github.com/google/guice

Guice的优点包括:

- 轻量级,不需要像Spring配置那么笨重的配置
- 使用注解标识依赖关系
- 支持AOP
- 运行时绑定,不需要采用单例
- 支持嵌入到现有代码中

Guice和Spring的区别在于Guice更轻量级,可以嵌入现有项目,而Spring提供了更全面的解决方案。

总之,Guice是轻量级注入框架的典范,值得学习和参考。


## java api doc
https://google.github.io/guice/api-docs/5.0.1/javadoc/index.html
https://google.github.io/guice/api-docs/6.0.0/javadoc/index.html


Package	Description
com.google.inject
Google Guice (pronounced "juice") is an ultra-lightweight dependency injection framework.

com.google.inject.assistedinject
Extension for combining factory interfaces with injection; this extension requires guice-assistedinject.jar.


com.google.inject.assistedinject.internal 


com.google.inject.binder
Interfaces which make up Binder's expression language.


com.google.inject.daggeradapter 


com.google.inject.grapher 


com.google.inject.grapher.graphviz 


com.google.inject.jndi
JNDI integration; this extension requires guice-jndi.jar.


com.google.inject.matcher
Used for matching things.


com.google.inject.multibindings
Extension for binding multiple instances in a collection; this extension requires guice-multibindings.jar.


com.google.inject.name
Support for binding to string-based names.


com.google.inject.persist
Guice Persist: a lightweight persistence library for Guice; this extension requires guice-persist.jar.


com.google.inject.persist.finder
Dynamic Finder API for Guice Persist.


com.google.inject.persist.jpa
guice-persist's Java Persistence API (JPA) support.


com.google.inject.servlet
Servlet API scopes, bindings and registration; this extension requires guice-servlet.jar.


com.google.inject.spi
Guice service provider interface


com.google.inject.spring
Spring integration; this extension requires guice-spring.jar.


com.google.inject.struts2 


com.google.inject.testing.fieldbinder 



com.google.inject.testing.throwingproviders 


com.google.inject.throwingproviders
Extension for injecting objects that may throw at provision time; this extension requires guice-throwingproviders.jar.


com.google.inject.tools.jmx
JMX integration; this extension requires guice-jmx.jar.


com.google.inject.util
Helper methods for working with Guice.

## example

https://gitee.com/edidada/guice-demo    报错
https://gitee.com/edidada/guice-example 可以跑起来
