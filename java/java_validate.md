#  java validate

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
