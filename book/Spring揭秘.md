# Spring揭秘



https://book.douban.com/subject/3897837/



Spring中bean的生命周期？

BeanPostProcess 实现propertity定义

对应Spring 2.5
Java 5还没有普及

### Chap. 2

依赖控制反转
本来应该new Object()的，现在直接获取@Autowired。
IoC注入的三种方式

1、接口注入
2、构造方法注入
3、setting方法注入

### Chap. 3
IoC Service Provider

### Chap. 4
4.3
Scope 自定义scope
默认single prototype是硬编码到代码中，其他的request是可以配置的
org.springframework.beans.factory.config.Scope

1、方法注入
<lookup-method>

2、


Spring ioc其他框架封装 aop 三个？？

### Chap. 5
ResourceLoader
MessageSource

### Chap. 7
aop

Servlet Filtter就是around切点

### Chap. 8
代理模式
动态代理
动态字节码生成

### Chap. 9
ThrowAdvice
MethodAdvice
DyamicIntroduceAdvice

9.4.2 IntroductionAdvisor只能应用于类注解
PointAdvisor可以应用于类，也可以应用于方法等

9.4.3 Ordered的作用
org.springframework.core.Ordered

### Chap. 10

方案1. BeanNameAutoProxyCreator
方案2. DefaultAdvisorAutoProxyCreator
方案3. 扩展
AbstractAutoProxyCreator
AbstractAdvisorAutoProxyCreator

org.springframework.aop.framework.autoproxy.BeanNameAutoProxyCreator
org.springframework.aop.framework.autoproxy.DefaultAdvisorAutoProxyCreator



### Chap. 20
事务

### Chap. 21



org.springframework.beans.factory.FactoryBean
getObject()

