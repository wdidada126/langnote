# jsr

JSR-51
nio
aio

 Java Rule Engine API（JSR 94）

- drtools与 Java Rule Engine API（JSR 94）兼容


jsr305
https://blog.csdn.net/JonasErosonAtsea/article/details/76038676


JSR 305是一项Java规范，用于提供一组注解，用于标记代码中的预期行为和约束。然而，JSR 305已经在2011年停止维护，并且不再推荐使用。因此，没有官方的Maven坐标可用于JSR 305。

如果您的项目需要使用JSR 305的注解，可以考虑使用以下非官方的Maven坐标：

```xml
<dependency>
    <groupId>com.google.code.findbugs</groupId>
    <artifactId>jsr305</artifactId>
    <version>3.0.2</version>
</dependency>
```

上述Maven坐标使用了FindBugs项目的扩展版本，其中包含JSR 305的注解。请注意，这只是一个非官方的提供方式，因此使用时请注意仔细评估和测试所选择的依赖项。

另外，建议您在考虑使用JSR 305之前，了解其他替代方案，例如使用Java 8及更高版本中的`javax.annotation`包中的注解（如`@Nonnull`和`@Nullable`），或者使用更现代的静态代码分析工具来实现类似的功能。


JSR-000356 JavaTM API for WebSocket (Maintenance Release)
https://jcp.org/aboutJava/communityprocess/mrel/jsr356/index.html

websocket
https://www.oracle.com/technical-resources/articles/java/jsr356.html


https://jax-rs-spec.java.net/nonav/2.0/apidocs/index.html

JSR-51
java.nio.channels.spi.SelectorProvider

JSR-330 'javax.inject.Inject' annotation found and supported for autowiring

Java并发编程的艺术

JSR是Java Specification Requests的缩写，意思是Java 规范提案。是指向JCP(Java Community Process)提出新增一个标准化技术规范的正式请求。任何人都可以提交JSR，以向Java平台增添新的API和服务。JSR已成为Java界的一个重要标准。而决定规范提案是否通过，则是需要由一些Java界大牛（这些大牛来自于各大公司、各个领域）组成的评审委员会审核通过。
在这众多规范中，有一些规范，可能会有不同的提供商、组织来实现。例如JDBC的规范，各个数据库提供商来实现。根据Jsp/Servlet规范，产生了各个Web 服务器。
DI规范，各种DI框架都会遵守。JAX-WS、JAX-RS规范，各个WebService框架都会遵守。
所以呢，在编程时，我们一定要遵守响应的规范，这样代码写一次，就可以在他们的各种实现之间切换，而不需要对我们的业务逻辑有任何的调整。
为了对规范有一个更好的理解，决定开启规范学习的系列。
最后附上JSR的链接：https://jcp.org/en/jsr/all


[Spring核心——JSR250与资源控制](https://my.oschina.net/chkui/blog/1858734)

JSR-175与元编程
要说明JSR-250先要解释清楚JSR-175
JSR-175的全文标题是 A Metadata Facility for the Java Programming Language （为Java语言提供元数据设施）。它明确提出了在Java平台引入“元编程”（Meta Programming）的思想，要求提供对“元数据”（Meta Data）的支持。这就是我们现在大量使用的“@”注解（Annotation）功能的最早来源。JSR-175之后的JSR-181（Web服务支持）、JSR-250、JSR-330都是基于“元数据”功能提出的一些更细节的实现。



[JSR-330标准注解](https://maxwell.gitbook.io/way-to-architect/java-yu-yan/zhu-jie/chang-yong-zhu-jie/jsr-330biao-zhun-zhu-jie)


JCache (JSR-107)

翻译的不错.大部分内容来自于jsr-133和Doug Lea的jsr-133 Cookbook,如果想深入研究这方面的问题,推荐仔细研究一下上面的两个文献和本书里提及到的引用文献(当然还有Lea的另外两本书),本书文献的引用只提及于书的正文,末尾并没有参考文献.也许是书名的"著"导致的这个问题.