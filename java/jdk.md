# jdk


java jar


C:\Program Files\Java\jre1.8.0_20\lib\charsets.jar
C:\Program Files\Java\jre1.8.0_20\lib\deploy.jar
C:\Program Files\Java\jre1.8.0_20\lib\javaws.jar
C:\Program Files\Java\jre1.8.0_20\lib\jce.jar
C:\Program Files\Java\jre1.8.0_20\lib\jfr.jar
C:\Program Files\Java\jre1.8.0_20\lib\jfxswt.jar
C:\Program Files\Java\jre1.8.0_20\lib\jsse.jar
C:\Program Files\Java\jre1.8.0_20\lib\management-agent.jar
C:\Program Files\Java\jre1.8.0_20\lib\plugin.jar
C:\Program Files\Java\jre1.8.0_20\lib\resources.jar
C:\Program Files\Java\jre1.8.0_20\lib\rt.jar
C:\Program Files\Java\jre1.8.0_20\lib\ext\access-bridge-64.jar
C:\Program Files\Java\jre1.8.0_20\lib\ext\cldrdata.jar
C:\Program Files\Java\jre1.8.0_20\lib\ext\dnsns.jar
C:\Program Files\Java\jre1.8.0_20\lib\ext\jaccess.jar
C:\Program Files\Java\jre1.8.0_20\lib\ext\jfxrt.jar
C:\Program Files\Java\jre1.8.0_20\lib\ext\localedata.jar
C:\Program Files\Java\jre1.8.0_20\lib\ext\nashorn.jar
C:\Program Files\Java\jre1.8.0_20\lib\ext\sunec.jar
C:\Program Files\Java\jre1.8.0_20\lib\ext\sunjce_provider.jar
C:\Program Files\Java\jre1.8.0_20\lib\ext\sunmscapi.jar
C:\Program Files\Java\jre1.8.0_20\lib\ext\sunpkcs11.jar
C:\Program Files\Java\jre1.8.0_20\lib\ext\zipfs.jar
C:\Program Files\Java\jre1.8.0_20\lib\security\local_policy.jar
C:\Program Files\Java\jre1.8.0_20\lib\security\US_export_policy.jar

各个jar包干嘛的

在Java的JRE（Java Runtime Environment，Java运行时环境）中，包含了多个JAR（Java ARchive）文件，这些文件是Java平台的核心组件，提供了各种库和功能。下面是对您列出的各个JAR文件用途的简要说明：

lib 目录下的 JAR 文件
charsets.jar：包含Java平台支持的字符集编码。
deploy.jar：用于Java Web Start（Java的浏览器启动技术）的部署和更新功能。
javaws.jar：Java Web Start的核心库，用于从Web上启动Java应用程序。
jce.jar：Java加密扩展（Java Cryptography Extension）的库，提供加密、密钥生成和消息摘要等安全功能。
jfr.jar：Java Flight Recorder的库，用于收集Java虚拟机（JVM）的性能数据。
jfxswt.jar：JavaFX与SWT（Standard Widget Toolkit）的集成库，允许JavaFX应用程序与SWT组件互操作。
jsse.jar：Java安全套接字扩展（Java Secure Socket Extension）的库，提供安全的网络通信功能。
management-agent.jar：Java管理扩展（JMX）的代理库，用于远程监控和管理Java应用程序。
plugin.jar：Java浏览器插件的库，用于在浏览器中运行Java小程序（Applet，现已废弃）。
resources.jar：包含Java平台的标准资源文件，如国际化资源。
rt.jar：Java运行时的核心库，包含了Java SE API的大部分类。
lib\ext 目录下的 JAR 文件
access-bridge-64.jar：Java Access Bridge的64位版本，用于提高Java应用程序与屏幕阅读器等辅助技术的互操作性。
cldrdata.jar：包含Unicode Common Locale Data Repository（CLDR）的数据，用于支持国际化。
dnsns.jar：DNS Name Service的扩展，可能用于处理域名服务相关的功能。
jaccess.jar：Java访问桥（Java Access Bridge）的库，同上但可能针对特定版本的JVM。
jfxrt.jar：JavaFX Runtime的库，提供JavaFX应用程序的运行时支持。
localedata.jar：包含本地化数据的库，用于支持不同语言和地区的本地化显示。
nashorn.jar：Nashorn JavaScript引擎的库，Java 8中引入的，用于在JVM上执行JavaScript代码。
sunec.jar：Sun的加密扩展库，提供额外的加密功能。
sunjce_provider.jar：Sun的Java加密扩展（JCE）提供程序库，包含加密算法的实现。
sunmscapi.jar：Sun的Microsoft CryptoAPI提供程序库，允许Java应用程序使用Windows平台上的加密服务。
sunpkcs11.jar：Sun的PKCS#11提供程序库，用于访问PKCS#11兼容的硬件安全模块（HSM）。
zipfs.jar：ZIP文件系统的库，允许将ZIP文件作为文件系统挂载和访问。
lib\security 目录下的 JAR 文件
local_policy.jar 和 US_export_policy.jar：这两个JAR文件包含Java加密策略的本地和美国出口限制版本。它们定义了哪些加密强度和算法在JVM中可用。
这些JAR文件共同构成了Java平台的基础，使得Java应用程序能够执行各种任务，包括网络通信、图形用户界面、国际化、安全通信等。

## 下载地址

https://jdk.java.net/archive/

https://www.oracle.com/java/technologies/downloads/#java8


jdk SelectorProvider
spi



jsr

jcp  流程 不是委员会

openjdk

oraclejdk

[jdk新特性](https://blog.csdn.net/lzw2497727771/article/details/104019737)

java为何要设计Cloneable这个接口clone这个方法很奇怪，它在Object类中被定义，定义时是个protected类型，也就是说只能被同一包中的类以及子类访问，这个方法没有实现Cloneable接口(一个只有名字没有任何方法的空接口).
然而java规定所有类若要使用clone方法必须要实现Clonneable接口，没错就是那个空接口，以达到标记的作用，不然会报CloneNotSupportedException，想必这些是在clone方法里面写好的
但是为什么一定要弄这个标记空接口呢？真的只是为了标记吗？那为什么clone方法需要被标记呢？感觉没什么用啊

Cloneable 本身就是个比较鸡肋的接口，尽量避免使用。

如果一个类重写了 Object 内定义的 clone() ，需要同时实现 Cloneable 接口（虽然这个接口内并没有定义 clone() 方法），否则在调用 clone() 时会报 CloneNotSupportedException 异常，也就是说， Cloneable 接口只是个合法调用 clone() 的标识（marker-interface）。

事实上，若想实现对象的克隆，你不得不重写 Object 的 clone() 方法，还得实现 Cloneable 接口，这样就有点麻烦了。

简单的做法，借助 Apache Commons 可以直接实现：

- 深克隆/拷贝（deep clone/copy）： [SerializationUtils](http://commons.apache.org/proper/commons-lang/api-2.5/org/apache/commons/lang/SerializationUtils.html)
- 浅克隆/拷贝（shallow clone/copy）：[BeanUtils](http://commons.apache.org/proper/commons-beanutils/)

简单的克隆，也可以通过 copy-constructor (拷贝构造方法) 实现，详情参考 Effective Java 作者 Josh Bloch 的这篇访谈：[Copy Constructor Versus Cloning](https://link.zhihu.com/?target=http%3A//www.artima.com/intv/bloch13.html)

其中也谈到了 Cloneable 接口的很多缺点。

C:\Program Files\JetBrains\IntelliJ IDEA 2018.2.4\jre64\lib\tools.jar

https://docs.oracle.com/javase/8/docs/technotes/tools/windows/jdkfiles.html#A1098669

Files used by the development tools. Includes tools.jar, which contains non-core classes for support of the tools and utilities in the JDK. Also includes dt.jar, the DesignTime archive of BeanInfo files that tell interactive development environments (IDEs) how to display the Java components and how to let the developer customize them for an application.

Jdk 二进制工具

Java agent

javap
反编译

jar
jarsigner
javac
javadoc
javah
javapackager
java-rmi
javaw
jcmd
jconsole

https://www.cnblogs.com/createyuan/p/11038958.html


tcp上层应用如何获取协议类型

Wireshark可以设置应用层解析的协议
Kafka，手动设置



java.util.function

JAVA8的java.util.function包
https://www.cnblogs.com/linzhanfly/p/9686941.html

https://www.jianshu.com/p/3c27dfd647f1
