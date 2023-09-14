#  java validate

[testvalidate Spring](https://bitbucket.org/sandisks/testvalidate/)
[testvalidate api](https://github.com/edidada/testvalidation)

### jar包maven坐标

```xml
        <dependency>
            <groupId>jakarta.validation</groupId>
            <artifactId>jakarta.validation-api</artifactId>
			<version>2.0.2</version>
        </dependency>
```

```xml
        <dependency>
            <groupId>javax.validation</groupId>
            <artifactId>validation-api</artifactId>
			<version>2.0.1.Final</version>
        </dependency>
```

```xml
        <dependency>
            <groupId>javax.el</groupId>
            <artifactId>javax.el-api</artifactId>
            <version>3.0.0</version>
        </dependency>
```


```shell
javax.validation.UnexpectedTypeException: HV000030: No validator could be found for constraint 'javax.validation.constraints.NotBlank' validating type 'java.util.Date'. Check configuration for 'receiveDate'
	at org.hibernate.validator.internal.engine.constraintvalidation.ConstraintTree.getExceptionForNullValidator(ConstraintTree.java:116)
	at org.hibernate.validator.internal.engine.constraintvalidation.ConstraintTree.getInitializedConstraintValidator(ConstraintTree.java:162)
	at org.hibernate.validator.internal.engine.constraintvalidation.SimpleConstraintTree.validateConstraints(SimpleConstraintTree.java:54)
	at org.hibernate.validator.internal.engine.constraintvalidation.ConstraintTree.validateConstraints(ConstraintTree.java:75)
	at org.hibernate.validator.internal.metadata.core.MetaConstraint.doValidateConstraint(MetaConstraint.java:130)
	at org.hibernate.validator.internal.metadata.core.MetaConstraint.validateConstraint(MetaConstraint.java:123)
	at org.hibernate.validator.internal.engine.ValidatorImpl.validateMetaConstraint(ValidatorImpl.java:555)
	at org.hibernate.validator.internal.engine.ValidatorImpl.validateConstraintsForSingleDefaultGroupElement(ValidatorImpl.java:518)
	at org.hibernate.validator.internal.engine.ValidatorImpl.validateConstraintsForDefaultGroup(ValidatorImpl.java:488)
	at org.hibernate.validator.internal.engine.ValidatorImpl.validateConstraintsForCurrentGroup(ValidatorImpl.java:450)
	at org.hibernate.validator.internal.engine.ValidatorImpl.validateInContext(ValidatorImpl.java:400)
	at org.hibernate.validator.internal.engine.ValidatorImpl.validate(ValidatorImpl.java:172)
	at org.springframework.validation.beanvalidation.SpringValidatorAdapter.validate(SpringValidatorAdapter.java:117)
	at org.springframework.boot.autoconfigure.validation.ValidatorAdapter.validate(ValidatorAdapter.java:70)
	at org.springframework.validation.DataBinder.validate(DataBinder.java:889)
	at org.springframework.web.servlet.mvc.method.annotation.AbstractMessageConverterMethodArgumentResolver.validateIfApplicable(AbstractMessageConverterMethodArgumentResolver.java:266)
	at org.springframework.web.servlet.mvc.method.annotation.RequestResponseBodyMethodProcessor.resolveArgument(RequestResponseBodyMethodProcessor.java:137)
	at org.springframework.web.method.support.HandlerMethodArgumentResolverComposite.resolveArgument(HandlerMethodArgumentResolverComposite.java:121)
	at org.springframework.web.method.support.InvocableHandlerMethod.getMethodArgumentValues(InvocableHandlerMethod.java:167)
	at org.springframework.web.method.support.InvocableHandlerMethod.invokeForRequest(InvocableHandlerMethod.java:134)
	at org.springframework.web.servlet.mvc.method.annotation.ServletInvocableHandlerMethod.invokeAndHandle(ServletInvocableHandlerMethod.java:105)
	at org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter.invokeHandlerMethod(RequestMappingHandlerAdapter.java:878)
	at org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerAdapter.handleInternal(RequestMappingHandlerAdapter.java:792)
	at org.springframework.web.servlet.mvc.method.AbstractHandlerMethodAdapter.handle(AbstractHandlerMethodAdapter.java:87)
	at org.springframework.web.servlet.DispatcherServlet.doDispatch(DispatcherServlet.java:1040)
	at org.springframework.web.servlet.DispatcherServlet.doService(DispatcherServlet.java:943)
	at org.springframework.web.servlet.FrameworkServlet.processRequest(FrameworkServlet.java:1006)
	at org.springframework.web.servlet.FrameworkServlet.doPost(FrameworkServlet.java:909)
	at javax.servlet.http.HttpServlet.service(HttpServlet.java:652)
	at org.springframework.web.servlet.FrameworkServlet.service(FrameworkServlet.java:883)
	at javax.servlet.http.HttpServlet.service(HttpServlet.java:733)
	at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:231)
	at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:166)
	at org.apache.tomcat.websocket.server.WsFilter.doFilter(WsFilter.java:53)
	at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:193)
	at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:166)
	at org.springframework.web.filter.RequestContextFilter.doFilterInternal(RequestContextFilter.java:100)
	at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:119)
	at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:193)
	at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:166)
	at org.springframework.web.filter.FormContentFilter.doFilterInternal(FormContentFilter.java:93)
	at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:119)
	at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:193)
	at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:166)
	at org.springframework.web.filter.CharacterEncodingFilter.doFilterInternal(CharacterEncodingFilter.java:201)
	at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:119)
	at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:193)
	at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:166)
	at org.apache.catalina.core.StandardWrapperValve.invoke(StandardWrapperValve.java:202)
	at org.apache.catalina.core.StandardContextValve.invoke(StandardContextValve.java:97)
	at org.apache.catalina.authenticator.AuthenticatorBase.invoke(AuthenticatorBase.java:541)
	at org.apache.catalina.core.StandardHostValve.invoke(StandardHostValve.java:143)
	at org.apache.catalina.valves.ErrorReportValve.invoke(ErrorReportValve.java:92)
	at org.apache.catalina.core.StandardEngineValve.invoke(StandardEngineValve.java:78)
	at org.apache.catalina.connector.CoyoteAdapter.service(CoyoteAdapter.java:343)
	at org.apache.coyote.http11.Http11Processor.service(Http11Processor.java:374)
	at org.apache.coyote.AbstractProcessorLight.process(AbstractProcessorLight.java:65)
	at org.apache.coyote.AbstractProtocol$ConnectionHandler.process(AbstractProtocol.java:868)
	at org.apache.tomcat.util.net.NioEndpoint$SocketProcessor.doRun(NioEndpoint.java:1590)
	at org.apache.tomcat.util.net.SocketProcessorBase.run(SocketProcessorBase.java:49)
	at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)
	at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)
	at org.apache.tomcat.util.threads.TaskThread$WrappingRunnable.run(TaskThread.java:61)
	at java.lang.Thread.run(Thread.java:750)
```


HV000030错误是由于在使用javax.validation.constraints.NotBlank注解时，将其应用于不支持该注解的数据类型上引起的。在您的错误信息中，出现了“validating type 'java.util.Date'”，表明javax.validation.constraints.NotBlank注解应用于java.util.Date类型的属性上，但是该注解不支持Date类型的校验。
javax.validation.constraints.NotBlank注解用于限制字符串不能为空字符串或者只包含空格的情况，它只能用于字符串类型的属性上。在Java中，Date类型不是字符串类型，因此不支持NotBlank注解。
如果您想要在校验Date类型的属性时，限制其不能为空，可以使用javax.validation.constraints.NotNull注解。该注解用于限制属性值不能为null，例如：

```java
public class Order {
    @NotNull(message = "receiveDate不能为空")
    private Date receiveDate;
    // getter和setter方法省略
}
```

在上述代码中，我们使用@NotNull注解来限制receiveDate属性值不能为null。如果传入的值为null，则会抛出ConstraintViolationException异常，提示“receiveDate不能为空”。
需要注意的是，如果您想要在校验Date类型的属性时，限制其不能为空，还需要考虑到Date类型的默认值问题。在Java中，如果没有为Date类型的属性设置初始值，它的默认值为null。因此，如果需要限制Date类型的属性不能为空，需要在实体类中为该属性设置初始值，例如：

```java
public class Order {
    @NotNull(message = "receiveDate不能为空")
    private Date receiveDate = new Date(); // 设置默认值为当前时间
    // getter和setter方法省略
}
```

在上述代码中，我们为receiveDate属性设置了默认值，这样即使在未设置receiveDate属性值的情况下，它的默认值也不会为null。
总之，在使用javax.validation注解时，需要确保注解应用于支持该注解的数据类型上，同时需要考虑到数据类型的默认值问题。如果在校验过程中出现任何问题，可以检查代码中的注解使用是否正确，并查看错误日志以了解具体的错误信息。


### api

hibernate-validator jar包的
SimpleConstraintTree
org.hibernate.validator.internal.engine.constraintvalidation.SimpleConstraintTree


SimpleConstraintTree hibernate-validator 6.2找不到了，替代类是？

在 Hibernate Validator 6.2 中，`SimpleConstraintTree` 类已被移除，因为它是一个内部实现类，不应该在应用程序中直接使用。如果您需要构建和操作验证约束树，可以使用 `ConstraintTree` 类来替代。

`ConstraintTree` 类提供了一些方法来构建和操作验证约束树。您可以使用 `ConstraintTree.Builder` 类来构建验证约束树的根节点，并使用方法链语法添加子节点和约束。以下是一个示例：

```java
import org.hibernate.validator.constraintvalidation.HibernateConstraintValidatorInitializationContext;
import org.hibernate.validator.constraintvalidation.HibernateConstraintValidatorInitializationContextImpl;
import org.hibernate.validator.internal.engine.constraintvalidation.ConstraintValidatorManager;

import javax.validation.ConstraintValidator;
import javax.validation.ConstraintViolation;
import java.util.Set;

public class Main {

    public static void main(String[] args) {
        ConstraintTree.Builder<MyObject> builder = ConstraintTree.builder();

        builder.addConstraint(NotEmpty.class)
                .addPropertyNode("name")
                .addConstraint(NotBlank.class);

        ConstraintTree<MyObject> constraintTree = builder.build();

        MyObject myObject = new MyObject("");
        Set<ConstraintViolation<MyObject>> violations = constraintTree.validate(myObject);

        for (ConstraintViolation<MyObject> violation : violations) {
            System.out.println(violation.getPropertyPath() + ": " + violation.getMessage());
        }
    }

    public static class MyObject {
        private String name;

        public MyObject(String name) {
            this.name = name;
        }

        public String getName() {
            return name;
        }
    }
}
```
在上面的示例中，我们使用 `ConstraintTree.Builder` 构建了一个验证约束树。我们添加了 `NotEmpty` 约束到 `name` 属性，并且在 `name` 属性上添加了 `NotBlank` 约束。然后，我们创建了一个 `MyObject` 实例，并使用验证约束树对其进行验证。
请注意，示例代码中的 `NotEmpty` 和 `NotBlank` 是示例约束注解，您需要根据您的实际需求替换为适合您的约束注解。另外，您需要确保您的项目中包含了 Hibernate Validator 6.2 或更高版本的依赖。


`SimpleConstraintTree` 是 `javax.validation` API 中的一个类，它代表了一个树形结构，用于表示一个或多个验证约束的组合。

`SimpleConstraintTree` 的主要作用是提供一种方便的方式来组合多个验证约束，并将它们应用于目标对象。它可以通过 `javax.validation.ConstraintTree` 接口来访问，并可以与其他 `javax.validation` API 类一起使用。

下面是一个示例，演示如何使用 `SimpleConstraintTree` 来组合多个验证约束：

```java
SimpleConstraintTree<Person> constraintTree = new SimpleConstraintTree<Person>(Person.class);
constraintTree.addConstraint("name", ConstraintType.NOT_NULL);
constraintTree.addConstraint("age", ConstraintType.MIN, 18);
```

在上述示例中，我们首先创建了一个 `SimpleConstraintTree` 实例，然后向其中添加两个约束：一个约束要求 `name` 属性不为 null，另一个约束要求 `age` 属性的值大于或等于 18。

然后，我们可以使用 `javax.validation.Validator` 实例来验证目标对象：

```java
Validator validator = Validation.buildDefaultValidatorFactory().getValidator();
Set<ConstraintViolation<Person>> violations = validator.validate(person, constraintTree);
```

在这个示例中，我们使用 `javax.validation.Validation` 工厂类创建了一个 `Validator` 实例，并将 `SimpleConstraintTree` 作为参数传递给 `validate` 方法。这样，`Validator` 实例就会根据 `SimpleConstraintTree` 中定义的约束来验证目标对象。

需要注意的是，`SimpleConstraintTree` 只是 `javax.validation` API 中的一个类，用于组合多个验证约束。实际上，还有其他方式来组合验证约束，例如使用注解或编程式 API。但如果你需要动态地组合多个验证约束，`SimpleConstraintTree` 可能是一个有用的工具。



org.hibernate.validator.HibernateValidator

ta继承了javax.validation.spi.ValidationProvider


`org.hibernate.validator.HibernateValidator` 是 `Hibernate Validator` 的一个类，它实现了 `javax.validation.ValidationProvider` 接口，用于将 `Hibernate Validator` 集成到 `javax.validation` API 中。

具体来说，当你在应用程序中使用 `javax.validation` API 时，`javax.validation.Validation` 工厂类会自动查找并加载实现了 `javax.validation.ValidationProvider` 接口的类。如果你使用的是 `Hibernate Validator`，那么 `HibernateValidator` 类就是实现了 `javax.validation.ValidationProvider` 接口的类之一。

`HibernateValidator` 类的主要作用是将 `Hibernate Validator` 集成到 `javax.validation` API 中，使得你可以使用标准的 JSR 303（Bean Validation）注解进行验证，并使用 `Hibernate Validator` 提供的扩展和增强功能。

当你在应用程序中创建 `javax.validation.Validator` 实例时，`javax.validation.Validation` 工厂类会自动使用 `HibernateValidator` 类来创建 `javax.validation.ValidatorFactory` 实例，并将其返回给你。这样，你就可以使用 `Hibernate Validator` 提供的所有功能来验证目标对象。

以下是一个使用 `Hibernate Validator` 进行 Bean 验证的示例：

```java
ValidatorFactory validatorFactory = Validation.byProvider(HibernateValidator.class)
        .configure()
        .buildValidatorFactory();

Validator validator = validatorFactory.getValidator();

Person person = new Person();
person.setName(null);
person.setAge(17);

Set<ConstraintViolation<Person>> violations = validator.validate(person);
```

在上述示例中，我们使用 `Validation.byProvider(HibernateValidator.class)` 方法创建一个 `ValidatorFactory` 实例，并将其配置为使用 `HibernateValidator`。然后，我们使用 `Validator` 实例来验证一个 `Person` 对象，并将验证结果存储在 `ConstraintViolation` 的集合中。

总之，`HibernateValidator` 类是 `Hibernate Validator` 的一部分，它实现了 `javax.validation.ValidationProvider` 接口，用于将 `Hibernate Validator` 集成到 `javax.validation` API 中。它的作用是使得你可以在应用程序中使用标准的 JSR 303（Bean Validation）注解进行验证，并使用 `Hibernate Validator` 提供的扩展和增强功能。


```java
    private static ValidatorFactory factory = Validation.byDefaultProvider()
        .configure()
        .messageInterpolator(new ParameterMessageInterpolator())
        .buildValidatorFactory();
```


org.hibernate.validator.messageinterpolation.ParameterMessageInterpolator 5.2才有的类
实现了javax.validation.MessageInterpolator


AbstractMessageInterpolator
实现类

```shell
AbstractMessageInterpolator (org.hibernate.validator.messageinterpolation)
    ParameterMessageInterpolator (org.hibernate.validator.messageinterpolation)
    ResourceBundleMessageInterpolator (org.hibernate.validator.messageinterpolation)
```

工厂模式

`org.hibernate.validator.HibernateValidator` 是 `Hibernate Validator` 的一个类，它实现了 `javax.validation.ValidationProvider` 接口，用于将 `Hibernate Validator` 集成到 `javax.validation` API 中。
具体来说，当你在应用程序中使用 `javax.validation` API 时，`javax.validation.Validation` 工厂类会自动查找并加载实现了 `javax.validation.ValidationProvider` 接口的类。如果你使用的是 `Hibernate Validator`，那么 `HibernateValidator` 类就是实现了 `javax.validation.ValidationProvider` 接口的类之一。
`HibernateValidator` 类的主要作用是将 `Hibernate Validator` 集成到 `javax.validation` API 中，使得你可以使用标准的 JSR 303（Bean Validation）注解进行验证，并使用 `Hibernate Validator` 提供的扩展和增强功能。
当你在应用程序中创建 `javax.validation.Validator` 实例时，`javax.validation.Validation` 工厂类会自动使用 `HibernateValidator` 类来创建 `javax.validation.ValidatorFactory` 实例，并将其返回给你。这样，你就可以使用 `Hibernate Validator` 提供的所有功能来验证目标对象。
以下是一个使用 `Hibernate Validator` 进行 Bean 验证的示例：

```java
ValidatorFactory validatorFactory = Validation.byProvider(HibernateValidator.class)
        .configure()
        .buildValidatorFactory();

Validator validator = validatorFactory.getValidator();

Person person = new Person();
person.setName(null);
person.setAge(17);

Set<ConstraintViolation<Person>> violations = validator.validate(person);
```

在上述示例中，我们使用 `Validation.byProvider(HibernateValidator.class)` 方法创建一个 `ValidatorFactory` 实例，并将其配置为使用 `HibernateValidator`。然后，我们使用 `Validator` 实例来验证一个 `Person` 对象，并将验证结果存储在 `ConstraintViolation` 的集合中。
总之，`HibernateValidator` 类是 `Hibernate Validator` 的一部分，它实现了 `javax.validation.ValidationProvider` 接口，用于将 `Hibernate Validator` 集成到 `javax.validation` API 中。它的作用是使得你可以在应用程序中使用标准的 JSR 303（Bean Validation）注解进行验证，并使用 `Hibernate Validator` 提供的扩展和增强功能。



使用注解来确定校验的范围
两组api
- javax.validation.constraints
- org.hibernate.validator.constraints

JSR提供的校验注解：         
@Null   被注释的元素必须为 null    
@NotNull    被注释的元素必须不为 null    
@AssertTrue     被注释的元素必须为 true    
@AssertFalse    被注释的元素必须为 false    
@Min(value)     被注释的元素必须是一个数字，其值必须大于等于指定的最小值    
@Max(value)     被注释的元素必须是一个数字，其值必须小于等于指定的最大值    
@DecimalMin(value)  被注释的元素必须是一个数字，其值必须大于等于指定的最小值    
@DecimalMax(value)  被注释的元素必须是一个数字，其值必须小于等于指定的最大值    
@Size(max=, min=)   被注释的元素的大小必须在指定的范围内    
@Digits (integer, fraction)     被注释的元素必须是一个数字，其值必须在可接受的范围内    
@Past   被注释的元素必须是一个过去的日期    
@Future     被注释的元素必须是一个将来的日期    
@Pattern(regex=,flag=)  被注释的元素必须符合指定的正则表达式


Hibernate Validator提供的校验注解：  
@NotBlank(message =)   验证字符串非null，且长度必须大于0    
@Email  被注释的元素必须是电子邮箱地址    
@Length(min=,max=)  被注释的字符串的大小必须在指定的范围内    
@NotEmpty   被注释的字符串的必须非空    
@Range(min=,max=,message=)  被注释的元素必须在合适的范围内



@Valid
类的属性也校验，加上@Valid
注解

validate-api spi
hibernate-validator 有spi配置文件吗？
是的，Hibernate Validator 提供了 SPI（Service Provider Interface）机制，可以通过 SPI 配置文件来自定义验证器和约束验证器的实现。
具体来说，Hibernate Validator 使用的是 Java 的 SPI 机制，需要在 `META-INF/services` 目录下创建名为 `javax.validation.ConstraintValidatorFactory` 和 `javax.validation.ValidationProvider` 的文件，然后在这些文件中指定相应的实现类。例如：
`META-INF/services/javax.validation.ConstraintValidatorFactory`
```
com.example.MyConstraintValidatorFactory
```
`META-INF/services/javax.validation.ValidationProvider`

```
org.hibernate.validator.HibernateValidator
```
在上述示例中，我们使用了自定义的 `MyConstraintValidatorFactory` 类作为约束验证器工厂类的实现，并将其指定为 `javax.validation.ConstraintValidatorFactory` SPI 的实现。同时，我们也指定了 Hibernate Validator 作为 `javax.validation.ValidationProvider` SPI 的实现。
值得注意的是，如果你想使用自定义的约束验证器，也需要在 `META-INF/services` 目录下创建名为 `javax.validation.ConstraintValidator` 的文件，并在其中指定相应的实现类。例如：
`META-INF/services/javax.validation.ConstraintValidator`
```
com.example.MyConstraintValidator
```
在上述示例中，我们使用了自定义的 `MyConstraintValidator` 类作为约束验证器的实现，并将其指定为 `javax.validation.ConstraintValidator` SPI 的实现。
总之，Hibernate Validator 提供了 SPI 机制来自定义验证器和约束验证器的实现。你可以通过在 `META-INF/services` 目录下创建相应的 SPI 配置文件来指定实现类。



javax.validation.spi.ValidationProvider文件
org.hibernate.validator.HibernateValidator

hibernate-validator-cdi jar

org.hibernate.validator.cdi.ValidationExtension

`hibernate-validator-cdi` 是 Hibernate Validator 项目中的一个可选模块，它提供了在 CDI（Contexts and Dependency Injection）环境下使用 Hibernate Validator 的支持。
具体来说，`hibernate-validator-cdi` 模块为 CDI 容器提供了一个扩展，使得在 CDI 环境下可以使用 Hibernate Validator 的验证器和约束注解。它可以让你在 CDI 中使用 `@Inject` 注入验证器和约束注解，以及在 CDI 生命周期中自动初始化和销毁验证器和约束注解。
另外，`hibernate-validator-cdi` 模块还提供了一个 `Validator` 类型的可注入对象，可以用于在 CDI 环境中进行验证操作。例如：

```java
@Inject
private Validator validator;

public void validateObject(Object object) {
    Set<ConstraintViolation<Object>> violations = validator.validate(object);
    // handle violations
}
```

在上述示例中，我们使用 `@Inject` 注入了 `Validator` 对象，并在 `validateObject` 方法中使用它对目标对象进行验证，并获取验证结果。

总之，`hibernate-validator-cdi` 模块是 Hibernate Validator 项目中的一个可选模块，它提供了在 CDI 环境下使用 Hibernate Validator 的支持，包括注入验证器和约束注解，以及提供可注入的 `Validator` 类型的对象用于验证操作。



testvalidation项目，使用logback打印日志成功
要在 Hibernate Validator 中使用 Logback 作为日志后端，需要在类路径下添加 `logback-classic` 和 `logback-core` 两个依赖，并在 `logback.xml` 中配置相应的日志输出规则。很方便

下面是一个简单的 `logback.xml` 配置示例，用于输出 Hibernate Validator 的调试日志信息：

```xml
<configuration>
  <appender name="console" class="ch.qos.logback.core.ConsoleAppender">
    <encoder>
      <pattern>%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern>
    </encoder>
  </appender>
  <logger name="org.hibernate.validator" level="DEBUG"/>
  <root level="INFO">
    <appender-ref ref="console" />
  </root>
</configuration>
```

在上述示例中，我们定义了一个名为 `console` 的控制台输出 appender，并将其添加到了 root logger 中。同时，我们也定义了一个名为 `org.hibernate.validator` 的 logger，用于输出 Hibernate Validator 的调试日志信息。通过设置 logger 的级别为 `DEBUG`，我们可以输出更详细的日志信息。

在应用程序启动时，Logback 会自动加载 `logback.xml` 配置文件，并根据其中的配置来输出日志信息。当 Hibernate Validator 初始化时，它会使用 Logback 作为日志后端，并按照相应的日志输出规则输出日志信息。

总之，要在 Hibernate Validator 中使用 Logback 作为日志后端，需要在类路径下添加相应的依赖，并配置相应的日志输出规则。这样可以让 Hibernate Validator 输出更详细的日志信息，帮助你更好地调试和排查问题。