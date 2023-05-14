# spring_jdbc_template

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