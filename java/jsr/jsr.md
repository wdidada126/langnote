# jsr

lambda表达式
com_annotations-1_0-fr-spec.pdf
jsr335-final.zip

https://www.jcp.org/en/jsr/detail?id=335

JSR 250 – Common Annotations 1.3
JSR 335: Lambda Expressions for the JavaTM Programming Language
JSR 366 – Java EE 8 Platform
JSR 365 – Contexts and Dependency Injection (CDI) 2.0
JSR 367 – The Java API for JSON Binding (JSON-B) 1.0
JSR 369 – Java Servlet 4.0
JSR 370 – Java API for RESTful Web Services (JAX-RS) 2.1
JSR 372 – JavaServer Faces (JSF) 2.3
JSR 374 – Java API for JSON Processing (JSON-P)1.1
JSR 375 – Java EE Security API 1.0
JSR 380 – Bean Validation 2.0
JSR 338 – Java Persistence 2.2
JSR 356 – Java API for WebSocket 1.1
JSR 919 – JavaMail 1.6

JSR-250规范定义的注解，它们分别是@Resource、@PostConstruct以及@PreDestroy。

JSR303 - Bean Validation 为JavaBean的验证定义了相关的元数据模型和API。
org.hibernate.validator.constraints.NotEmpty
作用？
Java中的Validator验证框架对应的JSR标准是JSR303，也被称为Bean Validation。在Java官方提出Bean Validation规范后，经历了JSR303、JSR349、JSR380三次标准的更迭，发展到了2.0。在Spring框架中，也有一个类似的验证机制，具体为@Validated，它是Spring对JSR-303规范的一种变种实现。
在 java 8 之后，又推出了JSR380 - Bean Validation 2.0


JSR-51
nio
aio

 Java Rule Engine API（JSR 94）

- drtools与 Java Rule Engine API（JSR 94）兼容

JSR-51，即“New I/O APIs”，是Java平台的一个重要规范，旨在为Java引入更高效、更强大的I/O处理能力。这个提议主要关注于非阻塞I/O和文件系统访问的改进，特别是为了支持高并发服务器应用的发展需求。下面是对JSR-51的详细介绍：

### 核心内容

1. 非阻塞I/O（Non-blocking I/O）:
   - JSR-51引入了`java.nio.channels`包，其中包含了对非阻塞I/O的支持。
   - 这种类型的I/O允许一个线程管理多个通道（Channel），从而提高了资源利用率和程序效率。

2. 选择器（Selectors）:
   - `Selector`类使得单个线程能够监控多个通道的状态变化（比如数据是否可读或可写），这样就可以在不使用多线程的情况下实现高效的网络服务端设计。
   
3. 字符集与编解码器（Charsets and Coders）:
   - 提供了灵活的字符编码转换机制，使得不同字符集之间的转换更加容易。
   - 通过`Charset`, `CharsetEncoder`, 和 `CharsetDecoder`类来实现。

4. 文件通道（File Channels）:
   - 引入了`FileChannel`类，提供了比传统`java.io`包中的文件访问方法更为强大和灵活的操作方式。
   - 支持文件锁定、内存映射文件等高级功能。

5. 内存映射文件（Memory-mapped Files）:
   - 允许将文件或文件的一部分直接映射到内存中，大大提高了大文件的读写速度。

### 影响与意义

JSR-51极大地增强了Java在处理网络通信和文件操作方面的能力，特别是在需要高性能和高并发的应用场景中。例如，它使得构建如Web服务器、数据库管理系统等软件变得更加简单和高效。此外，通过提供更加底层的I/O控制，也为开发者提供了更多的灵活性和控制力。

### 实现细节

JSR-51的具体实现依赖于操作系统提供的本地I/O特性。例如，在Linux上，非阻塞I/O通常会利用epoll机制；而在Windows平台上，则可能使用完成端口（Completion Ports）。这意味着，虽然JSR-51提供了跨平台的API，但其性能和行为可能会受到具体操作系统的影响。

总之，JSR-51是Java发展过程中的一个重要里程碑，它不仅扩展了语言的功能性，还为开发高性能应用程序奠定了基础。对于那些需要处理大量并发连接或者进行高效文件操作的应用来说，了解并掌握JSR-51的相关知识是非常有价值的。


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