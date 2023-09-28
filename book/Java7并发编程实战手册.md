# Java7并发编程实战手册

作者: [西]Javier Fernández González
出版社: 人民邮电出版社
出品方: 异步图书
原作名: Java 7 Concurrency Cookbook
译者: 申绍勇/俞黎敏
出版年: 2014-2
页数: 339
定价: 59.00元
装帧: 平装
ISBN: 9787115335296

新版本 Java9并发编程实战手册
https://book.douban.com/subject/34790228/

[Java7并发编程实战手册](https://book.douban.com/subject/25844475/)
Java7并发编程实战手册.pdf
随书源码
D:\git\github\testjdk8\docs\7881_code

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

1.2线程的创建

线程的创建
1、 继承Thread重写run()方法
2、创建一个实现Runnable接口的类。使用带参数的Thread构造器来创建Thread对象。

1.3 线程状态的获取

线程的优先级：
Thread.MIN_PRIORITY
Thread.NORM_PRIORITY
Thread.MAX_PRIORITY

### 

id

name

Thread.Status 枚举

NEW，RUNNABLE，BLOCKED，WAITING，TIMED_WAITING，TERMINATED

1.4 线程的中断

Thread interrupt()

isInterrupted()


```java
ExecutorService executorService = Executors.newSingleThreadExecutor();
Future<Integer> future = executorService.submit();
```

### chapter2 线程同步基础

synchronized ,java keyword
Lock
ReadWriteLock

2.8
Condiction 拼写错误

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
CyclicBarrier java提供
Phaser java提供   java.util.concurrent.Phaser 1.7

Exchanger java提供   Exchanger<V>



#### CyclicBarrier和CountDownLatch

#### Exchanger<V>

#### Semaphore用法

- availablePermits()
- tryAcquire()

https://www.cnblogs.com/panshan-lurenjia/p/16124358.html
限制线程对资源的并发访问量，比如数据库连接，当访问量超过设定的大小时，线程的执行就会被阻塞或受限。

注意跟CountDownLatch比较，CountDownLatch强调等待
Semaphore和CountDownLatch都是Java多线程编程中的同步工具，用于控制线程的执行顺序和对共享资源的访问控制。它们有一些相似之处，但也有一些区别。
相似之处：
它们都是用于控制线程的同步工具，可以用来确保线程在执行特定任务之前的等待时间，以及限制对共享资源的访问。
不同之处：
Semaphore用于限制同时访问共享资源的线程数量，它有一个许可证数量，每个线程在访问资源之前需要获取一个许可证，访问结束后释放该许可证。Semaphore可以重复使用，即许可证数量可以被释放和重新获取。
CountDownLatch则用于等待其他线程完成某个操作。在CountDownLatch初始化时，设置一个计数器，每个线程完成任务后将计数器减1，当计数器变为0时，等待的线程将被唤醒。它的使用方式是“一个线程（多个线程）等待”，即一个或多个线程等待其他多个线程完成某件事情之后才能执行。
综上所述，Semaphore和CountDownLatch虽然都是用于线程同步的工具，但它们的使用场景不同。Semaphore主要用于限制对共享资源的并发访问，而CountDownLatch则主要用于等待其他线程完成某个操作。

构造函数
Semaphore(int permits)

方法
- acquire()    获取令牌，获取不到阻塞
- tryAcquire 不阻塞获取令牌，返回成功或者失败
- release()

![Semaphore](..\imgs\javase\Semaphore.png)

CyclicBarrier是Java中的一个类，它用于实现固定大小的线程等待，直到所有线程都达到某个屏障点后，才会继续执行。
以下是CyclicBarrier类的API：
CyclicBarrier(int parties)：构造函数，指定屏障处的线程数parties。
CyclicBarrier(int parties, Runnable barrierAction)：构造函数，指定屏障处的线程数parties，barrierAction是屏障跳闸时执行的动作，由最后一个进入屏障的线程启动。
int await()：方法，parties个线程执行await()方法后，程序继续向下执行。
int await(long timeout, TimeUnit unit)：方法，如果在指定的时间内达到 parties 的数量，则程序继向下运行，否则如果出现超时，则抛出TimeoutException异常。
int getNumberWaiting()：方法获取有几个线程到达了屏障点。
reset()：方法，重置屏障。
这些方法的使用场景可以在包含固定大小的线程的程序中非常有用，这些线程有时必须彼此等待。如果所有线程都到达栅栏位置，那么栅栏将打开，此时所有的线程都将被释放，而栅栏将被重置以便下次使用。

#### 什么是相位器Phaser
jdk7中增加了一个用于多阶段同步控制的工具类，它包含了CyclicBarrier和CountDownLatch的相关功能，比它们更强大灵活。
对Phaser阶段协同器的理解，Phaser适用于多个线程协作的任务，分为多个阶段，每个阶段都可以有任意个参与者，线程可以随时注册并参与某个阶段；当一个阶段中所有任务都成功完成后，Phaser的onAdvance()被调用，然后Phaser释放等待线程，自动进入下个阶段。如此循环，直到Phaser不再包含任何参与者。

https://cloud.tencent.com/developer/article/1908152

#### Phaser API说明

-   构造方法
    -   `Phaser()` ：参与任务数0
    -   `Phaser(int parties)`：指定初始参与任务数
    -   `Phaser(Phaser parent)`：指定parent阶段器， 子对象作为一个整体加入parent对象，当子对象中没有参与者时，会自动从parent对象解除注册
    -   `Phaser(Phaser parent , int parties)`：集成上面两个方法的
-   增减参与任务数方法
    -   `int register()`：增加一个数，返回当前阶段号
    -   `int bulkRegister(int parties)`：增加指定个数，返回当前阶段号
    -   `int arriveAndDeregister()`：减少一个任务数，返回当前阶段号
-   到达等待方法
    -   `int arrive()`：到达，任务完成，返回当前阶段号
    -   `int arriveAndAwaitAdvance()`：到达后等待其他任务到达，返回到达阶段号
    -   `int awaitAdvance(int phase)`：在指定阶段等待(必须是当前阶段才有效)
    -   `int awaitAdvanceInterruptibly(int phase)`
    -   `int awaitAdvanceInterruptibly(int phase ， long timeout, TimeUnit unit)`
-   阶段到达触发动作
    -   `protected boolean onAdvance(int Phase , int registeredParties)`：类似于CyclicBarrier的触发命令，通过重写该方法来增加阶段到达动作
-   其它api
    -   `void forceTermination()`：强制结束
    -   `boolean isTerMinated()`：判断是否结束
    -   `void getPhase()`：获取当前阶段号


#### Phaser例子

场景：公司组织郊游活动，大家各自从家出发到公司集合，大家都到了后，出发到公园各自游玩，然后在公园门口集合，再去餐厅就餐，大家都到了就开始用餐。有的员工白天有事，选择晚上的聚餐，有的员工则晚上有事，只参加白天的活动。编程模拟实现。

-   第一阶段，到公司集合5人，任务数为5，去公园游玩。
-   第二阶段，到公园门口集合，有2人因为晚上有事，自行从公园回家；则3人去餐厅，这是减少参与数，任务数变为3
-   第三阶段，餐厅集合，有另外4人参加聚餐，这是增加参与数，任务数变为7


### chapter4 线程执行器

ES

ScheduledExecutorService 接口
ScheduledThreadPoolExecutor类

Executor接口
void execute(Runnable command)

![ScheduledExecutorService](..\imgs\javase\ScheduledExecutorService.png)

拒绝策略
acdd 四个

| 策略                                     | 解释                                           |
| ---------------------------------------- | ---------------------------------------------- |
| ThreadPoolExecutor.AbortPolicy()         | 抛出RejectedExecutionException异常。默认策略   |
| ThreadPoolExecutor.CallerRunsPolicy()    | 由向线程池提交任务的线程来执行该任务           |
| ThreadPoolExecutor.DiscardPolicy()       | 抛弃当前的任务                                 |
| ThreadPoolExecutor.DiscardOldestPolicy() | 抛弃最旧的任务（最先提交而没有得到执行的任务） |

public static class AbortPolicy implements RejectedExecutionHandler

RejectedExecutionHandler接口

```java
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

```java
        ForkJoinPool forkJoinPool = ForkJoinPool.commonPool();
```

ForkJoinPool.invoke()

#### fjp ForkJoinPool
#### RecursiveTask  rt

#### ForkJoinTask fjt

#### RecursiveAction ra

java.util.concurrent.ForkJoinTask abstract

java.util.concurrent.RecursiveTask abstract

java.util.concurrent.ForkJoinPool AbstractExecutorService子类

`ForkJoinTask`提供了两种任务类型：`RecursiveAction`和`RecursiveTask`。其中，`RecursiveAction`用于没有返回值的任务，`RecursiveTask`用于有返回值的任务。这两种任务类型都继承自`ForkJoinTask`。
`ForkJoinTask`框架的核心思想是“工作窃取”（Work Stealing）。具体来说，当一个线程完成了自己的任务后，如果它还有空闲时间，就会去“窃取”其他线程队列中的任务来执行，从而使得任务的执行更加高效。

https://blog.csdn.net/tyrroo/article/details/81390202

fork join

mapreduce

并行计算

ForkJoinPool构造函数 四个函数

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

cas compare and swap是算法，对应cpu指令 go rust c++都有

java.util.concurrent.atomic.AtomicBoolean

java.util.concurrent.atomic.AtomicInteger
java.util.concurrent.atomic.AtomicLong

java.util.concurrent.atomic.AtomicIntegerArray

java.util.concurrent.atomic.AtomicIntegerFieldUpdater abstract

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

shard
excusive

aqls AbstractQueuedLongSynchronizer

public abstract class AbstractQueuedLongSynchronizer
    extends AbstractOwnableSynchronizer


### chapter8 测试并发应用程序

FindBugs

MultithreadedTC 2007最新更新的
https://code.google.com/archive/p/multithreadedtc/downloads

FindBugs是一个静态分析工具，用于检测Java代码中的潜在错误和问题。它可以帮助测试并发应用程序，并发现可能导致错误或性能问题的潜在问题。
以下是一个使用FindBugs测试并发应用程序的例子：
假设你有一个简单的并发应用程序，其中包含一个线程类和一个主类。线程类负责执行一些任务，主类负责启动线程并等待任务完成。代码如下：

```java
public class MyThread extends Thread {  
    public void run() {  
        // 执行任务的代码  
    }  
}  
  
public class Main {  
    public static void main(String[] args) {  
        MyThread thread = new MyThread();  
        thread.start();  
        // 等待线程完成任务的代码  
    }  
}
```
你可以使用FindBugs来分析这个应用程序的代码。首先，将代码编译成.class文件或.jar文件。然后，运行FindBugs并指定要分析的代码路径：
```bash
findbugs -textui -low -longBugCodes -exclude . -output /path/to/output /path/to/compiled/code
```
这将生成一个包含潜在问题的报告。在这个例子中，FindBugs可能会报告以下问题：
在MyThread类的run方法中，没有同步任何代码块，这可能导致线程安全问题。
在Main类的main方法中，启动线程后没有正确等待线程完成任务，这可能导致死锁问题。
你可以根据FindBugs的报告修复这些问题，并重新运行分析，直到没有潜在问题为止。

MultithreadedTC是一个用于测试并发应用的Java库。它的主要目的是解决并发应用的不确定问题，通过内部节拍器来控制不同线程的执行顺序。如果您正在寻找竞品，以下是一些可能会对您有用的信息：

JUnit：JUnit是一个流行的Java测试框架，可用于编写和运行单元测试、集成测试和端到端测试。它提供了一个简洁的注解语法，可用于定义测试用例和断言，并支持测试套件和测试运行器等功能。
TestNG：TestNG是一个灵活的、基于注解的Java测试框架，它支持单元测试、集成测试、端到端测试和验收测试。它提供了丰富的断言和测试夹具，并支持并行测试、参数化测试和多线程测试等功能。
Selenium：Selenium是一个用于自动化Web应用程序测试的开源工具。它支持多种浏览器和操作系统，并提供了丰富的API和注解，可用于编写自动化测试脚本。Selenium还提供了用于测试Web服务的功能。
Rest Assured：Rest Assured是一个用于测试RESTful服务的Java库。它提供了一个简洁的API和注解语法，可用于构建和发送HTTP请求，并解析响应。Rest Assured还提供了用于测试JSON和XML数据的工具。
Cucumber：Cucumber是一个用于编写行为驱动开发(BDD)测试的Java框架。它提供了一个自然的、易于阅读的语言，可用于描述应用程序的行为和功能。Cucumber还提供了一个插件生态系统，可用于集成不同的测试框架和库。
这些工具和框架都是流行的竞品，您可以在它们之间进行选择，以满足您的测试需求。

Chaos Monkey：Netflix开发的用于测试分布式系统鲁棒性的工具，可以随机使系统中的组件失效。
TPCC：美国交易处理效能委员会(TPC)制定的用来模拟决策支持类应用的一个测试集，常用于模拟测试复杂的在线事务处理系统，以及在大压力情况测试数据库的事务处理能力。

