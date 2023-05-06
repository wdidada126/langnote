# Spring Aop

Spring2教案_aop事务.docx

可以用来拿方法返回值的通知.png
SpringAOP开发的引入.png
cglib动态代理的实现原理和步骤.png

https://gitee.com/edidada/spring-aopexample   spring aop
https://gitee.com/edidada/springexample

A : public class MyServiceImpl implements MyService
B : public class MyServiceImpl

上面的报错，

```java
Exception in thread "main" org.springframework.beans.factory.NoSuchBeanDefinitionException: No qualifying bean of type 'cn.wdidada.test.aop.impl.MyServiceImpl' available
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.getBean(DefaultListableBeanFactory.java:353)
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.getBean(DefaultListableBeanFactory.java:340)
	at org.springframework.context.support.AbstractApplicationContext.getBean(AbstractApplicationContext.java:1090)
	at cn.wdidada.test.aop.TestMyBatisAOPSpring.main(TestMyBatisAOPSpring.java:27)
```

下面的可以


上面为什么报错，因为aop方式是动态代理

internalAutoProxyCreator
internalAutoProxyCreator是Spring AOP中的一个Bean后置处理器，它的主要作用是自动创建AOP代理对象。

在Spring中，当一个Bean被注册到容器中时，internalAutoProxyCreator会检查该Bean是否需要被代理。如果该Bean需要被代理，并且没有指定具体的代理方式，internalAutoProxyCreator会根据该Bean的类型和配置信息自动选择合适的代理方式，并创建代理对象。代理对象将替代原始对象，成为该Bean在应用中的实际实例。
internalAutoProxyCreator的具体工作流程如下：
遍历所有Bean的定义，找到需要被代理的Bean。
根据代理的目标类型和配置信息，选择合适的代理方式（JDK动态代理或CGLIB代理）。
创建代理对象，将其注册到Spring容器中。
将代理对象返回给调用方，替代原始对象成为该Bean在应用中的实际实例。
需要注意的是，internalAutoProxyCreator只会对满足以下条件的Bean进行代理：
Bean必须是一个单例（Singleton）。
Bean必须是一个AOP代理的目标对象（Target Object）。
Bean必须符合AOP代理的切点条件。
由于internalAutoProxyCreator是一个Bean后置处理器，它是在Bean实例化之后、初始化之前被调用的。因此，在使用internalAutoProxyCreator时，需要确保代理的目标对象已经被实例化，但还没有被初始化。如果代理的目标对象已经被初始化，internalAutoProxyCreator将无法创建代理对象。
总的来说，internalAutoProxyCreator是Spring AOP中非常重要的一个组件，它为Spring AOP提供了自动代理的能力，简化了AOP的配置和使用。


`AspectJPointcutAdvisor`是Spring AOP中的一个类，用于将AspectJ切点与通知（Advice）关联起来，构成一个切面（Aspect）。它是Spring AOP中切面的基本组成部分之一。
在Spring AOP中，切面（Aspect）是由切点（Pointcut）和通知（Advice）组成的。切点用于定义需要拦截的方法，而通知用于定义拦截后需要执行的逻辑。`AspectJPointcutAdvisor`的作用就是将切点和通知组合在一起，创建一个切面。
`AspectJPointcutAdvisor`通过实现`org.springframework.aop.PointcutAdvisor`接口来实现。它包含两个重要的属性：`Pointcut`和`Advice`。`Pointcut`用于定义需要拦截的方法，可以使用AspectJ切点表达式来描述；`Advice`用于定义拦截后需要执行的逻辑，可以是前置通知、后置通知、环绕通知等。
例如，以下是一个示例，它使用`AspectJPointcutAdvisor`来定义一个切面，拦截`com.example.service.UserService`类的所有方法，并在方法执行前后输出日志信息：

```java
@Aspect
@Component
public class LoggingAspect {

    @Pointcut("execution(* com.example.service.UserService.*(..))")
    public void userServicePointcut() {}

    @Around("userServicePointcut()")
    public Object logMethodExecutionTime(ProceedingJoinPoint joinPoint) throws Throwable {
        long startTime = System.currentTimeMillis();
        Object result = joinPoint.proceed();
        long endTime = System.currentTimeMillis();
        String methodName = joinPoint.getSignature().getName();
        String className = joinPoint.getTarget().getClass().getSimpleName();
        System.out.println(className + "." + methodName + " executed in " + (endTime - startTime) + "ms");
        return result;
    }

    @Bean
    public AspectJPointcutAdvisor userServiceAdvisor() {
        AspectJExpressionPointcut pointcut = new AspectJExpressionPointcut();
        pointcut.setExpression("execution(* com.example.service.UserService.*(..))");
        return new AspectJPointcutAdvisor(pointcut, this::logMethodExecutionTime);
    }
}
```

在上面的示例中，`@Aspect`注解用于声明一个切面类，`@Pointcut`注解用于定义一个切点，它拦截`com.example.service.UserService`类的所有方法。`@Around`注解用于定义一个环绕通知，它拦截`userServicePointcut()`切点，并在方法执行前后输出日志信息。`@Bean`注解用于定义一个Bean，它创建一个`AspectJPointcutAdvisor`对象，将切点和通知组合在一起，形成一个切面。通过这种方式，可以将日志逻辑从业务逻辑中分离出来，以模块化的方式进行管理，提高代码的可维护性和可扩展性。
需要注意的是，`AspectJPointcutAdvisor`适用于使用AspectJ切点表达式的情况，如果需要使用其他类型的切点，可以使用其他类型的Advisor，例如`NameMatchMethodPointcutAdvisor`、`RegexpMethodPointcutAdvisor`等。

org.springframework.aop.aspectj.AspectJPointcutAdvisor




`AspectJPointcutAdvisor`是Spring AOP中的一个类，用于将AspectJ切点与通知（Advice）关联起来，构成一个切面（Aspect）。它是Spring AOP中切面的基本组成部分之一。
在Spring AOP中，切面（Aspect）是由切点（Pointcut）和通知（Advice）组成的。切点用于定义需要拦截的方法，而通知用于定义拦截后需要执行的逻辑。`AspectJPointcutAdvisor`的作用就是将切点和通知组合在一起，创建一个切面。
`AspectJPointcutAdvisor`通过实现`org.springframework.aop.PointcutAdvisor`接口来实现。它包含两个重要的属性：`Pointcut`和`Advice`。`Pointcut`用于定义需要拦截的方法，可以使用AspectJ切点表达式来描述；`Advice`用于定义拦截后需要执行的逻辑，可以是前置通知、后置通知、环绕通知等。
例如，以下是一个示例，它使用`AspectJPointcutAdvisor`来定义一个切面，拦截`com.example.service.UserService`类的所有方法，并在方法执行前后输出日志信息：
```java
@Aspect
@Component
public class LoggingAspect {

    @Pointcut("execution(* com.example.service.UserService.*(..))")
    public void userServicePointcut() {}

    @Around("userServicePointcut()")
    public Object logMethodExecutionTime(ProceedingJoinPoint joinPoint) throws Throwable {
        long startTime = System.currentTimeMillis();
        Object result = joinPoint.proceed();
        long endTime = System.currentTimeMillis();
        String methodName = joinPoint.getSignature().getName();
        String className = joinPoint.getTarget().getClass().getSimpleName();
        System.out.println(className + "." + methodName + " executed in " + (endTime - startTime) + "ms");
        return result;
    }

    @Bean
    public AspectJPointcutAdvisor userServiceAdvisor() {
        AspectJExpressionPointcut pointcut = new AspectJExpressionPointcut();
        pointcut.setExpression("execution(* com.example.service.UserService.*(..))");
        return new AspectJPointcutAdvisor(pointcut, this::logMethodExecutionTime);
    }
}
```

在上面的示例中，`@Aspect`注解用于声明一个切面类，`@Pointcut`注解用于定义一个切点，它拦截`com.example.service.UserService`类的所有方法。`@Around`注解用于定义一个环绕通知，它拦截`userServicePointcut()`切点，并在方法执行前后输出日志信息。`@Bean`注解用于定义一个Bean，它创建一个`AspectJPointcutAdvisor`对象，将切点和通知组合在一起，形成一个切面。通过这种方式，可以将日志逻辑从业务逻辑中分离出来，以模块化的方式进行管理，提高代码的可维护性和可扩展性。
需要注意的是，`AspectJPointcutAdvisor`适用于使用AspectJ切点表达式的情况，如果需要使用其他类型的切点，可以使用其他类型的Advisor，例如`NameMatchMethodPointcutAdvisor`、`RegexpMethodPointcutAdvisor`等。


<aop:aspectj-autoproxy proxy-target-class="true"/>

https://gitee.com/edidada/springbootwebaop  spring boot aop实现

### 应用领域
日志 数据库事务 安全 缓存


私有的方法spring的aop是不是不会生效的吗？

Spring AOP默认使用的是JDK动态代理，而JDK动态代理只能代理实现了接口的类，对于没有实现接口的类，Spring AOP会选择使用CGLIB来动态代理。CGLIB是一个强大的高性能的代码生成库，它可以在运行期扩展Java类与实现Java接口。但是，CGLIB不能代理final修饰的方法和类，同时也不能代理static修饰的方法和类。对于private方法，在Spring使用纯Spring AOP（只能拦截public/protected/包）都是无法被拦截的




spring AOP的五种通知 Advice
1、@Before：
前置通知，在目标方法执行前执行。
2、@After ：
后置通知，在目标方法返回结果之后执行，无论是否出现异常都会执行。
3、@AfterReturning：
返回后通知，在目标方法执行后执行，如果出现异常不会执行。
4、@AfterThrowing：
异常通知，在目标方法抛出异常后执行。
5、@Around：
环绕通知，围绕着方法执行.


JoinPoint

poincut

Aspect

Introduce

Weaveing



@Aspect注解作用
这个类是一个spring bean
声明aop
@Aspect注解是Spring AOP框架中的一个注解，用于声明一个切面（Aspect）。切面是一种横切逻辑，它可以拦截应用程序中的方法调用，并在方法执行前、执行后或执行异常时执行额外的逻辑。

在使用@Aspect注解时，需要结合其他注解一起使用，以定义切点和增强等相关信息。常用的注解包括：

@Pointcut：用于定义切点，可以将一组方法定义为一个切点。
@Before：用于在方法执行前执行增强逻辑。
@After：用于在方法执行后执行增强逻辑。
@AfterReturning：用于在方法正常返回后执行增强逻辑。
@AfterThrowing：用于在方法抛出异常后执行增强逻辑。

@Aspect注解修饰的类必须是spring ioc中的bean吗？
是的，使用@Aspect注解声明的切面类必须是Spring IoC容器中的Bean。这是因为Spring AOP框架是基于Spring IoC容器实现的，它通过在IoC容器中查找切面Bean来创建切面对象，从而实现切面的拦截和增强。
在使用@Aspect注解时，还需要结合其他注解一起使用，如@Pointcut、@Before、@After、@Around等注解，用于定义切点和增强等相关信息。这些注解都是Spring框架提供的注解，并依赖于Spring IoC容器来实现Bean的创建和管理。
因此，使用@Aspect注解声明的切面类必须交由Spring IoC容器管理，并且需要在配置文件或通过注解方式将其声明为Bean，才能被Spring框架正确地创建和使用。如果没有将切面类声明为Bean，Spring框架将无法创建切面对象，从而无法实现切面的拦截和增强。



D:\git\github\langnote\imgs\spring\spring_aop声明通知方法.PNG
aspect切点表达式.PNG

java切面.PNG

非侵入xml切面1.PNG
非侵入xml切面2.PNG

### 相关资料

spring实战4章

https://docs.spring.io/spring-framework/docs/3.0.x/spring-framework-reference/html/aop.html

spring aop没有生效

https://blog.csdn.net/weixin_39681171/article/details/113039439


```java
    @Pointcut("execution(public * cn.wdidada.test.springbootwebaop..*.*(..))")
```


匹配哪些方法
修饰符 返回值 类名 方法名 参数个数类型





创建注解
创建spring容器类 添加@Aspect注解
添加@PoinCut
添加@Aoround注解，注意返回值必须有，参数需要是ProceedingJoinPoint ，调用joinPoint.proceed();

```java
    @Around("planChangePointcut() && @annotation(cn.wdidada.test.springbootwebaop.annotion.PlanChange)")
    public Object planChangeAround(ProceedingJoinPoint joinPoint) throws Throwable{
        System.out.println("Around");
        MethodSignature methodSignature = (MethodSignature) joinPoint.getSignature();
        Method method = methodSignature.getMethod();
        PlanChange change = method.getAnnotation(PlanChange.class);
        change.tableName();
        return joinPoint.proceed();
    }
```




如何强制使用CGLIB实现AOP？

 （1）添加CGLIB库，SPRING_HOME/cglib/*.jar

 （2）在spring配置文件中加入<aop:aspectj-autoproxy proxy-target-class="true"/>



[基于注解的Spring AOP的配置和使用](https://my.oschina.net/sniperLi/blog/491854)

在Spring AOP中有两种代理方式，JDK动态代理和CGLIB代理。默认情况下，TargetObject实现了接口时，则采用JDK动态代理，例如，AServiceImpl；反之，采用CGLIB代理，例如，BServiceImpl。强制使用CGLIB代理需要将 <aop:config>的 proxy-target-class属性设为true。


```java

Caused by: java.lang.IllegalArgumentException: Pointcut is not well-formed: expecting 'identifier' at character position 0

^
	at org.aspectj.weaver.tools.PointcutParser.resolvePointcutExpression(PointcutParser.java:316)
	at org.aspectj.weaver.reflect.InternalUseOnlyPointcutParser.resolvePointcutExpression(InternalUseOnlyPointcutParser.java:36)
	at org.aspectj.weaver.reflect.Java15ReflectionBasedReferenceTypeDelegate.getDeclaredPointcuts(Java15ReflectionBasedReferenceTypeDelegate.java:307)
	at org.aspectj.weaver.ReferenceType.getDeclaredPointcuts(ReferenceType.java:884)
	at org.aspectj.weaver.ResolvedType$PointcutGetter.get(ResolvedType.java:243)
	at org.aspectj.weaver.ResolvedType$PointcutGetter.get(ResolvedType.java:241)
	at org.aspectj.weaver.Iterators$4$1.hasNext(Iterators.java:213)
	at org.aspectj.weaver.Iterators$4.hasNext(Iterators.java:230)
	at org.aspectj.weaver.ResolvedType.findPointcut(ResolvedType.java:743)
	at org.aspectj.weaver.patterns.ReferencePointcut.resolveBindings(ReferencePointcut.java:148)
	at org.aspectj.weaver.patterns.Pointcut.resolve(Pointcut.java:189)
	at org.aspectj.weaver.tools.PointcutParser.resolvePointcutExpression(PointcutParser.java:313)
	at org.aspectj.weaver.tools.PointcutParser.parsePointcutExpression(PointcutParser.java:294)
	at org.springframework.aop.aspectj.AspectJExpressionPointcut.buildPointcutExpression(AspectJExpressionPointcut.java:217)
	at org.springframework.aop.aspectj.AspectJExpressionPointcut.checkReadyToMatch(AspectJExpressionPointcut.java:190)
	at org.springframework.aop.aspectj.AspectJExpressionPointcut.getClassFilter(AspectJExpressionPointcut.java:169)
	at org.springframework.aop.support.AopUtils.canApply(AopUtils.java:220)
	at org.springframework.aop.support.AopUtils.canApply(AopUtils.java:279)
	at org.springframework.aop.support.AopUtils.findAdvisorsThatCanApply(AopUtils.java:311)
	at org.springframework.aop.framework.autoproxy.AbstractAdvisorAutoProxyCreator.findAdvisorsThatCanApply(AbstractAdvisorAutoProxyCreator.java:119)
	at org.springframework.aop.framework.autoproxy.AbstractAdvisorAutoProxyCreator.findEligibleAdvisors(AbstractAdvisorAutoProxyCreator.java:89)
	at org.springframework.aop.framework.autoproxy.AbstractAdvisorAutoProxyCreator.getAdvicesAndAdvisorsForBean(AbstractAdvisorAutoProxyCreator.java:70)
	at org.springframework.aop.framework.autoproxy.AbstractAutoProxyCreator.wrapIfNecessary(AbstractAutoProxyCreator.java:346)
	at org.springframework.aop.framework.autoproxy.AbstractAutoProxyCreator.postProcessAfterInitialization(AbstractAutoProxyCreator.java:298)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.applyBeanPostProcessorsAfterInitialization(AbstractAutowireCapableBeanFactory.java:423)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.initializeBean(AbstractAutowireCapableBeanFactory.java:1633)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.doCreateBean(AbstractAutowireCapableBeanFactory.java:555)
	... 60 more

```

```java

@Aspect
@Component
public class MyPersonalAnnotationAspect {

    @Pointcut("")
    public void testArgs(){

    }
}

```

Pointcut is not well-formed: expecting 'identifier' at character position 0

Spring 切面必须是Java Bean？ 对
MyPersonalAnnotationAspect不加Component注解就不会生效




私有的方法spring的aop是不是不会生效







自己实现SpringAOP，含AOP实现的步骤分解

　　　　（1）被代理类、被代理类的接口、通知的注解类的创建；

　　　　（2）创建一个“动态代理类”，并把“被代理类的实例”传给该代理类；在该动态代理类的invoke()方法中，实现前置通知、后置通知等各种通知，也是在该invoke()方法中调用、执行真正的代理类要执行的那个方法。

　　　　（3）创建一个可以动态创建“代理类的实例”的类，通过该类的getProxyInstance(Object obj)方法可以得到一个动态代理类的实例。
　　　　（4）给方法加通知注解，该方法的实例须已交由IOC容器管理的；
　　　　（5）遍历BeanFactory，找出方法上有@通知注解的bean，为这些bean生成代理类对象（步骤：MyProxy3.getProxyInstance(Object obj)）

　　　　（6）用代理类的实例去替代BeanFactory中的被代理类的实例

