# logback

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




common-logging是apache提供的一个通用的日志接口，
在common-logging中，有一个Simple logger的简单实现，但是它功能很弱，所以使用common-logging，通常都是配合着log4j来使用；

Commons Logging定义了一个自己的接口 org.apache.commons.logging.Log，以屏蔽不同日志框架的API差异，这里用到了Adapter Pattern（适配器模式）。


logback当前分成三个模块：logback-core,logback- classic和logback-access。logback-core是其它两个模块的基础模块。logback-classic是log4j的一个 改良版本。此外logback-classic完整实现SLF4J API使你可以很方便地更换成其它日志系统如log4j或JDK14 Logging。logback-access访问模块与Servlet容器集成提供通过Http来访问日志的功能

logback当前分成三个模块：logback-core,logback- classic和logback-access。logback-core是其它两个模块的基础模块。logback-classic是log4j的一个 改良版本。此外logback-classic完整实现SLF4J API使你可以很方便地更换成其它日志系统如log4j或JDK14 Logging。logback-access访问模块与Servlet容器集成提供通过Http来访问日志的功能