# jpa

## 库的功能 JPA则是ORM框架（对象关系映射框架）的统一接口标准

数据的存储

jpa使用jdbc的api？

- Hibernate
- eclipselink




实现 JPA 规范的库主要有以下几种：

1. Hibernate：Hibernate 是一个开源的 Java 持久化框架，它实现了 JPA 规范。Hibernate 可以将对象状态映射到关系数据库中，并提供了一系列的 API 来实现对数据的增删改查操作。Hibernate 有着丰富的特性和强大的功能，例如支持事务管理、支持乐观锁和悲观锁等。
2. EclipseLink：EclipseLink 是 Eclipse 开放源码项目的一部分，它是一个高性能的 Java 持久化框架，支持 JPA 规范和 JAXB。EclipseLink 提供了丰富的功能，例如支持多对一、一对多等关系映射、支持延迟加载、支持分布式事务等。
3. Spring Data JPA：Spring Data JPA 是 Spring 框架的一部分，它提供了一个更高层次的抽象层次，使得开发人员可以更加方便地操作数据库。Spring Data JPA 实现了 JPA 规范，并提供了许多常用的功能，例如支持分页查询、支持自定义查询等。
4. Apache OpenJPA：Apache OpenJPA 是 Apache 开放源码项目的一部分，它是一个高性能的 Java 持久化框架，支持 JPA 规范和 Java EE。Apache OpenJPA 具有可扩展性和灵活性，可以轻松地集成到其他 Java EE 应用中。

以上是常见的实现 JPA 规范的库，不同的库有着不同的特性和适用场景，开发人员可以根据实际需求选择合适的库。




JDBC和JPA都是用于与数据库交互的技术，但它们在许多方面都有所不同。首先，JDBC是数据库的统一接口标准，它是由各种数据库厂商提供类和接口组成的数据库驱动，为多种数据库提供统一访问。而JPA则是ORM框架（对象关系映射框架）的统一接口标准。

其次，JDBC更注重于直接与数据库进行交互，它提供了与数据库建立连接、发送操作数据库的语句等API。然而，JPA更注重于Java代码，它允许开发者使用面向对象的方式操作数据库，这使得代码更加直观和易于维护。尽管JPA实现的框架底层仍然使用JDBC与数据库进行交互，但通过JPA，开发者可以更方便地处理诸如实体映射、继承、关联等复杂关系。

最后，JPA提供了一种将Java对象映射到数据库表的方式，这使得开发者可以用面向对象的思维来处理数据。这种方式不仅提高了开发效率，也使代码更加清晰易懂。因此，即使在有了JDBC的情况下，JPA作为Java EE规范的一部分，仍然有其独特的价值和意义。

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

以下是 Maven 工程中导入 JPA 和 javax 相关依赖的示例：

```xml
<dependencies>
    <!-- JPA dependency -->
    <dependency>
        <groupId>javax.persistence</groupId>
        <artifactId>javax-persistence-api</artifactId>
        <version>2.2</version>
    </dependency>
    <!-- Hibernate JPA dependency -->
    <dependency>
        <groupId>org.hibernate</groupId>
        <artifactId>hibernate-core</artifactId>
        <version>5.4.31.Final</version>
    </dependency>
</dependencies>
```

请注意，上述坐标仅为示例，您需要将其替换为您需要的版本和组。

/Users/ibqo/Develop/git/gitee/spring-data-jpa

https://gitee.com/edidada/spring-data-jpa-examples

/Users/ibqo/Develop/git/gitee/pro_jpa2_code_maven

