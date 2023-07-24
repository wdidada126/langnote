# spring_webmvc


org.springframework.web.servlet.DispatcherServlet
org.springframework.web.servlet.FrameworkServlet



HandlerExecutionChain

这个也是重点类

MvcNamespaceHandler





| org.springframework.web.servlet | 类型      | 说明                                                         |
| ------------------------------- | --------- | ------------------------------------------------------------ |
| Interfaces                      |           |                                                              |
| AsyncHandlerInterceptor         | interface | extends HandlerInterceptor      void afterConcurrentHandlingStarted(HttpServletRequest request, HttpServletResponse response,  Object handler) |
| FlashMapManager                 | interface | saveOutputFlashMap(FlashMap flashMap, HttpServletRequest request, HttpServletResponse response)  FlashMap retrieveAndUpdate(HttpServletRequest request, HttpServletResponse response) |
| **HandlerAdapter**              | interface | ModelAndView handle(HttpServletRequest request, HttpServletResponse response, Object handler)  boolean supports(Object handler) |
| HandlerExceptionResolver        | interface | ModelAndView resolveException(       HttpServletRequest request, HttpServletResponse response, @Nullable Object handler, Exception ex); |
| HandlerInterceptor              | interface | preHandle() postHandle() afterCompletion()                   |
| HandlerMapping                  | interface | 处理器映射 url跟java对象的方法关联起来 HandlerExecutionChain getHandler(HttpServletRequest request)  还有常量 MATRIX_VARIABLES_ATTRIBUTE，见下面 |
| LocaleContextResolver           | interface | extends LocaleResolver    LocaleContext resolveLocaleContext(HttpServletRequest request) void setLocaleContext(HttpServletRequest request, @Nullable HttpServletResponse response,       @Nullable LocaleContext localeContext) |
| LocaleResolver                  | interface | 关联类 LocaleContext LocaleContextHolder                     |
| RequestToViewNameTranslator     | interface | String getViewName(HttpServletRequest request)  实现类DefaultRequestToViewNameTranslator |
| SmartView                       | interface | extends View  方法boolean isRedirectView();                  |
| ThemeResolver                   | interface | String resolveThemeName(HttpServletRequest request) void setThemeName(HttpServletRequest request, @Nullable HttpServletResponse response, @Nullable String themeName) |
| View                            | interface | *RESPONSE_STATUS_ATTRIBUTE*  *PATH_VARIABLES* *PATH_VARIABLES* *SELECTED_CONTENT_TYPE*常量 String getContentType() void render(@Nullable Map<String, ?> model, HttpServletRequest request, HttpServletResponse response) |
| ViewResolver                    | interface | View resolveViewName(String viewName, Locale locale) 实现类见下面 |
|                                 |           |                                                              |
| Classes                         |           |                                                              |
| DispatcherServlet               |           | public class DispatcherServlet extends FrameworkServlet EXCEPTION_ATTRIBUTE FLASH_MAP_MANAGER_ATTRIBUTE FLASH_MAP_MANAGER_BEAN_NAME HANDLER_ADAPTER_BEAN_NAME HANDLER_EXCEPTION_RESOLVER_BEAN_NAME HANDLER_MAPPING_BEAN_NAME INPUT_FLASH_MAP_ATTRIBUTE  LOCALE_RESOLVER_ATTRIBUTE LOCALE_RESOLVER_BEAN_NAME MULTIPART_RESOLVER_BEAN_NAME OUTPUT_FLASH_MAP_ATTRIBUTE PAGE_NOT_FOUND_LOG_CATEGORY pageNotFoundLogger REQUEST_TO_VIEW_NAME_TRANSLATOR_BEAN_NAME THEME_RESOLVER_ATTRIBUTE THEME_RESOLVER_BEAN_NAME THEME_SOURCE_ATTRIBUTE VIEW_RESOLVER_BEAN_NAME WEB_APPLICATION_CONTEXT_ATTRIBUTE |
| FlashMap                        |           | 继承HashMap<String, Object> implements Comparable<FlashMap>  |
| FrameworkServlet                | abstract  | 继承HttpServletBean，implements ApplicationContextAware 实现类DispatcherServlet   DEFAULT_NAMESPACE_SUFFIX DEFAULT_CONTEXT_CLASS SERVLET_CONTEXT_PREFIX INIT_PARAM_DELIMITERS  属性，见下面  protected abstract void doService(HttpServletRequest request, HttpServletResponse response) 抽象方法，子类需要实现 |
| HandlerExecutionChain           |           | applyPreHandle() applyPostHandle() triggerAfterCompletion() applyAfterConcurrentHandlingStarted()见下面  在org.springframework.web.servlet.DispatcherServlet#doDispatch()方法中被调用 |
| HttpServletBean                 | abstract  | 子类见下面  implements EnvironmentCapable, EnvironmentAware  |
| ModelAndView                    |           | 四个属性 Object view; ModelMap model;HttpStatus status;boolean cleared = false; |
|                                 |           |                                                              |
| Exceptions                      |           |                                                              |
| ModelAndViewDefiningException   | exception |                                                              |
| NoHandlerFoundException         | exception |                                                              |



HandlerAdapter HandlerExceptionResolver 都返回ModuleAndView




ViewResolver接口实现类

ViewResolverComposite (org.springframework.web.servlet.view)
AbstractCachingViewResolver (org.springframework.web.servlet.view)
    ResourceBundleViewResolver (org.springframework.web.servlet.view)
    XmlViewResolver (org.springframework.web.servlet.view)
    UrlBasedViewResolver (org.springframework.web.servlet.view)
        TilesViewResolver (org.springframework.web.servlet.view.tiles3)
        ScriptTemplateViewResolver (org.springframework.web.servlet.view.script)
        InternalResourceViewResolver (org.springframework.web.servlet.view)
        XsltViewResolver (org.springframework.web.servlet.view.xslt)
        AbstractTemplateViewResolver (org.springframework.web.servlet.view)
            MustacheViewResolver (org.springframework.boot.web.servlet.view)
            GroovyMarkupViewResolver (org.springframework.web.servlet.view.groovy)
            FreeMarkerViewResolver (org.springframework.web.servlet.view.freemarker)
ContentNegotiatingViewResolver (org.springframework.web.servlet.view)
StaticViewResolver in StandaloneMockMvcBuilder (org.springframework.test.web.servlet.setup)
BeanNameViewResolver (org.springframework.web.servlet.view)





1. **DEFAULT_NAMESPACE_SUFFIX**

该属性定义了 Spring MVC 框架默认的命名空间后缀，默认值为 `/`。

2. **DEFAULT_CONTEXT_CLASS**

该属性定义了 Spring MVC 框架默认的上下文类，默认值为 `org.springframework.web.context.WebApplicationContext`。

3. **SERVLET_CONTEXT_PREFIX**

该属性定义了 Spring MVC 框架中 Servlet 上下文的名称前缀，默认值为 `servletContext`。

4. **INIT_PARAM_DELIMITERS**

该属性定义了 Spring MVC 框架中 Servlet 初始化参数的分隔符，默认值为 `=`。

以下是这四个属性的使用场景：

* **DEFAULT_NAMESPACE_SUFFIX**：如果您在 Spring MVC 框架中使用了自定义的命名空间，那么您可以通过设置该属性来指定自定义的命名空间后缀。
* **DEFAULT_CONTEXT_CLASS**：如果您在 Spring MVC 框架中使用了自定义的上下文类，那么您可以通过设置该属性来指定自定义的上下文类。
* **SERVLET_CONTEXT_PREFIX**：如果您在 Spring MVC 框架中使用了自定义的 Servlet 上下文名称，那么您可以通过设置该属性来指定自定义的 Servlet 上下文名称。
* **INIT_PARAM_DELIMITERS**：如果您在 Spring MVC 框架中使用了自定义的 Servlet 初始化参数分隔符，那么您可以通过设置该属性来指定自定义的 Servlet 初始化参数分隔符。



HttpServletBean子类

GenericServlet (javax.servlet)
    HttpServlet (javax.servlet.http)
        HttpServletBean (org.springframework.web.servlet)
            FrameworkServlet (org.springframework.web.servlet)
                DispatcherServlet (org.springframework.web.servlet)
                    TestDispatcherServlet (org.springframework.test.web.servlet)





HandlerExecutionChain在Spring MVC中代表处理器执行链,包含处理器、拦截器等信息。它定义了四个方法:

1. applyPreHandle():调用处理器拦截器的preHandle方法。

- 使用场景:请求进入处理器前调用,常用于请求检查、准备等工作。

2. applyPostHandle():调用处理器拦截器的postHandle方法。

- 使用场景:请求处理后但视图渲染前调用,可用于清理工作。

3. triggerAfterCompletion():调用处理器拦截器的afterCompletion方法。

- 使用场景:整个请求处理完成后调用,进行最后清理工作。

4. applyAfterConcurrentHandlingStarted():调用异步处理开始时的回调。

- 使用场景:异步处理先后顺序需要控制的场景。

这些方法将拦截器链和处理器连接起来,使得拦截器可以介入处理流程的多个点,实现功能增强等目的。

配合拦截器使用,可以处理更多业务需求。



MatchableHandlerMapping (org.springframework.web.servlet.handler)
    RequestMappingHandlerMapping (org.springframework.web.servlet.mvc.method.annotation)
    AbstractUrlHandlerMapping (org.springframework.web.servlet.handler)
AbstractHandlerMapping (org.springframework.web.servlet.handler)
    AbstractUrlHandlerMapping (org.springframework.web.servlet.handler)
        AbstractDetectingUrlHandlerMapping (org.springframework.web.servlet.handler)
            BeanNameUrlHandlerMapping (org.springframework.web.servlet.handler)
        SimpleUrlHandlerMapping (org.springframework.web.servlet.handler)
        WelcomePageHandlerMapping (org.springframework.boot.autoconfigure.web.servlet)
    AbstractHandlerMethodMapping (org.springframework.web.servlet.handler)
        RequestMappingInfoHandlerMapping (org.springframework.web.servlet.mvc.method)
            RequestMappingHandlerMapping (org.springframework.web.servlet.mvc.method.annotation)
    RouterFunctionMapping (org.springframework.web.servlet.function.support)



AbstractHandlerMapping 类的，子类实现

protected abstract Object getHandlerInternal(HttpServletRequest request)



在Spring框架中,BeanFactoryUtils类提供了多种操作BeanFactory的工具方法。

其中beansOfTypeIncludingAncestors方法的作用是获取BeanFactory中指定类型的所有bean,包括从父级工厂继承的bean。

方法签名:

```java
public static <T> Map<String, T> beansOfTypeIncludingAncestors(ListableBeanFactory lbf, Class<T> type, boolean includeNonSingletons, boolean allowEagerInit)
```

参数说明:

- lbf: bean工厂
- type: 要获取的bean的类型
- includeNonSingletons: 是否包含prototype类型的bean
- allowEagerInit: 是否初始化lazy-init的bean

返回值:

返回指定类型的所有bean映射,key为bean名称,value为bean实例。

该方法通过遍历当前工厂及其所有父级工厂中的bean,筛选出指定类型的bean后返回。usefulll获取同一类型的所有bean实例。

例如可以用来获取所有@Repository bean,进行某种统一处理。





DispatcherServlet是Spring MVC的核心servlet,它主要协调Spring MVC的9大组件:

1. HandlerMapping:请求映射器,根据请求找到对应的Handler。

2. HandlerAdapter:处理适配器,执行Handler并处理返回值。 

3. HandlerExceptionResolver:异常解析器,处理 Handler 执行过程中的异常。

4. ViewResolver:视图解析器,将逻辑视图解析为实际视图对象。 

5. LocaleResolver:区域解析器,解析客户端语言环境。

6. ThemeResolver:主题解析器,解析页面主题。

7. MultipartResolver:文件上传解析器,支持文件上传。

8. FlashMapManager:FlashMap管理器,支持重定向数据传递。 

9. RequestToViewNameTranslator:请求到视图名转换器。

DispatcherServlet使用这些组件协同工作,实现核心的派发处理流程:

1. 接收请求,交给HandlerMapping查找对应Handler。 

2. HandlerAdapter调用Handler执行并处理返回值。

3. 将逻辑视图解析成实际视图。

4. 渲染模型数据,返回响应。

DispatcherServlet将流程连接起来,实现MVC核心功能。





initMultipartResolver(context);
initLocaleResolver(context);
initThemeResolver(context);
initHandlerMappings(context);
initHandlerAdapters(context);
initHandlerExceptionResolvers(context);
initRequestToViewNameTranslator(context);
initViewResolvers(context);
initFlashMapManager(context);



DispatcherServlet中定义了一些属性常量,主要作用如下:

- EXCEPTION_ATTRIBUTE:存储处理中出现的异常。

- FLASH_MAP_MANAGER_ATTRIBUTE:FlashMap管理器属性名。

- FLASH_MAP_MANAGER_BEAN_NAME:FlashMap管理器bean名。

- HANDLER_ADAPTER_BEAN_NAME:处理程序适配器bean名。

- HANDLER_EXCEPTION_RESOLVER_BEAN_NAME:异常解析器bean名。 

- HANDLER_MAPPING_BEAN_NAME:处理程序映射bean名。

- INPUT_FLASH_MAP_ATTRIBUTE:输入FlashMap属性名。

- LOCALE_RESOLVER_ATTRIBUTE:区域设置解析器属性名。

- LOCALE_RESOLVER_BEAN_NAME:区域设置解析器bean名。

- MULTIPART_RESOLVER_BEAN_NAME:多部分解析器bean名。

- OUTPUT_FLASH_MAP_ATTRIBUTE:输出FlashMap属性名。

- PAGE_NOT_FOUND_LOG_CATEGORY:404日志类别。

- REQUEST_TO_VIEW_NAME_TRANSLATOR_BEAN_NAME:请求视图名转换器bean名。

- THEME_RESOLVER_ATTRIBUTE:主题解析器属性名。

- THEME_RESOLVER_BEAN_NAME:主题解析器bean名。 

- THEME_SOURCE_ATTRIBUTE:主题源属性名。

- VIEW_RESOLVER_BEAN_NAME: 视图解析器bean名。

- WEB_APPLICATION_CONTEXT_ATTRIBUTE:Web应用上下文属性名。

这些属性定义了DispatcherServlet使用的各processor/resolver的标识名,方便统一配置。





在Spring MVC中,org.springframework.web.servlet.FlashMap 可以用于在重定向之间传递短期的模型数据。典型的使用示例如下:

1. 在Controller中创建FlashMap:

```java
@RequestMapping("/show")
public String show(Model model) {
  FlashMap flashMap = new FlashMap();
  flashMap.put("successMsg", "Operation succeeded!");
  
  model.addAttribute(RequestContextUtils.OUTPUT_FLASH_MAP_ATTRIBUTE, flashMap);
  return "redirect:/next";
}
```

2. 在重定向的方法中读取FlashMap:

```java  
@RequestMapping("/next")
public String next(Model model) {
  FlashMap flashMap = (FlashMap)model.asMap().get(RequestContextUtils.OUTPUT_FLASH_MAP_ATTRIBUTE);
  
  if(flashMap != null) {
    model.addAttribute("successMsg", flashMap.get("successMsg"));
  }
  return "nextView";
}
```

3. 这样就可以在next()中得到show()传递的flash信息。

4. 重定向后会自动清除FlashMap。

综上,FlashMap用于重定向场景下的短期数据传递,避免RedirectAttributes限制。





HandlerInterceptor子类

MappedInterceptor (org.springframework.web.servlet.handler)
AsyncHandlerInterceptor (org.springframework.web.servlet)
    WebRequestHandlerInterceptorAdapter (org.springframework.web.servlet.handler)
    HandlerInterceptorAdapter (org.springframework.web.servlet.handler)
        LocaleChangeInterceptor (org.springframework.web.servlet.i18n)
        ThemeChangeInterceptor (org.springframework.web.servlet.theme)
        ResourceUrlProviderExposingInterceptor (org.springframework.web.servlet.resource)
        UserRoleAuthorizationInterceptor (org.springframework.web.servlet.handler)
        UriTemplateVariablesHandlerInterceptor in AbstractUrlHandlerMapping (org.springframework.web.servlet.handler)
        CorsInterceptor in AbstractHandlerMapping (org.springframework.web.servlet.handler)
        ConversionServiceExposingInterceptor (org.springframework.web.servlet.handler)
        PathExposingHandlerInterceptor in AbstractUrlHandlerMapping (org.springframework.web.servlet.handler)
WebContentInterceptor (org.springframework.web.servlet.mvc)
StatHandlerInterceptor (com.alibaba.druid.support.spring.mvc)





在Spring MVC的HandlerMapping中,定义了一个名为_MATRIX_VARIABLES_ATTRIBUTE的常量字段,它的作用是:

1. 用来保存请求URL中矩阵变量的属性名。

2. 矩阵变量表示以分号';'分隔的URL路径参数。

3. 如/books;genre=tech,其中genre=tech就是矩阵变量。

4. HandlerMapping会提取这些矩阵变量,存入模型属性中。

5. 这个常量定义了矩阵变量对应的属性名:_MATRIX_VARIABLES_ATTRIBUTE。

6. 因此在Controller中可以通过这个属性名获得矩阵变量:

```java
@GetMapping("/books/{isbn};genre={genre}")
public void handle(Model model) {
  Map<String, String> matrixVars = model.asMap().get(HandlerMapping.MATRIX_VARIABLES_ATTRIBUTE);
  String genre = matrixVars.get("genre"); // tech
}
```

7. 这样可以方便地在Controller中访问矩阵变量。

总之,该常量让获取矩阵变量更加标准化和便捷。

矩阵变量也可表示复杂的参数,配合注解驱动使用可以优化URL的设计。



| org.springframework.web.servlet.config       |          |                                                              |
| -------------------------------------------- | -------- | ------------------------------------------------------------ |
| Classes                                      |          |                                                              |
| CorsBeanDefinitionParser                     |          | xml cors节点                                                 |
| FreeMarkerConfigurerBeanDefinitionParser     |          | freemarker-configurer节点                                    |
| GroovyMarkupConfigurerBeanDefinitionParser   |          | groovy-configurer节点                                        |
| MvcNamespaceHandler                          |          | extends NamespaceHandlerSupport 这个包的核心类，把xml配置中的节点跟java类关联起来 |
| MvcNamespaceUtils                            | abstract | BEAN_NAME_URL_HANDLER_MAPPING_BEAN_NAME 静态方法             |
| ScriptTemplateConfigurerBeanDefinitionParser |          | xml script-template-configurer节点                           |
| TilesConfigurerBeanDefinitionParser          |          | xml tiles-configurer节点                                     |
| ViewResolversBeanDefinitionParser            |          | xml view-resolvers节点                                       |





MvcNamespaceHandler



| org.springframework.web.servlet.config.annotation |            |                                                              |
| ------------------------------------------------- | ---------- | ------------------------------------------------------------ |
| Interfaces                                        |            |                                                              |
| WebMvcConfigurer                                  | interface  | 子类有WebMvcConfigurerComposite                              |
|                                                   |            |                                                              |
| Classes                                           |            |                                                              |
| AsyncSupportConfigurer                            |            |                                                              |
| ContentNegotiationConfigurer                      |            |                                                              |
| CorsRegistration                                  |            |                                                              |
| CorsRegistry                                      |            |                                                              |
| DefaultServletHandlerConfigurer                   |            |                                                              |
| DelegatingWebMvcConfiguration                     |            |                                                              |
| InterceptorRegistration                           |            |                                                              |
| InterceptorRegistry                               |            |                                                              |
| PathMatchConfigurer                               |            | 4.0.3                                                        |
| RedirectViewControllerRegistration                |            |                                                              |
| ResourceChainRegistration                         |            |                                                              |
| ResourceHandlerRegistration                       |            | 注册静态资源处理器                                           |
| ResourceHandlerRegistry                           |            |                                                              |
| UrlBasedViewResolverRegistration                  |            | 注册基于URL的视图解析器                                      |
| ViewControllerRegistration                        |            | 注册视图控制器                                               |
| ViewControllerRegistry                            |            |                                                              |
| ViewResolverRegistry                              |            |                                                              |
| WebMvcConfigurationSupport                        |            | 定义了很多Spring ico容器的bean，比如RequestMappingHandlerMapping |
| WebMvcConfigurerAdapter                           |            |                                                              |
| WebMvcConfigurerComposite                         |            | DelegatingWebMvcConfiguration里面有这个类的对象              |
|                                                   |            |                                                              |
| Annotation Types                                  |            |                                                              |
| EnableWebMvc                                      | @interface | @Import(DelegatingWebMvcConfiguration.class)  没找到注解处理器，但是WebMvcConfigurationSupport类有一堆@Bean注解修饰的方法，生成类注入spring ioc? |





Spring通过注解驱动来实现@EnableWebMvc的解析和应用,主要流程如下:

1. 在Spring容器刷新时,会调用PostProcessor的postProcessBeanDefinitionRegistry方法。

2. DelegatingWebMvcConfiguration这个PostProcessor实现了该方法。

3. 在方法内部,会通过注解工具类查找是否存在@EnableWebMvc注解:

   ```java
   if (AnnotatedElementUtils.hasAnnotation(element, EnableWebMvc.class)) {
     // ...
   }
   ```

4. 如果存在该注解,则会注册DelegatingWebMvcConfiguration的内部类WebMvcConfigurationSupport:

   ```java
   registry.registerBeanDefinition(WEB_MVC_CONFIGURATION_SUPPORT_BEAN_NAME,
                                  new RootBeanDefinition(WebMvcConfigurationSupport.class)); 
   ```

5. WebMvcConfigurationSupport中实现了Spring MVC的自动配置逻辑。

6. 如注册组件、添加内容协商解析器等,从而激活Spring MVC功能。

7. 这样当启动容器时,通过查找@EnableWebMvc注解,实现了Spring MVC的自动配置。

综上,Spring通过后处理器在容器刷新阶段解析注解,从而实现对应功能的激活。





@EnableWebMvc 注解可以用于 Spring MVC 项目中，也可以用于 Spring Boot 项目中。

在 Spring MVC 项目中，可以通过在 `@Configuration` 注解的类上使用 `@EnableWebMvc` 注解来开启 Spring MVC 功能。

在 Spring Boot 项目中，可以通过在 `@SpringBootApplication` 注解的类上使用 `@EnableWebMvc` 注解来开启 Spring MVC 功能。

以下是使用 `@EnableWebMvc` 注解在 Spring MVC 项目中开启 Spring MVC 功能的示例代码：

```
@Configuration
@EnableWebMvc
public class WebConfig {

}
```

以下是使用 `@EnableWebMvc` 注解在 Spring Boot 项目中开启 Spring MVC 功能的示例代码：

```
@SpringBootApplication
@EnableWebMvc
public class SpringBootWebMvcApplication {

    public static void main(String[] args) {
        SpringApplication.run(SpringBootWebMvcApplication.class, args);
    }

}
```



Spring 源码根据是否加上 `@EnableWebMvc` 注解来注入 bean，相关源码解析如下：

* 在 `WebMvcAutoConfiguration` 类中，会通过 `@ConditionalOnWebApplication` 注解判断当前应用是否为 Web 应用，如果是，则会通过 `@ConditionalOnClass` 注解判断是否存在 `DispatcherServlet` 类，如果存在，则会通过 `@Bean` 注解注册 `DispatcherServlet`  bean。
* 在 `DispatcherServletAutoConfiguration` 类中，会通过 `@ConditionalOnBean` 注解判断是否存在 `DispatcherServlet`  bean，如果存在，则会通过 `@Bean` 注解注册 `HandlerMapping`、`HandlerAdapter`、`ViewResolver`、`LocaleResolver`、`ThemeResolver`、`RequestToViewNameTranslator` 等 bean。
* 在 `WebMvcConfigurationSupport` 类中，会通过 `@ConditionalOnMissingBean` 注解判断是否存在 `RequestMappingHandlerMapping`  bean，如果不存在，则会通过 `@Bean` 注解注册 `RequestMappingHandlerMapping`  bean。
* 在 `RequestMappingHandlerMapping` 类中，会通过 `@Autowired` 注解自动注入 `RequestMappingHandlerAdapter`、`ContentNegotiatingViewResolver`、`RequestToViewNameTranslator`、`HandlerExceptionResolver` 等 bean。

通过以上源码解析，我们可以看到，Spring 源码根据是否加上 `@EnableWebMvc` 注解来注入 bean，如果加上了 `@EnableWebMvc` 注解，则会注入 `DispatcherServlet`、`HandlerMapping`、`HandlerAdapter`、`ViewResolver`、`LocaleResolver`、`ThemeResolver`、`RequestToViewNameTranslator`、`RequestMappingHandlerMapping`、`RequestMappingHandlerAdapter`、`ContentNegotiatingViewResolver`、`RequestToViewNameTranslator`、`HandlerExceptionResolver` 等 bean。如果没有加上 `@EnableWebMvc` 注解，则只会注入 `DispatcherServlet`  bean。



WebMvcAutoConfiguration WebMvcConfigurer

@EnableWebMvc 注解处理器位于 `org.springframework.web.servlet.config.annotation.WebMvcConfigurationSupport` 类中。

该类提供了一些方法来配置 Spring MVC 的组件，例如：

* 配置 DispatcherServlet
* 配置 HandlerMapping
* 配置 HandlerAdapter
* 配置 ViewResolver
* 配置 Interceptor
* 配置 Validator
* 配置 MessageSource
* 配置 LocaleResolver
* 配置 Formatter
* 配置 AsyncSupport

这些方法可以通过 `@EnableWebMvc` 注解来使用。

例如，以下代码配置了 DispatcherServlet：

```java
@Configuration
@EnableWebMvc
public class WebConfig {

    @Bean
    public DispatcherServlet dispatcherServlet() {
        return new DispatcherServlet();
    }

}
```

当使用 `@EnableWebMvc` 注解时，Spring MVC 会自动扫描该类所在的包及其子包，并加载其中的 `@Controller` 和 `@RestController` 注解的类。

这些类会被 Spring MVC 的组件识别，并被加载到 Spring 容器中。

当用户发送 HTTP 请求到 Spring MVC 时，Spring MVC 会根据请求的 URL 找到对应的 `@Controller` 或 `@RestController` 类，并调用其中的方法来处理请求。

请求处理完成后，Spring MVC 会根据配置的 ViewResolver 来将处理结果渲染成 HTML 页面，并返回给用户。





| org.springframework.web.servlet.function 整个包都是5.2才有的 |           |                        |
| ------------------------------------------------------------ | --------- | ---------------------- |
| Interfaces                                                   |           |                        |
| EntityResponse                                               | interface |                        |
| EntityResponse.Builder                                       | interface |                        |
| HandlerFilterFunction                                        | interface |                        |
| HandlerFunction                                              | interface |                        |
| RenderingResponse                                            | interface | extends ServerResponse |
| RenderingResponse.Builder                                    | interface |                        |
| RequestPredicate                                             | interface |                        |
| RequestPredicates.Visitor                                    | interface |                        |
| RouterFunction                                               | interface |                        |
| RouterFunctions.Builder                                      | interface |                        |
| RouterFunctions.Visitor                                      | interface |                        |
| ServerRequest                                                | interface |                        |
| ServerRequest.Builder                                        | interface |                        |
| ServerRequest.Headers                                        | interface |                        |
| ServerResponse                                               | interface |                        |
| ServerResponse.BodyBuilder                                   | interface |                        |
| ServerResponse.Context                                       | interface |                        |
| ServerResponse.HeadersBuilder                                | interface |                        |
|                                                              |           |                        |
| Classes                                                      |           |                        |
| RequestPredicates                                            | abstract  | 5.2才有的              |
| RouterFunctions                                              |           |                        |



| org.springframework.web.servlet.function.support |      |                                              |
| ------------------------------------------------ | ---- | -------------------------------------------- |
| Classes                                          |      |                                              |
| HandlerFunctionAdapter                           |      | 5.2才有的 implements HandlerAdapter, Ordered |
| RouterFunctionMapping                            |      |                                              |













| org.springframework.web.servlet.handler |           |                                                              |
| --------------------------------------- | --------- | ------------------------------------------------------------ |
| Interfaces                              |           |                                                              |
| HandlerMethodMappingNamingStrategy      | interface |                                                              |
| MatchableHandlerMapping                 | interface |                                                              |
|                                         |           |                                                              |
| Classes                                 |           |                                                              |
| AbstractDetectingUrlHandlerMapping      |           |                                                              |
| AbstractHandlerExceptionResolver        |           |                                                              |
| AbstractHandlerMapping                  |           |                                                              |
| AbstractHandlerMethodExceptionResolver  |           |                                                              |
| AbstractHandlerMethodMapping            |           | 有属性 CorsConfiguration ALLOW_CORS_CONFIG                   |
| AbstractUrlHandlerMapping               |           |                                                              |
| BeanNameUrlHandlerMapping               |           |                                                              |
| ConversionServiceExposingInterceptor    |           | HandlerInterceptorAdapter子类                                |
| DispatcherServletWebRequest             |           | ServletWebRequest子类 类比StandardServletAsyncWebRequest     |
| HandlerExceptionResolverComposite       |           |                                                              |
| HandlerInterceptorAdapter               | abstract  |                                                              |
| HandlerMappingIntrospector              |           | 4.3.1才有的                                                  |
| MappedInterceptor                       |           | 核心类                                                       |
| RequestMatchResult                      |           |                                                              |
| SimpleMappingExceptionResolver          |           |                                                              |
| SimpleServletHandlerAdapter             |           |                                                              |
| SimpleServletPostProcessor              |           |                                                              |
| SimpleUrlHandlerMapping                 |           | 用法 SimpleUrlHandlerMapping(Map<String, ?> urlMap, int order) 简单网页映射 |
| UserRoleAuthorizationInterceptor        |           |                                                              |
| WebRequestHandlerInterceptorAdapter     |           |                                                              |





在Spring MVC中,MappedInterceptor是框架内建的一个拦截器适配器,它的主要作用是:

1. 适配HandlerInterceptor接口,使拦截器可以与@ControllerAdvice注解配合使用。

2. 通过@ControllerAdvice定义的拦截器可以被应用到所有Controller请求中。

使用示例:

1. 定义一个统一的日志记录拦截器:

```java
@Component
public class LoggingInterceptor implements HandlerInterceptor {

  @Override
  public boolean preHandle(...) {
    // 打印请求日志
    return true; 
  }

}
```

2. 通过@ControllerAdvice应用该拦截器:

```java
@ControllerAdvice
public class GlobalConfig {

  @Autowired
  private LoggingInterceptor loggingInterceptor;

  @InitBinder
  public void initBinder(WebDataBinder binder) {
    binder.addInterceptors(new MappedInterceptor(null, loggingInterceptor)); 
  }
}
```

3. 这样LoggingInterceptor就会应用到所有Controller中。

综上,MappedInterceptor可以将自定义拦截器与@ControllerAdvice结合使用,实现全局配置。





| org.springframework.web.servlet.i18n |          |      |
| ------------------------------------ | -------- | ---- |
| Classes                              |          |      |
| AbstractLocaleContextResolver        | abstract | 4.0  |
| AbstractLocaleResolver               | abstract |      |
| AcceptHeaderLocaleResolver           |          |      |
| CookieLocaleResolver                 |          |      |
| FixedLocaleResolver                  |          |      |
| LocaleChangeInterceptor              |          |      |
| SessionLocaleResolver                |          |      |



这些类都是与Spring MVC国际化 Locale 解析相关的类,它们的区别与联系如下:

1. LocaleContextResolver:框架定义的LocaleContext的解析器接口。

2. AbstractLocaleContextResolver:实现了上述接口的抽象基类。

3. LocaleResolver:框架定义的Locale解析器接口。

4. AbstractLocaleResolver:实现了上述接口的抽象基类。

5. CookieLocaleResolver:使用Cookie解析Locale的实现。

6. SessionLocaleResolver:使用Session解析Locale的实现。

7. AcceptHeaderLocaleResolver:使用AcceptHeader解析Locale的实现。

8. FixedLocaleResolver:固定返回指定Locale的实现。

它们的区别在于解析策略不同:

- Cookie、Session、AcceptHeader根据不同的请求信息源解析

- Fixed直接返回固定的预设Locale

它们的联系是:

- 都实现了LocaleResolver接口或其扩展接口

- 都可以被注入到LocalContextResolver使用

- 提供不同的Locale解析策略

使用场景:

- 根据需求选择不同的解析策略,注入到LocalContextResolver使用

- 如网页根据Cookie保存用户选择,APP根据AcceptHeader发送等





| org.springframework.web.servlet.mvc |           |                                                              |
| ----------------------------------- | --------- | ------------------------------------------------------------ |
| Interfaces                          |           |                                                              |
| Controller                          | interface | ModelAndView handleRequest(HttpServletRequest request, HttpServletResponse response) |
| LastModified                        | interface |                                                              |
|                                     |           |                                                              |
| Classes                             |           |                                                              |
| AbstractController                  | abstract  | extends WebContentGenerator                                  |
| AbstractUrlViewController           | abstract  | AbstractUrlViewController                                    |
| HttpRequestHandlerAdapter           |           | HttpRequestHandler                                           |
| ParameterizableViewController       |           |                                                              |
| ServletForwardingController         |           |                                                              |
| ServletWrappingController           |           |                                                              |
| SimpleControllerHandlerAdapter      |           | Controller                                                   |
| UrlFilenameViewController           |           |                                                              |
| WebContentInterceptor               |           |                                                              |







| org.springframework.web.servlet.mvc.annotation |      |      |
| ---------------------------------------------- | ---- | ---- |
| Interfaces                                     |      |      |
| ModelAndViewResolver                           |      |      |
|                                                |      |      |
| Classes                                        |      |      |
| ResponseStatusExceptionResolver                |      |      |
|                                                |      |      |















| org.springframework.web.servlet.mvc.condition |      |      |
| --------------------------------------------- | ---- | ---- |
| Interfaces                                    |      |      |
| MediaTypeExpression                           |      |      |
| NameValueExpression                           |      |      |
| RequestCondition                              |      |      |
|                                               |      |      |
| Classes                                       |      |      |
| AbstractRequestCondition                      |      |      |
| CompositeRequestCondition                     |      |      |
| ConsumesRequestCondition                      |      |      |
| HeadersRequestCondition                       |      |      |
| ParamsRequestCondition                        |      |      |
| PatternsRequestCondition                      |      |      |
| ProducesRequestCondition                      |      |      |
| RequestConditionHolder                        |      |      |
| RequestMethodsRequestCondition                |      |      |









| org.springframework.web.servlet.mvc.method           |      |      |
| ---------------------------------------------------- | ---- | ---- |
| Interfaces                                           |      |      |
| RequestMappingInfo.Builder                           |      |      |
|                                                      |      |      |
| Classes                                              |      |      |
| AbstractHandlerMethodAdapter                         |      |      |
| RequestMappingInfo                                   |      |      |
| RequestMappingInfo.BuilderConfiguration              |      |      |
| RequestMappingInfoHandlerMapping                     |      |      |
| RequestMappingInfoHandlerMethodMappingNamingStrategy |      |      |









| org.springframework.web.servlet.mvc.method.annotation |      |                                                              |
| ----------------------------------------------------- | ---- | ------------------------------------------------------------ |
| Interfaces                                            |      |                                                              |
| MvcUriComponentsBuilder.MethodInvocationInfo          |      |                                                              |
| RequestBodyAdvice                                     |      |                                                              |
| ResponseBodyAdvice                                    |      |                                                              |
| SseEmitter.SseEventBuilder                            |      |                                                              |
| StreamingResponseBody                                 |      |                                                              |
|                                                       |      |                                                              |
| Classes                                               |      |                                                              |
| AbstractMappingJacksonResponseBodyAdvice              |      |                                                              |
| AbstractMessageConverterMethodArgumentResolver        |      |                                                              |
| AbstractMessageConverterMethodProcessor               |      |                                                              |
| AbstractMessageConverterMethodProcessor               |      |                                                              |
| AbstractMessageConverterMethodProcessor               |      |                                                              |
| CallableMethodReturnValueHandler                      |      |                                                              |
| DeferredResultMethodReturnValueHandler                |      |                                                              |
| ExceptionHandlerExceptionResolver                     |      |                                                              |
| ExtendedServletRequestDataBinder                      |      |                                                              |
| HttpEntityMethodProcessor                             |      |                                                              |
| HttpHeadersReturnValueHandler                         |      |                                                              |
| JsonViewRequestBodyAdvice                             |      |                                                              |
| JsonViewResponseBodyAdvice                            |      |                                                              |
| MatrixVariableMapMethodArgumentResolver               |      |                                                              |
| MatrixVariableMethodArgumentResolver                  |      |                                                              |
| ModelAndViewMethodReturnValueHandler                  |      |                                                              |
| ModelAndViewResolverMethodReturnValueHandler          |      |                                                              |
| MvcUriComponentsBuilder                               |      |                                                              |
| MvcUriComponentsBuilder.MethodArgumentBuilder         |      |                                                              |
| PathVariableMapMethodArgumentResolver                 |      |                                                              |
| PathVariableMethodArgumentResolver                    |      |                                                              |
| RedirectAttributesMethodArgumentResolver              |      |                                                              |
| RequestAttributeMethodArgumentResolver                |      |                                                              |
| RequestBodyAdviceAdapter                              |      |                                                              |
| RequestMappingHandlerAdapter                          |      |                                                              |
| RequestMappingHandlerMapping                          |      |                                                              |
| RequestPartMethodArgumentResolver                     |      |                                                              |
| RequestResponseBodyMethodProcessor                    |      |                                                              |
| ResponseBodyEmitter                                   |      |                                                              |
| ResponseBodyEmitter.DataWithMediaType                 |      |                                                              |
| ResponseBodyEmitterReturnValueHandler                 |      |                                                              |
| ResponseEntityExceptionHandler                        |      |                                                              |
| ServletCookieValueMethodArgumentResolver              |      |                                                              |
| ServletInvocableHandlerMethod                         |      | 实际执行  org.springframework.web.method.support.InvocableHandlerMethod#invokeForRequest    很重要 |
| ServletModelAttributeMethodProcessor                  |      |                                                              |
| ServletRequestDataBinderFactory                       |      |                                                              |
| ServletRequestMethodArgumentResolver                  |      |                                                              |
| ServletResponseMethodArgumentResolver                 |      |                                                              |
| ServletWebArgumentResolverAdapter                     |      |                                                              |
| SessionAttributeMethodArgumentResolver                |      |                                                              |
| SseEmitter                                            |      |                                                              |
| StreamingResponseBodyReturnValueHandler               |      |                                                              |
| UriComponentsBuilderMethodArgumentResolver            |      |                                                              |
| ViewMethodReturnValueHandler                          |      |                                                              |
| ViewNameMethodReturnValueHandler                      |      |                                                              |







| org.springframework.web.servlet.mvc.support |      |      |
| ------------------------------------------- | ---- | ---- |
| Interfaces                                  |      |      |
| RedirectAttributes                          |      |      |
|                                             |      |      |
| Classes                                     |      |      |
| DefaultHandlerExceptionResolver             |      |      |
| RedirectAttributesModelMap                  |      |      |







| org.springframework.web.servlet.resource |      |      |
| ---------------------------------------- | ---- | ---- |
| Interfaces                               |      |      |
| CssLinkResourceTransformer.LinkParser    |      |      |
| HttpResource                             |      |      |
| ResourceResolver                         |      |      |
| ResourceResolverChain                    |      |      |
| ResourceTransformer                      |      |      |
| ResourceTransformerChain                 |      |      |
| VersionPathStrategy                      |      |      |
| VersionStrategy                          |      |      |
|                                          |      |      |
| Classes                                  |      |      |











AbstractResourceResolver

AbstractVersionStrategy

AbstractVersionStrategy.FileNameVersionPathStrategy

AbstractVersionStrategy.PrefixVersionPathStrategy

AppCacheManifestTransformer

CachingResourceResolver

CachingResourceTransformer

ContentVersionStrategy

CssLinkResourceTransformer

CssLinkResourceTransformer.AbstractLinkParser

DefaultServletHttpRequestHandler

EncodedResourceResolver

FixedVersionStrategy

GzipResourceResolver

PathResourceResolver

ResourceHttpRequestHandler

ResourceTransformerSupport

ResourceUrlEncodingFilter

ResourceUrlProvider

ResourceUrlProviderExposingInterceptor

TransformedResource

VersionResourceResolver

WebJarsResourceResolver













| org.springframework.web.servlet.support              |      |      |
| ---------------------------------------------------- | ---- | ---- |
| Interfaces                                           |      |      |
| RequestDataValueProcessor                            |      |      |
|                                                      |      |      |
| Classes                                              |      |      |
| AbstractAnnotationConfigDispatcherServletInitializer |      |      |
| AbstractDispatcherServletInitializer                 |      |      |
| AbstractFlashMapManager                              |      |      |
| BindStatus                                           |      |      |
| JspAwareRequestContext                               |      |      |
| JstlUtils                                            |      |      |
| RequestContext                                       |      |      |
| RequestContextUtils                                  |      |      |
| ServletUriComponentsBuilder                          |      |      |
| SessionFlashMapManager                               |      |      |
| WebContentGenerator                                  |      |      |












| org.springframework.web.servlet.tags |      |      |
| ------------------------------------ | ---- | ---- |
| Interfaces                           |      |      |
| ArgumentAware                        |      |      |
| EditorAwareTag                       |      |      |
| ParamAware                           |      |      |
|                                      |      |      |
| Classes                              |      |      |
| ArgumentTag                          |      |      |
| BindErrorsTag                        |      |      |
| BindTag                              |      |      |
| EscapeBodyTag                        |      |      |
| EvalTag                              |      |      |
| HtmlEscapeTag                        |      |      |
| HtmlEscapingAwareTag                 |      |      |
| MessageTag                           |      |      |
| NestedPathTag                        |      |      |
| Param                                |      |      |
| ParamTag                             |      |      |
| RequestContextAwareTag               |      |      |
| ThemeTag                             |      |      |
| TransformTag                         |      |      |
| UrlTag                               |      |      |


















| org.springframework.web.servlet.theme |      |      |
| ------------------------------------- | ---- | ---- |
| Classes                               |      |      |
| AbstractCheckedElementTag             |      |      |
| AbstractDataBoundFormElementTag       |      |      |
| AbstractFormTag                       |      |      |
| AbstractHtmlElementBodyTag            |      |      |
| AbstractHtmlElementTag                |      |      |
| AbstractHtmlInputElementTag           |      |      |
| AbstractMultiCheckedElementTag        |      |      |
| AbstractSingleCheckedElementTag       |      |      |
| ButtonTag                             |      |      |
| CheckboxesTag                         |      |      |
| CheckboxTag                           |      |      |
| ErrorsTag                             |      |      |
| FormTag                               |      |      |
| HiddenInputTag                        |      |      |
| InputTag                              |      |      |
| LabelTag                              |      |      |
| OptionTag                             |      |      |
| PasswordInputTag                      |      |      |
| RadioButtonsTag                       |      |      |
| RadioButtonTag                        |      |      |
| SelectTag                             |      |      |
| TagWriter                             |      |      |
| TextareaTag                           |      |      |












| org.springframework.web.servlet.view    |          |                                                              |
| --------------------------------------- | -------- | ------------------------------------------------------------ |
| Interfaces                              |          |                                                              |
| AbstractCachingViewResolver.CacheFilter |          |                                                              |
|                                         |          |                                                              |
| Classes                                 |          |                                                              |
| AbstractCachingViewResolver             | abstract | 实现ViewResolver接口，ViewResolver的resolveViewName()方法调用protected abstract View loadView(String viewName, Locale locale) |
| AbstractTemplateView                    | abstract |                                                              |
| AbstractTemplateViewResolver            | abstract |                                                              |
| AbstractUrlBasedView                    | abstract |                                                              |
| AbstractView                            | abstract | 实现View接口 renderMergedOutputModel()                       |
| BeanNameViewResolver                    |          | 继承WebApplicationObjectSupport                              |
| ContentNegotiatingViewResolver          |          | 继承WebApplicationObjectSupport，返回json时的ViewResolver  ContentNegotiationManager ContentNegotiationManagerFactoryBean   属性 org.springframework.web.servlet.view.ContentNegotiatingViewResolver#getCandidateViews   方法很关键 |
| DefaultRequestToViewNameTranslator      |          |                                                              |
| InternalResourceView                    |          | 继承AbstractUrlBasedView                                     |
| InternalResourceViewResolver            |          |                                                              |
| Jstliew                                 |          |                                                              |
| RedirectView                            |          | 实现类 AbstractUrlBasedView 实现SmartView接口                |
| ResourceBundleViewResolver              |          |                                                              |
| UrlBasedViewResolver                    |          | 继承AbstractCachingViewResolver 实现父类的抽象方法 loadView() |
| ViewResolverComposite                   |          |                                                              |
| XmlViewResolver                         |          |                                                              |



ContentNegotiatingViewResolver

断点





UrlBasedViewResolver  跟AbstractUrlBasedView对应

buildView()

getViewClass()

setViewClass()





AbstractUrlBasedView子类



 AbstractUrlBasedView (org.springframework.web.servlet.view)
                AbstractPdfStamperView (org.springframework.web.servlet.view.document)
                RedirectView (org.springframework.web.servlet.view)
                AbstractTemplateView (org.springframework.web.servlet.view)
                    GroovyMarkupView (org.springframework.web.servlet.view.groovy)
                    MustacheView (org.springframework.boot.web.servlet.view)
                    FreeMarkerView (org.springframework.web.servlet.view.freemarker)
                TilesView (org.springframework.web.servlet.view.tiles3)
                XsltView (org.springframework.web.servlet.view.xslt)
                InternalResourceView (org.springframework.web.servlet.view)
                    JstlView (org.springframework.web.servlet.view)
                ScriptTemplateView (org.springframework.web.servlet.view.script)

AbstractView 子类

ApplicationObjectSupport (org.springframework.context.support)
    WebApplicationObjectSupport (org.springframework.web.context.support)
        AbstractView (org.springframework.web.servlet.view)
            AbstractJackson2View (org.springframework.web.servlet.view.json)
                MappingJackson2JsonView (org.springframework.web.servlet.view.json)
                MappingJackson2XmlView (org.springframework.web.servlet.view.xml)
            AbstractPdfView (org.springframework.web.servlet.view.document)
            MarshallingView (org.springframework.web.servlet.view.xml)
            AbstractUrlBasedView (org.springframework.web.servlet.view)
                AbstractPdfStamperView (org.springframework.web.servlet.view.document)
                RedirectView (org.springframework.web.servlet.view)
                AbstractTemplateView (org.springframework.web.servlet.view)
                    GroovyMarkupView (org.springframework.web.servlet.view.groovy)
                    MustacheView (org.springframework.boot.web.servlet.view)
                    FreeMarkerView (org.springframework.web.servlet.view.freemarker)
                TilesView (org.springframework.web.servlet.view.tiles3)
                XsltView (org.springframework.web.servlet.view.xslt)
                InternalResourceView (org.springframework.web.servlet.view)
                    JstlView (org.springframework.web.servlet.view)
                ScriptTemplateView (org.springframework.web.servlet.view.script)
            AbstractXlsView (org.springframework.web.servlet.view.document)
                AbstractXlsxView (org.springframework.web.servlet.view.document)
            FastJsonJsonView (com.alibaba.fastjson.support.spring)
            AbstractFeedView (org.springframework.web.servlet.view.feed)
                AbstractAtomFeedView (org.springframework.web.servlet.view.feed)
                AbstractRssFeedView (org.springframework.web.servlet.view.feed)





InternalResourceViewResolver 和 UrlBasedViewResolver 都是 Spring MVC 的 ViewResolver，用于将请求转发到相应的视图。

InternalResourceViewResolver 是 Spring MVC 默认的 ViewResolver，它将请求转发到一个内部资源，例如 `/WEB-INF/jsp/index.jsp`。

UrlBasedViewResolver 可以将请求转发到任何资源，包括内部资源和外部资源。

InternalResourceViewResolver 和 UrlBasedViewResolver 的区别如下：

* InternalResourceViewResolver 只能将请求转发到内部资源，而 UrlBasedViewResolver 可以将请求转发到任何资源。
* InternalResourceViewResolver 的配置比较简单，而 UrlBasedViewResolver 的配置比较复杂。
* InternalResourceViewResolver 的性能比 UrlBasedViewResolver 更高。

在实际开发中，如果需要将请求转发到内部资源，可以使用 InternalResourceViewResolver；如果需要将请求转发到任何资源，可以使用 UrlBasedViewResolver。







Spring MVC 返回 JSON 字符串的时候，ViewResolver 不是 InternalResourceViewResolver。

InternalResourceViewResolver 是 Spring MVC 默认的 ViewResolver，它用于将请求转发到一个内部资源，例如 `/WEB-INF/jsp/index.jsp`。

Spring MVC 返回 JSON 字符串的时候，需要使用 `ContentNegotiatingViewResolver` 来处理。

`ContentNegotiatingViewResolver` 是 Spring MVC 的视图解析器，它可以根据请求头中的 `Accept` 头来选择不同的视图。

如果请求头中的 `Accept` 头中包含 `application/json`，则 `ContentNegotiatingViewResolver` 会使用 `MappingJackson2JsonView` 来处理请求。

`MappingJackson2JsonView` 是 Spring MVC 的视图，它可以将模型对象转换成 JSON 字符串。

所以，Spring MVC 返回 JSON 字符串的时候，ViewResolver 不是 InternalResourceViewResolver，而是 ContentNegotiatingViewResolver。





BeanNameViewResolver ContentNegotiatingViewResolver InternalResourceViewResolver ResourceBundleViewResolver  UrlBasedViewResolver XmlViewResolver



这些类都是Spring MVC框架中的视图解析器(ViewResolver),它们的作用、联系和区别总结如下:

作用:
- BeanNameViewResolver - 通过Bean名称解析视图
- ContentNegotiatingViewResolver - 通过内容协商解析视图 
- InternalResourceViewResolver - 通过JSP和其他资源解析视图
- ResourceBundleViewResolver - 通过资源Bundle解析视图
- UrlBasedViewResolver - 通过视图URL解析视图
- XmlViewResolver - 通过XML文件解析视图

联系:
- 都实现了ViewResolver接口,提供视图解析功能
- 可以组合使用,形成链式解析

区别:  
- 解析策略不同,针对不同使用场景
- 如JSP、国际化资源、内容协商等

典型用法:
- InternalResourceViewResolver解析JSP 
- ContentNegotiatingViewResolver实现内容协商
- 组合多种解析器完成解析过程

综上,这些视图解析器实现了不同的解析策略,可以灵活组合使用。





StaticView in ErrorMvcAutoConfiguration (org.springframework.boot.autoconfigure.web.servlet.error)
HtmlResourceView in DefaultErrorViewResolver (org.springframework.boot.autoconfigure.web.servlet.error)
AbstractView (org.springframework.web.servlet.view)
    AbstractJackson2View (org.springframework.web.servlet.view.json)
    AbstractPdfView (org.springframework.web.servlet.view.document)
    MarshallingView (org.springframework.web.servlet.view.xml)
    AbstractUrlBasedView (org.springframework.web.servlet.view)
    AbstractXlsView (org.springframework.web.servlet.view.document)
    FastJsonJsonView (com.alibaba.fastjson.support.spring)
    AbstractFeedView (org.springframework.web.servlet.view.feed)
SmartView (org.springframework.web.servlet)
    RedirectView (org.springframework.web.servlet.view)
Anonymous in ContentNegotiatingViewResolver (org.springframework.web.servlet.view)
Anonymous in AbstractCachingViewResolver (org.springframework.web.servlet.view)





FastJsonJsonView 

renderMergedOutputModel()方法  AbstractView 的render()调用

这个方法的作用是往HttpServletResponse里面写json数据



org.springframework.web.servlet.view.document



Classes

AbstractPdfStamperView

AbstractPdfView

AbstractXlsView

AbstractXlsxStreamingView

AbstractXlsxView





org.springframework.web.servlet.view.feed



Classes

AbstractAtomFeedView

AbstractFeedView

AbstractRssFeedView





org.springframework.web.servlet.view.freemarker



Interfaces

FreeMarkerConfig

Classes

FreeMarkerConfigurer

FreeMarkerView

FreeMarkerViewResolver





org.springframework.web.servlet.view.groovy



Interfaces

GroovyMarkupConfig

Classes

GroovyMarkupConfigurer

GroovyMarkupView

GroovyMarkupViewResolver







| org.springframework.web.servlet.view.json |          |                                                              |
| ----------------------------------------- | -------- | ------------------------------------------------------------ |
| Classes                                   |          |                                                              |
| AbstractJackson2View                      | abstract | 4.1 public abstract void setModelKey(String modelKey) protected abstract Object filterModel(Map<String, Object> model); |
| MappingJackson2JsonView                   |          |                                                              |





MappingJackson2JsonView





org.springframework.web.servlet.view.script



Interfaces

ScriptTemplateConfig

Classes

RenderingContext

ScriptTemplateConfigurer

ScriptTemplateView

ScriptTemplateViewResolver





org.springframework.web.servlet.view.tiles3



Classes

AbstractSpringPreparerFactory

SimpleSpringPreparerFactory

SpringBeanPreparerFactory

SpringLocaleResolver

SpringWildcardServletTilesApplicationContext

TilesConfigurer

TilesView

TilesViewResolver







| org.springframework.web.servlet.view.xml |      |                 |
| ---------------------------------------- | ---- | --------------- |
| Classes                                  |      |                 |
| MappingJackson2XmlView                   |      | XmlMapper些数据 |
| MarshallingView                          |      |                 |





MappingJackson2XmlView

jackson http返回xml





org.springframework.web.servlet.view.xslt



Classes

XsltView

XsltViewResolver