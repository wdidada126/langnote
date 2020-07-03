# Spring Aop

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

Spring 切面必须是Java Bean？
MyPersonalAnnotationAspect不加Component注解就不会生效
<<<<<<< HEAD



私有的方法spring的aop是不是不会生效







自己实现SpringAOP，含AOP实现的步骤分解

　　　　（1）被代理类、被代理类的接口、通知的注解类的创建；

　　　　（2）创建一个“动态代理类”，并把“被代理类的实例”传给该代理类；在该动态代理类的invoke()方法中，实现前置通知、后置通知等各种通知，也是在该invoke()方法中调用、执行真正的代理类要执行的那个方法。

　　　　（3）创建一个可以动态创建“代理类的实例”的类，通过该类的getProxyInstance(Object obj)方法可以得到一个动态代理类的实例。
　　　　（4）给方法加通知注解，该方法的实例须已交由IOC容器管理的；
　　　　（5）遍历BeanFactory，找出方法上有@通知注解的bean，为这些bean生成代理类对象（步骤：MyProxy3.getProxyInstance(Object obj)）

　　　　（6）用代理类的实例去替代BeanFactory中的被代理类的实例
=======
>>>>>>> afe522da082020e5ece0b75c43067644b2edb768
