# mybatis spring

https://github.com/edidada/testmybatisspring

spring ioc中存的是MapperProxy代理类对象

mysql-connector-java

jdk
sun的包

不是Spring官方发布的

spring xml文件中配置的三个spring-mybatis包中的类
- org.apache.ibatis.datasource.pooled.PooledDataSource
- SqlSessionFactoryBean
- MapperFactoryBean  一次性配置一个Mapper接口
- MapperScannerConfigurer 一次配置一个package下面多个Mapper接口
- SqlSessionTemplate 线程安全，包装了一个SqlSessionFactory来进行增删改查操作，事务的commit rollback操作 动态代理




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
- msc
- ssfb

- org.mybatis.spring.SqlSessionFactoryBean
- org.mybatis.spring.mapper.MapperScannerConfigurer


MapperFactoryBean类的继承关系
DaoSupport (org.springframework.dao.support)
    SqlSessionDaoSupport (org.mybatis.spring.support)
        MapperFactoryBean (org.mybatis.spring.mapper)

### SqlSessionFactoryBean

SqlSessionFactoryBean 实现了 Spring 的 FactoryBean 接口。

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
### MapperFactoryBean
Mybatis在与Spring集成的时候可以配置MapperFactoryBean来生成Mapper接口的代理。MapperFactoryBean的出现为了代替手工使用SqlSessionDaoSupport或SqlSessionTemplate编写数据访问对象(DAO)的代码，使用动态代理实现。
MapperFactoryBean是MyBatis-Spring框架中的一个特殊的FactoryBean，它用于创建MyBatis Mapper接口的代理实例。MapperFactoryBean可以将一个Mapper接口封装为一个Spring Bean，并对其进行配置和管理，使得我们可以像使用普通的Spring Bean一样使用Mapper接口。
MapperFactoryBean的作用可以总结为以下几点：
管理Mapper接口
MapperFactoryBean可以将Mapper接口封装为一个Spring Bean，并对其进行配置和管理。我们可以通过Spring配置文件配置MapperFactoryBean来创建Mapper接口的代理实例，并将其注入到其他Spring Bean中。
提供灵活的Mapper代理配置
MapperFactoryBean提供了一些灵活的Mapper代理配置选项，例如Mapper接口的类对象、SqlSessionFactory实例、是否启用缓存等。这些配置选项可以通过Spring配置文件进行配置，使得Mapper代理的创建和管理更加灵活。
支持MyBatis-Spring的事务管理
MapperFactoryBean支持MyBatis-Spring框架的事务管理功能。我们可以将Mapper接口注入到事务管理器中，使得Mapper接口中的所有SQL操作都能够参与到Spring事务管理中。
提供MyBatis Mapper接口与DAO的转换
MapperFactoryBean提供了MyBatis Mapper接口与DAO的转换功能。我们可以将Mapper接口注入到DAO中，并在DAO中调用Mapper接口中的方法，从而实现对数据库的访问。
总之，MapperFactoryBean是MyBatis-Spring框架中的一个重要组件，它可以将Mapper接口封装为一个Spring Bean，并对其进行配置和管理，使得我们可以更加方便地使用Mapper接口。同时，MapperFactoryBean还提供了一些灵活的Mapper代理配置选项和支持Spring事务管理的功能，使得Mapper接口的使用更加灵活和可靠。


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
