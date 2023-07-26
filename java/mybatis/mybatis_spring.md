# mybatis spring

https://github.com/edidada/testmybatisspring



https://mybatis.org/spring/



spring ioc中存的是MapperProxy代理类对象

mysql-connector-java

jdk
sun的包

不是Spring官方发布的

spring xml文件中配置的三个spring-mybatis包中的类
- org.apache.ibatis.datasource.pooled.PooledDataSource
- SqlSessionFactoryBean xml配置类
- MapperFactoryBean  一次性配置一个Mapper接口
- MapperScannerConfigurer 一次配置一个package下面多个Mapper接口
- SqlSessionTemplate 线程安全，包装了一个SqlSessionFactory来进行增删改查操作，事务的commit rollback操作 动态代理



SqlSessionTemplate调用链
```shell
	at org.mybatis.spring.MyBatisExceptionTranslator.translateExceptionIfPossible(MyBatisExceptionTranslator.java:79)
	at org.mybatis.spring.SqlSessionTemplate$SqlSessionInterceptor.invoke(SqlSessionTemplate.java:447)
	at com.sun.proxy.$Proxy14.selectOne(Unknown Source)
	at org.mybatis.spring.SqlSessionTemplate.selectOne(SqlSessionTemplate.java:167)
	at org.apache.ibatis.binding.MapperMethod.execute(MapperMethod.java:83)
	at org.apache.ibatis.binding.MapperProxy.invoke(MapperProxy.java:59)
	at com.sun.proxy.$Proxy15.getUser(Unknown Source)
	at cn.wdidada.spring.testspringaop.service.impl.UserServiceImpl.getUser(UserServiceImpl.java:23)
	at cn.wdidada.spring.testspringaop.service.impl.UserServiceImpl$$FastClassBySpringCGLIB$$50e16ea6.invoke(<generated>)
```


MyBatisExceptionTranslator是如何将MyBatis异常翻译为Spring的标准异常的

MyBatisExceptionTranslator主要用于翻译MyBatis的异常,将其转换为Spring框架识别的DataAccessExceptions。

它的主要作用是:

1. 提供异常转化器,将MyBatis的各种数据库异常转换为Spring的标准异常。

2. 可以对MyBatis的异常进行拦截,实现自己的异常处理逻辑。

3. 与Spring事务一起使用时,可以根据MyBatis的异常决定是否回滚事务。

具体来说,MyBatisExceptionTranslator实现了Spring 的TranslateException接口,定义了translateException() 方法:

```java
public class MyBatisExceptionTranslator implements TranslateException {

   public DataAccessException translateExceptionIfPossible(
      RuntimeException ex) {
     
         // 如果是MyBatisDataAccessException,转换为Spring 的DataAccessException返回
         if (ex.getCause() instanceof MyBatisDataAccessException) {
            //...
            return new MyBatisDataAccessException(...);  
         }
   
         // 其他可能的MyBatis异常        
         if (ex instanceof TooManyResultsException){
            //...
            return new IncorrectResultSizeDataAccessException(...);  
         }
        
      return null;  // 不是MyBatis异常,不转换      
   } 
}
```

然后再Spring配置中注入 MyBatisExceptionTranslator:

```xml
<bean class="xx.MyBatisExceptionTranslator" />
```

这样一旦MyBatis操作数据库时发生了异常,Spring框架就会调用MyBatisExceptionTranslator 的translateException()方法来转换为Spring标准的DataAccessException。

最终可以与Spring的事务一起使用。




```xml
    <!--3 会话工厂bean sqlSessionFactoryBean -->
    <bean id="sqlSessionFactory" class="org.mybatis.spring.SqlSessionFactoryBean">
        <!-- 数据源 -->
        <property name="dataSource" ref="dataSource"></property>
        <!-- 别名 -->
        <property name="typeAliasesPackage" value="cn.wdidada.test.testmybatisspring.domain"></property>
        <!-- sql映射文件路径 -->
        <property name="mapperLocations" value="classpath*:mapper/*Mapper.xml"></property>
    </bean>
    <!-- 配置MapperFactoryBean -->
    <bean id="userMapper" class="org.mybatis.spring.mapper.MapperFactoryBean">
        <property name="mapperInterface" value="cn.wdidada.test.testmybatisspring.in.UserMapper"/>
        <property name="sqlSessionFactory" ref="sqlSessionFactory"/>
    </bean>

    <bean id="userFeedBackMapper" class="org.mybatis.spring.mapper.MapperFactoryBean">
        <property name="mapperInterface" value="cn.wdidada.test.testmybatisspring.in.UserFeedBackMapper"/>
        <property name="sqlSessionFactory" ref="sqlSessionFactory"/>
    </bean>
```

```xml
    <!--3 会话工厂bean sqlSessionFactoryBean -->
    <bean id="sqlSessionFactory" class="org.mybatis.spring.SqlSessionFactoryBean">
        <!-- 数据源 -->
        <property name="dataSource" ref="dataSource"></property>
        <!-- 别名 -->
        <property name="typeAliasesPackage" value="cn.wdidada.test.testmybatisspring.domain"></property>
        <!-- sql映射文件路径 -->
        <property name="mapperLocations" value="classpath*:mapper/*Mapper.xml"></property>
    </bean>

    <!--4 自动扫描对象关系映射 -->
    <bean class="org.mybatis.spring.mapper.MapperScannerConfigurer">
        <property name="basePackage" value="cn.wdidada.test.testmybatisspring.in"></property>
    </bean>
```

PooledDataSource 
driver
数据库用户名和密码 
url jdbc连接

SqlSessionFactoryBean ds mybatis配置文件 
mapperLocations sql的xml文件
typeAliasesPackage 数据库对应的javabean
configLocation mybatis-config.xml mybatis自身xml配置文件

MapperScannerConfigurer
basePackage 配置Java 接口对应的类


org.mybatis.spring.SqlSessionTemplate
根据传入的SqlSessionFactory
封装了增删改查接口
SqlSessionTemplate.png


mybatis-spring中的类
- ms
- msc MapperScannerConfigurer
- ssfb

- org.mybatis.spring.SqlSessionFactoryBean
- org.mybatis.spring.mapper.MapperScannerConfigurer


MapperFactoryBean类的继承关系
DaoSupport (org.springframework.dao.support)
    SqlSessionDaoSupport (org.mybatis.spring.support)
        MapperFactoryBean (org.mybatis.spring.mapper)

### SqlSessionFactoryBean

SqlSessionFactoryBean 实现了 Spring 的 FactoryBean 接口。 FactoryBean<SqlSessionFactory>

### MapperScannerConfigurer

当发现要使用多个MapperFactoryBean的时候，一个一个定义肯定非常麻烦，于是mybatis-spring提供了MapperScannerConfigurer这个类，它将会查找类路径下的映射器并自动将它们创建成MapperFactoryBean。

MapperScannerConfigurer是spring和mybatis整合的mybatis-spring的jar包中提供的一个类。

<bean class="org.mybatis.spring.mapper.MapperScannerConfigurer">
	<property name="basePackage" value="org.mybatis.spring.sample.mapper" />
</bean>

- org.mybatis.spring.annotation.MapperScan
当使用Java进行配置Mybatis时可以使用@MapperScan注解进行对MyBatis的Mapper interfaces进行注册。
https://www.jianshu.com/p/976aa407bda4


SqlSessionFactoryBean向spring容器注入
DefaultSqlSessionFactory对象
### MapperFactoryBean<T>
Mybatis在与Spring集成的时候可以配置MapperFactoryBean来生成Mapper接口的代理。MapperFactoryBean的出现为了代替手工使用SqlSessionDaoSupport或SqlSessionTemplate编写数据访问对象(DAO)的代码，使用动态代理实现。
MapperFactoryBean是MyBatis-Spring框架中的一个特殊的FactoryBean，它用于创建MyBatis Mapper接口的代理实例。MapperFactoryBean可以将一个Mapper接口封装为一个Spring Bean，并对其进行配置和管理，使得我们可以像使用普通的Spring Bean一样使用Mapper接口。
MapperFactoryBean的作用可以总结为以下几点：
1、管理Mapper接口
MapperFactoryBean可以将Mapper接口封装为一个Spring Bean，并对其进行配置和管理。我们可以通过Spring配置文件配置MapperFactoryBean来创建Mapper接口的代理实例，并将其注入到其他Spring Bean中。
提供灵活的Mapper代理配置
MapperFactoryBean提供了一些灵活的Mapper代理配置选项，例如Mapper接口的类对象、SqlSessionFactory实例、是否启用缓存等。这些配置选项可以通过Spring配置文件进行配置，使得Mapper代理的创建和管理更加灵活。
支持MyBatis-Spring的事务管理
MapperFactoryBean支持MyBatis-Spring框架的事务管理功能。我们可以将Mapper接口注入到事务管理器中，使得Mapper接口中的所有SQL操作都能够参与到Spring事务管理中。
提供MyBatis Mapper接口与DAO的转换
MapperFactoryBean提供了MyBatis Mapper接口与DAO的转换功能。我们可以将Mapper接口注入到DAO中，并在DAO中调用Mapper接口中的方法，从而实现对数据库的访问。
总之，MapperFactoryBean是MyBatis-Spring框架中的一个重要组件，它可以将Mapper接口封装为一个Spring Bean，并对其进行配置和管理，使得我们可以更加方便地使用Mapper接口。同时，MapperFactoryBean还提供了一些灵活的Mapper代理配置选项和支持Spring事务管理的功能，使得Mapper接口的使用更加灵活和可靠。



### MapperScannerConfigurer 

MapperScannerConfigurer public void postProcessBeanDefinitionRegistry(BeanDefinitionRegistry registry) 方法调用	ClassPathMapperScanner#scan()方法



MapperScannerConfigurer是MyBatis-Spring框架中的一个特殊的Bean后置处理器，它用于扫描指定的包，自动注册MyBatis的Mapper接口，并将其注入到Spring容器中。MapperScannerConfigurer可以自动扫描指定包下的所有Mapper接口，并将其创建为Spring Bean，使得我们可以在其他Spring Bean中直接使用Mapper接口。
MapperScannerConfigurer的作用可以总结为以下几点：
扫描指定包下的Mapper接口
MapperScannerConfigurer可以扫描指定包下的所有Mapper接口，并将其注入到Spring容器中。我们可以通过配置MapperScannerConfigurer的basePackage属性来指定要扫描的包路径。
自动注册Mapper接口
MapperScannerConfigurer可以将扫描到的Mapper接口自动注册为Spring Bean。在Spring容器启动时，MapperScannerConfigurer会自动扫描指定包下的所有Mapper接口，并将其创建为Spring Bean。
提供灵活的Mapper接口配置
MapperScannerConfigurer提供了一些灵活的Mapper接口配置选项，例如Mapper接口的父接口、Mapper接口的实现类等。这些配置选项可以通过Spring配置文件进行配置，使得Mapper接口的创建和管理更加灵活。
支持MyBatis-Spring的事务管理
MapperScannerConfigurer支持MyBatis-Spring框架的事务管理功能。我们可以将Mapper接口注入到事务管理器中，使得Mapper接口中的所有SQL操作都能够参与到Spring事务管理中。
总之，MapperScannerConfigurer是MyBatis-Spring框架中的一个重要组件，它可以自动扫描指定包下的所有Mapper接口，并将其创建为Spring Bean，使得我们可以在其他Spring Bean中直接使用Mapper接口。同时，MapperScannerConfigurer还提供了一些灵活的Mapper接口配置选项和支持Spring事务管理的功能，使得Mapper接口的使用更加灵活和可靠。

msc这个类，有个属性是basePackage
fb
mfb


msc这个类实现了BeanDefinitionRegistryPostProcessor接口
实现	void postProcessBeanDefinitionRegistry(BeanDefinitionRegistry registry) throws BeansException;

BeanDefinitionRegistryPostProcessor作用
BeanDefinitionRegistryPostProcessor是Spring框架提供的一个扩展点，可以在Spring容器加载BeanDefinition时对BeanDefinition进行修改或添加。它的作用是在BeanFactory标准初始化之后，在BeanDefinition加载完成之后、Bean实例化之前，对BeanDefinition进行进一步的处理和扩展。
具体来说，BeanDefinitionRegistryPostProcessor接口提供了一个方法postProcessBeanDefinitionRegistry，它的作用是在BeanDefinition加载完成之后，对BeanDefinitionRegistry进行进一步的处理和修改。在这个方法中，可以动态地注册新的BeanDefinition、修改已有的BeanDefinition，甚至可以删除不需要的BeanDefinition。此外，该扩展点还提供了另一个方法postProcessBeanFactory，用于在BeanFactory标准初始化之后、Bean实例化之前，对已经存在的BeanDefinition进行进一步的处理和修改。
通过实现BeanDefinitionRegistryPostProcessor接口，可以在Spring容器加载BeanDefinition时对BeanDefinition进行扩展和处理，从而实现一些自定义功能，例如：
动态注册BeanDefinition
可以在postProcessBeanDefinitionRegistry方法中动态地注册新的BeanDefinition，例如根据一些条件动态地创建和注册新的Bean。
修改已有的BeanDefinition
可以在postProcessBeanDefinitionRegistry方法中修改已有的BeanDefinition，例如修改Bean的作用域、属性等。
删除不需要的BeanDefinition
可以在postProcessBeanDefinitionRegistry方法中删除不需要的BeanDefinition，例如删除某些测试用例的BeanDefinition，避免它们被不必要地创建和加载。
需要注意的是，BeanDefinitionRegistryPostProcessor是在BeanFactory标准初始化之后、Bean实例化之前执行的，因此它能够修改BeanDefinition，但不能影响Bean实例化过程。如果需要在Bean实例化之后对Bean进行进一步的处理和修改，可以使用BeanPostProcessor接口。


ClassPathMapperScanner

ClassPathMapperScanner作用
ClassPathMapperScanner是Spring框架提供的一个类，用于扫描指定包下的所有类，并注册成为Spring的Bean。它的作用是自动扫描指定包下的所有类，并将符合条件的类自动注册成为Spring的Bean，方便进行依赖注入和使用。
具体来说，ClassPathMapperScanner会扫描指定包下的所有类，并使用Spring提供的ClassPathBeanDefinitionScanner来解析这些类，并将符合条件的类自动注册成为Spring的Bean，其中符合条件的类必须满足以下条件：
类必须是非抽象类和非接口。
类的作用域必须是public。
类必须有无参构造函数。
类必须标注了指定的注解（例如@Controller、@Service等）。
默认情况下，ClassPathMapperScanner会自动扫描指定包下所有的类，并将它们注册成为Spring的Bean。如果需要限制扫描的类的范围，可以使用setAnnotationClass、setIncludeFilters等方法来指定需要扫描的注解和过滤条件。
使用ClassPathMapperScanner可以方便地实现自动注册Bean的功能，避免手动编写大量的配置代码，提高了开发效率。但也需要注意，自动注册Bean可能会导致不必要的Bean被创建和加载，因此需要根据实际需求进行配置和调整。

spring-beans类ClassPathMapperScanner



MapperFactoryBean和SqlSessionFactoryBean都是Spring框架中用于整合MyBatis框架的类，但它们的作用和使用方式有所不同。都是FactoryBean接口的子类
1. MapperFactoryBean
MapperFactoryBean是一个FactoryBean，它的作用是将指定的MyBatis Mapper接口（例如DAO接口）注册为Spring的Bean，从而可以在Spring中使用依赖注入等功能。MapperFactoryBean需要配置一个SqlSessionTemplate或SqlSessionFactory作为数据源，以便在调用Mapper方法时获取必要的数据库连接和事务支持。
使用MapperFactoryBean的方式是在Spring的配置文件中配置一个MapperFactoryBean实例，并指定该实例的Mapper接口和数据源（SqlSessionTemplate或SqlSessionFactory），Spring容器会根据这些配置自动创建Mapper实例，并将其注册为Spring的Bean。
public class MapperFactoryBean<T> extends SqlSessionDaoSupport implements FactoryBean<T> {
泛型
2. SqlSessionFactoryBean
SqlSessionFactoryBean是一个FactoryBean，它的作用是创建MyBatis的SqlSessionFactory实例，用于管理MyBatis的SqlSession对象。SqlSessionFactoryBean需要配置一个数据源和MyBatis的配置文件，以便在创建SqlSessionFactory时进行配置。
使用SqlSessionFactoryBean的方式是在Spring的配置文件中配置一个SqlSessionFactoryBean实例，并指定该实例的数据源和MyBatis的配置文件，Spring容器会根据这些配置自动创建SqlSessionFactory实例，并将其注册为Spring的Bean。

总的来说，MapperFactoryBean和SqlSessionFactoryBean都是用于整合MyBatis框架的类，但MapperFactoryBean主要用于将MyBatis的Mapper接口注册为Spring的Bean，方便进行依赖注入等操作，
而SqlSessionFactoryBean主要用于创建MyBatis的SqlSessionFactory实例，管理MyBatis的SqlSession对象。


org.mybatis.spring.mapper.ClassPathMapperScanner类用到MapperFactoryBean

public class ClassPathMapperScanner extends ClassPathBeanDefinitionScanner

org.mybatis.spring.mapper.ClassPathMapperScanner#doScan

public Set<BeanDefinitionHolder> doScan(String... basePackages)

### 日志

	protected final Log logger = LogFactory.getLog(getClass());

org.apache.commons.logging.LogFactory

jcl



MyBatis-Spring 集成了 MyBatis 和 Spring 框架,
这里作为 Spring 框架的一部分提供了 MyBatis-Spring 的 API文档。
https://mybatis.org/spring/apidocs/index.html

两者的文档内容基本一致,主要类和接口包括:

- SqlSessionFactoryBean:构建SqlSessionFactory
- SqlSessionTemplate:封装了SqlSession的线程安全类
- MapperFactoryBean:构建Mapper代理
- MapperScannerConfigurer:扫描和注册Mapper
- plus一些辅助类如SqlSessionDaoSupport等
这些文档详细记录了组件的用法和配置方式,非常有助于使用MyBatis-Spring集成。



### 源代码核心类

ClassPathMapperScanner  扫描包，生成beanDefination 
SqlSessionTemplate
MapperFactoryBean
SqlSessionFactoryBean





# 分包详解


## org.mybatis.logging
| org.mybatis.logging | 类型 | 英文解析                                                     | 解释 |
| ------------------- | ---- | ------------------------------------------------------------ | ---- |
| Logger              |      | Wrapper of Log, allow log with lambda expressions.           |      |
| LoggerFactory       |      | LoggerFactory is a wrapper around LogFactory to support Logger. |      |
|                     |      |                                                              |      |



## org.mybatis.spring 

| org.mybatis.spring                       | 类型 | 英文描述                                                     | 解释                                                         |
| ---------------------------------------- | ---- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| MyBatisExceptionTranslator               |      | Default exception translator.                                | org.springframework.dao.support.PersistenceExceptionTranslator 接口实现类  有SQLExceptionTranslator接口属性  SqlSessionTemplate中调用 |
| MyBatisSystemException                   |      | MyBatis specific subclass of UncategorizedDataAccessException, for MyBatis system errors that do not match any concrete org.springframework.dao exceptions. |                                                              |
| SqlSessionFactoryBean                    |      | FactoryBean that creates a MyBatis SqlSessionFactory.        | FactoryBean<SqlSessionFactory>      xml 文件中配置了这个类 上面有很多例子 |
| SqlSessionHolder                         |      | Used to keep current SqlSession in TransactionSynchronizationManager. | org.springframework.transaction.support.ResourceHolderSupport  子类 |
| SqlSessionTemplate                       |      | Thread safe, Spring managed, SqlSession that works with Spring transaction management to ensure that the actual SqlSession used is the one associated with the current Spring transaction. | 模板类 select insert update delete                           |
| SqlSessionTemplate.SqlSessionInterceptor |      |                                                              | InvocationHandler子类                                        |
| SqlSessionUtils                          |      | Handles MyBatis SqlSession life cycle.                       |                                                              |



`SqlSessionTemplate` 是 MyBatis-Spring 框架中的一个核心类，它是一个线程安全的 MyBatis 的核心类 `SqlSession` 的实现类。通过使用 `SqlSessionTemplate`，我们可以方便地在 Spring 中使用 MyBatis 进行数据库操作，并且不需要手动管理 `SqlSession` 的生命周期。

以下是一个使用 `SqlSessionTemplate` 的例子：

```java
@Repository
public class UserDaoImpl implements UserDao {

    private static final String NAMESPACE = "com.example.mapper.UserMapper";

    @Autowired
    private SqlSessionTemplate sqlSessionTemplate;

    @Override
    public List<User> findAllUsers() {
        return sqlSessionTemplate.selectList(NAMESPACE + ".findAllUsers");
    }

    @Override
    public User findUserById(Long id) {
        return sqlSessionTemplate.selectOne(NAMESPACE + ".findUserById", id);
    }

    @Override
    public void addUser(User user) {
        sqlSessionTemplate.insert(NAMESPACE + ".addUser", user);
    }

    @Override
    public void updateUser(User user) {
        sqlSessionTemplate.update(NAMESPACE + ".updateUser", user);
    }

    @Override
    public void deleteUser(Long id) {
        sqlSessionTemplate.delete(NAMESPACE + ".deleteUser", id);
    }
}
```

在上面的代码中，我们使用 `SqlSessionTemplate` 实现了一个 `UserDao` 接口的实现类。通过 `@Autowired` 注解将 `SqlSessionTemplate` 注入到 DAO 类中，然后就可以在 DAO 方法中使用 `SqlSessionTemplate` 提供的方法来进行数据库操作。例如，在 `findAllUsers()` 方法中，我们使用 `SqlSessionTemplate` 的 `selectList()` 方法来查询所有的用户信息。

需要注意的是，`SqlSessionTemplate` 是一个线程安全的类，因此可以在多线程环境下使用。另外，`SqlSessionTemplate` 在 Spring 的事务管理下会自动管理其生命周期，所以我们不需要手动关闭 `SqlSession`。

总之，`SqlSessionTemplate` 是 MyBatis-Spring 框架中的一个核心类，它是一个线程安全的 MyBatis 的核心类 `SqlSession` 的实现类。通过使用 `SqlSessionTemplate`，我们可以方便地在 Spring 中使用 MyBatis 进行数据库操作，并且不需要手动管理 `SqlSession` 的生命周期。

[使用SqlSessionTemplate实现数据库的操作 - 夏末、初秋 - 博客园 (cnblogs.com)](https://www.cnblogs.com/xuerong/p/5000456.html)







### org.mybatis.spring.annotation

| org.mybatis.spring.annotation | 类型       |                                                              | 解释                                                        |
| ----------------------------- | ---------- | ------------------------------------------------------------ | ----------------------------------------------------------- |
| MapperScan                    | @interface | Use this annotation to register MyBatis mapper interfaces when using Java Config. |                                                             |
| MapperScannerRegistrar        |            | A ImportBeanDefinitionRegistrar to allow annotation configuration of MyBatis mapper scanning. | ImportBeanDefinitionRegistrar ResourceLoaderAware接口实现类 |
| MapperScans                   |            | The Container annotation that aggregates several MapperScan annotations. |                                                             |





## org.mybatis.spring.batch

| org.mybatis.spring.batch   | 类型 | Description                                                  | 解释 |
| -------------------------- | ---- | ------------------------------------------------------------ | ---- |
| MyBatisBatchItemWriter<T>  |      | ItemWriter that uses the batching features from SqlSessionTemplate to execute a batch of statements for all items provided. |      |
| MyBatisCursorItemReader<T> |      |                                                              |      |
| MyBatisPagingItemReader<T> |      | org.springframework.batch.item.ItemReader for reading database records using MyBatis in a paging fashion. |      |



spring-batch-infrastructure 依赖类



### org.mybatis.spring.batch.build

| org.mybatis.spring.batch.build    | 类型 | Description                                | 解释 |
| --------------------------------- | ---- | ------------------------------------------ | ---- |
| MyBatisBatchItemWriterBuilder<T>  |      | A builder for the MyBatisBatchItemWriter.  |      |
| MyBatisCursorItemReaderBuilder<T> |      | A builder for the MyBatisCursorItemReader. |      |
| MyBatisPagingItemReaderBuilder<T> |      | A builder for the MyBatisPagingItemReader. |      |





## org.mybatis.spring.config

| org.mybatis.spring.config         | 类型 | Description                                                  | 解释                                                         |
| --------------------------------- | ---- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| MapperScannerBeanDefinitionParser |      | A {#code BeanDefinitionParser} that handles the element scan of the MyBatis. | NamespaceHandler中调用，BeanDefinitionParser接口实现类 BeanDefinition parse(Element element, ParserContext parserContext);   private static final String *ATTRIBUTE_BASE_PACKAGE* = "base-package";private static final String *ATTRIBUTE_ANNOTATION* = "annotation";private static final String *ATTRIBUTE_MARKER_INTERFACE* = "marker-interface";private static final String *ATTRIBUTE_NAME_GENERATOR* = "name-generator";private static final String *ATTRIBUTE_TEMPLATE_REF* = "template-ref"; private static final String *ATTRIBUTE_FACTORY_REF* = "factory-ref"; |
| NamespaceHandler                  |      | Namespace handler for the MyBatis namespace.                 | registerBeanDefinitionParser("scan", new MapperScannerBeanDefinitionParser());    <mybatis:scan base-package="com.example.mapper"/> |





`org.mybatis.spring.config.NamespaceHandler` 是 MyBatis-Spring 框架中的一个命名空间处理器，它用于解析 MyBatis-Spring 的自定义 XML 配置文件中的标签，并将其转换为相应的 Spring Bean。在 MyBatis-Spring 中使用该命名空间处理器可以简化配置文件的编写，并提高配置文件的可读性和可维护性。

使用 `NamespaceHandler` 通常需要两个步骤：

1. 配置 XML 命名空间

```xml
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:mybatis="http://mybatis.org/schema/mybatis-spring"
       xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd
       http://mybatis.org/schema/mybatis-spring http://mybatis.org/schema/mybatis-spring.xsd">

    <!-- 这里是 MyBatis-Spring 的配置 -->
    ...
</beans>
```

在上面的代码中，我们使用 `xmlns:mybatis` 声明了一个名为 `mybatis` 的 XML 命名空间，并将其指向 `http://mybatis.org/schema/mybatis-spring`。这个命名空间所对应的 XSD 文件定义了 MyBatis-Spring 的自定义标签和属性。

2. 在 XML 配置文件中使用 MyBatis-Spring 标签

```xml
<mybatis:scan base-package="com.example.mapper"/>
```

在上面的代码中，我们使用 `mybatis:scan` 标签来配置 Mapper 扫描器，将 Mapper 映射器的包路径指定为 `com.example.mapper`。这个标签会被 `NamespaceHandler` 解析，并转换为相应的 Spring Bean。

总之，`org.mybatis.spring.config.NamespaceHandler` 是 MyBatis-Spring 框架中的一个命名空间处理器，用于解析 MyBatis-Spring 的自定义 XML 配置文件中的标签，并将其转换为相应的 Spring Bean。使用 `NamespaceHandler` 可以简化配置文件的编写，并提高配置文件的可读性和可维护性。





以下是一个使用 MyBatis-Spring 的 XML 配置示例，包括数据源配置、Mapper 映射器配置以及事务管理器配置：

```xml
<!-- 配置数据源 -->
<bean id="dataSource" class="org.springframework.jdbc.datasource.DriverManagerDataSource">
    <property name="driverClassName" value="com.mysql.jdbc.Driver"/>
    <property name="url" value="jdbc:mysql://localhost:3306/test"/>
    <property name="username" value="root"/>
    <property name="password" value="password"/>
</bean>

<!-- 配置 SqlSessionFactory -->
<bean id="sqlSessionFactory" class="org.mybatis.spring.SqlSessionFactoryBean">
    <property name="dataSource" ref="dataSource"/>
    <property name="typeAliasesPackage" value="com.example.model"/>
    <property name="mapperLocations" value="classpath*:mapper/*.xml"/>
</bean>

<!-- 配置 Mapper 映射器 -->
<bean class="org.mybatis.spring.mapper.MapperScannerConfigurer">
    <property name="basePackage" value="com.example.mapper"/>
</bean>

<!-- 配置事务管理器 -->
<bean id="transactionManager" class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
    <property name="dataSource" ref="dataSource"/>
</bean>
```

在上面的代码中，我们首先配置了一个数据源，使用的是 MySQL 数据库。接下来，我们配置了一个 `SqlSessionFactory`，并设置了数据源、实体类的别名和 Mapper 映射器的路径。其中，`mapperLocations` 属性指定了 Mapper 映射器 XML 文件的位置，使用通配符 `*` 表示在 `mapper` 目录下的所有 XML 文件。

然后，我们使用 `MapperScannerConfigurer` 配置了 Mapper 扫描器，将 Mapper 映射器的包路径指定为 `com.example.mapper`。这样，MyBatis-Spring 就能够自动扫描并注册这些 Mapper 映射器。

最后，我们配置了一个事务管理器，使用的是 Spring 的 `DataSourceTransactionManager`，并将数据源设置为前面配置的数据源。

总之，这是一个 MyBatis-Spring 的 XML 配置示例，包括了数据源配置、Mapper 映射器配置以及事务管理器配置。在实际使用时，需要根据具体的需求进行相应的配置。






## org.mybatis.spring.mapper
| org.mybatis.spring.mapper | 类型 | Description                                                  | 解释                                                         |
| ------------------------- | ---- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| ClassPathMapperScanner    |      | A ClassPathBeanDefinitionScanner that registers Mappers by basePackage, annotationClass, or markerInterface. | 根据package扫描包                                            |
| MapperFactoryBean<T>      |      | BeanFactory that enables injection of MyBatis mapper interfaces. | MapperFactoryBean 有属性 private Class<T> mapperInterface; 就是mybatis的接口 |
| MapperScannerConfigurer   |      | BeanDefinitionRegistryPostProcessor that searches recursively starting from a base package for interfaces and registers them as MapperFactoryBean. | 核心类                                                       |



MapperScannerConfigurer上面有详细解读

## org.mybatis.spring.support

| org.mybatis.spring.support | 类型     | Description                                                  | 解释                     |
| -------------------------- | -------- | ------------------------------------------------------------ | ------------------------ |
| SqlSessionDaoSupport       | abstract | Convenient super class for MyBatis SqlSession data access objects | 子类MapperFactoryBean<T> |



## org.mybatis.spring.transaction 

| org.mybatis.spring.transaction  | 类型 | Description                                                  | 解释                                                         |
| ------------------------------- | ---- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| SpringManagedTransaction        |      | SpringManagedTransaction handles the lifecycle of a JDBC connection. | org.apache.ibatis.transaction.Transaction接口实现类          |
| SpringManagedTransactionFactory |      | Creates a SpringManagedTransaction.                          | TransactionFactory接口实现类，返回SpringManagedTransaction对象 |
