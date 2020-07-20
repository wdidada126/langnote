# Java EE互联网轻量级框架整合开发

https://github.com/edidada/eeworkspace

### Chap. 1 认识SSM框架和Redis

1.1.1 Spring IoC简介
IoC是使用XML文件配置或者Java注解的方式来赋值对象
跟传统的

ObjectClass A = new ObjectClass();

1.1.2 Spring AOP

aspectj
java静态代理和动态代理


应用领域：数据库事务 日志

abatis
鹿砦/铁丝网

自动映射、动态SQL、级联、缓存、注解、代码和SQL分离等特性。

POJO(Plain Ordinary Java Object)

2.2 动态代理模式和责任链模式
JDK自带代理
继承InvocationHandler的invoke()方法

责任链模式
观察者模式
工厂模式
抽象工厂模式
建造者模式



### Chap.3 MyBatis


SqlSessionFactory ssf
SqlSession ss
SqlSessionFactoryBuilder ssfb


####### Chap.4

4章



####### Chap.7


Configure
Factory
Builder
BoudnleSQL

Mapper JDK动态代理


####### Chap.9
a
####### Chap.10


MyBatis-Spring项目，定义了类SqlSessionFactoryBean，实现了FactoryBean，ApplicationListener等接口，可以作为阅读Spring源码的参考资料。

SqlSessionTemplate
构造函数
弃用

MapperFactoryBean

MapperScannerConfigure

[Mybatis MapperScannerConfigurer 自动扫描 将Mapper接口生成代理注入到Spring](https://www.cnblogs.com/jpfss/p/7799806.html)


####### Chap.13


PlatformTransactionManager
TransactionTemplate

Spring中有很多事务管理器

Mybatis框架，用的最多的事务管理器是DataSourceTransactionManager (org.springframework.jdbc.datasource.DataSourceTransactionManager)

TransactionDefinition

DefaultTransactionDefinition

首先编程式事务允许自定义事务接口-TransactionDefinition， 它可以由 XML 或者注 解＠Transactional 进行配置，到了这里我们先谈谈＠Transactional 的配置项。

Transactional

事务定义类 TransactionDefinition
