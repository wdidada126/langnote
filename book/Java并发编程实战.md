# Java并发编程实战



[Java并发编程实战](https://book.douban.com/subject/10484692/)

本书作者都是Java Community Process JSR 166专家组（并发工具）的主要成员，并在其他很多JCP专家组里任职。Brian Goetz有20多年的软件咨询行业经验，并著有至少75篇关于Java开发的文章。Tim Peierls是“现代多处理器”的典范，他在BoxPop.biz、唱片艺术和戏剧表演方面也颇有研究。Joseph Bowbeer是一个Java ME专家，他对并发编程的兴趣始于Apollo计算机时代。David Holmes是《The Java Programming Language》一书的合著者，任职于Sun公司。Joshua Bloch是Google公司的首席Java架构师，《Effective Java》一书的作者，并参与著作了《Java Puzzlers》。Doug Lea是《Concurrent Programming》一书的作者，纽约州立大学 Oswego分校的计算机科学教授。




javax.annotation.concurrent.ThreadSafe



之前看不懂，现在看懂了



### 第1章　简介



### 第2章 线程安全性


非原子的64位操作
高低两个32位操作

对象的共享 可见性
举例：



### 第3章 对象的共享


final修饰变量 只能赋值一次
static修饰的变量 java内存模型里面有同步机制，确保线程安全

实现好的并发是一件困难的事情，所以很多时候我们都想躲避并发。避免并发最简单的方法就是线程封闭。

线程封闭的三种方式：Ad-hoc线程封闭、栈封闭、ThreadLocal封闭。
https://www.cnblogs.com/gnivor/p/4913132.html

20210406评注：自定义ThreadLocal
内存回收
remove方法主要是为了防止内存溢出和内存泄露，使用的时机一般是在线程运行结束之后使用，也就是「un。方法结束之后。下面介绍一下内存泄漏和内存溢的基本概念：
内存泄露(Memory Leak):是指程序中己动态分配的堆内存由于某种原因程序未释放或无法释放，造成系统内存的浪费，导致程序运行速度减慢甚至系统崩溃等严重后果。
内存溢出(Out Of Memory,简称OOM):是指应用系统中存在无法回收的内存或使用的内存过多，最终使得程序运行要用到的内存大于系统能提供的最大内存。此时程序就运行不了，系统会提示内存溢出。
https://www.cnblogs.com/east7/p/13893633.html

### 第4章 对象的组合



### 第5章 基础构建模块



同步工具类
Latch FutchTask
Semaphere
ConcurrentHashMap
size()
isEmpty()方法不一定准确
可以任意读
有限数量个写


CompleteService


ES

### 第6章 任务执行

CompleteService

### 第7章 取消与关闭
ES

Future

shutdownNow的局限性

### 第8章 线程池的使用

线程池参数
coreSize
maxSize

超时时间单位
超时时间数量

线程拒绝队列
线程工厂 ThreadFactory
拒绝策略 RejectExecutorHandler


   1、corePoolSize：核心线程数
       * 核心线程会一直存活，及时没有任务需要执行
       * 当线程数小于核心线程数时，即使有线程空闲，线程池也会优先创建新线程处理
       * 设置allowCoreThreadTimeout=true（默认false）时，核心线程会超时关闭
   2、queueCapacity：任务队列容量（阻塞队列）
       * 当核心线程数达到最大时，新任务会放在队列中排队等待执行
   3、maxPoolSize：最大线程数
       * 当线程数>=corePoolSize，且任务队列已满时。线程池会创建新线程来处理任务
       * 当线程数=maxPoolSize，且任务队列已满时，线程池会拒绝处理任务而抛出异常
   4、 keepAliveTime：线程空闲时间
       * 当线程空闲时间达到keepAliveTime时，线程会退出，直到线程数量=corePoolSize
       * 如果allowCoreThreadTimeout=true，则会直到线程数量=0
   5、allowCoreThreadTimeout：允许核心线程超时
   6、rejectedExecutionHandler：任务拒绝处理器
       * 两种情况会拒绝处理任务：
           - 当线程数已经达到maxPoolSize，切队列已满，会拒绝新任务
           - 当线程池被调用shutdown()后，会等待线程池里的任务执行完毕，再shutdown。如果在调用shutdown()和线程池真正shutdown之间提交任务，会拒绝新任务
       * 线程池会调用rejectedExecutionHandler来处理这个任务。如果没有设置默认是AbortPolicy，会抛出异常
       * ThreadPoolExecutor类有几个内部实现类来处理这类情况：
           - AbortPolicy 丢弃任务，抛运行时异常
           - CallerRunsPolicy 执行任务
           - DiscardPolicy 忽视，什么都不会发生
           - DiscardOldestPolicy 从队列中踢出最先进入队列（最后一个执行）的任务
  7、线程工厂 public interface ThreadFactory Thread newThread(Runnable r);

public ThreadPoolExecutor(int corePoolSize,
int maximumPoolSize,
long keepAliveTime,
TimeUnit unit,
BlockingQueue<Runnable> workQueue,
ThreadFactory threadFactory,
RejectedExecutionHandler handler)


### 第9章 图形用户界面应用程序



### 第10章 死锁
死锁模拟

jdk命令行工具检测
testjdk8项目Run_13

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

### 第11章

Amdahl定律


### 第12章 并发程序测试



### 第13章 显示锁



### 第14章

Condiction

ReentrantLock
Sephtere
Countdownlock
FutureTask

ReentrantReadWriteLock

### 第15章


CAS
ABA

### 第16章

Java内存模型简介
重排序
