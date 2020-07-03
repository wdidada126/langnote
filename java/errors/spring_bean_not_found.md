## spring bean 

```java
Exception in thread "main" org.springframework.beans.factory.NoSuchBeanDefinitionException: No qualifying bean of type 'io.shardingsphere.example.repository.mybatis.service.SpringBlogPojoService' available
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.getBean(DefaultListableBeanFactory.java:352)
	at org.springframework.beans.factory.support.DefaultListableBeanFactory.getBean(DefaultListableBeanFactory.java:339)
	at org.springframework.context.support.AbstractApplicationContext.getBean(AbstractApplicationContext.java:1092)
	at io.shardingsphere.example.spring.boot.mybatis.orche.SpringBootStarterExample.getBlogCommonService(SpringBootStarterExample.java:63)
	at io.shardingsphere.example.spring.boot.mybatis.orche.SpringBootStarterExample.process(SpringBootStarterExample.java:45)
	at io.shardingsphere.example.spring.boot.mybatis.orche.SpringBootStarterExample.main(SpringBootStarterExample.java:40)
```