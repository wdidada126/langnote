# springmvc

2023-03-27 02:05:11.405  WARN 2236 --- [nio-9990-exec-4] .w.s.m.s.DefaultHandlerExceptionResolver : Resolved exception caused by handler execution: org.springframework.web.HttpRequestMethodNotSupportedException: Request method 'GET' not supported


public String @ResponseBody xxx(){

    return new MyPOLO();
}

MyPOLO对象如何序列化成json格式的

https://blog.csdn.net/qq_43842093/article/details/124769772
通过 @RestController 注解实现，此时所有的方法都将会被添加 @ResponseBody 注解
@ResponseBody 通过各种类型转换器实现数据的转换，如将数据转换为 String、JSON、XML 等格式。并将数据写入到 response body 中。而且它们使用的都是 UTF-8 编码。

MappingJackson2HttpMessageConverter
MappingJackson2HttpMessageConverter是springboot中默认的Json消息转换器
https://blog.csdn.net/Heron22/article/details/109512976
消息转换器创建和生效原理
springboot Web项目中有两个重要的配置类需要知道。
一个是springmvc的原生配置类：WebMvcConfigurationSupport
另一个是springboot为springmvc写的自动配置类：WebMvcAutoConfiguration


SpringMVC默认包含一系列的数据转换器，此处不一一列举，就介绍几种常用的：
MappingJackson2XmlHttpMessageConverter 基于Jackson的XML转换器，能够将对象转换成XML格式的数据
MappingJackson2HttpMessageConverter 基于 Jackson 的JSON转换器，能够将对象转换成JSON格式的数据
GsonHttpMessageConverter 基于Gson的JSON转换器，能够将对象转换成JSON格式数据
因为SpringMVC在项目初始化时，会去扫描系统中的JAR包，然后根据扫描到的JAR包设置默认的转换类型，大概的扫描过程是：
1）检查系统中是否存在jackson-xml的JAR包，如果存在，就将数据转换类型列表中设置XML类型，以及其对应的转换器
2）检查系统中是否存在jackson-json的JAR包，如果存在，就在数据转换类型列表中设置JSON类型，以及其对应的转换器

因为是先检测的XML，因此XML排在JSON前面，如果系统两者的JAR包都存在，那么默认情况下数据会被转换成XML格式
————————————————
版权声明：本文为CSDN博主「Java后端何哥」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/CSDN2497242041/article/details/102618226


springmvc返回对象或集合
（1）我们可以通过SpringMVC帮助我们对对象集合进行json字符串的转换并回写

首先，需要在spring-mvc.xml中做出如下配置，配置处理器映射器

    <!--配置处理器映射器-->
    <bean class="org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter">
        <property name="messageConverters">
            <list>
                <bean class="org.springframework.http.converter.json.MappingJackson2HttpMessageConverter"/>
            </list>
        </property>
    </bean>
而后，直接返回对象就可以，即可返回json格式字符串

    @RequestMapping("/quick10")
    @ResponseBody
    public User save10()  {
 
        User user = new User();
        user.setAge(18);
        user.setName("xiaoming");
        return user;
    }
（2）我们可以利用MVC的注解驱动代码代替上述配置
在spring-mvc.xml下进行MVC注解驱动

<!--MVC注解驱动-->
<mvc:annotation-driven/>
————————————————
版权声明：本文为CSDN博主「m0_55247145」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/m0_55247145/article/details/120930590




spring-webmvc 这个jar包

handleradapter
运行时的对象
RequestMappingHandlerAdapter



Object handler强制转换成(HandlerMethod) handler


九大组件：
1、HandlerMapping   SimpleUrlHandlerMapping BeanNameUrlHandlerMapping RequestMappingHandlerMapping
2、HandlerAdapter
3、HandlerExceptionResolver   DefaultHandlerExceptionResolver
4、viewResolver
5、RequestToViewNameTranslator
6、LocalResolver
7、ThemeResolver
8、MultiPartResolver
9、FlashMapManager

// 初始化 MultipartResolver:主要用来处理文件上传.如果定义过当前类型的bean对象，那么直接获取，如果没有的话，可以为null
initMultipartResolver(context);
// 初始化 LocaleResolver:主要用来处理国际化配置,基于URL参数的配置(AcceptHeaderLocaleResolver)，基于session的配置(SessionLocaleResolver)，基于cookie的配置(CookieLocaleResolver)
initLocaleResolver(context);
// 初始化 ThemeResolver:主要用来设置主题Theme
initThemeResolver(context);
// 初始化 HandlerMapping:映射器，用来将对应的request跟controller进行对应
initHandlerMappings(context);
// 初始化 HandlerAdapter:处理适配器，主要包含Http请求处理器适配器，简单控制器处理器适配器，注解方法处理器适配器
initHandlerAdapters(context);
// 初始化 HandlerExceptionResolver:基于HandlerExceptionResolver接口的异常处理
initHandlerExceptionResolvers(context);
// 初始化 RequestToViewNameTranslator:当controller处理器方法没有返回一个View对象或逻辑视图名称，并且在该方法中没有直接往response的输出流里面写数据的时候，spring将会采用约定好的方式提供一个逻辑视图名称
initRequestToViewNameTranslator(context);
// 初始化 ViewResolver: 将ModelAndView选择合适的视图进行渲染的处理器
initViewResolvers(context);
// 初始化 FlashMapManager: 提供请求存储属性，可供其他请求使用
initFlashMapManager(context);





SpringMvc定义Controller有三种方式：
1、注解 @Controller
2、实现Controller接口
3、实现HttpRequestHandler
第二种和第三种实现Controller必须在配置文件中定义bean信息，定义的名称必须加上"/"

org.springframework.web.HttpRequestHandler 接口

ResourceHttpRequestHandler (org.springframework.web.servlet.resource)
DefaultServletHttpRequestHandler (org.springframework.web.servlet.resource)
HttpInvokerServiceExporter (org.springframework.remoting.httpinvoker)
BurlapServiceExporter (org.springframework.remoting.caucho)
HessianServiceExporter (org.springframework.remoting.caucho)

该HandlerMapping实际使用类为SimpleUrlHandlerMapping



@Controller修饰的类是如何注册到SimpleUrlHandlerMapping
https://blog.51cto.com/u_15651175/5545208



Spring MVC有三种映射策略

| 映射策略            | 实现类                       |
| ------------------- | ---------------------------- |
| 简单url映射         | SimpleUrlHandlerMapping      |
| BeanName映射        | BeanNameUrlHandlerMapping    |
| @RequestMapping映射 | RequestMappingHandlerMapping |



- 配置文件applicationContext.xml和xxx-servlet.xml
- 基于servlet
- 竞品 淘宝 webx



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
        return "main";//跳转到到main.jsp页面，如果main.jsp不存在，error页面
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