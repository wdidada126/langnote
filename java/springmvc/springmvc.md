# springmvc

springmvc使用jsr303提供报错信息
spring validate需要引用的jar包
在使用 Spring 的数据校验（Validation）功能时，需要引用以下依赖：
spring-context：Spring 的上下文依赖，包含了 Spring 核心容器的基本功能。
spring-web：Spring Web MVC 的依赖，包含了 Spring MVC 的基本功能。
javax.validation:validation-api：JSR 303 规范定义的数据校验 API，Spring 使用该 API 进行数据校验。
org.hibernate.validator:hibernate-validator：Hibernate Validator 实现了 JSR 303 规范，提供了更丰富的数据校验功能，Spring 也可以使用它进行数据校验。
在 Maven 中，可以通过以下方式引入这些依赖：

```xml
<dependencies>
    <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-context</artifactId>
        <version>5.3.14</version>
    </dependency>
    <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-web</artifactId>
        <version>5.3.14</version>
    </dependency>
    <dependency>
        <groupId>javax.validation</groupId>
        <artifactId>validation-api</artifactId>
        <version>2.0.1.Final</version>
    </dependency>
    <dependency>
        <groupId>org.hibernate.validator</groupId>
        <artifactId>hibernate-validator</artifactId>
        <version>6.2.0.Final</version>
    </dependency>
</dependencies>
```

jsr 303 api

JSR 303 是 Java EE 6 规范中定义的 Bean Validation API，提供了一种声明式的数据校验方式。通过在 Java 对象的字段上添加注解，可以定义该字段的数据校验规则，例如必填、长度限制、正则表达式等。使用 Bean Validation API，可以避免手动编写重复的数据校验逻辑，提高代码的可读性和可维护性。
JSR 303 API 主要包含以下注解：
@NotNull：检查对象是否为 null。
@Size：检查对象是否具有指定的大小。
@Min：检查对象是否大于等于指定的值。
@Max：检查对象是否小于等于指定的值。
@DecimalMin：检查对象是否大于等于指定的值，支持 BigDecimal 和 BigInteger。
@DecimalMax：检查对象是否小于等于指定的值，支持 BigDecimal 和 BigInteger。
@Email：检查对象是否为有效的电子邮件地址。
@Pattern：检查对象是否符合指定的正则表达式。
@AssertTrue：检查布尔值是否为 true。
@AssertFalse：检查布尔值是否为 false。

JSR 303 API 还定义了一些用于组合校验规则的注解，例如 @Valid、@GroupSequence、@GroupSequenceProvider 等。
需要注意的是，JSR 303 API 只定义了校验规则，具体的校验实现需要使用实现了该规范的校验框架，例如 Hibernate Validator、Apache BVal 等。在 Spring 中，可以使用 javax.validation:validation-api 和 org.hibernate.validator:hibernate-validator 依赖实现数据校验。


以下是一个使用 JSR 303 API 进行数据校验的示例：
假设有一个 User 类，包含了 name 和 age 两个字段：
```java
public class User {

    @NotNull(message = "姓名不能为空")
    private String name;

    @Min(value = 18, message = "年龄必须大于等于18岁")
    @Max(value = 100, message = "年龄必须小于等于100岁")
    private int age;

    // 省略 getter 和 setter 方法
}
```
在这个类中，使用了 @NotNull 和 @Min、@Max 注解进行数据校验。其中，@NotNull 注解用于检查 name 字段是否为 null，如果为 null 则抛出 message 指定的异常信息；@Min 和 @Max 注解用于检查 age 字段是否在指定的范围内。
接下来，在使用这个类的地方，可以通过如下方式进行数据校验：

```java
import javax.validation.Validation;
import javax.validation.Validator;
import javax.validation.ValidatorFactory;
import javax.validation.ConstraintViolation;
import java.util.Set;

public class Main {

    public static void main(String[] args) {
        User user = new User();
        user.setName(null);
        user.setAge(16);

        ValidatorFactory factory = Validation.buildDefaultValidatorFactory();
        Validator validator = factory.getValidator();
        Set<ConstraintViolation<User>> violations = validator.validate(user);

        for (ConstraintViolation<User> violation : violations) {
            System.out.println(violation.getMessage());
        }
    }
}
```
在这个示例中，首先创建了一个 User 对象，并设置了 name 为 null，age 为 16。接下来，通过 Validation.buildDefaultValidatorFactory() 创建一个 ValidatorFactory 对象，然后调用 factory.getValidator() 获取一个 Validator 对象。最后，调用 validator.validate(user) 对 User 对象进行校验，返回一个 Set 集合，其中包含了校验失败的信息。遍历这个 Set 集合，就可以获取到具体的校验失败信息。
如果运行这个示例，会输出如下信息：
姓名不能为空
年龄必须大于等于18岁
这是因为 User 对象中的 name 字段为 null，不符合 @NotNull 注解的要求；而 age 字段为 16，小于 @Min 注解指定的最小值 18。
需要注意的是，这只是一个简单的示例，实际使用中可能需要更复杂的校验规则和更多的注解。此外，可以在类级别或方法级别添加 @Validated 注解来启用数据校验功能，以及自定义校验规则并实现 ConstraintValidator 接口等。

springmvc使用jsr303提供报错信息
在 Spring MVC 中，可以使用 JSR 303 API 进行数据校验，并将校验结果以错误信息的形式返回给前端页面或客户端。具体实现方式如下：
在 Spring MVC 的配置文件中开启数据校验功能：
```xml
<mvc:annotation-driven validator="validator"/>
<bean id="validator" class="org.springframework.validation.beanvalidation.LocalValidatorFactoryBean"/>
```

LocalValidatorFactoryBean在spring-context包里
有一个成员变量时ValidatorFactory
javax.validation.ValidatorFactory

这段代码中，使用 <mvc:annotation-driven> 标签启用数据校验功能，并将 validator 属性指定为 LocalValidatorFactoryBean，它是 Spring 为 JSR 303 API 提供的一个实现类，用于执行数据校验操作。
在需要进行数据校验的 Controller 方法上添加 @Validated 注解，同时在方法参数中添加 BindingResult 参数，用于接收校验结果：
```java
import javax.validation.Valid;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/users")
public class UserController {

    @PostMapping
    public User addUser(@Valid @RequestBody User user, BindingResult result) {
        if (result.hasErrors()) {
            throw new RuntimeException(result.getFieldError().getDefaultMessage());
        }
        // 保存用户信息
    }
}
```
在这个示例中，使用 @Valid 注解标注了 User 类型的 user 参数，表示需要对它进行数据校验。同时，还添加了 BindingResult 参数，用于接收校验结果。如果校验失败，可以通过 result.getFieldError().getDefaultMessage() 方法获取到错误信息，并将其抛出到前端或客户端。
需要注意的是，如果不使用 BindingResult 参数接收校验结果，Spring MVC 会将校验结果存储在 Model 中，但这样可能会导致错误信息无法正确显示。因此，建议始终使用 BindingResult 参数接收校验结果。
通过使用 JSR 303 API 和 Spring MVC 的数据校验功能，可以避免手动编写重复的校验逻辑，提高代码的可读性和可维护性。同时，还可以方便地将校验结果以错误信息的形式返回给前端或客户端，提高用户体验。




org.springframework.http.MediaType

RequestMappingHandlerAdapter获取到的HttpMessageConverter列表

ByteArrayHttpMessageConverter
StringHttpMessageConverter
StringHttpMessageConverter
ResourceHttpMessageConverter
ResourceRegionHttpMessageConverter
SourceHttpMessageConverter
AllEncompassingFormHttpMessageConverter
MappingJackson2HttpMessageConverter
MappingJackson2HttpMessageConverter


这些都是Spring MVC框架中常用的HttpMessageConverter实现，它们负责将HTTP请求和响应中的body转换为Java对象，或将Java对象转换为HTTP响应的body。下面简要介绍这些HttpMessageConverter的作用及用途：
ByteArrayHttpMessageConverter
ByteArrayHttpMessageConverter是Spring Framework提供的一个HttpMessageConverter实现，用于将HTTP请求和响应中的body转换为byte数组。它通常用于处理二进制数据，例如图片、音频或视频等。
StringHttpMessageConverter
StringHttpMessageConverter是Spring Framework提供的一个HttpMessageConverter实现，用于将HTTP请求和响应中的body转换为String类型的数据。它通常用于处理文本数据，例如HTML、XML或JSON等。
ResourceHttpMessageConverter
ResourceHttpMessageConverter是Spring Framework提供的一个HttpMessageConverter实现，用于将HTTP请求和响应中的body转换为Resource对象。它通常用于处理静态文件，例如HTML页面、PDF文档或图片等。
ResourceRegionHttpMessageConverter
ResourceRegionHttpMessageConverter是Spring Framework提供的一个HttpMessageConverter实现，用于将HTTP请求和响应中的body转换为ResourceRegion对象。它通常用于处理部分请求，例如HTTP Range请求。
SourceHttpMessageConverter
SourceHttpMessageConverter是Spring Framework提供的一个HttpMessageConverter实现，用于将HTTP请求和响应中的body转换为Source对象。它通常用于处理XML数据，例如SOAP消息或RSS订阅等。
AllEncompassingFormHttpMessageConverter
AllEncompassingFormHttpMessageConverter是Spring Framework提供的一个HttpMessageConverter实现，用于将HTTP请求和响应中的body转换为MultiValueMap<String, String>或Map<String, Object>对象。它通常用于处理表单提交数据。
MappingJackson2HttpMessageConverter
MappingJackson2HttpMessageConverter是Spring Framework提供的一个HttpMessageConverter实现，用于将Java对象序列化为JSON或反序列化JSON为Java对象。它通常用于处理RESTful API的请求和响应。



DispatcherServlet类的父类是FrameworkServlet。FrameworkServlet是一个抽象类，它实现了Servlet的init()和service()方法，并提供了对Spring应用程序上下文的支持。DispatcherServlet继承了FrameworkServlet，进一步扩展了其功能，实现了Web MVC框架的核心控制器功能。


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
https://blog.csdn.net/CSDN2497242041/article/details/102618226



Fastjson的SerializerFeature序列化属性：
QuoteFieldNames———-输出key时是否使用双引号,默认为true
WriteMapNullValue——–是否输出值为null的字段,默认为false
WriteNullNumberAsZero—-数值字段如果为null,输出为0,而非null
WriteNullListAsEmpty—–List字段如果为null,输出为[],而非null
WriteNullStringAsEmpty—字符类型字段如果为null,输出为”“,而非null
WriteNullBooleanAsFalse–Boolean字段如果为null,输出为false,而非null
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


LocalValidatorFactoryBean
继承SpringValidatorAdapter
1、在spring ioc中吗？
是factoryBean，在ioc中



spring-webmvc 这个jar包

handleradapter
运行时的对象
RequestMappingHandlerAdapter


RequestMappingHandlerAdapter默认的messageConverters

在 Spring MVC 中，RequestMappingHandlerAdapter 是一个处理器适配器，用于执行处理器方法并将结果转换为 ModelAndView 或 ResponseEntity。RequestMappingHandlerAdapter 默认包含一些常见的消息转换器，用于处理请求和响应的消息体。
以下是 RequestMappingHandlerAdapter 默认包含的一些消息转换器：
ByteArrayHttpMessageConverter
用于处理字节数组格式的消息体，支持的媒体类型为 application/octet-stream。
StringHttpMessageConverter
用于处理文本格式的消息体，支持的媒体类型为 text/plain 和 text/html，默认字符集为 ISO-8859-1。
ResourceHttpMessageConverter
用于处理 Resource 类型的消息体，支持的媒体类型为 application/octet-stream、image/jpeg、image/gif、image/png 和 application/pdf。
SourceHttpMessageConverter
用于处理 Source 类型的消息体，支持的媒体类型为 application/xml 和 text/xml。
FormHttpMessageConverter
用于处理表单格式的消息体，支持的媒体类型为 application/x-www-form-urlencoded。
Jaxb2RootElementHttpMessageConverter
用于处理基于 JAXB2 的 XML 格式的消息体，支持的媒体类型为 application/xml 和 text/xml。
MappingJackson2HttpMessageConverter
用于处理 JSON 格式的消息体，支持的媒体类型为 application/json 和 application/*+json。
MappingJackson2XmlHttpMessageConverter
用于处理基于 Jackson 的 XML 格式的消息体，支持的媒体类型为 application/xml、text/xml 和 application/*+xml。
注意：以上是 RequestMappingHandlerAdapter 默认包含的一些消息转换器，具体的消息转换器列表可能会根据项目的实际情况而有所不同。如果需要自定义消息转换器，可以创建自己的类，并实现 HttpMessageConverter 接口或继承现有的消息转换器类，并将其添加到 RequestMappingHandlerAdapter 的 messageConverters 列表中。


Object handler强制转换成(HandlerMethod) handler

在 Spring MVC 中进行数据校验时，可以使用 BindingResult 类来保存校验结果。除了 BindingResult 类本身，Spring 还提供了以下三个 BindingResult 的子类：
Errors：是 BindingResult 的父类，用于保存所有类型的校验错误信息，包括字段错误、全局错误和对象错误等。
FieldErrors：用于保存字段级别的校验错误信息，可以通过 getFieldErrors() 方法获取所有字段错误信息，或通过 getFieldError(String field) 方法获取指定字段的错误信息。
ObjectErrors：用于保存对象级别的校验错误信息，可以通过 getGlobalErrors() 方法获取所有对象错误信息，或通过 getGlobalError(String code) 方法获取指定对象错误信息。


JSR 380 规范定义了 Java 中的 Bean Validation API，其中包括了数据校验相关的注解、校验器等内容。该规范于 2017 年发布，是 Java EE 8 的一部分。

Bean Validation API 提供了一套通用的数据校验框架，可以用于对 Java 对象进行数据校验，包括对属性的校验、对方法返回值的校验等。这些校验规则都是通过注解来定义的，例如 @NotNull、@Size、@Pattern 等。

在 Java 中进行数据校验时，可以使用 Bean Validation API 提供的注解来定义校验规则，然后通过校验器对目标对象进行校验。校验结果可以是一个布尔值，也可以是一组校验错误信息。

需要注意的是，虽然 Bean Validation API 是一个 JSR 规范，但是它不是 Java SE 的一部分，需要在应用中显式引入相关的依赖库，例如 Hibernate Validator。
Hibernate Validator 是一个实现了 Bean Validation API 规范的校验框架，提供了一些额外的功能，例如对集合、Map、数组等复杂类型的校验支持等。Hibernate Validator 6.x 版本实现了 JSR 380 规范，因此可以使用其中定义的所有注解和校验器。
总之，JSR 380 是 Bean Validation API 规范的版本号，同时也是 Hibernate Validator 实现的版本号。


除了Hibernate Validator之外，还有一些其他的实现库也可以用于实现JSR 380规范的数据校验功能，这些库包括：

Apache BVal
Apache BVal是Apache基金会下的一个开源项目，用于实现Java Bean Validation规范。它提供了JSR 303和JSR 349的实现，支持适用于Java SE和Java EE应用程序的数据校验功能。与Hibernate Validator相比，Apache BVal提供了更加灵活的API和更多的校验器，同时也支持JSR 349规范中新增的校验器。

OWASP ESAPI Validator
OWASP ESAPI Validator是由OWASP（开放式Web应用安全项目）提供的一个Java校验库，它提供了一组安全的校验规则，用于对输入数据进行校验，以防止应用程序遭受安全攻击。它支持JSR 303规范中定义的注解和校验器，并提供了一些扩展的校验器，例如对XSS攻击和SQL注入攻击的校验器。

Pinpoint Validator
Pinpoint Validator是由NAVER（韩国的一个IT公司）提供的一个Java校验库，它提供了一组简单易用的校验注解和校验器，支持JSR 303和JSR 349规范。与Hibernate Validator和Apache BVal相比，Pinpoint Validator具有更小的体积和更快的校验速度，适用于对性能要求较高的应用程序进行数据校验。

总之，以上是一些常见的JSR 380规范的实现库，开发人员可以根据具体需求进行选择和使用。无论使用哪个库，都需要遵循JSR 380规范定义的注解和校验器，以确保数据校验的正确性和安全性。



Spring MVC使用LocalValidatorFactoryBean类作为Validator的默认实现类

LocalValidatorFactoryBean类源码详细解读
LocalValidatorFactoryBean继承了SpringValidatorAdapter类，实现了ValidatorFactory、InitializingBean和DisposableBean接口。其中，InitializingBean和DisposableBean接口用于在Spring容器启动和关闭时执行一些初始化和清理操作。
LocalValidatorFactoryBean声明了多个属性，用于配置ValidatorFactory的行为。其中，mappingLocations和mappingClassNames用于指定校验规则的配置文件位置和类名；ignoreXmlConfiguration用于指定是否忽略XML配置文件；failFast用于指定是否启用快速失败模式；messageInterpolator、traversableResolver、constraintValidatorFactory、parameterNameProvider、hibernateValidatorConfiguration和validationProviderResolver等属性用于指定各种校验器的实现；targetValidatorFactory用于存储创建的ValidatorFactory实例；useFastFail用于指定是否启用快速失败模式。

afterPropertiesSet方法
afterPropertiesSet方法是InitializingBean接口的方法，用于在属性设置完成后执行一些初始化操作。在这个方法中，首先通过createValidatorFactory方法创建ValidatorFactory实例，然后将其包装成ThreadLocalValidatorFactory实例，并将Validator实例设置到SpringValidatorAdapter中。最后，如果messageInterpolator和traversableResolver不为空，将它们注册为Spring Bean。

createValidatorFactory方法
createValidatorFactory方法用于创建ValidatorFactory实例。在这个方法中，首先通过getConfiguration方法创建HibernateValidatorConfiguration实例，并通过messageInterpolator、traversableResolver、constraintValidatorFactory、parameterNameProvider等属性配置校验器的实现。然后，通过validationProviderResolver属性配置校验器的提供者。接着，通过failFast属性配置是否启用快速失败模式，通过useFastFail属性配置是否启用快速失败模式。最后，通过configureFromXml方法和configure方法配置校验规则，最终通过buildValidatorFactory方法创建ValidatorFactory实例。
destroy方法是DisposableBean接口的方法，用于在Spring容器关闭时执行一些清理操作。在这个方法中，首先通过targetValidatorFactoryMonitor对象同步获取targetValidatorFactory实例，并通过unwrap方法获取AutoCloseable接口，最后调用close方法关闭ValidatorFactory实例。

九大组件：
1、HandlerMapping   SimpleUrlHandlerMapping BeanNameUrlHandlerMapping RequestMappingHandlerMapping
2、HandlerAdapter
3、HandlerExceptionResolver   DefaultHandlerExceptionResolver
4、ViewResolver
5、RequestToViewNameTranslator  DefaultRequestToViewNameTranslator
6、LocalResolver
7、ThemeResolver
8、MultiPartResolver
9、FlashMapManager

ViewResolver是Spring MVC中用于解析逻辑视图名称的接口，它有多个实现类，包括InternalResourceViewResolver和ThymeleafViewResolver等


DefaultHandlerExceptionResolver的主要方法是resolveException()，它负责处理抛出的异常，并将其转换为HTTP响应。
determineStatusCode()方法是DefaultHandlerExceptionResolver的一个私有方法，用于确定抛出的异常应该被转换为哪种HTTP响应码。

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

实现HttpRequestHandler例子
HttpRequestHandler是Spring MVC框架中一个处理HTTP请求的接口，它是基于Servlet API的，可以在不使用@Controller注解的情况下处理HTTP请求。下面是一个实现HttpRequestHandler的例子：

public class MyHttpRequestHandler implements HttpRequestHandler {

    @Override
    public void handleRequest(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        // 处理请求逻辑
        String name = request.getParameter("name");
        String message = "Hello, " + name + "!";
        response.getWriter().write(message);
    }

}
在这个例子中，我们实现了HttpRequestHandler接口，并重写了其中的handleRequest方法。在handleRequest方法中，我们可以使用HttpServletRequest对象获取请求参数，并使用HttpServletResponse对象设置响应内容。在这里，我们获取了请求中的name参数，并返回一个"Hello, name!"的消息。
接下来，我们需要将这个处理器注册到Spring MVC框架中。这可以通过在Spring配置文件中配置mvc:resources元素来实现：
<mvc:resources mapping="/hello" location="/hello" />
<bean id="myHandler" class="com.example.MyHttpRequestHandler" />
在这个配置中，我们将/hello请求映射到MyHttpRequestHandler处理器上，并将处理器注册为Spring的一个bean。这样，在收到/hello请求时，Spring将会调用MyHttpRequestHandler的handleRequest方法来处理请求，并返回一个"Hello, name!"的消息。



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
| @RequestMapping映射 | RequestMappingHandlerMapping/DefaultAnnotationHandlerMapping |



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
在Spring MVC框架中，通常会有两个配置文件：applicationContext.xml和xxx-servlet.xml，它们的作用是不同的。

applicationContext.xml是Spring的核心配置文件，主要用于配置Spring容器中的bean，例如数据源、事务管理器、缓存管理器、消息队列等。这个配置文件通常是全局的，它会被所有的Servlet共享。在这个配置文件中，你可以使用任意的Spring特性来配置你的bean，例如依赖注入、AOP、事件监听器等。

xxx-servlet.xml是Spring MVC框架的配置文件，它主要用于配置与Web相关的bean，例如控制器、视图解析器、拦截器、数据绑定器等。这个配置文件通常是Servlet的局部配置文件，每个Servlet都有自己独立的配置文件。在这个配置文件中，你可以使用Spring MVC特有的特性来配置你的bean，例如@RequestMapping注解、@Controller注解、HandlerMapping、HandlerAdapter等。

通常情况下，你需要在web.xml文件中配置一个DispatcherServlet来处理HTTP请求。在这个配置中，你可以指定xxx-servlet.xml作为这个Servlet的配置文件。
applicationContext.xml是Spring的核心配置文件，用于全局配置Spring容器中的bean；xxx-servlet.xml是Spring MVC框架的配置文件，用于配置与Web相关的bean。在Web应用程序中，通常会有一个全局的applicationContext.xml文件和多个Servlet的局部配置文件。

20200115 写个servlet 访问不了，相对路径没有映射到SprinhMVC

<mvc:default-servlet-handler/>
作用
dler/是Spring MVC提供的一个配置元素，它的作用是将所有的请求映射到Servlet容器中的默认Servlet上。

在Web应用程序中，通常有一个默认Servlet用于处理静态资源，例如HTML、CSS、JavaScript等文件。这个默认Servlet通常是由Servlet容器提供的，例如Tomcat、Jetty等容器。当请求静态资源时，这个默认Servlet会负责将资源发送给客户端。

在Spring MVC框架中，默认情况下，所有的请求都会被映射到DispatcherServlet上，如果请求的资源是静态资源，那么DispatcherServlet会尝试去寻找对应的Controller来处理请求，这样会造成不必要的性能开销。

mvc:default-servlet-handler/就是为了解决这个问题而存在的。当我们配置了这个元素之后，Spring MVC就会将所有的请求都映射到Servlet容器中的默认Servlet上，如果请求的资源是静态资源，那么默认Servlet会负责将资源发送给客户端，而不是DispatcherServlet。

例如，我们可以这样在Spring配置文件中配置mvc:default-servlet-handler/：
<mvc:default-servlet-handler/>
这个配置就是将所有的请求映射到Servlet容器中的默认Servlet上，如果请求的资源是静态资源，那么默认Servlet会负责将资源发送给客户端。这样可以提高系统的性能和响应速度。

需要注意的是，mvc:default-servlet-handler/只有在Servlet 3.0及以上版本的容器中才支持。如果你的应用程序运行在Servlet 2.5或更低版本的容器中，那么你需要手动配置一个HandlerMapping来处理静态资源。

在Servlet 2.5或更低版本的容器中，如果你想要使用HandlerMapping来处理静态资源，可以按照以下步骤进行配置：

在Spring配置文件中添加以下配置：
<bean id="defaultServletHttpRequestHandler" class="org.springframework.web.servlet.resource.DefaultServletHttpRequestHandler" />
<bean class="org.springframework.web.servlet.handler.SimpleUrlHandlerMapping">
    <property name="mappings">
        <props>
            <prop key="/**/*.*">defaultServletHttpRequestHandler</prop>
        </props>
    </property>
</bean>

这里我们配置了一个DefaultServletHttpRequestHandler和一个SimpleUrlHandlerMapping。DefaultServletHttpRequestHandler是Spring MVC提供的一个处理静态资源的处理器，它会委托给Servlet容器中的默认Servlet来处理静态资源。SimpleUrlHandlerMapping则是用来将请求映射到DefaultServletHttpRequestHandler处理器上。

在web.xml文件中添加以下配置：
<servlet-mapping>
    <servlet-name>default</servlet-name>
    <url-pattern>*.css</url-pattern>
    <url-pattern>*.js</url-pattern>
    <url-pattern>*.png</url-pattern>
    <url-pattern>*.jpg</url-pattern>
    <url-pattern>*.gif</url-pattern>
    <url-pattern>*.ico</url-pattern>
</servlet-mapping>

这里我们将所有的静态资源请求都映射到Servlet容器中的默认Servlet上。这样，当请求静态资源时，Servlet容器会自动将请求转发给默认Servlet来处理。

需要注意的是，这种方式需要Servlet容器支持Servlet 2.5规范，同时也需要在web.xml文件中配置了默认Servlet。如果你使用的是Servlet 3.0及以上版本的容器，那么可以直接使用mvc:default-servlet-handler/来处理静态资源，无需手动配置HandlerMapping。

1.index.jsp访问不了，增加jstl依赖
<mvc:default-servlet-handler/>

2.Controller还是访问不了

<mvc:annotation-driven/>

如何理解servlet web.xml和springmvc的关系



配置项？

3. http路径没有映射到spring系统上，如何处理？

https://github.com/edidada/springmvccurl

20230430 支持返回xml格式的报文


配置了一个http路径失效，配置controler失效？查看有哪些Handler

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
在SpringMVC中，URL是否包括项目名是由Servlet容器的实现决定的。在Web应用程序中，Servlet容器会为每个应用程序分配一个ContextPath，也就是应用程序的上下文路径。当客户端发送请求时，请求的URL中必须包含ContextPath才能访问应用程序中的资源。
默认情况下，SpringMVC会自动将ContextPath添加到URL中，以确保客户端能够正确地访问应用程序中的资源。例如，如果应用程序的ContextPath为/myapp，那么访问控制器的URL就应该是/myapp/home，而不是/home。
如果你希望URL中不包含ContextPath，可以在SpringMVC的配置文件中添加以下配置：
<bean class="org.springframework.web.servlet.mvc.annotation.DefaultAnnotationHandlerMapping">
    <property name="alwaysUseFullPath" value="false"/>
</bean>
这里我们配置了一个DefaultAnnotationHandlerMapping，并设置了alwaysUseFullPath属性为false。这个属性的作用是控制URL是否包含ContextPath。如果将这个属性设置为false，那么URL就不会包含ContextPath，访问控制器的URL就可以是/home，而不是/myapp/home。
需要注意的是，如果你将alwaysUseFullPath属性设置为false，那么客户端就必须手动添加ContextPath才能访问应用程序中的资源。例如，如果应用程序的ContextPath为/myapp，那么访问控制器的URL就应该是/myapp/home，而不是/home。因此，在设置alwaysUseFullPath属性时需要谨慎考虑。


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

Mapped "{[/healthcheck.html]}" onto public java.lang.Object com.xxx.medium.test.isomerization.proxy.web.MainController.healthCheck()
Mapped "{[/healthcheck.html]}" onto public java.lang.Object com.xxxxxx.medium.test.isomerization.proxy.web.MainController.healthCheck()
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

Spring MVC配置介绍
https://blog.csdn.net/suifeng3051/article/details/51596511



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


注解@CrossOrigin解决跨域问题 
https://www.cnblogs.com/mmzs/p/9167743.html



20200405 写个servlet 访问不了，相对路径没有映射到SprinhMVC






SpringMVC：SpringMVC启动初始化过程
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

在SpringMVC中，MultipartResolver是用来解析HTTP请求中的文件上传的。它可以将上传的文件转换成MultipartFile对象，以方便在控制器中进行处理。SpringMVC提供了两个MultipartResolver的实现类：
1、CommonsMultipartResolver：基于Apache Commons FileUpload实现的MultipartResolver。需要引入commons-fileupload和commons-io两个依赖。
2、StandardServletMultipartResolver：基于Servlet 3.0规范实现的MultipartResolver。需要在web.xml中配置multipart-config元素。
你可以根据实际需求选择其中的一个实现类。

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