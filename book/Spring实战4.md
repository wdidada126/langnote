# Spring实战4

2016-4

Spring实战（第5版 ） 2020

java实现一个功能，首先看spring是否内置支持

spring支持发送邮件，就不用三方库了

克雷格·沃斯（Craig Walls）
Pivotal的首席软件工程师、畅销书作者、Spring框架的热情支持者，经常在各种技术会议上发表演讲。

https://book.douban.com/subject/26767354/
## 1

### Chap.1

EJB

JavaBean规范

POJO 简单老Java对象



应用上下文ApplicationContext
Android里面也有Context QT WPF里面
Spring容器 Spring container
WPF MVVM


问Spring的应用上下文有几种实现？有什么区别

主要是加载bean的方式不同
1.xml
2.注解



bean的生命周期
BeanName
BeanFactory
DisposeBean





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



```
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
```
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
```
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



```
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



@Autowired 可以对成员变量、方法以及构造函数进行注释
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


        <dependency>
            <groupId>javax.inject</groupId>
            <artifactId>javax.inject</artifactId>
            <version>1</version>
        </dependency>


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

在Spring 4之前，很难实现这种级别的条件化配置，但是Spring 4引入 了一个新的@Conditional注解，它可以用到带有@Bean注解的方 法上。如果给定的条件计算结果为true，就会创建这个bean，否则的话，这个bean会被忽略。

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

jionpoint
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

https://blog.csdn.net/qq_35029061/article/details/82945761



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
th


### Chap. 7 Spring MVC的高级技术

SpringMVC

处理异常

java异常等报错 -> http状态码

### Chap. 8 使用Spring WebFlow

WebFlux

Spring Security在web应用

Part 3

backend



### 9 保护Web应用



## 第3部分　后端中的Spring
### 第10章　通过Spring和JDBC征服数据库



### 第11章　使用对象-关系映射持久化数据

Hibernate

jpa

### 第12章　使用NoSQL数据库



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

https://gitee.com/edidada/spring_jms

ActiveMQ这个中间件


<amq:connectionFactory id="connectionFactory" 
      brokerURL="tcp://localhost:61616" />
      

### 第18章　使用WebSocket和STOMP实现消息功能



### 第19章　使用Spring发送Email

context-support jar

org.springframework.mail.SimpleMailMessage
https://gitee.com/edidada/spring_mail

### 第20章　使用JMX管理Spring　Bean



### 第21章　借助Spring Boot简化Spring开发







