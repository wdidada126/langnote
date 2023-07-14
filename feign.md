# feign


Retrofit和Feign是两种常用的HTTP客户端库，用于在Java应用程序中进行服务间的通信。它们具有以下区别：

1. 基于库的选择：Retrofit是Square公司开发的库，而Feign是Netflix公司开发的库。它们在设计和实现上有一些差异。

2. 使用方式：Retrofit使用注解和接口定义API请求，通过动态代理生成具体的HTTP请求代码。开发人员需要手动定义接口和注解，以描述请求和响应的结构。Feign则更加声明式，使用接口定义API请求，但是不需要手动实现接口，而是通过运行时代理来自动创建实现。

3. 支持的协议：Retrofit主要用于处理RESTful风格的HTTP请求，并支持多种HTTP协议（如GET、POST等）。Feign则是基于Java标准的JAX-RS（Java API for RESTful Web Services）规范，并支持更多的HTTP协议和功能。

4. 整合Spring Cloud：Feign在Spring Cloud框架中得到了广泛应用，并提供了与其他Spring Cloud组件的集成，如服务发现、负载均衡等。Retrofit通常与Android应用程序结合使用，也可以与其他框架进行集成，但没有专门针对Spring Cloud的支持。

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


import feign.Headers;
import feign.Param;
import feign.RequestLine;

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
github.com/openfeign/feign-form


POST 传输文件

openfeign_form_README.md

在 Feign 中，InvocationHandler 的默认实现是 SynchronousMethodHandler，它会将接口方法转换为对应的 HTTP 请求，并使用 Client 接口发送请求。

feign.ReflectiveFeign.FeignInvocationHandler类
  static class FeignInvocationHandler implements InvocationHandler 



feign api doc


feign-core
feign-form
feign-hyxtrix
feign-form-spring
feign-slf4j


注解
Body
Experimental
HeaderMap
Headers
Param
QueryMap
RequestLine


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


feign.RequestTemplate

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

package feign.auth;

Base64
public class BasicAuthRequestInterceptor implements RequestInterceptor


package feign.codec;
public class DecodeException extends FeignException
    public class EncodeException extends FeignException

public interface Decoder

public interface Encoder


public interface ErrorDecoder
public class StringDecoder implements Decoder

feign.optionals。OptionalDecoder implements Decoder


public class BeanQueryMapEncoder implements feign.QueryMapEncoder



feign-form

package feign.form;

public interface ContentProcessor
public enum ContentType
public class FormData
public class FormEncoder implements Encoder
public @interface FormProperty
public class MultipartFormContentProcessor implements ContentProcessor
public class UrlencodedFormContentProcessor implements ContentProcessor


package feign.form.util;
CharsetUtil
PojoUtil


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


feign-form-spring

feign.form.spring
public class SpringSingleMultipartFileWriter extends AbstractWriter {
public class SpringManyMultipartFilesWriter extends AbstractWriter {

public class SpringFormEncoder extends FormEncoder {

package feign.form.spring.converter;


class ByteArrayMultipartFile implements MultipartFile {
final class IgnoreKeyCaseMap extends HashMap<String, String> {
public class SpringManyMultipartFilesReader extends AbstractHttpMessageConverter<MultipartFile[]> {
