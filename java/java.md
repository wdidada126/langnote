# Java标准库
java历史
jdk2
jdk5 注解
jdk6 线程优化

jsl

- java.security
- java.clipher
- javax.annotation

### annotation
@Resource Spring项目中可以用
@Resources @Resoource的组合 java annotation的组合
@PostConstructor
@ConstructorArgs

### security
java.security
https访问

java新项目访问本地文件，跨操作系统方案
instance.getClass.getResourceAsStream("");

java 指令重排序，现代理解到cpu优化这一层次了，大部分被优化的java代码都不会带来问题，是按照编码人员的意图来执行的，少部分优化违背了编码人员的意图，需要编码人员通过java编程语言相关的关键字api去修正
涉及到编译

java主要开发领域在web
以前还有手机应用

Go 云计算
C++ 数据库 游戏引擎 搜索引擎

java接口里面的方法，默认是public abstrace的？
是的，Java接口中的方法默认是public abstract的。接口是一种完全抽象的类，它只包含抽象方法的定义，没有具体的实现。因此，接口中的方法默认都是public abstract的，不能是private或protected。
当你实现一个接口时，必须实现其所有的抽象方法。如果某个实现类没有实现接口中的所有方法，那么该类必须声明为抽象类。
需要注意的是，在Java 8及以后的版本中，你也可以在接口中定义默认方法和静态方法。默认方法允许你在接口中提供方法的默认实现，可以被实现接口的类选择性重写。静态方法则允许你在接口中定义与接口本身相关的一些工具方法，可以被接口的实现类调用。

重新学java
java语法 关键字 包 类 接口 注解 标准库 三方库 ssh

Java8为函数式接口引入了一个新注解@FunctionalInterface，主要用于编译级错误检查，加上该注解，当接口不符合函数式接口定义的时候，编译器会报错。

Function接口概述
java.util.function.Function<T,R> 接口用来根据一个类型的数据得到另一个类型的数据，前者称为前置条件，后者称为后置条件。

Predicate
根据接收参数进行断言，返回boolean类型

Supplier
返回一个结果，并不要求每次调用都返回一个新的或者独一的结果

java 8
stream api熟悉

java.util.function包

isbn
9787115521484

https://pan.baidu.com/s/1ej8BPxM-6YgFFf7x0zLbLg?pwd=6666 提取码:6666 如果有任何问题，记得留言告诉我哦！非常感谢您能在我店铺购买 1

java template技术动态生成html

java spec
https://docs.oracle.com/javase/specs/
Java注解三要素
java.lang.annotation.Annotation
1.注解的定义
2.注解的使用
3.注解处理器

接口默认方法的修饰符就是public abstract，所以可以省略

Java
STW
Stop The World
垃圾回收
Cms
Parnew
垃圾回收，单线程

gc.log
https://blog.csdn.net/qq_32641659/article/details/88030753



P1
互联网P8架构师的工作内容与能力重点是什么？

P2
【多线程】什么是CAS？（基本概念）
P3
【多线程】CAS在新的JUC包里有哪些运用？
P4
【多线程】用户态与内核态
P5
【多线程】对象的内存布局（大厂必问题）
P6
【多线程】锁升级过程
P7
【多线程】锁的细节1：锁重入
P8
【多线程】锁的细节2：偏向锁启动与偏向锁未启动
P9
【多线程】锁降级过程
P10
【多线程】synchonized实现过程
P11
马士兵：不同人群进大厂的攻略都有哪些？
P12
【多线程与高并发】课程规划
P13
【多线程与高并发】线程的概念
P14
【多线程与高并发】线程的启动方式
P15
【多线程与高并发】线程的3个方法
P16
【多线程与高并发】线程的状态

P17
【多线程与高并发】锁的概念

P18
【多线程与高并发】锁的特性

P19
【多线程与高并发】设计小程序验证锁的问题

P20
【多线程与高并发】锁的可重入属性

P21
【多线程与高并发】异常跟锁

P22
【多线程与高并发】锁的底层实现

P23
【多线程与高并发】第一天课后总结

P24
【多线程与高并发】第二天课前复习

P25
【多线程与高并发】Volatile保证线程可见性

P26
【多线程与高并发】Volatile禁止指令重排序

P27
【多线程与高并发】Volatile不能保证原子性

P28
【多线程与高并发】synchronized优化

P29
【多线程与高并发】day1课程简单回顾

P30
【多线程与高并发】CAS(1)

P31
【多线程与高并发】CAS(2)

P32
【多线程与高并发】第二天课后总结

P33
【多线程与高并发】第三天课前复习

P34
【多线程与高并发】LongAdder
P35 【多线程与高并发】ReentrantLock
P36
【多线程与高并发】CountDownLatch
P37
【多线程与高并发】CyclicBarrier
P38
【多线程与高并发】Phaser

P39
【多线程与高并发】ReadWriteLock

P40
【多线程与高并发】Semaphore

P41
【多线程与高并发】Exchanger

P42
【多线程与高并发】第四天课前复习和课程规划

P43
【多线程与高并发】LockSupport

P44
【多线程与高并发】面试题一(1)_volatile
P45
【多线程与高并发】面试题一(2)_wait,notify
P46
【多线程与高并发】面试题一(3)_CountDownLatch
P47
【多线程与高并发】面试题一(4)_Semaphore,其他思路
P48
【多线程与高并发】面试题二(1)_synchronized
P49
【多线程与高并发】面试题二(2)_CAS
P50
【多线程与高并发】读源码的方法
P51
【多线程与高并发】ReentrantLock源码
P52
【多线程与高并发】AQS源码

P53
【Spring】互联网架构演变之路

P54
【Spring】什么是微服务架构？

P55
【Spring】第一个Springboot程序

P56
【Spring】课间答疑

P57
【Spring】Springboot配置文件及区别

P58
【Spring】配置文件位置的优先级

P59
【Spring】SpringBoot基础回顾

P60
【Spring】SpringBoot整合Servlet

P61
【Spring】课间答疑

P62
【Spring】SpringBoot资源配置源码分析

P63
【Spring】Springboot启动源码解析一

P64
【Spring】Springboot启动源码解析二

P65
【Spring】Springboot启动源码解析三

P66
【Spring】SpringMvc的扩展

P67
【Spring】springMVC_概念引入

P68
【Spring】SpringMVC_创建并运行war项目

P69
【Spring】SpringMVC_框架搭建1

P70
【Spring】SpringMVC_框架搭建2

P71
【Spring】SpringMVC_框架搭建3

P72
【Spring】SpringMVC_执行流程和三大组件

P73
【Spring】SpringMVC_静态资源放行

P74
【Spring】SpringMVC_控制请求方式

P75
【Spring】SpringMVC_控制请求参数和请求头

P76
【Spring】SpringMVC_@PathVariable注解

P77
【Spring】SpringMVC_RESTFUL风格

P78
【Spring】SpringMVC_参数注入引入

P79
【Spring】SpringMVC_注入POJO类型参数

P80
【Spring】SpringMVC_注入Date类型参数

P81
【Spring】SpringMVC_注入List类型参数

P82
【Spring】thymelaf模板引擎

P83
【Redis】常识介绍--磁盘、内存、IO

P84
【Redis】数据存储发展进程
18:50
P85
【Redis】数据库引擎介绍
08:31
P86
【Redis】redis简单介绍
15:07
P87
【Redis】redis安装实操
【Redis】redis安装实操总结
【Redis】epoll介绍
【Redis】redis原理
【Redis】redis及NIO原理复习
【Redis】redis使用
【Redis】redis中value类型--字符串
【Redis】redis中value类型--数值
【Redis】redis--二进制安全
P96
【Redis】redis中value类型问题解决
P97
【Redis】redis中value类型--bitmap
P98
【Redis】redis中value类型--bitmap例一
P99
【Redis】redis中value类型--bitmap例二
P100
【Redis】redis中value类型--list
P101
【Redis】redis中value类型--hash
P102
【Redis】redis中value类型--set
P103
【Redis】redis中NIO问题解决
P104
【Redis】redis中value类型--sorted_set
P105
【Redis】redis中value类型--skiplist
P106
【JVM】课程规划
P107
【JVM】JVM基础1
【JVM】JVM基础2
【JVM】Class文件格式
【JVM】Class文件解读_1
【JVM】Class文件解读_2
【JVM】Class文件解读_3
【JVM】第一天课后作业
【JVM】第二天课前复习
【JVM】类加载器
【JVM】双亲委派
【JVM】父加载器
【JVM】类加载器范围
【JVM】自定义类加载器_1
【JVM】自定义类加载器_2
【JVM】加密
【JVM】编译器
【JVM】懒加载
【JVM】第二天课后总结
【JVM】第三天课前复习
【JVM】初始化
【JVM】单例模式 双重检查
【JVM】硬件层数据一致性
【JVM】缓存行、伪共享
【JVM】乱序问题
【JVM】乱序证明
P132
【JVM】硬件级别保证有序
P133
【JVM】第三天课后总结
P134
【Linux】知识点回顾
P135
【Linux】交换网络数据格式以及广播风暴
P136
【Linux】局域网和局域网之间通信
P137
【Linux】知识概要
P138
【Linux】网络基础
P139
【Linux】传输介质双绞线
P140
【Linux】常见的网络传输协议
P141
【Linux】网卡的协商机制
P142
【Linux】交换网络
P143
【Linux】网络速度计算
P144
【Linux】OSI网络模型上
P145
【Linux】OSI网络模型下
P146
【Linux】TCPIP模型上
P147
【Linux】TCPIP模型下
P148
【Linux】网关介绍
P149
【Linux】OSI7层网络模型数据传输的过程
P150
【Linux】TCP_IP模型和协议栈介绍
P151
【Linux】IP协议介绍
P152
【Linux】TCP协议概述
P153
【Linux】TCP建立连接的过程
P154
【Linux】TCP连接状态转换2
P155
【Linux】TCP报文格式和重要字段
06:40
P156
【Linux】TCP断开连接4次挥手
08:33
P157
【Linux】TCP断开连接的7种状态
05:23
P158
【Linux】wireshark抓包分析工具
02:21
P159
【Linux】wreshark抓包分析TCP三次握手
26:43
P160
【Linux】4四挥手抓包分析
03:37
P161
【Linux】给图
03:46
P162
【Linux】TCP断开连接的四次挥手抓包介绍
11:02
P163
【Linux】TCP数据封装过程
04:57
P164
【Linux】UDP协议介绍
04:42
P165
【Linux】常见的端口介绍
15:28
P166
【Linux】IP地址分类与IP地址分类开始字段
38:31
P167
【Linux】IP地址开始字段
00:29
P168
【Linux】知识点回顾
03:43
P169
【Linux】IPv4和IPv6介绍
09:09
P170
【Linux】特殊的IP地址介绍
11:04
P171
【Linux】特殊的IP地址补充
02:18
P172
【Linux】私有IP和公有IP的介绍
10:51
P173
【Linux】子网掩码介绍
10:25
P174
【Linux】子网掩码的计算方法
12:39
P175
【Linux】10进制转二进制算法
26:53
P176
【Linux】企业案例计算两个IP是否在一个网络
21:12
P177
【Linux】IP地址子网划分
13:08
P178
【IO/NIO】操作系统宏观介绍
12:21
P179
【IO/NIO】虚拟文件系统
36:04
P180
【IO/NIO】文件描述符,nodeid,脏读
11:47
P181
【IO/NIO】socket pipeline
40:04
P182
【IO/NIO】PageCache kernel
24:21
P183
【IO/NIO】pagecache
49:09
P184
【IO/NIO】 磁盘IO
1:04:04
P185
【IO/NIO】 TCPIP
1:02:45
P186
【IO/NIO】tcpip内核数据遗失
10:32
P187
【IO/NIO】tcpip 参数
21:50
P188
【IO/NIO】网络io变化 模型
42:51
P189
【IO/NIO】C10K
22:49
P190
【IO/NIO】拓扑结构
07:58
P191
【IO/NIO】Linux速度慢的原因
27:31
P192
【IO/NIO】答疑
27:02
P193
【IO/NIO】连接数超过1024的原因
06:38
P194
【IO/NIO】压测
08:13
P195
【IO/NIO】答疑
06:37
P196
【IO/NIO】GitHub移库
03:44
P197
【IO/NIO】多路复用器引入
15:46
P198
互联网架构的演变之路
13:58

Java SE中常用的package主要包括以下几个：
java.lang：包含Java语言的核心类，如Object、String、Thread等。
java.util：包含常用的工具类，如集合类（List、Set、Map等）、日期类（Date、Calendar等）、随机数类（Random）、UUID生成器等。
java.io：包含输入输出相关的类，如文件操作类、网络操作类、序列化类等。
java.net：包含网络编程相关的类，如Socket、URL等。
java.awt和javax.swing：分别是抽象窗口工具包和Swing图形用户界面工具包，用于开发图形化界面应用程序。
java.math：用于数学计算的类，如BigDecimal、BigInteger等。
java.sql：用于数据库操作的类，如JDBC相关的类等。
java.nio：用于非阻塞式I/O操作的类，如Buffer、Channel、Selector等。
java.security：用于安全相关的类，如加密、数字签名等。
java.text：用于处理文本的类，如DateFormat、NumberFormat等。
java.time：用于处理时间的类，如LocalDate、LocalDateTime、Duration等。
java.lang.reflect：用于反射操作的类，如Class、Method、Constructor等。

以上是Java SE中常用的package及其作用，可以满足Java程序开发的大部分需求。





java.sql包是Java提供的操作关系型数据库的核心API之一，其中包含了许多接口、注解和类。以下是java.sql包中比较重要的接口、注解和类：

接口：

Connection：表示一个数据库连接。
Statement：用于执行静态 SQL 语句并返回它所生成结果的对象。
PreparedStatement：是 Statement 的子接口，它表示一个预编译的 SQL 语句的对象。
CallableStatement：是 PreparedStatement 的子接口，它用于调用存储过程或函数。
ResultSet：表示一组数据库查询结果。
ResultSetMetaData：描述 ResultSet 对象的元数据，例如 ResultSet 中包含哪些列等信息。
DatabaseMetaData：描述数据库的元数据，例如数据库名称、版本号、驱动名称、驱动版本等信息。
RowSet：是 ResultSet 的子接口，可以使用 RowSet 封装数据并进行序列化。
Savepoint：表示事务处理中的保存点，可以在该点处回滚事务。
注解：

SQLType：指定 SQL 类型。
SQLData：表示自定义 SQL 数据类型的注解。
类：

DriverManager：提供了连接到数据库的方法。
Blob：用于操作二进制数据的对象。
Clob：用于操作字符数据的对象。
SQLWarning：表示数据库访问期间发生的警告。
SQLException：表示数据库访问期间发生的异常。
Types：定义了常用 SQL 数据类型的常量。
Date：表示 SQL DATE 值。
Time：表示 SQL TIME 值。
Timestamp：表示 SQL TIMESTAMP 值。
这里列举的只是java.sql包中比较重要的一部分接口、注解和类，还有其他的一些接口、注解和类，如果需要深入学习可以查看Java官方文档。





Java中的I/O（输入/输出）分为同步和异步两种方式。同步I/O在进行数据读写时，线程需要一直等待I/O操作完成，直到读写完成才能进行其他操作。异步I/O则是在进行数据读写时，线程可以继续执行其他操作，当数据读写完成后再通知线程进行处理。Java中，同步I/O一般采用传统的I/O模型，异步I/O一般采用NIO（New I/O）模型。

BIO（Blocking I/O）模型是同步I/O的一种实现方式，它采用阻塞方式进行数据读写操作。当一个线程进行I/O操作时，如果该操作没有完成，该线程就会被阻塞，等待I/O操作完成后才能进行其他操作。BIO模型适用于单线程或者并发请求数较小的情况，但是在高并发的场景下，BIO模型的效率很低。

NIO（Non-blocking I/O）模型是异步I/O的一种实现方式，它采用事件驱动方式进行数据读写操作。当一个线程进行I/O操作时，如果该操作没有完成，该线程不会被阻塞，而是继续执行其他操作。当数据读写完成后，会通知线程进行处理。NIO模型适用于并发请求数较大的情况，但是NIO模型的编程模型比较复杂。

Java 7引入了NIO.2（Java NIO with Non-blocking I/O (NIO.2)）API，包括文件系统API、异步套接字通道、Socket编程协议升级、多播、缓冲器池等功能，提高了NIO编程的易用性和灵活性，简化了编程模型。Java 8进一步增强了NIO.2 API，包括新的File API、CompletionHandler和CompletionStage等功能，提高了异步编程的效率和易用性。





Java 8中常用的函数接口有以下几个：

Predicate<T>：接受一个输入参数，返回一个布尔值结果。
Consumer<T>：接受一个输入参数，无返回值。
Function<T, R>：接受一个输入参数，返回一个结果。
Supplier<T>：无输入参数，返回一个结果。
UnaryOperator<T>：接受一个参数为类型T，返回值为类型T。
BinaryOperator<T>：接受两个参数为类型T，返回值为类型T。
此外，Java 8还引入了一些新的类来支持Lambda表达式，包括：

Optional：一个容器，用于表示可能存在或不存在的值。
Stream：用于支持集合和数组上的函数式操作。
CompletableFuture：一个异步计算的容器，可以在计算完成后获取其结果。
这些函数接口和类为Lambda表达式的使用提供了更多的便利，同时也让Java代码更加简洁和易读。




Condition在Concurrent包中，主要用于替代以前对象Object上的wait()、notify()等方法实现线程间的协作。
相比wait()、notify()，Condition根据和Lock的结合，可以实现更复杂和精细的线程协同和等待。
Condition包含了接口和在AbstractQueuedSynchronizer类中的ConditionObject类的实现
Cpp也有原子类
Java也有


map foreach

(k,v) -> {
  
}


java 命令行程序
```shell
java -h
用法: java [-options] class [args...]
           (执行类)
   或  java [-options] -jar jarfile [args...]
           (执行 jar 文件)
其中选项包括:
    -d32          使用 32 位数据模型 (如果可用)
    -d64          使用 64 位数据模型 (如果可用)
    -client       选择 "client" VM
    -server       选择 "server" VM
                  默认 VM 是 client.

    -cp <目录和 zip/jar 文件的类搜索路径>
    -classpath <目录和 zip/jar 文件的类搜索路径>
                  用 ; 分隔的目录, JAR 档案
                  和 ZIP 档案列表, 用于搜索类文件。
    -D<名称>=<值>
                  设置系统属性
    -verbose:[class|gc|jni]
                  启用详细输出
    -version      输出产品版本并退出
    -version:<值>
                  警告: 此功能已过时, 将在
                  未来发行版中删除。
                  需要指定的版本才能运行
    -showversion  输出产品版本并继续
    -jre-restrict-search | -no-jre-restrict-search
                  警告: 此功能已过时, 将在
                  未来发行版中删除。
                  在版本搜索中包括/排除用户专用 JRE
    -? -help      输出此帮助消息
    -X            输出非标准选项的帮助
    -ea[:<packagename>...|:<classname>]
    -enableassertions[:<packagename>...|:<classname>]
                  按指定的粒度启用断言
    -da[:<packagename>...|:<classname>]
    -disableassertions[:<packagename>...|:<classname>]
                  禁用具有指定粒度的断言
    -esa | -enablesystemassertions
                  启用系统断言
    -dsa | -disablesystemassertions
                  禁用系统断言
    -agentlib:<libname>[=<选项>]
                  加载本机代理库 <libname>, 例如 -agentlib:hprof
                  另请参阅 -agentlib:jdwp=help 和 -agentlib:hprof=help
    -agentpath:<pathname>[=<选项>]
                  按完整路径名加载本机代理库
    -javaagent:<jarpath>[=<选项>]
                  加载 Java 编程语言代理, 请参阅 java.lang.instrument
    -splash:<imagepath>
                  使用指定的图像显示启动屏幕
有关详细信息, 请参阅 http://www.oracle.com/technetwork/java/javase/documentation/index.html。
```



```
jps -v
5808 TokenServerStart -Djava.awt.headless=true -Djava.net.preferIPv4Stack=true -Xmx2g -Xms2g -Dfastjson.parser.safeMode=true -XX:+DisableExplicitGC -XX:+UseConcMarkSweepGC -XX:+CMSParallelRemarkEnabled -XX:+UseCMSCompactAtFullCollection -XX:LargePageSizeInBytes=128m -XX:+UseFastAccessorMethods -XX:+UseCMSInitiatingOccupancyOnly -XX:CMSInitiatingOccupancyFraction=70


10961 StartupMain -Djava.awt.headless=true -Djava.net.preferIPv4Stack=true -Xmx2g -Xms2g -Dfastjson.parser.safeMode=true -XX:+DisableExplicitGC -XX:+UseConcMarkSweepGC -XX:+CMSParallelRemarkEnabled -XX:+UseCMSCompactAtFullCollection -XX:LargePageSizeInBytes=128m -XX:+UseFastAccessorMethods -XX:+UseCMSInitiatingOccupancyOnly -XX:CMSInitiatingOccupancyFraction=70
26131 StartupMain -Djava.awt.headless=true -Djava.net.preferIPv4Stack=true -Xmx2g -Xms2g -Dfastjson.parser.safeMode=true -XX:+DisableExplicitGC -XX:+UseConcMarkSweepGC -XX:+CMSParallelRemarkEnabled -XX:+UseCMSCompactAtFullCollection -XX:LargePageSizeInBytes=128m -XX:+UseFastAccessorMethods -XX:+UseCMSInitiatingOccupancyOnly -XX:CMSInitiatingOccupancyFraction=70
17748 StartupMain -Djava.awt.headless=true -Djava.net.preferIPv4Stack=true -Xmx2g -Xms2g -Xss256k -Dfastjson.parser.safeMode=true -XX:+DisableExplicitGC -XX:+UseConcMarkSweepGC -XX:+CMSParallelRemarkEnabled -XX:+UseCMSCompactAtFullCollection -XX:LargePageSizeInBytes=128m -XX:+UseFastAccessorMethods -XX:+UseCMSInitiatingOccupancyOnly -XX:CMSInitiatingOccupancyFraction=70
30824 QuorumPeerMain -Dzookeeper.log.dir=. -Dzookeeper.root.logger=INFO,CONSOLE -Dcom.sun.management.jmxremote -Dcom.sun.management.jmxremote.local.only=false
23065 StartupMain -Djava.awt.headless=true -Djava.net.preferIPv4Stack=true -Xmx2g -Xms2g -Dfastjson.parser.safeMode=true -XX:+DisableExplicitGC -XX:+UseConcMarkSweepGC -XX:+CMSParallelRemarkEnabled -XX:+UseCMSCompactAtFullCollection -XX:LargePageSizeInBytes=128m -XX:+UseFastAccessorMethods -XX:+UseCMSInitiatingOccupancyOnly -XX:CMSInitiatingOccupancyFraction=70
25515 ResDataStartup -Djava.awt.headless=true -Djava.net.preferIPv4Stack=true -Xmx22g -Xms22g -Dfastjson.parser.safeMode=true -XX:+DisableExplicitGC -XX:+UseConcMarkSweepGC -XX:+CMSParallelRemarkEnabled -XX:+UseCMSCompactAtFullCollection -XX:LargePageSizeInBytes=128m -XX:+UseFastAccessorMethods -XX:+UseCMSInitiatingOccupancyOnly -XX:CMSInitiatingOccupancyFraction=70
10491 OrderServerStart -Djava.awt.headless=true -Djava.net.preferIPv4Stack=true -Xmx2g -Xms2g -Xss256k -Dfastjson.parser.safeMode=true -XX:+DisableExplicitGC -XX:+UseConcMarkSweepGC -XX:+CMSParallelRemarkEnabled -XX:+UseCMSCompactAtFullCollection -XX:LargePageSizeInBytes=128m -XX:+UseFastAccessorMethods -XX:+UseCMSInitiatingOccupancyOnly -XX:CMSInitiatingOccupancyFraction=70
18284 SpsServerStart -Djava.awt.headless=true -Djava.net.preferIPv4Stack=true -Xmx2g -Xms2g -Dfastjson.parser.safeMode=true -XX:+DisableExplicitGC -XX:+UseConcMarkSweepGC -XX:+CMSParallelRemarkEnabled -XX:+UseCMSCompactAtFullCollection -XX:LargePageSizeInBytes=128m -XX:+UseFastAccessorMethods -XX:+UseCMSInitiatingOccupancyOnly -XX:CMSInitiatingOccupancyFraction=70
19005 Jps -Denv.class.path=.:/lib/dt.jar:/lib/tools.jar -Dapplication.home=/data/yyy40/lib/java/jdk1.8.0_181 -Xms8m
18479 DataStatisticsApplication -Djava.awt.headless=true -Djava.net.preferIPv4Stack=true -Xmx2g -Xms2g -Xmn256m -Xss256k -XX:+DisableExplicitGC -XX:+UseConcMarkSweepGC -XX:+CMSParallelRemarkEnabled -XX:+UseCMSCompactAtFullCollection -XX:LargePageSizeInBytes=128m -XX:+UseFastAccessorMethods -XX:+UseCMSInitiatingOccupancyOnly -XX:CMSInitiatingOccupancyFraction=70
```

观察zk car tomcat jetty idea



jvm参数有哪些，在哪儿输入的？

-Xms

-X -D输入jvm参数


getResourceAsStream返回NULL

A.class.getResourceAsStream("/config.properties")



https://blog.csdn.net/qudany10061700/article/details/86590373



common-codec

bouncycastle



Java容器类api要记住



校招Java也考Jvm参数了



Java

自定义hashmap

最好能解决多线程下循环引用、数据丢失和1.8版本下的数据覆盖问题



java可以看作c++的一门脚本？

jvm



jar包截图



imgs/java_jar.png



扰动函数 hash



https://blog.csdn.net/qq_28523617/article/details/77533097

https://www.zhihu.com/question/20733617





JDK 自带的 JAXB xml


Java Architecture for XML Binding (JAXB)
https://www.oracle.com/technical-resources/articles/javase/jaxb.html



Java14 scp 

[在JDK 14中，共有16个新特性](https://zhuanlan.zhihu.com/p/114760294?utm_source=wechat_session&utm_medium=social&utm_oi=30429583245312)

DTO





java远程调用之RMI
https://zhuanlan.zhihu.com/p/80686193

把你的设计、思路、总结都写到日记里（我用evernote），便于你自己思路的整理，很多时候人脑的缓存是真不够用，后面回来找思路的时候，细节也都在笔记里面







Java大数据、云计算、微服务、分布式系统等这些都是薪资待遇很好的岗位





虚拟化技术(CloudStack)（比openstack易用）





java.lang.Void


### java学习方向
进阶
netty高并发

java8 函数式




```java
int a =2;

if("1".equals(a)){

}
```




[Java中的Comparable和Comparator](https://blog.csdn.net/qing_gee/article/details/103884684)



## java命令行工具

java -cp xxx.jar xxx.xxx.xx.MainClass

java.util.concurrent.SynchronousQueue

需要写例子

java log 分析java xml方式

Java监控线程池


java agent


指令重排 编议原理
Java多线程的场合需要禁用

Java后端开发调试方式
日志
断点
Debug

logback
1.4.2

队列1024

换成log4j2

Java基本类型共有八种，基本类型可以分为三类，字符类型char，布尔类型boolean以及数值类型byte、short、int、long、float、double。数值类型又可以分为整数类型byte、short、int、long和浮点数类型float、double。JAVA中的数值类型不存在无符号的，它们的取值范围是固定的，不会随着机器硬件环境或者操作系统的改变而改变。实际上，JAVA中还存在另外一种基本类型void，它也有对应的包装类 java.lang.Void，不过我们无法直接对它们进行操作。8 中类型表示范围如下：
byte：8位，最大存储数据量是255，存放的数据范围是-128~127之间。
short：16位，最大数据存储量是65536，数据范围是-32768~32767之间。
int：32位，最大数据存储容量是2的32次方减1，数据范围是负的2的31次方到正的2的31次方减1。
long：64位，最大数据存储容量是2的64次方减1，数据范围为负的2的63次方到正的2的63次方减1。
float：32位，数据范围在3.4e-45~1.4e38，直接赋值时必须在数字后加上f或F。
double：64位，数据范围在4.9e-324~1.8e308，赋值时可以加d或D也可以不加。
boolean：只有true和false两个取值。
char：16位，存储Unicode码，用单引号赋值。


ngrinder



javaagent 日志收集

https://github.com/dingjs/javaagent

JavaAgent 简单例子

https://blog.csdn.net/catoop/article/details/51034739

https://docs.oracle.com/javase/7/docs/api/java/lang/instrument/package-summary.html

`javap -v XXX.class`


一定程度上考虑边界条件和性能问题



SQL规范与性能优化

1.2.1、先提前声明，博主工作用到是MySQL，可能有些场景只针对MySQL。说到SQL优化，一些概念必须要理解，不然死记硬背一两天就忘记了。特别是执行计划的概念。

1.2.2、什么是执行计划：a.决定如何访问表数据，是否通过索引，是否排序等。b.多表关联是先访问哪个表。c.多表关联时，使用哪种连接方式，不过现在MySQL只有嵌套连接（嵌套循环，顾名思义就是将一个表为出发点，将该表全部记录逐条去遍历另外一张表的记录）。

1.2.3、SQL执行顺序：a.检查语法是否正确。b.检查表是否存在、权限是否满足等。c.根据统计信息(如data length,rows,index length、索引唯一度)，生成较优的执行计划。d.根据执行计划，进行数据检索、过滤、合并、排序等操作。访问数据时，内存中如存在表数据，则直接进行操作；否则，从磁带读取表数据，放入内存，再进行操作；如内存不足，则内存中较冷数据涮出内存，再从内存中读取数据。

1.2.4、索引：查询的时候如果使用上了索引，可以提高效率，因为建立了索引后，可以理解为数据字典的结构存储，因此根据条件查询的时候更加高效。下面看一下MySQL常用的索引类型的概念。 

a．普通索引：在创建普通索引时，不附加任何限制条件。这类索引可以创建在任何数据类型中，其值是否唯一和非空由字段本身的完整性约束条件决定。建立索引以后，查询时可以通过索引进行查询。例如，在student表的stu_id字段上建立一个普通索引。查询记录时，就可以根据该索引进行查询。

b．唯一性索引:使用UNIQUE参数可以设置索引为唯一性索引。在创建唯一性索引时，限制该索引的值必须是唯一的。例如，在student表的stu_name字段中创建唯一性索引，那么stu_name字段的值就必需是唯一的。通过唯一性索引，可以更快速地确定某条记录。主键就是一种特殊唯一性索引。
c．单列索引:在表中的单个字段上创建索引。单列索引只根据该字段进行索引。单列索引可以是普通索引，也可以是唯一性索引，还可以是全文索引。只要保证该索引只对应一个字段 即可。
d．多列索引：多列索引是在表的多个字段上创建一个索引。该索引指向创建时对应的多个字段，可以通过这几个字段进行查询。但是，只有查询条件中使用了这些字段中第一个字段时，索引才会被使用。例如，在表中的id、name和sex字段上建立一个多列索引，那么，只有查询条件使用了id字段时该索引才会被使用。
e . 全文索引：使用FULLTEXT参数可以设置索引为全文索引。全文索引只能创建在CHAR、VARCHAR或TEXT类型的字段上。查询数据量较大的字符串类型的字段时，使用全文索引可以提高查询速度。例如，student表的information字段是TEXT类型，该字段包含了很多的文字信息。在information字段上建立全文索引后，可以提高查询information字段的速度。MySQL数据库从3.23.23版开始支持全文索引，但只有MyISAM存储引擎支持全文检索。在默认情况下，全文索引的搜索执行方式不区分大小写。但索引的列使用二进制排序后，可以执行区分大小写的全文索引。

还有空间索引，平时也比较少用。目前只有MyISAM存储引擎支持空间检索。目前博主也只接触过InnoDB存储引擎。
1.2.5、一般一张表索引不要超过5个，而且避免重复索引，而且也不是建了索引，根据索引字段条件查询，索引就会起作用。
1.2.6、一般哪些场景会导致索引失效：a.使用like关键字匹配字符串第一个为”%”的场景。b.条件中包含or、in、not in、<>关键字，默认不走索引的。c.访问表上的数据行超出表总记录数30%，变成全表扫描。d.查询条件使用函数在索引列上，或者对索引列进行运算。e.多列索引中，第一个索引列使用范围查询，只能用到部份或无法使用索引。f.多列索引中，第一个查询条件不是最左索引列，上面多列索引概念中也有提到。肯定还有更多的场景，但是博主现在能想到的场景就这些了。
1.2.7、不能同时使用两个索引，一个过滤数据，一个用于排序（主键除外）。
1.2.8、DML语句如果使用索引，会导致lock全表；如果使用了非唯一索引，可能只是锁住一定范围。对此，建议更新/删除数据尽量用上索引，如果可以最好用上主键或唯一索引，另外事务要及时提交。
1.2.9、最后一点，如何看执行计划，分析SQL的性能。这个吧，三言两语说不清楚，直接看其他博主的博文吧：[mysql explain执行计划详解](https://link.zhihu.com/?target=http%3A//www.cnblogs.com/xiaoboluo768/p/5400990.html)。一定要看！！！





习惯查阅 Java API Doc


- Introduction to algorithms，作者首字母缩写 CLRS ，讲算法的。
- Structure and Interpretation of Computer Programs， 简称 SICP，一本有些被神化的书，不过的确值得一读。多数人初读此书，两章后会有眼前豁然开朗的感觉。虽然这书已经不再是教材了。封面是魔术师和 lamda 。什么是经典，这就是经典。
- Computer architecture: a quantitative approach，此书我还没看，因为我自己也不是科班出身，而且此前对硬件毫无兴趣（Dijkstra 说过 computer science is no more about computers than astronomy is about telescopes），不过据说讲计算机架构的书里这本很好。
- Concrete Mathematics: A Foundation for Computer Science，高德纳出品，讲述与计算机相关的数学知识。如果数学书只想看一本，这个应该差不多够了。
- Computer Networks，作者Tanenbaum。
- 一本讲数字电路基础的书……可以省略，不过还是挺有趣的。
- TAOCP，若能看下去就看吧，看不下去也没啥，科班的都未必看得去。
- The Art of UNIX Programming，The Cathedral and the Bazaar，这两本是传道书，有些内容现在看来已经是常识了，不过仍旧值得一读。



- Code Complete (2nd Ed) by Steve McConnell，比较系统的软件工业流程认知和编程常识读本。
- The Pragmatic Programmer, 这本书讲授编程实作中的基本套路，过一遍有助于扫清盲点。
- 《人月神话》（*The Mythical Man-Month*），中文版还不错。
- 《最后期限》（*The Deadline*），中文版也还不错。
- Refactoring: Improving the Design of Existing Code，“重构”理论的集大成者。
- Design Patterns，“设计模式”的集大成者，作者四人帮，封面是埃舍尔的画。什么是经典，这就是经典。
- Programming Pearls，《编程珠玑》，茶余饭后的鉴赏小品，虽然说不定哪天就用到了。


Java设计模式
https://github.com/iluwatar/java-design-patterns

Enumeration

https://www.zhihu.com/question/276361636/answer/388370036


作者：wuxinliulei
链接：https://www.zhihu.com/question/276361636/answer/388370036
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。


1.class文件是二进制形式，是紧凑的，不想xml那样各个属性见有明显的分隔符2.每个class文件的开头都是4个字节的魔数(Magic Number),它的唯一作用是确定这个文件是否为一个能被虚拟机接受的Class文件。其实很多文件存储标准中都使用魔数来进行身份识别，
比如图片格式的gif或者jpeg文件头中都存在有魔数。使用魔数而不是扩展名来进行识别主要是基于安全方面的考虑，
因为文件扩展名是可以随意改动的。3.紧接着魔数，后面的4个字节存储的是Class文件的版本号，第5和第6个字节是次版本号(Minor Version),
第7和第8个字节是主版本号(Major Version).高版本的JDK能向下兼容以前的Class文件，但不能运行以后版本的Class文件，
即使文件格式并未发生任何变化，虚拟机也必须拒绝执行超过其版本号的Class文件。4.紧接着主次版本号的是常量池入口。常量池的常亮数目是不固定的，
所以常量池的入口放置了两个字节的数据代表常量池容量计数值.
5.其后是访问标志6.其后是类索引、父类索引、接口索引集合7.字段表集合8.方法表集合对于方法的参数为什么不能超过255个，
重点在方法表集合当中；attribute是什么？可以是int long 也可以是Class对象，就是方法的参数，而attributes_count是一个一字节的数据，
我们知道1个字节可以表示从1到255，所以方法参数不能超过255个9.属性表集合

for循环必须加大括号

HashMap是使用链表法来处理Hash冲突的；
threadlocal另一种处理Hash冲突的方法-----开放地址法

java.lang.ThreadLocal.ThreadLocalMap

java.lang.ThreadLocal.ThreadLocalMap.Entry
java.lang.ref.WeakReference


父级package不能引用子目录下的public class?

- ThreadLocalRandom

annotation的持久策略如果保存到class文件，如果用类似bytecodeviewer查看的话，怎么才能查看到

javax.annotation.PostConstruct
javax.annotation.Resource
Generated
Resources


https://blog.csdn.net/dh_chao/article/details/79001016

https://blog.csdn.net/tjcyjd/article/details/11111401


Java RESTful

https://www.gajotres.net/best-available-java-restful-micro-frameworks/
https://www.jdon.com/soa/6-restful.html
https://github.com/smallnest/Jax-RS-Performance-Comparison
https://cloud.tencent.com/developer/article/1031616






···

// 校验订单号
if (order.getOrderId() == null) {
    throw new RuntimeException("订单编号不能为空");
}
if (order.getOrderId() < 2019000000L) {
    throw new RuntimeException
        ("订单编号最小不能小于本年度初始值");
}
// 校验客户编号
if (order.getCustomerId() == null) {
    throw new RuntimeException("客户编号不能为空");
}
if (order.getCustomerId().length() < 10 ||
    order.getCustomerId().length() > 20) {
    throw new RuntimeException
        ("客户编号长度最小10位，最大20位");
}

···

那真的应该尽快了解一下Validation验证框架，它能够消除散落在各层的重复性校验逻辑。

http://www.imooc.com/article/292304

Java 字符串 多行变一行

javax.imageio.ImageIO

throws new RuntimeException("");可以
throws new Exception("");不可以

Java package不能是enum
可以是enums

jucl java自带的日志库

package name包名区分大小写

```java
NamespaceHandlerSupport (org.springframework.beans.factory.xml)
    DruidStatNamespaceHandler (com.alibaba.druid.support.spring.stat.config)
    JeeNamespaceHandler (org.springframework.ejb.config)
    AopNamespaceHandler (org.springframework.aop.config)
    LangNamespaceHandler (org.springframework.scripting.config)
    OxmNamespaceHandler (org.springframework.oxm.config)
    JdbcNamespaceHandler (org.springframework.jdbc.config)
    RepositoryNameSpaceHandler (org.springframework.data.repository.config)
    TxNamespaceHandler (org.springframework.transaction.config)
    RedisNamespaceHandler (org.springframework.data.redis.config)
    DubboNamespaceHandler (com.alibaba.dubbo.config.spring.schema)
    ContextNamespaceHandler (org.springframework.context.config)
    NamespaceHandler (org.mybatis.spring.config)
    UtilNamespaceHandler (org.springframework.beans.factory.xml)
    MvcNamespaceHandler (org.springframework.web.servlet.config)
    TaskNamespaceHandler (org.springframework.scheduling.config)
    CacheNamespaceHandler (org.springframework.cache.config)
```

`dubbo:application`

```shell
    public void init() {
        registerBeanDefinitionParser("application", new DubboBeanDefinitionParser(ApplicationConfig.class, true));
        registerBeanDefinitionParser("module", new DubboBeanDefinitionParser(ModuleConfig.class, true));
        registerBeanDefinitionParser("registry", new DubboBeanDefinitionParser(RegistryConfig.class, true));
        registerBeanDefinitionParser("monitor", new DubboBeanDefinitionParser(MonitorConfig.class, true));
        registerBeanDefinitionParser("provider", new DubboBeanDefinitionParser(ProviderConfig.class, true));
        registerBeanDefinitionParser("consumer", new DubboBeanDefinitionParser(ConsumerConfig.class, true));
        registerBeanDefinitionParser("protocol", new DubboBeanDefinitionParser(ProtocolConfig.class, true));
        registerBeanDefinitionParser("service", new DubboBeanDefinitionParser(ServiceBean.class, true));
        registerBeanDefinitionParser("reference", new DubboBeanDefinitionParser(ReferenceBean.class, false));
        registerBeanDefinitionParser("annotation", new DubboBeanDefinitionParser(AnnotationBean.class, true));
    }
```


LinkedHashMap
protected boolean removeEldestEntry(Map.Entry<K,V> eldest)

AutoCloseable

```java
AutoCloseable接口位于java.lang包下，从JDK1.7开始引入。
1.在1.7之前，我们通过try{} finally{} 在finally中释放资源。
在finally中关闭资源存在以下问题：
1、自己要手动写代码做关闭的逻辑；
2、有时候还会忘记关闭一些资源；
3、关闭代码的逻辑比较冗长，不应该是正常的业务逻辑需要关注的；
2.对于实现AutoCloseable接口的类的实例，将其放到try后面（我们称之为：带资源的try语句），在try结束的时候，会自动将这些资源关闭（调用close方法）。

```


[javap的基本用法](https://blog.csdn.net/hantiannan/article/details/7659904)

关于System.err和System.out的使用区别
https://blog.csdn.net/captainCZY/article/details/79496959

log4j2中使用InheritableThreadLocal

[InheritableThreadLocal](https://docs.oracle.com/javase/6/docs/api/java/lang/InheritableThreadLocal.html)

```java

	import java.io.FileNotFoundException;
	import java.io.PrintWriter;
	import java.io.UnsupportedEncodingException;
	try {
	  PrintWriter writer = new PrintWriter("the-file-namess.txt", "UTF-8");
	  writer.println("access HttpPostRawAccessDto"+System.currentTimeMillis());
	  writer.println("The second line");
	  writer.close();
	} catch (FileNotFoundException e) {
	  e.printStackTrace();
	} catch (UnsupportedEncodingException e) {
	  e.printStackTrace();
	} finally {
	}

```

annotation中方法不能有访问权限修饰符（public private protected default）

[idea打印gc日志的2种方法](https://blog.csdn.net/bear_lam/article/details/79648701)

gc什么时候进行？
查看使用什么cms ？

枚举类型
Enum
也需要有构造函数
枚举类列表
，
，
；


Object

.wait()
Causes the current thread to wait until another thread invokes

[java关键字transient和volatile](https://www.iteye.com/blog/dongruan00-2090116)

[Java的四种引用](https://www.cnblogs.com/huajiezh/p/5835618.html)

强引用，软引用，弱引用，虚引用


access level


show variables like '%connect%';  查看链接参数
show status like '%connect%'  查看链接状态


java.lang.Enum是所有emun的父类

[Java并发编程实战----- AQS(四)：CLH同步队列](https://www.cnblogs.com/chenssy/p/5087652.html)

ResultSet
getBoolean()
getString()
getBlob(int columnIndex)

```java
       Statement stmt = con.createStatement(
                                      ResultSet.TYPE_SCROLL_INSENSITIVE,
                                      ResultSet.CONCUR_UPDATABLE);
       ResultSet rs = stmt.executeQuery("SELECT a, b FROM TABLE2");
```

statement 声明 陈述

DataSource
```java
Connection	getConnection(String username, String password)
```

[Java中Map遍历](https://www.cnblogs.com/fqfanqi/p/6187085.html)

[java static code block](https://stackoverflow.com/questions/2420389/static-initialization-blocks)

The non-static block:

{
    // Do Something...
}
Gets called every time an instance of the class is constructed. The static block only gets called once, when the class itself is initialized, no matter how many objects of that type you create.

Example:

public class Test {

    static{
        System.out.println("Static");
    }
    
    {
        System.out.println("Non-static block");
    }
    
    public static void main(String[] args) {
        Test t = new Test();
        Test t2 = new Test();
    }
}
This prints:

Static
Non-static block

[java enum 实现接口](https://blog.csdn.net/whl825/article/details/54582715)

[Java枚举实现接口](https://blog.csdn.net/qq_21508059/article/details/78806610)

[rsa-encryption-decryption-java](https://www.devglan.com/java8/rsa-encryption-decryption-java)

java enum 实现接口

https://blog.csdn.net/whl825/article/details/54582715

https://blog.csdn.net/qq_21508059/article/details/78806610



Reactive

Vert.x

Spring

Netty



GlassFish

WebLogic

Servlet不是nio，是bio，性能不高
以前高性能领域都是c cpp
现在用Netty



java字节码的安全 魔术





java 多进程

支持

https://www.cnblogs.com/chanshuyi/p/5331094.html





Java并发ConcurrentNavigableMap接口
https://www.yiibai.com/java_concurrency/concurrency_concurrentnavigablemap.html



http://dblab.xmu.edu.cn/post/google-bigtable/





**手写HashMap核心源码**

https://juejin.im/post/5d5cf60af265da03ec2e681a

构造方法
get
put
数组+链表红黑树


http://dblab.xmu.edu.cn/post/google-bigtable/





https://docs.oracle.com/en/java/javase/14/