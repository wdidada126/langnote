# spring_web

DispatcherServlet.properties 文件中HandlerAdapter的内容
```
org.springframework.web.servlet.HandlerAdapter=org.springframework.web.servlet.mvc.HttpRequestHandlerAdapter,\
	org.springframework.web.servlet.mvc.SimpleControllerHandlerAdapter,\
	org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter,\
	org.springframework.web.servlet.function.support.HandlerFunctionAdapter
```


四个处理器适配器（HandlerAdapter）的作用和适用范围如下：

1. `HttpRequestHandlerAdapter`：用于处理`HttpRequestHandler`接口的实现类，这种实现方式通常用于处理静态资源文件、文件下载等请求。
2. `SimpleControllerHandlerAdapter`：用于处理旧式的控制器实现，如`Controller`接口和`AbstractController`类。这种实现方式已过时，不建议再使用。
3. `RequestMappingHandlerAdapter`：是Spring MVC框架中的默认适配器，用于处理使用注解方式定义的控制器方法。它支持使用注解处理器（Annotation-based Handler Method）和HTTP消息转换器（HTTP Message Converter），能够将请求参数转换为方法参数，将方法返回值转换为响应消息。`RequestMappingHandlerAdapter`还支持异步请求处理、文件上传等高级特性。
4. `HandlerFunctionAdapter`：用于处理WebFlux框架中的函数式处理器（Handler Function）。`HandlerFunctionAdapter`将一个函数式处理器转换为一个处理器（Handler），并将其注册到WebFlux框架中。
需要注意的是，以上处理器适配器的使用和适用范围是不同的。在Spring MVC框架中，通常只需要使用`RequestMappingHandlerAdapter`即可。在WebFlux框架中，使用`HandlerFunctionAdapter`处理函数式处理器比较常见。`HttpRequestHandlerAdapter`和`SimpleControllerHandlerAdapter`的使用较为少见，仅在某些特定场景下使用。

HandlerFunctionAdapter对应
org.springframework.web.servlet.function.HandlerFunction接口

RequestMappingHandlerAdapter  org.springframework.web.method.HandlerMethod

HandlerMethodArgumentResolver hmar
spring-web这个jar下面的接口
public interface HandlerMethodArgumentResolver {
    boolean supportsParameter(MethodParameter parameter);

    @Nullable
    Object resolveArgument(MethodParameter parameter, @Nullable ModelAndViewContainer mavContainer, NativeWebRequest webRequest, @Nullable WebDataBinderFactory binderFactory) throws Exception;
}

springmvc自带的一些实现：
ServletRequestMethodArgumentResolver和ServletResponseMethodArgumentResolver处理了自动绑定HttpServletRequest和HttpServletResponse
RequestParamMapMethodArgumentResolver处理了@RequestParam
RequestHeaderMapMethodArgumentResolver处理了@RequestHeader
PathVariableMapMethodArgumentResolver处理了@PathVariable
ModelAttributeMethodProcessor处理了@ModelAttribute
RequestResponseBodyMethodProcessor处理了@RequestBody
https://www.cnblogs.com/wangjing666/p/10770726.html


https://tomcat.apache.org/lists.html
dev-subscribe@tomcat.apache.org

debug tomcat source code
https://blog.csdn.net/wangjunjie0817/article/details/102944338
https://juejin.cn/post/6844903859828031501



org.springframework.beans.factory.Aware

Spring实现Aware接口，完成对IOC容器的感知
https://blog.csdn.net/ilovejava_2010/article/details/7953582

BeanNameAware，可以在Bean中得到它在IOC容器中的Bean的实例的名字。
BeanFactoryAware，可以在Bean中得到Bean所在的IOC容器，从而直接在Bean中使用IOC容器的服务。
ApplicationContextAware，可以在Bean中得到Bean所在的应用上下文，从而直接在Bean中使用上下文的服务。
MessageSourceAware，在Bean中可以得到消息源。
ApplicationEventPublisherAware，在bean中可以得到应用上下文的事件发布器，从而可以在Bean中发布应用上下文的事件。
ResourceLoaderAware，在Bean中可以得到ResourceLoader，从而在bean中使用ResourceLoader加载外部对应的Resource资源。
ImportAware
EmbeddedValueResolverAware
EnvironmentAware
BootstrapContextAware
BeanClassLoaderAware
LoadTimeWeaverAware
NotificationPublisherAware
ServletConfigAware




MapMethodProcessor (org.springframework.web.method.annotation)
SortArgumentResolver (org.springframework.data.web)
    SortHandlerMethodArgumentResolver (org.springframework.data.web)
        HateoasSortHandlerMethodArgumentResolver (org.springframework.data.web)
ErrorsMethodArgumentResolver (org.springframework.web.method.annotation)
PathVariableMapMethodArgumentResolver (org.springframework.web.servlet.mvc.method.annotation)
AbstractNamedValueMethodArgumentResolver (org.springframework.web.method.annotation)
    RequestHeaderMethodArgumentResolver (org.springframework.web.method.annotation)
    RequestAttributeMethodArgumentResolver (org.springframework.web.servlet.mvc.method.annotation)
    RequestParamMethodArgumentResolver (org.springframework.web.method.annotation)
    AbstractCookieValueMethodArgumentResolver (org.springframework.web.method.annotation)
        ServletCookieValueMethodArgumentResolver (org.springframework.web.servlet.mvc.method.annotation)
    ExpressionValueMethodArgumentResolver (org.springframework.web.method.annotation)
    SessionAttributeMethodArgumentResolver (org.springframework.web.servlet.mvc.method.annotation)
    MatrixVariableMethodArgumentResolver (org.springframework.web.servlet.mvc.method.annotation)
    PathVariableMethodArgumentResolver (org.springframework.web.servlet.mvc.method.annotation)
RequestHeaderMapMethodArgumentResolver (org.springframework.web.method.annotation)
ModelMethodProcessor (org.springframework.web.method.annotation)
ModelAttributeMethodProcessor (org.springframework.web.method.annotation)
    ServletModelAttributeMethodProcessor (org.springframework.web.servlet.mvc.method.annotation)
    ProxyingHandlerMethodArgumentResolver (org.springframework.data.web)
ServletResponseMethodArgumentResolver (org.springframework.web.servlet.mvc.method.annotation)
SessionStatusMethodArgumentResolver (org.springframework.web.method.annotation)
RequestParamMapMethodArgumentResolver (org.springframework.web.method.annotation)
PrincipalMethodArgumentResolver (org.springframework.web.servlet.mvc.method.annotation)
ContinuationHandlerMethodArgumentResolver (org.springframework.web.servlet.mvc.method.annotation)
AbstractMessageConverterMethodArgumentResolver (org.springframework.web.servlet.mvc.method.annotation)
    RequestPartMethodArgumentResolver (org.springframework.web.servlet.mvc.method.annotation)
    AbstractMessageConverterMethodProcessor (org.springframework.web.servlet.mvc.method.annotation)
        RequestResponseBodyMethodProcessor (org.springframework.web.servlet.mvc.method.annotation)
        HttpEntityMethodProcessor (org.springframework.web.servlet.mvc.method.annotation)
AbstractWebArgumentResolverAdapter (org.springframework.web.method.annotation)
    ServletWebArgumentResolverAdapter (org.springframework.web.servlet.mvc.method.annotation)
PageableArgumentResolver (org.springframework.data.web)
    PageableHandlerMethodArgumentResolver (org.springframework.data.web)
PagedResourcesAssemblerArgumentResolver (org.springframework.data.web)
UriComponentsBuilderMethodArgumentResolver (org.springframework.web.servlet.mvc.method.annotation)
HandlerMethodArgumentResolverComposite (org.springframework.web.method.support)
ServletRequestMethodArgumentResolver (org.springframework.web.servlet.mvc.method.annotation)
RedirectAttributesMethodArgumentResolver (org.springframework.web.servlet.mvc.method.annotation)
MatrixVariableMapMethodArgumentResolver (org.springframework.web.servlet.mvc.method.annotation)
QuerydslPredicateArgumentResolver (org.springframework.data.web.querydsl)



RequestParamMapMethodArgumentResolver rp ear



ModelAndViewContainer


函数调用栈
org.springframework.web.method.support.InvocableHandlerMethod#invokeForRequest()

这个函数很重要

HandlerAdapter接口有handle方法

org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter#handleInternal



#### HandlerMethod类详解
org.springframework.web.method.HandlerMethod


属性列表
private final Object bean; 就是@Controller修饰的类，在Spring ioc容器中

private final MethodParameter[] parameters;

org.springframework.core.MethodParameter

org.springframework.web.method.HandlerMethod#resolvedFromHandlerMethod

ServletWebRequest
org.springframework.web.context.request.ServletWebRequest
`ServletWebRequest`是Spring MVC框架中的一个类，它封装了一个Servlet请求和响应，并提供了一些方法来访问和操作请求和响应的各种属性。
`ServletWebRequest`的主要作用是为`HandlerMethod`和`HandlerInterceptor`等处理器提供对Servlet请求和响应的访问和操作。通过`ServletWebRequest`，处理器可以获取请求的URL、HTTP方法、请求参数、请求头、Cookie、Session等信息，也可以设置响应的状态码、响应头、Cookie等信息，以及向响应中写入内容。
`ServletWebRequest`还提供了一些方便的方法来获取请求参数、请求头、Cookie和Session等常用的属性。例如，可以使用`getParameter()`方法获取请求参数，使用`getHeader()`方法获取请求头，使用`getCookies()`方法获取Cookie，使用`getSession()`方法获取Session等。
此外，`ServletWebRequest`还提供了一些方法来操作请求和响应的状态和属性。例如，可以使用`getResponse()`方法获取响应对象，然后使用响应对象的`setStatus()`方法设置响应状态码，使用`addHeader()`方法添加响应头，使用`addCookie()`方法添加Cookie等。


DefaultDataBinderFactory (org.springframework.web.bind.support)
    InitBinderDataBinderFactory (org.springframework.web.method.annotation)
        ServletRequestDataBinderFactory (org.springframework.web.servlet.mvc.method.annotation)


真实运行http项目的

GenericFilter (javax.servlet)
    RemoteIpFilter (org.apache.catalina.filters)
    CorsFilter (org.apache.catalina.filters)
    HttpFilter (javax.servlet.http)
    WsFilter (org.apache.tomcat.websocket.server)
    RequestDumperFilter (org.apache.catalina.filters)
    WebdavFixFilter (org.apache.catalina.filters)
CompositeFilter (org.springframework.web.filter)
SessionInitializerFilter (org.apache.catalina.filters)
WebStatFilter (com.alibaba.druid.support.http)
ServletFilterProxy in MockFilterChain (org.springframework.mock.web)
FilterBase (org.apache.catalina.filters)
    RemoteCIDRFilter (org.apache.catalina.filters)
    FailedRequestFilter (org.apache.catalina.filters)
    RequestFilter (org.apache.catalina.filters)
        RemoteHostFilter (org.apache.catalina.filters)
        RemoteAddrFilter (org.apache.catalina.filters)
    CsrfPreventionFilterBase (org.apache.catalina.filters)
        CsrfPreventionFilter (org.apache.catalina.filters)
        RestCsrfPreventionFilter (org.apache.catalina.filters)
    SetCharacterEncodingFilter (org.apache.catalina.filters)
    ExpiresFilter (org.apache.catalina.filters)
    AddDefaultCharsetFilter (org.apache.catalina.filters)
    HttpHeaderSecurityFilter (org.apache.catalina.filters)
PatternMappingFilterProxy (org.springframework.test.web.servlet.setup)
ErrorPageFilter (org.springframework.boot.web.servlet.support)
OrderedFilter (org.springframework.boot.web.servlet.filter)
    OrderedFormContentFilter (org.springframework.boot.web.servlet.filter)
    OrderedHiddenHttpMethodFilter (org.springframework.boot.web.servlet.filter)
    OrderedRequestContextFilter (org.springframework.boot.web.servlet.filter)
    OrderedCharacterEncodingFilter (org.springframework.boot.web.servlet.filter)
GenericFilterBean (org.springframework.web.filter)
    DelegatingFilterProxy (org.springframework.web.filter)
        Anonymous in DelegatingFilterProxyRegistrationBean (org.springframework.boot.web.servlet)
    ResourceUrlEncodingFilter (org.springframework.web.servlet.resource)
    OncePerRequestFilter (org.springframework.web.filter)
        CharacterEncodingFilter (org.springframework.web.filter)
        HiddenHttpMethodFilter (org.springframework.web.filter)
        HttpPutFormContentFilter (org.springframework.web.filter)
        RelativeRedirectFilter (org.springframework.web.filter)
        CorsFilter (org.springframework.web.filter)
        RequestContextFilter (org.springframework.web.filter)
        ApplicationContextHeaderFilter (org.springframework.boot.web.servlet.filter)
        ForwardedHeaderFilter (org.springframework.web.filter)
        FormContentFilter (org.springframework.web.filter)
        MultipartFilter (org.springframework.web.multipart.support)
        ShallowEtagHeaderFilter (org.springframework.web.filter)
        AbstractRequestLoggingFilter (org.springframework.web.filter)
        Anonymous in ErrorPageFilter (org.springframework.boot.web.servlet.support)
StatViewFilter (com.alibaba.druid.support.http)
LoggerContextFilter (ch.qos.logback.classic.selector.servlet)
MDCInsertingServletFilter (ch.qos.logback.classic.helpers)


javax.servlet.Filter

Filters are configured in the deployment descriptor of a web application
Examples that have been identified for this design are 
1) Authentication Filters 
2) Logging and Auditing Filters 
3) Image conversion Filters 
4) Data compression Filters 
5) Encryption Filters 
6) Tokenizing Filters 
7) Filters that trigger resource access events 
8) XSL/T filters 
9) Mime-type chain Filter 



org.springframework.web.servlet.DispatcherServlet类有属性
private List<HandlerAdapter> handlerAdapters;


BeanPropertyBindingResult
DirectFieldBindingResult 区别

`BeanPropertyBindingResult`和`DirectFieldBindingResult`都是Spring框架中用于封装数据绑定结果的类，它们主要是用于处理表单提交或其他HTTP请求的数据绑定操作。它们的主要区别在于数据绑定的方式和绑定的对象类型。

`BeanPropertyBindingResult`类是`org.springframework.validation.BeanPropertyBindingResult`的子类，它是通过JavaBean属性来进行数据绑定的。当使用Spring MVC框架进行表单提交时，通常会使用`BeanPropertyBindingResult`来封装表单数据绑定的结果。

`DirectFieldBindingResult`类是`org.springframework.validation.DirectFieldBindingResult`的子类，它是通过直接绑定字段来进行数据绑定的。当需要手动进行数据绑定操作时，通常会使用`DirectFieldBindingResult`来封装绑定结果。

具体来说，它们的区别如下：

1. 绑定方式：`BeanPropertyBindingResult`使用JavaBean属性来进行数据绑定，而`DirectFieldBindingResult`使用直接绑定字段来进行数据绑定。

2. 绑定对象类型：`BeanPropertyBindingResult`主要用于绑定JavaBean对象，而`DirectFieldBindingResult`可以用于绑定任何类型的对象。

3. 错误信息：`BeanPropertyBindingResult`会将错误信息绑定到对象的属性中，而`DirectFieldBindingResult`会将错误信息绑定到对象的字段中。

4. 错误类型：`BeanPropertyBindingResult`会在绑定错误时抛出`MethodArgumentNotValidException`异常，而`DirectFieldBindingResult`会在绑定错误时抛出`BindException`异常。

总的来说，`BeanPropertyBindingResult`和`DirectFieldBindingResult`都是用于封装数据绑定结果的类，它们的使用方式和适用场景有所不同。`BeanPropertyBindingResult`适用于需要绑定JavaBean对象的情况，而`DirectFieldBindingResult`适用于需要手动绑定任何类型的对象的情况。


HandlerMethodArgumentResolverComposite作用

`HandlerMethodArgumentResolverComposite`是Spring MVC框架中用于处理方法参数的解析器的复合类。它主要用于将一个或多个`HandlerMethodArgumentResolver`解析器组合在一起，以便在处理请求时调用多个解析器来解析方法参数。

在Spring MVC框架中，当一个请求被路由到一个控制器方法时，框架会使用`HandlerMethodArgumentResolver`解析器来解析方法的参数，并将解析结果传递给方法进行处理。`HandlerMethodArgumentResolver`解析器是一个接口，它定义了用于解析方法参数的方法。Spring MVC框架提供了许多内置的`HandlerMethodArgumentResolver`解析器，例如`RequestParamMethodArgumentResolver`、`ModelMethodArgumentResolver`等。
`HandlerMethodArgumentResolverComposite`类是多个`HandlerMethodArgumentResolver`解析器的复合类，它会将多个解析器组合在一起，以便在处理请求时调用多个解析器来解析方法参数。当处理请求时，`HandlerMethodArgumentResolverComposite`会按照解析器的顺序依次调用每个解析器，直到找到一个能够解析当前方法参数的解析器为止。如果没有找到匹配的解析器，则会抛出异常。

以下是`HandlerMethodArgumentResolverComposite`类的主要作用：
1. 组合多个`HandlerMethodArgumentResolver`解析器，以便在处理请求时调用多个解析器来解析方法参数。
2. 管理解析器的顺序，按照顺序依次调用每个解析器，直到找到一个能够解析当前方法参数的解析器为止。
3. 提供`addResolver()`和`addResolvers()`方法，用于向复合解析器中添加解析器。
4. 提供`getResolvers()`方法，用于获取当前复合解析器中包含的所有解析器。
总的来说，`HandlerMethodArgumentResolverComposite`类是Spring MVC框架中用于处理方法参数的解析器的复合类，它是多个`HandlerMethodArgumentResolver`解析器的组合，用于在处理请求时调用多个解析器来解析方法参数。





org.springframework.web.method.HandlerMethod.HandlerMethodParameter



org.springframework.web.servlet.mvc.method.annotation.AbstractMessageConverterMethodArgumentResolver#readWithMessageConverters(org.springframework.http.HttpInputMessage, org.springframework.core.MethodParameter, java.lang.reflect.Type)
这个方法调用MappingJackson2HttpMessageConverter转换数据

MappingJackson2HttpMessageConverter  实现了抽象类AbstractJackson2HttpMessageConverter


jackson的类
com.fasterxml.jackson.databind.JavaType
    com.fasterxml.jackson.databind.type.SimpleType



javax.validation.Valid

    @PostMapping({"/ddd"})
    public ResponseEntity<Object> queryXXX(@RequestBody @Valid XXRequest xxrequest, BindingResult result);


ErrorsMethodArgumentResolver
org.springframework.web.method.annotation.ErrorsMethodArgumentResolver


你好，这是 Bing。根据我的搜索结果，springmvc代码如何校验http body，把校验结果封装在 BindingResult result上的源码解析如下：
- 当控制器方法中使用 @Valid 或 @Validated 注解时，Spring MVC 会调用 RequestResponseBodyMethodProcessor 这个参数解析器来处理请求体中的参数¹²。
- RequestResponseBodyMethodProcessor 会使用 HttpMessageConverter 来将请求体中的内容转换为 Java 对象，并使用 WebDataBinder 来进行属性绑定和校验¹²。
- WebDataBinder 会遍历当前参数的所有注解，如果注解是 @Validated 或注解的名字以 ‘Valid’ 开头，则使用 Validator 对象来执行校验逻辑¹²。
- Validator 对象会使用 Bean Validation API 来对参数对象的所有字段进行校验，如果有错误，会将错误信息添加到 BindingResult 对象中¹²³。
- BindingResult 对象会被保存到 ModelAndViewContainer 对象中，以便后续使用¹²。
- 当控制器方法中有 BindingResult 类型的参数时，Spring MVC 会调用 ErrorsMethodArgumentResolver 这个参数解析器来处理该参数¹²。
- ErrorsMethodArgumentResolver 会从 ModelAndViewContainer 对象中获取 BindingResult 对象，并赋值给该参数¹²。
- BindingResult 参数必须紧跟在被校验的参数后面，否则会抛出 IllegalStateException 异常¹²。

希望这些信息对你有帮助。😊

源: 与必应的对话， 2023/6/7
(1) Spring5源码解析-使用@Valid进行Spring验证 - 知乎 - 知乎专栏. https://zhuanlan.zhihu.com/p/28577417.
(2) SpringMvc @Validated注解执行原理 - 知乎 - 知乎专栏. https://zhuanlan.zhihu.com/p/116916974.
(3) springmvc的@Validated/@Valid注解使用和BindingResult bindingResult - 穆晟铭 - 博客园. https://www.cnblogs.com/achengmu/p/9071343.html.




org.springframework.web.method.annotation.ErrorsMethodArgumentResolver#resolveArgument
方法
lastKey值为
org.springframework.validation.BindingResult.xxrequest

ModelAndViewContainer类属性defaultModel
	private final ModelMap defaultModel = new BindingAwareModelMap();

org.springframework.validation.support.BindingAwareModelMap

这个map在这个方法里面增加kv数据
org.springframework.web.method.support.ModelAndViewContainer#addAttribute(java.lang.String, java.lang.Object)


k是BindingResult.MODEL_KEY_PREFIX + name


org.springframework.web.bind.support.DefaultDataBinderFactory#createBinder


ExtendedServletRequestDataBinder

getBindingResult()








WebBindingInitializer接口
ConfigurableWebBindingInitializer实现类





是否直接报错吗？下面这个方法？
org.springframework.web.servlet.mvc.method.annotation.AbstractMessageConverterMethodArgumentResolver#isBindExceptionRequired


真正执行校验的方法

org.springframework.web.servlet.mvc.method.annotation.AbstractMessageConverterMethodArgumentResolver#validateIfApplicable
org.springframework.validation.DataBinder#validate(java.lang.Object...)

生成绑定结果
org.springframework.validation.DataBinder#createBeanPropertyBindingResult

### springmvc @RestController返回结果
org.springframework.http.converter.json.AbstractJackson2HttpMessageConverter#getJavaType也被调用



HttpEntityMethodProcessor

org.springframework.web.servlet.mvc.method.annotation.HttpEntityMethodProcessor

HttpEntity

