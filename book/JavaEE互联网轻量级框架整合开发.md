# Java EE互联网轻量级框架整合开发

轻量级Java EE企业应用实战(第5版)

https://book.douban.com/subject/27090950/

MyBatis
xml配置
MyBatis plugin
MyBatis Generator
MBG plugin

知乎读书上有电子版

## 第1部分 入门和技术基础
### 第1章 认识SSM框架和Redis 2
### 第2章 Java设计模式 15

第2部分 互联网持久框架——MyBatis
### 第3章 认识MyBatis核心组件 44
### 第4章 MyBatis配置 63
### 第5章 映射器 102
### 第6章 动态SQL 155
重点看
### 第7章 MyBatis的解析和运行原理 162

MapperMethod

MappedStatement

MapperRegister


AiasRegister
TypeHandlerRegister


四大组建
Execute
StatmengtHandler
ParamsHandler
ResultSetHandler 接口 实现类DefaultResultSetHandler



SqlSource 是提供 BoundSql 对象的地方，它是 MappedStatement 的一个属性。注意，它是一个接口，而不是一个实现类。对它而言有以下几个重要的实现类：DynamicSqlSource、ProviderSqlSource、RawSqlSource、StaticSqlSource。

MappedStatement 的作用是保存一个映射器节点（select|insert|delete|update）的内容。它是一个类，包括许多我们配置的 SQL、SQL 的 id、缓存信息、resultMap、parameterType、resultType、languageDriver 等重要内容。它还有一个重要的属性——sqlSource。MyBatis 通过读取它来获得某条 SQL 语句配置的所有信息。

MapperRegistry

`MapperRegistry`是MyBatis中的一个重要组件，它的作用是维护`Mapper`接口和对应的`MapperProxyFactory`对象之间的映射关系。在MyBatis框架中，每个`Mapper`接口都需要对应一个`MapperProxyFactory`对象，用于动态代理实现`Mapper`接口中的方法。
`MapperRegistry`类主要负责以下几个方面的工作：
1. 注册`Mapper`接口和对应的`MapperProxyFactory`对象
在MyBatis启动过程中，`MapperRegistry`会扫描所有的`Mapper`接口并创建对应的`MapperProxyFactory`对象，然后将它们注册到`MapperRegistry`中。这样，在后续的使用过程中，MyBatis就可以根据`Mapper`接口获取对应的`MapperProxyFactory`对象，从而动态代理实现`Mapper`接口中的方法。
2. 获取`Mapper`接口对应的`MapperProxyFactory`对象
在MyBatis中，每个`Mapper`接口都需要对应一个`MapperProxyFactory`对象，用于实现动态代理。`MapperRegistry`类提供了`getMapperProxyFactory`方法，用于根据`Mapper`接口获取对应的`MapperProxyFactory`对象。如果`MapperRegistry`中不存在该`Mapper`接口对应的`MapperProxyFactory`对象，则会抛出异常。
3. 获取所有已注册的`Mapper`接口
`MapperRegistry`类还提供了`getMappers`方法，用于获取所有已注册的`Mapper`接口。该方法返回一个`Set`集合，其中包含所有已注册的`Mapper`接口。
总的来说，`MapperRegistry`扮演着MyBatis框架中`Mapper`接口和`MapperProxyFactory`对象之间的桥梁角色，它的作用是维护这两者之间的映射关系，从而实现动态代理，并提供了一些方法，用于获取已注册的`Mapper`接口和对应的`MapperProxyFactory`对象。


`MapperProxyFactory`是MyBatis框架中的一个重要组件，它的作用是用于动态代理实现`Mapper`接口中的方法。在MyBatis中，每个`Mapper`接口都需要对应一个`MapperProxyFactory`对象，用于实现动态代理。
`MapperProxyFactory`类主要负责以下几个方面的工作：
1. 创建`Mapper`接口的代理对象
`MapperProxyFactory`类提供了`newInstance`方法，用于创建`Mapper`接口的代理对象。在创建代理对象时，会使用`MapperProxy`类对`Mapper`接口进行动态代理，从而实现对`Mapper`接口中方法的拦截和处理。
2. 获取`Mapper`接口的类型
`MapperProxyFactory`类还提供了`getMapperInterface`方法，用于获取该`MapperProxyFactory`对象对应的`Mapper`接口的类型。
3. 缓存`Mapper`接口的代理对象
`MapperProxyFactory`类还维护了一个`Map`对象，用于缓存已创建的`Mapper`接口的代理对象。这样，在后续的使用过程中，如果需要再次使用该`Mapper`接口的代理对象，就可以直接从缓存中获取，而无需重新创建。
总的来说，`MapperProxyFactory`扮演着MyBatis框架中动态代理的角色，它的作用是用于创建`Mapper`接口的代理对象，并缓存已创建的代理对象。`MapperProxyFactory`对象是`MapperRegistry`维护的一个重要组成部分，它们之间的映射关系由`MapperRegistry`负责维护。

实际上，SqlSession 是通过 Executor、StatementHandler、ParameterHandler 和 ResultSetHandler 完成数据库操作和结果返回的，在本书中我们把它们简称为四大对象 。


构建的真实对象是一个 RoutingStatementHandler 对象
RoutingStatementHandler 分为 3 种：SimpleStatementHandler、PreparedStatementHandler 和 CallableStatementHandler。它们对应 JDBC 的 Statement、PreparedStatement（预编译处理）和 CallableStatement（存储过程处理）。

XMLConfigBuilder 

plugin包下面的类
Interceptor
Plugin类继承了Invocation接口，动态代理
Invocation类

InterceptorChain

工具类 MetaObject


```java
package org.apache.ibatis.mapping;

public interface SqlSource {
  BoundSql getBoundSql(Object parameterObject);
}
```


实现类：org.apache.ibatis.scripting.xmltags.DynamicSqlSource
org.apache.ibatis.builder.annotation.ProviderSqlSource
org.apache.ibatis.scripting.defaults.RawSqlSource 调用 SqlSourceBuilder类将"#{xxx}“ 替换为占位符”?"，并绑定ParameterMapping，最后返回的RawSqlSource中持有一个由SqlSourceBuilder构建的SqlSource对象。




MyBatis初始化（二）之XMLConfigBuilder
https://blog.csdn.net/a1047003619/article/details/105620275



ObjectFactory是一个定义了创建新对象的接口，即如其名称得上是一个对象工厂。Mybatis每次在创建Mapper映射结果对象实例的时候，就会使用ObjectFactory来完成对象实例。其接口在Mybatis源代码中只有一个默认的实现，即DefaultObjectFactory。


ObjectFactory objectFactory = new DefaultObjectFactory();
List<String> list = objectFactory.create(List.class);
Robot robot = objectFactory.create(Robot.class);

https://blog.csdn.net/Jas000/article/details/126633311





### 第8章 插件 181

第3部分 Spring基础

### 第9章 Spring IoC的概念 208

### 第10章 装配Spring Bean 224
### 第11章 面向切面编程 267
### 第12章 Spring和数据库编程 307

SqlSessionTemplate



### 第13章 深入Spring数据库事务管理 330

13.7 @Transactional的自调用失效问题



自调用指的是在一个类中，某个方法直接调用该类中的另一个方法的情况。举个例子，假设有如下的Java类：

```java
@Service
public class UserService {
    
    @Autowired
    private UserDao userDao;
    
    @Transactional
    public void addUser(User user) {
        userDao.addUser(user);
        // 自调用
        updateCache(user);
    }
    
    @Transactional
    public void updateCache(User user) {
        // 更新缓存
    }
}
```

在上面的代码中，`addUser`方法会调用`userDao.addUser(user)`方法将用户信息插入到数据库中，然后通过`updateCache`方法更新缓存。由于`updateCache`方法也被标注了`@Transactional`注解，因此我们期望事务可以在这两个方法之间进行传递。但是，由于`updateCache`方法是在同一个类中被调用，它不会被Spring事务管理器拦截，因此事务也就无法生效，导致数据可能无法正确的更新到缓存中。

为了解决这个问题，我们可以通过将自调用方法的调用方式改为通过代理对象调用来解决，代码如下：

```java
@Service
public class UserService {
    
    @Autowired
    private UserDao userDao;
    
    @Autowired
    private UserService userServiceProxy;
    
    @Transactional
    public void addUser(User user) {
        userDao.addUser(user);
        // 通过代理对象调用自调用方法
        userServiceProxy.updateCache(user);
    }
    
    @Transactional
    public void updateCache(User user) {
        // 更新缓存
    }
}
```

在上面的代码中，我们新增了一个`userServiceProxy`属性，并在`addUser`方法中通过该代理对象来调用`updateCache`方法，从而使得该方法的事务注解可以被Spring事务管理器拦截，从而使得事务生效。



## 第4部分 Spring MVC框架
### 第14章 Spring MVC的初始化和流程 370

