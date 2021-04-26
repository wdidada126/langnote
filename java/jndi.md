# jndi

jndi 例子

testjdni

```
javax.naming.spi.ObjectFactory
```



https://blog.csdn.net/xiancaieeee/article/details/7881441

Tomcat是一种常见的Java EE容器，其他的还有JBoss,WebLogic，它们同时也实现了JNDI提供者规范

https://docs.oracle.com/javase/tutorial/jndi/overview/index.html

Java命名和目录接口（Java Naming and Directory Interface，缩写JNDI），是Java的一个目录服务应用程序界面（API），它提供一个目录系统，并将服务名称与对象关联起来，从而使得开发人员在开发过程中可以使用名称来访问对象。

例子
log4j2 xml格式的配置文件

<?xml version="1.0" encoding="UTF-8"?>
<Configuration status="error">
  <Appenders>
    <JDBC name="databaseAppender" tableName="dbo.application_log">
      <DataSource jndiName="java:/comp/env/jdbc/LoggingDataSource" />
      <Column name="eventDate" isEventTimestamp="true" />
      <Column name="level" pattern="%level" />
      <Column name="logger" pattern="%logger" />
      <Column name="message" pattern="%message" />
      <Column name="exception" pattern="%ex{full}" />
    </JDBC>
  </Appenders>
  <Loggers>
    <Root level="warn">
      <AppenderRef ref="databaseAppender"/>
    </Root>
  </Loggers>
</Configuration>


命名服务与目录服务 JNDI的目的就是对命名服务(Naming Service)与目录服务(Directory)中的资源进行查找或者管理，那么什么是命名服务,什么又是目录服务呢？ 命名服务的概念其实很好理解，在生活中也有很多的例子，最典型的就是DNS(Domain Naming Service)了。众所周知，DNS是用来对人类更便于记忆的域名和计算机更便于记忆的IP地址进行映射的。因此命名服务的核心就在于映射，讲一个值映射成另一个值。 至于目录服务呢，它其实是命名服务的一种自然扩展，两者之间的关键差别是目录服务中对象可以有属性，而命名服务中对象没有属性。举个简单的例子吧，我们手机中的电话簿就是一个典型的目录服务。它将一个电话号码映射成了拥有这个号码的人，但是人这个对象不仅仅会有姓名(尽管姓名最重要)，这也就是为什么电话簿中还可以增加这个人的家庭住址，公司，电子邮件，电话铃声等等。

https://blog.csdn.net/Jesministrator/article/details/78903293

JNDI中用了SPI


JPAAppender
As of Log4j 2.11.0, JPA support has moved from the existing module logj-core to the new module log4j-jpa


### jdni spi关系


概念JNDI（Java naming and directory interface）Java命名和目录接口。做什么的是一个应用程序设计的API,为开发人员提供查找和访问各种命名和目录服务的通用、统一的接口，类似JDBC构建在抽象层上。现在JNDI已经成J2EE的标准之一，所有的J2EE容器都必须提供一个JNDI服务。怎么做的JNDI主要有两部分组成：应用程序编程接口（API）和服务供应商接口(SPI)。应用程序编程接口提供了Java应用程序访问各种命名和目录服务的功能，服务供应商接口提供了任意一种服务的供应商使用的功能。所有实现API,SPI即完成了JNDI一个实例。代码示例：try{
Context cntxt = new InitialContext();
DataSource ds = (DataSource) cntxt.lookup("jdbc/dpt"); //API
}
catch(NamingException ne){
...
}上述代码意思是，通过JNDI这个J2EE标准，获取DataSource的java类。其中，lookup这个函数就是API。实现lookup函数就是SPI。注释J2EE容器指为J2EE应用程序组件提供运行时环境支持一个程序。分1）web容器，比如tomcat。2）EJB容器。EJB(EnterPrise Java Bean)企业Bean。分会话Bean、实体Bean、消息驱动Bean。
