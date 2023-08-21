# doc

bean的生命周期 《spring实战》

1.2.2 bean的生命周期




看英文文档

Usage scenarios
Enhancement 增强

### 重点
SockJS和STOMP消息传递

web.xml文件格式

<!-- Spring配置文件 -->

servlet web.xml

<context-param>
	<param-name>contextConfigLocation</param-name>
	<param-value>classpath:applicationContext.xml</param-value>
</context-param>

applicationContext.xml在Java代码的哪个地方解析的



ApplicationContext
ApplicationContext getParent();

GenericApplicationContext
ClassPathXmlApplicationContext
GenericGroovyApplicationContext

scope选项：
singleton
prototype
request
session
application
websocket

inner class
com.example.SomeThing$OtherThing

bean 如何处理

bean的创建
- Instantiation with a Constructor
- Instantiation with a Static Factory Method
- Instantiation by Using an Instance Factory Method



xml bean的属性

- factory-bean
- factory-method

<bean id="accountService"
    factory-bean="serviceLocator"
    factory-method="createAccountServiceInstance"/>

Spring doc bean

## Chap 1.6.1 Lifecycle Callbacks

@PostConstruct
@PreDestroy



interface BeanPostProcessor

Factory hook


SmartLifecycle

Lifecycle

## Chap. 17
bean继承



Bean
parent

## Chap.18 bean的其他定义方式

beanpostprocessor
beanfactorypostprocessor

factorybean

