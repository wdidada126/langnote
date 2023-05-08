# Java并发编程核心78讲

常见的并发工具类数不尽数：例如，线程池、各种 Lock、synchronized 关键字、ConcurrentHashMap、CopyOnWriteArrayList、ArrayBlockingQueue、ThreadLocal、原子类、CountDownLatch、Semaphore，等等，而它们的原理又包括 CAS、AQS、Java 内存模型等等。

Java并发知识体系.png





https://kaiwu.lagou.com/course/courseInfo.htm?courseId=16#/sale

拉勾教育

徐隆曦 滴滴出行高级工程师

徐隆曦，现就职于滴滴出行，硕士毕业于慕尼黑工业大学。主要负责小桔车服驾驶安全平台开发，经历了滴滴出行小桔车服的驾驶安全平台、客服治理平台等重点项目从 0 到 1 搭建全过程。在 Java 并发编程方面有丰富的实战经验，对 JUC 包的源码有深入研究。

### 06讲

一共有哪 3 种典型的线程安全问题呢？

- 1.运行结果错误；
- 2.发布和初始化导致线程安全问题；
- 3.活跃性问题。

第二种，举例说，线程start不是马上执行的，

第三种线程安全问题统称为活跃性问题，最典型的有三种，分别为死锁、活锁和饥饿。

### 08讲

那么什么情况下多线程编程会带来性能问题呢？主要有两个方面，一方面是线程调度，另一个方面是线程协作。

### 09讲

为什么要用线程池

java.util.concurrent.Executors 静态方法

阿里巴巴Java开发规范，调用java.util.concurrent.ThreadPoolExecutor#ThreadPoolExecutor(int, int, long, java.util.concurrent.TimeUnit, java.util.concurrent.BlockingQueue<java.lang.Runnable>)构造函数去创建线程池

如果每个任务都创建一个线程会带来哪些问题：

第一点，反复创建线程系统开销比较大，每个线程创建和销毁都需要时间，如果任务比较简单，那么就有可能导致创建和销毁线程消耗的资源比线程执行任务本身消耗的资源还要大。

第二点，过多的线程会占用过多的内存等资源，还会带来过多的上下文切换，同时还会导致系统不稳定。

记忆就行了，理解了

使用线程池比手动创建线程主要有三点好处。

第一点，线程池可以解决线程生命周期的系统开销问题，同时还可以加快响应速度。因为线程池中的线程是可以复用的，我们只用少量的线程去执行大量的任务，这就大大减小了线程生命周期的开销。而且线程通常不是等接到任务后再临时创建，而是已经创建好时刻准备执行任务，这样就消除了线程创建所带来的延迟，提升了响应速度，增强了用户体验。

第二点，线程池可以统筹内存和 CPU 的使用，避免资源使用不当。线程池会根据配置和任务数量灵活地控制线程数量，不够的时候就创建，太多的时候就回收，避免线程过多导致内存溢出，或线程太少导致 CPU 资源浪费，达到了一个完美的平衡。

第三点，线程池可以统一管理资源。比如线程池可以统一管理任务队列和线程，可以统一开始或结束任务，比单个线程逐一处理任务要更方便、更易于管理，同时也有利于数据统计，比如我们可以很方便地统计出已经执行过的任务的数量。

### 10讲

线程池的参数 7

3+1+3

coreSize

maxSize

keepAliveTime

时间单位

ThreadFactory

workQueue

handler





拒绝策略有以下四种：
 1）AbortPolicy 策略会直接抛出RejectedExecutionException 的 RuntimeException，程序可以采用重试或放弃。
 2） DiscardPolicy策略会直接默默丢失，不给你任何提示，不建议使用，容易莫名其妙丢任务。
 3） DiscardOldestPolicy 策略丢弃任务队列中等待事件最长的，即最老的任务，和上一个区别是上一个丢弃的是新提交的任务，这个丢弃的是最老的任务。丢弃后就可以腾出一个队列的空位存放任务。
 4） CallerRunsPolicy策略，谁提交任务谁来执行这个任务，即将任务执行放在提交的线程里面，减缓了线程的提交速度，相当于负反馈。在提交任务线程执行任务期间，线程池又可以执行完部分任务，从而腾出空间来。





java_线程池_拒绝策略.png



### 11讲

线程池拒绝策略

new ThreadPoolExecutor.DiscardOldestPolicy()

java.util.concurrent.RejectedExecutionHandler

DiscardOldestPolicy in ThreadPoolExecutor (java.util.concurrent)

AbortPolicy in ThreadPoolExecutor (java.util.concurrent)

CallerRunsPolicy in ThreadPoolExecutor (java.util.concurrent)

DiscardPolicy in ThreadPoolExecutor (java.util.concurrent)

第一种拒绝策略是 AbortPolicy，这种拒绝策略在拒绝任务时，会直接抛出一个类型为 RejectedExecutionException 的 RuntimeException，让你感知到任务被拒绝了，于是你便可以根据业务逻辑选择重试或者放弃提交等策略。

第二种拒绝策略是 DiscardPolicy，这种拒绝策略正如它的名字所描述的一样，当新任务被提交后直接被丢弃掉，也不会给你任何的通知，相对而言存在一定的风险，因为我们提交的时候根本不知道这个任务会被丢弃，可能造成数据丢失。

第三种拒绝策略是 DiscardOldestPolicy，如果线程池没被关闭且没有能力执行，则会丢弃任务队列中的头结点，通常是存活时间最长的任务，这种策略与第二种不同之处在于它丢弃的不是最新提交的，而是队列中存活时间最长的，这样就可以腾出空间给新提交的任务，但同理它也存在一定的数据丢失风险。

第四种拒绝策略是 CallerRunsPolicy，相对而言它就比较完善了，当有新任务提交后，如果线程池没被关闭且没有能力执行，则把这个任务交于提交任务的线程执行，也就是谁提交任务，谁就负责执行任务。这样做主要有两点好处。

第一点新提交的任务不会被丢弃，这样也就不会造成业务损失。

第二点好处是，由于谁提交任务谁就要负责执行任务，这样提交任务的线程就得负责执行任务，而执行任务又是比较耗时的，在这段期间，提交任务的线程被占用，也就不会再提交新的任务，减缓了任务提交的速度，相当于是一个负反馈。在此期间，线程池中的线程也可以充分利用这段时间来执行掉一部分任务，腾出一定的空间，相当于是给了线程池一定的缓冲期。

### 12讲

### 16讲

定制线程池

