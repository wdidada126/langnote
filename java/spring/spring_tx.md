# spring tx

api doc
https://docs.qq.com/sheet/DSU9VV2Zsand6bXdT

https://docs.spring.io/spring-framework/docs/current/javadoc-api/



PlatformTransactionManager

注入失败
开启事务
手动开启事务
手动提交事务



org.springframework.transaction.TransactionDefinition接口
封装了@Transactional的传播属性和隔离级别
某个实现类DefaultTransactionDefinition


spring-tx包里面的
DefaultTransactionDefinition (org.springframework.transaction.support)
    DefaultTransactionAttribute (org.springframework.transaction.interceptor)
        RuleBasedTransactionAttribute (org.springframework.transaction.interceptor)




org.springframework.aop.framework.CglibAopProxy.DynamicAdvisedInterceptor#intercept
    org.springframework.aop.framework.ReflectiveMethodInvocation#proceed
        org.springframework.aop.interceptor.ExposeInvocationInterceptor#invoke
            org.springframework.aop.framework.ReflectiveMethodInvocation#proceed
                org.springframework.transaction.interceptor.TransactionInterceptor#invoke
                    org.springframework.transaction.interceptor.TransactionAspectSupport#invokeWithinTransaction

AbstractPlatformTransactionManager
aptm
tm TransactionManager
dsTransactionManager

TransactionSynchronizationManager
TransactionSynchronizationManager主要用于多事务资源的协调,具体来说主要有以下作用:

1. 管理事务同步。它允许代码在事务提交或回滚时同步执行。这是通过注册TransactionSynchronization对象实现的。

2. 管理事务范围变量。它允许在事务范围内存储和访问变量。这些变量仅在事务提交后才对下一个事务可见。

3. 应用事务到无事务资源。它允许在事务中访问非事务性的资源,比如JMS目标等。

总的来说,TransactionSynchronizationManager是Spring提供的用于统一处理多事务资源的重要工具类。主要用于管理和协调事务中的各种资源,帮助事务资源之间具有一致性。

所以简单点说,TransactionSynchronizationManager主要用于:

- 事务提交和回滚时的同步工作(调用listener)
- 事务范围内的变量管理
- 将事务作用域扩展到非事务资源上



TransactionAspectSupport
`TransactionAspectSupport` 是 Spring 框架中的一个类，提供了在事务切面中使用的一些公共方法和属性。它是 Spring 事务管理的核心类之一，用于支持 Spring 中的声明式事务管理。

在 Spring 中，事务切面是通过 AOP 的方式实现的。当一个方法被声明为事务性方法时，Spring 会自动生成一个代理对象，该代理对象会织入事务切面的通知，以提供事务管理的功能。`TransactionAspectSupport` 类提供了一些实用方法，以便在事务切面中获取和管理事务相关的信息。

其中一些常用的方法包括：

- `currentTransactionStatus()`：获取当前方法的事务状态对象 `TransactionStatus`。
- `currentTransactionInfo()`：获取当前方法的事务信息对象 `TransactionInfo`。
- `invokeWithinTransaction()`：在当前事务上下文中执行给定的 `Callable` 对象，并返回其结果。
- `completeTransactionAfterThrowing()`：在事务发生异常时，回滚当前事务并将异常重新抛出。

`TransactionAspectSupport` 还提供了一些 Hook 方法，用于在事务切面中进行定制化的处理，如：

- `prepareTransactionInfo()`：在事务开始之前，准备事务信息对象 `TransactionInfo`。
- `prepareTransactionStatus()`：在事务开始之前，准备事务状态对象 `TransactionStatus`。
- `beginTransaction()`：在事务开始时，执行一些额外的处理。
- `commitTransactionAfterReturning()`：在事务正常结束时，提交当前事务并执行一些额外的处理。
- `handleException()`：在事务发生异常时，处理异常并执行一些额外的处理。

`TransactionAspectSupport` 是 Spring 事务管理的核心支持类之一，提供了丰富的方法和 Hook 方法，可以帮助开发人员实现各种定制化的事务处理逻辑。在使用 Spring 进行声明式事务管理时，开发人员可以继承 `TransactionAspectSupport` 类，以便在事务切面中使用其提供的实用方法和 Hook 方法。

	
https://github.com/edidada/testspringaops
https://gitee.com/edidada/testspringaops



MethodInterceptor接口
Object invoke(MethodInvocation invocation) throws Throwable;

org.springframework.transaction.interceptor.TransactionInterceptor#invoke

CglibAopProxy类继承AopProxy接口

@Transactional注解全路径
```
org.springframework.transaction.annotation.Transactional
```
打印事务日志


@Transactional注解

<aop:config>作用

propagation
传播;扩展;宣传;培养

https://blog.csdn.net/sayoko06/article/details/79164858

- REQUIRED：支持当前事务，如果当前没有事务，就新建一个事务。这是最常见的选择。 
- SUPPORTS：支持当前事务，如果当前没有事务，就以非事务方式执行。 
- MANDATORY：支持当前事务，如果当前没有事务，就抛出异常。 
- REQUIRES_NEW：新建事务，如果当前存在事务，把当前事务挂起。 
- NOT_SUPPORTED：以非事务方式执行操作，如果当前存在事务，就把当前事务挂起。 
- NEVER：以非事务方式执行，如果当前存在事务，则抛出异常。 
- NESTED：支持当前事务，如果当前事务存在，则执行一个嵌套事务，如果当前没有事务，就新建一个事务。

https://www.cnblogs.com/xd502djj/p/10940627.html


spring 事务 如何打印日志
https://cloud.tencent.com/developer/ask/116430

```shell script
2012-08-22 18:50:00,031 TRACE - Getting transaction for [com.MyClass.myMethod]
[my own log statements from method com.MyClass.myMethod]
2012-08-22 18:50:00,142 TRACE - Completing transaction for [com.MyClass.myMethod]
```

Spring context日志打印了，tx jdbc的日志没有打印
1、源码调试 jcl需要尤其注意
2、问开源社区

tx jdbc

https://blog.csdn.net/liujianyangbj/article/details/104990100

debug 改变量的值
[main] TRACE org.springframework.transaction.interceptor.TransactionInterceptor - Completing transaction for [cn.wdidada.spring.testspringaop.service.impl.UserServiceImpl.insertUser] after exception: java.lang.RuntimeException: 
[main] TRACE org.springframework.transaction.interceptor.RuleBasedTransactionAttribute - Applying rules to determine whether transaction should rollback on java.lang.RuntimeException: 
[main] TRACE org.springframework.transaction.interceptor.RuleBasedTransactionAttribute - Winning rollback rule is: RollbackRuleAttribute with pattern [java.lang.Exception]

spring源码重写了 apache.commons.logging

```shell script
org.springframework.context.support.AbstractApplicationContext
```
apache.commons.logging

spring-context强依赖apache commons log（也是日志接口）

```shell script
[TRACE] TransactionSynchronizationManager - Bound value [org.springframework.jdbc.datasource.ConnectionHolder@7393222f] for key [HikariDataSource (HikariPool-1)] to thread [main]
[TRACE] TransactionSynchronizationManager - Retrieved value [org.springframework.jdbc.datasource.ConnectionHolder@7393222f] for key [HikariDataSource (HikariPool-1)] bound to thread [main]
[TRACE] TransactionSynchronizationManager - Retrieved value [org.springframework.jdbc.datasource.ConnectionHolder@7393222f] for key [HikariDataSource (HikariPool-1)] bound to thread [main]
[TRACE] TransactionSynchronizationManager - Retrieved value [org.mybatis.spring.SqlSessionHolder@389b0789] for key [org.apache.ibatis.session.defaults.DefaultSqlSessionFactory@35a3d49f] bound to thread [main]
[TRACE] TransactionSynchronizationManager - Retrieved value [org.mybatis.spring.SqlSessionHolder@389b0789] for key [org.apache.ibatis.session.defaults.DefaultSqlSessionFactory@35a3d49f] bound to thread [main]
[TRACE] TransactionInterceptor - Completing transaction for [cn.wdidada.spring.testspringaop.service.impl.UserServiceImpl.getUser]
[TRACE] DataSourceTransactionManager - Triggering beforeCommit synchronization
[TRACE] DataSourceTransactionManager - Triggering beforeCompletion synchronization
[TRACE] TransactionSynchronizationManager - Removed value [org.mybatis.spring.SqlSessionHolder@389b0789] for key [org.apache.ibatis.session.defaults.DefaultSqlSessionFactory@35a3d49f] from thread [main]
[TRACE] TransactionSynchronizationManager - Retrieved value [org.springframework.jdbc.datasource.ConnectionHolder@7393222f] for key [HikariDataSource (HikariPool-1)] bound to thread [main]
[TRACE] TransactionSynchronizationManager - Removed value [org.springframework.jdbc.datasource.ConnectionHolder@7393222f] for key [HikariDataSource (HikariPool-1)] from thread [main]
[DEBUG] DataSourceUtils - Returning JDBC Connection to DataSource
[TRACE] DataSourceTransactionManager - Triggering afterCommit synchronization
[TRACE] TransactionSynchronizationManager - Clearing transaction synchronization
[TRACE] DataSourceTransactionManager - Triggering afterCompletion synchronization
[DEBUG] DefaultListableBeanFactory - Returning cached instance of singleton bean 'transactionManager'
[DEBUG] DataSourceTransactionManager - Creating new transaction with name [cn.wdidada.spring.testspringaop.service.impl.UserServiceImpl.insertUser]: PROPAGATION_REQUIRED,ISOLATION_DEFAULT; '',-java.lang.Exception
```
spring transtraction注解用法
https://www.cnblogs.com/yepei/p/4716112.html

在 Spring 中，`TransactionSynchronizationManager` 是一个用于管理事务同步器的类。它提供了一组静态方法，用于注册和管理与当前事务关联的事务同步器。在 Spring 的事务管理机制中，事务同步器用于在事务提交或回滚时执行一些额外的操作，例如清理资源、发送消息等。

`TransactionSynchronizationManager` 主要作用如下：

1. 注册同步器：`TransactionSynchronizationManager` 可以注册事务同步器，以便在事务提交或回滚时执行一些额外的操作。开发者可以通过 `TransactionSynchronizationManager.registerSynchronization()` 方法注册同步器。
2. 获取同步器状态：`TransactionSynchronizationManager` 可以获取当前事务中所有同步器的状态，并提供了一些查询同步器的方法。例如，可以通过 `TransactionSynchronizationManager.isSynchronizationActive()` 方法判断当前是否有事务同步器处于活动状态。
3. 提供同步器列表：`TransactionSynchronizationManager` 可以提供当前事务中所有同步器的列表，并提供了一些查询同步器列表的方法。例如，可以通过 `TransactionSynchronizationManager.getSynchronizations()` 方法获取当前事务中所有的同步器列表。

使用 `TransactionSynchronizationManager` 可以非常方便地管理事务同步器，实现在事务提交或回滚时执行一些额外的操作。示例代码如下：

```java
@Service
public class UserServiceImpl implements UserService {
    @Autowired
    private UserDao userDao;

    @Transactional
    public void addUser(User user) {
        userDao.addUser(user);
        TransactionSynchronizationManager.registerSynchronization(new TransactionSynchronizationAdapter() {
            @Override
            public void afterCommit() {
                sendEmail(user.getEmail());
            }
        });
    }

    private void sendEmail(String email) {
        // 发送邮件
    }
}
```

在上面的示例中，`addUser()` 方法使用了 `@Transactional` 注解开启了一个事务，并在事务提交后注册了一个同步器。该同步器会在事务提交后执行 `sendEmail()` 方法，从而实现发送邮件的功能。

总之，`TransactionSynchronizationManager` 是一个用于管理事务同步器的类，它提供了一组静态方法，用于注册和管理与当前事务关联的事务同步器。通过使用 `TransactionSynchronizationManager`，开发者可以在事务提交或回滚时执行一些额外的操作，例如清理资源、发送消息等。



解析tx:annotation-driven元素
TxNamespaceHandler解析tx:annotation-driven元素，用于启用使用@Transactional注解的事务管理。tx:annotation-driven元素会注册AnnotationTransactionAttributeSource、TransactionInterceptor和BeanNameAutoProxyCreator等BeanPostProcessor，以支持使用@Transactional注解的事务管理。



数据库事务
消息队列事务

ejb

javaee

TxNamespaceHandler解析tx:annotation-driven元素，用于启用使用@Transactional注解的事务管理。tx:annotation-driven元素会注册AnnotationTransactionAttributeSource、TransactionInterceptor和BeanNameAutoProxyCreator等BeanPostProcessor，以支持使用@Transactional注解的事务管理。

是的，您说得很对。

`TxNamespaceHandler` 是 Spring 框架提供的一个命名空间处理器，它可以解析 Spring 配置文件中的 `tx` 命名空间，并将其中的 `annotation-driven` 元素转换为 Spring 事务管理所需的相关组件，以支持使用 `@Transactional` 注解进行事务管理。

具体地说，`annotation-driven` 元素会注册 `AnnotationTransactionAttributeSource`、`TransactionInterceptor` 和 `BeanNameAutoProxyCreator` 等 Bean 后置处理器，以支持使用 `@Transactional` 注解的事务管理。其中，`AnnotationTransactionAttributeSource` 用于解析 `@Transactional` 注解中的事务属性，`TransactionInterceptor` 用于拦截带有 `@Transactional` 注解的方法，并根据事务属性来开启、提交或回滚事务，`BeanNameAutoProxyCreator` 用于自动为带有 `@Transactional` 注解的方法创建代理对象。

使用 `tx:annotation-driven` 元素可以非常方便地启用基于 `@Transactional` 注解的事务管理。示例代码如下：

```xml
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:tx="http://www.springframework.org/schema/tx"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
                           http://www.springframework.org/schema/beans/spring-beans.xsd
                           http://www.springframework.org/schema/tx
                           http://www.springframework.org/schema/tx/spring-tx.xsd">

    <tx:annotation-driven/>

    <bean id="transactionManager" class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
        <property name="dataSource" ref="dataSource"/>
    </bean>

    <bean id="userService" class="com.example.UserService">
        <property name="userDao" ref="userDao"/>
    </bean>

    <bean id="userDao" class="com.example.UserDao">
        <property name="dataSource" ref="dataSource"/>
    </bean>

    <bean id="dataSource" class="org.springframework.jdbc.datasource.DriverManagerDataSource">
        <property name="driverClassName" value="com.mysql.jdbc.Driver"/>
        <property name="url" value="jdbc:mysql://localhost:3306/test"/>
        <property name="username" value="root"/>
        <property name="password" value="root"/>
    </bean>

</beans>
```

在上面的示例中，`tx:annotation-driven` 元素启用了基于 `@Transactional` 注解的事务管理，`transactionManager` Bean 是事务管理器，`userService` Bean 和 `userDao` Bean 都带有 `@Transactional` 注解。当调用 `userService` 中带有 `@Transactional` 注解的方法时，Spring 会自动为其创建代理对象，并根据事务属性来管理事务。

总之，`TxNamespaceHandler` 可以解析 Spring 配置文件中的 `tx` 命名空间，将其中的 `annotation-driven` 元素转换为 Spring 事务管理所需的相关组件，以支持使用 `@Transactional` 注解进行事务管理。

### AnnotationTransactionAttributeSource

在 Spring 中，`AnnotationTransactionAttributeSource` 是用于解析 `@Transactional` 注解的事务属性的类。它可以将带有 `@Transactional` 注解的方法中的事务属性解析为事务的隔离级别、传播行为、只读属性等信息，从而在事务管理器中对事务进行更加精细的管理。

`AnnotationTransactionAttributeSource` 主要作用如下：

1. 解析 `@Transactional` 注解：`AnnotationTransactionAttributeSource` 可以解析 `@Transactional` 注解中的属性，包括事务的隔离级别、传播行为、只读属性等信息。

2. 提供事务属性元数据：`AnnotationTransactionAttributeSource` 可以将解析出的事务属性封装为 `TransactionAttribute` 对象，并提供事务属性元数据。

3. 支持多种事务管理器：`AnnotationTransactionAttributeSource` 支持多种事务管理器，包括 JDBC 事务、Hibernate 事务、JTA 事务等。开发者可以根据具体的应用场景选择合适的事务管理器。

使用 `AnnotationTransactionAttributeSource` 可以非常方便地解析 `@Transactional` 注解中的事务属性，并将其封装为 `TransactionAttribute` 对象。示例代码如下：

```java
@Service
public class UserServiceImpl implements UserService {
    @Autowired
    private UserDao userDao;

    @Transactional
    public void addUser(User user) {
        userDao.addUser(user);
    }

    @Transactional(propagation = Propagation.REQUIRED, isolation = Isolation.READ_COMMITTED)
    public User getUser(int userId) {
        return userDao.getUser(userId);
    }
}
```

在上面的代码中，`AnnotationTransactionAttributeSource` 可以解析 `addUser()` 和 `getUser()` 方法上的 `@Transactional` 注解中的事务属性，并封装为 `TransactionAttribute` 对象。这些信息会被用于在事务管理器中管理事务。

总之，`AnnotationTransactionAttributeSource` 是用于解析 `@Transactional` 注解的事务属性的类，它可以解析 `@Transactional` 注解中的事务属性，并封装为 `TransactionAttribute` 对象，从而在事务管理器中对事务进行更加精细的管理。

### TransactionInterceptor



### BeanNameAutoProxyCreator
在 Spring 中，`BeanNameAutoProxyCreator` 是一个 Bean 后置处理器，它可以自动为指定名称的 Bean 创建代理对象，并将其应用于所有符合指定规则的方法上。通常情况下，`BeanNameAutoProxyCreator` 用于实现基于方法拦截的 AOP 编程。

`BeanNameAutoProxyCreator` 主要作用如下：
1. 创建代理对象：`BeanNameAutoProxyCreator` 可以自动为指定名称的 Bean 创建代理对象，实现对 Bean 的方法拦截和增强。
2. 应用代理对象：`BeanNameAutoProxyCreator` 可以将创建的代理对象应用于所有符合指定规则的方法上，例如指定 Bean 中所有以 "get" 开头的方法。
3. 支持多种 AOP 拦截器：`BeanNameAutoProxyCreator` 支持多种 AOP 拦截器，例如 `TransactionInterceptor`、`SecurityInterceptor` 等。开发者可以根据需要选择合适的拦截器，来实现不同的方法拦截和增强。

使用 `BeanNameAutoProxyCreator` 可以非常方便地实现基于方法拦截的 AOP 编程。示例代码如下：

```xml
<bean id="proxyCreator" class="org.springframework.aop.framework.autoproxy.BeanNameAutoProxyCreator">
    <property name="beanNames">
        <list>
            <value>userService</value>
        </list>
    </property>
    <property name="interceptorNames">
        <list>
            <value>transactionInterceptor</value>
        </list>
    </property>
</bean>

<bean id="transactionInterceptor" class="org.springframework.transaction.interceptor.TransactionInterceptor">
    <property name="transactionManager" ref="transactionManager"/>
    <property name="transactionAttributes">
        <props>
            <prop key="add*">PROPAGATION_REQUIRED</prop>
            <prop key="get*">PROPAGATION_SUPPORTS,readOnly</prop>
        </props>
    </property>
</bean>

<bean id="transactionManager" class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
    <property name="dataSource" ref="dataSource"/>
</bean>

<bean id="userService" class="com.example.UserService">
    <property name="userDao" ref="userDao"/>
</bean>

<bean id="userDao" class="com.example.UserDao">
    <property name="dataSource" ref="dataSource"/>
</bean>

<bean id="dataSource" class="org.springframework.jdbc.datasource.DriverManagerDataSource">
    <property name="driverClassName" value="com.mysql.jdbc.Driver"/>
    <property name="url" value="jdbc:mysql://localhost:3306/test"/>
    <property name="username" value="root"/>
    <property name="password" value="root"/>
</bean>
```

在上面的示例中，`BeanNameAutoProxyCreator` 创建了一个代理对象，并将其应用于名为 `userService` 的 Bean 中以 "add" 开头的方法上。代理对象使用了 `transactionInterceptor` 拦截器，该拦截器实现了事务管理的能力。当调用 `userService` 中以 "add" 开头的方法时，代理对象会自动应用 `transactionInterceptor` 拦截器，从而实现事务管理的能力。

总之，`BeanNameAutoProxyCreator` 是一个 Bean 后置处理器，它可以自动为指定名称的 Bean 创建代理对象，并将其应用于所有符合指定规则的方法上，从而实现基于方法拦截的 AOP 编程。



在 Spring 中，以下是一些常用的事务管理器及其对应的技术：

1. `DataSourceTransactionManager`：该事务管理器适用于 JDBC 数据源事务管理，通过使用 JDBC API 来管理事务。

2. `HibernateTransactionManager`：该事务管理器适用于 Hibernate 的事务管理，可以管理 Hibernate SessionFactory 创建的所有 Session。

3. `JtaTransactionManager`：该事务管理器适用于 JTA 事务管理，可以与 JTA 事务管理器一起使用，以实现跨多个事务资源的事务管理。

4. `JpaTransactionManager`：该事务管理器适用于 JPA 的事务管理，可以管理 JPA EntityManagerFactory 创建的所有 EntityManager。

这些事务管理器都实现了 Spring 的 `PlatformTransactionManager` 接口，该接口定义了事务管理器的基本行为，例如开启事务、提交事务、回滚事务等。

开发者可以根据具体的应用场景选择合适的事务管理器。例如，如果应用程序使用的是 JDBC 数据源，则可以选择 `DataSourceTransactionManager`；如果应用程序使用的是 Hibernate 框架，则可以选择 `HibernateTransactionManager`；如果应用程序需要跨多个事务资源进行事务管理，则可以选择 `JtaTransactionManager` 等。

总之，不同的事务管理器适用于不同的技术和场景，开发者可以根据具体的应用场景选择合适的事务管理器来管理事务。


spring-tx，被@Transaction修饰的方法相互调用，传播属性最终是？

第一个方法的传播属性

因为事务是从外层方法开始的,每个嵌套的 transactional 方法继承外层方法的事务上下文。


spring是如何统计被@Transcational修饰的方法的，这些方法被调用，spring又是如何开启事务的


Spring是如何统计被@Transactional修饰的方法的:

1. 当Spring启动时,它会扫描所有被@Transactional注解的方法。

2. 对于每个方法,Spring会记录下对应的事务属性,如事务隔离级别、传播行为、回滚规则等。

3. Spring使用这些信息创建事务模版(TransactionTemplate),并缓存这些事务模版。

Spring是如何为这些方法开启事务的:

1. 当一个被@Transactional注解的方法被调用时,Spring会为这个方法创建一个事务执行对象(TransactionInterceptor)。

2. 这个事务执行对象会拦截方法调用,在方法执行前检查是否需要开始事务。

3. 如果需要开始事务,事务执行对象会使用之前缓存的事务模版来获取事务信息,并开始一个事务。

4. 方法执行完毕后,事务执行对象会根据事务属性提交或回滚事务。

5. 如果方法中抛出未检查的异常,事务执行对象也会回滚事务。

大致过程如下:
1. Spring启动时扫描并记录@Transactional方法信息,创建事务模版。
2. 当@Transactional方法被调用时,Spring创建一个TransactionInterceptor拦截器对象。
3. 拦截器在方法执行前根据事务属性开始一个事务。
4. 方法执行完毕后,拦截器根据事务属性提交或回滚事务。
5. 如果方法抛出异常,拦截器回滚事务。
通过这种方式,Spring才能控制投入和回滚事务,实现面向方法的事务管理。

总的来说,@Transactional注解给Spring提供了足够的信息来管理对应方法的事务。Spring利用这个信息创建拦截器,在方法调用时开始控制事务。










是的,被@Transactional修饰的类必须是注册到Spring IoC容器中的Bean。
原因是:
1. Spring通过扫描@Transactional注解来获取事务属性信息,生成TransactionTemplate等。这需要类是容器管理的Bean。
2. Spring使用AOP来实现事务,需要为@Transactional类创建TransactionInterceptor拦截器。这也需要类是容器管理的Bean。
3. 只有容器管理的Bean,Spring才能在正确时机给予事务性的处理。
所以总的来说,若一个类没有注册到Spring IoC容器中,即使它被@Transactional修饰,Spring也无法为它提供事务支持。
一个简单的示例:

```java
// 不是Spring Bean,没有事务支持
public class NotManagedClass {
    
    @Transactional
    public void method() {
       ...
    }
}

// 注册为Spring Bean,有事务支持    
@Component
public class ManagedClass {
    
    @Transactional
    public void method() {
       ...
    }
}
```

这样,ManagedClass中的@Transactional方法就能受到Spring的事务管理,而NotManagedClass方法则无法。
所以结论是,要想让@Transactional起作用,类必须首先是Spring IoC容器管理的Bean。
除此之外,事务代理也只对public方法起作用,私有方法不会被代理。





spring项目，如何查看整个项目中定义了哪些切点切面，哪些方法命中了切点？

您可以通过多个方式检查Spring项目中定义的切点、切面及命中切点的方法:

1. 查看配置文件:在Spring配置文件(如XML配置或注解配置)中,可以查看定义的切面及切点。

2. 日志输出:在Spring启动时,它会输出定义的切点和切面信息到日志中。

3. 使用AspectJ Weaver工具:可以使用AspectJ的ajc编译器或woven工具查看项目中的切点信息。

4. 使用AspectJ断点:可以在项目中设置AspectJ断点,在运行时打印命中的切点信息。

举个简单的例子:

```xml
<!-- 定义一个切点 --> 
<pointcut id="recordExecution" expression="execution(* com.myapp.service.*.*(..))"/>

<!-- 定义一个切面 -->
<aspectj-autoproxy/>
<aop:aspect ref="logAspect">
  
   <!-- 使用上面定义的切点 -->
   <aop:around pointcut-ref="recordExecution" method="log"/>
    
</aop:aspect>
```

Spring启动时会在日志中输出:

```
Defined cutpoint 'recordExecution' covering execution(com.myapp.service.*.*(..))
Advicing aspect 'logAspect' at cutpoint 'recordExecution'
```

使用AspectJ的woven工具或ajc编译器也可以查看项目中定义的切点详情。
通过设置AspectJ的切点断点,在程序运行时也可以查看到哪些方法命中了这个切点。
总的来说,您可以通过配置文件、日志、AspectJ工具等多种方式查看Spring项目中的AOP定义和使用情况。这有助于理解和调试Spring AOP。


TransactionInterceptor

org.springframework.transaction.interceptor.TransactionInterceptor spring-tx中的类





@Transactional这个注解，跟我自己自定义一个注解myCustomerAnnotation，然后用在方法上，一样吗？

@Transactional和自定义注解略有不同。
相同点:
- 二者都能被用在方法上,为了给方法加上额外的功能。
- 二者在方法声明上通过annotation都能被Spring扫描到。
不同点主要有两点:
1. 功能上的区别
@Transactional能为方法提供事务功能,可以指定事务属性,让方法在事务中运行。
而自定义注解只是一个标记,无法提供具体的功能。
2. 实现上的区别
@Transactional是Spring框架内置的注解,Spring知道如何处理它。
而自定义注解,Spring不知道如何处理,需要我们额外的配置。
例如:
- 自定义注解需要通过`@Import`导入自定义组件。
- 通过`@EnableAspectJAutoProxy`启用AOP。
- 定义一个切面,处理该自定义注解。
这样自定义注解才能起作用。
总的来说:
- @Transactional属于框架层面的注解,Spring默认就知道如何处理。
- 自定义注解需要我们额外的配置和实现,才能提供相应的功能。
而且@Transactional能很方便地为方法提供事务功能,而自定义注解不一定能提供和事务一样方便的功能。
所以二者很相似,但很不一样:
- @Transactional 是一个内置的框架注解,能很方便地为方法提供事务功能。
- 自定义注解需要额外的配置、实现,只是一个标记,无法提供具体的功能。
确保你理解了 @Transactional 是 Spring 框架如何为方法提供事务的一个关键手段。同时也理解自定义注解需要我们额外的实现。




spring是如何处理@Transactional注解的

Spring是通过AOP来处理@Transactional注解的。具体过程如下:
1. Spring启动时,会扫描所有被@Transactional注解的方法。
2. 对于每个方法,Spring会记录对应的事务属性,如传播行为、隔离级别等。
3. Spring会为这些方法创建TransactionInterceptor事务拦截器。
4. 当方法被调用时,TransactionInterceptor会拦截该方法调用。
5. TransactionInterceptor会在方法执行前根据事务属性启动一个事务。
6. 方法执行完成后,根据返回值和异常情况提交或回滚事务。
7. 如果方法抛出未检查异常,TransactionInterceptor也会回滚事务。
简单来说,流程是:
- Spring启动时扫描@Transactional方法,记录事务属性。
- 为这些方法创建TransactionInterceptor拦截器。
- 当方法执行时,TransactionInterceptor会拦截方法。
- TransactionInterceptor内部会在方法前后执行事务管理逻辑:
  - 方法前启动事务
  - 方法后根据情况提交或回滚事务
这就实现了面向方法的声明式事务管理。
主要涉及到的点有:
1. Spring启动时扫描@Transactional注解
2. 为这些方法创建TransactionInterceptor拦截器
3. 拦截器在方法执行前后管理事务
4. 提交或回滚依赖于执行情况

总的来说,@Transactional注解给了Spring足够的信息来管理对应的方法事务。Spring利用AOP的方式,在方法调用前后织入事务管理逻辑,从而提供声明式事务。




是不是有一个@Transactional修饰的方法，就会创建一个TrancactionIntercept类对象？
是的,如果一个方法使用了@Transactional注解,Spring会为这个方法创建一个TransactionInterceptor对象。
一个TransactionInterceptor对象会对应一个@Transactional方法,为这个方法提供事务支持。
举个例子:

```java
@Service
public class ServiceClass {

  @Transactional
  public void method1() { .. }

}
```

对于这个例子:
- method1()使用了@Transactional注解,证明需要事务支持。
- Spring会为method1()创建一个TransactionInterceptor1对象。
- TransactionInterceptor1对象会:

1) 在method1()执行前启动事务  
2) method1()执行后,根据情况提交或回滚事务
3) 如果method1()抛出异常,TransactionInterceptor1回滚事务
TransactionInterceptor1就像一个切面,能在method1()的执行前后织入事务管理逻辑。
所以总的来说:@Transactional方法和TransactionInterceptor对象是一一对应的关系。
一个@Transactional方法需要事务管理,Spring会为这个方法创建一个TransactionInterceptor对象。
这个TransactionInterceptor对象会在方法调用前后提供事务支持。
这也是Spring通过AOP来实现面向方法声明式事务的基本原理。
所以答案是:一个@Transactional方法对应的是一个TransactionInterceptor对象。
TransactionInterceptor为这个@Transactional方法提供事务支持。



