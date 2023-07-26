# Retrofit

## 封装成spring boot starter

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

## 源代码分包解析

### com.github.lianjiatech.retrofit.spring.boot.annotation


| com.github.lianjiatech.retrofit.spring.boot.annotation | 类型       | 解释                                              |
| ------------------------------------------------------ | ---------- | ------------------------------------------------- |
| Intercept                                              | @interface | 自动将注解上的参数值赋值到handleInterceptor实例上 |
| InterceptMark                                          | @interface | 拦截标记注解                                      |
| Intercepts                                             | @interface |                                                   |
| OkHttpClientBuilder                                    | @interface |                                                   |
| RetrofitClient                                         | @interface |                                                   |
| RetrofitScan                                           | @interface |                                                   |


### com.github.lianjiatech.retrofit.spring.boot.config

| com.github.lianjiatech.retrofit.spring.boot.config           | 类型   | 解释                                                         |
| ------------------------------------------------------------ | ------ | ------------------------------------------------------------ |
| DegradeProperty                                              |        | 熔断降级配置 BaseResourceNameParser子类                      |
| LogProperty                                                  |        | 日志属性设置                                                 |
| PoolConfig                                                   |        | 连接池参数配置                                               |
| RetrofitAutoConfiguration                                    |        |                                                              |
| RetrofitAutoConfiguration.RetrofitProcessorAutoConfiguration | 内部类 |                                                              |
| RetrofitAutoConfiguration.RetrofitScannerRegistrarNotFoundConfiguration | 内部类 |                                                              |
| RetrofitConfigBean                                           |        | spring ioc容器对象，通过java代码注入com.github.lianjiatech.retrofit.spring.boot.config.RetrofitAutoConfiguration#retrofitConfigBean |
| RetrofitProperties                                           |        | 配置文件对应的类，见例子，.yml文件以retrofit开头             |
| RetryProperty                                                |        | 5个属性，5个可设置项                                         |





### com.github.lianjiatech.retrofit.spring.boot.degrade


| com.github.lianjiatech.retrofit.spring.boot.degrade | 类型       | 解释                                                         |
| --------------------------------------------------- | ---------- | ------------------------------------------------------------ |
| BaseDegradeInterceptor                              | abstract   | com.github.lianjiatech.retrofit.spring.boot.config.DegradeProperty 中用 接口实现类 DefaultResourceNameParser 子类 SentinelDegradeInterceptor |
| BaseResourceNameParser                              | abstract   | 子类 DefaultResourceNameParser   RetrofitConfigBean类resourceNameParser属性  resourceNameParser() 方法 |
| DefaultResourceNameParser                           |            | BaseResourceNameParser实现类                                 |
| Degrade                                             | @interface |                                                              |
| DegradeStrategy                                     | enum       |                                                              |
| DegradeType                                         | enum       |                                                              |
| FallbackFactory<T>                                  |            | 见下面                                                       |
| HttpMethodPath                                      |            | method path两个String属性的类                                |
| RetrofitBlockException                              | exception  |                                                              |
| RetrofitDegradeRule                                 |            | 属性 DegradeStrategy degradeStrategy                         |
| RetrofitDegradeRuleInitializer                      |            | sentinel 实现ApplicationListener<ApplicationReadyEvent>  接口，DegradeProperty degradeProperty List<RetrofitDegradeRule> *LIST*属性 |
| SentinelDegradeInterceptor                          |            | sentinal BaseDegradeInterceptor子类                          |





com.github.lianjiatech.retrofit.spring.boot.degrade.FallbackFactory



`FallbackFactory` 是 `com.github.lianjiatech.retrofit.spring.boot.degrade` 包中的一个接口，它是用于在 Retrofit 接口调用失败时提供降级策略的工厂类。使用 `FallbackFactory` 可以提供更加灵活的降级方案，它可以在降级时获取到异常信息，以便根据异常信息进行不同的降级处理。

下面是一个使用 `FallbackFactory` 的例子：

首先，我们需要定义一个 Retrofit 接口，并为它添加一个降级方法：

```java
public interface MyApi {
    @GET("/users/{id}")
    User getUser(@Path("id") Long id);

    @Component
    class MyApiFallbackFactory implements FallbackFactory<MyApi> {
        @Override
        public MyApi create(Throwable throwable) {
            return new MyApi() {
                @Override
                public User getUser(Long id) {
                    // 降级处理逻辑
                    // ...
                    return null;
                }
            };
        }
    }
}
```

在上面的代码中，我们定义了一个 `MyApi` 接口，并为它添加了一个降级方法 `MyApiFallbackFactory.create()`。这个方法会在 Retrofit 接口调用失败时被调用，它可以根据异常信息来进行不同的降级处理。在这个例子中，我们只是简单地返回了 `null`。

然后，我们需要将 `MyApiFallbackFactory` 注册为 Spring Bean：

```java
@Configuration
public class MyAppConfig {
    @Bean
    public FallbackFactory<MyApi> myApiFallbackFactory() {
        return new MyApi.MyApiFallbackFactory();
    }

    @Bean
    public RetrofitFactoryBean<MyApi> myApi() {
        RetrofitFactoryBean<MyApi> factoryBean = new RetrofitFactoryBean<>(MyApi.class);
        factoryBean.setBaseUrl("http://localhost:8080");
        factoryBean.setFallbackFactory(myApiFallbackFactory());
        return factoryBean;
    }
}
```

在上面的代码中，我们创建了一个 `FallbackFactory<MyApi>` 实例，并将它注册为 Spring Bean。然后，我们创建了一个 `RetrofitFactoryBean` 实例，并设置了 Retrofit 的基础 URL。在这个例子中，我们通过 `setFallbackFactory()` 方法将 `FallbackFactory<MyApi>` 实例添加到了 Retrofit 实例中。

这样，当 Retrofit 接口调用失败时，就会自动调用 `MyApiFallbackFactory.create()` 方法，提供降级处理的逻辑。

总之，`FallbackFactory` 是 `com.github.lianjiatech.retrofit.spring.boot.degrade` 包中的一个接口，它用于在 Retrofit 接口调用失败时提供降级策略的工厂类。使用 `FallbackFactory` 可以提供更加灵活的降级方案。使用它的步骤包括定义 Retrofit 接口并添加降级方法、将降级工厂类注册为 Spring Bean、将降级工厂类添加到 Retrofit 实例中。







以下是一个简单的 `MyApiFallbackFactory` 示例代码，用于提供 `MyApi` 接口的降级处理：

```java
@Component
public class MyApiFallbackFactory implements FallbackFactory<MyApi> {

    @Override
    public MyApi create(Throwable throwable) {
        return new MyApi() {

            @Override
            public User getUser(Long id) {
                // 这里是降级处理逻辑，例如返回一个默认值
                return new User(-1L, "default", null);
            }

            // 可以为 MyApi 接口中的其他方法添加相应的降级处理逻辑
        };
    }
}
```

在上面的代码中，我们创建了一个 `MyApiFallbackFactory` 类，并实现了 `FallbackFactory<MyApi>` 接口。`FallbackFactory` 接口有一个 `create(Throwable throwable)` 方法，该方法在 Retrofit 抛出异常时被调用，可以根据异常信息进行不同的降级处理。

在 `create()` 方法中，我们返回了一个匿名内部类，该类实现了 `MyApi` 接口，并为其中的 `getUser()` 方法添加了一个简单的降级处理逻辑，即返回一个默认的 `User` 对象。如果需要对其他方法添加降级处理逻辑，可以在该匿名内部类中继续实现对应的方法。

最后，我们将 `MyApiFallbackFactory` 类标记为 Spring 组件，以便可以被自动扫描到并注册为 Spring Bean。

总之，`MyApiFallbackFactory` 是一个实现了 `FallbackFactory<MyApi>` 接口的 Spring 组件，该组件提供了 `MyApi` 接口的降级处理逻辑。在 `create()` 方法中，我们可以根据异常信息进行不同的降级处理。



### com.github.lianjiatech.retrofit.spring.boot.core



| com.github.lianjiatech.retrofit.spring.boot.core   |           | 解释                                                         |
| -------------------------------------------------- | --------- | ------------------------------------------------------------ |
| AutoConfiguredRetrofitScannerRegistrar             |           |                                                              |
| BasicTypeConverterFactory                          |           | 基本类型转换，http返回数据 Converter.Factory子类             |
| BasicTypeConverterFactory.BooleanResponseConverter |           | Converter<F, T> 子类  convert(F value)方法                   |
| BasicTypeConverterFactory.DoubleResponseConverter  |           |                                                              |
| BasicTypeConverterFactory.FloatResponseConverter   |           |                                                              |
| BasicTypeConverterFactory.IntegerResponseConverter |           |                                                              |
| BasicTypeConverterFactory.LongResponseConverter    |           |                                                              |
| BasicTypeConverterFactory.StringResponseConverter  |           |                                                              |
| BodyCallAdapterFactory                             |           | retrofit2 jar包 CallAdapter.Factory子类 跟ResponseCallAdapterFactory比较 |
| BodyCallAdapterFactory.BodyCallAdapter             |           | retrofit2.CallAdapter子类                                    |
| ClassPathRetrofitClientScanner                     |           | ClassPathBeanDefinitionScanner子类                           |
| DefaultErrorDecoder                                |           | ErrorDecoder接口实现类                                       |
| ErrorDecoder                                       | interface |                                                              |
| NoValidServiceInstanceChooser                      |           | ServiceInstanceChooser接口实现类                             |
| PrototypeInterceptorBdfProcessor                   |           | BeanDefinitionRegistryPostProcessor接口实现类  void postProcessBeanDefinitionRegistry(BeanDefinitionRegistry registry) 见下面  com.github.lianjiatech.retrofit.spring.boot.config.RetrofitAutoConfiguration.RetrofitProcessorAutoConfiguration#prototypeInterceptorBdfProcessor中定义bean |
| ResponseCallAdapterFactory                         |           | CallAdapter.Factory子类  跟BodyCallAdapterFactory 比较       |
| ResponseCallAdapterFactory.ResponseCallAdapter     |           |                                                              |
| **RetrofitClientScannerRegistrar**                 |           |                                                              |
| **RetrofitFactoryBean<T>**                         |           | FactoryBean<T>  见下面  com.github.lianjiatech.retrofit.spring.boot.core.RetrofitFactoryBean#getObject调用 RetrofitInvocationHandler |
| RetrofitInvocationHandler                          |           | InvocationHandler接口实现类 动态代理  com.github.lianjiatech.retrofit.spring.boot.core.RetrofitFactoryBean#getObject 里面被调用 |
| ServiceInstanceChooser                             | interface | URI choose(String serviceId) 接口实现类 SpringCloudServiceInstanceChooser  NoValidServiceInstanceChooser |
| SpringCloudServiceInstanceChooser                  |           | spring cloud里面的                                           |





Factory in CallAdapter (retrofit2)
    DefaultCallAdapterFactory (retrofit2)
    CompletableFutureCallAdapterFactory (retrofit2)
    ResponseCallAdapterFactory (com.github.lianjiatech.retrofit.spring.boot.core)
    BodyCallAdapterFactory (com.github.lianjiatech.retrofit.spring.boot.core)
    RxJava2CallAdapterFactory (retrofit2.adapter.rxjava2)







`PrototypeInterceptorBdfProcessor` 是 `com.github.lianjiatech.retrofit.spring.boot.core` 包中的一个类，它是一个 Bean 后置处理器，用于将 Retrofit 的拦截器设置为原型模式。

在 Retrofit 中，拦截器是一个可重用的组件，它可以被多个请求共享。默认情况下，当我们通过 Spring Boot 的自动配置来创建 Retrofit 实例时，Retrofit 的拦截器是单例模式的，也就是说，在整个应用程序中只有一个拦截器实例。这意味着，如果我们在拦截器中保存了一些状态，那么这些状态会被多个请求共享，可能会导致线程安全问题。

为了解决这个问题，`PrototypeInterceptorBdfProcessor` 类提供了一个解决方案，它可以将 Retrofit 的拦截器设置为原型模式，这样每个请求都会创建一个新的拦截器实例，避免了线程安全问题。

下面是一个使用 `PrototypeInterceptorBdfProcessor` 的例子：

```java
@Configuration
public class MyAppConfig {
    @Bean
    public PrototypeInterceptorBdfProcessor prototypeInterceptorBdfProcessor() {
        return new PrototypeInterceptorBdfProcessor();
    }

    @Bean
    public RetrofitFactoryBean<MyApi> myApi() {
        RetrofitFactoryBean<MyApi> factoryBean = new RetrofitFactoryBean<>(MyApi.class);
        factoryBean.setBaseUrl("http://localhost:8080");
        factoryBean.setInterceptors(Collections.singletonList(new MyInterceptor()));
        return factoryBean;
    }
}
```

在上面的代码中，我们创建了一个 `PrototypeInterceptorBdfProcessor` 实例，并将它注册为 Spring Bean。然后，我们创建了一个 `RetrofitFactoryBean` 实例，并设置了 Retrofit 的基础 URL。在这个例子中，我们还通过 `setInterceptors()` 方法将一个拦截器 `MyInterceptor` 添加到了 Retrofit 实例中。

由于我们注册了 `PrototypeInterceptorBdfProcessor` Bean，因此 Retrofit 的拦截器将会被设置为原型模式，每个请求都会创建一个新的拦截器实例。这样，即使在拦截器中保存了一些状态，也不会导致线程安全问题。

总之，`PrototypeInterceptorBdfProcessor` 是 `com.github.lianjiatech.retrofit.spring.boot.core` 包中的一个 Bean 后置处理器，它可以将 Retrofit 的拦截器设置为原型模式，避免了线程安全问题。使用它可以确保拦截器实例在每个请求中都是独立的。





com.github.lianjiatech.retrofit.spring.boot.core.RetrofitFactoryBean 泛型类是啥？

@RetrofitClient注解修饰的类





ClassPathRetrofitClientScanner includeFilters属性有

org.springframework.core.type.filter.AnnotationTypeFilter 对象

实际:annotationType 是com.github.lianjiatech.retrofit.spring.boot.annotation.RetrofitClient



mybatis也有自定义类ClassPathMapperScanner继承ClassPathBeanDefinitionScanner





在Spring Boot中,代码

```java
@Import({AutoConfiguredRetrofitScannerRegistrar.class})
```

的作用是导入AutoConfiguredRetrofitScannerRegistrar这个注册器类。

主要用于自动配置Retrofit客户端。

@Import注解用来导入配置类或其他类到Spring容器中。

而AutoConfiguredRetrofitScannerRegistrar实现了ImportBeanDefinitionRegistrar接口,它会在容器导入这个类时通过registerBeanDefinitions方法注册额外的Bean定义。

这里它主要注册的Bean定义是:

1. RetrofitClientScannerConfigure:Retrofit客户端扫描器

2. OkHttpClientBuilderConfigurer: OkHttp客户端构建器配置器

所以通过导入这个Registrar类,RetrofitClientScannerConfigure和OkHttpClientBuilderConfigurer会被自动配置到Spring容器中。

这样就可以实现自动扫描加载Retrofit客户端,并可自定义OkHttp客户端。

综上,@Import此注册器是启用Retrofit客户端自动配置的关键。



### com.github.lianjiatech.retrofit.spring.boot.exception



| com.github.lianjiatech.retrofit.spring.boot.exception |           |      |
| ----------------------------------------------------- | --------- | ---- |
| ReadResponseBodyException                             | exception |      |
| RetrofitException                                     | exception |      |
| RetrofitIOException                                   | exception |      |
| ServiceInstanceChooseException                        | exception |      |



### com.github.lianjiatech.retrofit.spring.boot.interceptor



| com.github.lianjiatech.retrofit.spring.boot.interceptor |           | 解释                                                         |
| ------------------------------------------------------- | --------- | ------------------------------------------------------------ |
| BaseGlobalInterceptor                                   | abstract  | PrototypeInterceptor接口实现类                               |
| BaseLoggingInterceptor                                  | abstract  | NetworkInterceptor接口实现类                                 |
| BasePathMatchInterceptor                                | abstract  | PrototypeInterceptor接口实现类                               |
| DefaultLoggingInterceptor                               |           | BaseLoggingInterceptor子类                                   |
| ErrorDecoderInterceptor                                 |           | okhttp3.Interceptor接口实现类                                |
| LogLevel                                                | enum      |                                                              |
| LogStrategy                                             | enum      |                                                              |
| NetworkInterceptor                                      | interface | okhttp3.Interceptor子接口  接口实现类DefaultLoggingInterceptor |
| PrototypeInterceptor                                    | interface | okhttp3.Interceptor子接口                                    |
| ServiceInstanceChooserInterceptor                       |           | okhttp3.Interceptor接口实现类                                |





BasePathMatchInterceptor抽象类，自定义

testspringbootretrofit项目

HeadersInterceptor.java



### com.github.lianjiatech.retrofit.spring.boot.retry



| com.github.lianjiatech.retrofit.spring.boot.retry |            | 解释                                                         |
| ------------------------------------------------- | ---------- | ------------------------------------------------------------ |
| BaseRetryInterceptor                              | abstract   | protected abstract Response retryIntercept(int maxRetries, int intervalMs, RetryRule[] retryRules, Chain chain); 子类 DefaultRetryInterceptor |
| **DefaultRetryInterceptor**                       |            | 继承 BaseRetryInterceptor                                    |
| Retry                                             | @interface | 见下面                                                       |
| RetryRule                                         | enum       |                                                              |
| RetryStrategy                                     |            | 重试机制 private int maxRetries; private int intervalMs;     |





`Retry` 是 `com.github.lianjiatech.retrofit.spring.boot.retry` 包中的一个注解，它可以用于标记 Retrofit 接口方法，表示在请求失败时进行重试。使用 `Retry` 注解可以避免因为网络波动等原因导致的接口请求失败，从而提高接口请求的可靠性。

以下是一个使用 `Retry` 注解的示例代码：

```java
public interface MyApi {
    @Retry(maxRetries = 3, retryOn = SocketTimeoutException.class)
    @GET("/users/{id}")
    User getUser(@Path("id") Long id);
}
```

在上面的代码中，我们为 `getUser()` 方法添加了 `@Retry` 注解，并设置了 `maxRetries` 和 `retryOn` 参数。`maxRetries` 表示最大重试次数，`retryOn` 表示重试的异常类型。在这个例子中，我们设置最大重试次数为 3，重试的异常类型为 `SocketTimeoutException`。

当我们调用 `getUser()` 方法时，如果请求失败并抛出了 `SocketTimeoutException` 异常，Retrofit 会自动进行重试，最多进行 3 次重试，直到请求成功或达到最大重试次数为止。

需要注意的是，`Retry` 注解只能用于 Retrofit 接口方法上，不能用于拦截器中的处理逻辑。

总之，`Retry` 是一个用于标记 Retrofit 接口方法的注解，它可以在请求失败时进行重试。使用 `Retry` 注解可以提高接口请求的可靠性。在使用时，需要设置最大重试次数和重试的异常类型。

| com.github.lianjiatech.retrofit.spring.boot.util |      |      |
| ------------------------------------------------ | ---- | ---- |
| ApplicationContextUtils                          |      |      |
| BeanExtendUtils                                  |      |      |
| RetrofitUtils                                    |      |      |







BeanFactory  org.springframework.beans.factory.BeanFactory

org.springframework.beans.factory.BeanFactory#containsBean()方法

org.springframework.beans.factory.BeanFactory#getBean(java.lang.String, java.lang.Class<T>)



BeanFactoryAware接口



`ImportBeanDefinitionRegistrar` 接口是 Spring Framework 中的一个扩展点，用于允许开发人员在运行时动态地注册其他 BeanDefinition。

通常情况下，我们可以在 `@Configuration` 类上使用 `@Import` 注解来导入其他的 `@Configuration` 类，以便将它们的 BeanDefinition 注册到 Spring 容器中。但是，在某些情况下，我们需要在运行时动态地注册 BeanDefinition，这时就可以使用 `ImportBeanDefinitionRegistrar` 接口。

当一个 `@Configuration` 类实现了 `ImportBeanDefinitionRegistrar` 接口后，它必须实现 `registerBeanDefinitions()` 方法。在这个方法中，开发人员可以使用 `BeanDefinitionRegistry` 接口动态地注册其他的 BeanDefinition，这些 BeanDefinition 可以是通过编程方式创建的，也可以是通过解析配置文件等方式创建的。

总之，`ImportBeanDefinitionRegistrar` 接口提供了一种动态注册 BeanDefinition 的机制，使得开发人员可以更加灵活地管理 Spring 容器中的 Bean。




com.github.lianjiatech.retrofit.spring.boot.core.RetrofitFactoryBean#getObject

核心类

作用是把retrofit 接口的动态代理类注入spring容器

https://github.com/edidada/retrofit-spring-boot-starter





AutoConfiguredRetrofitScannerRegistrar

使用beanFactory

ImportBeanDefinitionRegistrar

ClassPathRetrofitClientScanner



RetrofitConfigBean





注意spring boot 2
spring boot 3的区别

https://gitee.com/edidada/testspringbootretrofit

## retrofit vs retrofit spring boot starter

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
## Retrofit VS feign


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

