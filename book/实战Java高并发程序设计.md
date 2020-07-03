# 实战Java高并发程序设计

第2版
https://book.douban.com/subject/30358019/
葛一鸣



https://www.sohu.com/a/256535222_494939

实战Java虚拟机：JVM故障诊断与性能优化（第2版）



1、总览

概念

同步（Synchronous）和异步（Asynchronous）

并发（Concurrency）和并行（Parallelism）

临界区

阻塞（Blocking）和非阻塞（Non-Blocking）

死锁（Deadlock）、饥饿（Starvation）和活锁（Livelock）



并发级别

- 阻塞（Blocking）
- 无饥饿（Starvation-Free）
- 无障碍（Obstruction-Free）
- 无锁（Lock-Free）
- 无等待（Wait-Free）



并行的两个重要定律

Amdahl定律

Gustafson定律



JMM 

三个特性

原子性，可见性，有序性

哪些指令不能重排

Happen-Before

具体的规则：
(1)程序顺序规则：一个线程中的每个操作，happens-before于该线程中的任意后续操作。
(2)监视器锁规则：对一个锁的解锁，happens-before于随后对这个锁的加锁。
(3)volatile变量规则：对一个volatile域的写，happens-before于任意后续对这个volatile域的读。
(4)传递性：如果A happens-before B，且B happens-before C，那么A happens-before C。
(5)start()规则：如果线程A执行操作ThreadB.start()（启动线程B），那么A线程的ThreadB.start()操作happens-before于线程B中的任意操作。
(6)Join()规则：如果线程A执行操作ThreadB.join()并成功返回，那么线程B中的任意操作happens-before于线程A从ThreadB.join()操作成功返回。
(7)程序中断规则：对线程interrupted()方法的调用先行于被中断线程的代码检测到中断时间的发生。
(8)对象finalize规则：一个对象的初始化完成（构造函数执行结束）先行于发生它的finalize()方法的开始。






### Chap. 2 Java并行程序基础


-server jvm开启Server模式
与Server模式相关的是Client模式


JVM工作在Server模式可以大大提高性能，但应用的启动会比client模式慢大概10%。当该参数不指定时，虚拟机启动检测主机是否为服务器，如果是，则以Server模式启动，否则以client模式启动，J2SE5.0检测的根据是至少2个CPU和最低2GB内存。

　　当JVM用于启动GUI界面的交互应用时适合于使用client模式，当JVM用于运行服务器后台程序时建议用Server模式。
　　JVM在client模式默认-Xms是1M，-Xmx是64M；JVM在Server模式默认-Xms是128M，-Xmx是1024M。我们可以通过运行:java -version来查看jvm默认工作在什么模式。

https://www.cnblogs.com/wxw7blog/p/7221756.html

64位因为只支持server模式，如果我们修改了配置，启动JVM时会报错，无法启动

1. 当前是Client or Server？
使用Java -version命令就能显示出当前虚拟机处于哪种模式。 
Client： 
如下图所示，可以看到HotSpot虚拟机采用Server模式启动的。 
C:\Users\edidada>java -version
java version "1.8.0_231"
Java(TM) SE Runtime Environment (build 1.8.0_231-b11)
Java HotSpot(TM) 64-Bit Server VM (build 25.231-b11, mixed mode)





intrupt


isInturepted（）  Thread.currentThread()

intrupted（） static

线程中断跟cpu的中断

isInturepted（）  对象方法 Thread.currentThread()

intrupted（） static方法

线程中断跟cpu的中断 联系与区别？







#### Chap. 3 JDK并发包




synchronized

wait

notify/notifyAll



ReEntryLock/Condition




CountDownLatch类


构造函数设置n

countDown（）； -1

awit()等待为0



CyclicBarrier  //TODO:
构造方法
public CyclicBarrier(int parties)
public CyclicBarrier(int parties, Runnable barrierAction)

重要方法
public int await() throws InterruptedException, BrokenBarrierException
public int await(long timeout, TimeUnit unit) throws InterruptedException, BrokenBarrierException, TimeoutException

**解析：**

- 线程调用 await() 表示自己已经到达栅栏
- BrokenBarrierException 表示栅栏已经被破坏，破坏的原因可能是其中一个线程 await() 时被中断或者超时

https://www.cnblogs.com/JMLiu/p/10697476.html





LockSupport 线程阻塞工具类 直接使用UnSafe

pack()

unpack()








https://www.jianshu.com/p/333fd8faa56e

##### CyclicBarrier 与 CountDownLatch 区别

- CountDownLatch 是一次性的，CyclicBarrier 是可循环利用的
- CountDownLatch 参与的线程的职责是不一样的，有的在倒计时，有的在等待倒计时结束。CyclicBarrier 参与的线程职责是一样的。

LockSupport 线程阻塞工具类

`LockSupport`是一个线程阻塞工具类，所有的方法都是静态方法，可以让线程在任意位置阻塞，当然阻塞之后肯定得有唤醒的方法。

主要有两类方法：`park`和`unpark`。park英文意思为停车，unpark就是让车启动然后跑起来。



线程池

Executor

Executors



ThreadPoolExecutor execute submit

Future







ConcurrentSkipListMap



一、ConcurrentSkipListMap介绍

ConcurrentSkipListMap是线程安全的有序的哈希表，适用于高并发的场景。
ConcurrentSkipListMap和TreeMap，它们虽然都是有序的哈希表。但是，第一，它们的线程安全机制不同，TreeMap是非线程安全的，而ConcurrentSkipListMap是线程安全的。第二，ConcurrentSkipListMap是通过跳表实现的，而TreeMap是通过红黑树实现的。

在4线程1.6万数据的条件下，ConcurrentHashMap 存取速度是ConcurrentSkipListMap 的4倍左右。
但ConcurrentSkipListMap有几个ConcurrentHashMap 不能比拟的优点：
1、ConcurrentSkipListMap 的key是有序的。
2、ConcurrentSkipListMap 支持更高的并发。ConcurrentSkipListMap 的存取时间是log（N），和线程数几乎无关。也就是说在数据量一定的情况下，并发的线程越多，ConcurrentSkipListMap越能体现出他的优势。
在非多线程的情况下，应当尽量使用TreeMap。此外对于并发性相对较低的并行程序可以使用Collections.synchronizedSortedMap将TreeMap进行包装，也可以提供较好的效率。对于高并发程序，应当使用ConcurrentSkipListMap，能够提供更高的并发度。
所以在多线程程序中，如果需要对Map的键值进行排序时，请尽量使用ConcurrentSkipListMap，可能得到更好的并发度。
注意，调用ConcurrentSkipListMap的size时，由于多个线程可以同时对映射表进行操作，所以映射表需要遍历整个链表才能返回元素个数，这个操作是个O(log(n))的操作。





CopyonWriteArrayList

适合读多写少



BlockQueue

解耦 消费者和生产者

arrayqueue

linkqueue



#### 4 锁的优化及注意事项



AtomicInteger 

AtomicReference

AtomicIntegerArray

AtomicIntegerFieldUpdater



#### 5 并行模式与算法

Disruptor

Future模式



#### 6 Java 8/9/10与并发



Java 8中为井行计算做的新的改进， 包括并行流、 CompletableFuture、 StampedLock和J LongAdder



Future CompletableFuture

读写锁的改进：StampedLock

更快的原子类：LongAdder





#### 7 使用Akka构建高并发程序





actor



#### 8 并行程序调试



#### 9 Jetty核心代码分析




