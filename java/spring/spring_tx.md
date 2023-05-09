# spring tx


	
https://github.com/edidada/testspringaops


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