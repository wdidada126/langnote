# Spring实战4



https://book.douban.com/subject/26767354/



### Chap.1

EJB

JavaBean规范

POJO 简单老Java对象



应用上下文ApplicationContext

Android里面也有Context QT WPF里面

Spring容器 Spring container



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

### Chap . 2



@Autowired注解可以使用哪些地方

field

构造函数？

方法？



@Autowired 可以对成员变量、方法以及构造函数进行注释

https://www.cnblogs.com/acm-bingzi/p/springAutowired.html





javax.inject.Inject

javax.inject.Named



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


​		
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





### Chap. 3

在3.1版本中，Spring引入了bean profile的功能。要使用profile，你首 先要将所有不同的bean定义整理到一个或多个profile之中，在将应用 部署到每个环境时，要确保对应的profile处于激活（active）的状态

在Spring 4之前，很难实现这种级别的条件化配置，但是Spring 4引入 了一个新的@Conditional注解，它可以用到带有@Bean注解的方 法上。如果给定的条件计算结果为true，就会创建这个bean，否则 的话，这个bean会被忽略。

### Chap. 4

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

## Chap.5



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

## Chap. 6



## Chap. 7

SpringMVC

## Chap. 8

WebFlux

Spring Security在web应用

Part 3

backend

## Chap. 21


