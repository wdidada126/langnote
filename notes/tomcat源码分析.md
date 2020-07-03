源码打日志的方式

```java
    	log.info("--isDebugEnabled--"+Boolean.toString(log.isDebugEnabled()));
    	log.info("--isInfoEnabled--"+Boolean.toString(log.isInfoEnabled()));	
```



tomcat端口占用启动报错

```shell
java.net.BindException: Address already in use: JVM_Bind
	at java.net.DualStackPlainSocketImpl.bind0(Native Method)
	at java.net.DualStackPlainSocketImpl.socketBind(Unknown Source)
	at java.net.AbstractPlainSocketImpl.bind(Unknown Source)
	at java.net.PlainSocketImpl.bind(Unknown Source)
	at java.net.ServerSocket.bind(Unknown Source)
	at java.net.ServerSocket.<init>(Unknown Source)
	at org.apache.catalina.core.StandardServer.await(StandardServer.java:441)
	at org.apache.catalina.startup.Catalina.await(Catalina.java:769)
	at org.apache.catalina.startup.Catalina.start(Catalina.java:715)
	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at sun.reflect.NativeMethodAccessorImpl.invoke(Unknown Source)
	at sun.reflect.DelegatingMethodAccessorImpl.invoke(Unknown Source)
	at java.lang.reflect.Method.invoke(Unknown Source)
	at org.apache.catalina.startup.Bootstrap.start(Bootstrap.java:353)
	at org.apache.catalina.startup.Bootstrap.main(Bootstrap.java:494)
```


反射调用的类

Service

Method

Digester

Coyote

gzip deflate

ArpEngponit

chap 3

$CATALINA_BASE/conf/catalina.properties


conf/web.xml
conf/server.xml

web.xml是所有部署到tomcat工程的配置文件
org.apache.catalina.servlets.DefaultServlet
org.apache.jasper.servlet.JspServlet

chap 4
Jasper tomcat中的JSP引擎

Apache tribes

JNDI Java Name Directory Interface




tomcat 源码研究之war工程解析

http://584431411.iteye.com/blog/2376753

https://www.cnblogs.com/coldridgeValley/p/6096154.html

HostConfig对war工程前期的校验 而ContextConfig对war包的真正解析
ExpandWar

HostConfig.DeployWar



Authenticator负责收集按照不同的认证方式收集数据，并调用Realm完成认证





Tomcat

webapps文件夹下面，可以放置多个war文件

自定义classloader

多个应用相互之间不能访问，保证安全


