# Java 7并发编程实战手册



[Java 7并发编程实战手册](https://book.douban.com/subject/25844475/)







### chapter1 线程管理
- java.lang.Runnable
- java.lang.Thread


java.lang.Thread.State


java.lang.Thread#setPriority

java.lang.ThreadGroup

java.lang.Thread#setName
java.lang.Runnable#run

java.util.concurrent.TimeUnit#SECONDS

java.util.concurrent.TimeUnit#sleep

join() 等待线程终止
ThreadFactory接口



Chap. 1

1.2线程的创建

线程的创建

1、 继承Thread重写run()方法

2、创建一个实现Runnable接口的类。使用带参数的Thread构造器来创建Thread对象。

1.3 线程状态的获取

线程的优先级：

Thread.MIN_PRIORITY

Thread.NORM_PRIORITY

Thread.MAX_PRIORITY

java 7并发编程实战 第一章读书笔记

id

name

Thread.Status 枚举

NEW，RUNNABLE，BLOCKED，WAITING，TIMED_WAITING，TERMINATED

1.4 线程的中断

Thread interrupt()

isInterrupted()



### chapter2 线程同步基础

synchronized java keyword
Lock
ReadWriteLock

2.8
Condiction

await（）

条件锁 Condiction接口及其子类
读写锁



```
Lock lock = new ReentrantLock();
Condition condition = lock.newCondition();
```



![类](https://img-blog.csdnimg.cn/20190804170455298.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2ExNDM5Nzc1NTIw,size_16,color_FFFFFF,t_70)



### chapter3线程同步辅助类

Semaphore 大多数语言都提供
CountDownLatch java提供
一个线程等待另一个线程执行完
CyclicBarries java提供
Phaser java提供   java.util.concurrent.Phaser 1.7

Exchanger java提供   Exchanger<V>





Semaphore用法

https://www.cnblogs.com/panshan-lurenjia/p/16124358.html
限制线程对资源的并发访问量，比如数据库连接，当访问量超过设定的大小时，线程的执行就会被阻塞或受限。

注意跟CountDownLatch比较，CountDownLatch强调等待


构造函数
Semaphore(int permits)

方法
- acquire()    获取令牌，获取不到阻塞
- tryAcquire 不阻塞获取令牌，返回成功或者失败
- release()

![Semaphore](..\imgs\javase\Semaphore.png)

什么是相位器Phaser
jdk7中增加了一个用于多阶段同步控制的工具类，它包含了CyclicBarrier和CountDownLatch的相关功能，比它们更强大灵活。
对Phaser阶段协同器的理解，Phaser适用于多个线程协作的任务，分为多个阶段，每个阶段都可以有任意个参与者，线程可以随时注册并参与某个阶段；当一个阶段中所有任务都成功完成后，Phaser的onAdvance()被调用，然后Phaser释放等待线程，自动进入下个阶段。如此循环，直到Phaser不再包含任何参与者。

https://cloud.tencent.com/developer/article/1908152




### chapter4 线程执行器

ES



ScheduledExecutorService 接口
ScheduledThreadPoolExecutor类

Executor接口
void execute(Runnable command)



![ScheduledExecutorService](..\imgs\javase\ScheduledExecutorService.png)



| 策略                                     | 解释                                           |
| ---------------------------------------- | ---------------------------------------------- |
| ThreadPoolExecutor.AbortPolicy()         | 抛出RejectedExecutionException异常。默认策略   |
| ThreadPoolExecutor.CallerRunsPolicy()    | 由向线程池提交任务的线程来执行该任务           |
| ThreadPoolExecutor.DiscardPolicy()       | 抛弃当前的任务                                 |
| ThreadPoolExecutor.DiscardOldestPolicy() | 抛弃最旧的任务（最先提交而没有得到执行的任务） |

public static class AbortPolicy implements RejectedExecutionHandler





```java
RejectedExecutionHandler接口
java.util.concurrent.RejectedExecutionHandler

    void rejectedExecution(Runnable r, ThreadPoolExecutor executor);
```



java.util.concurrent.BlockingQueue接口实现类



ArrayBlockingQueue (java.util.concurrent)
DelayedWorkQueue in ScheduledThreadPoolExecutor (java.util.concurrent)
SynchronousQueue (java.util.concurrent)
BlockingDeque (java.util.concurrent)
    LinkedBlockingDeque (java.util.concurrent)
DelayQueue (java.util.concurrent)
TransferQueue (java.util.concurrent)
    LinkedTransferQueue (java.util.concurrent)
LinkedBlockingQueue (java.util.concurrent)
PriorityBlockingQueue (java.util.concurrent)






### chapter5 Fork/Join框架



java.util.concurrent.ForkJoinTask abstract

java.util.concurrent.RecursiveTask abstract

java.util.concurrent.ForkJoinPool AbstractExecutorService子类



https://blog.csdn.net/tyrroo/article/details/81390202



fork join

mapreduce

并行计算



public ForkJoinPool(int parallelism,
                        ForkJoinWorkerThreadFactory factory,
                        UncaughtExceptionHandler handler,
                        boolean asyncMode)

- parallelism：可并行级别，Fork/Join框架将依据这个并行级别的设定，决定框架内并行执行的线程数量。并行的每一个任务都会有一个线程进行处理，但是千万不要将这个属性理解成Fork/Join框架中最多存在的线程数量，也不要将这个属性和ThreadPoolExecutor线程池中的corePoolSize、maximumPoolSize属性进行比较，因为ForkJoinPool的组织结构和工作方式与后者完全不一样。而后续的讨论中，读者还可以发现Fork/Join框架中可存在的线程数量和这个参数值的关系并不是绝对的关联（有依据但并不全由它决定）。
- factory：当Fork/Join框架创建一个新的线程时，同样会用到线程创建工厂。只不过这个线程工厂不再需要实现ThreadFactory接口，而是需要实现ForkJoinWorkerThreadFactory接口。后者是一个函数式接口，只需要实现一个名叫newThread的方法。在Fork/Join框架中有一个默认的ForkJoinWorkerThreadFactory接口实现：DefaultForkJoinWorkerThreadFactory。
- handler：异常捕获处理器。当执行的任务中出现异常，并从任务中被抛出时，就会被handler捕获。
- asyncMode：这个参数也非常重要，从字面意思来看是指的异步模式，它并不是说Fork/Join框架是采用同步模式还是采用异步模式工作。Fork/Join框架中为每一个独立工作的线程准备了对应的待执行任务队列，这个任务队列是使用数组进行组合的双向队列。即是说存在于队列中的待执行任务，即可以使用先进先出的工作模式，也可以使用后进先出的工作模式。





```
// 这是Fork/Join框架的线程池
ForkJoinPool pool = new ForkJoinPool();
ForkJoinTask<Integer> taskFuture =  pool.submit(new MyForkJoinTask(1,1001));
try {
    Integer result = taskFuture.get();
    System.out.println("result = " + result);
} 
```







### chapter6 并发集合 

原子变量

原子数组



java.util.concurrent.atomic.AtomicBoolean

java.util.concurrent.atomic.AtomicInteger

java.util.concurrent.atomic.AtomicIntegerArray

java.util.concurrent.atomic.AtomicIntegerFieldUpdater abstract

java.util.concurrent.atomic.AtomicLong

java.util.concurrent.atomic.AtomicLongArray

java.util.concurrent.atomic.AtomicLongFieldUpdater abstract

java.util.concurrent.atomic.AtomicMarkableReference<V>

java.util.concurrent.atomic.AtomicReference

java.util.concurrent.atomic.AtomicReferenceArray

java.util.concurrent.atomic.AtomicReferenceFieldUpdater<T,V>

java.util.concurrent.atomic.AtomicStampedReference<V>

java.util.concurrent.atomic.DoubleAccumulator java1.8

java.util.concurrent.atomic.DoubleAdder   java1.8

java.util.concurrent.atomic.LongAccumulator  java1.8

java.util.concurrent.atomic.LongAdder java1.8

java.util.concurrent.atomic.Striped64



17个类



### chapter7 定制并发类

定制Lock类



java.util.concurrent.locks.StampedLock       java1.8

java.util.concurrent.locks.ReentrantReadWriteLock

java.util.concurrent.locks.ReentrantLock

java.util.concurrent.locks.ReadWriteLock interface

java.util.concurrent.locks.LockSupport

java.util.concurrent.locks.Lock  interface

java.util.concurrent.locks.Condition   interface



public abstract class AbstractQueuedSynchronizer
    extends AbstractOwnableSynchronizer





public abstract class AbstractQueuedLongSynchronizer
    extends AbstractOwnableSynchronizer




### chapter8 测试并发应用程序

FindBugs

MultithreadedTC 2007最新更新的

https://code.google.com/archive/p/multithreadedtc/downloads





