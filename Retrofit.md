# Retrofit

### 封装成spring boot starter

com.github.lianjiatech.retrofit.spring.boot.annotation

com.github.lianjiatech.retrofit.spring.boot.config

com.github.lianjiatech.retrofit.spring.boot.core

com.github.lianjiatech.retrofit.spring.boot.degrade

com.github.lianjiatech.retrofit.spring.boot.exception

com.github.lianjiatech.retrofit.spring.boot.interceptor

com.github.lianjiatech.retrofit.spring.boot.retry

com.github.lianjiatech.retrofit.spring.boot.util




        <dependency>
            <groupId>com.github.lianjiatech</groupId>
            <artifactId>retrofit-spring-boot-starter</artifactId>
            <version>2.2.16</version>
        </dependency>



| com.github.lianjiatech.retrofit.spring.boot.annotation |      |      |
| ------------------------------------------------------ | ---- | ---- |
| Intercept                                              |      |      |
| InterceptMark                                          |      |      |
| Intercepts                                             |      |      |
| OkHttpClientBuilder                                    |      |      |
| RetrofitClient                                         |      |      |
| RetrofitScan                                           |      |      |



| com.github.lianjiatech.retrofit.spring.boot.config |      |      |
| -------------------------------------------------- | ---- | ---- |
| DegradeProperty                                    |      |      |
| LogProperty                                        |      |      |
| PoolConfig                                         |      |      |
| RetrofitAutoConfiguration                          |      |      |
| RetrofitConfigBean                                 |      |      |
| RetrofitProperties                                 |      |      |
| RetryProperty                                      |      |      |



| com.github.lianjiatech.retrofit.spring.boot.core |      |      |
| ------------------------------------------------ | ---- | ---- |
|                                                  |      |      |
|                                                  |      |      |
|                                                  |      |      |



| com.github.lianjiatech.retrofit.spring.boot.degrade |      |      |
| --------------------------------------------------- | ---- | ---- |
| AutoConfiguredRetrofitScannerRegistrar              |      |      |
| BasicTypeConverterFactory                           |      |      |
| BasicTypeConverterFactory.BooleanResponseConverter  |      |      |
| BasicTypeConverterFactory.DoubleResponseConverter   |      |      |
| BasicTypeConverterFactory.FloatResponseConverter    |      |      |
| BasicTypeConverterFactory.IntegerResponseConverter  |      |      |
| BasicTypeConverterFactory.LongResponseConverter     |      |      |
| BasicTypeConverterFactory.StringResponseConverter   |      |      |
| BodyCallAdapterFactory                              |      |      |
| BodyCallAdapterFactory.BodyCallAdapter              |      |      |
|                                                     |      |      |
|                                                     |      |      |



| com.github.lianjiatech.retrofit.spring.boot.exception |      |      |
| ----------------------------------------------------- | ---- | ---- |
|                                                       |      |      |
|                                                       |      |      |
|                                                       |      |      |



| com.github.lianjiatech.retrofit.spring.boot.interceptor |      |      |
| ------------------------------------------------------- | ---- | ---- |
|                                                         |      |      |
|                                                         |      |      |
|                                                         |      |      |



| com.github.lianjiatech.retrofit.spring.boot.retry |      |      |
| ------------------------------------------------- | ---- | ---- |
|                                                   |      |      |
|                                                   |      |      |
|                                                   |      |      |



| com.github.lianjiatech.retrofit.spring.boot.util |      |      |
| ------------------------------------------------ | ---- | ---- |
|                                                  |      |      |
|                                                  |      |      |
|                                                  |      |      |




com.github.lianjiatech.retrofit.spring.boot.core.RetrofitFactoryBean#getObject

核心类

作用是把retrofit 接口的动态代理类注入spring容器

https://github.com/edidada/retrofit-spring-boot-starter





AutoConfiguredRetrofitScannerRegistrar



RetrofitConfigBean





注意spring boot 2
spring boot 3的区别

https://gitee.com/edidada/testspringbootretrofit

### retrofit vs retrofit spring boot starter

retrofit
```java
        @POST(UrlConstant.BAIWANG_ET_INVOICE_RED_INFO)
        Call<Result<InvoiceRedInfoResult>> applyInvoiceRedInfo4(@HeaderMap Map<String, String> headers, @Body InvoiceRedInfoParam invoiceRedInfoParam);

        @POST(UrlConstant.BAIWANG_ET_INVOICE_RED_INFO)
        Observable<Result<InvoiceRedInfoResult>> applyInvoiceRedInfo5(@HeaderMap Map<String, String> headers, @Body InvoiceRedInfoParam invoiceRedInfoParam);
```


retrofit spring boot starter
```java

        @POST(UrlConstant.BAIWANG_ET_INVOICE_RED_INFO)
        Result<InvoiceRedInfov252Result> applyInvoiceRedInfo3(@HeaderMap Map<String, String> headers, @Body InvoiceRedInfoParam invoiceRedInfoParam);
```

https://gitee.com/edidada/retrofitdemo

cn.wdidada.test.retrofitdemo.adapter.BodyCallAdapterFactory 这个类要记住

Retrofit

使用
okio
okhttp



https://www.jianshu.com/p/1f3b646db6d5


```shell
"D:\Program Files\Java\jdk-1.8\bin\java.exe" "-javaagent:D:\dev_tools\JetBrains\IntelliJ IDEA 2023.1.1\lib\idea_rt.jar=56594:D:\dev_tools\JetBrains\IntelliJ IDEA 2023.1.1\bin" -Dfile.encoding=UTF-8 -classpath "D:\Program Files\Java\jdk-1.8\jre\lib\charsets.jar;D:\Program Files\Java\jdk-1.8\jre\lib\deploy.jar;D:\Program Files\Java\jdk-1.8\jre\lib\ext\access-bridge-64.jar;D:\Program Files\Java\jdk-1.8\jre\lib\ext\cldrdata.jar;D:\Program Files\Java\jdk-1.8\jre\lib\ext\dnsns.jar;D:\Program Files\Java\jdk-1.8\jre\lib\ext\jaccess.jar;D:\Program Files\Java\jdk-1.8\jre\lib\ext\jfxrt.jar;D:\Program Files\Java\jdk-1.8\jre\lib\ext\localedata.jar;D:\Program Files\Java\jdk-1.8\jre\lib\ext\nashorn.jar;D:\Program Files\Java\jdk-1.8\jre\lib\ext\sunec.jar;D:\Program Files\Java\jdk-1.8\jre\lib\ext\sunjce_provider.jar;D:\Program Files\Java\jdk-1.8\jre\lib\ext\sunmscapi.jar;D:\Program Files\Java\jdk-1.8\jre\lib\ext\sunpkcs11.jar;D:\Program Files\Java\jdk-1.8\jre\lib\ext\zipfs.jar;D:\Program Files\Java\jdk-1.8\jre\lib\javaws.jar;D:\Program Files\Java\jdk-1.8\jre\lib\jce.jar;D:\Program Files\Java\jdk-1.8\jre\lib\jfr.jar;D:\Program Files\Java\jdk-1.8\jre\lib\jfxswt.jar;D:\Program Files\Java\jdk-1.8\jre\lib\jsse.jar;D:\Program Files\Java\jdk-1.8\jre\lib\management-agent.jar;D:\Program Files\Java\jdk-1.8\jre\lib\plugin.jar;D:\Program Files\Java\jdk-1.8\jre\lib\resources.jar;D:\Program Files\Java\jdk-1.8\jre\lib\rt.jar;D:\code_repo\IdeaProjects\retrofitdemo\target\classes;D:\Maven_Repository\qy\com\squareup\retrofit2\converter-jackson\2.4.0\converter-jackson-2.4.0.jar;D:\Maven_Repository\qy\com\fasterxml\jackson\core\jackson-databind\2.9.4\jackson-databind-2.9.4.jar;D:\Maven_Repository\qy\com\fasterxml\jackson\core\jackson-annotations\2.9.0\jackson-annotations-2.9.0.jar;D:\Maven_Repository\qy\com\fasterxml\jackson\core\jackson-core\2.9.4\jackson-core-2.9.4.jar;D:\Maven_Repository\qy\com\squareup\retrofit2\retrofit\2.4.0\retrofit-2.4.0.jar;D:\Maven_Repository\qy\com\squareup\okhttp3\okhttp\3.10.0\okhttp-3.10.0.jar;D:\Maven_Repository\qy\com\squareup\okio\okio\1.14.0\okio-1.14.0.jar" cn.wdidada.test.retrofitdemo.Main
Exception in thread "main" java.lang.IllegalArgumentException: Unable to create converter for cn.wdidada.test.retrofitdemo.domain.BaseResult<cn.wdidada.test.retrofitdemo.domain.UserInfoData>
    for method APIService.login
	at retrofit2.ServiceMethod$Builder.methodError(ServiceMethod.java:755)
	at retrofit2.ServiceMethod$Builder.createResponseConverter(ServiceMethod.java:741)
	at retrofit2.ServiceMethod$Builder.build(ServiceMethod.java:172)
	at retrofit2.Retrofit.loadServiceMethod(Retrofit.java:170)
	at retrofit2.Retrofit$1.invoke(Retrofit.java:147)
	at com.sun.proxy.$Proxy0.login(Unknown Source)
	at cn.wdidada.test.retrofitdemo.Main.main(Main.java:18)
Caused by: java.lang.IllegalArgumentException: Could not locate ResponseBody converter for cn.wdidada.test.retrofitdemo.domain.BaseResult<cn.wdidada.test.retrofitdemo.domain.UserInfoData>.
  Tried:
   * retrofit2.BuiltInConverters
	at retrofit2.Retrofit.nextResponseBodyConverter(Retrofit.java:351)
	at retrofit2.Retrofit.responseBodyConverter(Retrofit.java:313)
	at retrofit2.ServiceMethod$Builder.createResponseConverter(ServiceMethod.java:739)
	... 5 more

Process finished with exit code 1
```

解决：

```java
        Retrofit retrofit=new Retrofit.Builder()
                .baseUrl(baseurl)
                .addConverterFactory(JacksonConverterFactory.create())
                .build();
```


```shell
java.lang.IllegalArgumentException: Unable to create call adapter for
for method HttpApiV252.applyInvoiceRedInfo

	at retrofit2.Utils.methodError(Utils.java:54)
	at retrofit2.HttpServiceMethod.createCallAdapter(HttpServiceMethod.java:116)
	at retrofit2.HttpServiceMethod.parseAnnotations(HttpServiceMethod.java:67)
	at retrofit2.ServiceMethod.parseAnnotations(ServiceMethod.java:39)
	at retrofit2.Retrofit.loadServiceMethod(Retrofit.java:202)
	at retrofit2.Retrofit$1.invoke(Retrofit.java:160)
	at com.sun.proxy.$Proxy136.applyInvoiceRedInfo(Unknown Source)
```


DefaultCallAdapterFactory
CompletableFutureCallAdapterFactory

问题：
retrofit源代码 如何生成http param headers body
retrofit源代码  如何解析http response



在 Retrofit 2.4.0 的源代码中，`@FormUrlEncoded` 注解的处理逻辑主要位于 `FormUrlEncodedConverterFactory` 类中。该类是 `Converter.Factory` 接口的实现类，用于处理表单 URL 编码的请求。

在 `FormUrlEncodedConverterFactory` 类中，当解析请求注解时，会判断方法是否使用了 `@FormUrlEncoded` 注解。如果使用了该注解，就会创建一个 `FormUrlEncodedRequestBody` 对象，并将其添加到请求的 `Call` 中。`FormUrlEncodedRequestBody` 是一个特殊的请求体，用于将请求参数编码为表单 URL 编码格式。

具体的实现细节可以在 `FormUrlEncodedConverterFactory` 类的源代码中找到。您可以查看该类的 `RequestBodyConverter` 实现，了解它是如何解析方法参数并生成表单 URL 编码的请求体的。

请注意，以上是对 Retrofit 2.4.0 源代码中 `@FormUrlEncoded` 注解处理的大致描述。具体的实现细节可能会有所变化，具体还需根据您所使用的 Retrofit 版本来查看源代码来获取准确的信息。




Java doc

https://square.github.io/retrofit/2.x/retrofit/

retrofit2包下面的类

Call
CallAdapter
CallAdapter.Factory
Callback
Converter
Converter.Factory

HttpException
Invocation

Response
Retrofit
Retrofit.Builder
SkipCallbackExecutor



retrofit2.http

Body

DELETE
Field
FieldMap
FormUrlEncoded
GET
HEAD
Header
HeaderMap
Headers
HTTP

Multipart
OPTIONS
Part
PartMap
PATCH
Path
POST
PUT
Query
QueryMap
QueryName

Streaming
Tag
Url

retrofit2.internal





OkHttpCall
ServiceMethod  parseParameterAnnotation()
retrofit2.ParameterHandler 子类 retrofit2.ParameterHandler.HeaderMap   retrofit2.ParameterHandler.Body


`ParameterHandler` 及其子类是 Retrofit2 中用于处理 HTTP 请求参数的类。Retrofit2 是一个基于 OkHttp 的 RESTful HTTP 网络请求库，它允许您将 HTTP API 转换为 Java 接口。

在 Retrofit2 中，参数处理程序负责将 Java 方法参数转换为 HTTP 请求的查询参数、表单参数、请求体等。Retrofit2 提供了以下几种参数处理程序：

- `Query`：用于将 Java 方法参数转换为查询参数。
- `Field`：用于将 Java 方法参数转换为表单字段。
- `Part`：用于将 Java 方法参数转换为 `multipart` 请求体的一部分。
- `Body`：用于将 Java 方法参数转换为请求体。
- `Header`：用于将 Java 方法参数转换为请求头。
- `Path`：用于将 Java 方法参数转换为 URL 路径参数。

这些参数处理程序被封装在 `retrofit2.ParameterHandler` 抽象类及其具体实现类中，您可以根据需要选择适当的处理程序来处理 HTTP 请求参数。通过使用 Retrofit2 的参数处理程序，您可以轻松地将 Java 方法参数转换为 HTTP 请求参数，从而更加方便地构建和发送 HTTP 请求。


retrofit是基于OkHttp 的封装


转换器
http request body
response body
retrofit2.Converter 接口 

主要分析以下几个框架
HttpClient
HttpURLConnection
Volley
OkHttp
Retrofit

RxJava+Retrofit+OkHttp

https://github.com/square/retrofit

Retrofit requires at minimum Java 8+ or Android API 21+.

### 用法
新建接口
```java
public interface IBeanService {
    @GET("show")
    Call<Bean> getMenuById(@Query("id") String id);
}
```

```java
retrofit2.Retrofit retrofit = new retrofit2.Retrofit.Builder()
                .baseUrl("http://www.tngou.net/api/food/")
                .addConverterFactory(GsonConverterFactory.create())
                .build();
         IBeanService service = retrofit.create(IBeanService.class);
```

### 原理

InvocationHandler
动态代理
# Retrofit VS feign


https://blog.csdn.net/choi2016/article/details/54974137



https://zhuanlan.zhihu.com/p/384451261

Feign 通过给我们定义的目标接口（比如例子中的 GitHub）生成一个 HardCodedTarget 类型的代理对象，由 JDK 动态代理实现，生成代理的时候会根据注解来生成一个对应的 Map<Method, MethodHandler>，这个 Map 被 InvocationHandler 持有，接口方法调用的时候，进入 InvocationHandler 的 invoke 方法（为什么会进入这里？JDK 动态代理的基础知识）。

然后根据调用的方法从 Map<Method, MethodHandler> 获取对应的 MethodHandler，然后通过 MethodHandler 根据指定的 client 来完成对应处理， MethodHandler 中的实现类 DefaultMethodHandler 处理默认方法（接口的默认方法）的请求处理的，SynchronousMethodHandler 实现类是完成其它方法的 HTTP 请求的实现，这就是 Feign 的主要核心流程

feign设置url的时候，支持设置微服务名称，会从注册中心获取url列表？

是的，Feign 支持通过微服务名称来访问服务，其会从注册中心获取服务的 URL 列表，并进行负载均衡和容错处理。

在 Feign 中，您可以使用 `@FeignClient` 注解中的 `value` 或 `name` 属性来指定要访问的微服务名称。例如：

```
@FeignClient(value = "user-service")
public interface UserServiceClient {
    ...
}
```

在这个例子中，我们使用 `value` 属性将 Feign 客户端绑定到 `user-service` 微服务上。
当 Feign 调用微服务时，它会通过注册中心获取 `user-service` 的实例列表，并使用负载均衡算法选择一个实例进行请求。如果选择的实例发生故障或不可用，Feign 会使用容错机制自动切换到其它可用的实例进行请求。
需要注意的是，Feign 的负载均衡和容错机制是基于 Ribbon 实现的，因此需要同时引入 Ribbon 依赖。另外，您还需要在应用程序中配置注册中心的地址和协议等信息，以便 Feign 可以正确地从注册中心获取服务的实例列表。


spring boot与retrofit

https://gitee.com/edidada/testspringbootretrofit

