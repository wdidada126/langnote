# Spring揭秘



https://book.douban.com/subject/3897837/



Spring中bean的生命周期？

BeanPostProcess 实现propertity定义

对应Spring 2.5
Java 5还没有普及

1 Spring框架的由来



### Chap. 2 IoC的基本概念

依赖控制反转
本来应该new Object()的，现在直接获取@Autowired。
IoC注入的三种方式

1、接口注入
2、构造方法注入
3、setting方法注入

### Chap. 3 掌管大局的IoC Service Provider
IoC Service Provider

### Chap. 4 Spring的IoC容器之BeanFactory
4.3
Scope 自定义scope
默认single prototype是硬编码到代码中，其他的request是可以配置的
org.springframework.beans.factory.config.Scope

1、方法注入
<lookup-method>

2、


Spring ioc其他框架封装 aop 三个？？

### Chap. 5 Spring IoC容器ApplicationContext
ResourceLoader
MessageSource

第6章 Spring IoC容器之扩展篇



### Chap. 7 一起来看AOP
aop

Servlet Filtter就是around切点

### Chap. 8 Spring AOP概述及其实现机制
代理模式
动态代理
动态字节码生成

### Chap. 9 Spring AOP一世
ThrowAdvice
MethodAdvice
DyamicIntroduceAdvice

9.4.2 IntroductionAdvisor只能应用于类注解
PointAdvisor可以应用于类，也可以应用于方法等

9.4.3 Ordered的作用
org.springframework.core.Ordered

### Chap. 10 Spring AOP二世

方案1. BeanNameAutoProxyCreator
方案2. DefaultAdvisorAutoProxyCreator
方案3. 扩展
AbstractAutoProxyCreator
AbstractAdvisorAutoProxyCreator

org.springframework.aop.framework.autoproxy.BeanNameAutoProxyCreator
org.springframework.aop.framework.autoproxy.DefaultAdvisorAutoProxyCreator



第11章 AOP应用案例



第12章 Spring AOP之扩展篇



第四部分 使用Spring访问数据
第13章 统一的数据访问异常层次体系



第14章 JDBC API的最佳实践



第15章 Spring对各种ORM的集成



第16章 Spring数据访问之扩展篇



第17章 有关事务的楔子





第18章 群雄逐鹿下的Java事务管理



第19章 Spring事务王国的架构





### Chap. 20 使用Spring进行事务管理
事务

### Chap. 21 Spring事务管理之扩展篇



org.springframework.beans.factory.FactoryBean
getObject()

第六部分 Spring的Web MVC框架
第22章 迈向Spring MVC的旅程





第23章 Spring MVC初体验



