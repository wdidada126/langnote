# hikari


<<<<<<< HEAD

```
target\classes\spring\spring-hikari.xml]: Bean instantiation via constructor failed; nested exception is org.springframework.beans.BeanInstantiationException: Failed to instantiate [com.zaxxer.hikari.HikariDataSource]: Constructor threw exception; nested exception is com.zaxxer.hikari.pool.HikariPool$PoolInitializationException: Failed to initialize pool
```



 通过端口 1433 连接到主机 172.17.16.62 的 TCP/IP 连接失败。错误:“connect timed out。请验证连接属性。确保 SQL Server 的实例正在主机上运行，且在此端口接受 TCP/IP 连接，还要确保防火墙没有阻止到此端口的 TCP 连接。”。


```shell
at org.springframework.beans.factory.support.ConstructorResolver.createArgumentArray(ConstructorResolver.java:749)
=======
target\classes\spring\spring-hikari.xml]: Bean instantiation via constructor failed; nested exception is org.springframework.beans.BeanInstantiationException: Failed to instantiate [com.zaxxer.hikari.HikariDataSource]: Constructor threw exception; nested exception is com.zaxxer.hikari.pool.HikariPool$PoolInitializationException: Failed to initialize pool: 通过端口 1433 连接到主机 172.17.16.62 的 TCP/IP 连接失败。错误:“connect timed out。请验证连接属性。确保 SQL Server 的实例正在主机上运行，且在此端口接受 TCP/IP 连接，还要确保防火墙没有阻止到此端口的 TCP 连接。”。


```shell

	at org.springframework.beans.factory.support.ConstructorResolver.createArgumentArray(ConstructorResolver.java:749)
>>>>>>> afe522da082020e5ece0b75c43067644b2edb768
	at org.springframework.beans.factory.support.ConstructorResolver.autowireConstructor(ConstructorResolver.java:189)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.autowireConstructor(AbstractAutowireCapableBeanFactory.java:1193)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBeanInstance(AbstractAutowireCapableBeanFactory.java:1095)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.doCreateBean(AbstractAutowireCapableBeanFactory.java:513)
	at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.createBean(AbstractAutowireCapableBeanFactory.java:483)
	at org.springframework.beans.factory.support.AbstractBeanFactory$1.getObject(AbstractBeanFactory.java:306)
	at org.springframework.beans.factory.support.DefaultSingletonBeanRegistry.getSingleton(DefaultSingletonBeanRegistry.java:230)
	at org.springframework.beans.factory.support.AbstractBeanFactory.doGetBean(AbstractBeanFactory.java:302)
	at org.springframework.beans.factory.support.AbstractBeanFactory.getBean(AbstractBeanFactory.java:197)
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.preInstantiateSingletons(DefaultListableBeanFactory.java:761)
	at org.springframework.context.support.AbstractApplicationContext.finishBeanFactoryInitialization(AbstractApplicationContext.java:867)
	at org.springframework.context.support.AbstractApplicationContext.refresh(AbstractApplicationContext.java:543)
	at org.springframework.test.context.web.AbstractGenericWebContextLoader.loadContext(AbstractGenericWebContextLoader.java:134)
	at org.springframework.test.context.web.AbstractGenericWebContextLoader.loadContext(AbstractGenericWebContextLoader.java:61)
	at org.springframework.test.context.support.AbstractDelegatingSmartContextLoader.delegateLoading(AbstractDelegatingSmartContextLoader.java:108)
	at org.springframework.test.context.support.AbstractDelegatingSmartContextLoader.loadContext(AbstractDelegatingSmartContextLoader.java:251)
	at org.springframework.test.context.cache.DefaultCacheAwareContextLoaderDelegate.loadContextInternal(DefaultCacheAwareContextLoaderDelegate.java:98)
	at org.springframework.test.context.cache.DefaultCacheAwareContextLoaderDelegate.loadContext(DefaultCacheAwareContextLoaderDelegate.java:116)
<<<<<<< HEAD
=======

>>>>>>> afe522da082020e5ece0b75c43067644b2edb768
```







