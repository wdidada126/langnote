# log4j2

SLF4J: Class path contains multiple SLF4J bindings.
SLF4J: Found binding in [jar:file:/D:/mavenrepository/201904/org/slf4j/slf4j-simple/1.7.25/slf4j-simple-1.7.25.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: Found binding in [jar:file:/D:/mavenrepository/201904/org/apache/logging/log4j/log4j-slf4j-impl/2.9.1/log4j-slf4j-impl-2.9.1.jar!/org/slf4j/impl/StaticLoggerBinder.class]
SLF4J: See http://www.slf4j.org/codes.html#multiple_bindings for an explanation.
SLF4J: Actual binding is of type [org.slf4j.impl.SimpleLoggerFactory]



[log4j2常见配置](https://www.cnblogs.com/gavinYang/p/8168928.html)


filePattern="${logDirect}/${logFileName}.%d{yyyy-MM-dd}.%i.log"

facial-recognition.2019-09-17.1.log



xml配置文件中不定义FILE_NAME变量
会产生
${FILE_NAME}-info.log


log.info("Save file to FastDFS and MySQL cost time: {} ms", System.currentTimeMillis() - start);

[%date][%c{1.}][%t][%p] dstTraceId:[%X{dstTraceId}] [%X{TRACE_LOG_ID}] -%msg%xEx%n
`[2019-09-16 19:37:02,334][c.b.m.i.e.s.i.ExtractImageServiceImpl][DubboServerHandler-172.17.47.182:20880-thread-3][INFO] dstTraceId:[] [default_request_id] -Save file to FastDFS and MySQL cost time: 13 ms`

Jetty 输出到Consule的日志，就输出到Jetty上
Tomcat是不是也这样

日志框架与log4j2

log4j2.garbagefreeThreadContextMap

自定义ContextDataInjector
ThreadContextDataInjector

log4j2.contextDataInjector
ContextDataInjector

org.apache.logging.log4j.core.ContextDataInjector

```java

ForGarbageFreeThreadContextMap in ThreadContextDataInjector (org.apache.logging.log4j.core.impl)
ForCopyOnWriteThreadContextMap in ThreadContextDataInjector (org.apache.logging.log4j.core.impl)
ForDefaultThreadContextMap in ThreadContextDataInjector (org.apache.logging.log4j.core.impl)

```

```java

Use %X by itself to include the full contents of the Map.
Use %X{key} to include the specified key.
Use %x to include the full contents of the Stack.

```

```java

ERROR StatusLogger No log4j2 configuration file found. Using default configuration: logging only errors to the console. Set system property 'org.apache.logging.log4j.simplelog.StatusLogger.level' to TRACE to show Log4j2 internal initialization logging.

```


[log4j2 读取配置文件](https://blog.csdn.net/honghailiang888/article/details/52859923)

@Slf4j2

`log.info("This is log:{}",traceLogId);`
不是
`log.info("This is log:{}"+traceLogId);`


```
Scanner-2 ERROR MarkerPatternSelector contains an invalid element or attribute "charset"
```

[PatternMatch key](https://www.docs4dev.com/docs/zh/log4j2/2.x/all/manual-usage.html)


[web环境下使用log4j2](https://zhuanlan.zhihu.com/p/36554554)

https://logging.apache.org/log4j/2.x/

[自测代码](https://github.com/edidada/testlog4j2)

[log4j2 实际使用详解](https://blog.csdn.net/vbirdbest/article/details/71751835)
[log4j2 使用详解](https://blog.csdn.net/lrenjun/article/details/8178875)

公司的日志规范 java开发规范 监控那边的日志规范
项目中log4j2的使用

RollingRandomAccessFile 会根据命名规则当文件满足一定大小时就会另起一个新的文件

Log4J 主要构件

Log4J 是 Apache 组织提供的一个日志组件, 它设计了灵活的配置文件，利用它可以在不更改程序的情况下,通过修改配置文件来调控日志的输出。下面是 Log4J 最主要的三大基本构件：

记录器（Loger）
对日志信息进行分类筛选。通过指定优先级，控制程序中日志信息的输出：高于优先级的日志可以被输出，低于优先级的日志则被忽略。

输出源（Appenders）
指定日志信息的输出设备。Log4J 目前支持的输出设备有以下几种：

org.apache.log4j.ConsoleAppender(控制台)
org.apache.log4j.FileAppender（文件）
org.apache.log4j.DailyRollingFileAppender（每天产生一个日志文件）
org.apache.log4j.RollingFileAppender（文件大小到达指定尺寸的时候产生一个新的文件）
org.apache.log4j.WriterAppender（将日志信息以流格式发送到任意指定的地方）
org.apache.log4j.SocketAppender (Socket)
org.apache.log4j.NtEventLogAppender (NT的Event Log)
org.apache.log4j.JMSAppender (电子邮件）
程序员也可以根据自己的需要定制 Appenders，实现更复杂和更为方便实用的日志管理，比如把日志输入数据库，或者传输到统一的日志服务器，等等。

布局（Layouts）
指定日志输出的格式。Log4J 提供的 Layout 有以下几种：


org.apache.log4j.HTMLLayout（以 HTML 表格形式布局）
org.apache.log4j.PatternLayout（可以灵活地指定布局模式）
org.apache.log4j.SimpleLayout（包含日志信息的级别和信息字符串）
org.apache.log4j.TTCCLayout（包含日志产生的时间、线程、类别等等信息）

ConsoleAppender父类类继承关系图

AbstractLifeCycle (org.apache.logging.log4j.core)
    AbstractFilterable (org.apache.logging.log4j.core.filter)
        AbstractAppender (org.apache.logging.log4j.core.appender)
            AbstractOutputStreamAppender (org.apache.logging.log4j.core.appender)
                RollingRandomAccessFileAppender (org.apache.logging.log4j.core.appender)
                MemoryMappedFileAppender (org.apache.logging.log4j.core.appender)
                ConsoleAppender (org.apache.logging.log4j.core.appender)
                SocketAppender (org.apache.logging.log4j.core.appender)
                    SyslogAppender (org.apache.logging.log4j.core.appender)
                FileAppender (org.apache.logging.log4j.core.appender)
                RandomAccessFileAppender (org.apache.logging.log4j.core.appender)
                OutputStreamAppender (org.apache.logging.log4j.core.appender)
                RollingFileAppender (org.apache.logging.log4j.core.appender)


ConfigurationBuilderFactory (org.apache.logging.log4j.core.config.builder.api)
    ConfigurationFactory (org.apache.logging.log4j.core.config)
        XmlConfigurationFactory (org.apache.logging.log4j.core.config.xml)
            ServerConfigurationFactory in AbstractSocketServer (org.apache.logging.log4j.core.net.server)
        JsonConfigurationFactory (org.apache.logging.log4j.core.config.json)
        PropertiesConfigurationFactory (org.apache.logging.log4j.core.config.properties)
        Factory in ConfigurationFactory (org.apache.logging.log4j.core.config)
        YamlConfigurationFactory (org.apache.logging.log4j.core.config.yaml)

NDC

MDC
Mapped Diagnostic Context

Log4j能够自动检测配置文件的更改并重新配置自身。如果在配置元素上指定了monitorInterval属性并将其设置为非零值，则下次评估和/或记录日志事件时将检查该文件，并且自上次检查后已经过了monitorInterval。


从版本2.9开始，出于安全原因，Log4j不处理XML文件中的DTD。如果要将配置拆分为多个文件，请使用XInclude或 Composite Configuration。

XInclude 多个文件 公司有用到



<?xml version="1.0" encoding="UTF-8"?>;
<Configuration>
  <Properties>
    <Property name="name1">value</property>
    <Property name="name2" value="value2"/>
  </Properties>
  <filter  ... />
  <Appenders>
    <appender ... >
      <filter  ... />
    </appender>
    ...
  </Appenders>
  <Loggers>
    <Logger name="name1">
      <filter  ... />
    </Logger>
    ...
    <Root level="level">
      <AppenderRef ref="name"/>
    </Root>
  </Loggers>
</Configuration>


org.apache.logging.log4j.spi


### Lookup


### 

log4j2的日志文件可以同时分级别（info、error等），分进进程存储


https://logging.apache.org/log4j/2.x/manual/lookups.html

OutputStreamAppender

RandomAccessFileAppender
RewriteAppender


doc目录
Layout
Appender


@伍成?正好以此为契机，伍成去调研一下log4j2，两周后给我们团队内部做个培训
顺便调研一下MDC和ThreadContext的区别，以及看一下log4j2能否或者如何使用MDC

mdc Mapped Diagnostic Context

[thread context 和mdc](https://logging.apache.org/log4j/2.x/manual/thread-context.html)

log4j-1.2-api

log4j-slf4j-impl

https://logging.apache.org/log4j/2.x/runtime-dependencies.html

https://veerasundar.com/blog//2009/11/log4j-mdc-mapped-diagnostic-context-example-code/

门面模式

SLF4J，即简单日志门面（Simple Logging Facade for Java），不是具体的日志解决方案，它只服务于各种各样的日志系统。按照官方的说法，SLF4J是一个用于日志系统的简单Facade，允许最终用户在部署其应用时使用其所希望的日志System.

实际上，SLF4J所提供的核心API是一些接口以及一个LoggerFactory的工厂类。从某种程度上，SLF4J有点类似JDBC，不过比JDBC更简单，在JDBC中，你需要指定驱动程序，而在使用SLF4J的时候，不需要在代码中或配置文件中指定你打算使用那个具体的日志系统。如同使用JDBC基本不用考虑具体数据库一样，SLF4J提供了统一的记录日志的接口，只要按照其提供的方法记录即可，最终日志的格式、记录级别、输出方式等通过具体日志系统的配置来实现，因此可以在应用中灵活切换日志系统。

java.lang.ref.WeakReference

javax.xml.transform.stream.StreamSource

<dependency>
    <groupId>org.slf4j</groupId>
    <artifactId>slf4j-log4j12</artifactId>
    <version>1.7.25</version>
    <scope>test</scope>
</dependency>


大纲：
log4j2的更新记录，与log4j的区别
log4j2与其他java日志框架的区别
log4j2的使用方式lombok slf4j结合
配置文件 xml格式
设置buffer大小，自动归类
分date存储
自带的环境变量
mdc
ThreadContext

-x
ThreadContext.put()
push()/pop()

Loggers配置项
分级logger

Log4j2 Route作用
输出日志到不同的文件

https://blog.csdn.net/userwyh/article/details/52862216

我们使用%X{userName}来定义此处会打印MDC里面key为userName的value，如果所定义的字段在MDC不存在对应的key，那么将不会打印，会留一个占位符。

@Slf4j
log.info("");

在log4j2中,一切皆插件,框架通过PluginRegistry扫描并发现插件配置.
PluginRegistry支持两种扫描方式

一种是使用指定的ClassLoader读取classpath下所有的META-INF/org/apache/logging/log4j/core/config/plugins/Log4j2Plugins.dat文件,产生PluginType;
另一种是扫描classpath下指定的packageName,内省带有@Plugin注解的类文件,产生PluginType.
