# jdbc



Java必备的 15 个框架，推荐看下。

要连接到数据库，客户端需要连接器驱动程序。在Java领域，Sql最常见的驱动程序是JDBC。问题是，这个驱动程序阻塞了。它在套接字级别阻塞。一个线程总会卡在那里，直到它返回一个响应。

毋庸置疑，驱动程序一直是实现完全无阻塞应用程序的瓶颈。幸运的是，在具有多个活动分叉的异步驱动程序上取得了进展（尽管是非官方的），其中包括：





- https://github.com/eclipse-vertx/vertx-sql-client
- https://github.com/jasync-sql/jasync-sql





[JDBC操作MySQL（3）—查询（普通、流式、游标）](https://www.jianshu.com/p/c7c5dbe63019)



CommonDataSource
DataSource (javax.sql)
    MysqlDataSource (com.mysql.jdbc.jdbc2.optional)
        MysqlConnectionPoolDataSource (com.mysql.jdbc.jdbc2.optional)
        FabricMySQLDataSource (com.mysql.fabric.jdbc)
        MysqlXADataSource (com.mysql.jdbc.jdbc2.optional)
    DriverDataSource (com.zaxxer.hikari.util)
    DelegatingDataSource (org.springframework.jdbc.datasource)
        TransactionAwareDataSourceProxy (org.springframework.jdbc.datasource)
        UserCredentialsDataSourceAdapter (org.springframework.jdbc.datasource)
        LazyConnectionDataSourceProxy (org.springframework.jdbc.datasource)
    AbstractDataSource (org.springframework.jdbc.datasource)
        AbstractDriverBasedDataSource (org.springframework.jdbc.datasource)
        AbstractRoutingDataSource (org.springframework.jdbc.datasource.lookup)
    PooledDataSource (org.apache.ibatis.datasource.pooled)
    HikariDataSource (com.zaxxer.hikari)
    SmartDataSource (org.springframework.jdbc.datasource)
        SingleConnectionDataSource (org.springframework.jdbc.datasource)
    UnpooledDataSource (org.apache.ibatis.datasource.unpooled)
    EmbeddedDatabase (org.springframework.jdbc.datasource.embedded)
        EmbeddedDataSourceProxy in EmbeddedDatabaseFactory (org.springframework.jdbc.datasource.embedded)
ConnectionPoolDataSource (javax.sql)
    MysqlConnectionPoolDataSource (com.mysql.jdbc.jdbc2.optional)
XADataSource (javax.sql)
    MysqlXADataSource (com.mysql.jdbc.jdbc2.optional)



### 获取Connection的两种方式
- DriverManager       Connection getConnection(String url,String user, String password)   java.sql.DriverManager
- DataSource        Connection getConnection()                                            javax.sql.DataSource

DriverManager是获取一个connection，用完就进行关闭，需要又重新建立连接；
Datasource获取多个connection并管理起来，作为数据库连接池；很多第三方连接池都通过实现该接口来做连接池；

https://blog.csdn.net/jinhaijing/article/details/84284847



github.com/edidada/testjdbc

[jdk sql相关源码可以参考](https://github.com/edidada/jdk7-source)

- Driver

- PrepareStatument
- CallStatument

- DataSource
- Connector
- Statument
- ResultSet

### DataSource

Connection getConnection()

DataSource -> Connection

### Connection

Statement createStatement()

### Statement

jdk源码中并没有DataSource的实现类，交给三方库实现

比如：com.zaxxer.hikari.util.DriverDataSource

针对不同的数据库(MySQL pg),jdk是如何封装的呢？

javax.sql.DataSource

jdbc是API
mysql-connector                com.mysql.fabric.jdbc.FabricMySQLDriver
pg---
是不同数据库厂商提供的

<<<<<<< HEAD




`?useUnicode=true&characterEncoding=utf-8&useSSL=false`





=======
>>>>>>> afe522da082020e5ece0b75c43067644b2edb768
