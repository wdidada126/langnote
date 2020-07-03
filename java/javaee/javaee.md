# javaee

`lusrmgr.msc`

查看windows系统用户





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










首先，将近五年前它被称为Java EE。首字母缩略词J2EE仍指5.0之前的较旧Java EE版本。

对于Glassfish，这是Oracle对Java EE的具体实现。 Java EE是一个抽象的API，每个人都可以自由实现。有几种可用的Java EE实现，或者是像Oracle Glassfish 3，JBoss AS 6等完整的实现，还是像Apache Tomcat 7，Eclipse Jetty 8这样的部分(仅JSP / Servlet)实现。Glassfish Web Profile也是其中的一部分实施。

如果您打算仅使用JSP / Servlet进行开发，那么Glassfish Web Profile就足够了。如果您打算在Netbeans IDE的帮助下进行开发，请选择与Netbeans捆绑销售的产品。但是，除了Netbeans，您还可以选择Eclipse或IntelliJ作为IDE。

