# feign


Retrofit和Feign是两种常用的HTTP客户端库，用于在Java应用程序中进行服务间的通信。它们具有以下区别：
1. 基于库的选择：Retrofit是Square公司开发的库，而Feign是Netflix公司开发的库。它们在设计和实现上有一些差异。
2. 使用方式：Retrofit使用注解和接口定义API请求，通过动态代理生成具体的HTTP请求代码。开发人员需要手动定义接口和注解，以描述请求和响应的结构。Feign则更加声明式，使用接口定义API请求，但是不需要手动实现接口，而是通过运行时代理来自动创建实现。feign.ReflectiveFeign$FeignInvocationHandler.invoke()
3. 支持的协议：Retrofit主要用于处理RESTful风格的HTTP请求，并支持多种HTTP协议（如GET、POST等）。Feign则是基于Java标准的JAX-RS（Java API for RESTful Web Services）规范，并支持更多的HTTP协议和功能。
4. 整合Spring Cloud：Feign在Spring Cloud框架中得到了广泛应用，并提供了与其他Spring Cloud组件的集成，如服务发现、负载均衡等。
5. 定制化能力：由于Retrofit和Feign的设计理念和实现方式不同，它们在定制化能力上也有一些差异。Retrofit提供了更多的灵活性和可定制性，可以通过拦截器、转换器等机制来扩展和定制请求和响应的处理。Feign则提供了更多的自动化功能，并通过Spring Cloud的集成来实现更高级的功能，如服务注册、负载均衡等。
总体而言，Retrofit更适合于构建自定义的、面向RESTful API的HTTP客户端，而Feign更适合于与Spring Cloud等微服务框架集成，并且更加声明式和自动化。选择哪个库取决于您的具体需求和项目背景。


SpringCloud原理之feign.md


Spring Boot提供了一种非常方便的方式来使用Feign来实现RESTful服务之间的通信。

以下是使用Spring Boot配置Feign的步骤：

1.添加Feign依赖项
在Maven项目中，您需要添加以下依赖项：

<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-openfeign</artifactId>
</dependency>



2.启用Feign
在Spring Boot应用程序中启用Feign，您需要使用@EnableFeignClients注释：
@SpringBootApplication
@EnableFeignClients
public class MyApp {
   // ...
}
3.创建Feign客户端接口
创建一个接口，用于定义Feign客户端。该接口应该包含对远程服务的所有请求，以及所需的任何参数。例如：

@FeignClient(name = "my-service")
public interface MyServiceClient {
    @GetMapping("/users/{userId}")
    User getUserById(@PathVariable("userId") Long userId);
}


Spring Boot提供了一种非常方便的方式来使用Feign来实现RESTful服务之间的通信。

以下是使用Spring Boot配置Feign的步骤：

1.添加Feign依赖项
在Maven项目中，您需要添加以下依赖项：

php
Copy code
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-openfeign</artifactId>
</dependency>
2.启用Feign
在Spring Boot应用程序中启用Feign，您需要使用@EnableFeignClients注释：

less
Copy code
@SpringBootApplication
@EnableFeignClients
public class MyApp {
   // ...
}
3.创建Feign客户端接口
创建一个接口，用于定义Feign客户端。该接口应该包含对远程服务的所有请求，以及所需的任何参数。例如：

less
Copy code
@FeignClient(name = "my-service")
public interface MyServiceClient {
    @GetMapping("/users/{userId}")
    User getUserById(@PathVariable("userId") Long userId);
}
4.使用Feign客户端
使用Feign客户端非常简单，只需将其注入到您的代码中即可：


```java
@Service
public class MyService {
    private final MyServiceClient client;

    public MyService(MyServiceClient client) {
        this.client = client;
    }

    public User getUserById(Long userId) {
        return client.getUserById(userId);
    }
}
```



5.配置Feign客户端
您可以通过创建Feign配置类来配置Feign客户端的行为。例如，您可以使用以下配置来启用Feign的日志记录：



@Configuration
public class FeignConfig {
    @Bean
    Logger.Level feignLoggerLevel() {
        return Logger.Level.FULL;
    }
}


以上是使用Spring Boot配置Feign的基本步骤。根据您的具体需求，您可能需要进行其他配置来满足您的需求。



### feign body中自动填充参数

{
        head:{}
        body:{}
}

head部分自动填充


16:11:16.408 [main] INFO  org.springframework.cloud.openfeign.FeignClientFactoryBean : [378] - For '' URL not provided. Will try picking an instance via load-balancing. 
16:11:17.046 [main] INFO  org.springframework.cloud.openfeign.FeignClientFactoryBean : [378] - For '' URL not provided. Will try picking an instance via load-balancing.


### ribbon
spring cloud feign添加ribbon
1、引入pom依赖

2、设置负载ip列表
loadblanceclient2.ribbon.listOfServers=http://localhost:9001, http://localhost:9002

3、设置注解的name或value
@FeignClient(value = "loadblanceclient2"
        ,configuration = {LoadBlanceRequestInterceptor.class}
)



spring cloud feign打印日志 没有生效

打印日志，暂时用插值器替换
feign 插值器
FeignException
FeignClient使用@RequestLine注解, 而未配置feign自带契约Contract时, @Headers不会起作用, 而且启动项目会报错:
Method xxx not annotated with HTTP method type (ex. GET, POST)
https://blog.csdn.net/hkk666123/article/details/113964715



tutorials\feign

一个Java接口

```java
import feign.Headers;
import feign.Param;
import feign.RequestLine;
```


http协议
get 路径参数
http body
form-data
urlencoded
raw
bin



io.github.openfeign



Feign、OpenFeign及SpringCloud Feign的区别
Feign是Spring Cloud组件中一个轻量级RESTful的HTTP服务客户端，Feign内置了Ribbon，用来做客户端负载均衡，去调用服务注册中心的服务。Feign的使用方式是：使用Feign的注解定义接口，调用接口，就可以调用服务注册中心的服务。
由于 Netflix 公司不再维护feign，feign由社区维护，feign更名为 openfeign，并且项目迁移到新的仓库。后续版本仅使用“io.github.openfeign”，推荐使用该依赖。
spring-cloud-openfeign是基于openfeign进行包装，集成了SpringMVC的注解等方便SpringBoot项目开发的一个组件。

Spring Cloud OpenFeign简介
Spring Cloud OpenFeign是一个声明式的HTTP客户端，它简化了HTTP客户端的开发，使编写Web服务的客户端变得更容易。使用Spring Cloud OpenFeign，只需要创建一个接口并注解，就能很容易地调用各服务提供的HTTP接口。Spring Cloud OpenFeign基于OpenFeign实现，它除了提供声明式的 HTTP客户端外，还整合了Spring Cloud Hystrix，能够轻松实现熔断器模型。

测试的例子

https://gitee.com/edidada/openfeigndemo

https://gitee.com/edidada/springboothttpserver


doc
https://github.com/spring-cloud/spring-cloud-openfeign

https://cloud.spring.io/spring-cloud-openfeign/reference/html/


org.springframework.beans.factory.UnsatisfiedDependencyException: Error creating bean with name 'com.example.openfeigndemo.StoreClientTest': Unsatisfied dependency expressed through field 'storeClient'; nested exception is org.springframework.beans.factory.BeanCreationException: Error creating bean with name 'com.example.openfeigndemo.httprpc.StoreClient': Unexpected exception during bean creation; nested exception is java.lang.IllegalStateException: No Feign Client for loadBalancing defined. Did you forget to include spring-cloud-starter-netflix-ribbon or spring-cloud-starter-loadbalancer?


README_feign.md

https://github.com/OpenFeign/feign
https://github.com/openfeign/feign-form


POST 传输文件

openfeign_form_README.md

在 Feign 中，InvocationHandler 的默认实现是 SynchronousMethodHandler，它会将接口方法转换为对应的 HTTP 请求，并使用 Client 接口发送请求。

feign.ReflectiveFeign.FeignInvocationHandler类
  static class FeignInvocationHandler implements InvocationHandler 



## feign api doc


- feign-core
- feign-form
- feign-hyxtrix
- feign-form-spring
- feign-slf4j
- feign-hystrix

### feign-core

feign.ReflectiveAsyncFeign.AsyncFeignInvocationHandler是动态代理
    调用 feign.SynchronousMethodHandler#invoke()
        feign.SynchronousMethodHandler#executeAndDecode()
            feign.Client#execute()

debug代码，实际是LoadBalancerFeignClient #execute()

feign.Client子类feign.Client.Default使用HttpURLConnection来发起http请求

feign.Client.Default#convertResponse

注解
- Body
- Experimental
- HeaderMap
- Headers
- Param
- ueryMap
- RequestLine





feign.Target 接口
feign.Target.HardCodedTarget 内部静态接口



feign.Feign
feign.InvocationHandlerFactory.MethodHandler 接口
feign.SynchronousMethodHandler  feign.SynchronousMethodHandler#invoke 这个方法很重要，静态
feign.SynchronousMethodHandler.Factory 内部类

静态 feign.ReflectiveFeign.FeignInvocationHandler 内部类，实现InvocationHandler接口

异常
feign.FeignException
feign.RetryableException
feign.RetryableException
AsyncJoinException

请求返回
feign.Response
feign.Request




feign.Feign
feign.AsyncFeign
feign.ReflectiveFeign
feign.ReflectiveAsyncFeign



AsyncClient
feign.AsyncClient.Default
feign.AsyncClient.Pseudo



feign.Contract
feign.Contract.BaseContract
feign.DeclarativeContract



feign.Client
feign.Client.Default

feign.RequestInterceptor


feign.RequestTemplate  request的body header获取

feign.CollectionFormat
feign.QueryMapEncoder
feign.DefaultMethodHandler
AsyncResponseHandler
feign.Types
Feign 中的 Types 类提供了一些静态方法，用于获取各种类型的 Type 对象，例如获取泛型类型、获取数组类型、获取参数化类型等。Feign 使用 Java 的反射机制来解析接口定义中的泛型信息，并将其转换为对应的 Type 对象。使用 Types 类可以方便地获取这些 Type 对象，以便在 Feign 客户端中正确地处理泛型类型。
Types 类中的一些常用方法包括：
- `genericArrayType(Type componentType)`：返回表示指定组件类型的数组类型的 Type 对象。
- `parameterizedType(Class<?> rawType, Type... typeArguments)`：返回表示具有指定原始类型和类型参数的参数化类型的 Type 对象。
- `typeVariable(String name, Type... bounds)`：返回表示具有指定名称和边界的类型变量的 Type 对象。
- `wildcardType(Type[] upperBounds, Type[] lowerBounds)`：返回表示具有指定上界和下界的通配符类型的 Type 对象。
- `resolve(Type context, Class<?> contextRawType, Type toResolve)`：将指定的类型解析为在给定上下文中的实际类型，例如解析包含类型变量的参数化类型。
这些方法可以帮助我们在使用 Feign 客户端时，正确地处理各种类型的参数，避免出现类型转换错误或参数解析错误。
需要注意的是，Types 类是 Feign 内部使用的类，通常情况下不需要直接使用该类。如果您需要在 Feign 客户端中处理复杂的类型，可以参考 Feign 的官方文档中关于泛型的说明，了解如何在接口定义中正确地使用泛型。


feign.template.BodyTemplate
UriTemplate
HeaderTemplate


QueryTemplate


TemplateChunk
Expression implements TemplateChunk
Literal implements TemplateChunk
Expressions

UriUtils



#### feign.auth



| feign.auth                  | 类型 |                            |
| --------------------------- | ---- | -------------------------- |
| Base64                      |      |                            |
| BasicAuthRequestInterceptor |      | RequestInterceptor接口子类 |
|                             |      |                            |



package feign.auth;

feign.auth.Base64
feign.auth.BasicAuthRequestInterceptor implements RequestInterceptor





| feign.codec     | 类型      |      |
| --------------- | --------- | ---- |
| DecodeException |           |      |
| Decoder         | interface |      |
| Encoder         |           |      |
| ErrorDecoder    | interface |      |
| StringDecoder   |           |      |
|                 |           |      |
|                 |           |      |
|                 |           |      |
|                 |           |      |

package feign.codec;
public class DecodeException extends FeignException
    public class EncodeException extends FeignException

public interface Decoder

public interface Encoder

public interface ErrorDecoder
public class StringDecoder implements Decoder



#### feign.optionals

| feign.optionals | 类型 |      |
| --------------- | ---- | ---- |
| OptionalDecoder |      |      |
|                 |      |      |
|                 |      |      |





feign.optionals.OptionalDecoder implements Decoder



#### feign.querymap



| feign.querymap                           | 类型 |      |
| ---------------------------------------- | ---- | ---- |
| BeanQueryMapEncoder                      |      |      |
| BeanQueryMapEncoder.ObjectParamMetadata  |      |      |
| FieldQueryMapEncoder                     |      |      |
| FieldQueryMapEncoder.ObjectParamMetadata |      |      |



public class BeanQueryMapEncoder implements feign.QueryMapEncoder



| feign.stream                            |      |                   |
| --------------------------------------- | ---- | ----------------- |
| StreamDecoder                           |      | Decoder接口实现类 |
| StreamDecoder.IteratorParameterizedType |      |                   |
|                                         |      |                   |





#### feign.template



| feign.template               | 类型      |              |
| ---------------------------- | --------- | ------------ |
| BodyTemplate                 |           |              |
| Expression                   | abstract  |              |
| Expressions                  |           |              |
| Expressions.SimpleExpression |           |              |
| HeaderTemplate               |           |              |
| Literal                      |           |              |
| QueryTemplate                |           |              |
| Template                     |           |              |
| Template.ChunkTokenizer      |           |              |
| Template.EncodingOptions     | enum      |              |
| Template.ExpansionOptions    | enum      |              |
| TemplateChunk                | interface |              |
| UriTemplate                  |           | Template子类 |
| UriUtils                     |           |              |





### feign-form



| feign.form                     | 类型       |      |
| ------------------------------ | ---------- | ---- |
| ContentProcessor               | interface  |      |
| ContentType                    | enum       |      |
| FormData                       |            |      |
| FormEncoder                    |            |      |
| FormProperty                   | @interface |      |
| MultipartFormContentProcessor  |            |      |
| UrlencodedFormContentProcessor |            |      |



package feign.form;

public interface ContentProcessor
public enum ContentType
public class FormData
public class FormEncoder implements Encoder
public @interface FormProperty
public class MultipartFormContentProcessor implements ContentProcessor
public class UrlencodedFormContentProcessor implements ContentProcessor



#### feign.form.util

| feign.form.util              |      |      |
| ---------------------------- | ---- | ---- |
| CharsetUtil                  |      |      |
| PojoUtil                     |      |      |
| PojoUtil.SetAccessibleAction |      |      |



package feign.form.util;
CharsetUtil
PojoUtil





####  feign.form.multipart



| feign.form.multipart |      |      |
| -------------------- | ---- | ---- |
|                      |      |      |
|                      |      |      |
|                      |      |      |




package feign.form.multipart;

public interface Writer
public abstract class AbstractWriter implements Writer
public class ByteArrayWriter extends AbstractWriter
public class DelegateWriter extends AbstractWriter
public class FormDataWriter extends AbstractWriter
public class ManyFilesWriter extends AbstractWriter
public class ManyParametersWriter extends AbstractWriter
public class PojoWriter extends AbstractWriter
public class SingleFileWriter extends AbstractWriter
public class SingleParameterWriter extends AbstractWriter

Output


### feign-form-spring





| feign.form.spring               |      | 说明 |
| ------------------------------- | ---- | ---- |
| SpringSingleMultipartFileWriter |      |      |
| SpringManyMultipartFilesWriter  |      |      |
| SpringFormEncoder               |      |      |

public class SpringSingleMultipartFileWriter extends AbstractWriter
public class SpringManyMultipartFilesWriter extends AbstractWriter

public class SpringFormEncoder extends FormEncoder



#### feign.form.spring.converter

| feign.form.spring.converter    |      | 说明                             |
| ------------------------------ | ---- | -------------------------------- |
| ByteArrayMultipartFile         |      |                                  |
| IgnoreKeyCaseMap               |      |                                  |
| SpringManyMultipartFilesReader |      | AbstractHttpMessageConverter子类 |



package feign.form.spring.converter;


class ByteArrayMultipartFile implements MultipartFile
final class IgnoreKeyCaseMap extends HashMap<String, String>
public class SpringManyMultipartFilesReader extends AbstractHttpMessageConverter<MultipartFile[]>

### feign.hystrix



| feign.hystrix               |           |      |
| --------------------------- | --------- | ---- |
| FallbackFactory<T>          | interface |      |
| Default<T>                  |           |      |
| HystrixCapability           |           |      |
| HystrixDelegatingContract   |           |      |
| HystrixFeign                |           |      |
| HystrixFeign.Builder        |           |      |
| HystrixInvocationHandler    |           |      |
| ObservableCompletableFuture |           |      |
| SetterFactory               | interface |      |
| SetterFactory.Default       |           |      |



### spring cloud feign


org.springframework.cloud.openfeign.FeignClientFactoryBean
org.springframework.cloud.openfeign.FeignContext

org.springframework.cloud.openfeign.EnableFeignClients 注解  @Import(FeignClientsRegistrar.class)
org.springframework.cloud.openfeign.FeignClient 注解

```shell
feign.RetryableException: Connection refused: connect executing POST http://localhost:9991/httpserver/getAbc?device=1

```


编码器找不到

org.springframework.cloud.openfeign.support.SpringEncoder
org.springframework.cloud.openfeign.support.PageableSpringEncoder

`SpringEncoder` 和 `PageableSpringEncoder` 都是 Feign 中的编码器，用于将请求体转换为指定的格式，并发送到服务端。它们都是 Spring Cloud 对 Feign 的扩展，提供了对 Spring MVC 中常用的参数类型的支持，例如 `MultiValueMap`、`Pageable` 等。

`SpringEncoder` 是一个基于 Spring 的编码器，它使用 Spring 的 `HttpMessageConverter` 将请求体转换为指定的格式。默认情况下，`SpringEncoder` 支持将 Java 对象转换为 JSON 或 XML 格式的请求体。可以在 Feign 的配置类中添加以下代码，启用 `SpringEncoder` 编码器：

```java
@Configuration
public class FeignConfig {
    @Bean
    public Encoder feignEncoder() {
        return new SpringEncoder();
    }
}
```

`PageableSpringEncoder` 是一个扩展于 `SpringEncoder` 的编码器，它支持将 Spring MVC 中的 `Pageable` 对象转换为 HTTP 请求参数，并将其发送到服务端。`PageableSpringEncoder` 还支持将 Spring MVC 中的 `MultiValueMap` 对象转换为 HTTP 请求参数。可以在 Feign 的配置类中添加以下代码，启用 `PageableSpringEncoder` 编码器：

```java
@Configuration
public class FeignConfig {
    @Bean
    public Encoder feignEncoder() {
        return new PageableSpringEncoder(new SpringEncoder());
    }
}
```

在使用 `PageableSpringEncoder` 编码器时，需要在 Feign 的接口方法中使用 `Pageable` 类型的参数，例如：

```java
@GetMapping("/users")
public List<User> getUsers(@RequestParam("page") int page, @RequestParam("size") int size, Pageable pageable);
```

在发送请求时，Feign 将使用 `PageableSpringEncoder` 编码器将 `Pageable` 对象转换为 HTTP 请求参数，并发送到指定的服务端。

需要注意的是，为了正确地将 Java 对象转换为指定格式的请求体，需要在该 Java 对象的类定义中添加相应的注解，例如 `@JsonProperty`、`@JsonRootName` 等。这些注解可以告诉 `SpringEncoder` 如何将 Java 对象转换为指定格式的请求体。


```shell
feign.FeignException$NotFound: [404] during [POST] to [http://localhost:9991/httpserver/httpserver/feign/list] [OrgApi#getOrgList(OrgSearchParam)]: [{"timestamp":1689307337419,"status":404,"error":"Not Found","message":"No message available","path":"/httpserver/httpserver/feign/list"}]

```



## feign-hystrix源代码分包详解 





### 源代码分包详解 spring cloud openfeign

https://cloud.spring.io/spring-cloud-openfeign/reference/html/
v2.2.5



#### org.springframework.cloud.openfeign



| org.springframework.cloud.openfeign                      | 类型 | 解释  |
|----------------------------------------------------------| ---- | ---- |
| AnnotatedParameterProcessor                              |      |      |
| AnnotatedParameterProcessor.AnnotatedParameterContext    |      |      |
| CollectionFormat                                         |      |      |
| DefaultFeignLoggerFactory                                |      |      |
| DefaultTargeter                                          |      |      |
| EnableFeignClients                                       |  @interface    |      |
| FeignAutoConfiguration                                   |      |      |
| FeignAutoConfiguration.DefaultFeignTargeterConfiguration |      |      |
| FeignAutoConfiguration.HttpClientFeignConfiguration      |      |      |
| FeignAutoConfiguration.HystrixFeignTargeterConfiguration |      |      |
| FeignAutoConfiguration.OkHttpFeignConfiguration          |      |      |
| FeignClient                                              |   @interface   |      |
| FeignClientBuilder                                       |      |      |
| FeignClientBuilder.Builder                               |      |      |
| FeignClientFactoryBean                                   |      |      |
| FeignClientProperties                                    |      |      |
| FeignClientProperties.FeignClientConfiguration           |      |      |
| FeignClientsConfiguration                                |      |      |
| FeignClientsConfiguration.HystrixFeignConfiguration      |      |      |
| FeignClientsConfiguration.SpringPojoFormEncoder          |      |      |
| FeignClientSpecification                                 |      |      |
| FeignClientsRegistrar                                    |      |      |
| FeignClientsRegistrar.AllTypeFilter                      |      |      |
| FeignContext                                             |      |      |
| FeignErrorDecoderFactory                                 |      |      |
| FeignFormatterRegistrar                                  |      |      |
| FeignLoggerFactory                                       |      |      |
| HystrixTargeter                                     |      |      |
|    SpringQueryMap                                       |      |      |
|    Targeter                             |      |      |


FeignAutoConfiguration
定义了spring ioc中的bean
FeignContext


FeignClientsConfiguration spring ioc注解配置类

spring cloud feign
两个注解在哪儿被处理
FeignClient在
org.springframework.cloud.openfeign.FeignClientsRegistrar#registerFeignClients

EnableFeignClients在
org.springframework.cloud.openfeign.FeignClientsRegistrar#registerDefaultConfiguration


FeignClientSpecification在FeignClientsRegistrar中调用


FeignClientsRegistrar在EnableFeignClients中调用


ClassPathScanningCandidateComponentProvider scanner
scanner.addIncludeFilter(new AnnotationTypeFilter(FeignClient.class));
candidateComponents.addAll(scanner.findCandidateComponents(basePackage));

获取bean定义
ScannedGenericBeanDefinition

BeanDefinitionReaderUtils.registerBeanDefinition(holder, registry);



interface FeignLoggerFactory
DefaultFeignLoggerFactory implements FeignLoggerFactory

interface Targeter
DefaultTargeter implements Targeter

interface FallbackFactory<T>

FeignAutoConfiguration


interface FeignBuilderCustomizer


FeignCircuitBreaker

FeignCircuitBreakerDisabledConditions extends AnyNestedCondition

FeignCircuitBreakerInvocationHandler implements InvocationHandler

FeignCircuitBreakerTargeter implements Targeter
FeignClientBuilder

FeignClientFactoryBean implements FactoryBean<Object>, InitializingBean,
		ApplicationContextAware, BeanFactoryAware

@ConfigurationProperties("feign.client")
public class FeignClientProperties

@Configuration(proxyBeanMethods = false)
public class FeignClientsConfiguration

class FeignClientSpecification implements NamedContextFactory.Specification

FeignClientsRegistrar
FeignContext extends NamedContextFactory<FeignClientSpecification>

FeignErrorDecoderFactory

public interface FeignFormatterRegistrar extends FormatterRegistrar

FeignLoggerFactory
public class HttpClient5DisabledConditions extends AnyNestedCondition
class HystrixDisabledConditions extends AnyNestedCondition


class HystrixTargeter implements Targeter

interface Targeter







#### org.springframework.cloud.openfeign.annotation

| org.springframework.cloud.openfeign.annotation | 类型 |   解释   |
| ---------------------------------------------- | ---- | ---- |
| MatrixVariableParameterProcessor               |      |      |
| PathVariableParameterProcessor                 |      |      |
| QueryMapParameterProcessor                     |      |      |
| RequestHeaderParameterProcessor                |      |      |
| RequestParamParameterProcessor                 |      |      |
| RequestPartParameterProcessor                  |      |      |



都是AnnotatedParameterProcessor子类




org.springframework.cloud.openfeign包

interface AnnotatedParameterProcessor

注解
CollectionFormat
EnableFeignClients
FeignClient
SpringQueryMap





#### org.springframework.cloud.openfeign.clientconfig



| org.springframework.cloud.openfeign.clientconfig |     类型      | 解释  |
| ------------------------------------------------ | --------- | ---- |
| FeignClientConfigurer                            | interface |      |
| HttpClientFeignConfiguration                     |           |      |
| OkHttpFeignConfiguration                         |           |      |




interface FeignClientConfigurer
HttpClient5FeignConfiguration

@Configuration(proxyBeanMethods = false)
@ConditionalOnMissingBean(CloseableHttpClient.class)
public class HttpClientFeignConfiguration

@Configuration(proxyBeanMethods = false)
@ConditionalOnMissingBean(okhttp3.OkHttpClient.class)
public class OkHttpFeignConfiguration



#### org.springframework.cloud.openfeign.encoding
| org.springframework.cloud.openfeign.encoding |   类型   | 解释  |
| ----------------------------------------------- | ---- | ---- |
| BaseRequestInterceptor | abstract |      |
| FeignAcceptGzipEncodingAutoConfiguration |      |      |
| FeignAcceptGzipEncodingInterceptor |      |      |
| FeignClientEncodingProperties | | |
| FeignContentGzipEncodingAutoConfiguration | | |
| FeignContentGzipEncodingInterceptor | | |
| HttpEncoding | interface | |



public abstract class BaseRequestInterceptor implements RequestInterceptor





@ConditionalOnMissingBean(type = "okhttp3.OkHttpClient")
@AutoConfigureAfter(FeignAutoConfiguration.class)
public class FeignAcceptGzipEncodingAutoConfiguration

FeignAcceptGzipEncodingInterceptor extends BaseRequestInterceptor




@ConfigurationProperties("feign.compression.request")
public class FeignClientEncodingProperties



@ConditionalOnMissingBean(type = "okhttp3.OkHttpClient")
@ConditionalOnProperty("feign.compression.request.enabled")
@AutoConfigureAfter(FeignAutoConfiguration.class)
public class FeignContentGzipEncodingAutoConfiguration



FeignContentGzipEncodingInterceptor extends BaseRequestInterceptor

interface HttpEncoding



BaseRequestInterceptor子类

BaseRequestInterceptor (org.springframework.cloud.openfeign.encoding)
    FeignAcceptGzipEncodingInterceptor (org.springframework.cloud.openfeign.encoding)
    FeignContentGzipEncodingInterceptor (org.springframework.cloud.openfeign.encoding)






#### org.springframework.cloud.openfeign.hateoas
| org.springframework.cloud.openfeign.hateoas |   类型   |  解释   |
| ----------------------------------------------- | ---- | ---- |
|                                                 |      |      |
| FeignHalAutoConfiguration |      |      |
|                                                 |      |      |



@Configuration(proxyBeanMethods = false)
@ConditionalOnWebApplication
@ConditionalOnClass(RepresentationModel.class)
@AutoConfigureAfter({ JacksonAutoConfiguration.class,
		HttpMessageConvertersAutoConfiguration.class,
		RepositoryRestMvcAutoConfiguration.class })
public class FeignHalAutoConfiguration



#### org.springframework.cloud.openfeign.loadbalancer

| org.springframework.cloud.openfeign.loadbalancer |   类型   |  解释    |
| ------------------------------------------------ | ---- | ---- |
| DefaultFeignLoadBalancerConfiguration            |      |      |
| FeignBlockingLoadBalancerClient                  |      |      |
| FeignLoadBalancerAutoConfiguration               |      |      |
| HttpClientFeignLoadBalancerConfiguration         |      |      |
| OkHttpFeignLoadBalancerConfiguration             |      |      |
|                                                  |      |      |




@Configuration(proxyBeanMethods = false)
class DefaultFeignLoadBalancerConfiguration
public class FeignBlockingLoadBalancerClient implements Client


@Import({ HttpClientFeignLoadBalancerConfiguration.class,
		OkHttpFeignLoadBalancerConfiguration.class,
		HttpClient5FeignLoadBalancerConfiguration.class,
		DefaultFeignLoadBalancerConfiguration.class })
public class FeignLoadBalancerAutoConfiguration

@Configuration(proxyBeanMethods = false)
@ConditionalOnClass(ApacheHttp5Client.class)
@ConditionalOnBean(BlockingLoadBalancerClient.class)
@ConditionalOnProperty(value = "feign.httpclient.hc5.enabled", havingValue = "true")
@Import(HttpClient5FeignConfiguration.class)
class HttpClient5FeignLoadBalancerConfiguration



@Configuration(proxyBeanMethods = false)
@ConditionalOnClass(ApacheHttpClient.class)
@ConditionalOnBean(BlockingLoadBalancerClient.class)
@ConditionalOnProperty(value = "feign.httpclient.enabled", matchIfMissing = true)
@Conditional(HttpClient5DisabledConditions.class)
@Import(HttpClientFeignConfiguration.class)
class HttpClientFeignLoadBalancerConfiguration


LoadBalancerResponseStatusCodeException extends RetryableStatusCodeException


@Configuration(proxyBeanMethods = false)
@ConditionalOnClass(OkHttpClient.class)
@ConditionalOnProperty("feign.okhttp.enabled")
@ConditionalOnBean(BlockingLoadBalancerClient.class)
@Import(OkHttpFeignConfiguration.class)
class OkHttpFeignLoadBalancerConfiguration


OnRetryNotEnabledCondition extends AnyNestedCondition



RetryableFeignBlockingLoadBalancerClient implements Client


#### org.springframework.cloud.openfeign.ribbon


| org.springframework.cloud.openfeign.ribbon |  类型    |   解释   |
| ----------------------------------------------- | ---- | ---- |
| CachingSpringLoadBalancerFactory |      |      |
| DefaultFeignLoadBalancedConfiguration |      |      |
| FeignLoadBalancer | | |
| FeignLoadBalancer.RibbonRequest | | |
| FeignLoadBalancer.RibbonResponse | | |
| FeignRetryPolicy | | |
| FeignRetryPolicy.FeignRetryPolicyServiceInstance |      |      |
| FeignRibbonClientAutoConfiguration | | |
| HttpClientFeignLoadBalancedConfiguration | | |
| LoadBalancerFeignClient | | |
| LoadBalancerFeignClient.FeignOptionsClientConfig | | |
| OkHttpFeignLoadBalancedConfiguration | | |
| RetryableFeignLoadBalancer | | |
| RibbonResponseStatusCodeException | | |



CachingSpringLoadBalancerFactory
DefaultFeignLoadBalancedConfiguration
FeignLoadBalancer extends
		AbstractLoadBalancerAwareClient<FeignLoadBalancer.RibbonRequest, FeignLoadBalancer.RibbonResponse>



@Import({ HttpClientFeignLoadBalancedConfiguration.class,
		OkHttpFeignLoadBalancedConfiguration.class,
		HttpClient5FeignLoadBalancedConfiguration.class,
		DefaultFeignLoadBalancedConfiguration.class })
public class FeignRibbonClientAutoConfiguration



@Configuration(proxyBeanMethods = false)
@ConditionalOnClass(ApacheHttp5Client.class)
@ConditionalOnProperty(value = "feign.httpclient.hc5.enabled", havingValue = "true")
@Import(HttpClient5FeignConfiguration.class)
class HttpClient5FeignLoadBalancedConfiguration


@Configuration(proxyBeanMethods = false)
@ConditionalOnClass(ApacheHttpClient.class)
@ConditionalOnProperty(value = "feign.httpclient.enabled", matchIfMissing = true)
@Conditional(HttpClient5DisabledConditions.class)
@Import(HttpClientFeignConfiguration.class)
class HttpClientFeignLoadBalancedConfiguration


LoadBalancerFeignClient implements Client


@Configuration(proxyBeanMethods = false)
@ConditionalOnClass(OkHttpClient.class)
@ConditionalOnProperty("feign.okhttp.enabled")
@Import(OkHttpFeignConfiguration.class)
class OkHttpFeignLoadBalancedConfiguration

RetryableFeignLoadBalancer extends FeignLoadBalancer
		implements ServiceInstanceChooser

RibbonResponseStatusCodeException extends RetryableStatusCodeException


#### org.springframework.cloud.openfeign.support



| org.springframework.cloud.openfeign.support |  类型    |  解释    |
| ----------------------------------------------- | ---- | ---- |
| AbstractFormWriter | abstract |      |
| DefaultGzipDecoder |      |      |
| DefaultGzipDecoderConfiguration |      |      |
| FallbackCommand | | |
| FeignEncoderProperties | | @ConfigurationProperties("feign.encoder") |
| FeignHttpClientProperties | |  |
| FeignHttpClientProperties.Hc5Properties | |  |
| FeignUtils | |  |
| JsonFormWriter | |  |
| PageableSpringEncoder | |  |
| PageableSpringQueryMapEncoder | |  |
| PageJacksonModule | |  |
| PageJacksonModule.PageMixIn | interface |  |
| PageJacksonModule.SimplePageImpl | |  |
| ResponseEntityDecoder | | Decoder接口实现类 |
| SortJacksonModule | | Module子类 |
| SortJsonComponent | |  |
| SortJsonComponent. | |  |
| SortJsonComponent. | |  |
| SpringDecoder | |  |
| SpringDecoder. | |  |
| SpringEncoder | |  |
| SpringEncoder. | |  |
| SpringMvcContract | |  |
| SpringMvcContract.ConvertingExpander | |  |
| SpringMvcContract.ConvertingExpanderFactory | |  |
| SpringMvcContract.SimpleAnnotatedParameterContext | |  |



abstract class AbstractFormWriter extends AbstractWriter



DefaultGzipDecoder implements Decoder



@Configuration(proxyBeanMethods = false)
@ConditionalOnProperty("feign.compression.response.enabled")
// The OK HTTP client uses "transparent" compression.
// If the accept-encoding header is present, it disables transparent compression
@ConditionalOnMissingBean(type = "okhttp3.OkHttpClient")
@AutoConfigureAfter(FeignAutoConfiguration.class)
public class DefaultGzipDecoderConfiguration

class FallbackCommand<T> extends HystrixCommand<T>



@ConfigurationProperties("feign.encoder")
public class FeignEncoderProperties

@ConfigurationProperties(prefix = "feign.httpclient")
public class FeignHttpClientProperties

FeignUtils

class JsonFormWriter extends AbstractFormWriter

class PageableSpringEncoder implements Encoder
class PageableSpringQueryMapEncoder extends BeanQueryMapEncoder

class PageJacksonModule extends Module
class ResponseEntityDecoder implements Decoder
class SortJacksonModule extends Module
SortJsonComponent
class SpringDecoder implements Decoder
class SpringEncoder implements Encoder
class SpringMvcContract extends Contract.BaseContract implements ResourceLoaderAware











Feign 源码中的 `@RequestLine` 注解是通过 Feign 的编译期代码生成机制来支持的。
在使用 `@RequestLine` 注解时，Feign 会在编译期间通过 Java Annotation Processing 工具解析该注解，并根据注解中的信息生成对应的 HTTP 请求方法。
具体来说，Feign 会通过 `feign.processor.Processor` 接口定义的 `process()` 方法来处理 `@RequestLine` 注解。该接口定义了两个方法：`processAnnotation()` 和 `processMethod()`，分别用于处理类注解和方法注解。
在处理 `@RequestLine` 注解时，Feign 会首先在类上查找 `@Headers` 注解，以获取请求头信息。然后，它会解析 `@RequestLine` 注解中的请求方法、请求 URL 和请求参数信息，并生成相应的 HTTP 请求方法。
具体来说，Feign 会根据 `@RequestLine` 注解中指定的请求方法和 URL 生成一个 `RequestTemplate` 对象，并在该对象中设置请求参数信息。然后，它会将 `RequestTemplate` 对象传递给 `Target` 对象，以执行实际的 HTTP 请求。
例如，下面的代码演示了如何使用 `@RequestLine` 注解来定义一个 HTTP GET 请求：

```java
@FeignClient(name = "my-service")
public interface MyServiceClient {

    @RequestLine("GET /api/users/{userId}")
    User getUser(@Param("userId") Long userId);

}
```

在这个例子中，`@RequestLine` 注解指定了 HTTP 请求方法为 GET，请求 URL 为 `/api/users/{userId}`，其中 `{userId}` 是一个路径参数。`@Param` 注解用于指定请求参数名为 `userId`。

在编译期间，Feign 会解析这个注解，并生成一个 HTTP GET 方法，以执行实际的 HTTP 请求。生成的方法将会接受一个 `Long` 类型的参数 `userId`，并返回一个 `User` 类型的对象。

总的来说，Feign 使用编译期代码生成机制来支持 `@RequestLine` 注解。它可以帮助开发人员方便地定义 HTTP 请求方法，并自动生成相应的代码。



MatrixVariable注解
MatrixVariableParameterProcessor


feign.Contract.Default
构造函数，注册注解与注解处理器

super.registerClassAnnotation(Headers.class,
super.registerClassAnnotation(RequestLine.class,
super.registerClassAnnotation(Body.class,
super.registerClassAnnotation(Headers.class,
super.registerClassAnnotation(Param.class,
super.registerClassAnnotation(QueryMap.class,
super.registerClassAnnotation(HeaderMap.class,


自定义feign.DeclarativeContract.AnnotationProcessor 子类




public abstract class DeclarativeContract extends BaseContract {

  private final List<GuardedAnnotationProcessor> classAnnotationProcessors = new ArrayList<>();
  private final List<GuardedAnnotationProcessor> methodAnnotationProcessors = new ArrayList<>();

classAnnotationProcessors
methodAnnotationProcessors


feign.DeclarativeContract.GuardedAnnotationProcessor 私有内部类

封装了
    private final Predicate<Annotation> predicate;
    private final DeclarativeContract.AnnotationProcessor<Annotation> processor;



feign
用了注解，自定义注解处理器

java5新增的

java注解处理器对应java se中的哪个类

Java 注解处理器对应 Java SE 中的 `javax.annotation.processing` 包下的一组类和接口。

在 Java SE 中，`javax.annotation.processing` 包提供了一组 API，用于编写注解处理器。其中，最核心的接口是 `javax.annotation.processing.Processor`，它定义了一个注解处理器的基本接口。

除了 `Processor` 接口，`javax.annotation.processing` 包中还包含了许多其他的类和接口，用于协助开发者编写注解处理器。例如，`javax.annotation.processing.AbstractProcessor` 是一个抽象类，实现了 `Processor` 接口的大部分方法，可以帮助开发者更方便地编写注解处理器。另外，`javax.annotation.processing.RoundEnvironment` 接口用于表示一个编译轮次中所有的注解和元素，通过该接口，开发者可以访问到当前编译轮次中所有的注解和元素信息。

总的来说，Java 注解处理器通过实现 `javax.annotation.processing.Processor` 接口和其他相关的类和接口，可以对 Java 程序中的注解进行解析和处理。这些处理器在编译期间运行，可以帮助开发者生成额外的代码，或者进行其他的代码转换和优化操作。

public abstract class AbstractProcessor implements Processor

public interface Processor

