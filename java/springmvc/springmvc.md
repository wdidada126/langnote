# springmvc



- 配置文件applicationContext.xml和xxx-servlet.xml
- 基于servlet
- 竞品 淘宝 webx





问题：

applicationContext.xml和xxx-servlet.xml的区别

都是bean配置文件，有层级关系

https://www.cnblogs.com/parryyang/p/5783399.html



20200115 写个servlet 访问不了，相对路径没有映射到SprinhMVC



1.index.jsp访问不了，增加jstl依赖
<mvc:default-servlet-handler/>

2.Controller还是访问不了

<mvc:annotation-driven/>

如何理解servlet web.xml和springmvc的关系



配置项？

3. http路径没有映射到spring系统上，如何处理？

https://github.com/edidada/springmvccurl

配置了一个http路径失效，配置controler失效？

查看有哪些Handler

？？？？






通过@PathVariable获取路径中的参数



[idea工程中web.xml报错Servlet should have a mapping](https://www.cnblogs.com/yadongliang/p/7755071.html)

idea工程中web.xml报错

[Servlet should have a mapping](https://www.cnblogs.com/yadongliang/p/7755071.html)


```
<dependency>
    <groupId>org.springframework</groupId>
    <artifactId>spring-webmvc</artifactId>
    <version>4.2.9.RELEASE</version>
</dependency>
```

No Spring WebApplicationInitializer types detected on classpath

https://stackoverflow.com/questions/16321819/no-spring-webapplicationinitializer-types-detected-on-classpath

在web.xml中定义servlet
DispatchServlet



- SpringMVC设置URL是是否包括项目名


SpringMVC接收参数的原理

https://blog.csdn.net/u013041642/article/details/72611065

```java


    @RequestMapping("/")
    public String index(){
        return "main";//跳转到error页面
    }
	
	
    @RequestMapping("/")
    public @ResponseBody String index(){
        return "main";//返回的http body到
    }

```


```java

	<bean
		class="org.springframework.web.servlet.view.InternalResourceViewResolver">
		<property name="prefix" value="/WEB-INF/jsp/"></property>
		<property name="suffix" value=".jsp"></property>
		<property name="viewClass" value = "org.springframework.web.servlet.view.JstlView"></property>
	</bean>

```

```java

<<<<<<< HEAD
Mapped "{[/healthcheck.html]}" onto public java.lang.Object com.xxx.medium.test.isomerization.proxy.web.MainController.healthCheck()
=======
Mapped "{[/healthcheck.html]}" onto public java.lang.Object com.xxxxxx.medium.test.isomerization.proxy.web.MainController.healthCheck()
>>>>>>> afe522da082020e5ece0b75c43067644b2edb768
Mapped "{[/healthcheck_test.html]}" onto public java.lang.Object com.xxxxxx.medium.test.isomerization.proxy.web.MainController.healthChecks()
Mapped "{[/healthcheck_image_extraction.html]}" onto public java.lang.Object com.xxxxxx.medium.test.isomerization.proxy.web.TestImageExtractionController.healthChecks()

```

Spring MVC中的两个context（上下文）

主要配置项：
<context-param>和<listener>:配置Spring的RootContext，对应配置文件为root-context.xml
<servlet>和<servlet-mapping>：配置Spring的WebContext，对应配置文件默认为为WEB-INF/{servlet-name}-servlet.xml

https://blog.csdn.net/suifeng3051/article/details/51596511



在Spring3.0以后，SpringMVC便支持Java Validation API了，Java Validation API提供了一些注解来约束对象属性值，这些注解有：

```
注解	解释
@AssertFalse	The annotated element must be a Boolean type and be false.
@AssertTrue	The annotated element must be a Boolean type and be true.
@DecimalMax	The annotated element must be a number whose value is less than or equal toa given BigDecimalString value.
@DecimalMin	The annotated element must be a number whose value is greater than orequal to a given BigDecimalString value.
@Digits	The annotated element must be a number whose value has a specified number of digits.
@Future	The value of the annotated element must be a date in the future.
@Max	The annotated element must be a number whose value is less than or equal to a given value.
@Min	The annotated element must be a number whose value is greater than or equal to a given value.
@NotNull	The value of the annotated element must not be null.
@Null	The value of the annotated element must be null.
@Past	The value of the annotated element must be a date in the past.
@Pattern	The value of the annotated element must match a given regular expression.
@Size	The value of the annotated element must be either a String, a collection, or an array whose length fits within the given range.

```
https://blog.csdn.net/suifeng3051/article/details/51596511


https://blog.csdn.net/qq_36769100/article/details/71746449



```shell

healthCheckController
org.springframework.context.annotation.internalConfigurationAnnotationProcessor
org.springframework.context.annotation.internalAutowiredAnnotationProcessor
org.springframework.context.annotation.internalRequiredAnnotationProcessor
org.springframework.context.annotation.internalCommonAnnotationProcessor
org.springframework.context.event.internalEventListenerProcessor
org.springframework.context.event.internalEventListenerFactory
org.springframework.context.support.PropertySourcesPlaceholderConfigurer#0
test-isomerization-proxy
com.alibaba.dubbo.config.RegistryConfig
dubbo
isomerizationAccessService
com.alibaba.dubbo.config.spring.AnnotationBean
mvcContentNegotiationManager
org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerMapping
mvcCorsConfigurations
org.springframework.format.support.FormattingConversionServiceFactoryBean#0
org.springframework.validation.beanvalidation.OptionalValidatorFactoryBean#0
org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter
mvcUriComponentsContributor
org.springframework.web.servlet.handler.MappedInterceptor#0
org.springframework.web.servlet.mvc.method.annotation.ExceptionHandlerExceptionResolver#0
org.springframework.web.servlet.mvc.annotation.ResponseStatusExceptionResolver#0
org.springframework.web.servlet.mvc.support.DefaultHandlerExceptionResolver#0
org.springframework.web.servlet.handler.BeanNameUrlHandlerMapping
org.springframework.web.servlet.mvc.HttpRequestHandlerAdapter
org.springframework.web.servlet.mvc.SimpleControllerHandlerAdapter
mvcHandlerMappingIntrospector
multipartResolver
org.springframework.aop.config.internalAutoProxyCreator
org.springframework.format.support.FormattingConversionServiceFactoryBean#1
org.springframework.validation.beanvalidation.OptionalValidatorFactoryBean#1
org.springframework.web.servlet.handler.MappedInterceptor#1
org.springframework.web.servlet.mvc.method.annotation.ExceptionHandlerExceptionResolver#1
org.springframework.web.servlet.mvc.annotation.ResponseStatusExceptionResolver#1
org.springframework.web.servlet.mvc.support.DefaultHandlerExceptionResolver#1
testPostRowServiceImpl

```







```
org.springframework.web.bind.annotation.ExceptionHandler
```





ExceptionHandler



Spring异常处理@ExceptionHandler

https://www.cnblogs.com/shuimuzhushui/p/6791600.html





org.springframework.web.bind.annotation.CrossOrigin



Spring Framework 4.2 GA为CORS提供了第一类支持，使您比通常的基于过滤器的解决方案更容易和更强大地配置它。所以springMVC的版本要在4.2或以上版本才支持@CrossOrigin



https://www.cnblogs.com/mmzs/p/9167743.html



20200405 写个servlet 访问不了，相对路径没有映射到SprinhMVC







https://segmentfault.com/a/1190000010203210

springmvc

listener fileter servlet按照这三个顺序去启动的

Spring MVC默认每个Controller是单例

https://zhuanlan.zhihu.com/p/70768325



handlermap

handleradaptor

moduleAndview



