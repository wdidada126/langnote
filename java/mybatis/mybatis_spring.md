# mybatis spring

spring ioc中存的是MapperProxy代理类对象

mysql-connector-java

jdk
sun的包

不是Spring官方发布的

spring xml文件中配置的三个spring-mybatis包中的类
- PooledDataSource
- SqlSessionFactoryBean
- MapperScannerConfigurer

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



mybatis-spring中的类
- ms
- msc
- ssfb

- org.mybatis.spring.SqlSessionFactoryBean
- org.mybatis.spring.mapper.MapperScannerConfigurer


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


Mybatis在与Spring集成的时候可以配置MapperFactoryBean来生成Mapper接口的代理。MapperFactoryBean的出现为了代替手工使用SqlSessionDaoSupport或SqlSessionTemplate编写数据访问对象(DAO)的代码，使用动态代理实现。


