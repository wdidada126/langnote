# spring_jdbc_template

JdbcTemplate是Spring为了简化JDBC操作而封装的一个类。它主要做了以下两件事:
1. 隐藏了原生JDBC API。用户不需要直接操作Connection、Statement等JDBC对象,而是使用JdbcTemplate提供的方法。
2. 实现了模板方法设计模式。它提供了一系列模板方法,如queryForObject()、update()等。这些模板方法内部完成了JDBC资源的获取、异常处理等重复性工作。
具体来说,JdbcTemplate主要封装了以下方面:
1. 连接池:JdbcTemplate通过DataSource获取JDBC连接,完成了对连接池的封装。用户只需要注入DataSource即可。
2. 事务管理:利用SqlSET uprising集成Spring事务管理功能。
3. 参数设置:提供了参数设置的方法,用户不需要直接操作PreparedStatement。
4. 结果集处理:提供方法来处理结果集,如queryForObject()、query()等。
5. 异常处理:内部统一处理JDBC异常,减少用户捕获异常的代码。
6. 释放资源:自动释放JDBC资源,用户无需手动关闭Statement、Connection。
通过以上这些方面,JdbcTemplate完全封装掉了对原生JDBC API的访问,而提供了一系列简单易用的方法来执行SQL操作。
总的来说,JdbcTemplate就是通过实现模板方法设计模式,隐藏JDBC API,为用户提供带模板的方法来访问数据库。从而简化了JDBC编码。



jdbctemplate hibernate mybatis对应的spring事务管理器分别是
- JdbcTemplate对应的事务管理器是DataSourceTransactionManager
- Hibernate对应的事务管理器是HibernateTransactionManager
- MyBatis对应的事务管理器是DataSourceTransactionManager

分别说明如下:
1. JdbcTemplate:

直接使用JDBC操作数据库,所以对应的事务管理器是DataSourceTransactionManager:

```xml
<bean id="transactionManager" 
    class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
    <constructor-arg ref="dataSource"/>
</bean>
```

DataSourceTransactionManager管理JDBC连接,实现事务。
2. Hibernate:
Hibernate是ORM框架,操作数据库使用Hibernate API,所以对应的事务管理器是:
```xml
<bean id="transactionManager" 
      class="org.springframework.orm.hibernate5.HibernateTransactionManager">
   <constructor-arg ref="sessionFactory"/>
</bean>
```
HibernateTransactionManager管理Hibernate SessionFactory,实现事务。
3. MyBatis:
MyBatis使用JDBC语句或存储过程操作数据库,所以对应的事务管理器是:
```xml
<bean id="transactionManager"
    class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
   <constructor-arg ref="dataSource" />
</bean>
</bean>  
```
仍然是DataSourceTransactionManager,和JdbcTemplate一致。
所以总的来说:
- 如果使用JDBC或者MyBatis,对应事务管理器是DataSourceTransactionManager
- 如果使用Hibernate,对应事务管理器是HibernateTransactionManager

希望以上信息能为您回答JdbcTemplate、Hibernate 和MyBatis对应的Spring事务管理器!如果仍有疑问,欢迎继续提问。

org.springframework.transaction.interceptor.TransactionAspectSupport#commitTransactionAfterReturning
org.springframework.transaction.interceptor.TransactionAspectSupport#completeTransactionAfterThrowing

TransactionInterceptor父类TransactionAspectSupport


DataSourceTransactionManager遇到异常回滚事务对应的代码在哪儿，详细说明
DataSourceTransactionManager这个事务管理器负责管理JDBC事务。

当方法出现异常时回滚事务,对应的代码主要在以下两个地方:


1. 在完成事务方法调用后, xxx() 方法中: 备注，这个方法不真实存在

```java
protected void xxx(int status) {
    // Check if transaction is actually active to avoid an exception.
    if (this.currentTransactionStatus == null) {
        throw new IllegalStateException("No transaction aspect-managed transaction available - " + 
        	"no transaction manager assigned?");
    }
    
    if (status == STATUS_COMMITTED) {
         // Commit transaction.
        if (this.transactionManager != null) {
            this.transactionManager.commit(this.currentTransactionStatus); 
        }   
    } 
    else {
         // Rollback transaction.
        if (this.transactionManager != null) {
            this.transactionManager.rollback(this.currentTransactionStatus);
        }
    }
}
```

这里会根据事务方法调用的状态,决定是否提交还是回滚事务:

- 如果status为STATUS_COMMITTED,则提交事务
- 否则,回滚事务  

2. 在rollback() 方法中实现具体的回滚逻辑:
org.springframework.transaction.support.AbstractTransactionStatus

AbstractTransactionStatus (org.springframework.transaction.support)
    SimpleTransactionStatus (org.springframework.transaction.support)
    DefaultTransactionStatus (org.springframework.transaction.support)


AbstractTransactionStatus类里面执行rollback()

```java
public void rollback(PlatformTransactionStatus status) {
   DefaultTransactionStatus defStatus = (DefaultTransactionStatus) status;
   // ...
   try {
       doRollback(defStatus);
   }
   catch (RollbackException ex) {
       // ...
   }    
}
```

doRollback() 方法中做了如下操作:

```java
 protected void doRollback(DefaultTransactionStatus status) {
    DataSourceTransactionObject txObject = getTransaction(status);
    try {
    	// 执行回滚操作
        txObject.rollback();           
    }
    catch (TransactionSystemException ex) {
      ...
    }     
  }
```

这就是 DataSourceTransactionManager 在检测到事务方法发生异常后,调用rollback() 方法回滚事务的过程。

org.springframework.transaction.support.AbstractPlatformTransactionManager#rollback
org.springframework.transaction.support.AbstractPlatformTransactionManager#commit


 AbstractTransactionStatus的rollback


 DataSourceTransactionManager实现抽象类AbstractPlatformTransactionManager
 AbstractPlatformTransactionManager实现接口PlatformTransactionManager

PlatformTransactionManager有commit()
rollback()
getTransaction()

在使用Spring的JdbcTemplate进行数据库操作时，可以通过使用`org.springframework.jdbc.core.JdbcTemplate`类的`update`方法进行insert操作。如果想要打印insert语句的入参，可以通过使用`PreparedStatementCreator`和`PreparedStatementSetter`来实现。

具体步骤如下：

1. 实现`PreparedStatementCreator`接口，用于创建PreparedStatement对象，并将参数设置到PreparedStatement对象中。在`createPreparedStatement`方法中，可以打印insert语句的入参。

```java
PreparedStatementCreator psc = new PreparedStatementCreator() {
    @Override
    public PreparedStatement createPreparedStatement(Connection conn) throws SQLException {
        String sql = "INSERT INTO user(name, age, gender) VALUES (?, ?, ?)";
        PreparedStatement ps = conn.prepareStatement(sql);
        ps.setString(1, user.getName());
        ps.setInt(2, user.getAge());
        ps.setString(3, user.getGender());
        System.out.println("Insert SQL: " + sql + ", Parameters: " + user.getName() + ", " + user.getAge() + ", " + user.getGender());
        return ps;
    }
};
```

2. 实现`PreparedStatementSetter`接口，用于设置PreparedStatement对象中的参数。在`setValues`方法中，可以打印PreparedStatement对象中的参数值。

```java
PreparedStatementSetter pss = new PreparedStatementSetter() {
    @Override
    public void setValues(PreparedStatement ps) throws SQLException {
        ps.setString(1, user.getName());
        ps.setInt(2, user.getAge());
        ps.setString(3, user.getGender());
        ResultSetMetaData metaData = ps.getMetaData();
        int count = metaData.getColumnCount();
        StringBuilder sb = new StringBuilder("Insert Parameters: ");
        for (int i = 1; i <= count; i++) {
            sb.append(metaData.getColumnLabel(i)).append("=").append(ps.getObject(i)).append(", ");
        }
        System.out.println(sb.substring(0, sb.length() - 2));
    }
};
```

3. 调用JdbcTemplate的`update`方法，并将`PreparedStatementCreator`和`PreparedStatementSetter`作为参数传入。

```java
int rows = jdbcTemplate.update(psc, pss);
```

通过实现`PreparedStatementCreator`和`PreparedStatementSetter`接口，可以在JdbcTemplate执行insert语句时打印出入参，方便调试和问题排查。



例子
- spring-jdbc-template
- 

https://gitee.com/edidada/spring-jdbc-template


org.springframework.jdbc.core.BeanPropertyRowMapper#newInstance(java.lang.Class<T>)

`BeanPropertyRowMapper` 是 Spring 框架提供的一个用于将 SQL 查询结果集映射到 Java 对象的 RowMapper 实现类。它可以将 ResultSet 中的每一行数据映射到一个 Java 对象，并使用该对象的属性来表示 ResultSet 中的每一列数据。
`BeanPropertyRowMapper` 主要的作用如下：
1. 简化 SQL 查询结果集到 Java 对象的映射操作。使用 `BeanPropertyRowMapper` 可以避免手动编写映射代码，从而减少开发时间和代码量。
2. 提高映射操作的可读性和可维护性。使用 `BeanPropertyRowMapper` 可以让代码更加易于理解和修改，并且可以利用 Java 对象的属性名来描述和约束查询结果集中的列名。
3. 支持自动类型转换和格式化。`BeanPropertyRowMapper` 可以自动将 ResultSet 中的数据转换为 Java 对象的属性类型，并且可以进行一些格式化操作，如日期格式化、字符串转换等。
使用 `BeanPropertyRowMapper` 时，需要指定要映射的 Java 类型，例如：

```java
public class User {
    private Long id;
    private String name;
    private Integer age;
    // ... 省略 getter 和 setter 方法
}

RowMapper<User> rowMapper = new BeanPropertyRowMapper<>(User.class);
List<User> userList = jdbcTemplate.query("SELECT * FROM user", rowMapper);
```

在上述代码中，我们创建了一个 `BeanPropertyRowMapper` 对象，并指定了要映射的 Java 类型为 `User.class`。然后，我们使用该 `BeanPropertyRowMapper` 对象将查询结果集 `ResultSet` 映射到 `List<User>` 对象中。
需要注意的是，`BeanPropertyRowMapper` 对象的映射规则是将 ResultSet 中的列名与 Java 对象的属性名进行匹配，如果列名与属性名不一致，需要使用别名或者指定列名别名映射。另外，`BeanPropertyRowMapper` 也不支持复杂类型的映射，如嵌套对象、集合等类型的映射。如果需要进行复杂类型的映射，需要使用其他的 RowMapper 实现类或者自定义映射逻辑。


NamedParameterJdbcTemplate

queryForList()
queryForRowSet


RowMapper
BeanPropertyRowMapper<T> implements RowMapper
SingleColumnRowMapper

JdbcTemplate.png


### JdbcTemplate类详解
构造函数
- 空
- 传入一个DataSource
JdbcTemplate(DataSource dataSource, boolean lazyInit) 

public void setDataSource(@Nullable DataSource dataSource) 

update
batchUpdate
execute
get
query

setXXX

数据库操作，增删改查

删除
update
`jdbcTemplate.update("DELETE FROM blog WHERE id=?", id);`



org.springframework.dao.EmptyResultDataAccessException: Incorrect result size: expected 1, actual 0

