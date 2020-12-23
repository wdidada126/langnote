# javaee

`lusrmgr.msc`

查看windows系统用户





DAO 是 Data Access Object 的缩写，专门用于进行数据库访问的操作



DO BO VO是JavaEE的规范？


[java ee规范中文](https://blog.csdn.net/u012410733/article/details/72567195)

java ee包括servlet jdbc ejb ws等等

```

            <dependency>
                <groupId>javax</groupId>
                <artifactId>javaee-api</artifactId>
                <version>8.0</version>
                <scope>provided</scope>
            </dependency>

```

java ee 8
weblogic


java 8
https://www.oracle.com/technetwork/java/javase/8-whats-new-2157071.html

JavaEE主要技术
JavaEE 号称有十三种核心技术。它们分别是：JDBC、JNDI、EJB、RMI、Servlet、JSP、XML、JMS、Java IDL、JTS、JTA、JavaMail和JAF。
https://blog.csdn.net/Neuf_Soleil/article/details/80962686



Jakarta EE



狭义的 Java EE 是 Sun 公司为企业级应用推出的标准平台，用来开发B/S架构软件，可以说是一个框架，也可以说是一种规范。



广义的 Java EE 包含各种框架，其中最重要的就是 Spring 全家桶。Spring 诞生之初是为了改进 Java EE 开发的体验，后来逐渐成为了 Java Web 开发的实际标准。后面的文章里，会对 Spring 进行进一步的说明。





JavaEE 与 JavaSE 的区别与联系

JavaEE 是在 JavaSE 的基础上构建的，是对 JavaSE 的扩展，增加了一些更加便捷的应用框架。



企业级 JavaBean（Enterprise JavaBean, EJB）



JavaEE 拥有广泛市场的原因之一就是可以使用多种框架来使开发变得简单。对于框架的选择多种多样，目前比较常见的**框架组合**有 **SSH**和**SSM**。



JDBC  -> spring-jdbc

servlet ->srpingmvc sping-web-mvc





JNDI

Java 命名和目录接口（Java Naming and Directory Interface，JNDI），是 Java 的一个**目录服务应用程序界面**（API），它提供一个目录系统，并将服务名称与对象关联起来，从而使得开发人员在开发过程中可以使用名称来访问对象。



weblogic *WebLogic*是美国Oracle公司出品的一个application server，确切的说是一个基于JAVAEE架构的中间件，*WebLogic*是用于开发、集成、部署和管理大型分布式Web应用、网络应用和数据库应用的Java应用服务器。

websphere *WebSphere* 是 IBM 的软件平台 *WebSphere* Application Server








首先，将近五年前它被称为Java EE。首字母缩略词J2EE仍指5.0之前的较旧Java EE版本。

对于Glassfish，这是Oracle对Java EE的具体实现。 Java EE是一个抽象的API，每个人都可以自由实现。有几种可用的Java EE实现，或者是像Oracle Glassfish 3，JBoss AS 6等完整的实现，还是像Apache Tomcat 7，Eclipse Jetty 8这样的部分(仅JSP / Servlet)实现。Glassfish Web Profile也是其中的一部分实施。

如果您打算仅使用JSP / Servlet进行开发，那么Glassfish Web Profile就足够了。如果您打算在Netbeans IDE的帮助下进行开发，请选择与Netbeans捆绑销售的产品。但是，除了Netbeans，您还可以选择Eclipse或IntelliJ作为IDE。

