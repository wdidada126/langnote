# SSM框架集合





[Java EE互联网轻量级框架整合开发](https://book.douban.com/subject/27090950/)



第1章 认识SSM框架和Redis



第2章 Java设计模式



## Chap. 3 认识MyBatis核心组件

- SqlSessionFactoryBuilder
- SqlSessionFactory
- SqlSession
- SQL Map映射器

### SqlSessionFactoryBuilder和SqlSessionFactory

Configure DefaultSqlSessionFactory（单线程），SqlSessionManager(多线程，调用了DefaultSqlSessionFactory)
创建SqlSessionFactory的方式有两种

- XML
- 使用代码

### SqlSession

在MyBatis中，SqlSession有两个实现类，分别是

- DefaultSqlSession
- SqlSessionManager

SqlSession的作用：

- 获取Mapper
- 发送SQL
- 控制数据库事务

### 映射器

映射器有一个接口和一个xml文件组成，可以配置一下内容：

- 描述映射规则
- 提供SQL语句，并可以配置SQL参数类型，返回类型，缓存刷新等信息
- 配置缓存
- 提供动态SQL

步骤：
定义pojo
实现接口
使用xml配置或者使用注解

发送sql的方式:
使用SqlSession发送
使用Mapper发送



## Chap.4 MyBatis配置

1



第5章 映射器



2



第6章 动态SQL



3



第8章 插件



9



第9章 Spring IoC的概念



10



第10章 装配Spring Bean



第11章 面向切面编程



第12章 Spring和数据库编程



第13章 深入Spring数据库事务管理



第14章 Spring MVC的初始化和流程



第15章 深入Spring MVC组件开发



第16章 Spring MVC高级应用



第17章 Redis概述



第18章 Redis数据结构常用命令



第19章 Redis的一些常用技术



第20章 Redis配置



第21章 Spring缓存机制和Redis的结合



第22章 高并发业务



