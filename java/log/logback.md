# logback

logback additivity="false"作用

在Logback中，`additivity`属性是用于控制日志事件是否传递到父级Logger的一个属性。当`additivity`属性设置为`true`时，日志事件会被传递到父级Logger中，而父级Logger也会处理这些日志事件。当`additivity`属性设置为`false`时，日志事件不会传递到父级Logger中，而只会在当前Logger中处理。
通常情况下，我们会将`additivity`属性设置为`true`，这样日志事件会被传递到父级Logger中，父级Logger也可以进行相应的处理。但是，在某些情况下，我们可能希望只在当前Logger中处理日志事件，而不希望将日志事件传递到父级Logger中，这时就可以将`additivity`属性设置为`false`。
例如，如果我们有一个应用程序，其中有多个模块，每个模块都有自己的Logger，同时还有一个根Logger，用于记录应用程序的所有日志事件。如果我们在某个模块中将`additivity`属性设置为`false`，那么该模块中的日志事件就不会传递到根Logger中，而只会在该模块的Logger中处理。这样可以避免在根Logger中重复记录该模块的日志事件。
需要注意的是，如果同时存在多个Logger，而其中某些Logger的`additivity`属性设置为`false`，那么这些Logger中的所有日志事件都不会传递到根Logger中。因此，在设置`additivity`属性时，需要根据实际情况进行选择，以便正确地记录和处理日志事件。


logback.grovvy


logback.xml
<configuration debug="true">开启debug

```shell
15:48:21,350 |-INFO in ch.qos.logback.classic.LoggerContext[default] - Could NOT find resource [logback.groovy]
15:48:21,350 |-INFO in ch.qos.logback.classic.LoggerContext[default] - Could NOT find resource [logback-test.xml]
15:48:21,350 |-INFO in ch.qos.logback.classic.LoggerContext[default] - Found resource [logback.xml] at [file:/D:/git/github/SpringAOPExample/target/classes/logback.xml]
15:48:21,540 |-INFO in ch.qos.logback.core.joran.action.AppenderAction - About to instantiate appender of type [ch.qos.logback.core.ConsoleAppender]
15:48:21,545 |-INFO in ch.qos.logback.core.joran.action.AppenderAction - Naming appender as [STDOUT]
15:48:21,638 |-INFO in ch.qos.logback.core.joran.action.AppenderAction - About to instantiate appender of type [ch.qos.logback.core.rolling.RollingFileAppender]
15:48:21,642 |-INFO in ch.qos.logback.core.joran.action.AppenderAction - Naming appender as [FILE]
15:48:21,668 |-INFO in c.q.l.core.rolling.TimeBasedRollingPolicy - No compression will be used
15:48:21,671 |-INFO in c.q.l.core.rolling.TimeBasedRollingPolicy - Will use the pattern /git/github/SpringAOPExample/log/TestWeb.log.%d{yyyy-MM-dd}.log for the active file
15:48:21,677 |-INFO in c.q.l.core.rolling.DefaultTimeBasedFileNamingAndTriggeringPolicy - The date pattern is 'yyyy-MM-dd' from file name pattern '/git/github/SpringAOPExample/log/TestWeb.log.%d{yyyy-MM-dd}.log'.
15:48:21,678 |-INFO in c.q.l.core.rolling.DefaultTimeBasedFileNamingAndTriggeringPolicy - Roll-over at midnight.
15:48:21,682 |-INFO in c.q.l.core.rolling.DefaultTimeBasedFileNamingAndTriggeringPolicy - Setting initial period to Mon Apr 12 15:48:21 CST 2021
15:48:21,694 |-INFO in ch.qos.logback.core.rolling.RollingFileAppender[FILE] - Active log file name: /git/github/SpringAOPExample/log/TestWeb.log.2021-04-12.log
15:48:21,695 |-INFO in ch.qos.logback.core.rolling.RollingFileAppender[FILE] - File property is set to [null]
15:48:21,696 |-INFO in ch.qos.logback.classic.joran.action.RootLoggerAction - Setting level of ROOT logger to DEBUG
15:48:21,697 |-INFO in ch.qos.logback.core.joran.action.AppenderRefAction - Attaching appender named [FILE] to Logger[ROOT]
15:48:21,698 |-INFO in ch.qos.logback.classic.joran.action.ConfigurationAction - End of configuration.
15:48:21,701 |-INFO in ch.qos.logback.classic.joran.JoranConfigurator@21bcffb5 - Registering current configuration as safe fallback point
```



common-logging通过动态查找的机制， 在程序运行时自动找出真正使用的日志库。由于它使用了ClassLoader寻找和载入底层的日志库， 导致了象OSGI这样的框架无法正常工作，因为OSGI的不同的插件使用自己的ClassLoader。 OSGI的这种机制保证了插件互相独立，然而却使Apache Common-Logging无法工作。

slf4j在编译时静态绑定真正的Log库,因此可以再OSGI中使用。另外，SLF4J 支持参数化的log字符串，避免了之前为了减少字符串拼接的性能损耗而不得不写的if(logger.isDebugEnable())，现在你可以直接写：logger.debug(“current user is: {}”, user)。拼装消息被推迟到了它能够确定是不是要显示这条消息的时候，但是获取参数的代价并没有幸免。


Chapter 12: Groovy Configuration
https://logback.qos.ch/manual/groovy.html

logback改进了log4j1
core api
classic 核心实现
https://www.cnblogs.com/warking/p/5710303.html


[日志：slf4j+logback 的配置与使用](https://blog.csdn.net/duguxiaobiao/article/details/78988409)

在springboot 中 ，也是使用的  slf4j + logback，所以我们划掉了 JCL

Logback是由log4j创始人设计的一个开源日志组件。logback当前分成三个模块：logback-core,logback-classic和logback-access。logback-core是其它两个模块的基础模块。logback-classic是log4j的一个改良版本。


<dependency>
    <groupId>ch.qos.logback</groupId>
    <artifactId>logback-classic</artifactId>
    <version>1.2.3</version>
    <scope>test</scope>
</dependency>

logback-classic依赖core
logback-access依赖core

<dependency>
    <groupId>ch.qos.logback</groupId>
    <artifactId>logback-access</artifactId>
    <version>1.2.3</version>
</dependency>


logback-access访问模块与Servlet容器集成提供通过Http来访问日记的功能。 


Spring使用common-logging
common-logging是apache提供的一个通用的日志接口，
在common-logging中，有一个Simple logger的简单实现，但是它功能很弱，所以使用common-logging，通常都是配合着log4j来使用；

Commons Logging定义了一个自己的接口 org.apache.commons.logging.Log，以屏蔽不同日志框架的API差异，这里用到了Adapter Pattern（适配器模式）。


logback当前分成三个模块：logback-core,logback- classic和logback-access。logback-core是其它两个模块的基础模块。logback-classic是log4j的一个 改良版本。此外logback-classic完整实现SLF4J API使你可以很方便地更换成其它日志系统如log4j或JDK14 Logging。logback-access访问模块与Servlet容器集成提供通过Http来访问日志的功能
