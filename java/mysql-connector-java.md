# mysql-connector-java

很多时候忘记引入pom，会报错


### log
d

### 使用方式
Class.forName("com.mysql.jdbc.Driver");
DriverManager.getConnection();

DataSource.getConnection


### Connection池
d

### sql类


```java
	prepareStatement = connection.prepareStatement(sql);
	// 设置参数
	prepareStatement.setLong(1, 1l);
	// 执行查询
	rs = prepareStatement.executeQuery();
	Statement statement = connection.createStatement();
	CallableStatement callableStatement = connection.prepareCall("");
```


Connection

JDBC4Connection com.mysql.jdbc.JDBC4Connection

Statement
CallStatuemnt sp（存储过程
PrepareStatement
ResultSet



getString
getInteger



打印日志
java.sql.DriverManager#println


spi 代码

DriverManager static代码块里面的   java.sql.DriverManager#loadInitialDrivers
```java
    static {
        try {
            java.sql.DriverManager.registerDriver(new Driver());
        } catch (SQLException E) {
            throw new RuntimeException("Can't register driver!");
        }
    }
    static {
        loadInitialDrivers();
        println("JDBC DriverManager initialized");
    }
```



Class.forName("jdbc.Driver")

Driver.getconnection()
反射调用
JDBC4FabricMySQLConnectionProxy类的构造函数



java.lang.ref.ReferenceQueue


com.mysql.fabric.jdbc.FabricMySQLDriver#connect方法

AbandonedConnectionCleanupThread Class.forName()



```java
            Constructor<?> jdbc4proxy = Class.forName("com.mysql.fabric.jdbc.JDBC4FabricMySQLConnectionProxy")
                    .getConstructor(new Class[] { Properties.class });
            return (Connection) com.mysql.jdbc.Util.handleNewInstance(jdbc4proxy, new Object[] { parsedProps }, null);
```




r2dbc jdbc异步版本


```java
        MysqlDataSource dataSource = new MysqlDataSource();
        dataSource.setUser("root");
        String url = "jdbc:mysql://127.0.0.1:3306/stockmarket?useUnicode=true&characterEncoding=utf-8&useSSL=false";

        dataSource.setUrl(url);
        dataSource.setPassword("5%edidada");
        Connection connection = dataSource.getConnection();

```





