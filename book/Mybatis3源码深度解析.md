# Mybatis3源码深度解析

https://github.com/edidada/mybatis-book

https://book.douban.com/subject/34836563/


https://download.oracle.com/otndocs/jcp/jdbc-4_2-mrel2-spec/index.html      


本书从MyBatis源码的角度分析Mapper绑定过程、SqlSession操作数据库原理、插件实现原理等，同时介绍一些MyBatis的高级用法，并挖掘MyBatis源码中使用的设计模式。

本书共13章，分为MyBatis 3源码篇和MyBatis Spring源码篇。第1~11章介绍MyBatis核心源码，从源码的角度分析MyBatis的实现原理，并介绍一些MyBatis的高级用法。MyBatis大多数情况下会与Spring整合使用，第12~13章介绍MyBatis Spring的实现原理，并分析MyBatis Spring模块的核心代码。

本书适合掌握了MyBatis的基本用法并希望了解MyBatis底层实现的Java开发人员、架构师以及对Java开源项目感兴趣的读者阅读。

## 第1篇 MyBatis 3源码
### 第1章 搭建MyBatis源码环境 3
1.1 MYBATIS 3简介 3
1.2 环境准备 4
1.3 获取MYBATIS源码 4
1.4 导入MYBATIS源码到IDE 6
1.5 HSQLDB数据库简介 9
1.6 本章小结 11
### 第2章 JDBC规范详解 13
2.1 JDBC API简介 13
2.1.1 建立数据源连接 14
2.1.2 执行SQL语句 15
2.1.3 处理SQL执行结果 16
2.1.4 使用JDBC操作数据库 16
2.2 JDBC API中的类与接口 17
2.2.1 java.sql包详解 17
2.2.2 javax.sql包详解 20
2.3 CONNECTION详解 24
2.3.1 JDBC驱动类型 24
2.3.2 java.sql.Driver接口 26
2.3.3 Java SPI机制简介 27
2.3.4 java.sql.DriverAction接口 29
2.3.5 java.sql.DriverManager类 29
2.3.6 javax.sql.DataSource接口 31
2.3.7 使用JNDI API增强应用的可移植性 32
2.3.8 关闭Connection对象 34
2.4 STATEMENT详解 35
2.4.1 java.sql.Statement接口 35
2.4.2 java.sql.PreparedStatement接口 39
2.4.3 java.sql.CallableStatement接口 43
2.4.4 获取自增长的键值 44
2.5 RESULTSET详解 45
2.5.1 ResultSet类型 45
2.5.2 ResultSet并行性 46
2.5.3 ResultSet可保持性 46
2.5.4 ResultSet属性设置 47
2.5.5 ResultSet游标移动 47
2.5.6 修改ResultSet对象 48
2.5.7 关闭ResultSet对象 50
2.6 DATABASEMETADATA详解 51
2.6.1 创建DatabaseMetaData对象 51
2.6.2 获取数据源的基本信息 51
2.6.3 获取数据源支持特性 53
2.6.4 获取数据源限制 53
2.6.5 获取SQL对象及属性 54
2.6.6 获取事务支持 54
2.7 JDBC事务 54
2.7.1 事务边界与自动提交 55
2.7.2 事务隔离级别 55
2.7.3 事务中的保存点 56
2.8 本章小结 57
### 第3章 MyBatis常用工具类 58
3.1 使用SQL类生成语句 58
3.2 使用SCRIPTRUNNER执行脚本 64
3.3 使用SQLRUNNER操作数据库 67
3.4 METAOBJECT详解 71
3.5 METACLASS详解 72
3.6 OBJECTFACTORY详解 73
3.7 PROXYFACTORY详解 74
3.8 本章小结 75
### 第4章 MyBatis核心组件介绍 76
4.1 使用MYBATIS操作数据库 76
4.2 MYBATIS核心组件 80
4.3 CONFIGURATION详解 82
4.4 EXECUTOR详解 88
4.5 MAPPEDSTATEMENT详解 90
4.6 STATEMENTHANDLER详解 92
4.7 TYPEHANDLER详解 94
4.8 PARAMETERHANDLER详解 97
4.9 RESULTSETHANDLER详解 98
4.10 本章小结 100
### 第5章 SqlSession的创建过程 101
5.1 XPATH方式解析XML文件 101
5.2 CONFIGURATION实例创建过程 104
5.3 SQLSESSION实例创建过程 108
5.4 本章小结 109
### 第6章 SqlSession执行Mapper过程 110
6.1 MAPPER接口的注册过程 110
6.2 MAPPEDSTATEMENT注册过程 114
6.3 MAPPER方法调用过程详解 119
6.4 SQLSESSION执行MAPPER过程 126
6.5 本章小结 130
### 第7章 MyBatis缓存 131
7.1 MYBATIS缓存的使用 131
7.2 MYBATIS缓存实现类 132
7.3 MYBATIS一级缓存实现原理 135
7.4 MYBATIS二级缓存实现原理 138
7.5 MYBATIS使用REDIS缓存 142
7.6 本章小结 145
### 第8章 MyBatis日志实现 146
8.1 JAVA日志体系 146
8.2 MYBATIS日志实现 149
8.3 本章小结 155
### 第9章 动态SQL实现原理 156
9.1 动态SQL的使用 156
9.2 SQLSOURCE与BOUNDSQL详解 159
9.3 LANGUAGEDRIVER详解 161
9.4 SQLNODE详解 164
9.5 动态SQL解析过程 169
9.6 从源码角度分析#{}和${}的区别 179
9.7 本章小结 182
### 第10章 MyBatis插件原理及应用 184
10.1 MYBATIS插件实现原理 184
10.2 自定义一个分页插件 193
10.3 自定义慢SQL统计插件 198
10.4 本章小结 200
### 第11章 MyBatis级联映射与懒加载 201
11.1 MYBATIS级联映射详解 201
11.1.1 准备工作 201
11.1.2 一对多关联映射 205
11.1.3 一对一关联映射 206
11.1.4 Discriminator详解 209
11.2 MYBATIS懒加载机制 210
11.3 MYBATIS级联映射实现原理 212
11.3.1 ResultMap详解 212
11.3.2 ResultMap解析过程 213
11.3.3 级联映射实现原理 218
11.4 懒加载实现原理 225
11.5 本章小结 230
## 第2篇 MyBatis Spring源码
### 第12章 MyBatis与Spring整合案例 233
12.1 准备工作 233
12.2 MYBATIS与SPRING整合 234
12.3 用户注册案例 236
12.4 本章小结 239
### 第13章 MyBatis Spring的实现原理 240
13.1 SPRING中的一些概念 240
13.2 SPRING容器启动过程 243
13.3 MAPPER动态代理对象注册过程 244
13.4 MYBATIS整合SPRING事务管理 248
13.5 本章小结 253