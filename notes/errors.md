# error

[id: 0x56973676, /10.0.75.1:3676 => /10.0.75.1:20800], dubbo version: 2.5.8, current host: 10.0.75.1
768373 [ZkClient-EventThread-82-127.0.0.1:2181] INFO  com.alibaba.dubbo.rpc.protocol.dubbo.DubboProtocol  -  [DUBBO] disconected from /10.0.75.1:20800,url:dubbo://10.0.75.1:20800/com.xxxx.media.platform.isomerization.proxy.api.IsomerizationAccessService?anyhost=true&application=test-isomerization-proxy&check=false&codec=dubbo&dispatcher=message&dubbo=2.5.8&generic=false&heartbeat=60000&interface=com.xxxx.media.platform.isomerization.proxy.api.IsomerizationAccessService&methods=access,accessHttp&pid=19644&register.ip=10.0.75.1&remote.timestamp=1565871967455&revision=1.7.0&side=consumer&timestamp=1565872042449, dubbo version: 2.5.8, current host: 10.0.75.1

Caused by: 
java.lang.ClassNotFoundException: org.apache.commons.fileupload.FileItemFactory
	at java.net.URLClassLoader.findClass(URLClassLoader.java:381)
	at java.lang.ClassLoader.loadClass(ClassLoader.java:424)
	at java.lang.ClassLoader.loadClass(ClassLoader.java:357)
	at org.eclipse.jetty.webapp.WebAppClassLoader.loadClass(WebAppClassLoader.java:430)
	at org.eclipse.jetty.webapp.WebAppClassLoader.loadClass(WebAppClassLoader.java:383)
	at java.lang.Class.getDeclaredMethods0(Native Method)
	at java.lang.Class.privateGetDeclaredMethods(Class.java:2701)
	at java.lang.Class.getDeclaredMethods(Class.java:1975)
	at org.springframework.util.ReflectionUtils.getDeclaredMethods(ReflectionUtils.java:613)
	at org.springframework.util.ReflectionUtils.doWithMethods(ReflectionUtils.java:524)
	at org.springframework.util.ReflectionUtils.doWithMethods(ReflectionUtils.java:510)
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor.determineCandidateConstructors(AutowiredAnnotationBeanPostProcessor.java:247)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.determineConstructorsFromBeanPostProcessors(AbstractAutowireCapableBeanFactory.java:1118)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBeanInstance(AbstractAutowireCapableBeanFactory.java:1091)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.doCreateBean(AbstractAutowireCapableBeanFactory.java:513)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBean(AbstractAutowireCapableBeanFactory.java:483)
	at org.springframework.beans.factory.support.AbstractBeanFactory$1.getObject(AbstractBeanFactory.java:306)
	at org.springframework.beans.factory.support.DefaultSingletonBeanRegistry.getSingleton(DefaultSingletonBeanRegistry.java:230)
	at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:302)
	at org.springframework.beans.factory.support.AbstractBeanFactory.getBean(AbstractBeanFactory.java:197)
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.preInstantiateSingletons(DefaultListableBeanFactory.java:761)
	at org.springframework.context.support.AbstractApplicationContext.finishBeanFactoryInitialization(AbstractApplicationContext.java:867)
	at org.springframework.context.support.AbstractApplicationContext.refresh(AbstractApplicationContext.java:543)
	at org.springframework.web.servlet.FrameworkServlet.configureAndRefreshWebApplicationContext(FrameworkServlet.java:668)
	at org.springframework.web.servlet.FrameworkServlet.createWebApplicationContext(FrameworkServlet.java:634)
	at org.springframework.web.servlet.FrameworkServlet.createWebApplicationContext(FrameworkServlet.java:682)
	at org.springframework.web.servlet.FrameworkServlet.initWebApplicationContext(FrameworkServlet.java:553)
	at org.springframework.web.servlet.FrameworkServlet.initServletBean(FrameworkServlet.java:494)
	at org.springframework.web.servlet.HttpServletBean.init(HttpServletBean.java:171)
	at javax.servlet.GenericServlet.init(GenericServlet.java:244)
	at org.eclipse.jetty.servlet.ServletHolder.initServlet(ServletHolder.java:534)
	at org.eclipse.jetty.servlet.ServletHolder.doStart(ServletHolder.java:346)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.servlet.ServletHandler.initialize(ServletHandler.java:786)
	at org.eclipse.jetty.servlet.ServletContextHandler.startContext(ServletContextHandler.java:265)


```

Caused by: org.springframework.beans.PropertyBatchUpdateException: Failed properties: Property 'name' threw exception; nested exception is java.lang.IllegalStateException: Invalid name="${dubbo.applicationName}" contain illegal charactor, only digit, letter, '-', '_' and '.' is legal.
	at org.springframework.beans.AbstractPropertyAccessor.setPropertyValues(AbstractPropertyAccessor.java:121) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.AbstractPropertyAccessor.setPropertyValues(AbstractPropertyAccessor.java:75) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.applyPropertyValues(AbstractAutowireCapableBeanFactory.java:1564) ~[spring-beans-4.3.12.RELEASE.jar:4.3.12.RELEASE]
	... 35 more

```

```

java.lang.ClassNotFoundException: org.apache.commons.fileupload.FileItemFactory
	at java.net.URLClassLoader.findClass(URLClassLoader.java:381)
	at java.lang.ClassLoader.loadClass(ClassLoader.java:424)
	at java.lang.ClassLoader.loadClass(ClassLoader.java:357)
	at org.eclipse.jetty.webapp.WebAppClassLoader.loadClass(WebAppClassLoader.java:430)
	at org.eclipse.jetty.webapp.WebAppClassLoader.loadClass(WebAppClassLoader.java:383)
	at java.lang.Class.getDeclaredMethods0(Native Method)
	at java.lang.Class.privateGetDeclaredMethods(Class.java:2701)
	at java.lang.Class.getDeclaredMethods(Class.java:1975)
	at org.springframework.util.ReflectionUtils.getDeclaredMethods(ReflectionUtils.java:613)
	at org.springframework.util.ReflectionUtils.doWithMethods(ReflectionUtils.java:524)
	at org.springframework.util.ReflectionUtils.doWithMethods(ReflectionUtils.java:510)
	at org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor.determineCandidateConstructors(AutowiredAnnotationBeanPostProcessor.java:247)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.determineConstructorsFromBeanPostProcessors(AbstractAutowireCapableBeanFactory.java:1118)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBeanInstance(AbstractAutowireCapableBeanFactory.java:1091)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.doCreateBean(AbstractAutowireCapableBeanFactory.java:513)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBean(AbstractAutowireCapableBeanFactory.java:483)
	at org.springframework.beans.factory.support.AbstractBeanFactory$1.getObject(AbstractBeanFactory.java:306)
	at org.springframework.beans.factory.support.DefaultSingletonBeanRegistry.getSingleton(DefaultSingletonBeanRegistry.java:230)
	at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:302)
	at org.springframework.beans.factory.support.AbstractBeanFactory.getBean(AbstractBeanFactory.java:197)
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.preInstantiateSingletons(DefaultListableBeanFactory.java:761)
	at org.springframework.context.support.AbstractApplicationContext.finishBeanFactoryInitialization(AbstractApplicationContext.java:867)
	at org.springframework.context.support.AbstractApplicationContext.refresh(AbstractApplicationContext.java:543)
	at org.springframework.web.servlet.FrameworkServlet.configureAndRefreshWebApplicationContext(FrameworkServlet.java:668)
	at org.springframework.web.servlet.FrameworkServlet.createWebApplicationContext(FrameworkServlet.java:634)
	at org.springframework.web.servlet.FrameworkServlet.createWebApplicationContext(FrameworkServlet.java:682)
	at org.springframework.web.servlet.FrameworkServlet.initWebApplicationContext(FrameworkServlet.java:553)
	at org.springframework.web.servlet.FrameworkServlet.initServletBean(FrameworkServlet.java:494)
	at org.springframework.web.servlet.HttpServletBean.init(HttpServletBean.java:171)
	at javax.servlet.GenericServlet.init(GenericServlet.java:244)
	at org.eclipse.jetty.servlet.ServletHolder.initServlet(ServletHolder.java:534)
	at org.eclipse.jetty.servlet.ServletHolder.doStart(ServletHolder.java:346)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.servlet.ServletHandler.initialize(ServletHandler.java:786)
	at org.eclipse.jetty.servlet.ServletContextHandler.startContext(ServletContextHandler.java:265)
	at org.eclipse.jetty.webapp.WebAppContext.startContext(WebAppContext.java:1242)
	at org.eclipse.jetty.server.handler.ContextHandler.doStart(ContextHandler.java:717)
	at org.eclipse.jetty.webapp.WebAppContext.doStart(WebAppContext.java:494)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:64)
	at org.eclipse.jetty.deploy.ContextDeployer.deploy(ContextDeployer.java:359)
	at org.eclipse.jetty.deploy.ContextDeployer.access$000(ContextDeployer.java:82)
	at org.eclipse.jetty.deploy.ContextDeployer$ScannerListener.fileAdded(ContextDeployer.java:107)
	at org.eclipse.jetty.util.Scanner.reportAddition(Scanner.java:615)
	at org.eclipse.jetty.util.Scanner.reportDifferences(Scanner.java:540)
	at org.eclipse.jetty.util.Scanner.scan(Scanner.java:403)
	at org.eclipse.jetty.util.Scanner$1.run(Scanner.java:353)

```
