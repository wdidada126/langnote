# springmvc



- 配置文件applicationContext.xml和xxx-servlet.xml
- 基于servlet
- 竞品 淘宝 webx


在Spring MVC中，HandlerMapping是一个非常重要的接口，它的主要作用是将HTTP请求映射到对应的Controller处理器。当DispatcherServlet接收到一个HTTP请求时，会首先通过HandlerMapping接口来查找合适的Controller处理器，然后再将请求交给对应的Controller进行处理。

HandlerMapping接口定义了一个方法：getHandler(HttpServletRequest request)，该方法返回一个HandlerExecutionChain对象，其中包含了一个Controller对象以及一些HandlerInterceptor对象，这些对象可以协同工作来处理HTTP请求。

在Spring MVC中，常见的HandlerMapping实现类有：

BeanNameUrlHandlerMapping：根据URL路径中的Bean名称来查找对应的Controller。

DefaultAnnotationHandlerMapping：根据Controller中的注解来映射URL请求。

SimpleUrlHandlerMapping：根据URL路径来映射Controller。

RequestMappingHandlerMapping：根据Controller方法上的@RequestMapping注解来映射URL请求。

其中，RequestMappingHandlerMapping是最常用的HandlerMapping实现类，它支持多种URL请求映射方式，包括基于URL路径、HTTP请求方法、请求参数等方式。

在HandlerMapping的实现中，需要注意的是映射顺序的问题。由于存在多个HandlerMapping实现类，它们可能会产生冲突，导致无法正确地将HTTP请求映射到对应的Controller。因此，在配置HandlerMapping时，需要仔细考虑映射顺序，以保证每个请求都能正确地被处理。









在Spring MVC中，FrameServlet是整个Spring MVC的入口，它的主要作用是将所有的HTTP请求转发到对应的Controller中进行处理。但是，Spring MVC中的Controller不是一个普通的Java类，而是需要通过IoC容器创建并管理的，也就是说，Spring MVC中的Controller是一个Bean，需要由Spring容器管理。

而DispatchServlet的作用则是扩展了FrameServlet的功能。它作为Spring MVC框架的核心控制器，负责接收所有的HTTP请求，并根据配置信息将请求转发到相应的Controller处理。与FrameServlet不同的是，DispatchServlet可以直接通过Spring容器获取到Controller的实例，从而省去了手动创建Controller实例的步骤。此外，DispatchServlet还支持HandlerMapping、HandlerAdapter等多种机制，可以更加方便地实现URL到Controller方法的映射。

另外，DispatchServlet还支持模板引擎的解析，将Controller处理的数据渲染到模板中返回给用户。DispatchServlet还提供了拦截器机制，可以通过拦截器对请求进行统一的预处理和后处理，例如权限校验、日志记录等。

综上所述，DispatchServlet不仅继承了FrameServlet的基本功能，还扩展了Spring MVC框架的很多重要功能。因此，在Spring MVC框架中同时使用FrameServlet和DispatchServlet，可以更加方便地管理和处理HTTP请求，并实现更加灵活和高效的Web开发。












在Spring MVC中，HandlerExecutionChain是一个包含HandlerInterceptor和Controller对象的类，它的主要作用是将HTTP请求与Controller以及HandlerInterceptor绑定起来，实现请求的处理和拦截功能。
当DispatcherServlet接收到一个HTTP请求时，首先会通过HandlerMapping查找到对应的HandlerExecutionChain对象，然后通过HandlerExecutionChain中的HandlerInterceptor对象对请求进行预处理，最终将请求交给对应的Controller进行处理。在请求处理完成后，DispatcherServlet会再次通过HandlerExecutionChain中的HandlerInterceptor对象对响应进行后处理，以实现全局的拦截功能。
HandlerExecutionChain类的主要属性包括：
Object handler：表示请求对应的Controller对象。
List<HandlerInterceptor> interceptors：表示请求对应的HandlerInterceptor对象列表，可以实现请求的预处理和后处理功能。
int interceptorIndex：表示当前请求所处的HandlerInterceptor对象的位置，用于控制请求拦截器的执行顺序。
在HandlerExecutionChain中，HandlerInterceptor对象的执行顺序由interceptorIndex属性决定。当DispatcherServlet接收到一个HTTP请求时，会依次执行HandlerInterceptor对象列表中的preHandle方法，直到所有的HandlerInterceptor对象都执行完毕或者有一个HandlerInterceptor对象返回false为止。在请求处理完成后，DispatcherServlet会再次依次执行HandlerInterceptor对象列表中的postHandle方法和afterCompletion方法，完成请求的后处理工作。
总之，HandlerExecutionChain在Spring MVC中扮演着非常重要的角色，它可以将Controller对象和HandlerInterceptor对象绑定在一起，实现请求的处理和拦截功能，为Web应用程序的开发提供了非常方便和灵活的机制。




springmvc全局异常处理器
要知道全局异常处理，SpringMVC提供了两种方式：
实现HandlerExceptionResolver接口，自定义异常处理器。

使用HandlerExceptionResolver接口的子类，也就是SpringMVC提供的异常处理器。
可以看出有四种：
DefaultHandlerExceptionResolver，默认的异常处理器。根据各个不同类型的异常，返回不同的异常视图。
SimpleMappingExceptionResolver，简单映射异常处理器。通过配置异常类和view的关系来解析异常。
ResponseStatusExceptionResolver，状态码异常处理器。解析带有@ResponseStatus注释类型的异常。
ExceptionHandlerExceptionResolver，注解形式的异常处理器。对@ExceptionHandler注解的方法进行异常解析。
https://mp.weixin.qq.com/s/licKK-8n9N6LNWEkTtj-Aw


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


springweb

- RestTemplate
- AsyncRestTemplate

自带http客户端


spring 源码分析 CommonsMultipartFile 如何base64解码
https://blog.csdn.net/qq_41615095/article/details/80781933
https://blog.csdn.net/weixin_42319989/article/details/102504418



精尽Spring MVC源码分析 - MultipartResolver 组件
https://www.cnblogs.com/lifullmoon/p/14136982.html


```java
public interface MultipartResolver {
    /**
     * 是否为 multipart 请求
     */
    boolean isMultipart(HttpServletRequest request);
    /**
     * 将 HttpServletRequest 请求封装成 MultipartHttpServletRequest 对象
     */
    MultipartHttpServletRequest resolveMultipart(HttpServletRequest request) throws MultipartException;

    /**
     * 清理处理 multipart 产生的资源，例如临时文件
     */
    void cleanupMultipart(MultipartHttpServletRequest request);
}
```

```java
public interface MultipartRequest {
    Iterator<String> getFileNames();
    MultipartFile getFile(String name);
    List<MultipartFile> getFiles(String name);
    Map<String, MultipartFile> getFileMap();
    MultiValueMap<String, MultipartFile> getMultiFileMap();
    String getMultipartContentType(String paramOrFileName);
}
```



org.springframework.web.multipart.support.StandardMultipartHttpServletRequest.StandardMultipartFile#transferTo



    at org.springframework.http.client.SimpleBufferingClientHttpRequest.executeInternal(SimpleBufferingClientHttpRequest.java:78)
    at org.springframework.http.client.AbstractBufferingClientHttpRequest.executeInternal(AbstractBufferingClientHttpRequest.java:48)
    at org.springframework.http.client.AbstractClientHttpRequest.execute(AbstractClientHttpRequest.java:53)
    at org.springframework.web.client.RestTemplate.doExecute(RestTemplate.java:652)


RestTemplate 可以使用Netty实现

```java
    Bootstrap bootstrap = new Bootstrap();
    bootstrap.group(this.eventLoopGroup).channel(NioSocketChannel.class)
            .handler(new ChannelInitializer<SocketChannel>() {
                @Override
                protected void initChannel(SocketChannel channel) throws Exception {
                    configureChannel(channel.config());
                    ChannelPipeline pipeline = channel.pipeline();
                    if (isSecure) {
                        Assert.notNull(sslContext, "sslContext should not be null");
                        pipeline.addLast(sslContext.newHandler(channel.alloc(), uri.getHost(), uri.getPort()));
                    }
                    pipeline.addLast(new HttpClientCodec());
                    pipeline.addLast(new HttpObjectAggregator(maxResponseSize));
                    if (readTimeout > 0) {
                        pipeline.addLast(new ReadTimeoutHandler(readTimeout,
                                TimeUnit.MILLISECONDS));
                    }
                }
            });
```