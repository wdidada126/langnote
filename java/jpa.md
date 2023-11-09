# jpa


EclipseLink的Maven坐标如下：

```xml
<dependency>
    <groupId>org.eclipse.persistence</groupId>
    <artifactId>eclipselink</artifactId>
    <version>2.7.11</version>
</dependency>
```

注意，版本号可能会随着时间推移而发生变化，请根据实际情况选择合适的版本。




要在Java中使用JPA（Java Persistence API）自动创建表，需要在实体类上添加 `@Entity`注解，并使用 `persistence.xml`配置文件。以下是一个简单的示例：

1. 创建一个实体类，例如 `User.java`：

```java
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;

@Entity
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String name;
    private String email;

    // 构造方法、getter和setter方法省略
}
```

2. 在 `persistence.xml`配置文件中配置数据源和实体管理器工厂：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<persistence version="2.1" xmlns="http://xmlns.jcp.org/xml/ns/persistence" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/persistence http://xmlns.jcp.org/xml/ns/persistence/persistence_2_1.xsd">
    <persistence-unit name="myPU" transaction-type="RESOURCE_LOCAL">
        <provider>org.hibernate.jpa.HibernatePersistenceProvider</provider>
        <class>User</class>
        <properties>
            <property name="javax.persistence.jdbc.driver" value="com.mysql.jdbc.Driver"/>
            <property name="javax.persistence.jdbc.url" value="jdbc:mysql://localhost:3306/mydb?useSSL=false"/>
            <property name="javax.persistence.jdbc.user" value="username"/>
            <property name="javax.persistence.jdbc.password" value="password"/>
            <property name="hibernate.dialect" value="org.hibernate.dialect.MySQLDialect"/>
            <property name="hibernate.hbm2ddl.auto" value="update"/>
        </properties>
    </persistence-unit>
</persistence>
```

在这个例子中，我们使用了Hibernate作为JPA实现。`hibernate.hbm2ddl.auto`属性设置为 `update`，表示在启动应用程序时自动创建或更新数据库表。如果需要手动创建表，可以将此属性设置为 `create`。

JSR 220
https://www.oracle.com/technical-resources/articles/java/jpa.html
https://docs.oracle.com/javaee/5/tutorial/doc/?wp406143&PersistenceIntro.html#wp78460
是一套java ee api规范，只提供了定义，没有提供实现

hibernate实现了jpa

## books 书籍

Spring Data JPA：入门、实战与进阶

https://book.douban.com/subject/35659940/

Pro JPA2中文版

英文版 mac电脑已经下载了

中文版 mac电脑
http://www.java1234.com/a/javabook/javaweb/2015/0620/4446.html

轻量级Java EE企业应用实战（第5版） : Struts 2+Spring 5+Hibernate 5/JPA 2整合开发
https://book.douban.com/subject/30179599/

第6章 深入使用Hibernate与JPA

https://gitee.com/yetugeng/hrsystem

https://docs.oracle.com/javaee/5/tutorial/doc/bnbqw.html#bnbrk
