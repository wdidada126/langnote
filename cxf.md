# cxf

github repo


本质是HTTP

test tool: soapui


区块链 拜占庭将军问题 笔记2-理解 Quorum 概念
https://zhuanlan.zhihu.com/p/104700455



Soap

https://blog.csdn.net/chen_long_yue/article/details/90411006



spring + cxf 的整合
http://cxf.apache.org/docs/writing-a-service-with-spring.html



# Spring和CXF整合发布WebService(服务端、客户端)

https://blog.csdn.net/yhahaha_/article/details/81395397





[visit wsdl](http://localhost:8109/springcxf-1.0-SNAPSHOT/service)





webservice是分布式的，基于http的，可以基于七层，四层去做负载均衡



接口暴露是通过wsdl的



SC是通过http协议的



SOAP 由 IBM、Microsoft、UserLand 和 DevelopMentor 在 1998 年共同提出，并得到 IBM、Lotus、Compaq 等公司的支持，于 2000 年提交 W3C。目前 SOAP 1.1 版是业界标准，是第二代 XML 协定。第一代的主要代表为 XML-RPC 和 WDDX。

SOAP 的一个简单例子：假设，有一个房价的数据库，SOAP 消息参数中指定房价查询信息，Web 服务点根据该查询信息，返回一个 XML 格式信息，其中包含查询结果（如价格、位置、特点，或者其他信息）。由于 XML 数据是一种结构化文本标准，可以被第三方使用。



[概念——SOAP（简单对象访问协议）](https://www.cnblogs.com/liuning8023/archive/2012/07/28/2613620.html)

而soap是简单对象访问协议，而soap绑定服务的时候可以是http smtp ftp等任意一种，貌似还可以绑定jms ejb..



cxf.png





webservice简单来说是一个规范，它定义了多个不同平台下不同语言开发的项目之间如何通信。

比如有两个项目，一个是windows系统的C#项目，一个是运行在linux系统中的java项目，那么这两个项目就可以通过实现了webservice规范的技术来实现之间的通信



```shell
D:\Java\jdk1.8.0_231\bin\java.exe -DSTOP.PORT=0 -Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.port=1099 -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.ssl=false -DOPTIONS=jmx "-javaagent:C:\Program Files\JetBrains\IntelliJ IDEA 2018.2.4\lib\idea_rt.jar=13710:C:\Program Files\JetBrains\IntelliJ IDEA 2018.2.4\bin" -Dfile.encoding=GBK -classpath D:\jetty-distribution-8.1.13.v20130916-1\start.jar;D:\Java\jdk1.8.0_231\lib\tools.jar org.eclipse.jetty.start.Main C:\Users\edidada\AppData\Local\Temp\context8537config\contexts-config.xml
[2020-04-27 05:41:14,514] Artifact springcxf:war: Waiting for server connection to start artifact deployment...
Detected server http port: 8109
WARNING: System properties and/or JVM args set.  Consider using --dry-run or --exec
2020-04-27 17:41:16.521:WARN:oejd.ContextDeployer:ContextDeployer is deprecated. Use ContextProvider
STOP.PORT=13725
STOP.KEY=14q0y8lvw7dhc
2020-04-27 17:41:16.527:INFO:oejs.Server:jetty-8.1.13.v20130916
2020-04-27 17:41:16.543:INFO:oejdp.ScanningAppProvider:Deployment monitor D:\jetty-distribution-8.1.13.v20130916-1\webapps at interval 1
2020-04-27 17:41:16.547:INFO:oejd.DeploymentManager:Deployable added: D:\jetty-distribution-8.1.13.v20130916-1\webapps\spdy.war
2020-04-27 17:41:16.644:INFO:oejw.WebInfConfiguration:Extract jar:file:/D:/jetty-distribution-8.1.13.v20130916-1/webapps/spdy.war!/ to C:\Users\edidada\AppData\Local\Temp\jetty-0.0.0.0-8109-spdy.war-_spdy-any-\webapp
2020-04-27 17:41:17.538:INFO:oejdp.ScanningAppProvider:Deployment monitor D:\jetty-distribution-8.1.13.v20130916-1\contexts at interval 1
2020-04-27 17:41:17.540:INFO:oejd.DeploymentManager:Deployable added: D:\jetty-distribution-8.1.13.v20130916-1\contexts\javadoc.xml
2020-04-27 17:41:17.563:INFO:oejd.DeploymentManager:Deployable added: D:\jetty-distribution-8.1.13.v20130916-1\contexts\test.xml
2020-04-27 17:41:17.641:INFO:oejw.WebInfConfiguration:Extract jar:file:/D:/jetty-distribution-8.1.13.v20130916-1/webapps/test.war!/ to C:\Users\edidada\AppData\Local\Temp\jetty-0.0.0.0-8109-test.war-_-any-\webapp
2020-04-27 17:41:19.906:INFO:oejs.TransparentProxy:TransparentProxy @ /javadoc-proxy to http://download.eclipse.org/jetty/stable-8/apidocs
2020-04-27 17:41:19.919:INFO:oejs.AbstractConnector:Started SelectChannelConnector@0.0.0.0:8109
ShutdownMonitorThread already started2020-04-27 17:41:19.937:INFO:oejs.Server:jetty-8.1.13.v20130916
Connected to server
[2020-04-27 05:41:19,949] Artifact springcxf:war: Artifact is being deployed, please wait...
2020-04-27 17:41:21.982:INFO:oejd.ContextDeployer:Deploy C:\Users\edidada\AppData\Local\Temp\context3681deploy\springcxf-1.0-SNAPSHOT.xml -> o.e.j.w.WebAppContext{/springcxf-1.0-SNAPSHOT,null},D:\git\github\springcxf\target\springcxf-1.0-SNAPSHOT.war
2020-04-27 17:41:22.042:INFO:oejw.WebInfConfiguration:Extract jar:file:/D:/git/github/springcxf/target/springcxf-1.0-SNAPSHOT.war!/ to D:\git\github\springcxf\target\springcxf-1.0-SNAPSHOT
2020-04-27 17:41:25.127:INFO:/.0-SNAPSHOT:No Spring WebApplicationInitializer types detected on classpath
2020-04-27 17:41:25.197:INFO:/.0-SNAPSHOT:Initializing Spring root WebApplicationContext
四月 27, 2020 5:41:25 下午 org.springframework.web.context.ContextLoader initWebApplicationContext
信息: Root WebApplicationContext: initialization started
四月 27, 2020 5:41:25 下午 org.springframework.web.context.support.XmlWebApplicationContext prepareRefresh
信息: Refreshing Root WebApplicationContext: startup date [Mon Apr 27 17:41:25 CST 2020]; root of context hierarchy
四月 27, 2020 5:41:25 下午 org.springframework.beans.factory.xml.XmlBeanDefinitionReader loadBeanDefinitions
信息: Loading XML bean definitions from class path resource [spring.xml]
四月 27, 2020 5:41:25 下午 org.springframework.beans.factory.xml.XmlBeanDefinitionReader loadBeanDefinitions
信息: Loading XML bean definitions from class path resource [spring-cxf.xml]
四月 27, 2020 5:41:26 下午 org.apache.cxf.wsdl.service.factory.ReflectionServiceFactoryBean buildServiceFromClass
信息: Creating Service {http://impl.springcxf.wdidada.cn/}HelloServiceImpService from class cn.wdidada.springcxf.HelloService
四月 27, 2020 5:41:26 下午 org.apache.cxf.endpoint.ServerImpl initDestination
信息: Setting the server's publish address to be /hello
四月 27, 2020 5:41:26 下午 org.springframework.web.context.ContextLoader initWebApplicationContext
信息: Root WebApplicationContext: initialization completed in 1551 ms
[2020-04-27 05:41:27,169] Artifact springcxf:war: Artifact is deployed successfully
[2020-04-27 05:41:27,169] Artifact springcxf:war: Deploy took 7,220 milliseconds
四月 27, 2020 5:41:28 下午 org.apache.cxf.service.invoker.AbstractInvoker invoke
严重: Invocation without a binding operation.
四月 27, 2020 5:41:28 下午 org.apache.cxf.phase.PhaseInterceptorChain doDefaultLogging
警告: Interceptor for {http://impl.springcxf.wdidada.cn/}HelloServiceImpService has thrown exception, unwinding now
org.apache.cxf.interceptor.Fault: No binding operation info while invoking unknown method with params unknown.
	at org.apache.cxf.service.invoker.AbstractInvoker.invoke(AbstractInvoker.java:58)
	at org.apache.cxf.interceptor.ServiceInvokerInterceptor$1.run(ServiceInvokerInterceptor.java:59)
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511)
	at java.util.concurrent.FutureTask.run(FutureTask.java:266)
	at org.apache.cxf.interceptor.ServiceInvokerInterceptor$2.run(ServiceInvokerInterceptor.java:126)
	at org.apache.cxf.workqueue.SynchronousExecutor.execute(SynchronousExecutor.java:37)
	at org.apache.cxf.interceptor.ServiceInvokerInterceptor.handleMessage(ServiceInvokerInterceptor.java:131)
	at org.apache.cxf.phase.PhaseInterceptorChain.doIntercept(PhaseInterceptorChain.java:308)
	at org.apache.cxf.transport.ChainInitiationObserver.onMessage(ChainInitiationObserver.java:121)
	at org.apache.cxf.transport.http.AbstractHTTPDestination.invoke(AbstractHTTPDestination.java:251)
	at org.apache.cxf.transport.servlet.ServletController.invokeDestination(ServletController.java:234)
	at org.apache.cxf.transport.servlet.ServletController.invoke(ServletController.java:208)
	at org.apache.cxf.transport.servlet.ServletController.invoke(ServletController.java:160)
	at org.apache.cxf.transport.servlet.CXFNonSpringServlet.invoke(CXFNonSpringServlet.java:180)
	at org.apache.cxf.transport.servlet.AbstractHTTPServlet.handleRequest(AbstractHTTPServlet.java:293)
	at org.apache.cxf.transport.servlet.AbstractHTTPServlet.doGet(AbstractHTTPServlet.java:217)
	at javax.servlet.http.HttpServlet.service(HttpServlet.java:735)
	at org.apache.cxf.transport.servlet.AbstractHTTPServlet.service(AbstractHTTPServlet.java:268)
	at org.eclipse.jetty.servlet.ServletHolder.handle(ServletHolder.java:686)
	at org.eclipse.jetty.servlet.ServletHandler.doHandle(ServletHandler.java:501)
	at org.eclipse.jetty.server.handler.ScopedHandler.handle(ScopedHandler.java:137)
	at org.eclipse.jetty.security.SecurityHandler.handle(SecurityHandler.java:533)
	at org.eclipse.jetty.server.session.SessionHandler.doHandle(SessionHandler.java:231)
	at org.eclipse.jetty.server.handler.ContextHandler.doHandle(ContextHandler.java:1086)
	at org.eclipse.jetty.servlet.ServletHandler.doScope(ServletHandler.java:428)
	at org.eclipse.jetty.server.session.SessionHandler.doScope(SessionHandler.java:193)
	at org.eclipse.jetty.server.handler.ContextHandler.doScope(ContextHandler.java:1020)
	at org.eclipse.jetty.server.handler.ScopedHandler.handle(ScopedHandler.java:135)
	at org.eclipse.jetty.server.handler.ContextHandlerCollection.handle(ContextHandlerCollection.java:255)
	at org.eclipse.jetty.server.handler.HandlerCollection.handle(HandlerCollection.java:154)
	at org.eclipse.jetty.server.handler.HandlerWrapper.handle(HandlerWrapper.java:116)
	at org.eclipse.jetty.server.Server.handle(Server.java:370)
	at org.eclipse.jetty.server.AbstractHttpConnection.handleRequest(AbstractHttpConnection.java:489)
	at org.eclipse.jetty.server.AbstractHttpConnection.headerComplete(AbstractHttpConnection.java:949)
	at org.eclipse.jetty.server.AbstractHttpConnection$RequestHandler.headerComplete(AbstractHttpConnection.java:1011)
	at org.eclipse.jetty.http.HttpParser.parseNext(HttpParser.java:644)
	at org.eclipse.jetty.http.HttpParser.parseAvailable(HttpParser.java:235)
	at org.eclipse.jetty.server.AsyncHttpConnection.handle(AsyncHttpConnection.java:82)
	at org.eclipse.jetty.io.nio.SelectChannelEndPoint.handle(SelectChannelEndPoint.java:668)
	at org.eclipse.jetty.io.nio.SelectChannelEndPoint$1.run(SelectChannelEndPoint.java:52)
	at org.eclipse.jetty.util.thread.QueuedThreadPool.runJob(QueuedThreadPool.java:608)
	at org.eclipse.jetty.util.thread.QueuedThreadPool$3.run(QueuedThreadPool.java:543)
	at java.lang.Thread.run(Thread.java:748)

四月 27, 2020 5:41:39 下午 org.apache.cxf.service.invoker.AbstractInvoker invoke
严重: Invocation without a binding operation.
四月 27, 2020 5:41:39 下午 org.apache.cxf.phase.PhaseInterceptorChain doDefaultLogging
警告: Interceptor for {http://impl.springcxf.wdidada.cn/}HelloServiceImpService has thrown exception, unwinding now
org.apache.cxf.interceptor.Fault: No binding operation info while invoking unknown method with params unknown.
	at org.apache.cxf.service.invoker.AbstractInvoker.invoke(AbstractInvoker.java:58)
	at org.apache.cxf.interceptor.ServiceInvokerInterceptor$1.run(ServiceInvokerInterceptor.java:59)
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511)
	at java.util.concurrent.FutureTask.run(FutureTask.java:266)
	at org.apache.cxf.interceptor.ServiceInvokerInterceptor$2.run(ServiceInvokerInterceptor.java:126)
	at org.apache.cxf.workqueue.SynchronousExecutor.execute(SynchronousExecutor.java:37)
	at org.apache.cxf.interceptor.ServiceInvokerInterceptor.handleMessage(ServiceInvokerInterceptor.java:131)
	at org.apache.cxf.phase.PhaseInterceptorChain.doIntercept(PhaseInterceptorChain.java:308)
	at org.apache.cxf.transport.ChainInitiationObserver.onMessage(ChainInitiationObserver.java:121)
	at org.apache.cxf.transport.http.AbstractHTTPDestination.invoke(AbstractHTTPDestination.java:251)
	at org.apache.cxf.transport.servlet.ServletController.invokeDestination(ServletController.java:234)
	at org.apache.cxf.transport.servlet.ServletController.invoke(ServletController.java:208)
	at org.apache.cxf.transport.servlet.ServletController.invoke(ServletController.java:160)
	at org.apache.cxf.transport.servlet.CXFNonSpringServlet.invoke(CXFNonSpringServlet.java:180)
	at org.apache.cxf.transport.servlet.AbstractHTTPServlet.handleRequest(AbstractHTTPServlet.java:293)
	at org.apache.cxf.transport.servlet.AbstractHTTPServlet.doGet(AbstractHTTPServlet.java:217)
	at javax.servlet.http.HttpServlet.service(HttpServlet.java:735)
	at org.apache.cxf.transport.servlet.AbstractHTTPServlet.service(AbstractHTTPServlet.java:268)
	at org.eclipse.jetty.servlet.ServletHolder.handle(ServletHolder.java:686)
	at org.eclipse.jetty.servlet.ServletHandler.doHandle(ServletHandler.java:501)
	at org.eclipse.jetty.server.handler.ScopedHandler.handle(ScopedHandler.java:137)
	at org.eclipse.jetty.security.SecurityHandler.handle(SecurityHandler.java:533)
	at org.eclipse.jetty.server.session.SessionHandler.doHandle(SessionHandler.java:231)
	at org.eclipse.jetty.server.handler.ContextHandler.doHandle(ContextHandler.java:1086)
	at org.eclipse.jetty.servlet.ServletHandler.doScope(ServletHandler.java:428)
	at org.eclipse.jetty.server.session.SessionHandler.doScope(SessionHandler.java:193)
	at org.eclipse.jetty.server.handler.ContextHandler.doScope(ContextHandler.java:1020)
	at org.eclipse.jetty.server.handler.ScopedHandler.handle(ScopedHandler.java:135)
	at org.eclipse.jetty.server.handler.ContextHandlerCollection.handle(ContextHandlerCollection.java:255)
	at org.eclipse.jetty.server.handler.HandlerCollection.handle(HandlerCollection.java:154)
	at org.eclipse.jetty.server.handler.HandlerWrapper.handle(HandlerWrapper.java:116)
	at org.eclipse.jetty.server.Server.handle(Server.java:370)
	at org.eclipse.jetty.server.AbstractHttpConnection.handleRequest(AbstractHttpConnection.java:489)
	at org.eclipse.jetty.server.AbstractHttpConnection.headerComplete(AbstractHttpConnection.java:949)
	at org.eclipse.jetty.server.AbstractHttpConnection$RequestHandler.headerComplete(AbstractHttpConnection.java:1011)
	at org.eclipse.jetty.http.HttpParser.parseNext(HttpParser.java:644)
	at org.eclipse.jetty.http.HttpParser.parseAvailable(HttpParser.java:235)
	at org.eclipse.jetty.server.AsyncHttpConnection.handle(AsyncHttpConnection.java:82)
	at org.eclipse.jetty.io.nio.SelectChannelEndPoint.handle(SelectChannelEndPoint.java:668)
	at org.eclipse.jetty.io.nio.SelectChannelEndPoint$1.run(SelectChannelEndPoint.java:52)
	at org.eclipse.jetty.util.thread.QueuedThreadPool.runJob(QueuedThreadPool.java:608)
	at org.eclipse.jetty.util.thread.QueuedThreadPool$3.run(QueuedThreadPool.java:543)
	at java.lang.Thread.run(Thread.java:748)

四月 27, 2020 5:41:43 下午 org.apache.cxf.service.invoker.AbstractInvoker invoke
严重: Invocation without a binding operation.
四月 27, 2020 5:41:43 下午 org.apache.cxf.phase.PhaseInterceptorChain doDefaultLogging
警告: Interceptor for {http://impl.springcxf.wdidada.cn/}HelloServiceImpService has thrown exception, unwinding now
org.apache.cxf.interceptor.Fault: No binding operation info while invoking unknown method with params unknown.
	at org.apache.cxf.service.invoker.AbstractInvoker.invoke(AbstractInvoker.java:58)
	at org.apache.cxf.interceptor.ServiceInvokerInterceptor$1.run(ServiceInvokerInterceptor.java:59)
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511)
	at java.util.concurrent.FutureTask.run(FutureTask.java:266)
	at org.apache.cxf.interceptor.ServiceInvokerInterceptor$2.run(ServiceInvokerInterceptor.java:126)
	at org.apache.cxf.workqueue.SynchronousExecutor.execute(SynchronousExecutor.java:37)
	at org.apache.cxf.interceptor.ServiceInvokerInterceptor.handleMessage(ServiceInvokerInterceptor.java:131)
	at org.apache.cxf.phase.PhaseInterceptorChain.doIntercept(PhaseInterceptorChain.java:308)
	at org.apache.cxf.transport.ChainInitiationObserver.onMessage(ChainInitiationObserver.java:121)
	at org.apache.cxf.transport.http.AbstractHTTPDestination.invoke(AbstractHTTPDestination.java:251)
	at org.apache.cxf.transport.servlet.ServletController.invokeDestination(ServletController.java:234)
	at org.apache.cxf.transport.servlet.ServletController.invoke(ServletController.java:208)
	at org.apache.cxf.transport.servlet.ServletController.invoke(ServletController.java:160)
	at org.apache.cxf.transport.servlet.CXFNonSpringServlet.invoke(CXFNonSpringServlet.java:180)
	at org.apache.cxf.transport.servlet.AbstractHTTPServlet.handleRequest(AbstractHTTPServlet.java:293)
	at org.apache.cxf.transport.servlet.AbstractHTTPServlet.doGet(AbstractHTTPServlet.java:217)
	at javax.servlet.http.HttpServlet.service(HttpServlet.java:735)
	at org.apache.cxf.transport.servlet.AbstractHTTPServlet.service(AbstractHTTPServlet.java:268)
	at org.eclipse.jetty.servlet.ServletHolder.handle(ServletHolder.java:686)
	at org.eclipse.jetty.servlet.ServletHandler.doHandle(ServletHandler.java:501)
	at org.eclipse.jetty.server.handler.ScopedHandler.handle(ScopedHandler.java:137)
	at org.eclipse.jetty.security.SecurityHandler.handle(SecurityHandler.java:533)
	at org.eclipse.jetty.server.session.SessionHandler.doHandle(SessionHandler.java:231)
	at org.eclipse.jetty.server.handler.ContextHandler.doHandle(ContextHandler.java:1086)
	at org.eclipse.jetty.servlet.ServletHandler.doScope(ServletHandler.java:428)
	at org.eclipse.jetty.server.session.SessionHandler.doScope(SessionHandler.java:193)
	at org.eclipse.jetty.server.handler.ContextHandler.doScope(ContextHandler.java:1020)
	at org.eclipse.jetty.server.handler.ScopedHandler.handle(ScopedHandler.java:135)
	at org.eclipse.jetty.server.handler.ContextHandlerCollection.handle(ContextHandlerCollection.java:255)
	at org.eclipse.jetty.server.handler.HandlerCollection.handle(HandlerCollection.java:154)
	at org.eclipse.jetty.server.handler.HandlerWrapper.handle(HandlerWrapper.java:116)
	at org.eclipse.jetty.server.Server.handle(Server.java:370)
	at org.eclipse.jetty.server.AbstractHttpConnection.handleRequest(AbstractHttpConnection.java:489)
	at org.eclipse.jetty.server.AbstractHttpConnection.headerComplete(AbstractHttpConnection.java:949)
	at org.eclipse.jetty.server.AbstractHttpConnection$RequestHandler.headerComplete(AbstractHttpConnection.java:1011)
	at org.eclipse.jetty.http.HttpParser.parseNext(HttpParser.java:644)
	at org.eclipse.jetty.http.HttpParser.parseAvailable(HttpParser.java:235)
	at org.eclipse.jetty.server.AsyncHttpConnection.handle(AsyncHttpConnection.java:82)
	at org.eclipse.jetty.io.nio.SelectChannelEndPoint.handle(SelectChannelEndPoint.java:668)
	at org.eclipse.jetty.io.nio.SelectChannelEndPoint$1.run(SelectChannelEndPoint.java:52)
	at org.eclipse.jetty.util.thread.QueuedThreadPool.runJob(QueuedThreadPool.java:608)
	at org.eclipse.jetty.util.thread.QueuedThreadPool$3.run(QueuedThreadPool.java:543)
	at java.lang.Thread.run(Thread.java:748)

四月 27, 2020 5:41:47 下午 org.apache.cxf.service.invoker.AbstractInvoker invoke
严重: Invocation without a binding operation.
四月 27, 2020 5:41:47 下午 org.apache.cxf.phase.PhaseInterceptorChain doDefaultLogging
警告: Interceptor for {http://impl.springcxf.wdidada.cn/}HelloServiceImpService has thrown exception, unwinding now
org.apache.cxf.interceptor.Fault: No binding operation info while invoking unknown method with params unknown.
	at org.apache.cxf.service.invoker.AbstractInvoker.invoke(AbstractInvoker.java:58)
	at org.apache.cxf.interceptor.ServiceInvokerInterceptor$1.run(ServiceInvokerInterceptor.java:59)
	at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511)
	at java.util.concurrent.FutureTask.run(FutureTask.java:266)
	at org.apache.cxf.interceptor.ServiceInvokerInterceptor$2.run(ServiceInvokerInterceptor.java:126)
	at org.apache.cxf.workqueue.SynchronousExecutor.execute(SynchronousExecutor.java:37)
	at org.apache.cxf.interceptor.ServiceInvokerInterceptor.handleMessage(ServiceInvokerInterceptor.java:131)
	at org.apache.cxf.phase.PhaseInterceptorChain.doIntercept(PhaseInterceptorChain.java:308)
	at org.apache.cxf.transport.ChainInitiationObserver.onMessage(ChainInitiationObserver.java:121)
	at org.apache.cxf.transport.http.AbstractHTTPDestination.invoke(AbstractHTTPDestination.java:251)
	at org.apache.cxf.transport.servlet.ServletController.invokeDestination(ServletController.java:234)
	at org.apache.cxf.transport.servlet.ServletController.invoke(ServletController.java:208)
	at org.apache.cxf.transport.servlet.ServletController.invoke(ServletController.java:160)
	at org.apache.cxf.transport.servlet.CXFNonSpringServlet.invoke(CXFNonSpringServlet.java:180)
	at org.apache.cxf.transport.servlet.AbstractHTTPServlet.handleRequest(AbstractHTTPServlet.java:293)
	at org.apache.cxf.transport.servlet.AbstractHTTPServlet.doGet(AbstractHTTPServlet.java:217)
	at javax.servlet.http.HttpServlet.service(HttpServlet.java:735)
	at org.apache.cxf.transport.servlet.AbstractHTTPServlet.service(AbstractHTTPServlet.java:268)
	at org.eclipse.jetty.servlet.ServletHolder.handle(ServletHolder.java:686)
	at org.eclipse.jetty.servlet.ServletHandler.doHandle(ServletHandler.java:501)
	at org.eclipse.jetty.server.handler.ScopedHandler.handle(ScopedHandler.java:137)
	at org.eclipse.jetty.security.SecurityHandler.handle(SecurityHandler.java:533)
	at org.eclipse.jetty.server.session.SessionHandler.doHandle(SessionHandler.java:231)
	at org.eclipse.jetty.server.handler.ContextHandler.doHandle(ContextHandler.java:1086)
	at org.eclipse.jetty.servlet.ServletHandler.doScope(ServletHandler.java:428)
	at org.eclipse.jetty.server.session.SessionHandler.doScope(SessionHandler.java:193)
	at org.eclipse.jetty.server.handler.ContextHandler.doScope(ContextHandler.java:1020)
	at org.eclipse.jetty.server.handler.ScopedHandler.handle(ScopedHandler.java:135)
	at org.eclipse.jetty.server.handler.ContextHandlerCollection.handle(ContextHandlerCollection.java:255)
	at org.eclipse.jetty.server.handler.HandlerCollection.handle(HandlerCollection.java:154)
	at org.eclipse.jetty.server.handler.HandlerWrapper.handle(HandlerWrapper.java:116)
	at org.eclipse.jetty.server.Server.handle(Server.java:370)
	at org.eclipse.jetty.server.AbstractHttpConnection.handleRequest(AbstractHttpConnection.java:489)
	at org.eclipse.jetty.server.AbstractHttpConnection.headerComplete(AbstractHttpConnection.java:949)
	at org.eclipse.jetty.server.AbstractHttpConnection$RequestHandler.headerComplete(AbstractHttpConnection.java:1011)
	at org.eclipse.jetty.http.HttpParser.parseNext(HttpParser.java:644)
	at org.eclipse.jetty.http.HttpParser.parseAvailable(HttpParser.java:235)
	at org.eclipse.jetty.server.AsyncHttpConnection.handle(AsyncHttpConnection.java:82)
	at org.eclipse.jetty.io.nio.SelectChannelEndPoint.handle(SelectChannelEndPoint.java:668)
	at org.eclipse.jetty.io.nio.SelectChannelEndPoint$1.run(SelectChannelEndPoint.java:52)
	at org.eclipse.jetty.util.thread.QueuedThreadPool.runJob(QueuedThreadPool.java:608)
	at org.eclipse.jetty.util.thread.QueuedThreadPool$3.run(QueuedThreadPool.java:543)
	at java.lang.Thread.run(Thread.java:748)

四月 27, 2020 5:44:44 下午 org.apache.cxf.phase.PhaseInterceptorChain doDefaultLogging
警告: Interceptor for {http://impl.springcxf.wdidada.cn/}HelloServiceImpService#{http://springcxf.wdidada.cn/}sayHello has thrown exception, unwinding now
org.apache.cxf.interceptor.Fault: Unmarshalling Error: 意外的元素 (uri:"", local:"name")。所需元素为<{}arg0> 
	at org.apache.cxf.jaxb.JAXBEncoderDecoder.unmarshall(JAXBEncoderDecoder.java:905)
	at org.apache.cxf.jaxb.JAXBEncoderDecoder.unmarshall(JAXBEncoderDecoder.java:712)
	at org.apache.cxf.jaxb.io.DataReaderImpl.read(DataReaderImpl.java:179)
	at org.apache.cxf.wsdl.interceptors.DocLiteralInInterceptor.handleMessage(DocLiteralInInterceptor.java:109)
	at org.apache.cxf.phase.PhaseInterceptorChain.doIntercept(PhaseInterceptorChain.java:308)
	at org.apache.cxf.transport.ChainInitiationObserver.onMessage(ChainInitiationObserver.java:121)
	at org.apache.cxf.transport.http.AbstractHTTPDestination.invoke(AbstractHTTPDestination.java:251)
	at org.apache.cxf.transport.servlet.ServletController.invokeDestination(ServletController.java:234)
	at org.apache.cxf.transport.servlet.ServletController.invoke(ServletController.java:208)
	at org.apache.cxf.transport.servlet.ServletController.invoke(ServletController.java:160)
	at org.apache.cxf.transport.servlet.CXFNonSpringServlet.invoke(CXFNonSpringServlet.java:180)
	at org.apache.cxf.transport.servlet.AbstractHTTPServlet.handleRequest(AbstractHTTPServlet.java:293)
	at org.apache.cxf.transport.servlet.AbstractHTTPServlet.doPost(AbstractHTTPServlet.java:212)
	at javax.servlet.http.HttpServlet.service(HttpServlet.java:755)
	at org.apache.cxf.transport.servlet.AbstractHTTPServlet.service(AbstractHTTPServlet.java:268)
	at org.eclipse.jetty.servlet.ServletHolder.handle(ServletHolder.java:686)
	at org.eclipse.jetty.servlet.ServletHandler.doHandle(ServletHandler.java:501)
	at org.eclipse.jetty.server.handler.ScopedHandler.handle(ScopedHandler.java:137)
	at org.eclipse.jetty.security.SecurityHandler.handle(SecurityHandler.java:533)
	at org.eclipse.jetty.server.session.SessionHandler.doHandle(SessionHandler.java:231)
	at org.eclipse.jetty.server.handler.ContextHandler.doHandle(ContextHandler.java:1086)
	at org.eclipse.jetty.servlet.ServletHandler.doScope(ServletHandler.java:428)
	at org.eclipse.jetty.server.session.SessionHandler.doScope(SessionHandler.java:193)
	at org.eclipse.jetty.server.handler.ContextHandler.doScope(ContextHandler.java:1020)
	at org.eclipse.jetty.server.handler.ScopedHandler.handle(ScopedHandler.java:135)
	at org.eclipse.jetty.server.handler.ContextHandlerCollection.handle(ContextHandlerCollection.java:255)
	at org.eclipse.jetty.server.handler.HandlerCollection.handle(HandlerCollection.java:154)
	at org.eclipse.jetty.server.handler.HandlerWrapper.handle(HandlerWrapper.java:116)
	at org.eclipse.jetty.server.Server.handle(Server.java:370)
	at org.eclipse.jetty.server.AbstractHttpConnection.handleRequest(AbstractHttpConnection.java:489)
	at org.eclipse.jetty.server.AbstractHttpConnection.content(AbstractHttpConnection.java:960)
	at org.eclipse.jetty.server.AbstractHttpConnection$RequestHandler.content(AbstractHttpConnection.java:1021)
	at org.eclipse.jetty.http.HttpParser.parseNext(HttpParser.java:865)
	at org.eclipse.jetty.http.HttpParser.parseAvailable(HttpParser.java:240)
	at org.eclipse.jetty.server.AsyncHttpConnection.handle(AsyncHttpConnection.java:82)
	at org.eclipse.jetty.io.nio.SelectChannelEndPoint.handle(SelectChannelEndPoint.java:668)
	at org.eclipse.jetty.io.nio.SelectChannelEndPoint$1.run(SelectChannelEndPoint.java:52)
	at org.eclipse.jetty.util.thread.QueuedThreadPool.runJob(QueuedThreadPool.java:608)
	at org.eclipse.jetty.util.thread.QueuedThreadPool$3.run(QueuedThreadPool.java:543)
	at java.lang.Thread.run(Thread.java:748)
Caused by: javax.xml.bind.UnmarshalException
 - with linked exception:
[com.sun.istack.SAXParseException2; lineNumber: 6; columnNumber: 10; 意外的元素 (uri:"", local:"name")。所需元素为<{}arg0>]
	at com.sun.xml.bind.v2.runtime.unmarshaller.UnmarshallerImpl.handleStreamException(UnmarshallerImpl.java:483)
	at com.sun.xml.bind.v2.runtime.unmarshaller.UnmarshallerImpl.unmarshal0(UnmarshallerImpl.java:417)
	at com.sun.xml.bind.v2.runtime.unmarshaller.UnmarshallerImpl.unmarshal(UnmarshallerImpl.java:394)
	at org.apache.cxf.jaxb.JAXBEncoderDecoder.doUnmarshal(JAXBEncoderDecoder.java:855)
	at org.apache.cxf.jaxb.JAXBEncoderDecoder.access$100(JAXBEncoderDecoder.java:102)
	at org.apache.cxf.jaxb.JAXBEncoderDecoder$2.run(JAXBEncoderDecoder.java:894)
	at java.security.AccessController.doPrivileged(Native Method)
	at org.apache.cxf.jaxb.JAXBEncoderDecoder.unmarshall(JAXBEncoderDecoder.java:892)
	... 39 more
Caused by: com.sun.istack.SAXParseException2; lineNumber: 6; columnNumber: 10; 意外的元素 (uri:"", local:"name")。所需元素为<{}arg0>
	at com.sun.xml.bind.v2.runtime.unmarshaller.UnmarshallingContext.handleEvent(UnmarshallingContext.java:740)
	at com.sun.xml.bind.v2.runtime.unmarshaller.Loader.reportError(Loader.java:262)
	at com.sun.xml.bind.v2.runtime.unmarshaller.Loader.reportError(Loader.java:257)
	at com.sun.xml.bind.v2.runtime.unmarshaller.Loader.reportUnexpectedChildElement(Loader.java:124)
	at com.sun.xml.bind.v2.runtime.unmarshaller.Loader.childElement(Loader.java:105)
	at com.sun.xml.bind.v2.runtime.unmarshaller.StructureLoader.childElement(StructureLoader.java:262)
	at com.sun.xml.bind.v2.runtime.unmarshaller.UnmarshallingContext._startElement(UnmarshallingContext.java:573)
	at com.sun.xml.bind.v2.runtime.unmarshaller.UnmarshallingContext.startElement(UnmarshallingContext.java:555)
	at com.sun.xml.bind.v2.runtime.unmarshaller.StAXStreamConnector.handleStartElement(StAXStreamConnector.java:246)
	at com.sun.xml.bind.v2.runtime.unmarshaller.StAXStreamConnector.bridge(StAXStreamConnector.java:180)
	at com.sun.xml.bind.v2.runtime.unmarshaller.UnmarshallerImpl.unmarshal0(UnmarshallerImpl.java:415)
	... 45 more
Caused by: javax.xml.bind.UnmarshalException: 意外的元素 (uri:"", local:"name")。所需元素为<{}arg0>
	... 56 more

四月 27, 2020 5:53:40 下午 org.apache.cxf.phase.PhaseInterceptorChain doDefaultLogging
警告: Interceptor for {http://impl.springcxf.wdidada.cn/}HelloServiceImpService#{http://springcxf.wdidada.cn/}sayHello has thrown exception, unwinding now
org.apache.cxf.interceptor.Fault: Unmarshalling Error: 意外的元素 (uri:"http://springcxf.wdidada.cn/", local:"name")。所需元素为<{}arg0> 
	at org.apache.cxf.jaxb.JAXBEncoderDecoder.unmarshall(JAXBEncoderDecoder.java:905)
	at org.apache.cxf.jaxb.JAXBEncoderDecoder.unmarshall(JAXBEncoderDecoder.java:712)
	at org.apache.cxf.jaxb.io.DataReaderImpl.read(DataReaderImpl.java:179)
	at org.apache.cxf.wsdl.interceptors.DocLiteralInInterceptor.handleMessage(DocLiteralInInterceptor.java:109)
	at org.apache.cxf.phase.PhaseInterceptorChain.doIntercept(PhaseInterceptorChain.java:308)
	at org.apache.cxf.transport.ChainInitiationObserver.onMessage(ChainInitiationObserver.java:121)
	at org.apache.cxf.transport.http.AbstractHTTPDestination.invoke(AbstractHTTPDestination.java:251)
	at org.apache.cxf.transport.servlet.ServletController.invokeDestination(ServletController.java:234)
	at org.apache.cxf.transport.servlet.ServletController.invoke(ServletController.java:208)
	at org.apache.cxf.transport.servlet.ServletController.invoke(ServletController.java:160)
	at org.apache.cxf.transport.servlet.CXFNonSpringServlet.invoke(CXFNonSpringServlet.java:180)
	at org.apache.cxf.transport.servlet.AbstractHTTPServlet.handleRequest(AbstractHTTPServlet.java:293)
	at org.apache.cxf.transport.servlet.AbstractHTTPServlet.doPost(AbstractHTTPServlet.java:212)
	at javax.servlet.http.HttpServlet.service(HttpServlet.java:755)
	at org.apache.cxf.transport.servlet.AbstractHTTPServlet.service(AbstractHTTPServlet.java:268)
	at org.eclipse.jetty.servlet.ServletHolder.handle(ServletHolder.java:686)
	at org.eclipse.jetty.servlet.ServletHandler.doHandle(ServletHandler.java:501)
	at org.eclipse.jetty.server.handler.ScopedHandler.handle(ScopedHandler.java:137)
	at org.eclipse.jetty.security.SecurityHandler.handle(SecurityHandler.java:533)
	at org.eclipse.jetty.server.session.SessionHandler.doHandle(SessionHandler.java:231)
	at org.eclipse.jetty.server.handler.ContextHandler.doHandle(ContextHandler.java:1086)
	at org.eclipse.jetty.servlet.ServletHandler.doScope(ServletHandler.java:428)
	at org.eclipse.jetty.server.session.SessionHandler.doScope(SessionHandler.java:193)
	at org.eclipse.jetty.server.handler.ContextHandler.doScope(ContextHandler.java:1020)
	at org.eclipse.jetty.server.handler.ScopedHandler.handle(ScopedHandler.java:135)
	at org.eclipse.jetty.server.handler.ContextHandlerCollection.handle(ContextHandlerCollection.java:255)
	at org.eclipse.jetty.server.handler.HandlerCollection.handle(HandlerCollection.java:154)
	at org.eclipse.jetty.server.handler.HandlerWrapper.handle(HandlerWrapper.java:116)
	at org.eclipse.jetty.server.Server.handle(Server.java:370)
	at org.eclipse.jetty.server.AbstractHttpConnection.handleRequest(AbstractHttpConnection.java:489)
	at org.eclipse.jetty.server.AbstractHttpConnection.content(AbstractHttpConnection.java:960)
	at org.eclipse.jetty.server.AbstractHttpConnection$RequestHandler.content(AbstractHttpConnection.java:1021)
	at org.eclipse.jetty.http.HttpParser.parseNext(HttpParser.java:865)
	at org.eclipse.jetty.http.HttpParser.parseAvailable(HttpParser.java:240)
	at org.eclipse.jetty.server.AsyncHttpConnection.handle(AsyncHttpConnection.java:82)
	at org.eclipse.jetty.io.nio.SelectChannelEndPoint.handle(SelectChannelEndPoint.java:668)
	at org.eclipse.jetty.io.nio.SelectChannelEndPoint$1.run(SelectChannelEndPoint.java:52)
	at org.eclipse.jetty.util.thread.QueuedThreadPool.runJob(QueuedThreadPool.java:608)
	at org.eclipse.jetty.util.thread.QueuedThreadPool$3.run(QueuedThreadPool.java:543)
	at java.lang.Thread.run(Thread.java:748)
Caused by: javax.xml.bind.UnmarshalException
 - with linked exception:
[com.sun.istack.SAXParseException2; lineNumber: 5; columnNumber: 8; 意外的元素 (uri:"http://springcxf.wdidada.cn/", local:"name")。所需元素为<{}arg0>]
	at com.sun.xml.bind.v2.runtime.unmarshaller.UnmarshallerImpl.handleStreamException(UnmarshallerImpl.java:483)
	at com.sun.xml.bind.v2.runtime.unmarshaller.UnmarshallerImpl.unmarshal0(UnmarshallerImpl.java:417)
	at com.sun.xml.bind.v2.runtime.unmarshaller.UnmarshallerImpl.unmarshal(UnmarshallerImpl.java:394)
	at org.apache.cxf.jaxb.JAXBEncoderDecoder.doUnmarshal(JAXBEncoderDecoder.java:855)
	at org.apache.cxf.jaxb.JAXBEncoderDecoder.access$100(JAXBEncoderDecoder.java:102)
	at org.apache.cxf.jaxb.JAXBEncoderDecoder$2.run(JAXBEncoderDecoder.java:894)
	at java.security.AccessController.doPrivileged(Native Method)
	at org.apache.cxf.jaxb.JAXBEncoderDecoder.unmarshall(JAXBEncoderDecoder.java:892)
	... 39 more
Caused by: com.sun.istack.SAXParseException2; lineNumber: 5; columnNumber: 8; 意外的元素 (uri:"http://springcxf.wdidada.cn/", local:"name")。所需元素为<{}arg0>
	at com.sun.xml.bind.v2.runtime.unmarshaller.UnmarshallingContext.handleEvent(UnmarshallingContext.java:740)
	at com.sun.xml.bind.v2.runtime.unmarshaller.Loader.reportError(Loader.java:262)
	at com.sun.xml.bind.v2.runtime.unmarshaller.Loader.reportError(Loader.java:257)
	at com.sun.xml.bind.v2.runtime.unmarshaller.Loader.reportUnexpectedChildElement(Loader.java:124)
	at com.sun.xml.bind.v2.runtime.unmarshaller.Loader.childElement(Loader.java:105)
	at com.sun.xml.bind.v2.runtime.unmarshaller.StructureLoader.childElement(StructureLoader.java:262)
	at com.sun.xml.bind.v2.runtime.unmarshaller.UnmarshallingContext._startElement(UnmarshallingContext.java:573)
	at com.sun.xml.bind.v2.runtime.unmarshaller.UnmarshallingContext.startElement(UnmarshallingContext.java:555)
	at com.sun.xml.bind.v2.runtime.unmarshaller.StAXStreamConnector.handleStartElement(StAXStreamConnector.java:246)
	at com.sun.xml.bind.v2.runtime.unmarshaller.StAXStreamConnector.bridge(StAXStreamConnector.java:180)
	at com.sun.xml.bind.v2.runtime.unmarshaller.UnmarshallerImpl.unmarshal0(UnmarshallerImpl.java:415)
	... 45 more
Caused by: javax.xml.bind.UnmarshalException: 意外的元素 (uri:"http://springcxf.wdidada.cn/", local:"name")。所需元素为<{}arg0>
	... 56 more

四月 27, 2020 5:54:06 下午 org.apache.cxf.phase.PhaseInterceptorChain doDefaultLogging
警告: Interceptor for {http://impl.springcxf.wdidada.cn/}HelloServiceImpService#{http://springcxf.wdidada.cn/}sayHello has thrown exception, unwinding now
org.apache.cxf.interceptor.Fault: Unmarshalling Error: 意外的元素 (uri:"", local:"name")。所需元素为<{}arg0> 
	at org.apache.cxf.jaxb.JAXBEncoderDecoder.unmarshall(JAXBEncoderDecoder.java:905)
	at org.apache.cxf.jaxb.JAXBEncoderDecoder.unmarshall(JAXBEncoderDecoder.java:712)
	at org.apache.cxf.jaxb.io.DataReaderImpl.read(DataReaderImpl.java:179)
	at org.apache.cxf.wsdl.interceptors.DocLiteralInInterceptor.handleMessage(DocLiteralInInterceptor.java:109)
	at org.apache.cxf.phase.PhaseInterceptorChain.doIntercept(PhaseInterceptorChain.java:308)
	at org.apache.cxf.transport.ChainInitiationObserver.onMessage(ChainInitiationObserver.java:121)
	at org.apache.cxf.transport.http.AbstractHTTPDestination.invoke(AbstractHTTPDestination.java:251)
	at org.apache.cxf.transport.servlet.ServletController.invokeDestination(ServletController.java:234)
	at org.apache.cxf.transport.servlet.ServletController.invoke(ServletController.java:208)
	at org.apache.cxf.transport.servlet.ServletController.invoke(ServletController.java:160)
	at org.apache.cxf.transport.servlet.CXFNonSpringServlet.invoke(CXFNonSpringServlet.java:180)
	at org.apache.cxf.transport.servlet.AbstractHTTPServlet.handleRequest(AbstractHTTPServlet.java:293)
	at org.apache.cxf.transport.servlet.AbstractHTTPServlet.doPost(AbstractHTTPServlet.java:212)
	at javax.servlet.http.HttpServlet.service(HttpServlet.java:755)
	at org.apache.cxf.transport.servlet.AbstractHTTPServlet.service(AbstractHTTPServlet.java:268)
	at org.eclipse.jetty.servlet.ServletHolder.handle(ServletHolder.java:686)
	at org.eclipse.jetty.servlet.ServletHandler.doHandle(ServletHandler.java:501)
	at org.eclipse.jetty.server.handler.ScopedHandler.handle(ScopedHandler.java:137)
	at org.eclipse.jetty.security.SecurityHandler.handle(SecurityHandler.java:533)
	at org.eclipse.jetty.server.session.SessionHandler.doHandle(SessionHandler.java:231)
	at org.eclipse.jetty.server.handler.ContextHandler.doHandle(ContextHandler.java:1086)
	at org.eclipse.jetty.servlet.ServletHandler.doScope(ServletHandler.java:428)
	at org.eclipse.jetty.server.session.SessionHandler.doScope(SessionHandler.java:193)
	at org.eclipse.jetty.server.handler.ContextHandler.doScope(ContextHandler.java:1020)
	at org.eclipse.jetty.server.handler.ScopedHandler.handle(ScopedHandler.java:135)
	at org.eclipse.jetty.server.handler.ContextHandlerCollection.handle(ContextHandlerCollection.java:255)
	at org.eclipse.jetty.server.handler.HandlerCollection.handle(HandlerCollection.java:154)
	at org.eclipse.jetty.server.handler.HandlerWrapper.handle(HandlerWrapper.java:116)
	at org.eclipse.jetty.server.Server.handle(Server.java:370)
	at org.eclipse.jetty.server.AbstractHttpConnection.handleRequest(AbstractHttpConnection.java:489)
	at org.eclipse.jetty.server.AbstractHttpConnection.content(AbstractHttpConnection.java:960)
	at org.eclipse.jetty.server.AbstractHttpConnection$RequestHandler.content(AbstractHttpConnection.java:1021)
	at org.eclipse.jetty.http.HttpParser.parseNext(HttpParser.java:865)
	at org.eclipse.jetty.http.HttpParser.parseAvailable(HttpParser.java:240)
	at org.eclipse.jetty.server.AsyncHttpConnection.handle(AsyncHttpConnection.java:82)
	at org.eclipse.jetty.io.nio.SelectChannelEndPoint.handle(SelectChannelEndPoint.java:668)
	at org.eclipse.jetty.io.nio.SelectChannelEndPoint$1.run(SelectChannelEndPoint.java:52)
	at org.eclipse.jetty.util.thread.QueuedThreadPool.runJob(QueuedThreadPool.java:608)
	at org.eclipse.jetty.util.thread.QueuedThreadPool$3.run(QueuedThreadPool.java:543)
	at java.lang.Thread.run(Thread.java:748)
Caused by: javax.xml.bind.UnmarshalException
 - with linked exception:
[com.sun.istack.SAXParseException2; lineNumber: 5; columnNumber: 8; 意外的元素 (uri:"", local:"name")。所需元素为<{}arg0>]
	at com.sun.xml.bind.v2.runtime.unmarshaller.UnmarshallerImpl.handleStreamException(UnmarshallerImpl.java:483)
	at com.sun.xml.bind.v2.runtime.unmarshaller.UnmarshallerImpl.unmarshal0(UnmarshallerImpl.java:417)
	at com.sun.xml.bind.v2.runtime.unmarshaller.UnmarshallerImpl.unmarshal(UnmarshallerImpl.java:394)
	at org.apache.cxf.jaxb.JAXBEncoderDecoder.doUnmarshal(JAXBEncoderDecoder.java:855)
	at org.apache.cxf.jaxb.JAXBEncoderDecoder.access$100(JAXBEncoderDecoder.java:102)
	at org.apache.cxf.jaxb.JAXBEncoderDecoder$2.run(JAXBEncoderDecoder.java:894)
	at java.security.AccessController.doPrivileged(Native Method)
	at org.apache.cxf.jaxb.JAXBEncoderDecoder.unmarshall(JAXBEncoderDecoder.java:892)
	... 39 more
Caused by: com.sun.istack.SAXParseException2; lineNumber: 5; columnNumber: 8; 意外的元素 (uri:"", local:"name")。所需元素为<{}arg0>
	at com.sun.xml.bind.v2.runtime.unmarshaller.UnmarshallingContext.handleEvent(UnmarshallingContext.java:740)
	at com.sun.xml.bind.v2.runtime.unmarshaller.Loader.reportError(Loader.java:262)
	at com.sun.xml.bind.v2.runtime.unmarshaller.Loader.reportError(Loader.java:257)
	at com.sun.xml.bind.v2.runtime.unmarshaller.Loader.reportUnexpectedChildElement(Loader.java:124)
	at com.sun.xml.bind.v2.runtime.unmarshaller.Loader.childElement(Loader.java:105)
	at com.sun.xml.bind.v2.runtime.unmarshaller.StructureLoader.childElement(StructureLoader.java:262)
	at com.sun.xml.bind.v2.runtime.unmarshaller.UnmarshallingContext._startElement(UnmarshallingContext.java:573)
	at com.sun.xml.bind.v2.runtime.unmarshaller.UnmarshallingContext.startElement(UnmarshallingContext.java:555)
	at com.sun.xml.bind.v2.runtime.unmarshaller.StAXStreamConnector.handleStartElement(StAXStreamConnector.java:246)
	at com.sun.xml.bind.v2.runtime.unmarshaller.StAXStreamConnector.bridge(StAXStreamConnector.java:180)
	at com.sun.xml.bind.v2.runtime.unmarshaller.UnmarshallerImpl.unmarshal0(UnmarshallerImpl.java:415)
	... 45 more
Caused by: javax.xml.bind.UnmarshalException: 意外的元素 (uri:"", local:"name")。所需元素为<{}arg0>
	... 56 more
```



```shell
D:\Java\jdk1.8.0_231\bin\java.exe -DSTOP.PORT=0 -Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.port=1099 -Dcom.sun.management.jmxremote.authenticate=false -Dcom.sun.management.jmxremote.ssl=false -DOPTIONS=jmx "-javaagent:C:\Program Files\JetBrains\IntelliJ IDEA 2018.2.4\lib\idea_rt.jar=3149:C:\Program Files\JetBrains\IntelliJ IDEA 2018.2.4\bin" -Dfile.encoding=GBK -classpath D:\jetty-distribution-8.1.13.v20130916-1\start.jar;D:\Java\jdk1.8.0_231\lib\tools.jar org.eclipse.jetty.start.Main C:\Users\edidada\AppData\Local\Temp\context6203config\contexts-config.xml
[2020-04-27 06:03:44,711] Artifact springcxf:war: Waiting for server connection to start artifact deployment...
Detected server http port: 8109
WARNING: System properties and/or JVM args set.  Consider using --dry-run or --exec
2020-04-27 18:03:46.593:WARN:oejd.ContextDeployer:ContextDeployer is deprecated. Use ContextProvider
STOP.PORT=3206
STOP.KEY=1mm46ewp1yccg
2020-04-27 18:03:46.598:INFO:oejs.Server:jetty-8.1.13.v20130916
2020-04-27 18:03:46.625:INFO:oejdp.ScanningAppProvider:Deployment monitor D:\jetty-distribution-8.1.13.v20130916-1\webapps at interval 1
2020-04-27 18:03:46.630:INFO:oejd.DeploymentManager:Deployable added: D:\jetty-distribution-8.1.13.v20130916-1\webapps\spdy.war
2020-04-27 18:03:46.710:INFO:oejw.WebInfConfiguration:Extract jar:file:/D:/jetty-distribution-8.1.13.v20130916-1/webapps/spdy.war!/ to C:\Users\edidada\AppData\Local\Temp\jetty-0.0.0.0-8109-spdy.war-_spdy-any-\webapp
2020-04-27 18:03:47.393:INFO:oejdp.ScanningAppProvider:Deployment monitor D:\jetty-distribution-8.1.13.v20130916-1\contexts at interval 1
2020-04-27 18:03:47.394:INFO:oejd.DeploymentManager:Deployable added: D:\jetty-distribution-8.1.13.v20130916-1\contexts\javadoc.xml
2020-04-27 18:03:47.413:INFO:oejd.DeploymentManager:Deployable added: D:\jetty-distribution-8.1.13.v20130916-1\contexts\test.xml
2020-04-27 18:03:47.508:INFO:oejw.WebInfConfiguration:Extract jar:file:/D:/jetty-distribution-8.1.13.v20130916-1/webapps/test.war!/ to C:\Users\edidada\AppData\Local\Temp\jetty-0.0.0.0-8109-test.war-_-any-\webapp
2020-04-27 18:03:49.967:INFO:oejs.TransparentProxy:TransparentProxy @ /javadoc-proxy to http://download.eclipse.org/jetty/stable-8/apidocs
2020-04-27 18:03:49.993:INFO:oejs.AbstractConnector:Started SelectChannelConnector@0.0.0.0:8109
ShutdownMonitorThread already started2020-04-27 18:03:49.994:INFO:oejs.Server:jetty-8.1.13.v20130916
Connected to server
[2020-04-27 06:03:50,077] Artifact springcxf:war: Artifact is being deployed, please wait...
2020-04-27 18:03:52.040:INFO:oejd.ContextDeployer:Deploy C:\Users\edidada\AppData\Local\Temp\context9209deploy\springcxf-1.0-SNAPSHOT.xml -> o.e.j.w.WebAppContext{/springcxf-1.0-SNAPSHOT,null},D:\git\github\springcxf\target\springcxf-1.0-SNAPSHOT.war
2020-04-27 18:03:52.107:INFO:oejw.WebInfConfiguration:Extract jar:file:/D:/git/github/springcxf/target/springcxf-1.0-SNAPSHOT.war!/ to D:\git\github\springcxf\target\springcxf-1.0-SNAPSHOT
2020-04-27 18:03:54.393:INFO:/.0-SNAPSHOT:No Spring WebApplicationInitializer types detected on classpath
2020-04-27 18:03:54.462:INFO:/.0-SNAPSHOT:Initializing Spring root WebApplicationContext
四月 27, 2020 6:03:54 下午 org.springframework.web.context.ContextLoader initWebApplicationContext
信息: Root WebApplicationContext: initialization started
四月 27, 2020 6:03:54 下午 org.springframework.context.support.AbstractApplicationContext prepareRefresh
信息: Refreshing Root WebApplicationContext: startup date [Mon Apr 27 18:03:54 CST 2020]; root of context hierarchy
四月 27, 2020 6:03:54 下午 org.springframework.beans.factory.xml.XmlBeanDefinitionReader loadBeanDefinitions
信息: Loading XML bean definitions from class path resource [spring.xml]
四月 27, 2020 6:03:54 下午 org.springframework.beans.factory.xml.XmlBeanDefinitionReader loadBeanDefinitions
信息: Loading XML bean definitions from class path resource [spring-cxf.xml]
四月 27, 2020 6:03:55 下午 org.apache.cxf.wsdl.service.factory.ReflectionServiceFactoryBean buildServiceFromClass
信息: Creating Service {http://impl.springcxf.wdidada.cn/}HelloServiceImpService from class cn.wdidada.springcxf.HelloService
四月 27, 2020 6:03:56 下午 org.apache.cxf.endpoint.ServerImpl initDestination
信息: Setting the server's publish address to be /hello
四月 27, 2020 6:03:56 下午 org.springframework.web.context.ContextLoader initWebApplicationContext
信息: Root WebApplicationContext: initialization completed in 1786 ms
[2020-04-27 06:03:56,500] Artifact springcxf:war: Artifact is deployed successfully
[2020-04-27 06:03:56,500] Artifact springcxf:war: Deploy took 6,423 milliseconds
四月 27, 2020 6:04:37 下午 org.apache.cxf.phase.PhaseInterceptorChain doDefaultLogging
警告: Interceptor for {http://impl.springcxf.wdidada.cn/}HelloServiceImpService has thrown exception, unwinding now
org.apache.cxf.binding.soap.SoapFault: Error reading XMLStreamReader: Undeclared namespace prefix "spr"
 at [row,col {unknown-source}]: [1,264]
	at org.apache.cxf.binding.soap.interceptor.StartBodyInterceptor.handleMessage(StartBodyInterceptor.java:65)
	at org.apache.cxf.binding.soap.interceptor.StartBodyInterceptor.handleMessage(StartBodyInterceptor.java:37)
	at org.apache.cxf.phase.PhaseInterceptorChain.doIntercept(PhaseInterceptorChain.java:308)
	at org.apache.cxf.transport.ChainInitiationObserver.onMessage(ChainInitiationObserver.java:121)
	at org.apache.cxf.transport.http.AbstractHTTPDestination.invoke(AbstractHTTPDestination.java:251)
	at org.apache.cxf.transport.servlet.ServletController.invokeDestination(ServletController.java:234)
	at org.apache.cxf.transport.servlet.ServletController.invoke(ServletController.java:208)
	at org.apache.cxf.transport.servlet.ServletController.invoke(ServletController.java:160)
	at org.apache.cxf.transport.servlet.CXFNonSpringServlet.invoke(CXFNonSpringServlet.java:180)
	at org.apache.cxf.transport.servlet.AbstractHTTPServlet.handleRequest(AbstractHTTPServlet.java:293)
	at org.apache.cxf.transport.servlet.AbstractHTTPServlet.doPost(AbstractHTTPServlet.java:212)
	at javax.servlet.http.HttpServlet.service(HttpServlet.java:755)
	at org.apache.cxf.transport.servlet.AbstractHTTPServlet.service(AbstractHTTPServlet.java:268)
	at org.eclipse.jetty.servlet.ServletHolder.handle(ServletHolder.java:686)
	at org.eclipse.jetty.servlet.ServletHandler.doHandle(ServletHandler.java:501)
	at org.eclipse.jetty.server.handler.ScopedHandler.handle(ScopedHandler.java:137)
	at org.eclipse.jetty.security.SecurityHandler.handle(SecurityHandler.java:533)
	at org.eclipse.jetty.server.session.SessionHandler.doHandle(SessionHandler.java:231)
	at org.eclipse.jetty.server.handler.ContextHandler.doHandle(ContextHandler.java:1086)
	at org.eclipse.jetty.servlet.ServletHandler.doScope(ServletHandler.java:428)
	at org.eclipse.jetty.server.session.SessionHandler.doScope(SessionHandler.java:193)
	at org.eclipse.jetty.server.handler.ContextHandler.doScope(ContextHandler.java:1020)
	at org.eclipse.jetty.server.handler.ScopedHandler.handle(ScopedHandler.java:135)
	at org.eclipse.jetty.server.handler.ContextHandlerCollection.handle(ContextHandlerCollection.java:255)
	at org.eclipse.jetty.server.handler.HandlerCollection.handle(HandlerCollection.java:154)
	at org.eclipse.jetty.server.handler.HandlerWrapper.handle(HandlerWrapper.java:116)
	at org.eclipse.jetty.server.Server.handle(Server.java:370)
	at org.eclipse.jetty.server.AbstractHttpConnection.handleRequest(AbstractHttpConnection.java:489)
	at org.eclipse.jetty.server.AbstractHttpConnection.content(AbstractHttpConnection.java:960)
	at org.eclipse.jetty.server.AbstractHttpConnection$RequestHandler.content(AbstractHttpConnection.java:1021)
	at org.eclipse.jetty.http.HttpParser.parseNext(HttpParser.java:865)
	at org.eclipse.jetty.http.HttpParser.parseAvailable(HttpParser.java:240)
	at org.eclipse.jetty.server.AsyncHttpConnection.handle(AsyncHttpConnection.java:82)
	at org.eclipse.jetty.io.nio.SelectChannelEndPoint.handle(SelectChannelEndPoint.java:668)
	at org.eclipse.jetty.io.nio.SelectChannelEndPoint$1.run(SelectChannelEndPoint.java:52)
	at org.eclipse.jetty.util.thread.QueuedThreadPool.runJob(QueuedThreadPool.java:608)
	at org.eclipse.jetty.util.thread.QueuedThreadPool$3.run(QueuedThreadPool.java:543)
	at java.lang.Thread.run(Thread.java:748)
Caused by: com.ctc.wstx.exc.WstxParsingException: Undeclared namespace prefix "spr"
 at [row,col {unknown-source}]: [1,264]
	at com.ctc.wstx.sr.StreamScanner.constructWfcException(StreamScanner.java:614)
	at com.ctc.wstx.sr.StreamScanner.throwParseError(StreamScanner.java:487)
	at com.ctc.wstx.sr.InputElementStack.resolveAndValidateElement(InputElementStack.java:505)
	at com.ctc.wstx.sr.BasicStreamReader.handleStartElem(BasicStreamReader.java:2979)
	at com.ctc.wstx.sr.BasicStreamReader.nextFromTree(BasicStreamReader.java:2839)
	at com.ctc.wstx.sr.BasicStreamReader.next(BasicStreamReader.java:1073)
	at org.apache.cxf.binding.soap.interceptor.StartBodyInterceptor.handleMessage(StartBodyInterceptor.java:59)
	... 37 more

四月 27, 2020 6:04:37 下午 org.apache.cxf.phase.PhaseInterceptorChain doDefaultLogging
警告: Interceptor for {http://impl.springcxf.wdidada.cn/}HelloServiceImpService has thrown exception, unwinding now
org.apache.cxf.binding.soap.SoapFault: Error reading XMLStreamReader: Undeclared namespace prefix "spr"
 at [row,col {unknown-source}]: [1,264]
	at org.apache.cxf.binding.soap.interceptor.StartBodyInterceptor.handleMessage(StartBodyInterceptor.java:65)
	at org.apache.cxf.binding.soap.interceptor.StartBodyInterceptor.handleMessage(StartBodyInterceptor.java:37)
	at org.apache.cxf.phase.PhaseInterceptorChain.doIntercept(PhaseInterceptorChain.java:308)
	at org.apache.cxf.transport.ChainInitiationObserver.onMessage(ChainInitiationObserver.java:121)
	at org.apache.cxf.transport.http.AbstractHTTPDestination.invoke(AbstractHTTPDestination.java:251)
	at org.apache.cxf.transport.servlet.ServletController.invokeDestination(ServletController.java:234)
	at org.apache.cxf.transport.servlet.ServletController.invoke(ServletController.java:208)
	at org.apache.cxf.transport.servlet.ServletController.invoke(ServletController.java:160)
	at org.apache.cxf.transport.servlet.CXFNonSpringServlet.invoke(CXFNonSpringServlet.java:180)
	at org.apache.cxf.transport.servlet.AbstractHTTPServlet.handleRequest(AbstractHTTPServlet.java:293)
	at org.apache.cxf.transport.servlet.AbstractHTTPServlet.doPost(AbstractHTTPServlet.java:212)
	at javax.servlet.http.HttpServlet.service(HttpServlet.java:755)
	at org.apache.cxf.transport.servlet.AbstractHTTPServlet.service(AbstractHTTPServlet.java:268)
	at org.eclipse.jetty.servlet.ServletHolder.handle(ServletHolder.java:686)
	at org.eclipse.jetty.servlet.ServletHandler.doHandle(ServletHandler.java:501)
	at org.eclipse.jetty.server.handler.ScopedHandler.handle(ScopedHandler.java:137)
	at org.eclipse.jetty.security.SecurityHandler.handle(SecurityHandler.java:533)
	at org.eclipse.jetty.server.session.SessionHandler.doHandle(SessionHandler.java:231)
	at org.eclipse.jetty.server.handler.ContextHandler.doHandle(ContextHandler.java:1086)
	at org.eclipse.jetty.servlet.ServletHandler.doScope(ServletHandler.java:428)
	at org.eclipse.jetty.server.session.SessionHandler.doScope(SessionHandler.java:193)
	at org.eclipse.jetty.server.handler.ContextHandler.doScope(ContextHandler.java:1020)
	at org.eclipse.jetty.server.handler.ScopedHandler.handle(ScopedHandler.java:135)
	at org.eclipse.jetty.server.handler.ContextHandlerCollection.handle(ContextHandlerCollection.java:255)
	at org.eclipse.jetty.server.handler.HandlerCollection.handle(HandlerCollection.java:154)
	at org.eclipse.jetty.server.handler.HandlerWrapper.handle(HandlerWrapper.java:116)
	at org.eclipse.jetty.server.Server.handle(Server.java:370)
	at org.eclipse.jetty.server.AbstractHttpConnection.handleRequest(AbstractHttpConnection.java:489)
	at org.eclipse.jetty.server.AbstractHttpConnection.content(AbstractHttpConnection.java:960)
	at org.eclipse.jetty.server.AbstractHttpConnection$RequestHandler.content(AbstractHttpConnection.java:1021)
	at org.eclipse.jetty.http.HttpParser.parseNext(HttpParser.java:865)
	at org.eclipse.jetty.http.HttpParser.parseAvailable(HttpParser.java:235)
	at org.eclipse.jetty.server.AsyncHttpConnection.handle(AsyncHttpConnection.java:82)
	at org.eclipse.jetty.io.nio.SelectChannelEndPoint.handle(SelectChannelEndPoint.java:668)
	at org.eclipse.jetty.io.nio.SelectChannelEndPoint$1.run(SelectChannelEndPoint.java:52)
	at org.eclipse.jetty.util.thread.QueuedThreadPool.runJob(QueuedThreadPool.java:608)
	at org.eclipse.jetty.util.thread.QueuedThreadPool$3.run(QueuedThreadPool.java:543)
	at java.lang.Thread.run(Thread.java:748)
Caused by: com.ctc.wstx.exc.WstxParsingException: Undeclared namespace prefix "spr"
 at [row,col {unknown-source}]: [1,264]
	at com.ctc.wstx.sr.StreamScanner.constructWfcException(StreamScanner.java:614)
	at com.ctc.wstx.sr.StreamScanner.throwParseError(StreamScanner.java:487)
	at com.ctc.wstx.sr.InputElementStack.resolveAndValidateElement(InputElementStack.java:505)
	at com.ctc.wstx.sr.BasicStreamReader.handleStartElem(BasicStreamReader.java:2979)
	at com.ctc.wstx.sr.BasicStreamReader.nextFromTree(BasicStreamReader.java:2839)
	at com.ctc.wstx.sr.BasicStreamReader.next(BasicStreamReader.java:1073)
	at org.apache.cxf.binding.soap.interceptor.StartBodyInterceptor.handleMessage(StartBodyInterceptor.java:59)
	... 37 more

```



c#



https://www.cnblogs.com/chenghu/p/5249737.html

