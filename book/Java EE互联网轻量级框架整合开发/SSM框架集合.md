# SSM框架集合

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



## Chap.4 
