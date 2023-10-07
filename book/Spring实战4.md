# Spring实战4

4 版本 2016-4
Spring实战（第5版 ） 2020

java实现一个功能，首先看spring是否内置支持
spring支持发送邮件，就不用三方库了
克雷格·沃斯（Craig Walls）
Pivotal的首席软件工程师、畅销书作者、Spring框架的热情支持者，经常在各种技术会议上发表演讲。

https://book.douban.com/subject/26767354/

spring 官方对接三方库
其他团队提供的对接库
redis
neo4j
quartz
elasticjob

## 第1部分　Spring的核心
### Chap.1 第1章　Spring之旅

EJB
JavaBean规范
POJO 简单老Java对象

应用上下文ApplicationContext
Android里面也有Context QT WPF里面也有Context
Spring容器 Spring container
WPF MVVM

问Spring的应用上下文有几种实现？有什么区别

主要是加载bean的方式不同
1.xml
2.注解

bean的生命周期
BeanNameAware    void setBeanName(String name);                org.springframework.beans.factory.BeanNameAware
BeanFactoryAware void setBeanFactory(BeanFactory beanFactory)  
ApplicationContextAware void setApplicationContext(ApplicationContext applicationContext)
BeanPostProcessor  default Object postProcessBeforeInitialization(Object bean, String beanName)
InitializingBean void afterPropertiesSet()

xxx自定义方法 bean的生命周期 调用自定义初始化方法

BeanPostProcessor  default Object postProcessAfterInitialization(Object bean, String beanName)

DisposeBean void destroy()

Bean的生命周期中,调用自定义初始化方法的地方有以下几个:
1. 通过实现InitializingBean接口的afterPropertiesSet()方法
InitializingBean是JavaBean的标准接口,实现这个接口可以重写afterPropertiesSet()方法,用于自定义Bean初始化逻辑。这个方法会在所有属性被设置完毕后被自动调用。
2. 通过@PostConstruct注解标注的方法
@PostConstruct注解标注的初始化方法会在Bean属性被赋值并依赖注入完成后执行。这是Java EE标准的注解,被各大框架支持。
3. 自定义初始化方法
可以定义一个没有任何注解的自定义初始化方法,然后在XML配置文件或JavaConfig中通过init-method属性指定这个方法作为初始化方法进行调用。
4. BeanFactoryPostProcessor扩展点
实现BeanFactoryPostProcessor接口,可以在Bean定义加载完成后处理所有Bean定义,包括调用自定义初始化逻辑。
5. ApplicationContextAware扩展点
实现ApplicationContextAware接口回调初始化方法,可以在容器初始化阶段调用自定义逻辑。
6. 其他框架扩展点
部分框架(如Spring Boot)还提供了其他生命周期回调点,用于执行自定义逻辑,比如CommandLineRunner。
所以总的来说,通过上述几种方式都可以在Bean初始化阶段调用自定义逻辑进行额外初始化。其中@PostConstruct和InitializingBean是比较常用的实现方式。

aop
jdbc
Spring EL表达式
`#{}`

@componentScan
@Bean

### Chap. 2 装配Bean
@Autowired注解可以使用哪些地方
field
构造函数？
方法？

@Autowired注解可以使用哪些地方
@Autowired注解可以用在以下几个地方：
1. 类的成员变量上

@Autowired注解可以用在类的成员变量上，Spring会自动将匹配的Bean注入到该成员变量中。例如：

```java
@Component
public class MyService {
    // 自动注入 MyRepository Bean
    @Autowired
    private MyRepository myRepository;
    ...
}
```

2. 构造方法上
@Autowired注解也可以用在构造方法上，Spring会在创建Bean实例时，自动将匹配的Bean注入到构造方法参数中。例如：
```java
@Component
public class MyService {
    private MyRepository myRepository;

    // 构造方法注入 MyRepository Bean
    @Autowired
    public MyService(MyRepository myRepository) {
        this.myRepository = myRepository;
    }
    ...
}
```

3. Setter方法上
@Autowired注解也可以用在Setter方法上，Spring会在创建Bean实例后，自动调用Setter方法，并将匹配的Bean注入到Setter方法参数中。例如：
```java
@Component
public class MyService {
    private MyRepository myRepository;

    // Setter方法注入 MyRepository Bean
    @Autowired
    public void setMyRepository(MyRepository myRepository) {
        this.myRepository = myRepository;
    }
    ...
}
```

需要注意的是，如果一个类中有多个构造方法或Setter方法，并且这些方法都有@Autowired注解，那么Spring会根据参数类型和名称来匹配Bean进行注入。

另外，还可以使用@Qualifier注解来指定要注入的Bean的名称，例如：

```java
@Component
public class MyService {
    // 指定注入名称为 "myRepository2"
    @Autowired
    @Qualifier("myRepository2")
    private MyRepository myRepository;
    ...
}
```

以上就是@Autowired注解可以使用的地方，使用@Autowired注解可以方便地实现自动装配Bean的功能。

@Autowired可以对成员变量、方法以及构造函数进行注释
https://www.cnblogs.com/acm-bingzi/p/springAutowired.html

有多个bean时，配合Qualifier注解使用
@Autowired
@Qualifier("myRepository2")

javax.inject.Inject
javax.inject.Named
javax.inject.Named是JSR 330中的注解之一，该JSR的全称为"Dependency Injection for Java"。JSR 330定义了一组标准的注解和API，用于支持依赖注入（Dependency Injection，DI）和控制反转（Inversion of Control，IoC）。

@Autowired是Spring特有的注解。如果你不愿意在代码中到处使用Spring的特定注解来完成自动装配任务的话，那么你可以考虑将其替换 为@Inject:

[Java 依赖注入标准 JSR-330 简介](https://blog.csdn.net/u010278882/article/details/50773687)

@Inject注解来源于Java依赖注入规范
@Inject
需要导入javax.inject的包，和Autowired的功能一样但是没有required=false的功能，支持@Primary注解。

maven依赖如下：

```xml
        <dependency>
            <groupId>javax.inject</groupId>
            <artifactId>javax.inject</artifactId>
            <version>1</version>
        </dependency>
```

创建bean的name

xml创建bean时如何确保配置信息正确
https://www.cnblogs.com/yangming1996/p/7784615.html

Spring为<constructor-arg>元素提供了c-命名空 间作为替代方案

p

Spring bean的生命周期

在Spring中装配bean的三种主要方式：自动化 配置、基于Java的显式配置以及基于XML的显式配置。

基于Java的显式配置，@Bean

https://blog.csdn.net/qq_30038111/article/details/79611167

xml

配置命名空间

Spring中的c命名空间是一种用于设置Bean构造函数参数值的方式。
在Spring中，p命名空间是一种用于简化XML配置文件中Bean属性设置的方式。通过使用p命名空间，可以直接在XML配置文件中设置Bean的属性值，而无需编写繁琐的<property>标签。

### Chap. 3 高级装配

在3.1版本中，Spring引入了bean profile的功能。要使用profile，你首 先要将所有不同的bean定义整理到一个或多个profile之中，在将应用 部署到每个环境时，要确保对应的profile处于激活（active）的状态

在Spring 4之前，很难实现这种级别的条件化配置，但是Spring 4引入 了一个新的@Conditional注解，它可以用到带有@Bean注解的方法上。如果给定的条件计算结果为true，就会创建这个bean，否则的话，这个bean会被忽略。
org.springframework.context.annotation.Conditional spring-context包中

### Chap. 4 面向切面的Spring
描述切面的常用术语有通知(advice)、切点(pointcut)和连接点(join point)
如果你的AOP需求超过了简单的方法调用(如构造器或属性拦截)，那么你需要考虑使用AspectJ来实现切面。

源码不在

aop的四种方式
- 基于代理的经典Spring AOP
- 纯POJO切面
- @AspectJ注解驱动的切面
- 注入式AspectJ切面（适用于Spring各版本）

基于代理的经典Spring AOP
org.springframework.aop.framework.ProxyFactoryBean
基本不用了

Spring所创建的通知都是用标准的Java类编写。

joinpoint
pointcut
advice
before
after
after-return
after-throw
around

AspectJ指示器 描述
arg()         限制连接点匹配参数为指定类型的执行方法
@args()       限制连接点匹配参数由指定注解标注的执行方法
execution()   用于匹配是连接点的执行方法
this()        限制连接点匹配AOP代理的bean引用为指定类型的类
target        限制连接点匹配目标对象为指定类型的类
@target()     限制连接点匹配特定的执行对象，这些对象对应的类要具有指定类 型的注解
within()      限制连接点匹配指定的类型
@within()     限制连接点匹配指定注解所标注的类型（当使用Spring AOP时，方法定义在由指定的注解所标注的类里）
@annotation   限定匹配带有指定注解的连接点

AOP配置元素            用途
<aop:advisor>          定义AOP通知器
<aop:after>            定义AOP后置通知（不管被通知的方法是否执行成功）
<aop:afterreturning>   定义AOP返回通知
<aop:afterthrowing>    定义AOP异常通知
<aop:around>           定义AOP环绕通知
<aop:aspect>           定义一个切面
<aop:aspectjautoproxy> 启用@AspectJ注解驱动的切面
<aop:before>           定义一个AOP前置通知
<aop:config>           顶层的AOP配置元素。大多数的<aop:*>元素必须包含 在<aop:config>元素内
<aop:declareparents>   以透明的方式为被通知的对象引入额外的接口
<aop:pointcut>         定义一个切点

## 第２部分　Web中的Spring
### Chap.5 构建Spring Web应用程序

<mvc:annotation-driven>

[mvc:annotation-driven注解的作用](https://blog.csdn.net/qq_35029061/article/details/82945761)
`mvc:annotation-driven`是Spring MVC框架中的一个配置元素，用于启用一些常用的注解驱动的功能。它的作用是自动注册和配置一些关键的注解驱动组件，以便在Spring MVC应用程序中使用它们。

具体来说，`mvc:annotation-driven`的作用包括以下几个方面：
1. 启用注解驱动的处理器映射器和处理器适配器：`mvc:annotation-driven`会自动注册`RequestMappingHandlerMapping`和`RequestMappingHandlerAdapter`，它们分别负责处理控制器类的映射和方法的调用。这样，您可以使用`@RequestMapping`注解来定义请求映射和处理方法，而不需要显式配置XML文件。
2. 支持数据绑定和类型转换：`mvc:annotation-driven`会自动注册`RequestMappingHandlerAdapter`中的一些关键组件，如`HandlerMethodArgumentResolver`和`HandlerMethodReturnValueHandler`，它们负责处理请求参数的绑定和响应结果的转换。通过这些组件，您可以在控制器方法中直接使用JavaBean对象作为参数，并让Spring MVC自动将请求参数绑定到该对象上。
3. 支持请求验证和错误处理：`mvc:annotation-driven`会自动注册`Validator`和`ExceptionHandlerExceptionResolver`，它们用于请求验证和全局的异常处理。通过使用`@Valid`注解和`BindingResult`对象，您可以在控制器方法中进行请求参数验证，并获取验证结果。此外，您还可以定义`@ExceptionHandler`注解的方法来处理控制器中的异常。
4. 支持异步请求处理：`mvc:annotation-driven`会自动注册`AsyncRequestTimeoutException`和`DeferredResultProcessingInterceptor`，以支持异步请求处理。这使得您可以在控制器方法中使用`DeferredResult`和`Callable`类型的返回值，实现异步处理请求和响应。
通过使用`mvc:annotation-driven`，您可以轻松地启用并配置这些注解驱动的功能，减少了显式的XML配置，使得开发更加便捷和高效。

<context:annotation-config/> 注解

当我们需要使用BeanPostProcessor时，直接在Spring配置文件中定义这些Bean显得比较笨拙，例如：
使用@Autowired注解，必须事先在Spring容器中声明AutowiredAnnotationBeanPostProcessor的Bean
使用 @Required注解，就必须声明RequiredAnnotationBeanPostProcessor的Bean
类似地，使用@Resource、@PostConstruct、@PreDestroy等注解就必须声明 CommonAnnotationBeanPostProcessor；使用@PersistenceContext注解，就必须声明 PersistenceAnnotationBeanPostProcessor的Bean。

GenericServlet？
HttpServlet
FrameworkServlet？
DispatcherServlet

HandlerMapping

随书代码
IDEA打开

Could not determine the class-path for interface org.jetbrains.kotlin.gradle.KotlinGradleModel.

Warning:<i><b>root project 'Spittr': Web Facets/Artifacts will not be configured properly</b>
Details: org.gradle.api.artifacts.ResolveException: Could not resolve all dependencies for configuration ':runtime'.
Caused by: org.gradle.internal.resolve.ModuleVersionResolveException: Could not resolve org.springframework:spring-webmvc:4.0.7.RELEASE.
Required by:
    project :
Caused by: org.gradle.internal.resolve.ModuleVersionResolveException: No cached version of org.springframework:spring-webmvc:4.0.7.RELEASE available for offline mode.</i>

https://stackoverflow.com/questions/37747449/no-cached-version-of-com-google-gmsgoogle-services1-x-x-available-for-offline

### Chap. 6 渲染Web视图
jsp
thymeleaf

备注：springmvc支持excel和pdf
AbstractPdfView

返回json字符串
MappingJackson2JsonView
MappingJackson2XmlView

FastJsonJsonView com.alibaba.fastjson.support.spring.FastJsonJsonView fastjson.jar

### Chap. 7 Spring MVC的高级技术

SpringMVC
处理异常
java异常等报错 -> http状态码

### Chap. 8 使用Spring WebFlow
异步 vert.x库
WebFlux
Spring Security在web应用

Part 3

backend

### 9 保护Web应用
Spring Security

## 第3部分　后端中的Spring
### 第10章　通过Spring和JDBC征服数据库

10.3.2　使用JDBC模板

### 第11章　使用对象-关系映射持久化数据

Hibernate

jpa
Spring Data
### 第12章　使用NoSQL数据库
使用MongoTemplate访问MongoDB
使用Neo4jTemplat
使用RedisTemplate

MongoDB
Neo4j
Redis

### 第13章　缓存数据

### 第14章　保护方法应用

spring security

## 第4部分　Spring集成
###  第15章　使用远程服务



### 第16章　使用Spring MVC创建REST API



### 第17章　Spring消息
jms
amqp

spring-jsm这个jar
org.springframework.jms.core.JmsOperations
convertAndSend()
AMQP
https://gitee.com/edidada/spring_jms
ActiveMQ这个中间件

<amq:connectionFactory id="connectionFactory" 
      brokerURL="tcp://localhost:61616" />
      

### 第18章　使用WebSocket和STOMP实现消息功能



### 第19章　使用Spring发送Email

context-support jar

org.springframework.mail.SimpleMailMessage
https://gitee.com/edidada/spring_mail

使用Thymeleaf构建Email消息
使用Velocity构建Email消息
### 第20章　使用JMX管理Spring　Bean



### 第21章　借助Spring Boot简化Spring开发

