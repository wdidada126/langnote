# Spring Aop

Spring2教案_aop事务.docx

可以用来拿方法返回值的通知.png
SpringAOP开发的引入.png
cglib动态代理的实现原理和步骤.png

https://gitee.com/edidada/spring-aopexample
https://github.com/edidada/testmybatisspring   spring aop


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

