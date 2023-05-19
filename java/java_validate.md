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
