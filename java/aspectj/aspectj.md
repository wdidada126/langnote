# aspectj

Aspectj 

https://blog.csdn.net/autfish/article/details/51184405
https://blog.csdn.net/woshiyigeliangliang/article/details/81450443

https://gitee.com/edidada/testaspectj  @Aspectj注解
https://gitee.com/edidada/aspectj  .aj文件
https://gitee.com/edidada/spring-aopexample spring使用@Aspectj注解

https://www.eclipse.org/aspectj/


runtime
weaver

aspectjrt - the AspectJ runtime
aspectjweaver - the AspectJ weaver
aspectjtools - the AspectJ compiler
aspectjmatcher - the AspectJ matcher

aspectjtools这个jar包有main函数，ajbrowser ajc ajdoc命令行工具的实现
java程序只需要引入aspectjtools就可以编译

@Aspect注解在aspectjtools这个jar包里面
@Before注解在aspectjtools这个jar包里面

https://www.eclipse.org/aspectj/doc/released/runtime-api/index.html
https://www.eclipse.org/aspectj/doc/released/weaver-api/index.html


书籍
https://www.amazon.com/exec/obidos/ASIN/0321245873/


源代码仓库
https://github.com/eclipse-aspectj/aspectj

跟java的兼容性
https://github.com/eclipse-aspectj/aspectj/blob/master/docs/dist/doc/JavaVersionCompatibility.md



JoinPoint 接口实现类
JoinPointImpl

org.aspectj.lang.JoinPoint
    ProceedingJoinPoint (org.aspectj.lang)
        JoinPointImpl (org.aspectj.runtime.reflect)


JoinPoint api
Signature getSignature()
SourceLocation getSourceLocation()


kind method-execution

### ajc



## AOP术语

连接点（Joinpoint）

被增强的方法是连接点也叫切入点(某一类的里面的所有方法)，增强（Advice）内容里面的方法都是连接点，也存在是连接点，但不是切入点的情况。就是没被增强的方法，就不是切入点。

切点（Pointcut）

被增强的连接点是切入点。没被增强的是连接点但不是切入点。

AOP通过“切点”定位特定的连接点。连接点相当于数据库中的记录，而切点相当于查询条件。

增强（Advice）

就相当于你走到切入点了，然后你告诉切入点“不行！刚刚用拳头打的不过瘾，我要用锤子“增强”一下。”这个顺便要做的事情就是增强。

1.前置增强：就是在被增强方法执行前执行

2.后置增强：被增强方法执行后紧接着执行

3.异常增强：爆出异常时候执行（后置增强和异常增强二者只能执行一个）

4.最终增强：最终一定会执行的增强也是最后执行。

织入（Weaving）

织入说白了就是将切面与切入点结合这是个逻辑过程，AOP有三种织入的方式：

a、编译期织入，这要求使用特殊的Java编译器。

b、类装载期织入，这要求使用特殊的类装载器。

c、动态代理织入，在运行期为目标类添加增强生成子类的方式。



而spring 使用了aspectJ注解的一小部分（正如前面所说的，受限于jdk的动态代理，spring只支持方法级别的切面）

只看spring整合aspectj

aspectj pom.xml依赖

AspectJ的几种织入方式，分别是compile-time、post-compile 和 load-time，分别对应着编译期、后编译期、加载期织入
spring是在运行期进行的织入。
spring是在运行期进行的织入。
spring是在运行期进行的织入。

[maven-weave-aspectj](https://github.com/edidada/maven-weave-aspectj)



1.8.9



1.9.3



Java5+ 之后 AspectJ 可以写成 Java 类加注解的方式，*.aj 文件一般都没太大必要了



只要用 `@Aspect` 标识出它是一个 Aspect, 或者也可以完全用 AspectJ 语法，创建 *.aj 文件，里面写 `public aspect MethodStartAspect` 这样的的定义



http://www.eclipse.org/aspectj/



https://www.eclipse.org/aspectj/doc/released/progguide/examples-howto.html



有可执行文件，生成.class文件？

asm字节码技术




[使用插件 aspectj-maven-plugin 织入 AspectJ AOP](https://blog.csdn.net/weixin_34417814/article/details/92531310)

使用插件 aspectj-maven-plugin 织入 AspectJ AOP

https://blog.csdn.net/weixin_34417814/article/details/92531310



aspectj-maven-plugin

```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.codehaus.mojo</groupId>
            <artifactId>aspectj-maven-plugin</artifactId>
            <version>1.11</version>
            <executions>
                <execution>
                    <goals>
                        <goal>compile</goal>
                    </goals>
                </execution>
            </executions>
            <configuration>
                <source>1.8</source>
                <target>1.8</target>
                <sourceDirectory>src/main/aspect</sourceDirectory>
                <outputDirectory>target/aspect-classes</outputDirectory>
            </configuration>
        </plugin>
    </plugins>
</build>
```



[aspectjweaver和aspectjrt的作用 作用、说明、案例 ](https://www.cnblogs.com/Peter-Yu/p/11604969.html)

[aspectjweaver和aspectjrt的作用？（作用、说明、案例）](https://www.cnblogs.com/Peter-Yu/p/11604969.html)






aspectjweaver

aj.org.objectweb.asm.CurrentFrame



aspectjweaver包含aspectjrt



例子

AspectJ是一个面向切面的AOP框架，AOP的织入方式分为编译期织入、装载期织入、运行期织入。



[AspectJ使用示例](https://blog.csdn.net/u012477420/article/details/71981950)



aspectj vs Spring AOP

[比较Spring AOP与AspectJ](https://juejin.im/post/5a695b3cf265da3e47449471)



简而言之，Spring AOP和AspectJ有不同的目标。
 Spring AOP旨在通过Spring IoC提供一个简单的AOP实现，以解决编码人员面临的最常出现的问题。这并不是完整的AOP解决方案，它只能用于Spring容器管理的beans。

另一方面，AspectJ是最原始的AOP实现技术，提供了完整的AOP解决方案。AspectJ更为健壮，相对于Spring AOP也显得更为复杂。值得注意的是，AspectJ能够被应用于所有的领域对象。

Spring AOP 是一个基于代理的AOP框架。这意味着，要实现目标对象的切面，将会创建目标对象的代理类。这可以通过下面两种方式实现：

- JDK动态代理：Spring AOP的首选方法。 每当目标对象实现一个接口时，就会使用JDK动态代理。
- CGLIB代理：如果目标对象没有实现接口，则可以使用CGLIB代理。






[Aspectj中call与execution区别，织入代码位置不同](https://blog.csdn.net/Dax1n/article/details/81944975)

[AspectJ切入点@Pointcut语法详解](https://www.mekau.com/4880.html)

分类pointcuts 遵循特定的语法用于捕获每一个种类的可使用连接点。 主要的种类：
方法执行：execution(MethodSignature)
方法调用：call(MethodSignature)
构造器执行：execution(ConstructorSignature)
构造器调用：call(ConstructorSignature)
类初始化：staticinitialization(TypeSignature)
属性读操作：get(FieldSignature)
属性写操作：set(FieldSignature)
例外处理执行：handler(TypeSignature)
对象初始化：initialization(ConstructorSignature)
对象预先初始化：preinitialization(ConstructorSignature)





.aj文件

aspectj自用编译器



下一步，查看其他编程语言是如何实现aop的



aop的实现原理



修改字节码

ajc编译器



[AspectJ 入门](https://www.jianshu.com/p/f9acae180f81)






https://www.eclipse.org/aspectj/doc/released/progguide/examples-howto.html



[AspectJ在Spring中的使](https://www.jianshu.com/p/958af6a90477)

## 源码解读 v1.9.6

org.aspectj.lang.annotation



https://javadoc.dev/online/api/org.aspectj/aspectjweaver/1.9.6/index.html



| Annotation Types   |      |        |
| ------------------ | ---- | ------ |
|                    |      |        |
| AdviceName         |      |        |
| After              | 注解 |        |
| AfterReturning     |      |        |
| AfterThrowing      |      |        |
| Around             |      |        |
| Aspect             | 注解 | 很重要 |
| Before             | 注解 |        |
| DeclareAnnotation  |      |        |
| DeclareError       |      |        |
| DeclareMixin       |      |        |
| DeclareParents     |      |        |
| DeclarePrecedence  |      |        |
| DeclareWarning     |      |        |
| Pointcut           | 注解 |        |
| RequiredTypes      |      |        |
| SuppressAjWarnings |      |        |

