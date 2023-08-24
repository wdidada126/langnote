# Java源码剖析34讲

Java面试真题及源码剖析34讲

https://kaiwu.lagou.com/course/courseInfo.htm?courseId=59#/content

前 360 技术专家

10 多年 Java 老兵，5 年大厂面试官经验。拥有 10 多年大型系统设计、开发和调优经验，热衷于技术分享，是阿里云社区的认证专家，腾讯社区 2019 年年度最佳作者。资深面试官与面试辅导讲师，曾辅导过 1000+ Java 工程师找到满意工作。

java知识点

第一道题

String

1、String类是final的

2 StringBuffer StrigBuilder为参数构造String对象

百度应届生考的

8种基本数据类型 占用的字节数

Rust语言设计的时候就有int32 int64

java标准库

io

nio Netty

序列化

java集合类

Collection

Map

List

Set

Araray

Set是如何保证没有重复元素的 Map的key

List如何边遍历，边删除 用迭代器

map解决hash冲突

1、链表法（chaining）

在哈希表中，每一个桶（bucket）或者槽（slot）都会对应一条链表，所有哈希值相同的元素放到相同槽位对应的链表中。

2、开放寻址法

核心思想：如果出现散列冲突，我们就**重新探测**一个空闲位置，再将元素插入。

一种比较简单的探测方法：**线性探测法**（Linear Probing）

另外的两种探测方法是**二次探测法**（Quadratic probing）和**双重散列法**（Double hashing）

juc 多线程

每个线程私有数据 tl remove

Thread ThreadStatus

ThreadGroup

AQS

UnSafe

内存

内存模型

垃圾回收算法

垃圾回收器

编译原理相关的

ClassLoader

双亲委派模型

内存泄漏工具

多线程 死锁工具

虚拟机相关的 jvm

Spring/Spring Boot/Spring Cloud

消息队列 rabbitmq kafka

分库分表

SS

数据库

事务

分布式事务

数据库 MySQL Oracle SQL Server

网络编程

io的

TCP 状态机

前沿 dpkg 

软件工程

设计模式

架构图

缓存

分布式缓存 Redis

CDN

DNS

分布式系统

分布式锁

分布式id生成器

分布式事务







结合面试题的

发现几乎所有大厂的面试套路都是一样的：他们会从一个简单的面试题问起，然后扩展到和这个知识点相关的更深层次的知识点细节，直到问的你答不上来为止，以此来探寻你的技术边际，这样就能更深入地了解你的技术能力。

### 第01讲：String 的特点是什么？它有哪些重要的方法？



String

 JDK 版本 1.8 来说，String 内部实际存储结构为 char 数组



几乎所有的 Java 面试都是以 String 开始的



印刻效应



String 是如何实现的？它有哪些重要的方法？

典型回答
以主流的 JDK 版本 1.8 来说，String 内部实际存储结构为 char 数组，源码如下：



```
public final class String
    implements java.io.Serializable, Comparable<String>, CharSequence {
    // 用于存储字符串的值
    private final char value[];
    // 缓存字符串的 hash code
    private int hash; // Default to 0
    // ......其他内容
}
```



1. 多构造方法
2. equals() 比较两个字符串是否相等
3. compareTo() 比较两个字符串
4. 其他重要方法
indexOf()：查询字符串首次出现的下标位置
lastIndexOf()：查询字符串最后出现的下标位置
contains()：查询字符串中是否包含另一个字符串
toLowerCase()：把字符串全部转换成小写
toUpperCase()：把字符串全部转换成大写
length()：查询字符串的长度
trim()：去掉字符串首尾空格
replace()：替换字符串中的某些字符
split()：把字符串分割并返回字符串数组
join()：把字符串数组转为字符串

### 第02讲：HashMap 底层实现原理是什么？JDK8 做了哪些优化？

HashMap

非线程安全的

多线程下的死循环问题 jdk7头部插入

jdk8改成了尾部插入

三个重要方法

get put resize



典型回答
在 JDK 1.7 中 HashMap 是以数组加链表的形式组成的，JDK 1.8 之后新增了红黑树的组成结构，当链表大于 8 并且容量大于 64 时，链表结构会转换成红黑树结构



第三讲

Thread

LockSupport.park() .unpark()

线程状态转换图 

ThreadStatus

共6种

线程的常用方法

join

yield

第四讲

ThreadPoolExecutor

第 1 个参数：corePoolSize 表示线程池的常驻核心线程数。

第 2 个参数：maximumPoolSize 表示线程池在任务最多时，最大可以创建的线程数。

第 3 个参数：keepAliveTime 表示线程的存活时间，当线程池空闲时并且超过了此时间，多余的线程就会销毁。

第 4 个参数：unit 表示存活时间的单位，它是配合 keepAliveTime 参数共同使用的。

第 5 个参数：workQueue 表示线程池执行的任务队列，当线程池的所有线程都在处理任务时，如果来了新任务就会缓存到此任务队列中排队等待执行。

第 6 个参数：threadFactory 表示线程的创建工厂。

第 7 个参数：RejectedExecutionHandler 表示指定线程池的拒绝策略，当线程池的任务已经在缓存队列 workQueue 中存储满了之后，并且不能创建新的线程来执行此任务时，就会用到此拒绝策略，它属于一种限流保护的机制。

与 ThreadPoolExecutor 相关的面试题还有以下几个：

ThreadPoolExecutor 的执行方法有几种？它们有什么区别？

什么是线程的拒绝策略？

拒绝策略的分类有哪些？

如何自定义拒绝策略？

ThreadPoolExecutor 能不能实现扩展？如何实现扩展？



### 第05讲：synchronized 和 ReentrantLock 的实现原理



synchronized 和 ReentrantLock 都提供了锁的功能，具备互斥性和不可见性。在 JDK 1.5 中 synchronized 的性能远远低于  ReentrantLock，但在 JDK 1.6 之后  synchronized 的性能略低于  ReentrantLock，它的区别如下：

synchronized 是 JVM 隐式实现的，而 ReentrantLock 是 Java 语言提供的 API；
ReentrantLock 可设置为公平锁，而 synchronized 却不行；
ReentrantLock 只能修饰代码块，而 synchronized 可以用于修饰方法、修饰代码块等；
ReentrantLock 需要手动加锁和释放锁，如果忘记释放锁，则会造成资源被永久占用，而 synchronized 无需手动释放锁；
ReentrantLock 可以知道是否成功获得了锁，而 synchronized  却不行。



synchronized 刚开始为偏向锁，随着锁竞争越来越激烈，会升级为轻量级锁和重量级锁。



ReentrantLock 中的 lock() 是通过 sync.lock() 实现的，但 Sync 类中的 lock() 是一个抽象方法，需要子类 NonfairSync 或 FairSync 去实现



JDK 1.5 在升级为 JDK 1.6 时，HotSpot 虚拟机团队在锁的优化上下了很大功夫，比如实现了自适应式自旋锁、锁升级等。



### 6



ABA 的常见处理方式是添加版本号，每次修改之后更新版本号，拿上面的例子来说，假如每次移动箱子之后，箱子的位置就会发生变化，而这个变化的位置就相当于“版本号”，当某人进来之后发现箱子的位置发生了变化就知道有人动了手脚，就会放弃原有的计划，这样就解决了 ABA 的问题。

JDK 在 1.5 时提供了 AtomicStampedReference 类也可以解决 ABA 的问题，此类维护了一个“版本号” Stamp，每次在比较时不止比较当前值还比较版本号，这样就解决了 ABA 的问题。

AtomicStampedReference





可重入锁
可重入锁也叫递归锁，指的是同一个线程，如果外面的函数拥有此锁之后，内层的函数也可以继续获取该锁。在 Java 语言中 ReentrantLock 和 synchronized 都是可重入锁。



共享锁和独占锁
只能被单线程持有的锁叫独占锁，可以被多线程持有的锁叫共享锁。







### 第24讲：垃圾回收算法有哪些？



垃圾回收器首先要做的就是，判断一个对象是存活状态还是死亡状态，死亡的对象将会被标识为垃圾数据并等待收集器进行清除。



判断一个对象是否为死亡状态的常用算法有两个：引用计数器算法和可达性分析算法。

引用计数算法（Reference Counting）

可达性分析算法（Reachability Analysis）



当确定了对象的状态之后（存活还是死亡）接下来就是进行垃圾回收了，垃圾回收的常见算法有以下几个：

标记-清除算法；

标记-复制算法；

标记-整理算法。

标记-清除（Mark-Sweep）







### 第23讲：说一下 JVM 的内存布局和运行原理





根据《Java虚拟机规范》的规定，JVM 的内存布局分为以下几个部分：

![java 内存布局](file:///Users/ibqo/Develop/git/github/LangNote/%E6%8B%89%E9%92%A9%E6%95%99%E8%82%B2/../imgs/lagou_edu/java_me.png?lastModify=1593526355)



类加载 类的生命周期会经历以下 7 个阶段：

加载阶段（Loading） 验证阶段（Verification） 准备阶段（Preparation） 解析阶段（Resolution） 初始化阶段（Initialization） 使用阶段（Using） 卸载阶段（Unloading） 其中验证、准备、解析 3 个阶段统称为连接（Linking），如下图所示：



![java_class_load](file:///Users/ibqo/Develop/git/github/LangNote/%E6%8B%89%E9%92%A9%E6%95%99%E8%82%B2/../imgs/lagou_edu/java_class_load.png?lastModify=1593526355)



### 第25讲：你用过哪些垃圾回收器？它们有什么区别

HotSpot 中使用的垃圾收集器主要包括 7 个：Serial、ParNew、Parallel Scavenge、Serial Old、Parallel Old、CMS 和 G1（Garbage First）收集器。





### 第26讲：生产环境如何排除和优化 JVM

jps、jstat、jinfo、jmap、jhat 和 jstack



JVM 常见调优参数包含以下这些：

-Xmx，设置最大堆内存大小； -Xms，设置初始堆内存大小； -XX:MaxNewSize，设置新生代的最大内存； -XX:MaxTenuringThreshold，设置新生代对象经过一定的次数晋升到老生代； -XX:PretrnureSizeThreshold，设置大对象的值，超过这个值的对象会直接进入老生代； -XX:NewRatio，设置分代垃圾回收器新生代和老生代内存占比； -XX:SurvivorRatio，设置新生代 Eden、Form Survivor、To Survivor 占比。



JVM 排查的 6 个基本命令行工具：jps、jstat、jinfo、jmap、jhat、jstack，以及 2 个视图排查工具：JConsole 和 JVisualVM；同时还讲了 JVM 的常见调优参数，希望本课时的内容可以切实的帮助到你。