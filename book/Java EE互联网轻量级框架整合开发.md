# Java EE互联网轻量级框架整合开发

轻量级Java EE企业应用实战(第5版)

https://book.douban.com/subject/27090950/


MyBatis
xml配置
MyBatis plugin
MyBatis Generator
MBG plugin

知乎读书上有电子版


第1部分 入门和技术基础
第1章 认识SSM框架和Redis 2
第2章 Java设计模式 15


第2部分 互联网持久框架——MyBatis
第3章 认识MyBatis核心组件 44
第4章 MyBatis配置 63
第5章 映射器 102
第6章 动态SQL 155
第7章 MyBatis的解析和运行原理 162
第8章 插件 181


第3部分 Spring基础
第9章 Spring IoC的概念 208
第10章 装配Spring Bean 224
第11章 面向切面编程 267
第12章 Spring和数据库编程 307
第13章 深入Spring数据库事务管理 330
第4部分 Spring MVC框架
第14章 Spring MVC的初始化和流程 370


### Chap. 7 


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


实际上，SqlSession 是通过 Executor、StatementHandler、ParameterHandler 和 ResultSetHandler 完成数据库操作和结果返回的，在本书中我们把它们简称为  四大对象  。


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
org.apache.ibatis.scripting.defaults.RawSqlSource   调用 SqlSourceBuilder类将"#{xxx}“ 替换为占位符”?"，并绑定ParameterMapping，最后返回的RawSqlSource中持有一个由SqlSourceBuilder构建的SqlSource对象。




MyBatis初始化（二）之XMLConfigBuilder
https://blog.csdn.net/a1047003619/article/details/105620275



ObjectFactory是一个定义了创建新对象的接口，即如其名称得上是一个对象工厂。Mybatis每次在创建Mapper映射结果对象实例的时候，就会使用ObjectFactory来完成对象实例。其接口在Mybatis源代码中只有一个默认的实现，即DefaultObjectFactory。


ObjectFactory objectFactory = new DefaultObjectFactory();
List<String> list = objectFactory.create(List.class);
Robot robot = objectFactory.create(Robot.class);

https://blog.csdn.net/Jas000/article/details/126633311
