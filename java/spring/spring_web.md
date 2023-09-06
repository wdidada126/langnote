# spring web





## 源代码分包详解
### org.springframework.http

| Interfaces                           |      |      |
| ------------------------------------ | ---- | ---- |
|                                      |      |      |
| ContentDisposition.Builder           |      |      |
| HttpInputMessage                     |      |      |
| HttpMessage                          |      |      |
| HttpOutputMessage                    |      |      |
| HttpRequest                          |      |      |
| ReactiveHttpInputMessage             |      |      |
| ReactiveHttpOutputMessage            |      |      |
| RequestEntity.BodyBuilder            |      |      |
| RequestEntity.HeadersBuilder         |      |      |
| ResponseCookie.ResponseCookieBuilder |      |      |
| ResponseEntity.BodyBuilder           |      |      |
| ResponseEntity.HeadersBuilder        |      |      |
| StreamingHttpOutputMessage           |      |      |
| StreamingHttpOutputMessage.Body      |      |      |
| ZeroCopyHttpOutputMessage            |      |      |
|                                      |      |      |
| Classes                              |      |      |
|                                      |      |      |
| CacheControl                         |      |      |
| ContentDisposition                   |      |      |
| HttpCookie                           |      |      |
| HttpEntity                           |      |      |
| HttpHeaders                          |      |      |
| HttpLogging                          |      |      |
| HttpRange                            |      |      |
| MediaType                            |      |      |
| MediaTypeEditor                      |      |      |
| MediaTypeFactory                     |      |      |
| RequestEntity                        |      |      |
| ResponseCookie                       |      |      |
| ResponseEntity                       |      |      |
|                                      |      |      |
| Enums                                |      |      |
|                                      |      |      |
| HttpMethod                           |      |      |
| HttpStatus                           |      |      |
| HttpStatus.Series                    |      |      |
|                                      |      |      |
| Exceptions                           |      |      |
|                                      |      |      |
| InvalidMediaTypeException            |      |      |





#### org.springframework.http.client



|                                             |      |      |
| ------------------------------------------- | ---- | ---- |
| Interfaces                                  |      |      |
|                                             |      |      |
| AsyncClientHttpRequest                      |      |      |
| AsyncClientHttpRequestExecution             |      |      |
| AsyncClientHttpRequestFactory               |      |      |
| AsyncClientHttpRequestInterceptor           |      |      |
| ClientHttpRequest                           |      |      |
| ClientHttpRequestExecution                  |      |      |
| ClientHttpRequestFactory                    |      |      |
| ClientHttpRequestInitializer                |      |      |
| ClientHttpRequestInterceptor                |      |      |
| ClientHttpResponse                          |      |      |
| MultipartBodyBuilder.PartBuilder            |      |      |
|                                             |      |      |
| Classes                                     |      |      |
|                                             |      |      |
| AbstractClientHttpRequest                   |      |      |
| AbstractClientHttpRequestFactoryWrapper     |      |      |
| AbstractClientHttpResponse                  |      |      |
| BufferingClientHttpRequestFactory           |      |      |
| HttpComponentsAsyncClientHttpRequestFactory |      |      |
| HttpComponentsClientHttpRequestFactory      |      |      |
| InterceptingAsyncClientHttpRequestFactory   |      |      |
| InterceptingClientHttpRequestFactory        |      |      |
| MultipartBodyBuilder                        |      |      |
| Netty4ClientHttpRequestFactory              |      |      |
| OkHttp3ClientHttpRequestFactory             |      |      |
| SimpleClientHttpRequestFactory              |      |      |



##### org.springframework.http.client.reactive



|                             |      |      |
| --------------------------- | ---- | ---- |
| Interfaces                  |      |      |
|                             |      |      |
| ClientHttpConnector         |      |      |
| ClientHttpRequest           |      |      |
| ClientHttpResponse          |      |      |
|                             |      |      |
| Classes                     |      |      |
|                             |      |      |
| AbstractClientHttpRequest   |      |      |
| ClientHttpRequestDecorator  |      |      |
| ClientHttpResponseDecorator |      |      |
| JettyClientHttpConnector    |      |      |
| JettyResourceFactory        |      |      |
| ReactorClientHttpConnector  |      |      |
| ReactorResourceFactory      |      |      |





##### org.springframework.http.client.support



|                                |      |      |
| ------------------------------ | ---- | ---- |
| Classes                        |      |      |
|                                |      |      |
| AsyncHttpAccessor              |      |      |
| BasicAuthenticationInterceptor |      |      |
| BasicAuthorizationInterceptor  |      |      |
| HttpAccessor                   |      |      |
| HttpRequestWrapper             |      |      |
| InterceptingAsyncHttpAccessor  |      |      |
| InterceptingHttpAccessor       |      |      |
| ProxyFactoryBean               |      |      |





#### org.springframework.http.codec



|                                           |      |      |
| ----------------------------------------- | ---- | ---- |
| Interfaces                                |      |      |
|                                           |      |      |
| ClientCodecConfigurer                     |      |      |
| ClientCodecConfigurer.ClientDefaultCodecs |      |      |
| ClientCodecConfigurer.MultipartCodecs     |      |      |
| CodecConfigurer                           |      |      |
| CodecConfigurer.CustomCodecs              |      |      |
| CodecConfigurer.DefaultCodecConfig        |      |      |
| CodecConfigurer.DefaultCodecs             |      |      |
| HttpMessageDecoder                        |      |      |
| HttpMessageEncoder                        |      |      |
| HttpMessageReader                         |      |      |
| HttpMessageWriter                         |      |      |
| ServerCodecConfigurer                     |      |      |
| ServerCodecConfigurer.ServerDefaultCodecs |      |      |
| ServerSentEvent.Builder                   |      |      |
|                                           |      |      |
| Classes                                   |      |      |
|                                           |      |      |
| DecoderHttpMessageReader                  |      |      |
| EncoderHttpMessageWriter                  |      |      |
| FormHttpMessageReader                     |      |      |
| FormHttpMessageWriter                     |      |      |
| LoggingCodecSupport                       |      |      |
| ResourceHttpMessageReader                 |      |      |
| ResourceHttpMessageWriter                 |      |      |
| ServerSentEvent                           |      |      |
| ServerSentEventHttpMessageReader          |      |      |
| ServerSentEventHttpMessageWriter          |      |      |





##### org.springframework.http.codec.cbor



|                     |      |      |
| ------------------- | ---- | ---- |
| Classes             |      |      |
|                     |      |      |
| Jackson2CborDecoder |      |      |
| Jackson2CborEncoder |      |      |



##### org.springframework.http.codec.json



|                         |      |      |
| ----------------------- | ---- | ---- |
| Classes                 |      |      |
|                         |      |      |
| AbstractJackson2Decoder |      |      |
| AbstractJackson2Encoder |      |      |
| Jackson2CodecSupport    |      |      |
| Jackson2JsonDecoder     |      |      |
| Jackson2JsonEncoder     |      |      |
| Jackson2SmileDecoder    |      |      |
| Jackson2SmileEncoder    |      |      |



##### org.springframework.http.codec.multipart



|                                  |      |      |
| -------------------------------- | ---- | ---- |
| Interfaces                       |      |      |
|                                  |      |      |
| FilePart                         |      |      |
| FormFieldPart                    |      |      |
| Part                             |      |      |
|                                  |      |      |
| Classes                          |      |      |
|                                  |      |      |
| MultipartHttpMessageReader       |      |      |
| MultipartHttpMessageWriter       |      |      |
| SynchronossPartHttpMessageReader |      |      |



##### org.springframework.http.codec.protobuf



| org.springframework.http.codec.protobuf |      |      |
| --------------------------------------- | ---- | ---- |
| Classes                                 |      |      |
|                                         |      |      |
| ProtobufCodecSupport                    |      |      |
| ProtobufDecoder                         |      |      |
| ProtobufEncoder                         |      |      |
| ProtobufHttpMessageWriter               |      |      |



##### org.springframework.http.codec.support



| org.springframework.http.codec.support |      |      |
| -------------------------------------- | ---- | ---- |
| Classes                                |      |      |
|                                        |      |      |
| DefaultClientCodecConfigurer           |      |      |
| DefaultServerCodecConfigurer           |      |      |



##### org.springframework.http.codec.xml

| org.springframework.http.codec.xml |      |      |
| ---------------------------------- | ---- | ---- |
|                                    |      |      |
| Classes                            |      |      |
|                                    |      |      |
| Jaxb2XmlDecoder                    |      |      |
| Jaxb2XmlEncoder                    |      |      |
| XmlEventDecoder                    |      |      |



##### org.springframework.http.converter



|                                     |      |      |
| ----------------------------------- | ---- | ---- |
| Interfaces                          |      |      |
|                                     |      |      |
| GenericHttpMessageConverter         |      |      |
| HttpMessageConverter                |      |      |
|                                     |      |      |
| Classes                             |      |      |
|                                     |      |      |
| AbstractGenericHttpMessageConverter |      |      |
| AbstractHttpMessageConverter        |      |      |
| BufferedImageHttpMessageConverter   |      |      |
| ByteArrayHttpMessageConverter       |      |      |
| FormHttpMessageConverter            |      |      |
| ObjectToStringHttpMessageConverter  |      |      |
| ResourceHttpMessageConverter        |      |      |
| ResourceRegionHttpMessageConverter  |      |      |
| StringHttpMessageConverter          |      |      |
|                                     |      |      |
| Exceptions                          |      |      |
|                                     |      |      |
| HttpMessageConversionException      |      |      |
| HttpMessageNotReadableException     |      |      |
| HttpMessageNotWritableException     |      |      |



##### org.springframework.http.converter.cbor

| org.springframework.http.converter.cbor |      |      |
| --------------------------------------- | ---- | ---- |
| MappingJackson2CborHttpMessageConverter |      |      |
|                                         |      |      |
|                                         |      |      |



##### org.springframework.http.converter.feed



|                                      |      |      |
| ------------------------------------ | ---- | ---- |
| Classes                              |      |      |
|                                      |      |      |
| AbstractWireFeedHttpMessageConverter |      |      |
| AtomFeedHttpMessageConverter         |      |      |
| RssChannelHttpMessageConverter       |      |      |



##### org.springframework.http.converter.json



|                                      |      |      |
| ------------------------------------ | ---- | ---- |
| Classes                              |      |      |
|                                      |      |      |
| AbstractJackson2HttpMessageConverter |      |      |
| AbstractJsonHttpMessageConverter     |      |      |
| GsonBuilderUtils                     |      |      |
| GsonFactoryBean                      |      |      |
| GsonHttpMessageConverter             |      |      |
| Jackson2ObjectMapperBuilder          |      |      |
| Jackson2ObjectMapperFactoryBean      |      |      |
| JsonbHttpMessageConverter            |      |      |
| MappingJackson2HttpMessageConverter  |      |      |
| MappingJacksonInputMessage           |      |      |
| MappingJacksonValue                  |      |      |
| SpringHandlerInstantiator            |      |      |



##### org.springframework.http.converter.protobuf



|                                        |      |      |
| -------------------------------------- | ---- | ---- |
| Interfaces                             |      |      |
|                                        |      |      |
| ExtensionRegistryInitializer           |      |      |
|                                        |      |      |
| Classes                                |      |      |
|                                        |      |      |
| ProtobufHttpMessageConverter           |      |      |
| ProtobufJsonFormatHttpMessageConverter |      |      |



##### org.springframework.http.converter.smile



| org.springframework.http.converter.smile |      |      |
| ---------------------------------------- | ---- | ---- |
| MappingJackson2SmileHttpMessageConverter |      |      |
|                                          |      |      |
|                                          |      |      |



##### org.springframework.http.converter.support



AllEncompassingFormHttpMessageConverter



##### org.springframework.http.converter.xml



|                                        |      |      |
| -------------------------------------- | ---- | ---- |
| Classes                                |      |      |
|                                        |      |      |
| AbstractJaxb2HttpMessageConverter      |      |      |
| AbstractXmlHttpMessageConverter        |      |      |
| Jaxb2CollectionHttpMessageConverter    |      |      |
| Jaxb2RootElementHttpMessageConverter   |      |      |
| MappingJackson2XmlHttpMessageConverter |      |      |
| MarshallingHttpMessageConverter        |      |      |
| SourceHttpMessageConverter             |      |      |



#### org.springframework.http.server



|                                      |      |      |
| ------------------------------------ | ---- | ---- |
| Interfaces                           |      |      |
|                                      |      |      |
| PathContainer                        |      |      |
| PathContainer.Element                |      |      |
| PathContainer.PathSegment            |      |      |
| PathContainer.Separator              |      |      |
| RequestPath                          |      |      |
| ServerHttpAsyncRequestControl        |      |      |
| ServerHttpRequest                    |      |      |
| ServerHttpResponse                   |      |      |
|                                      |      |      |
| Classes                              |      |      |
|                                      |      |      |
| PathContainer.Options                |      |      |
| ServletServerHttpAsyncRequestControl |      |      |
| ServletServerHttpRequest             |      |      |
| ServletServerHttpResponse            |      |      |



### org.springframework.remoting



|                                  |      |      |
| -------------------------------- | ---- | ---- |
| Exceptions                       |      |      |
|                                  |      |      |
| RemoteAccessException            |      |      |
| RemoteConnectFailureException    |      |      |
| RemoteInvocationFailureException |      |      |
| RemoteLookupFailureException     |      |      |
| RemoteProxyFailureException      |      |      |
| RemoteTimeoutException           |      |      |





#### org.springframework.remoting.caucho



|                              |      |      |
| ---------------------------- | ---- | ---- |
| Classes                      |      |      |
|                              |      |      |
| HessianClientInterceptor     |      |      |
| HessianExporter              |      |      |
| HessianProxyFactoryBean      |      |      |
| HessianServiceExporter       |      |      |
| SimpleHessianServiceExporter |      |      |





#### org.springframework.remoting.httpinvoker



|                                          |      |      |
| ---------------------------------------- | ---- | ---- |
| Interfaces                               |      |      |
|                                          |      |      |
| HttpInvokerClientConfiguration           |      |      |
| HttpInvokerRequestExecutor               |      |      |
|                                          |      |      |
| Classes                                  |      |      |
|                                          |      |      |
| AbstractHttpInvokerRequestExecutor       |      |      |
| HttpComponentsHttpInvokerRequestExecutor |      |      |
| HttpInvokerClientInterceptor             |      |      |
| HttpInvokerProxyFactoryBean              |      |      |
| HttpInvokerServiceExporter               |      |      |
| SimpleHttpInvokerRequestExecutor         |      |      |
| SimpleHttpInvokerServiceExporter         |      |      |





#### org.springframework.remoting.jaxws



|                                      |      |      |
| ------------------------------------ | ---- | ---- |
| Classes                              |      |      |
|                                      |      |      |
| AbstractJaxWsServiceExporter         |      |      |
| JaxWsPortClientInterceptor           |      |      |
| JaxWsPortProxyFactoryBean            |      |      |
| LocalJaxWsServiceFactory             |      |      |
| LocalJaxWsServiceFactoryBean         |      |      |
| SimpleHttpServerJaxWsServiceExporter |      |      |
| SimpleJaxWsServiceExporter           |      |      |
|                                      |      |      |
| Exceptions                           |      |      |
|                                      |      |      |
| JaxWsSoapFaultException              |      |      |



### org.springframework.web

| org.springframework.web                | 类型      | 解释                                                         |
| -------------------------------------- | --------- | ------------------------------------------------------------ |
| Interfaces                             |           |                                                              |
| HttpRequestHandler                     | interface | void handleRequest(HttpServletRequest request, HttpServletResponse response) 子类 |
| WebApplicationInitializer              | interface | void onStartup(ServletContext servletContext)                |
|                                        |           |                                                              |
| Classes                                |           |                                                              |
| SpringServletContainerInitializer      |           | implements ServletContainerInitializer                       |
|                                        |           |                                                              |
| Exceptions                             |           |                                                              |
| HttpMediaTypeException                 | exception |                                                              |
| HttpMediaTypeNotAcceptableException    | exception |                                                              |
| HttpMediaTypeNotSupportedException     | exception |                                                              |
| HttpRequestMethodNotSupportedException | exception |                                                              |
| HttpSessionRequiredException           | exception |                                                              |



HttpRequestHandler接口子类

ResourceHttpRequestHandler (org.springframework.web.servlet.resource)
DefaultServletHttpRequestHandler (org.springframework.web.servlet.resource)
PreFlightHandler in AbstractHandlerMapping (org.springframework.web.servlet.handler)
HttpInvokerServiceExporter (org.springframework.remoting.httpinvoker)
HessianServiceExporter (org.springframework.remoting.caucho)





WebApplicationInitializer接口实现类

SpringBootServletInitializer (org.springframework.boot.web.servlet.support)
AbstractContextLoaderInitializer (org.springframework.web.context)
    AbstractDispatcherServletInitializer (org.springframework.web.servlet.support)
        AbstractAnnotationConfigDispatcherServletInitializer (org.springframework.web.servlet.support)
AbstractReactiveWebInitializer (org.springframework.web.server.adapter)
JerseyWebApplicationInitializer in JerseyAutoConfiguration (org.springframework.boot.autoconfigure.jersey)



#### org.springframework.web.accept

| org.springframework.web.accept                 |           |                                                              |
| ---------------------------------------------- | --------- | ------------------------------------------------------------ |
| Interfaces                                     |           |                                                              |
| ContentNegotiationStrategy                     | interface | List<MediaType> resolveMediaTypes(NativeWebRequest webRequest) |
| MediaTypeFileExtensionResolver                 | interface | List<String> resolveFileExtensions(MediaType mediaType); List<String> getAllFileExtensions(); |
|                                                |           |                                                              |
| Classes                                        |           |                                                              |
| AbstractMappingContentNegotiationStrategy      | abstract  | extends MappingMediaTypeFileExtensionResolver       implements ContentNegotiationStrategy |
| ContentNegotiationManager                      |           | implements ContentNegotiationStrategy, MediaTypeFileExtensionResolver |
| ContentNegotiationManagerFactoryBean           |           | implements FactoryBean<ContentNegotiationManager>, ServletContextAware, InitializingBean |
| FixedContentNegotiationStrategy                |           | implements ContentNegotiationStrategy  类比HeaderContentNegotiationStrategy ParameterContentNegotiationStrategy PathExtensionContentNegotiationStrategy ServletPathExtensionContentNegotiationStrategy |
| HeaderContentNegotiationStrategy               |           | 类比 FixedContentNegotiationStrategy ParameterContentNegotiationStrategy PathExtensionContentNegotiationStrategy ServletPathExtensionContentNegotiationStrategy |
| MappingMediaTypeFileExtensionResolver          |           | implements MediaTypeFileExtensionResolver                    |
| ParameterContentNegotiationStrategy            |           |                                                              |
| PathExtensionContentNegotiationStrategy        |           |                                                              |
| ServletPathExtensionContentNegotiationStrategy |           |                                                              |



ContentNegotiationStrategy接口实现类

FixedContentNegotiationStrategy (org.springframework.web.accept)
AbstractMappingContentNegotiationStrategy (org.springframework.web.accept)
    PathExtensionContentNegotiationStrategy (org.springframework.web.accept)
        ServletPathExtensionContentNegotiationStrategy (org.springframework.web.accept)
    ParameterContentNegotiationStrategy (org.springframework.web.accept)
ContentNegotiationManager (org.springframework.web.accept)
OptionalPathExtensionContentNegotiationStrategy in WebMvcAutoConfiguration (org.springframework.boot.autoconfigure.web.servlet)
HeaderContentNegotiationStrategy (org.springframework.web.accept)



MediaTypeFileExtensionResolver接口实现类

MappingMediaTypeFileExtensionResolver (org.springframework.web.accept)
    AbstractMappingContentNegotiationStrategy (org.springframework.web.accept)
        PathExtensionContentNegotiationStrategy (org.springframework.web.accept)
            ServletPathExtensionContentNegotiationStrategy (org.springframework.web.accept)
        ParameterContentNegotiationStrategy (org.springframework.web.accept)
ContentNegotiationManager (org.springframework.web.accept)



 这些类都是Spring MVC中用于内容协商(Content Negotiation)的策略类,它们的作用和联系如下:

1. FixedContentNegotiationStrategy:固定使用一种媒体类型进行内容协商。

2. HeaderContentNegotiationStrategy:根据请求头中的Accept头部信息进行内容协商。

3. ParameterContentNegotiationStrategy:根据请求参数中的format参数进行内容协商。 

4. PathExtensionContentNegotiationStrategy:根据请求URL的路径扩展名进行内容协商。

5. ServletPathExtensionContentNegotiationStrategy:继承自PathExtensionContentNegotiationStrategy,额外增加了ignoreAcceptHeader属性,可以忽略Accept头。

异同点:

1. 它们实现了Spring的ContentNegotiationStrategy接口,提供各自的内容协商策略。

2. Fixed直接固定一种类型;Header和Parameter根据请求信息;PathExtension根据路径解析。

联系:

1. 都可用于配置Spring MVC的内容协商策略。

2. 可以多个策略链联一起使用,形成组合策略,来综合确定最终请求的媒体类型。

3. 通过ContentNegotiationManager组合整合多个策略。

所以这些策略可以根据需要组合使用,构建完整的内容协商机制,灵活地支持RESTful服务。







#### org.springframework.web.bind

| org.springframework.web.bind | 类型 | 解释 |
| ---------------------------- | ---- | ---- |
|     Classes                         |      |      |
|        EscapedErrors                      |      | implements Errors |
|        ServletRequestDataBinder                      |      | extends WebDataBinder 见下面 |
|   ServletRequestParameterPropertyValues                           |      | extends MutablePropertyValues |
|     ServletRequestUtils                         |      |      |
|       WebDataBinder                       |      | 重要 |
|    Exceptions                          | exception |      |
|      MethodArgumentNotValidException                        | exception |      |
|     MissingMatrixVariableException                         | exception |      |
|    MissingPathVariableException                          | exception |      |
|      MissingRequestCookieException                        | exception |      |
|     MissingRequestHeaderException                         | exception |      |
|         MissingServletRequestParameterException                     | exception |      |
|        ServletRequestBindingException                      | exception |      |
| UnsatisfiedServletRequestParameterException | exception | |



ServletRequestDataBinder是Spring MVC中的一个数据绑定器,它的作用和使用场景如下:
ExtendedServletRequestDataBinder 这个类void addBindValues(MutablePropertyValues mpvs, ServletRequest request)方法才实现
1. 作用:将HTTP请求中的参数绑定到JavaBean对象。

2. 使用场景:

- Controller中的方法参数绑定
- @ModelAttribute注解的方法参数绑定
- @RequestBody/@ResponseBody注解的对象绑定

3. 与WebDataBinder的联系与区别:

- 联系:两者都是继承自AbstractDataBinder,都是数据绑定器

- 区别:
  - ServletRequestDataBinder专门用于Servlet请求参数的绑定
  - WebDataBinder为更通用的Web绑定器,可以绑定请求参数,也可以不针对请求进行绑定

所以,ServletRequestDataBinder是WebDataBinder的一个子类,专门用于Servlet请求参数(如GET/POST请求)到JavaBean的绑定,它将Servlet请求的特有信息考虑在内,而WebDataBinder则是更通用的绑定器。

在Spring MVC中,Controller方法通常需要ServletRequestDataBinder来绑定请求参数到方法参数的JavaBean中。





ServletRequestParameterPropertyValues 是 Spring Framework 中的一个类，用于从 ServletRequest 中获取属性值并封装为 PropertyValues 对象。它的作用是将 ServletRequest 中的参数值封装成 PropertyValues 对象，以便 Spring 可以将表单参数绑定到对象上，并进行数据绑定和验证等操作。

ServletRequestParameterPropertyValues 可以用于在 Spring MVC 中将表单参数绑定到对象上。在 Spring MVC 中，表单参数会以键值对的形式保存在 HttpServletRequest 对象中，并通过 DataBinder 对象进行数据绑定和验证。ServletRequestParameterPropertyValues 可以将 HttpServletRequest 对象中的参数值封装成 PropertyValues 对象，以便 DataBinder 对象进行数据绑定和验证等操作。

下面是一个使用 ServletRequestParameterPropertyValues 的例子：

```java
@Controller
@RequestMapping("/user")
public class UserController {
    @PostMapping("/register")
    public String register(HttpServletRequest request) {
        User user = new User();
        ServletRequestParameterPropertyValues propertyValues = new ServletRequestParameterPropertyValues(request);
        DataBinder dataBinder = new DataBinder(user);
        dataBinder.bind(propertyValues);
        if (dataBinder.getBindingResult().hasErrors()) {
            return "register";
        }
        userService.save(user);
        return "redirect:/user/login";
    }
}
```

在上面的例子中，我们首先创建了一个 UserController 类，并定义了一个 register() 方法，该方法接收一个 HttpServletRequest 对象。在 register() 方法中，我们首先创建了一个 User 对象，然后使用 ServletRequestParameterPropertyValues 类的构造方法将 HttpServletRequest 对象封装成 ServletRequestParameterPropertyValues 对象。接着，我们创建了一个 DataBinder 对象，并使用该对象的 bind() 方法将 ServletRequestParameterPropertyValues 对象绑定到 User 对象上。最后，我们使用 DataBinder 对象的 getBindingResult() 方法获取 BindingResult 对象，判断是否有错误，如果有错误，则返回 "register" 视图，否则保存 User 对象，并重定向到 "/user/login"。

总之，ServletRequestParameterPropertyValues 是 Spring Framework 中的一个类，用于从 ServletRequest 中获取属性值并封装为 PropertyValues 对象。它可以用于在 Spring MVC 中将表单参数绑定到对象上，并进行数据绑定和验证等操作。使用它可以方便地将 HttpServletRequest 对象中的参数值封装成 PropertyValues 对象，以便 DataBinder 对象进行数据绑定和验证等操作。



WebDataBinder 是 Spring Framework 中的一个类，用于将 HTTP 请求参数绑定到 Java 对象上。它的作用是将 HTTP 请求参数转换为 Java 对象，并进行数据验证和数据转换等操作。

WebDataBinder 可以用于在 Spring MVC 中将 HTTP 请求参数绑定到 Java 对象上。在 Spring MVC 中，HTTP 请求参数会以键值对的形式保存在 HttpServletRequest 对象中，并通过 WebDataBinder 对象进行数据绑定和验证。WebDataBinder 可以将 HTTP 请求参数转换为 Java 对象，并进行数据验证和数据转换等操作。

下面是一个使用 WebDataBinder 的例子：

```java
@Controller
@RequestMapping("/user")
public class UserController {
    @PostMapping("/register")
    public String register(@Valid User user, BindingResult bindingResult) {
        if (bindingResult.hasErrors()) {
            return "register";
        }
        userService.save(user);
        return "redirect:/user/login";
    }

    @InitBinder
    public void initBinder(WebDataBinder webDataBinder) {
        webDataBinder.addValidators(new UserValidator());
    }
}

public class UserValidator implements Validator {
    @Override
    public boolean supports(Class<?> clazz) {
        return User.class.isAssignableFrom(clazz);
    }

    @Override
    public void validate(Object target, Errors errors) {
        ValidationUtils.rejectIfEmptyOrWhitespace(errors, "username", "field.required", "Username is required.");
        ValidationUtils.rejectIfEmptyOrWhitespace(errors, "password", "field.required", "Password is required.");
    }
}
```

在上面的例子中，我们首先创建了一个 UserController 类，并定义了一个 register() 方法，该方法接收一个 @Valid User 对象和一个 BindingResult 对象。在 register() 方法中，我们首先判断 BindingResult 对象中是否有错误，如果有错误，则返回 "register" 视图，否则保存 User 对象，并重定向到 "/user/login"。接着，我们使用 @InitBinder 注解定义了一个 initBinder() 方法，该方法接收一个 WebDataBinder 对象。在 initBinder() 方法中，我们使用 webDataBinder.addValidators() 方法添加了一个 UserValidator 验证器，用于验证 User 对象的参数。

总之，WebDataBinder 是 Spring Framework 中的一个类，用于将 HTTP 请求参数绑定到 Java 对象上。它可以用于在 Spring MVC 中将 HTTP 请求参数转换为 Java 对象，并进行数据验证和数据转换等操作。使用它可以方便地将 HTTP 请求参数绑定到 Java 对象上，并进行数据验证和数据转换等操作。



#### org.springframework.web.bind.annotation

| org.springframework.web.bind.annotation | 类型       |     解释                                                         |
| --------------------------------------- | ---------- | ------------------------------------------------------------ |
| Interfaces                              |            |                                                              |
| ValueConstants                          |            | @RequestParam(required = false, defaultValue = ValueConstants.DEFAULT_NONE) |
|                                         |            |                                                              |
| Enums                                   |            |                                                              |
| RequestMethod                           |            |                                                              |
|                                         |            |                                                              |
| Annotation Types                        |            |                                                              |
| ControllerAdvice                        | @interface | 见下面                                                       |
| CookieValue                             | @interface |                                                              |
| CrossOrigin                             | @interface |                                                              |
| DeleteMapping                           | @interface |                                                              |
| ExceptionHandler                        | @interface |                                                              |
| GetMapping                              | @interface |                                                              |
| InitBinder                              | @interface |                                                              |
| Mapping                                 | @interface |                                                              |
| MatrixVariable                          | @interface |                                                              |
| ModelAttribute                          | @interface |                                                              |
| PatchMapping                            | @interface |                                                              |
| PathVariable                            | @interface |                                                              |
| PostMapping                             | @interface |                                                              |
| PutMapping                              | @interface |                                                              |
| RequestAttribute                        | @interface |                                                              |
| RequestBody                             | @interface |                                                              |
| RequestHeader                           | @interface |                                                              |
| RequestMapping                          | @interface |                                                              |
| RequestParam                            | @interface |                                                              |
| RequestPart                             | @interface |                                                              |
| ResponseBody                            | @interface |                                                              |
| ResponseStatus                          | @interface |                                                              |
| RestController                          | @interface |                                                              |
| RestControllerAdvice                    | @interface |                                                              |
| SessionAttribute                        | @interface |                                                              |
| SessionAttributes                       | @interface |                                                              |



ValueConstants 是 Spring Framework 中的一个接口，定义了一些常量，用于表示 HTTP 请求参数的默认值。它的作用是提供了一些常量，用于表示 HTTP 请求参数的默认值，方便开发人员在编写代码时使用。

ValueConstants 可以用于在 Spring MVC 中处理 HTTP 请求参数时，表示参数的默认值。在 Spring MVC 中，HTTP 请求参数可能有默认值，例如，当用户没有输入参数时，参数的值可能为 null 或空字符串。ValueConstants 接口中定义了一些常量，用于表示 HTTP 请求参数的默认值，例如，ValueConstants.DEFAULT_NONE 表示参数的默认值为 null。

下面是一个使用 ValueConstants 的例子：

```java
@Controller
@RequestMapping("/user")
public class UserController {
    @PostMapping("/register")
    public String register(@RequestParam(required = false, defaultValue = ValueConstants.DEFAULT_NONE) String username,
                           @RequestParam(required = false, defaultValue = "123456") String password) {
        User user = new User();
        user.setUsername(username);
        user.setPassword(password);
        userService.save(user);
        return "redirect:/user/login";
    }
}
```

在上面的例子中，我们首先创建了一个 UserController 类，并定义了一个 register() 方法，该方法接收两个 @RequestParam 注解的参数：username 和 password。在 @RequestParam 注解中，我们使用了 ValueConstants.DEFAULT_NONE 常量表示 username 参数的默认值为 null。接着，我们创建了一个 User 对象，并将 username 和 password 参数设置给 User 对象的对应属性，并保存 User 对象。最后，我们重定向到 "/user/login"。

总之，ValueConstants 是 Spring Framework 中的一个接口，用于表示 HTTP 请求参数的默认值。它可以用于在 Spring MVC 中处理 HTTP 请求参数时，表示参数的默认值。使用它可以方便地表示 HTTP 请求参数的默认值，并提高代码的可读性和可维护性。









@ControllerAdvice注解用于定义全局的Controller增强,它的典型使用示例如下:

1. 定义一个注解了@ControllerAdvice的类

```java
@ControllerAdvice
public class GlobalControllerExceptionHandler {

  @ExceptionHandler(value = Exception.class)
  public ResponseEntity<String> handleException(Exception ex) {
    return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(ex.getMessage()); 
  }

}
```

2. 在这个类中使用@ExceptionHandler注解定义全局的异常处理方法

3. 这样的异常处理方法会应用到所有@RequestMapping注解的Controller中

4. 也可以在@ControllerAdvice中使用其他切面注解:@InitBinder、@ModelAttribute等

5. @ControllerAdvice可以定义多个,也可以通过annotations属性指定应用到哪些Controller

综上,@ControllerAdvice定义全局的Controller增强机制,实现切面功能,包括异常处理、数据绑定等,可以应用到所有Controller中,简化重复代码。



#### org.springframework.web.bind.support

| org.springframework.web.bind.support | 类型 |  解释    |
| ------------------------------------ | ---- | ---- |
| Interfaces                           |      |      |
| SessionAttributeStore                |      |      |
| SessionStatus                        |      |      |
| WebArgumentResolver                  |      |      |
| WebBindingInitializer                |      |      |
| WebDataBinderFactory                 |      |      |
|                                      |      |      |
| Classes                              |      |      |
| ConfigurableWebBindingInitializer    |      |      |
| DefaultDataBinderFactory             |      |      |
| DefaultSessionAttributeStore         |      |      |
| SimpleSessionStatus                  |      |      |
| SpringWebConstraintValidatorFactory  |      |      |
| WebExchangeDataBinder                |      |      |
| WebRequestDataBinder                 |      |      |
|                                      |      |      |
| Exceptions                           |      |      |
| WebExchangeBindException             |      |      |
|                                      |      |      |







#### org.springframework.web.client

| org.springframework.web.client                               | 类型      |    解释                                                          |
| ------------------------------------------------------------ | --------- | ------------------------------------------------------------ |
| Interfaces                                                   |           |                                                              |
| AsyncRequestCallback                                         | interface | @Deprecated                                                  |
| AsyncRestOperations                                          |           | @Deprecated                                                  |
| RequestCallback                                              |           | void doWithRequest(ClientHttpRequest request)                |
| ResponseErrorHandler                                         |           | boolean hasError(ClientHttpResponse response) void handleError(URI url, HttpMethod method, ClientHttpResponse response) |
| ResponseExtractor<T>                                         |           | T extractData(ClientHttpResponse response) 接口实现类HttpMessageConverterExtractorr |
| RestOperations                                               |           | <T> T getForObject(String url, Class<T> responseType, Object... uriVariables) |
|                                                              |           |                                                              |
| Classes                                                      |           |                                                              |
| AsyncRestTemplate                                            |           | @Deprecated                                                  |
| DefaultResponseErrorHandler                                  |           | implements ResponseErrorHandler 类比ExtractingResponseErrorHandler |
| ExtractingResponseErrorHandler                               |           |                                                              |
| HttpMessageConverterExtractorr<T>                            |           |                                                              |
| RestTemplate                                                 |           |                                                              |
| org.springframework.web.client.RestTemplate.AcceptHeaderRequestCallback |           |                                                              |
| org.springframework.web.client.RestTemplate.HttpEntityRequestCallback |           |                                                              |
| org.springframework.web.client.RestTemplate.ResponseEntityResponseExtractor |           |                                                              |
| org.springframework.web.client.RestTemplate.HeadersExtractor |           |                                                              |
|                                                              |           |                                                              |
| Exceptions                                                   |           |                                                              |
| HttpClientErrorException                                     |           |                                                              |







HttpClientErrorException.BadRequest

HttpClientErrorException.Conflict

HttpClientErrorException.Forbidden

HttpClientErrorException.Gone

HttpClientErrorException.MethodNotAllowed

HttpClientErrorException.NotAcceptable

HttpClientErrorException.NotFound

HttpClientErrorException.TooManyRequests

HttpClientErrorException.Unauthorized

HttpClientErrorException.UnprocessableEntity

HttpClientErrorException.UnsupportedMediaType

HttpServerErrorException

HttpServerErrorException.BadGateway

HttpServerErrorException.GatewayTimeout

HttpServerErrorException.InternalServerError

HttpServerErrorException.NotImplemented

HttpServerErrorException.ServiceUnavailable

HttpStatusCodeException

ResourceAccessException

RestClientException

RestClientResponseException

UnknownContentTypeException

UnknownHttpStatusCodeException







RestTemplate是Spring提供的用于访问REST服务的客户端模板工具类,下面是一个使用RestTemplate调用REST API的示例:

1. 创建RestTemplate实例

```java 
RestTemplate restTemplate = new RestTemplate();
```

2. 使用RestTemplate调用GET请求

```java
String url = "http://example.com/api/users/{userId}";

Map<String, String> params = new HashMap<>();
params.put("userId", "1");

User user = restTemplate.getForObject(url, User.class, params);
```

3. 使用RestTemplate调用POST请求

```java
String url = "http://example.com/api/users";

User user = new User(1, "John", "password");

URI uri = restTemplate.postForLocation(url, user, User.class);
```

4. 也可以使用exchange()方法更灵活地发送请求

RestTemplate封装了与HTTP服务交互的细节,提供了多种便捷的方法来发送GET、POST等请求,获取响应结果。非常适合用来调用外部REST服务。





DefaultResponseErrorHandler  自定义404页面







org.springframework.web.client.support


RestGatewaySupport

#### org.springframework.web.context

| org.springframework.web.context   | 类型      |     解释                                                         |
| --------------------------------- | --------- | ------------------------------------------------------------ |
| Interfaces                        |           |                                                              |
| ConfigurableWebApplicationContext | interface | extends WebApplicationContext, ConfigurableApplicationContext   核心方法 void setConfigLocations(String... configLocations) String[] getConfigLocations(); |
| ConfigurableWebEnvironment        | interface | extends ConfigurableEnvironment                              |
| ServletConfigAware                | interface | extends Aware                                                |
| ServletContextAware               | interface | extends Aware                                                |
| WebApplicationContext             | interface | extends ApplicationContext                                   |
|                                   |           |                                                              |
| Classes                           |           |                                                              |
| AbstractContextLoaderInitializer  | abstract  | implements WebApplicationInitializer                         |
| ContextCleanupListener            |           | implements ServletContextListener                            |
| ContextLoader                     |           |                                                              |
| ContextLoaderListener             |           | extends ContextLoader implements ServletContextListener   web.xml中配置这个类 |
|                                   |           |                                                              |

ServletContextListener
javax.servlet.ServletContextListener
    public void contextInitialized(ServletContextEvent sce);
    public void contextDestroyed(ServletContextEvent sce);


在Spring MVC应用的web.xml文件中配置ContextLoaderListener监听器,可以实现自动装载Spring应用上下文。
具体配置方式:

```xml
<listener>
  <listener-class>
    org.springframework.web.context.ContextLoaderListener
  </listener-class>
</listener>
```

这会注册ContextLoaderListener到Servlet容器中。

它的作用是:

1. 在Web应用启动时自动创建Spring的根ApplicationContext。
2. 读取contextConfigLocation参数配置的Spring配置文件。
3. 将根ApplicationContext存储在ServletContext属性中。
4. 后续Spring MVC的DispatcherServlet等组件可以使用这个根上下文。
5. 实现了Web层服务与业务层Spring容器的集成。
所以在Spring MVC项目中,通常会配置ContextLoaderListener来自动装载Spring上下文。
这为后续的Spring MVC配置提供基础,实现Web层和服务层的无缝集成。

ContextLoader 是 Spring Framework 中的一个类，用于加载和初始化 Spring 应用程序上下文。它的作用是在 Web 应用程序中加载和初始化 Spring 应用程序上下文，并将其绑定到 ServletContext 中，使得在整个 Web 应用程序中都可以访问 Spring 应用程序上下文。

ContextLoader 可以用于在 Web 应用程序中加载和初始化 Spring 应用程序上下文。在 Web 应用程序中，Spring 应用程序上下文通常是在 ServletContextListener 或 ServletContextInitializer 中加载和初始化的。ContextLoader 类提供了一种方便的方式来加载和初始化 Spring 应用程序上下文，并将其绑定到 ServletContext 中，使得在整个 Web 应用程序中都可以访问 Spring 应用程序上下文。

下面是 ContextLoader 类的各个属性及其作用：

1. CONTEXT_CLASS_PARAM：指定 Spring 应用程序上下文的实现类，默认为 XmlWebApplicationContext。
2. CONFIG_LOCATION_PARAM：指定 Spring 应用程序上下文的配置文件路径或配置类，默认为 /WEB-INF/applicationContext.xml。
3. CONTEXT_INITIALIZER_CLASSES_PARAM：指定 Spring 应用程序上下文的初始化器类，默认为 null。
4. CONTEXT_SCOPE_PARAM：指定 Spring 应用程序上下文的作用域，默认为 WebApplicationContext.SCOPE_APPLICATION。
5. CONTEXT_ID_PARAM：指定 Spring 应用程序上下文的 ID，默认为 null。
6. CONTEXT_INITIALIZER_CLASSES_PROPERTY_NAME：用于在 ServletContext 初始化参数中指定 Spring 应用程序上下文的初始化器类的属性名，默认为 "contextInitializerClasses"。

使用 ContextLoader 可以方便地加载和初始化 Spring 应用程序上下文，并将其绑定到 ServletContext 中，使得在整个 Web 应用程序中都可以访问 Spring 应用程序上下文。可以通过设置不同的属性来自定义 Spring 应用程序上下文的实现类、配置文件路径或配置类、初始化器类、作用域和 ID 等。





ContextLoaderListener是Spring的监听器,它的主要作用是启动Web应用时自动加载Spring的上下文。

使用示例:

1. 在web.xml中配置ContextLoaderListener监听器

```xml
<listener>
    <listener-class>org.springframework.web.context.ContextLoaderListener</listener-class> 
</listener>
```

2. 还需要配置contextConfigLocation参数指定Spring配置文件位置

```xml
<context-param>
    <param-name>contextConfigLocation</param-name>
    <param-value>classpath:spring.xml</param-value>
</context-param>
```

3. 服务器启动时会自动加载spring.xml配置Spring上下文

源码解析:

ContextLoaderListener实现了ServletContextListener接口,在web应用启动时调用contextInitialized方法:

1. 根据contextConfigLocation加载Spring配置,创建WebApplicationContext实例

2. 将其存储到ServletContext属性中,名为WebApplicationContext.ROOT_WEB_APPLICATION_CONTEXT_ATTRIBUTE

3. 后续RequestContextListener和DispatcherServlet等组件就可以获取使用

所以它自动装载Spring上下文,是Spring MVC配置的基础。



##### org.springframework.web.context.annotation  

| org.springframework.web.context.annotation | 类型       |   解释   |
| ------------------------------------------ | ---------- | ---- |
| ApplicationScope                           | @interface |      |
| RequestScope                               | @interface |      |
| SessionScope                               | @interface |      |
|                                            |            |      |





@ApplicationScope、@RequestScope、@SessionScope是Spring MVC中用于声明Bean作用域的注解,它们的作用、使用场景和源码分析如下:

1. 作用:声明一个Bean的作用域,分别对应应用作用域、请求作用域和会话作用域。

2. 使用场景:

- @ApplicationScope - 声明应用级别的Bean,在整个应用生命周期内只有一个实例。

- @RequestScope - 声明请求级别的Bean,每个请求创建一个实例。

- @SessionScope - 声明会话级别的Bean,每个会话创建一个实例。

3. 源码解析:

- 这些注解实现了Spring的ScopeMetadataResolver接口,并指定了不同的作用域类型。

- 在创建Bean时,通过ScopeMetadataResolver解析出作用域类型,然后交给Scope实现实例化。

- 如WebApplicationContext会用SessionScope、RequestScope来创建Bean。

4. 使用注解注入时要开启对应作用域的代理模式。

综上,这些注解可以通过声明的方式定义Bean的作用域,避免硬编码Scope名称,使配置更清晰。





##### org.springframework.web.context.annotation  

| org.springframework.web.context.request | 类型      |     解释                                                         |
| --------------------------------------- | --------- | ------------------------------------------------------------ |
| Interfaces                              |           |                                                              |
| AsyncWebRequestInterceptor              | interface | void afterConcurrentHandlingStarted(WebRequest request)  extends WebRequestInterceptor |
| NativeWebRequest                        | interface | extends WebRequest                                           |
| RequestAttributes                       | interface |                                                              |
| WebRequest                              | interface | extends RequestAttributes                                    |
| WebRequestInterceptor                   | interface | void preHandle(WebRequest request)  void postHandle(WebRequest request, @Nullable ModelMap model)  void afterCompletion(WebRequest request, @Nullable Exception ex) |
|                                         |           |                                                              |
| Classes                                 |           |                                                              |
| AbstractRequestAttributes               | abstract  |                                                              |
| AbstractRequestAttributesScope          |           | implements Scope                                             |
| DestructionCallbackBindingListener      |           | implements HttpSessionBindingListener                        |
| FacesRequestAttributes                  |           |                                                              |
| FacesWebRequest                         |           | extends FacesRequestAttributes implements NativeWebRequest   |
| RequestContextHolder                    |           |                                                              |
| RequestContextListener                  |           |                                                              |
| RequestScope                            |           |                                                              |
| ServletRequestAttributes                |           |                                                              |
| ServletWebRequest                       |           | extends ServletRequestAttributes implements NativeWebRequest |
| SessionScope                            |           | extends AbstractRequestAttributesScope                       |
|                                         |           |                                                              |

FacesWebRequest和ServletWebRequest都是Spring中表示请求信息的类,两者的主要异同点是:

相同点:

- 两者都继承自WebRequest接口,提供获取请求参数、setAttribute等通用方法。

- 都能表示请求的上下文信息。

不同点:

- FacesWebRequest用于JSF环境,表示JSF managed bean请求。

- ServletWebRequest用于Servlet环境,表示HTTP Servlet请求。

- 获取参数的方法不同:

  - FacesWebRequest从FacesContext获取参数

  - ServletWebRequest从NativeWebRequest方法获取参数

- 属性存储范围不同:

  - FacesWebRequest存储在FacesContext

  - ServletWebRequest存储在基于Servlet的WebRequest

总结:

- 两者针对不同环境表示请求信息

- FacesWebRequest面向JSF管理Bean

- ServletWebRequest面向Servlet请求参数

- 也可以转换:FacesContextUtils.getWebRequest(FacesContext)

所以两者信息表示有重合,但又区分不同使用场景。



HttpSessionBindingEvent是Java Servlet规范中定义的一个事件类,它与HttpSession绑定或解除绑定对象时触发,主要用于监听HttpSession中对象绑定的事件。

作用:

1. 通知感兴趣的监听器对象被绑定到HttpSession或从HttpSession解除绑定的事件。

2. 可以通过这种机制感知Session中对象的绑定和解除绑定。

例子:

```java
// 实现HttpSessionBindingListener接口
public class User implements HttpSessionBindingListener {

  @Override
  public void valueBound(HttpSessionBindingEvent event) { 
    System.out.println("User bound to session");
  }

  @Override
  public void valueUnbound(HttpSessionBindingEvent event) {
    System.out.println("User removed from session");
  }

}

// 设置监听器
httpSession.setAttribute("user", new User()); 
```

使用场景:

- 监听用户登录session、购物车等重要对象被绑定到Session中的事件
- 对象从Session移除时需要清理资源或记录日志
- 了解Session中对象的生命周期变化

所以HttpSessionBindingEvent很有用,可以帮助监控Session对象的绑定情况。





##### org.springframework.web.context.request.async



| org.springframework.web.context.request.async | 类型      |       解释                                                       |
| --------------------------------------------- | --------- | ------------------------------------------------------------ |
| Interfaces                                    |           |                                                              |
| AsyncWebRequest                               | interface | extends NativeWebRequest                                     |
| CallableProcessingInterceptor                 | interface | 见下面                                                       |
| DeferredResult.DeferredResultHandler          | interface | org.springframework.web.context.request.async.DeferredResult.DeferredResultHandler 内部类 |
| DeferredResultProcessingInterceptor           | interface | 实现类见下面                                                 |
|                                               |           |                                                              |
| Classes                                       |           |                                                              |
| CallableProcessingInterceptorAdapter          | abstract  | @Deprecated                                                  |
| DeferredResult<T>                             |           |                                                              |
| DeferredResultProcessingInterceptorAdapter    | abstract  | @Deprecated                                                  |
| StandardServletAsyncWebRequest                |           | extends ServletWebRequest implements AsyncWebRequest, AsyncListener |
| TimeoutCallableProcessingInterceptor          |           | implements CallableProcessingInterceptor                     |
| TimeoutDeferredResultProcessingInterceptor    |           | implements DeferredResultProcessingInterceptor               |
| WebAsyncManager                               |           | final类，见下面                                              |
| WebAsyncTask<V>                               |           | implements BeanFactoryAware                                  |
| WebAsyncUtils                                 | abstract  | static类                                                     |
|                                               |           |                                                              |
| Exceptions                                    |           |                                                              |
| AsyncRequestTimeoutException                  |           |                                                              |



WebAsyncManager 是 Spring Framework 中的一个类，用于管理 Web 应用程序中的异步请求。它的作用是在 Web 应用程序中管理异步请求，包括 Callable 和 DeferredResult 等异步请求的处理。

WebAsyncManager 可以用于管理 Web 应用程序中的异步请求。在 Spring MVC 中，异步请求通常是通过 Callable 和 DeferredResult 来处理的。WebAsyncManager 可以用于管理这些异步请求的处理，例如，设置超时时间、拦截器等。WebAsyncManager 还可以用于在异步请求的处理过程中，共享数据和上下文，例如，将 HttpServletRequest 对象绑定到当前线程中，以便在异步请求的处理过程中访问 HttpServletRequest 对象。

下面是一个使用 WebAsyncManager 的例子：

```java
@Controller
public class MyController {
    @RequestMapping("/async")
    @ResponseBody
    public Callable<String> async() {
        return () -> {
            // 异步处理逻辑
            return "result";
        };
    }

    @RequestMapping("/async2")
    @ResponseBody
    public DeferredResult<String> async2() {
        DeferredResult<String> deferredResult = new DeferredResult<>();

        // 异步处理逻辑
        new Thread(() -> {
            try {
                Thread.sleep(5000);
                deferredResult.setResult("result");
            } catch (InterruptedException e) {
                deferredResult.setErrorResult(e.getMessage());
            }
        }).start();

        return deferredResult;
    }
}

public class MyCallableProcessingInterceptor implements CallableProcessingInterceptor {
    @Override
    public <T> void beforeConcurrentHandling(NativeWebRequest request, Callable<T> task) throws Exception {
        // 在 Callable 对象执行之前执行的操作
        log.debug("beforeConcurrentHandling");
        WebAsyncManager asyncManager = WebAsyncUtils.getAsyncManager(request);
        asyncManager.setTimeout(60 * 1000L);
        asyncManager.registerCallableInterceptors(new MyCallableProcessingInterceptor());
    }
}

public class MyDeferredResultProcessingInterceptor implements DeferredResultProcessingInterceptor {
    @Override
    public <T> void beforeConcurrentHandling(NativeWebRequest request, DeferredResult<T> deferredResult) throws Exception {
        // 在 DeferredResult 对象执行之前执行的操作
        log.debug("beforeConcurrentHandling");
        WebAsyncManager asyncManager = WebAsyncUtils.getAsyncManager(request);
        asyncManager.setTimeout(60 * 1000L);
        asyncManager.registerDeferredResultInterceptors(new MyDeferredResultProcessingInterceptor());
    }
}
```

在上面的例子中，我们创建了一个 MyController 类，并实现了两个处理异步请求的方法 async() 和 async2()，分别返回 Callable 和 DeferredResult 对象。接着，我们创建了一个 MyCallableProcessingInterceptor 类和一个 MyDeferredResultProcessingInterceptor 类，用于拦截异步请求的处理。在这两个拦截器中，我们获取了 WebAsyncManager 对象，并设置了超时时间和拦截器。

总之，WebAsyncManager 是 Spring Framework 中的一个类，用于管理 Web 应用程序中的异步请求。它可以用于设置超时时间、拦截器等，并共享数据和上下文。在处理异步请求的方法中，我们可以通过 WebAsyncUtils.getAsyncManager(request) 方法获取 WebAsyncManager 对象，并设置超时时间和拦截器等。这样可以便于管理异步请求的处理，并共享数据和上下文。





WebAsyncTask是Spring MVC中的一个接口,它代表一个异步执行的任务,主要用于异步请求处理。

作用:

1. 在Spring MVC中使用它来实现控制器的异步请求处理。

2. 通过实现该接口,可以在不同线程中执行任务,而不阻塞主线程。

使用示例:

```java
@Controller
public class AsyncController {

  @GetMapping("/async")
  public WebAsyncTask<String> asyncHandler() {
    return new WebAsyncTask<String>() {

      @Override
      public String call() throws Exception {
        // ...执行异步任务
        return "Async result";
      }
    
    };
  }

}
```

在这个示例中,我们实现了一个自定义的WebAsyncTask来处理异步请求。在call()方法中可以执行长时间运行的任务,而不会阻塞主线程。

Spring MVC会等待这个异步任务执行完成后,再向客户端返回结果。

这样可以实现控制器的异步处理,大大提高系统响应性能。



DeferredResultProcessingInterceptor接口实现类

TimeoutDeferredResultProcessingInterceptor (org.springframework.web.context.request.async)
DeferredResultProcessingInterceptorAdapter (org.springframework.web.context.request.async)
Anonymous in DeferredResult (org.springframework.web.context.request.async)
Anonymous in TestDispatcherServlet (org.springframework.test.web.servlet)



DeferredResultProcessingInterceptor 是 Spring Framework 中的一个接口，用于拦截处理异步请求的 DeferredResult 对象。它的作用是在处理异步请求时，拦截 DeferredResult 对象的执行，并在 DeferredResult 对象执行之前和之后执行一些操作。

下面是一个使用 DeferredResultProcessingInterceptor 的例子：

```java
@Configuration
public class MyConfig implements WebMvcConfigurer {
    @Override
    public void configureAsyncSupport(AsyncSupportConfigurer configurer) {
        configurer.setDefaultTimeout(60 * 1000);
        configurer.registerDeferredResultInterceptors(new MyDeferredResultProcessingInterceptor());
    }
}

public class MyDeferredResultProcessingInterceptor implements DeferredResultProcessingInterceptor {
    @Override
    public <T> void beforeConcurrentHandling(NativeWebRequest request, DeferredResult<T> deferredResult) throws Exception {
        // 在 DeferredResult 对象执行之前执行的操作
        log.debug("beforeConcurrentHandling");
    }

    @Override
    public <T> void preProcess(NativeWebRequest request, DeferredResult<T> deferredResult) throws Exception {
        // 在 DeferredResult 对象执行之前执行的操作
        log.debug("preProcess");
    }

    @Override
    public <T> void postProcess(NativeWebRequest request, DeferredResult<T> deferredResult, Object concurrentResult) throws Exception {
        // 在 DeferredResult 对象执行之后执行的操作
        log.debug("postProcess");
    }

    @Override
    public <T> boolean handleTimeout(NativeWebRequest request, DeferredResult<T> deferredResult) throws Exception {
        // 处理超时的操作
        log.debug("handleTimeout");
        return false;
    }

    @Override
    public <T> boolean handleError(NativeWebRequest request, DeferredResult<T> deferredResult, Throwable t) throws Exception {
        // 处理异常的操作
        log.debug("handleError");
        return false;
    }

    @Override
    public <T> void afterCompletion(NativeWebRequest request, DeferredResult<T> deferredResult) throws Exception {
        // 在 DeferredResult 对象执行完成之后执行的操作
        log.debug("afterCompletion");
    }
}
```

在上面的例子中，我们创建了一个 MyConfig 类，并实现了 WebMvcConfigurer 接口，并重写了 configureAsyncSupport() 方法。在 configureAsyncSupport() 方法中，我们设置了默认超时时间为 60 秒，并注册了一个 MyDeferredResultProcessingInterceptor 对象作为 DeferredResultProcessingInterceptor。接着，我们创建了一个 MyDeferredResultProcessingInterceptor 类，并实现了 DeferredResultProcessingInterceptor 接口。在 MyDeferredResultProcessingInterceptor 类中，我们实现了 DeferredResultProcessingInterceptor 接口中的各个方法，并在不同的方法中执行不同的操作，例如，在 beforeConcurrentHandling() 方法中记录日志，在 postProcess() 方法中添加 HTTP 响应头等。

与 CallableProcessingInterceptor 相比，DeferredResultProcessingInterceptor 的作用类似，都是拦截异步请求的执行，但是它们拦截的对象不同，CallableProcessingInterceptor 拦截 Callable 对象的执行，而 DeferredResultProcessingInterceptor 拦截 DeferredResult 对象的执行。另外，DeferredResultProcessingInterceptor 中的 handleTimeout() 和 handleError() 方法返回值为 boolean 类型，表示是否处理了超时或异常，而 CallableProcessingInterceptor 中的 handleTimeout() 和 handleError() 方法返回值为 Object 类型，表示处理超时或异常后的返回值。



CallableProcessingInterceptor 是 Spring Framework 中的一个接口，用于拦截处理异步请求的 Callable 对象。它的作用是在处理异步请求时，拦截 Callable 对象的执行，并在 Callable 对象执行之前和之后执行一些操作。

CallableProcessingInterceptor 可以用于在处理异步请求时，拦截 Callable 对象的执行，并在 Callable 对象执行之前和之后执行一些操作。在 Spring MVC 中，异步请求通常是通过 Callable 和 DeferredResult 来处理的。CallableProcessingInterceptor 可以用于拦截 Callable 对象的执行，例如，可以记录日志、处理异常、添加 HTTP 响应头等操作。

下面是一个使用 CallableProcessingInterceptor 的例子：

```java
@Configuration
public class MyConfig implements WebMvcConfigurer {
    @Override
    public void configureAsyncSupport(AsyncSupportConfigurer configurer) {
        configurer.setDefaultTimeout(60 * 1000);
        configurer.registerCallableInterceptors(new MyCallableProcessingInterceptor());
    }
}

public class MyCallableProcessingInterceptor implements CallableProcessingInterceptor {
    @Override
    public <T> void beforeConcurrentHandling(NativeWebRequest request, Callable<T> task) throws Exception {
        // 在 Callable 对象执行之前执行的操作
        log.debug("beforeConcurrentHandling");
    }

    @Override
    public <T> void preProcess(NativeWebRequest request, Callable<T> task) throws Exception {
        // 在 Callable 对象执行之前执行的操作
        log.debug("preProcess");
    }

    @Override
    public <T> void postProcess(NativeWebRequest request, Callable<T> task, Object concurrentResult) throws Exception {
        // 在 Callable 对象执行之后执行的操作
        log.debug("postProcess");
    }

    @Override
    public <T> Object handleTimeout(NativeWebRequest request, Callable<T> task) throws Exception {
        // 处理超时的操作
        log.debug("handleTimeout");
        return null;
    }

    @Override
    public <T> Object handleError(NativeWebRequest request, Callable<T> task, Throwable t) throws Exception {
        // 处理异常的操作
        log.debug("handleError");
        return null;
    }

    @Override
    public <T> void afterCompletion(NativeWebRequest request, Callable<T> task) throws Exception {
        // 在 Callable 对象执行完成之后执行的操作
        log.debug("afterCompletion");
    }
}
```

在上面的例子中，我们首先创建了一个 MyConfig 类，并实现了 WebMvcConfigurer 接口，并重写了 configureAsyncSupport() 方法。在 configureAsyncSupport() 方法中，我们设置了默认超时时间为 60 秒，并注册了一个 MyCallableProcessingInterceptor 对象作为 CallableProcessingInterceptor。接着，我们创建了一个 MyCallableProcessingInterceptor 类，并实现了 CallableProcessingInterceptor 接口。在 MyCallableProcessingInterceptor 类中，我们实现了 CallableProcessingInterceptor 接口中的各个方法，并在不同的方法中执行不同的操作，例如，在 beforeConcurrentHandling() 方法中记录日志，在 postProcess() 方法中添加 HTTP 响应头等。

总之，CallableProcessingInterceptor 是 Spring Framework 中的一个接口，用于拦截处理异步请求的 Callable 对象。它可以用于在处理异步请求时，拦截 Callable 对象的执行，并在 Callable 对象执行之前和之后执行一些操作。使用它可以方便地记录日志、处理异常、添加 HTTP 响应头等操作。



##### org.springframework.web.context.support

| org.springframework.web.context.support  | 类型     |     解释                                                         |
| ---------------------------------------- | -------- | ------------------------------------------------------------ |
| Classes                                  |          |                                                              |
| AbstractRefreshableWebApplicationContext | abstract |                                                              |
| AnnotationConfigWebApplicationContext    |          | implements AnnotationConfigRegistry                          |
| ContextExposingHttpServletRequest        |          | extends HttpServletRequestWrapper                            |
| GenericWebApplicationContext             |          | 跟AnnotationConfigWebApplicationContext GroovyWebApplicationContext类比 |
| GroovyWebApplicationContext              |          | ApplicationContext                                           |
| HttpRequestHandlerServlet                |          | servlet 跟LiveBeansViewServlet类比                           |
| LiveBeansViewServlet                     |          | servlet                                                      |
| RequestHandledEvent                      |          | extends ApplicationEvent                                     |
| ServletConfigPropertySource              |          | extends EnumerablePropertySource<ServletConfig>              |
| ServletContextAttributeExporter          |          |                                                              |
| ServletContextAttributeFactoryBean       |          | implements FactoryBean<Object>, ServletContextAware          |
| ServletContextAwareProcessor             |          | implements ServletContextAware                               |
| ServletContextLiveBeansView              |          | extends LiveBeansView                                        |
| ServletContextParameterFactoryBean       |          | implements FactoryBean<String>, ServletContextAware          |
| ServletContextPropertySource             |          | extends EnumerablePropertySource<ServletContext>             |
| ServletContextResource                   |          | extends AbstractFileResolvingResource implements ContextResource |
| ServletContextResourceLoader             |          | extends DefaultResourceLoader                                |
| ServletContextResourcePatternResolver    |          | extends PathMatchingResourcePatternResolver                  |
| ServletContextScope                      |          | implements Scope, DisposableBean                             |
| ServletRequestHandledEvent               |          | extends RequestHandledEvent                                  |
| SpringBeanAutowiringSupport              |          |                                                              |
| StandardServletEnvironment               |          |                                                              |
| StaticWebApplicationContext              |          | extends StaticApplicationContext<br/>       implements ConfigurableWebApplicationContext, ThemeSource |
| WebApplicationContextUtils               | abstract | static                                                       |
| WebApplicationObjectSupport              | abstract | extends ApplicationObjectSupport implements ServletContextAware |
| XmlWebApplicationContext                 |          | ApplicationContext                                           |





在Spring MVC中,WebApplicationObjectSupport是一个抽象基类,它的主要作用是:

1. 它实现了ApplicationObjectSupport接口,可以作为Web层对象的基类使用。

2. 它持有WebApplicationContext类型的应用上下文引用。

3. 子类可以通过getWebApplicationContext()方法获得对应用上下文的访问权限。

4. 可以通过setApplicationContext()注入所需的应用上下文。

5. 也可以通过initApplicationContext()初始化上下文。

示例用法:

```java
public class MyService extends WebApplicationObjectSupport {

  public void doSomething() {
    // 获取Web应用上下文
    WebApplicationContext ctx = getWebApplicationContext();
  }

}
```

这样通过继承WebApplicationObjectSupport,子类可以方便获得Web应用上下文,进行后续处理。

而不需要手动获取上下文,简化了代码。这在需要应用上下文的服务类中非常有用。

综上,WebApplicationObjectSupport主要目的是方便Web层组件获得应用上下文。



 

ApplicationEvent 子类

​    ApplicationEvent (org.springframework.context)
​        RedisKeyspaceEvent (org.springframework.data.redis.core)
​            RedisKeyExpiredEvent (org.springframework.data.redis.core)
​        ObjectMapperConfigured (springfox.documentation.schema.configuration)
​        ServiceBeanExportedEvent (org.apache.dubbo.config.spring.context.event)
​        InstanceRegisteredEvent (org.springframework.cloud.client.discovery.event)
​        SubscribedServicesChangedEvent (com.alibaba.cloud.dubbo.registry.event)
​        RefreshScopeRefreshedEvent (org.springframework.cloud.context.scope.refresh)
​        NacosDiscoveryInfoChangedEvent (com.alibaba.cloud.nacos.event)
​        RepositoriesPopulatedEvent (org.springframework.data.repository.init)
​        HeartbeatEvent (org.springframework.cloud.client.discovery.event)
​        DataSourceSchemaCreatedEvent (org.springframework.boot.autoconfigure.jdbc)
​        ServiceInstancesChangedEvent (com.alibaba.cloud.dubbo.registry.event)
​            FakeServiceInstancesChangedEvent in ReSubscribeManager (com.alibaba.cloud.dubbo.registry)
​        ServiceInstancePreRegisteredEvent (com.alibaba.cloud.dubbo.registry.event)
​        CreateVoucherAfterDeliveryOrderAutoPreSetEvent (com.wdidada.test.erp.fi.service.event)
​        CreateBaiWangInvoiceStatesQueryEvent (com.wdidada.test.erp.fi.service.event)
​        TestContextEvent (org.springframework.test.context.event)
​            AfterTestClassEvent (org.springframework.test.context.event)
​            BeforeTestExecutionEvent (org.springframework.test.context.event)
​            PrepareTestInstanceEvent (org.springframework.test.context.event)
​            AfterTestExecutionEvent (org.springframework.test.context.event)
​            BeforeTestClassEvent (org.springframework.test.context.event)
​            BeforeTestMethodEvent (org.springframework.test.context.event)
​            AfterTestMethodEvent (org.springframework.test.context.event)
​        ServiceInstancePreDeregisteredEvent (com.alibaba.cloud.dubbo.registry.event)
​        InvoiceQuerySuccessEvent (com.wdidada.test.erp.fi.support)
​        InvoiceObsSuccessEvent (com.wdidada.test.erp.fi.support)
​        WebServerInitializedEvent (org.springframework.boot.web.context)
​            ReactiveWebServerInitializedEvent (org.springframework.boot.web.reactive.context)
​            ServletWebServerInitializedEvent (org.springframework.boot.web.servlet.context)
​        PayloadApplicationEvent (org.springframework.context)
​            AvailabilityChangeEvent (org.springframework.boot.availability)
​        ApplicationContextEvent (org.springframework.context.event)
​            ContextClosedEvent (org.springframework.context.event)
​            ContextRefreshedEvent (org.springframework.context.event)
​            ContextStoppedEvent (org.springframework.context.event)
​            ContextStartedEvent (org.springframework.context.event)
​        EnvironmentChangeEvent (org.springframework.cloud.context.environment)
​        ExitCodeEvent (org.springframework.boot)
​        ParentHeartbeatEvent (org.springframework.cloud.client.discovery.event)
​        CreateVoucherAfterJmDeliveryOrderAutoPreSetEvent (com.wdidada.test.erp.fi.jiameng.event)
​        ParentContextAvailableEvent in ParentContextApplicationContextInitializer (org.springframework.boot.builder)
​        MappingContextEvent (org.springframework.data.mapping.context)
​        ServiceInstanceRegisteredEvent (com.alibaba.cloud.dubbo.registry.event)
​        SpringApplicationEvent (org.springframework.boot.context.event)
​            ApplicationContextInitializedEvent (org.springframework.boot.context.event)
​            ApplicationEnvironmentPreparedEvent (org.springframework.boot.context.event)
​            ApplicationPreparedEvent (org.springframework.boot.context.event)
​            ApplicationStartedEvent (org.springframework.boot.context.event)
​            ApplicationReadyEvent (org.springframework.boot.context.event)
​            ApplicationFailedEvent (org.springframework.boot.context.event)
​            ApplicationStartingEvent (org.springframework.boot.context.event)
​        InstancePreRegisteredEvent (org.springframework.cloud.client.discovery.event)
​        DubboBootstrapStartedEvent (com.alibaba.cloud.dubbo.bootstrap.event)
​        KeyValueEvent (org.springframework.data.keyvalue.core.event)
​            BeforeDropKeySpaceEvent in KeyValueEvent (org.springframework.data.keyvalue.core.event)
​            KeyBasedEvent in KeyValueEvent (org.springframework.data.keyvalue.core.event)
​            AfterDropKeySpaceEvent in KeyValueEvent (org.springframework.data.keyvalue.core.event)
​        RefreshEvent (org.springframework.cloud.endpoint.event)
​        RSocketServerInitializedEvent (org.springframework.boot.rsocket.context)
​        JobExecutionEvent (org.springframework.boot.autoconfigure.batch)
​        RequestHandledEvent (org.springframework.web.context.support)
​            ServletRequestHandledEvent (org.springframework.web.context.support)





在Spring MVC中,WebApplicationObjectSupport是一个抽象基类,它的主要作用是:

1. 它实现了ApplicationObjectSupport接口,可以作为Web层对象的基类使用。

2. 它持有WebApplicationContext类型的应用上下文引用。

3. 子类可以通过getWebApplicationContext()方法获得对应用上下文的访问权限。

4. 可以通过setApplicationContext()注入所需的应用上下文。

5. 也可以通过initApplicationContext()初始化上下文。

示例用法:

```java
public class MyService extends WebApplicationObjectSupport {

  public void doSomething() {
    // 获取Web应用上下文
    WebApplicationContext ctx = getWebApplicationContext();
  }

}
```

这样通过继承WebApplicationObjectSupport,子类可以方便获得Web应用上下文,进行后续处理。

而不需要手动获取上下文,简化了代码。这在需要应用上下文的服务类中非常有用。

综上,WebApplicationObjectSupport主要目的是方便Web层组件获得应用上下文。



ServletContextResource 是 Spring Framework 中的一个类，用于表示 Web 应用程序中的资源。它的作用是提供了一种方便的方式来访问 Web 应用程序中的资源，例如，静态文件、模板文件等。

ServletContextResource 可以用于访问 Web 应用程序中的资源。它可以从 ServletContext 或者 WebApplicationContext 中获取资源，并提供了一系列方法来访问资源的信息，例如，资源的 URL、输入流、文件名、大小等。

下面是一个使用 ServletContextResource 的例子：

```java
@Controller
public class MyController {
    @Autowired
    private ServletContext servletContext;

    @RequestMapping("/resource")
    public void resource(HttpServletResponse response) throws IOException {
        ServletContextResource resource = new ServletContextResource(servletContext, "/static/image.jpg");
        response.setContentType("image/jpeg");
        response.setContentLength((int) resource.contentLength());
        IOUtils.copy(resource.getInputStream(), response.getOutputStream());
    }
}
```

在上面的例子中，我们创建了一个 MyController 类，并注入了一个 ServletContext 对象。在 resource() 方法中，我们创建了一个 ServletContextResource 对象，并传入了 ServletContext 和资源的路径。接着，我们设置了响应的内容类型为 image/jpeg，并设置了响应的内容长度为资源的长度。最后，我们通过 IOUtils.copy() 方法将资源的输入流复制到响应的输出流中，以便将资源作为响应返回给客户端。

总之，ServletContextResource 是 Spring Framework 中的一个类，用于表示 Web 应用程序中的资源。它可以从 ServletContext 或者 WebApplicationContext 中获取资源，并提供了一系列方法来访问资源的信息。使用 ServletContextResource 可以方便地访问 Web 应用程序中的资源，例如，静态文件、模板文件等。





ServletContextLiveBeansView 是 Spring Framework 中的一个类，用于提供 Web 应用程序中的 bean 的实时运行状态。它的作用类似于 Spring Framework 中的 LiveBeansView，但是可以在 Web 应用程序中使用。

ServletContextLiveBeansView 可以用于提供 Web 应用程序中的 bean 的实时运行状态。它可以在 Web 应用程序中使用，通过访问 /application/beans URL 来查看当前 Web 应用程序中的 bean 的状态。ServletContextLiveBeansView 可以显示 Web 应用程序中的 bean 的名称、类型、作用域、状态等信息，并支持按名称、类型、作用域等进行过滤和搜索。

下面是一个使用 ServletContextLiveBeansView 的例子：

```java
@Configuration
public class MyConfig implements WebMvcConfigurer {
    @Bean
    public ServletRegistrationBean<ServletContextLiveBeansView> liveBeansView() {
        ServletRegistrationBean<ServletContextLiveBeansView> servletRegistrationBean = new ServletRegistrationBean<>(new ServletContextLiveBeansView());
        servletRegistrationBean.addUrlMappings("/application/beans");
        return servletRegistrationBean;
    }
}
```

在上面的例子中，我们创建了一个 MyConfig 类，并实现了 WebMvcConfigurer 接口。在 MyConfig 类中，我们创建了一个 ServletRegistrationBean 对象，并将 ServletContextLiveBeansView 实例作为参数传入。接着，我们设置了 ServletContextLiveBeansView 的 URL 映射为 /application/beans，这样我们就可以通过访问 /application/beans URL 来查看当前 Web 应用程序中的 bean 的状态。

总之，ServletContextLiveBeansView 是 Spring Framework 中的一个类，用于提供 Web 应用程序中的 bean 的实时运行状态。它可以在 Web 应用程序中使用，并通过访问 /application/beans URL 来查看当前 Web 应用程序中的 bean 的状态。使用 ServletContextLiveBeansView 可以方便地查看 Web 应用程序中的 bean 的状态，并支持按名称、类型、作用域等进行过滤和搜索。



#### org.springframework.web.cors

| org.springframework.web.cors    | 类型      |      解释                                                        |
| ------------------------------- | --------- | ------------------------------------------------------------ |
| Interfaces                      |           |                                                              |
| CorsConfigurationSource         | interface | CorsConfiguration getCorsConfiguration(HttpServletRequest request) 接口实现类 UrlBasedCorsConfigurationSource |
| CorsProcessor                   | interface | boolean processRequest(@Nullable CorsConfiguration configuration, HttpServletRequest request,     HttpServletResponse response)  接口实现类 DefaultCorsProcessor |
|                                 |           |                                                              |
| Classes                         |           |                                                              |
| CorsConfiguration               |           |                                                              |
| CorsUtils                       | abstract  |                                                              |
| DefaultCorsProcessor            |           | implements CorsProcessor                                     |
| UrlBasedCorsConfigurationSource |           | implements CorsConfigurationSource                           |



在 Spring MVC 中,org.springframework.web.cors.DefaultCorsProcessor 是一个实现了 CorsProcessor 接口的类,它的主要作用是:

1. 负责根据指定的 CORS 配置来处理 CORS 请求。

2. 判断请求是否为有效的 CORS 请求,如果是则根据配置添加相应的 CORS 响应头。

3. 内部包含一个 CorsConfigurationSource 用于获取配置。

4. 可以处理预检请求并验证是否通过。

5. 默认实现了 CORS 协议的相关规则。

使用方式:

```java
@Bean 
public CorsProcessor corsProcessor() {
  DefaultCorsProcessor processor = new DefaultCorsProcessor(corsConfigurationSource());
  return processor;
}
```

然后在过滤器中使用:

```java
CorsProcessor processor = corsProcessor();
processor.processRequest(corsRequest, response);
```

总之,DefaultCorsProcessor 是 CORS 功能默认的处理器实现类,用来根据配置来处理 CORS 流程,省去了大量实现细节。



在Spring MVC中,org.springframework.web.cors.UrlBasedCorsConfigurationSource这个类的作用是:

1. 它实现了CorsConfigurationSource接口,用于提供基于路径的CORS配置。

2. 内部包含一个map, key是路径,value是CorsConfiguration实例。

3. 根据请求路径,查找匹配的CORS配置来使用。

4. 常用来构建自定义的CORS配置源。

示例用法:

```java
UrlBasedCorsConfigurationSource configSource = new UrlBasedCorsConfigurationSource();

CorsConfiguration config = new CorsConfiguration(); 
config.setAllowCredentials(true);

configSource.registerCorsConfiguration("/api/**", config);

return configSource;
```

这里我们创建了一个UrlBasedCorsConfigurationSource的实例,并注册了一个路径对应配置的映射。

这样就可以用它来作为自定义的CORS配置源使用:

```java
@Bean
CorsConfigurationSource corsConfigSource() {
  return configSource; 
}
```

总之,UrlBasedCorsConfigurationSource允许自定义和组合CORS策略,
非常灵活。



在Spring MVC中,org.springframework.web.cors.CorsConfiguration这个类是用于配置CORS(跨域资源共享)相关选项的。其主要作用如下:

1. 用于定义CORS的各种配置参数,如允许的起始请求、允许的请求头、允许的方法等。

2. 可以设置CORS配置的映射路径,即对哪些路径生效。

3. 配置是否允许使用凭据(Credentials)。

4. 配置预检请求(preflight requests)的缓存时间。

5. 可以设置是否发送CORS请求时发送 cookies。

使用方式:

```java
@Configuration
public class CorsConfig {

  @Bean
  public WebMvcConfigurer corsConfigurer() {
    return new WebMvcConfigurer() {
      @Override
      public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/api/**")
            .allowedOrigins("http://domain2.com")
            .allowedMethods("PUT", "DELETE")
            .allowCredentials(true)
            .maxAge(3600);
      }
    };
  }
}
```

这便定义了一个对/api/**路径生效的CORS配置。

综上,CorsConfiguration用来配置CORS行为,定制CORS策略,以适应不同的跨域需求。



##### org.springframework.web.cors.reactive

| org.springframework.web.cors.reactive | 类型      | 解释     |
| ------------------------------------- | --------- | ---- |
| Interfaces                            |           |      |
| CorsConfigurationSource               | interface |      |
| CorsProcessor                         | interface |      |
|                                       |           |      |
| Classes                               |           |      |
| CorsUtils                             |           |      |
| CorsWebFilter                         |           |      |
| DefaultCorsProcessor                  |           |      |
| UrlBasedCorsConfigurationSource       |           |      |
|                                       |           |      |





#### org.springframework.web.filter

| org.springframework.web.filter     | 类型 |  解释    |
| ---------------------------------- | ---- | ---- |
|                                    |      |      |
| Classes                            |      |      |
| AbstractRequestLoggingFilter       |      |      |
| CharacterEncodingFilter            |      |      |
| CommonsRequestLoggingFilter        |      |      |
| CompositeFilter                    |      |      |
| CorsFilter                         |      |      |
| DelegatingFilterProxy              |      |      |
| FormContentFilter                  |      |      |
| ForwardedHeaderFilter              |      |      |
| GenericFilterBean                  |      |      |
| HiddenHttpMethodFilter             |      |      |
| HttpPutFormContentFilter           |      |      |
| OncePerRequestFilter               |      |      |
| RelativeRedirectFilter             |      |      |
| RequestContextFilter               |      |      |
| ServletContextRequestLoggingFilter |      |      |
| ShallowEtagHeaderFilter            |      |      |






CharacterEncodingFilter

```xml
  <filter>
    <filter-name>CharacterEncodingFilter</filter-name>
    <filter-class>org.springframework.web.filter.CharacterEncodingFilter</filter-class>
    <init-param>
      <param-name>encoding</param-name>
      <param-value>UTF-8</param-value>
    </init-param>
  </filter>
```


| org.springframework.web.filter.reactive | 类型 | 解释     |
| --------------------------------------- | ---- | ---- |
| Classes                                 |      |      |
| ForwardedHeaderFilter                   |      |      |
| HiddenHttpMethodFilter                  |      |      |
| ServerWebExchangeContextFilter          |      |      |



#### org.springframework.web.jsf

| org.springframework.web.jsf        | 类型 |   解释   |
| ---------------------------------- | ---- | ---- |
| Classes                            |      |      |
| DecoratingNavigationHandler        |      |      |
| DelegatingNavigationHandlerProxy   |      |      |
| DelegatingPhaseListenerMulticaster |      |      |
| FacesContextUtils                  |      |      |











##### org.springframework.web.jsf.el

| org.springframework.web.jsf.el       | 类型 | 解释     |
| ------------------------------------ | ---- | ---- |
| Classes                              |      |      |
| SpringBeanFacesELResolver            |      |      |
| WebApplicationContextFacesELResolver |      |      |









#### org.springframework.web.method



| org.springframework.web.method | 类型 |  解释    |
| ------------------------------ | ---- | ---- |
| Classes                        |      |      |
| ControllerAdviceBean           |      |      |
| HandlerMethod                  |      |      |
| HandlerTypePredicate           |      |      |
| HandlerTypePredicate.Builder   |      |      |





##### org.springframework.web.method.annotation

| org.springframework.web.method.annotation               | 类型 |  解释    |
| ------------------------------------------------------- | ---- | ---- |
| Classes                                                 |      |      |
| AbstractCookieValueMethodArgumentResolver               |      |      |
| AbstractNamedValueMethodArgumentResolver                |      |      |
| AbstractNamedValueMethodArgumentResolver.NamedValueInfo |      |      |
| AbstractWebArgumentResolverAdapter                      |      |      |
| ErrorsMethodArgumentResolver                            |      |      |
| ExceptionHandlerMethodResolver                          |      |      |
| ExpressionValueMethodArgumentResolver                   |      |      |
| InitBinderDataBinderFactory                             |      |      |
| MapMethodProcessor                                      |      |      |
| ModelAttributeMethodProcessor                           |      |      |
| ModelFactory                                            |      |      |
| ModelMethodProcessor                                    |      |      |
| RequestHeaderMapMethodArgumentResolver                  |      |      |
| RequestHeaderMethodArgumentResolver                     |      |      |
| RequestParamMapMethodArgumentResolver                   |      |      |
| RequestParamMethodArgumentResolver                      |      |      |
| SessionAttributesHandler                                |      |      |
| SessionStatusMethodArgumentResolver                     |      |      |
|                                                         |      |      |
| Exceptions                                              |      |      |
| MethodArgumentConversionNotSupportedException           |      |      |
| MethodArgumentTypeMismatchException                     |      |      |



##### org.springframework.web.method.support

| org.springframework.web.method.support   | 类型 |   解释   |
| ---------------------------------------- | --------- | ---- |
| Interfaces                               |           |      |
| AsyncHandlerMethodReturnValueHandler     | interface |      |
| HandlerMethodArgumentResolver            | interface |  resolveArgument()    |
| HandlerMethodReturnValueHandler          | interface |      |
| UriComponentsContributor                 | interface |      |
|                                          |           |      |
| Classes                                  |           |      |
| CompositeUriComponentsContributor        |           |      |
| HandlerMethodArgumentResolverComposite   |           |      |
| HandlerMethodReturnValueHandlerComposite |           |      |
| InvocableHandlerMethod                   |           |      |
| ModelAndViewContainer                    |           |      |



#### org.springframework.web.multipart

| org.springframework.web.multipart |   类型        |  解释    |
| --------------------------------- | --------- | ---- |
| Interfaces                        |           |      |
| MultipartFile                     | interface |      |
| MultipartHttpServletRequest       | interface |      |
| MultipartRequest                  | interface |      |
| MultipartResolver                 | interface |      |
|                                   |           |      |
| Exceptions                        |           |      |
| MaxUploadSizeExceededException    |           |      |
| MultipartException                |           |      |



##### org.springframework.web.multipart.commons

| org.springframework.web.multipart.commons       |  类型    | 解释     |
| ----------------------------------------------- | ---- | ---- |
| Classes                                         |      |      |
| CommonsFileUploadSupport                        |      |      |
| CommonsFileUploadSupport.MultipartParsingResult |      |      |
| CommonsMultipartFile                            |      |      |
| CommonsMultipartResolver                        |      |      |



    <!-- 多部分文件上传 -->
    <bean id="multipartResolver" class="org.springframework.web.multipart.commons.CommonsMultipartResolver">
        <property name="maxUploadSize" value="104857600" />
        <property name="maxInMemorySize" value="4096" />
        <property name="defaultEncoding" value="UTF-8"></property>
    </bean>

CommonsMultipartFile implements MultipartFile



##### org.springframework.web.multipart.support


| org.springframework.web.multipart.support |  类型    |   解释   |
| ----------------------------------------- | ---- | ---- |
| Classes                                   |      |      |
| AbstractMultipartHttpServletRequest       |      |      |
| ByteArrayMultipartFileEditor              |      |      |
| DefaultMultipartHttpServletRequest        |      |      |
| MultipartFilter                           |      |      |
| MultipartResolutionDelegate               |      |      |
| RequestPartServletServerHttpRequest       |      |      |
| StandardMultipartHttpServletRequest       |      |      |
| StandardServletMultipartResolver          |      |      |
| StringMultipartFileEditor                 |      |      |
|                                           |      |      |
| Exceptions                                |      |      |
| MissingServletRequestPartException        |      |      |



#### org.springframework.web.server

| org.springframework.web.server       |     类型      | 解释     |
| ------------------------------------ | --------- | ---- |
| Interfaces                           |           |      |
| ServerWebExchange                    | interface |      |
| ServerWebExchange.Builder            | interface |      |
| WebExceptionHandler                  | interface |      |
| WebFilter                            | interface |      |
| WebFilterChain                       | interface |      |
| WebHandler                           | interface |      |
| WebSession                           | interface |      |
|                                      |           |      |
| Classes                              |           |      |
| ServerWebExchangeDecorator           |           |      |
|                                      |           |      |
| Exceptions                           |           |      |
| MediaTypeNotSupportedStatusException |           |      |
| MethodNotAllowedException            |           |      |
| NotAcceptableStatusException         |           |      |
| ResponseStatusException              |           |      |
| ServerErrorException                 |           |      |
| ServerWebInputException              |           |      |
| UnsupportedMediaTypeStatusException  |           |      |







##### org.springframework.web.server.adapter  

| org.springframework.web.server.adapter |   类型   |  解释    |
| -------------------------------------- | ---- | ---- |
|                                        |      |      |
| Classes                                |      |      |
| AbstractReactiveWebInitializer         |      |      |
| DefaultServerWebExchange               |      |      |
| ForwardedHeaderTransformer             |      |      |
| HttpWebHandlerAdapter                  |      |      |
| WebHttpHandlerBuilder                  |      |      |











##### org.springframework.web.server.handler

| org.springframework.web.server.handler |   类型   | 解释     |
| -------------------------------------- | ---- | ---- |
| Classes                                |      |      |
| DefaultWebFilterChain                  |      |      |
| ExceptionHandlingWebHandler            |      |      |
| FilteringWebHandler                    |      |      |
| ResponseStatusExceptionHandler         |      |      |
| WebHandlerDecorator                    |      |      |



















##### org.springframework.web.server.i18n

| org.springframework.web.server.i18n |     类型      |  解释    |
| ----------------------------------- | --------- | ---- |
| Interfaces                          |           |      |
| LocaleContextResolver               | interface |      |
|                                     |           |      |
| Classes                             |           |      |
| AcceptHeaderLocaleContextResolver   |           |      |
| FixedLocaleContextResolver          |           |      |





##### org.springframework.web.server.session

| org.springframework.web.server.session |   类型        | 解释     |
| -------------------------------------- | --------- | ---- |
| Interfaces                             |           |      |
| WebSessionIdResolver                   | interface |      |
| WebSessionManager                      | interface |      |
| WebSessionStor                         | interface |      |
|                                        |           |      |
| Classes                                |           |      |
| CookieWebSessionIdResolver             |           |      |
| DefaultWebSessionManager               |           |      |
| HeaderWebSessionIdResolver             |           |      |
| InMemoryWebSessionStore                |           |      |



## 笔记

@RequestBody注解修饰的类

org.springframework.web.servlet.mvc.method.annotation.AbstractMessageConverterMethodArgumentResolver#readWithMessageConverters(org.springframework.http.HttpInputMessage, org.springframework.core.MethodParameter, java.lang.reflect.Type)

在这里赋值


把jackson替换成fastjson来序列化，反序列化http入参，出参

java代码

```java
@Configuration
public class HttpReqRespConfig {

        @Bean
        public HttpMessageConverters fastJsonHttpMessageConverters() {
            // 创建FastJson的配置对象
            FastJsonConfig fastJsonConfig = new FastJsonConfig();
            // 配置FastJson的相关参数

            // 创建FastJson的消息转换器
            FastJsonHttpMessageConverter converter = new FastJsonHttpMessageConverter();
            converter.setFastJsonConfig(fastJsonConfig);

            // 返回HttpMessageConverters对象
            return new HttpMessageConverters(converter);
    }

}
```


GenericHttpMessageConverter在org.springframework.web.servlet.mvc.method.annotation.AbstractMessageConverterMethodProcessor#writeWithMessageConverters(T, org.springframework.core.MethodParameter, org.springframework.http.server.ServletServerHttpRequest, org.springframework.http.server.ServletServerHttpResponse)被调用



AbstractGenericHttpMessageConverter

canRead
canWrite
public final void write(final T t, @Nullable final Type type, @Nullable MediaType contentType, HttpOutputMessage outputMessage)


org.springframework.http.converter.json.AbstractJackson2HttpMessageConverter#writeInternal

源码
```java
FastJsonHttpMessageConverter extends AbstractHttpMessageConverter<Object>//
        implements GenericHttpMessageConverter<Object>
```


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
- 当控制器方法中使用 @Valid 或 @Validated 注解时，Spring MVC 会调用 RequestResponseBodyMethodProcessor 这个参数解析器来处理请求体中的参数。
- RequestResponseBodyMethodProcessor 会使用 HttpMessageConverter 来将请求体中的内容转换为 Java 对象，并使用 WebDataBinder 来进行属性绑定和校验。
- WebDataBinder 会遍历当前参数的所有注解，如果注解是 @Validated 或注解的名字以 ‘Valid’ 开头，则使用 Validator 对象来执行校验逻辑。
- Validator 对象会使用 Bean Validation API 来对参数对象的所有字段进行校验，如果有错误，会将错误信息添加到 BindingResult 对象中。
- BindingResult 对象会被保存到 ModelAndViewContainer 对象中，以便后续使用。
- 当控制器方法中有 BindingResult 类型的参数时，Spring MVC 会调用 ErrorsMethodArgumentResolver 这个参数解析器来处理该参数。
- ErrorsMethodArgumentResolver 会从 ModelAndViewContainer 对象中获取 BindingResult 对象，并赋值给该参数。
- BindingResult 参数必须紧跟在被校验的参数后面，否则会抛出 IllegalStateException 异常。

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



## springmvc validate api

spring-context这个jar
org.springframework.validation.beanvalidation.LocalValidatorFactoryBean

LocalValidatorFactoryBean实现了ValidatorFactory接口

ValidatorContext
MessageInterpolator


`LocalValidatorFactoryBean` 是 `javax.validation` API 的一个实现，它是一个 Spring Framework 的工厂 bean，用于创建 `javax.validator.Validator` 和 `javax.validation.ValidatorFactory` 实例。

它的作用是将 `javax.validation` API 集成到 Spring 应用程序中，以便在应用程序中执行 Bean 验证和其他类型的验证。

当你在 Spring 应用程序中创建一个 `LocalValidatorFactoryBean` 实例时，它会自动配置 `javax.validation` API，并使用 Spring 的资源束机制来查找验证消息。通过使用 `LocalValidatorFactoryBean`，你可以在 Spring 应用程序中使用标准的 JSR-303（Bean Validation）注解进行验证，并处理验证错误。

需要注意的是，在使用 `LocalValidatorFactoryBean` 进行验证之前，你需要在应用程序中添加 `javax.validation` API 的依赖项，例如：

```xml
<dependency>
    <groupId>javax.validation</groupId>
    <artifactId>validation-api</artifactId>
    <version>2.0.1.Final</version>
</dependency>
```

除了上述作用，`LocalValidatorFactoryBean` 还具有其他功能，例如：

- 可以自定义 `javax.validation.ValidatorFactory` 实例的创建过程，以使用自定义的 `javax.validation.ConstraintValidatorFactory` 和 `javax.validation.MessageInterpolator` 实例。
- 可以通过 `setValidationMessageSource` 方法设置验证消息的来源。默认情况下，它使用 Spring 的 `MessageSource` 来查找资源束，并将其用于验证消息的本地化。

总之，`LocalValidatorFactoryBean` 是 Spring 框架与 `javax.validation` API 集成的核心组件之一，它提供了一种简单而强大的方式来实现 Bean 验证和其他类型的验证。


spring-boot-autoconfig

org.springframework.boot.autoconfigure.validation.ValidationAutoConfiguration#defaultValidator


springmvc validate断点
org.hibernate.validator.internal.engine.ValidatorImpl#validate


org.springframework.web.servlet.mvc.method.annotation.RequestResponseBodyMethodProcessor#resolveArgument
    org.springframework.web.servlet.mvc.method.annotation.AbstractMessageConverterMethodArgumentResolver#validateIfApplicable
        org.springframework.validation.DataBinder#validate(java.lang.Object...)
            org.springframework.boot.autoconfigure.validation.ValidatorAdapter#validate(java.lang.Object, org.springframework.validation.Errors, java.lang.Object...)
                org.springframework.validation.beanvalidation.SpringValidatorAdapter#validate(java.lang.Object, org.springframework.validation.Errors, java.lang.Object...)
                    org.hibernate.validator.internal.engine.ValidatorImpl#validate




springmvc处理validate结果
org.springframework.validation.beanvalidation.SpringValidatorAdapter#processConstraintViolations

校验结果存储在
BeanPropertyBindingResult

ta实现了Errors接口

BeanPropertyBindingResult
addError()



org.springframework.validation.FieldError
ObjectError
DefaultMessageSourceResolvable








org.springframework.web.util.UrlPathHelper
	public String getLookupPathForRequest(HttpServletRequest request, @Nullable String lookupPathAttributeName)
