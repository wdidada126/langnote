# JTA


atomikos

在上面JTA实现多数据源的事务管理，使用方式还是相对简单，通过两阶段的提交，可以同时管理多个数据源的事务。但是暴露出的问题也非常明显，就是比较严重的性能问题,由于同时操作多个数据源,如果其中一个数据源获取数据的时间过长,会导致整个请求都非常的长,事务时间太长,锁数据的时间就会太长，自然就会导致低性能和低吞吐量。

因此在实际开发过程中，对性能要求比较高的系统很少使用JTA组件做事务管理。作为一个轻量级的分布式事务解决方案，在小的系统中还是值得推荐尝试的。

最后作为Java下的API，原理和用法还是值得学习一下，开阔眼界和思路。

*JTA*，即Java Transaction API，*JTA*允许应用程序执行分布式事务处理——在两个或多个网络计算机资源上访问并且更新数据。JDBC驱动程序的*JTA*支持极大地增强了数据访问能力。



<dependency>
    <groupId>javax.transaction</groupId>
    <artifactId>jta</artifactId>
    <version>1.1</version>
</dependency>



![java_spring_tx](imgs/java_spring_tx.png)



https://blog.csdn.net/qingmuluoyang/article/details/82961801



https://blog.csdn.net/weixin_30409927/article/details/105438267





java.tranzaction.UserTransaction



javax.persistence.EntityManager
javax.persistence.EntityManagerFactory
javax.persistence.EntityTransaction
javax.persistence.Persistence



<dependency>
    <groupId>javax.persistence</groupId>
    <artifactId>javax.persistence-api</artifactId>
    <version>2.2</version>
</dependency>





<dependency>
    <groupId>javax.persistence</groupId>
    <artifactId>persistence-api</artifactId>
    <version>1.0.2</version>
</dependency>

Java Transaction API，简称JTA



由于JDBC无法实现分布式事务，而如今的分布式场景越来越多，所以，JTA事务就应运而生。



JTA和它的同胞Java事务服务(JTS；Java TransactionService)，为J2EE平台提供了分布式事务服务。不过JTA只是提供了一个接口，并没有提供具体的实现，而是由j2ee服务器提供商 根据JTS规范提供的，常见的JTA实现有以下几种：

- 1.J2EE容器所提供的JTA实现(JBoss)
- 2.独立的JTA实现:如JOTM，Atomikos.这些实现可以应用在那些不使用J2EE应用服务器的环境里用以提供分布事事务保证。如Tomcat,Jetty以及普通的java应用。



分布式事务（Distributed Transaction）包括事务管理器（Transaction Manager）和一个或多个支持 XA 协议的资源管理器 ( Resource Manager )。



如果，你在工作中没有遇到JDBC事务无法解决的场景，那么只能说你做的项目还都太小。拿电商网站来说，我们一般把一个电商网站横向拆分成商品模块、订单模块、购物车模块、消息模块、支付模块等。然后我们把不同的模块部署到不同的机器上，各个模块之间通过远程服务调用(RPC)等方式进行通信。以一个分布式的系统对外提供服务。



[分布式事务常用的解决方案及优缺点](https://blog.csdn.net/weixin_42719412/article/details/86012429)

#### jta

分布式事务常用的解决方案及优缺点
https://blog.csdn.net/weixin_42719412/article/details/86012429


https://github.com/javaee/jta-spec

[Java中的事务——JDBC事务和JTA事务](https://www.hollischuang.com/archives/1658)

[使用atomikos+jta解决分布式事务问题](https://blog.csdn.net/kisscatforever/article/details/79129055)

Atomikos TransactionsEssentials 是一个为Java平台提供增值服务的并且开源类事务管理器，以下是包括在这个开源版本中的一些功能：

为XA和非XA提供内置的JDBC适配器



```shell
<dependency>
    <groupId>javax.transaction</groupId>
    <artifactId>jta</artifactId>
	<version>1.1</version>
</dependency>
```

Atomikos TransactionsEssentials 是一个为Java平台提供增值服务的并且开源类事务管理器，以下是包括在这个开源版本中的一些功能：

    <dependency>
      <groupId>javax.transaction</groupId>
      <artifactId>jta</artifactId>
      <version>1.1</version>
    </dependency>

Atomikos TransactionsEssentials 是一个为Java平台提供增值服务的并且开源类事务管理器，以下是包括在这个开源版本中的一些功能：

- 全面崩溃 / 重启恢复
- 兼容标准的SUN公司JTA API
- 嵌套事务
- 为XA和非XA提供内置的JDBC适配器

Google Chubby的作者Mike Burrows说过， there is only one consensus protocol, and that’s Paxos” – all other approaches are just broken versions of Paxos. 意即世上只有一种一致性算法，
那就是Paxos
