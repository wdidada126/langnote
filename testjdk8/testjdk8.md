# testjdk8


testjdk8项目cn.wdidada.lambda.Lambda2
Java 8 动态类型语言Lambda表达式实现原理分析
https://blog.csdn.net/raintungli/article/details/54910152
Java的调用函数的四大指令（invokevirtual、invokespecial、invokestatic、invokeinterface)，通常方法的符号引用在静态类型语言编译时就能产生，而动态类型语言只有在运行期才能确定接收者类型，改变四大指令的语意对java的版本有很大的影响，所以在JSR 292 《Supporting Dynamically Typed Languages on the Java Platform》添加了一个新的指令


java8中map新增方法详解
java8中Stream的使用   20210406评注：面试题
java8中Collection新增方法详解
java8中Collectors的方法使用实例
java8中常用函数式接口
java8中的方法引用和构造函数引用
java8中的Collectors.groupingBy用法
java8中的Optional用法
java8中的日期和时间API


```shell
D:\git\github\testjdk8>jps
12880 RemoteMavenServer36
75520 Run_13
76148 Jps
66872
12124 jar

D:\git\github\testjdk8>jstack 75520
2021-04-06 19:25:00
Full thread dump Java HotSpot(TM) 64-Bit Server VM (25.231-b11 mixed mode):

"DestroyJavaVM" #13 prio=5 os_prio=0 tid=0x0000000002743800 nid=0x12d28 waiting on condition [0x0000000000000000]
   java.lang.Thread.State: RUNNABLE

"Thread-1" #12 prio=5 os_prio=0 tid=0x000000001d30d800 nid=0xd560 waiting for monitor entry [0x000000001df9f000]
   java.lang.Thread.State: BLOCKED (on object monitor)
        at cn.wdidada.deadlock.Run_13$DealThread.run(Run_13.java:49)
        - waiting to lock <0x000000076b437618> (a java.lang.Object)
        - locked <0x000000076b437628> (a java.lang.Object)
        at java.lang.Thread.run(Thread.java:748)

"Thread-0" #11 prio=5 os_prio=0 tid=0x000000001d30b000 nid=0x132dc waiting for monitor entry [0x000000001de9e000]
   java.lang.Thread.State: BLOCKED (on object monitor)
        at cn.wdidada.deadlock.Run_13$DealThread.run(Run_13.java:36)
        - waiting to lock <0x000000076b437628> (a java.lang.Object)
        - locked <0x000000076b437618> (a java.lang.Object)
        at java.lang.Thread.run(Thread.java:748)

"Service Thread" #10 daemon prio=9 os_prio=0 tid=0x000000001d2a3800 nid=0x12dd4 runnable [0x0000000000000000]
   java.lang.Thread.State: RUNNABLE

"C1 CompilerThread2" #9 daemon prio=9 os_prio=2 tid=0x000000001d29e000 nid=0xd834 waiting on condition [0x0000000000000000]
   java.lang.Thread.State: RUNNABLE

"C2 CompilerThread1" #8 daemon prio=9 os_prio=2 tid=0x000000001d245000 nid=0x13170 waiting on condition [0x0000000000000000]
   java.lang.Thread.State: RUNNABLE

"C2 CompilerThread0" #7 daemon prio=9 os_prio=2 tid=0x000000001d244000 nid=0x10b64 waiting on condition [0x0000000000000000]
   java.lang.Thread.State: RUNNABLE

"Monitor Ctrl-Break" #6 daemon prio=5 os_prio=0 tid=0x000000001d22a000 nid=0x130a0 runnable [0x000000001d89e000]
   java.lang.Thread.State: RUNNABLE
        at java.net.SocketInputStream.socketRead0(Native Method)
        at java.net.SocketInputStream.socketRead(SocketInputStream.java:116)
        at java.net.SocketInputStream.read(SocketInputStream.java:171)
        at java.net.SocketInputStream.read(SocketInputStream.java:141)
        at sun.nio.cs.StreamDecoder.readBytes(StreamDecoder.java:284)
        at sun.nio.cs.StreamDecoder.implRead(StreamDecoder.java:326)
        at sun.nio.cs.StreamDecoder.read(StreamDecoder.java:178)
        - locked <0x000000076b307568> (a java.io.InputStreamReader)
        at java.io.InputStreamReader.read(InputStreamReader.java:184)
        at java.io.BufferedReader.fill(BufferedReader.java:161)
        at java.io.BufferedReader.readLine(BufferedReader.java:324)
        - locked <0x000000076b307568> (a java.io.InputStreamReader)
        at java.io.BufferedReader.readLine(BufferedReader.java:389)
        at com.intellij.rt.execution.application.AppMainV2$1.run(AppMainV2.java:61)

"Attach Listener" #5 daemon prio=5 os_prio=2 tid=0x000000001be60000 nid=0x12fc0 waiting on condition [0x0000000000000000]
   java.lang.Thread.State: RUNNABLE

"Signal Dispatcher" #4 daemon prio=9 os_prio=2 tid=0x000000001d1b0800 nid=0xb7b8 runnable [0x0000000000000000]
   java.lang.Thread.State: RUNNABLE

"Finalizer" #3 daemon prio=8 os_prio=1 tid=0x0000000002837000 nid=0x12b18 in Object.wait() [0x000000001d19e000]
   java.lang.Thread.State: WAITING (on object monitor)
        at java.lang.Object.wait(Native Method)
        - waiting on <0x000000076b188ed8> (a java.lang.ref.ReferenceQueue$Lock)
        at java.lang.ref.ReferenceQueue.remove(ReferenceQueue.java:144)
        - locked <0x000000076b188ed8> (a java.lang.ref.ReferenceQueue$Lock)
        at java.lang.ref.ReferenceQueue.remove(ReferenceQueue.java:165)
        at java.lang.ref.Finalizer$FinalizerThread.run(Finalizer.java:216)

"Reference Handler" #2 daemon prio=10 os_prio=2 tid=0x0000000002834000 nid=0x131c4 in Object.wait() [0x000000001d09f000]
   java.lang.Thread.State: WAITING (on object monitor)
        at java.lang.Object.wait(Native Method)
        - waiting on <0x000000076b186c00> (a java.lang.ref.Reference$Lock)
        at java.lang.Object.wait(Object.java:502)
        at java.lang.ref.Reference.tryHandlePending(Reference.java:191)
        - locked <0x000000076b186c00> (a java.lang.ref.Reference$Lock)
        at java.lang.ref.Reference$ReferenceHandler.run(Reference.java:153)

"VM Thread" os_prio=2 tid=0x000000001be17000 nid=0x13168 runnable

"GC task thread#0 (ParallelGC)" os_prio=0 tid=0x0000000002759800 nid=0x126e4 runnable

"GC task thread#1 (ParallelGC)" os_prio=0 tid=0x000000000275b000 nid=0x1316c runnable

"GC task thread#2 (ParallelGC)" os_prio=0 tid=0x000000000275c800 nid=0x12938 runnable

"GC task thread#3 (ParallelGC)" os_prio=0 tid=0x000000000275e000 nid=0xcefc runnable

"VM Periodic Task Thread" os_prio=2 tid=0x000000001d2d6000 nid=0x130c0 waiting on condition

JNI global references: 12


Found one Java-level deadlock:
=============================
"Thread-1":
  waiting to lock monitor 0x000000001be406d8 (object 0x000000076b437618, a java.lang.Object),
  which is held by "Thread-0"
"Thread-0":
  waiting to lock monitor 0x000000001be3dce8 (object 0x000000076b437628, a java.lang.Object),
  which is held by "Thread-1"

Java stack information for the threads listed above:
===================================================
"Thread-1":
        at cn.wdidada.deadlock.Run_13$DealThread.run(Run_13.java:49)
        - waiting to lock <0x000000076b437618> (a java.lang.Object)
        - locked <0x000000076b437628> (a java.lang.Object)
        at java.lang.Thread.run(Thread.java:748)
"Thread-0":
        at cn.wdidada.deadlock.Run_13$DealThread.run(Run_13.java:36)
        - waiting to lock <0x000000076b437628> (a java.lang.Object)
        - locked <0x000000076b437618> (a java.lang.Object)
        at java.lang.Thread.run(Thread.java:748)

Found 1 deadlock.
```


java8中的Collectors.groupingBy用法
https://blog.csdn.net/u014231523/article/details/102535902

- CyclicBarrierDemo

CyclicBarrier await
CyclicBarrie构造函数有一个runnable参数

[设置Maven的默认jdk编译版本](https://blog.csdn.net/jxchallenger/article/details/90247471)

SPI
Java spi

solid 面向接口编程，接口与实现分离



更改SPI实现类需要重启程序吗？还是更改文件后就试试生效



- TestJavaSPI 可以运行的程序



java.util.ServiceLoader#load(java.lang.Class<S>)

javax.annotation.concurrent.ThreadSafe   注解，标注类是线程安全的

java.lang.ref.WeakReference

JUnit 多个方法测试顺序
@FixMethodOrder(MethodSorters.NAME_ASCENDING)作用在类上


### javax.inject



### java.util.Dictionary

java.util.Dictionary 抽象类
废弃了

新类继承Map，不需要继承Dictionary
Hashtable extends Dictionary impl Map

### java.lang

####  java.lang.annotation

ProcessBuilder



ProcessBuilder类是J2SE 1.5在java.lang中新添加的一个新类，此类用于创建操作系统进程，它提供一种启动和管理进程（也就是应用程序）的方法。在J2SE 1.5之前，都是由Process类处来实现进程的控制管理。




java 1.8

StringBuffer
synchronized

java.lang.reflect.AnnotatedElement



下面列出Java NIO中最重要的集中Channel的实现：



java io

Reader/Wroter

InputStream OutputStream





Throwable Exception RuntimeException

NullPointException IllegralStateException



common-io 二..七版本IOUtils FileUtils不支持



FileChannel
DatagramChannel
SocketChannel
ServerSocketChannel
FileChannel用于文件的数据读写。 DatagramChannel用于UDP的数据读写。 SocketChannel用于TCP的数据读写。 ServerSocketChannel允许我们监听TCP链接请求，每个请求会创建会一个SocketChannel.



[JAVA网络编程-NIO之SocketChannel代码实例](https://www.cnblogs.com/kooker/p/9559040.html)

[Java NIO Channel示例](https://blog.csdn.net/lianggx3/article/details/89297720)

Buffer的基本原理
buffer中有三个重要参数：位置（position）、容量（capacity）、上限（limit）。
位置（position）：当前缓冲区（Buffer）的位置，将从该位置往后读或写数据。
容量（capacity）：缓冲区的总容量上限。
上限（limit）：缓冲区的实际容量大小。

[Java NIO编程实例之二Channel](https://zhuanlan.zhihu.com/p/25914350)



AIO编程
JDK1.7引入了Asynchronous I/O,既AIO。再进行I/O编程中，常用到两种模式 ：Reactor和Proactor。Java的NIO就是Reactor，当有事件触发时，服务器端得到通知，进行相应的处理。
AIO即NIO2.0，叫做异步不阻塞的IO。AIO引入异步通道的概念，采用了Proactor模式，简化了程序编写，一个有效的请求才启动一个线程，它的特点是先有操作系统完成后才通知服务端程序启动线程去处理，一般适用于连接数较多且连接时间长的应用。

java.lang.annotation.ElementType#TYPE_PARAMETER

java.lang.annotation.ElementType#TYPE_USE




The common interface extended by all annotation types

java.lang.annotation.Annotation



[Java NIO系列教程（七） FileChannel](https://ifeve.com/file-channel/)



###### log

这里贴出JDK关于该类的介绍

Logger 对象用来记录特定系统或应用程序组件的日志消息。一般使用圆点分隔的层次名称空间来命名 Logger。Logger 名称可以是任意的字符串，但是它们一般应该基于被记录组件的包名或类名，如 java.net 或 javax.swing。此外，可以创建“匿名”的 Logger，其名称未存储在 Logger 名称空间中。
可通过调用某个 getLogger 工厂方法来获得 Logger 对象。这些方法要么创建一个新 Logger，要么返回一个合适的现有 Logger。
日志消息被转发到已注册的 Handler 对象，该对象可以将消息转发到各种目的地，包括控制台、文件、OS 日志等等。
每个 Logger 都跟踪一个“父”Logger，也就是 Logger 名称空间中与其最近的现有祖先。
每个 Logger 都有一个与其相关的 "Level"。这反映了此 logger 所关心的最低 Level。如果将 Logger 的级别设置为 null，那么它的有效级别继承自父 Logger，这可以通过其父 Logger 一直沿树向上递归得到。
可以根据日志配置文件的属性来配置日志级别，在 LogManager 类的描述中对此有所说明。但是也可以通过调用 Logger.setLevel 方法动态地改变它。如果日志级别改变了，则此变化也会影响它的子 logger，因为任何级别为 null 的子 logger 的有效级别都继承自它的父 Logger。
对于每次日志记录调用，Logger 最初都依照 logger 的有效日志级别对请求级别（例如 SEVERE 或 FINE）进行简单的检查。如果请求级别低于日志级别，则日志记录调用将立即返回。
通过此初始（简单）测试后，Logger 将分配一个 LogRecord 来描述日志记录消息。接着调用 Filter（如果存在）进行更详细的检查，以确定是否应该发布该记录。如果检查通过，则将 LogRecord 发布到其输出 Handler。在默认情况下，logger 也将 LogRecord 沿树递推发布到其父 Handler。
每个 Logger 都有一个与其关联的 ResourceBundle 名称。该指定的包用于本地化日志消息。如果一个 Logger 没有自己的 ResourceBundle 名称，则它将通过其父 Logger 沿树递归继承到 ResourceBundle 名称。
大多数 logger 输出方法都带有 "msg" 参数。此 msg 参数可以是一个原始值，也可以是一个本地化的键。在格式化期间，如果 logger 具有（或继承）一个本地化 ResourceBundle，并且 ResourceBundle 包含 msg 字符串的映射关系，那么用本地化值替换 msg 字符串。否则使用原来的 msg 字符串。通常，格式器使用 java.text.MessageFormat 形式的格式来格式化参数，例如，格式字符串 "{0} {1}" 将两个参数格式化为字符串。
将 ResourceBundle 名称映射到 ResourceBundle 时，Logger 首先试图使用该线程的 ContextClassLoader。如果 ContextClassLoader 为 null，则 Logger 将尝试 SystemClassLoader。作为初始实现中的临时过渡功能，如果 Logger 无法从 ContextClassLoader 或 SystemClassLoaderis 中找到一个 ResourceBundle，则 Logger 将会向上搜索类堆栈并连续调用 ClassLoader 来试图找到 ResourceBundle（此调用堆栈搜索是为了允许容器过渡到使用 ContextClassLoader，该功能可能在以后版本中取消）。
格式化（包括本地化）是输出 Handler 的责任，它通常会调用格式器。
注意，格式化不必同步发生。它可以延迟，直到 LogRecord 被实际写入到外部接收器。
日志记录方法划分为 5 个主要类别：
一系列的 "log" 方法，这种方法带有日志级别、消息字符串，以及可选的一些消息字符串参数。
一系列的 "logp" 方法（即 "log precise"），其与 "log" 方法相似，但是带有显式的源类名称和方法名称。
一系列的 "logrb" 方法（即 "log with resource bundle"），其与 "logp" 方法相似，但是带有显式的在本地化日志消息中使用的资源包名称。
还有跟踪方法条目（"entering" 方法）、方法返回（"exiting" 方法）和抛出异常（"throwing" 方法）的便捷方法。
最后，还有一系列在非常简单的情况下（如开发人员只想为给定的日志级别记录一条简单的字符串）使用的便捷方法。这些方法按标准级别名称命名（"severe"、"warning"、"info" 等等)，并带有单个参数，即一个消息字符串。
对于不带显式源名和方法名的方法，日志记录框架将尽可能确定日志记录方法中调用了哪个类和方法。但是应认识到，这样自动推断的信息可能只是近似的，甚至可能是完全错误的。这是因为允许虚拟机在 JIT 编译时可以进行广泛的优化，并且可以完全移除栈帧，导致它无法可靠地找到调用的类和方法。
Logger 上执行的所有方法都是多线程安全的。
子类化信息：注意，对于名称空间中的任意点，LogManager 类都可以提供自身的指定 Logger 实现。因此，Logger 的任何子类（它们与新的 LogManager 类一起实现的情况除外）要注意应该从 LogManager 类获得一个 Logger 实例，并应该将诸如 "isLoggable" 和 "log(LogRecord)" 这样的操作委托给该实例。注意，为了截取所有的日志记录输出，子类只需要重写 log(LogRecord) 方法。所有其他日志记录方法作为在此 log(LogRecord) 方法上的调用而实现。






### java.rmi

[通过一个小例子了解Java RMI](https://blog.csdn.net/DXZCZH/article/details/71403139)

[java RMI简介和例子](https://blog.csdn.net/lubiaopan/article/details/4614696)

[Java RMI初探](https://crowhawk.github.io/2017/07/17/RMI/)

java多线程编程 读书笔记
[《Java多线程核心技术》读书笔记](https://crowhawk.github.io/2017/07/06/MultiThread/)





###  java.util
Red-Black tree based {@link NavigableMap}

CountDownLatch

CyclicBarrier



```
CyclicBarrier
public CyclicBarrier(int parties)
public CyclicBarrier(int parties, Runnable barrierAction)
public int await() throws InterruptedException, BrokenBarrierException
public int await(long timeout, TimeUnit unit) throws InterruptedException, BrokenBarrierException, TimeoutException
```



CountDownLatch 是一次性的，CyclicBarrier 是可循环利用的

CountDownLatch 参与的线程的职责是不一样的，有的在倒计时，有的在等待倒计时结束。CyclicBarrier 参与的线程职责是一样的。



作者：一团捞面
链接：https://www.jianshu.com/p/333fd8faa56e
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。





### java.io

DefaultFileSystem not public class

inputstream
outputstream
reader
writer

转换流
ObjectInput extends DataInput




### java.net/sun.net

java.net.StandardProtocolFamily.INET
java.net.StandardProtocolFamily.INET6



```
Throwable (java.lang)
    Exception (java.lang)
        IOException (java.io)
            SocketException (java.net)
                ConnectionResetException (sun.net)
                ConnectException (java.net)
                PortUnreachableException (java.net)
                BindException (java.net)
                UnixSocketException (com.sun.deploy.net.socket)
                    UnixDomainSocketException (com.sun.deploy.net.socket)
                NoRouteToHostException (java.net)
```

URLConnection


### javax.xml.validation
javax.xml.validation.SchemaFactoryFinder            java 1.5
javax.xml.validation.SecuritySupport                      

`mvn clean install -e -X  -DconfigurePath=hello`

[java.security KeyFactory类详解](https://blog.csdn.net/kzcming/article/details/80097116)
密钥工厂用于将密钥(key类型的不透明密钥)转换成密钥规范(底层密钥密钥材料的透明表示),反之亦然,密钥工厂是双向的,对于同一个密钥可以存在多个兼容的密钥规范

获得对象:
一般通过静态方法getInstance()获得

方法:
generatePrivate(keySpec) ;根据给定的密钥材料生产私钥对象
generatePublic(keySpec);根据给定的密钥材料生产公钥对象
getAlgorithm();返回算法名称
getInstance();返回keyFactory对象,此方法有多个重载方法
getKeySpec();返回给定密钥的规范(密钥材料)
getProvider();返回底层算法实现的提供商
translateKey();将提供者可能未知或不受信任的密钥对象转换成此密钥工厂对应的密钥对象
支持的算法:
DiffieHellman    
DSA
RSA
EC

java.security Cipher 对象详细介绍

创建Cipher 对象:
通过Cipher.getInstance("str")  ,传入的值有两种情况:1.算法名称 2.算法/模式/填充

[Java 8 in action source code](https://github.com/edidada/Java8InAction)



Class
getName()       含有类命，还有包名
getSimpleName() 只有类命

[Java关键字transient和volatile小结](https://www.cnblogs.com/widow/p/3952827.html)



Jdk类命名规则
Collections
org.apache.logging.log4j.util.Strings

```java
    Resource resource = new ClassPathResource("");
    InputStream inputStream = resource.getInputStream();
```

[Java使用Cipher类实现加密，包括DES，DES3，AES和RSA加密](https://www.cnblogs.com/caizhaokai/p/10944667.html)


本项目有的可执行程序

- TestQueue 搞不定
- SymmetricEncoder 测试对称加密(AES)
- TestEncode 测试编码     java.util.Arrays#toString(byte[])
- SnowFlake 雪花算法 生成ID的，推特开源的
- ObjectToXmlUtil
- PropertyEditorSample
- JDBCDemo  需要调用close() java.lang.ClassNotFoundException: com.mysql.jdbc.Driver  mysql-connector-java-5.1.42.jar connection/j
- TryableSemaphoreTest 测试hystrix的信号量
- FunctionExam



```xml
<?xml version="1.0" encoding="UTF-8"?>
<java version="1.8.0_231" class="java.beans.XMLDecoder">
 <object class="cn.edidada.testjdk8.test.beans.Person">
  <void property="content">
   <string>备注的信息</string>
  </void>
  <void property="id">
   <int>1</int>
  </void>
  <void property="name">
   <string>tan</string>
  </void>
 </object>
</java>
```



```
java.beans.XMLDecoder
java.beans.XMLEncoder
```


java.beans.PropertyEditorManager#registerEditor

java.beans.Introspector#getBeanInfo(java.lang.Class<?>)



java.beans.BeanInfo
java.beans.PropertyDescriptor
java.beans.PropertyEditorManager#findEditor







[java8-Function实例](https://www.jianshu.com/p/66d1da6cc873)



- FunctionExam



闭包 Closure

闭包其实是，将代码跟代码所处于的环境做为一个整体来看待。周围的环境，表现为代码所使用的数据。在有些语言中，这个概念叫代码块（block），匿名函数(lambda)等等。



java.security.InvalidParameterException


获取Connection的两种方式

```java
DataSource ds = null;
conn ds.getConnection(username,password)
Class.forName(name);//指定连接类型
conn = DriverManager.getConnection(url, user, password);//获取连接
```

- ServiceLoaderApp    SPI 的例子 动态加载
ServiceLoader 实现了Iterator接口

[dubbo-spi](http://dubbo.apache.org/zh-cn/docs/source_code_guide/dubbo-spi.html)

- HttpTest
- TestHashMap
- DownloadImage             //java.net.URLConnection
- TestClassLoader         自定义java.lang.ClassLoader
- TestSax                            //第一个SAX读取xml文件程序 Spring也是用sax解析定义bean的xml文件的 javax.xml.parsers.SAXParser javax.xml.parsers.SAXParserFactory



公共接口BeanInfo
使用该BeanInfo接口创建一个BeanInfo类，并提供有关bean的方法，属性，事件和其他功能的显式信息。
在开发bean时，您可以实现应用程序任务所需的bean功能，而省略其余BeanInfo功能。它们将通过使用bean方法的低级反射和应用标准设计模式通过自动分析获得。您有机会通过各种描述符类提供其他bean信息。

查看SimpleBeanInfo类是一个方便的类基本BeanInfo类。您可以覆盖类的方法和属性SimpleBeanInfo以定义特定信息。

另请参阅Introspector该类以了解有关bean行为的更多信息。

[Java中的Timer源码分析及缺陷mdous](https://zhuanlan.zhihu.com/p/32712413)
Timer.TaskQueue 
Timer.TimerThread
TimerTask 抽象类 实现了Runnable接口

Timer的实现原理很简单，概括的说就是：Timer有两个内部类，TaskQueue和TimerThread，TaskQueue其实就是一个最小堆（按TimerTask下一个任务执行时间点先后排序），它存放该Timer的所有定时任务，也就是TimerTask，而TimerThread就是Timer开启的任务执行线程，在run中用一个死循环不断检查是否有任务需要开始执行了，有就执行它（注意还是在这个线程执行）。


javaee定时任务框架
quritz

## 分析String

两个String比较

## 分析ThradLocal
remove

由于ThreadLocalMap的key是弱引用，而Value是强引用。这就导致了一个问题，ThreadLocal在有外部对象强引用时，发生GC时弱引用Key会被回收，而Value不会回收，如果创建ThreadLocal的线程一直持续运行，那么这个Entry对象中的value就有可能一直得不到回收，发生内存泄露。
如何避免泄漏
既然Key是弱引用，那么我们要做的事，就是在调用ThreadLocal的get()、set()方法时完成后再调用remove方法，将Entry节点和Map的引用关系移除，这样整个Entry对象在GC Roots分析后就变成不可达了，下次GC的时候就可以被回收。
如果使用ThreadLocal的set方法之后，没有显示的调用remove方法，就有可能发生内存泄露，所以养成良好的编程习惯十分重要，使用完ThreadLocal之后，记得调用remove方法。



## 配置环境
IDEA Windows 10
junit 4.10

JDK 8 11 12

### jdk8 java.util.UUID

表示不可变通用唯一标识符（UUID）的类。UUID表示128位值。
存在这些全局标识符的不同变体。该类的方法用于操纵Leach-Salz变体，尽管构造函数允许创建任何UUID变体（如下所述）。
变体2（Leach-Salz）UUID的布局如下：最重要的长度包括以下无符号字段：

 0xFFFFFFFF00000000 time_low
 0x00000000FFFF0000 time_mid
 0x000000000000F000版本
 0x0000000000000FFF time_hi

最不重要的长整数由以下无符号字段组成：
 0xC000000000000000变种
 0x3FFF000000000000 clock_seq
 0x0000FFFFFFFFFFFF节点

variant字段包含一个标识其布局的值 UUID。上述位布局仅对UUID变量值为2的a 有效，表示Leach-Salz变量。
version字段包含一个描述其类型的值UUID。UUID有四种不同的基本类型：基于时间，DCE安全性，基于名称和随机生成的UUID。这些类型的版本值分别为1,2,3和4。
有关包括用于创建UUIDs的算法的更多信息，请参阅RFC 4122：通用唯一标识符（UUID）URN命名空间，第4.2节“用于创建基于时间的UUID的算法”。


### [策略模式 Java比较](https://blog.csdn.net/u011240877/article/details/53399019)

Comparable 自然排序 一个类继承此接口，实现compareTo方法，此类对象就可以直接比较了
Comparator 定制排序 需要 Collections.sort()等调用

### java.util.List sort方法 Java8新增


### java.util.stream



### java.util.function

### java.rmi

### java.beans

### IDEA Junit4快捷键

[IntelliJ IDEA中用快捷键自动创建测试类](https://blog.csdn.net/JavaLixy/article/details/76284524)

### ConcurrentNavigableMap接口以及实现类
ConcurrentSkipListMap (java.util.concurrent)
SubMap in ConcurrentSkipListMap (java.util.concurrent)

ConcurrentNavigableMap接口的常用方法

- subMap
- headMap
- tailMap


队列的单个元素类告诉我们，class在定义过程中就可以使用
使用类时，不是一定要先定义

### CountDownLatch
常用api
await() 
countDown()

Java并发编程：CountDownLatch、CyclicBarrier和Semaphore


### 由装饰者模式来深入理解Java I/O整体框架

[java io](https://blog.csdn.net/u013309870/article/details/75735676)


Spring默认属性编辑器
PropertyEditor是属性编辑器的接口，它规定了将外部设置值转换为内部JavaBean属性值的转换接口方法。PropertyEditor主要的接口方法说明如下：
Object getValue()：返回属性的当前值。基本类型被封装成对应的包装类实例；
void setValue(Object newValue)：设置属性的值，基本类型以包装类传入（自动装箱）；
String getAsText()：将属性对象用一个字符串表示，以便外部的属性编辑器能以可视化的方式显示。缺省返回null，表示该属性不能以字符串表示；
void setAsText(String text)：用一个字符串去更新属性的内部值，这个字符串一般从外部属性编辑器传入；
String[] getTags()：返回表示有效属性值的字符串数组（如boolean属性对应的有效Tag为true和false），以便属性编辑器能以下拉框的方式显示出来。缺省返回null，表示属性没有匹配的字符值有限集合；
String getJavaInitializationString()：为属性提供一个表示初始值的字符串，属性编辑器以此值作为属性的默认值。

BeanInfo
BeanInfo主要描述了JavaBean哪些属性可以编辑以及对应的属性编辑器，每一个属性对应一个属性描述器PropertyDescriptor。PropertyDescriptor的构造函数有两个入参：PropertyDescriptor(String propertyName, Class beanClass) ，其中propertyName为属性名；而beanClass为JavaBean对应的Class。


通过xml解析器解析出bean定义之后，解析出来的是一个一个的字符串，但是bean的属性可以各种java类型，那么在对bean进行初始化时需要在这些字符串和java类型之间进行转换，比如我的bean有个Class属性，那么在注入这个Class属性时在只能给property设置一个字符串value="a.b.C" ，框架在最终填充这个属性的时候需要把"a.b.C"转换成Class对象，这项工作是通过什么来完成的呢？它就是几天这篇博客的主角，PropertyEditor。

PropertyEditor的处理过程如下：
调用setAsText把待处理的text传递到PropertyEditor，PropertyEditor把text转换成相应类型的值并且保存到PropertyEditor
调用getValue把获取上面步骤转换后的value

[Spring PropertyEditor分析](https://blog.csdn.net/pentiumchen/article/details/44026575)

PropertyEditorRegistrySupport

[PropertyEditorRegistry](https://blog.huitu.club/2018/02/23/Spring/Beans/PropertyEditorRegistry/)

PropertyEditorRegistrySupport.createDefaultEditors()

```java
private void createDefaultEditors() {
   this.defaultEditors = new HashMap<Class<?>, PropertyEditor>(64);
 
   // Simple editors, without parameterization capabilities.
   // The JDK does not contain a default editor for any of these target types.
   this.defaultEditors.put(Charset.class, new CharsetEditor());
   this.defaultEditors.put(Class.class, new ClassEditor());
   this.defaultEditors.put(Class[].class, new ClassArrayEditor());
   this.defaultEditors.put(Currency.class, new CurrencyEditor());
   this.defaultEditors.put(File.class, new FileEditor());
   this.defaultEditors.put(InputStream.class, new InputStreamEditor());
   this.defaultEditors.put(InputSource.class, new InputSourceEditor());
   this.defaultEditors.put(Locale.class, new LocaleEditor());
   this.defaultEditors.put(Pattern.class, new PatternEditor());
   this.defaultEditors.put(Properties.class, new PropertiesEditor());
   this.defaultEditors.put(Resource[].class, new ResourceArrayPropertyEditor());
   this.defaultEditors.put(TimeZone.class, new TimeZoneEditor());
   this.defaultEditors.put(URI.class, new URIEditor());
   this.defaultEditors.put(URL.class, new URLEditor());
   this.defaultEditors.put(UUID.class, new UUIDEditor());
 
   // Default instances of collection editors.
   // Can be overridden by registering custom instances of those as custom editors.
   this.defaultEditors.put(Collection.class, new CustomCollectionEditor(Collection.class));
   this.defaultEditors.put(Set.class, new CustomCollectionEditor(Set.class));
   this.defaultEditors.put(SortedSet.class, new CustomCollectionEditor(SortedSet.class));
   this.defaultEditors.put(List.class, new CustomCollectionEditor(List.class));
   this.defaultEditors.put(SortedMap.class, new CustomMapEditor(SortedMap.class));
 
   // Default editors for primitive arrays.
   this.defaultEditors.put(byte[].class, new ByteArrayPropertyEditor());
   this.defaultEditors.put(char[].class, new CharArrayPropertyEditor());
 
   // The JDK does not contain a default editor for char!
   this.defaultEditors.put(char.class, new CharacterEditor(false));
   this.defaultEditors.put(Character.class, new CharacterEditor(true));
 
   // Spring's CustomBooleanEditor accepts more flag values than the JDK's default editor.
   this.defaultEditors.put(boolean.class, new CustomBooleanEditor(false));
   this.defaultEditors.put(Boolean.class, new CustomBooleanEditor(true));
 
   // The JDK does not contain default editors for number wrapper types!
   // Override JDK primitive number editors with our own CustomNumberEditor.
   this.defaultEditors.put(byte.class, new CustomNumberEditor(Byte.class, false));
   this.defaultEditors.put(Byte.class, new CustomNumberEditor(Byte.class, true));
   this.defaultEditors.put(short.class, new CustomNumberEditor(Short.class, false));
   this.defaultEditors.put(Short.class, new CustomNumberEditor(Short.class, true));
   this.defaultEditors.put(int.class, new CustomNumberEditor(Integer.class, false));
   this.defaultEditors.put(Integer.class, new CustomNumberEditor(Integer.class, true));
   this.defaultEditors.put(long.class, new CustomNumberEditor(Long.class, false));
   this.defaultEditors.put(Long.class, new CustomNumberEditor(Long.class, true));
   this.defaultEditors.put(float.class, new CustomNumberEditor(Float.class, false));
   this.defaultEditors.put(Float.class, new CustomNumberEditor(Float.class, true));
   this.defaultEditors.put(double.class, new CustomNumberEditor(Double.class, false));
   this.defaultEditors.put(Double.class, new CustomNumberEditor(Double.class, true));
   this.defaultEditors.put(BigDecimal.class, new CustomNumberEditor(BigDecimal.class, true));
   this.defaultEditors.put(BigInteger.class, new CustomNumberEditor(BigInteger.class, true));
 
   // Only register config value editors if explicitly requested.
   if (this.configValueEditorsActive) {
      StringArrayPropertyEditor sae = new StringArrayPropertyEditor();
      this.defaultEditors.put(String[].class, sae);
      this.defaultEditors.put(short[].class, sae);
      this.defaultEditors.put(int[].class, sae);
      this.defaultEditors.put(long[].class, sae);
   }
}
```



```
java.lang.Class#isInstance(Object obj)
判断是否是某个类的对象


### Integer类 -127 ~ 128的缓存



[mybatis generetor](https://github.com/mybatis/generator)

生成接口和Mapper xml文件
package org.mybatis.generator


### Java标准库中的jdbc和
java.sql.DriverManager 开启日志

​```java
DriverManager.setLogWriter(new PrintWriter(System.out));
```

java.sql.Driver

com.mysql.jdbc.Driver继承了com.mysql.jdbc.NonRegisteringDriver类


##### NonRegisteringDriver
有描述数据
LICENSE = "GPL"
VERSION = "5.1.42"
NAME = "MySQL Connector Java"


NonRegisteringDriver.DEBUG debug开关 final的，自己编译源码可以改

NonRegisteringDriver.ConnectionPhantomReference

PhantomReference
Reference

SoftReference
WeakReference

[java.lang.ref](https://docs.oracle.com/javase/7/docs/api/java/lang/ref/package-summary.html)
Going from strongest to weakest, the different levels of reachability reflect the life cycle of an object. They are operationally defined as follows:
- An object is strongly reachable if it can be reached by some thread without traversing any reference objects. A newly-created object is strongly reachable by the thread that created it.
An object is softly reachable if it is not strongly reachable but can be reached by traversing a soft reference.
An object is weakly reachable if it is neither strongly nor softly reachable but can be reached by traversing a weak reference. When the weak references to a weakly-reachable object are cleared, the object becomes eligible for finalization.
An object is phantom reachable if it is neither strongly, softly, nor weakly reachable, it has been finalized, and some phantom reference refers to it.
Finally, an object is unreachable, and therefore eligible for reclamation, when it is not reachable in any of the above ways.




com.mysql.DatabaseMetaData类实现java.sql.DatabaseMetaData接口

### SecurityManager

jdk class



### jdk

静态代码块在java标准库中大量使用



An enum is a kind of class and an annotation is a kind of interface

ss项目中有enum继承接口的，就是这个原因


The primitive Java types (boolean, byte, char, short, int, long, float, and double), and the keyword void are also represented as Class objects.


### Class

getName()
getClassLoader()
getSimpleName()


System.getProperty("os.arch")
System.getProperty("java.version")
System.getProperty("java.vendor")


mysql jdbc
- mxj
- loadbalance
- replication


URL url = ClassLoader.getSystemResource("log4j.properties");
Classloader抽象类调用static方法



### ConcurrentMap

V putIfAbsent(K key, V value)


### java.util.ServiceLoader

public static  ServiceLoader load(Class service) 

### java.util.logging
jul包


- RBTreeTest
测试自己实现的红黑树 RBTree

Arrays 例子

- ArraysBasicTest 测试排序char int 数组
- ArraysTest 测试排序自定义bean

### Set Array区别？

List：元素有序，可重复。
ArrayList：数组。特点：有索引（脚标），所以查找快，增删后每个元素的索引都发生改变，所以增删慢，而且数组越长增删越慢
LinkedList：链表。特点：无索引，每个元素都包含下一元素地址，查找需要逐一进行，所以查找慢，但是增删快只需要改变元素后面的地址。
Vector：线程同步数组 基本抛弃使用。
Set：元素无序，不重复，无索引。
HashSet：哈希表。特点：线程非同步，保证元素唯一性原理：判断hashCode是个屁相同，洗过相同在判断equals方法是否为true。
TreeSet：二叉树。特点：可对用两种方法对集合中元素排序，1.实现comparable接口，覆盖compareTo方法。2.集合建立时规定，并自定义比较类。

HashSet
LinkedHashSet

AbstractSet

toString()
equals()
boolean removeAll(Collection)

JDK 8 Optional

[Java注解处理器lombok](http://patamon.me/icemimosa/Java/[Lombok%E5%8E%9F%E7%90%861]%E8%87%AA%E5%AE%9A%E4%B9%89%E6%B3%A8%E8%A7%A3%E5%A4%84%E7%90%86%E5%99%A8/)


APT annotation process tool

### URI

System.arraycopy()


### TestEncode

[参考](https://blog.csdn.net/xiongchao2011/article/details/7276834)

```shell
utf-8编码：[-28, -67, -96, -27, -91, -67]
gbk编码：[-60, -29, -70, -61]
--------------------
utf-8解码：你好
gbk解码：浣犲ソ
gbk用utf-8解码：���
---------------------
用utf-8编码回去
锟斤拷锟
```


### Connection数据库事务

```java
Connection conn = DriverManager.getConnection(...);
try{
  con.setAutoCommit(false);
  Statement stmt = con.createStatement();

   //1 or more queries or updates

   con.commit();
}catch(Exception e){
   con.rollback();
}finally{
   con.close();
}


```

### java.beans.PropertyEditorSupport


### aes

- SymmetricEncoder

- javax.annotation.processing.Processor
- javax.annotation.processing.AbstractProcessor
- javax.annotation.processing.RoundEnvironment


RoundEnvironment 参数用于查询某些注解注释的元素。

```java


public class MyProcessor extends AbstractProcessor {
  @Override
  public synchronized void init(ProcessingEnvironment env) { }
  @Override
  public boolean process(Set<? extends TypeElement> annotations, RoundEnvironment env) { }
  @Override
  public Set<String> getSupportedAnnotationTypes() { }
  @Override
  public SourceVersion getSupportedSourceVersion() { }
}

```
github.com/edidada/transformer-playground



### javax.net

javax.net.DefaultSocketFactory

[一篇文章研究清楚javax.net.ssl包](https://www.10tiao.com/html/308/201603/402304724/1.html)

https://www.iteye.com/blog/willtea-1841281


```java

keytool -genkey -v -alias bluedash-ssl-demo-client -keyalg RSA -keystore ./client_ks -dname "CN=localhost,OU=cn,O=cn,L=cn,ST=cn,C=cn" -storepass client -keypass 456456
keytool -genkey -v -alias bluedash-ssl-demo-server -keyalg RSA -keystore ./server_ks -dname "CN=localhost,OU=cn,O=cn,L=cn,ST=cn,C=cn" -storepass client -keypass 456456
keytool -export -alias bluedash-ssl-demo-server -keystore ./server_ks -file server_key.cer   
keytool -import -trustcacerts -alias bluedash-ssl-demo-server -file ./server_key.cer -keystore ./client_ks 
```

```shell
"D:\Program Files\Java\jdk1.8.0_161\bin\java.exe" "-javaagent:C:\Program Files\JetBrains\IntelliJ IDEA 2018.2.4\lib\idea_rt.jar=5085:C:\Program Files\JetBrains\IntelliJ IDEA 2018.2.4\bin" -Dfile.encoding=UTF-8 -classpath "D:\Program Files\Java\jdk1.8.0_161\jre\lib\charsets.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\deploy.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\ext\access-bridge-64.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\ext\cldrdata.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\ext\dnsns.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\ext\jaccess.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\ext\jfxrt.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\ext\localedata.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\ext\nashorn.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\ext\sunec.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\ext\sunjce_provider.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\ext\sunmscapi.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\ext\sunpkcs11.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\ext\zipfs.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\javaws.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\jce.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\jfr.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\jfxswt.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\jsse.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\management-agent.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\plugin.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\resources.jar;D:\Program Files\Java\jdk1.8.0_161\jre\lib\rt.jar;D:\testjdk8\target\classes;D:\mavenrepository\201904\commons-io\commons-io\2.5\commons-io-2.5.jar;D:\mavenrepository\201904\com\google\code\gson\gson\2.8.2\gson-2.8.2.jar" org.bluedash.tryssl.SSLClient
trustStore is: d:\client_ks
trustStore type is : jks
trustStore provider is : 
init truststore
adding as trusted cert:
  Subject: CN=localhost, OU=cn, O=cn, L=cn, ST=cn, C=cn
  Issuer:  CN=localhost, OU=cn, O=cn, L=cn, ST=cn, C=cn
  Algorithm: RSA; Serial number: 0x5684f065
  Valid from Mon Nov 25 17:27:06 CST 2019 until Sun Feb 23 17:27:06 CST 2020

adding as trusted cert:
  Subject: CN=localhost, OU=cn, O=cn, L=cn, ST=cn, C=cn
  Issuer:  CN=localhost, OU=cn, O=cn, L=cn, ST=cn, C=cn
  Algorithm: RSA; Serial number: 0x55f7a31f
  Valid from Mon Nov 25 17:18:40 CST 2019 until Sun Feb 23 17:18:40 CST 2020

keyStore is : 
keyStore type is : jks
keyStore provider is : 
init keystore
init keymanager of type SunX509
trigger seeding of SecureRandom
done seeding SecureRandom
Allow unsafe renegotiation: false
Allow legacy hello messages: true
Is initial handshake: true
Is secure renegotiation: false
Ignoring unsupported cipher suite: TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384 for TLSv1
Ignoring unsupported cipher suite: TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384 for TLSv1
Ignoring unsupported cipher suite: TLS_RSA_WITH_AES_256_CBC_SHA256 for TLSv1
Ignoring unsupported cipher suite: TLS_ECDH_ECDSA_WITH_AES_256_CBC_SHA384 for TLSv1
Ignoring unsupported cipher suite: TLS_ECDH_RSA_WITH_AES_256_CBC_SHA384 for TLSv1
Ignoring unsupported cipher suite: TLS_DHE_RSA_WITH_AES_256_CBC_SHA256 for TLSv1
Ignoring unsupported cipher suite: TLS_DHE_DSS_WITH_AES_256_CBC_SHA256 for TLSv1
Ignoring unsupported cipher suite: TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384 for TLSv1.1
Ignoring unsupported cipher suite: TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384 for TLSv1.1
Ignoring unsupported cipher suite: TLS_RSA_WITH_AES_256_CBC_SHA256 for TLSv1.1
Ignoring unsupported cipher suite: TLS_ECDH_ECDSA_WITH_AES_256_CBC_SHA384 for TLSv1.1
Ignoring unsupported cipher suite: TLS_ECDH_RSA_WITH_AES_256_CBC_SHA384 for TLSv1.1
Ignoring unsupported cipher suite: TLS_DHE_RSA_WITH_AES_256_CBC_SHA256 for TLSv1.1
Ignoring unsupported cipher suite: TLS_DHE_DSS_WITH_AES_256_CBC_SHA256 for TLSv1.1
%% No cached client session
*** ClientHello, TLSv1.2
RandomCookie:  GMT: 1557831352 bytes = { 218, 232, 197, 132, 170, 100, 58, 98, 132, 58, 38, 31, 188, 6, 87, 106, 143, 228, 145, 193, 66, 28, 27, 33, 253, 243, 151, 84 }
Session ID:  {}
Cipher Suites: [TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384, TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384, TLS_RSA_WITH_AES_256_CBC_SHA256, TLS_ECDH_ECDSA_WITH_AES_256_CBC_SHA384, TLS_ECDH_RSA_WITH_AES_256_CBC_SHA384, TLS_DHE_RSA_WITH_AES_256_CBC_SHA256, TLS_DHE_DSS_WITH_AES_256_CBC_SHA256, TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA, TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA, TLS_RSA_WITH_AES_256_CBC_SHA, TLS_ECDH_ECDSA_WITH_AES_256_CBC_SHA, TLS_ECDH_RSA_WITH_AES_256_CBC_SHA, TLS_DHE_RSA_WITH_AES_256_CBC_SHA, TLS_DHE_DSS_WITH_AES_256_CBC_SHA, TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256, TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256, TLS_RSA_WITH_AES_128_CBC_SHA256, TLS_ECDH_ECDSA_WITH_AES_128_CBC_SHA256, TLS_ECDH_RSA_WITH_AES_128_CBC_SHA256, TLS_DHE_RSA_WITH_AES_128_CBC_SHA256, TLS_DHE_DSS_WITH_AES_128_CBC_SHA256, TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA, TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA, TLS_RSA_WITH_AES_128_CBC_SHA, TLS_ECDH_ECDSA_WITH_AES_128_CBC_SHA, TLS_ECDH_RSA_WITH_AES_128_CBC_SHA, TLS_DHE_RSA_WITH_AES_128_CBC_SHA, TLS_DHE_DSS_WITH_AES_128_CBC_SHA, TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384, TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256, TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384, TLS_RSA_WITH_AES_256_GCM_SHA384, TLS_ECDH_ECDSA_WITH_AES_256_GCM_SHA384, TLS_ECDH_RSA_WITH_AES_256_GCM_SHA384, TLS_DHE_RSA_WITH_AES_256_GCM_SHA384, TLS_DHE_DSS_WITH_AES_256_GCM_SHA384, TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256, TLS_RSA_WITH_AES_128_GCM_SHA256, TLS_ECDH_ECDSA_WITH_AES_128_GCM_SHA256, TLS_ECDH_RSA_WITH_AES_128_GCM_SHA256, TLS_DHE_RSA_WITH_AES_128_GCM_SHA256, TLS_DHE_DSS_WITH_AES_128_GCM_SHA256, TLS_ECDHE_ECDSA_WITH_3DES_EDE_CBC_SHA, TLS_ECDHE_RSA_WITH_3DES_EDE_CBC_SHA, SSL_RSA_WITH_3DES_EDE_CBC_SHA, TLS_ECDH_ECDSA_WITH_3DES_EDE_CBC_SHA, TLS_ECDH_RSA_WITH_3DES_EDE_CBC_SHA, SSL_DHE_RSA_WITH_3DES_EDE_CBC_SHA, SSL_DHE_DSS_WITH_3DES_EDE_CBC_SHA, TLS_EMPTY_RENEGOTIATION_INFO_SCSV]
Compression Methods:  { 0 }
Extension elliptic_curves, curve names: {secp256r1, secp384r1, secp521r1, sect283k1, sect283r1, sect409k1, sect409r1, sect571k1, sect571r1, secp256k1}
Extension ec_point_formats, formats: [uncompressed]
Extension signature_algorithms, signature_algorithms: SHA512withECDSA, SHA512withRSA, SHA384withECDSA, SHA384withRSA, SHA256withECDSA, SHA256withRSA, SHA256withDSA, SHA1withECDSA, SHA1withRSA, SHA1withDSA
Extension extended_master_secret
***
main, WRITE: TLSv1.2 Handshake, length = 207
main, READ: TLSv1.2 Handshake, length = 1277
*** ServerHello, TLSv1.2
RandomCookie:  GMT: 1557831352 bytes = { 114, 197, 105, 166, 44, 195, 144, 218, 174, 166, 53, 78, 234, 204, 7, 15, 25, 112, 10, 95, 86, 233, 67, 24, 147, 26, 24, 108 }
Session ID:  {93, 219, 159, 184, 244, 142, 101, 48, 152, 254, 107, 90, 86, 86, 187, 76, 125, 236, 229, 111, 223, 253, 99, 49, 236, 74, 185, 59, 159, 110, 142, 232}
Cipher Suite: TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384
Compression Method: 0
Extension renegotiation_info, renegotiated_connection: <empty>
Extension extended_master_secret
***
%% Initialized:  [Session-1, TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384]
** TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384
*** Certificate chain
chain [0] = [
[
  Version: V3
  Subject: CN=localhost, OU=cn, O=cn, L=cn, ST=cn, C=cn
  Signature Algorithm: SHA256withRSA, OID = 1.2.840.113549.1.1.11

  Key:  Sun RSA public key, 2048 bits
  modulus: 23532387302289715290163033691961387860933135268699609158767942673387024599890907103859580215465816865445587154888388847021608742189351719135147264803479751925244656141565421633631233240433829512884380583589235637736685705825239102989698249992441704273745167036730211108270471108557357068874334263974303515437290482886531666066542462531904352693422984398768946131739822888033197186254616380410581613701370400190895927123710379146371678320295793245803363184703614972450353598289338362307521531589113281856322764439475094336768707786900453439064695639801023298993604870357466029677526993683870355400059419516054979572579
  public exponent: 65537
  Validity: [From: Mon Nov 25 17:27:06 CST 2019,
               To: Sun Feb 23 17:27:06 CST 2020]
  Issuer: CN=localhost, OU=cn, O=cn, L=cn, ST=cn, C=cn
  SerialNumber: [    5684f065]

Certificate Extensions: 1
[1]: ObjectId: 2.5.29.14 Criticality=false
SubjectKeyIdentifier [
KeyIdentifier [
0000: 54 EC E3 31 EA 9B 2A 4C   60 C7 45 39 89 49 37 1E  T..1..*L`.E9.I7.
0010: DF F4 31 FD                                        ..1.
]
]

]
  Algorithm: [SHA256withRSA]
  Signature:
0000: 5D AD 21 A9 C8 12 12 26   EC 43 91 D8 CF 54 71 2C  ].!....&.C...Tq,
0010: E0 35 94 24 E3 D1 4B 46   E9 67 F0 88 03 EE F1 08  .5.$..KF.g......
0020: A4 3E D7 93 EA ED 09 EB   CF 1F F8 79 7E E1 65 EC  .>.........y..e.
0030: 5B 89 2E CC AA 75 B5 18   9C D7 78 97 DA B6 F7 9E  [....u....x.....
0040: CA CA 34 4D 84 60 B8 A3   22 8A 12 62 63 DD 0D 7B  ..4M.`.."..bc...
0050: 12 C8 9A 1A 3F 1F 41 C5   F0 02 BC 5D CC 6F C0 90  ....?.A....].o..
0060: 6B BD B0 9A FB B5 13 5B   20 58 DA 72 A2 4C 0E C1  k......[ X.r.L..
0070: A8 4B 23 FD 67 9A 3B 45   E4 6B 4A AE 57 69 0D 3E  .K#.g.;E.kJ.Wi.>
0080: 8C D9 1F FF 2F 54 89 27   CE 39 D9 97 B9 4C 35 63  ..../T.'.9...L5c
0090: BB 35 B8 EB 5D BB 84 C2   9E 25 01 38 40 B3 AD 94  .5..]....%.8@...
00A0: EB 03 CE D0 E7 2F 28 4E   76 D9 1E 31 F8 BC 9D E2  ...../(Nv..1....
00B0: C3 56 4F C4 E7 56 C8 77   02 BA 7A 8D C1 71 ED 80  .VO..V.w..z..q..
00C0: E6 A4 E9 2C 2C B7 C5 D4   F3 9B 7A 10 DF D2 87 F7  ...,,.....z.....
00D0: 51 63 9F 5E 76 09 A4 24   72 F8 26 A9 83 10 1B D3  Qc.^v..$r.&.....
00E0: 00 6C 41 B9 9E CD 58 65   B4 EA D3 E6 00 38 B0 27  .lA...Xe.....8.'
00F0: 54 2D 43 2F A7 81 E1 9C   D9 56 BE 0D 91 30 5C 87  T-C/.....V...0\.

]
***
Found trusted certificate:
[
[
  Version: V3
  Subject: CN=localhost, OU=cn, O=cn, L=cn, ST=cn, C=cn
  Signature Algorithm: SHA256withRSA, OID = 1.2.840.113549.1.1.11

  Key:  Sun RSA public key, 2048 bits
  modulus: 23532387302289715290163033691961387860933135268699609158767942673387024599890907103859580215465816865445587154888388847021608742189351719135147264803479751925244656141565421633631233240433829512884380583589235637736685705825239102989698249992441704273745167036730211108270471108557357068874334263974303515437290482886531666066542462531904352693422984398768946131739822888033197186254616380410581613701370400190895927123710379146371678320295793245803363184703614972450353598289338362307521531589113281856322764439475094336768707786900453439064695639801023298993604870357466029677526993683870355400059419516054979572579
  public exponent: 65537
  Validity: [From: Mon Nov 25 17:27:06 CST 2019,
               To: Sun Feb 23 17:27:06 CST 2020]
  Issuer: CN=localhost, OU=cn, O=cn, L=cn, ST=cn, C=cn
  SerialNumber: [    5684f065]

Certificate Extensions: 1
[1]: ObjectId: 2.5.29.14 Criticality=false
SubjectKeyIdentifier [
KeyIdentifier [
0000: 54 EC E3 31 EA 9B 2A 4C   60 C7 45 39 89 49 37 1E  T..1..*L`.E9.I7.
0010: DF F4 31 FD                                        ..1.
]
]

]
  Algorithm: [SHA256withRSA]
  Signature:
0000: 5D AD 21 A9 C8 12 12 26   EC 43 91 D8 CF 54 71 2C  ].!....&.C...Tq,
0010: E0 35 94 24 E3 D1 4B 46   E9 67 F0 88 03 EE F1 08  .5.$..KF.g......
0020: A4 3E D7 93 EA ED 09 EB   CF 1F F8 79 7E E1 65 EC  .>.........y..e.
0030: 5B 89 2E CC AA 75 B5 18   9C D7 78 97 DA B6 F7 9E  [....u....x.....
0040: CA CA 34 4D 84 60 B8 A3   22 8A 12 62 63 DD 0D 7B  ..4M.`.."..bc...
0050: 12 C8 9A 1A 3F 1F 41 C5   F0 02 BC 5D CC 6F C0 90  ....?.A....].o..
0060: 6B BD B0 9A FB B5 13 5B   20 58 DA 72 A2 4C 0E C1  k......[ X.r.L..
0070: A8 4B 23 FD 67 9A 3B 45   E4 6B 4A AE 57 69 0D 3E  .K#.g.;E.kJ.Wi.>
0080: 8C D9 1F FF 2F 54 89 27   CE 39 D9 97 B9 4C 35 63  ..../T.'.9...L5c
0090: BB 35 B8 EB 5D BB 84 C2   9E 25 01 38 40 B3 AD 94  .5..]....%.8@...
00A0: EB 03 CE D0 E7 2F 28 4E   76 D9 1E 31 F8 BC 9D E2  ...../(Nv..1....
00B0: C3 56 4F C4 E7 56 C8 77   02 BA 7A 8D C1 71 ED 80  .VO..V.w..z..q..
00C0: E6 A4 E9 2C 2C B7 C5 D4   F3 9B 7A 10 DF D2 87 F7  ...,,.....z.....
00D0: 51 63 9F 5E 76 09 A4 24   72 F8 26 A9 83 10 1B D3  Qc.^v..$r.&.....
00E0: 00 6C 41 B9 9E CD 58 65   B4 EA D3 E6 00 38 B0 27  .lA...Xe.....8.'
00F0: 54 2D 43 2F A7 81 E1 9C   D9 56 BE 0D 91 30 5C 87  T-C/.....V...0\.

]
*** ECDH ServerKeyExchange
Signature Algorithm SHA512withRSA
Server key: Sun EC public key, 256 bits
  public x coord: 114912780302849005079407495253257261370743636542391775166879531667809915954546
  public y coord: 33770834023855555810376965784218344029824246347651213616719280940342704574520
  parameters: secp256r1 [NIST P-256, X9.62 prime256v1] (1.2.840.10045.3.1.7)
*** ServerHelloDone
*** ECDHClientKeyExchange
ECDH Public value:  { 4, 189, 25, 93, 111, 68, 112, 127, 189, 17, 61, 179, 230, 165, 147, 177, 235, 112, 185, 151, 141, 179, 105, 207, 113, 234, 43, 146, 41, 109, 123, 151, 15, 178, 23, 46, 90, 243, 82, 20, 13, 91, 157, 69, 207, 2, 196, 47, 166, 0, 195, 79, 188, 127, 167, 108, 13, 58, 132, 87, 228, 179, 209, 153, 34 }
main, WRITE: TLSv1.2 Handshake, length = 70
SESSION KEYGEN:
PreMaster Secret:
0000: 6A 1E 53 A9 B3 D7 58 62   B8 41 DE CA C1 28 15 7B  j.S...Xb.A...(..
0010: 34 26 8D 97 A0 81 C3 E2   E1 A7 A8 E1 A5 E4 9A 16  4&..............
CONNECTION KEYGEN:
Client Nonce:
0000: 5D DB 9F B8 DA E8 C5 84   AA 64 3A 62 84 3A 26 1F  ]........d:b.:&.
0010: BC 06 57 6A 8F E4 91 C1   42 1C 1B 21 FD F3 97 54  ..Wj....B..!...T
Server Nonce:
0000: 5D DB 9F B8 72 C5 69 A6   2C C3 90 DA AE A6 35 4E  ]...r.i.,.....5N
0010: EA CC 07 0F 19 70 0A 5F   56 E9 43 18 93 1A 18 6C  .....p._V.C....l
Master Secret:
0000: 30 95 AA 6C 5F 3C 20 06   A0 AF 5F 76 2D A7 48 96  0..l_< ..._v-.H.
0010: D9 20 50 F1 2E 2C 12 66   4E BC E2 4C 11 3B 8A 81  . P..,.fN..L.;..
0020: E1 72 3A 6B 10 4E 30 AE   2D AF 55 8F F4 43 A8 B0  .r:k.N0.-.U..C..
Client MAC write Secret:
0000: 73 F1 F1 88 02 2A AC 22   52 1E E8 97 FD 7F 10 37  s....*."R......7
0010: 40 02 65 B1 93 6B 32 2A   43 A0 BC B3 F9 09 38 BC  @.e..k2*C.....8.
0020: 4C 74 C6 4C E2 35 7A 8E   D7 3A 26 32 96 3C FD 54  Lt.L.5z..:&2.<.T
Server MAC write Secret:
0000: CE 22 AF E8 6C CA F9 A1   9D B1 10 2F 7D EB E5 9A  ."..l....../....
0010: 50 4E EC 68 C0 A5 B7 98   FB 7B 6C B4 FD D0 C1 CA  PN.h......l.....
0020: DC 7A DA 80 53 D6 F6 69   35 EC 67 1C 1D 28 1D F8  .z..S..i5.g..(..
Client write key:
0000: 64 B1 F7 A5 44 CA 1B B3   11 9A 20 B5 69 AA 21 47  d...D..... .i.!G
0010: F3 A7 0D DF CC 3E F2 19   9A F0 6D AB E1 21 D2 2B  .....>....m..!.+
Server write key:
0000: 8A C8 93 68 5C EA E0 44   A5 13 A3 80 24 E9 ED F4  ...h\..D....$...
0010: EE FF D8 F4 1F 76 86 B1   48 44 7E 15 42 CB 6A 46  .....v..HD..B.jF
... no IV derived for this protocol
main, WRITE: TLSv1.2 Change Cipher Spec, length = 1
*** Finished
verify_data:  { 119, 179, 137, 114, 206, 190, 33, 200, 123, 180, 9, 95 }
***
main, WRITE: TLSv1.2 Handshake, length = 96
main, READ: TLSv1.2 Change Cipher Spec, length = 1
main, READ: TLSv1.2 Handshake, length = 96
*** Finished
verify_data:  { 70, 144, 11, 239, 251, 116, 238, 238, 26, 255, 188, 23 }
***
%% Cached client session: [Session-1, TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384]
main, WRITE: TLSv1.2 Application Data, length = 80
main, READ: TLSv1.2 Application Data, length = 80
hello
main, called close()
main, called closeInternal(true)
main, SEND TLSv1.2 ALERT:  warning, description = close_notify
main, WRITE: TLSv1.2 Alert, length = 80
main, called closeSocket(true)

Process finished with exit code 0

```


### beans

ConstructorProperties spring 实际上就是构造器注入？
[spring中@ConstructorProperties的作用](https://blog.csdn.net/wslyk606/article/details/78861999)

java.beans.EventHandler 中有用ConstructorProperties

java.beans.EventHandler 例子
https://doc.yonyoucloud.com/doc/jdk6-api-zh/java/beans/EventHandler.html

```java

EventHandler.create(ActionListener.class, myButton, "nextFocusableComponent", "source")

//Equivalent code using an inner class instead of EventHandler.
new ActionListener() {
    public void actionPerformed(ActionEvent e) {
        myButton.setNextFocusableComponent((Component)e.getSource()); 
    }
}
```

## mac complar error

程序包com.sun.image.codec.jpeg不存在

[ERROR] /Users/ibqo/development/IdeaProjects/testjdk8/src/main/java/net/jeeshop/core/util/ImageUtils.java:[22,31] 错误: 程序包com.sun.image.codec.jpeg不存在
[ERROR] /Users/ibqo/development/IdeaProjects/testjdk8/src/main/java/net/jeeshop/core/util/ImageUtils.java:[23,31] 错误: 程序包com.sun.image.codec.jpeg不存在
[ERROR] /Users/ibqo/development/IdeaProjects/testjdk8/src/main/java/net/jeeshop/core/util/ImageUtils.java:[235,9] 错误: 找不到符号


https://blog.csdn.net/plm609337931/article/details/79670686

遇到的坑：
A.<bootclasspath><extdirs>两个标签，如果配置多个数据，mac,linux用冒号(:)，而windows用分号(;)
B.<bootclasspath><extdirs>两个标签，windows路径用\，mac，linux用/

 java.lang.SecurityException: Prohibited package name: java.net
https://stackoverflow.com/questions/3804442/why-java-lang-securityexception-prohibited-package-name-java-is-required



### javax.persistence

<dependency>
    <groupId>org.eclipse.persistence</groupId>
    <artifactId>javax.persistence</artifactId>
    <version>2.1.0</version>
</dependency>

github.com/edidada/basic


### logging

Logger的默认等级是定义在执行环境的属性文件logging.properties中，这个文件位于JRE安装目录的lib目录下。部分内容如下：

### Limit the message that are printed on the console to INFO and above.

java.util.logging.ConsoleHandler.level = INFO
java.util.logging.ConsoleHandler.formatter = java.util.logging.SimpleFormatter


https://docs.oracle.com/javase/8/docs/technotes/guides/logging/overview.html

### sax

sax只能解析xml？
能不能生成xml？

### getResourceAsStream

SaxParserXMlTest.class.getClassLoader().getResourceAsStream("abc.xml")
SaxParserXMlTest.class.getResourceAsStream("abc.xml")//报错


### javax.xml.parsers
Spring中用到

https://docs.oracle.com/javase/8/docs/api/index.html?javax/xml/parsers/package-summary.html

Provides classes allowing the processing of XML documents.

DocumentBuilder
DocumentBuilderFactory

DocumentBuilder
org.w3c.dom.Document parse(InputStream is)


### 重点看

[java之DocumentBuilderFactory解析xml](https://blog.csdn.net/u011068702/article/details/80543576)

- java.lang.FunctionalInterface

[java8学习总结——函数式接口@FunctionalInterface](https://blog.csdn.net/qq_36372507/article/details/78757811)

[JDK8新特性：函数式接口@FunctionalInterface的使用说明](https://blog.csdn.net/aitangyong/article/details/54137067)

默认clone方法时浅克隆

[关于Cloneable接口和clone方法](https://www.cnblogs.com/yangfei629/p/11392034.html)

```java
public class DocumentBuilderTest{
//public class DocumentBuilderTest extends TestSuite {//Tests in error:  initializationError(cn.wdidada.xml.DocumentBuilderTest): No runnable methods
```

Dubbo用到RpcContext.getContext().getRemoteAddress()

java.net.InetSocketAddress

- TestHashMap
- TestSax


### TestHashMap

HashMap get()
当index超出范围时，会报错IndexOutOfBoundsException



map

key/value是否可以为null



### TestSax
Spring使用sax解析
spring解析xml最后获得一个Document对象，根据Document创建bean metadata。

```java

public class DocumentBuilderTest{
//public class DocumentBuilderTest extends TestSuite {//Tests in error:  initializationError(cn.wdidada.xml.DocumentBuilderTest): No runnable methods

```
```java
Dubbo用到RpcContext.getContext().getRemoteAddress()

java.net.InetSocketAddress
xx

```



AtomicReference它可以保证你在修改对象引用时的线程安全性

java.util.concurrent.atomic.AtomicReferenceFieldUpdater#newUpdater

原子更新自定义





windows IDEA  新建junit4测试类

ctrl+shift+t  --> create new test



Java ArrayList深复制 浅复制



ArrayList clone() – ArrayList deep copy and shallow copy



ByteArrayInputStream和ByteArrayOutputStream是线程安全的





关于deep copy的第三方库很多，比如Dozer（https://github.com/DozerMapper/dozer），Kryo（https://github.com/EsotericSoftware/kryo），cloning（https://github.com/kostaskougios/cloning）等，使用成熟类库可以很快且高效的实现deep copy



### java condtiction lock

Lock是java 1.5中引入的线程同步工具，它主要用于多线程下共享资源的控制。



```
// 让线程进入等通知待状态 
void await() throws InterruptedException; 
void awaitUninterruptibly();
//让线程进入等待通知状态，超时结束等待状态，并抛出异常  
long awaitNanos(long nanosTimeout) throws InterruptedException; 
boolean await(long time, TimeUnit unit) throws InterruptedException; 
boolean awaitUntil(Date deadline) throws InterruptedException; 

//将条件队列中的一个线程，从等待通知状态转换为等待锁状态 
void signal(); 

//将条件队列中的所有线程，从等待通知阻塞状态转换为等待锁阻塞状态
void signalAll();
```



![java 锁图示](imgs/condiction_lock_java.png)

https://blog.csdn.net/u010015108/article/details/56845029





例子：Condition Communication



Lock

Condition



```shell
        Lock lock = new ReentrantLock();
        Condition condition = lock.newCondition();

        lock.lock();
        condition.await();
        condition.signal();
        condition.signalAll();

        lock.unlock();
```





