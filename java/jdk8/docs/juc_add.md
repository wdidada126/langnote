# testjuc


juc里面的异常

- BrokenBarrierException
- CancellationException
- CompletionException


juc里面的接口 不包括atomic包和locks包
- BlockingDeque BlockingQueue的子接口
- BlockingQueue
- Callable
- CompletionService
- CompletionStage
- ConcurrentMap
- ConcurrentNavigableMap
- Delayed
- Executor
- ExecutorService
- Future
- RejectedExecutionHandler
- RunnableFuture
- RunnableScheduledFuture
- ScheduledExecutorService
- ScheduledFuture
- ThreadFactory
- TransferQueue
- 
- 
- 
- 
- 
- 



BiConsumer
BiFunction
BinaryOperator
BiPredicate
BooleanSupplier
Consumer
DoubleBinaryOperator
DoubleConsumer
DoubleFunction
DoublePredicate
DoubleSupplier
DoubleTolntFunction
DoubleToLongFunction
DoublellnaryOperator
Function
IntBinaryOperator
IntConsumer
IntFunction
IntPredicate
IntSupplier
IntToDoubleFunction
IntToLongFunction
IntUnaryOperator
LongBinaryOperator
LongConsumer
LongFunction
LongPredicate
LongSupplier
LongToDoubleFunction
LongTolntFunction
LongUnaryOperator
ObjDoubleConsumer
ObjlntConsumer
ObjLongConsumer
Predicate
Supplier
ToDoubleBiFunction
ToDoubleFunction
TolntBiFunction
TolntFunction
ToLongBiFunction
ToLongFunction
UnaryOperator


### juc
stream


Abstractpipeline
Abstra ctShortCi rcuitTask
AbstractSpinedBuffer
AbstractTask
BaseStream
Collector
Collectors
DistinctOps
DoublePipeline
DoubleStream
FindOps
ForEachOps
IntPipeline
₄ IntStream
LongPipeline
LongStream
MatchOps
Node
Nodes
PipelineHelper
ReduceOps
ReferencePipeline
Sink
SliceOps
SortedOps
SpinedBuffer
Stream
StreamOpFlag
Streams
StreamShape
StreamSpliterators
StreamSupport
TerminalOp
Terminalsink
Tripwire


[CAS](http://tutorials.jenkov.com/java-concurrency/compare-and-swap.html)

[参考博客](https://blog.csdn.net/zxc123e/article/details/52057289)

AtomicReference
- get()
- set()
- boolean compareAndSet(V expect, V update) 


https://blog.csdn.net/king866/article/details/53945400

https://blog.csdn.net/leehsiao/article/details/51691637

[java.util.concurrent.locks包下的锁实现分析](https://www.jianshu.com/p/22dcefce6ef4)



1、基本类：AtomicInteger、AtomicLong、AtomicBoolean；
2、引用类型：AtomicReference、AtomicReference的ABA实例、AtomicStampedRerence、AtomicMarkableReference；
3、数组类型：AtomicIntegerArray、AtomicLongArray、AtomicReferenceArray
4、属性原子修改器（Updater）：AtomicIntegerFieldUpdater、AtomicLongFieldUpdater、AtomicReferenceFieldUpdater


抽象类AbstractOwnableSynchronizer、AbstractQueuedLongSynchronizer、AbstractQueuedSynchronizer
接口Lock、ReadWriteLock、Condition
抽象类AbstractOwnableSynchronizer 该类是主要定义让线程以独占方式拥有同步器，此类为创建锁和相关同步器提供了基础，类本身不管理或使用此信息 很简单的两个方法setExclusiveOwnerThread(Thread t)设置当前拥有独占访问的线程 和getExclusiveOwnerThread() 返回由 setExclusiveOwnerThread最后设置的线程；如果从未设置，则返回 null。
抽象类AbstractQueuedSynchronizer 继承自AbstractOwnableSynchronizer该类为实现依赖于先进先出 (FIFO) 等待队列的阻塞锁和相关同步器（信号量、事件，等等）提供一个框架 和是MCSLock的扩展。该类有个属性 private volatile int state; 是The synchronization state. 同步的状态表示。拥有正常的set和get方法后，还有个compareAndSetState方法，是基于unsafe类的compareAndSwapInt来实现的，由此类实现同步。
相似的AbstractQueuedLongSynchronizer类的属性定义是private volatile long state;可以看出是LONG型的属性值。调用的是unsafe.compareAndSwapLong，所以二者的区别就基本知道了，其它没啥区别。


java.util.concurrent.atomic.AtomicIntegerArray类提供了可以以原子方式读取和写入的底层int数组的操作，还包含高级原子操作。 AtomicIntegerArray支持对底层int数组变量的原子操作。 它具有获取和设置方法，如在变量上的读取和写入。 也就是说，一个集合与同一变量上的任何后续get相关联。 原子compareAndSet方法也具有这些内存一致性功能。

[AtomicIntegerArray参考博文](https://www.yiibai.com/java_concurrency/concurrency_atomicintegerarray.html)

[Atomic包之FieldUpdater深度解析](https://juejin.im/entry/59c5e85a5188257e826787d1)
[AtomicReferenceFieldUpdater 使用](https://czj4451.iteye.com/blog/2152041)

AbstractExecutorService
已知子类
- Executors.DelegatedExecutorService
- ThreadPoolExecutor


```java
public class MyAbstractExecutorService extends AbstractExecutorService {

	@Override
	public void shutdown() {
	}

	@Override
	public List<Runnable> shutdownNow() {
		return null;
	}

	@Override
	public boolean isShutdown() {
		return false;
	}

	@Override
	public boolean isTerminated() {
		return false;
	}

	@Override
	public boolean awaitTermination(long timeout, TimeUnit unit)
			throws InterruptedException {
		return false;
	}

	@Override
	public void execute(Runnable command) {
	}
}
```

[BlockingQueue的使用](https://www.cnblogs.com/liuling/p/2013-8-20-01.html)

 1.BlockingQueue定义的常用方法如下: 
        1)add(anObject):把anObject加到BlockingQueue里,即如果BlockingQueue可以容纳,则返回true,否则报异常 
        2)offer(anObject):表示如果可能的话,将anObject加到BlockingQueue里,即如果BlockingQueue可以容纳,则返回true,否则返回false. 
        3)put(anObject):把anObject加到BlockingQueue里,如果BlockQueue没有空间,则调用此方法的线程被阻断直到BlockingQueue里面有空间再继续. 
        4)poll(time):取走BlockingQueue里排在首位的对象,若不能立即取出,则可以等time参数规定的时间,取不到时返回null 
        5)take():取走BlockingQueue里排在首位的对象,若BlockingQueue为空,阻断进入等待状态直到Blocking有新的对象被加入为止 
2.BlockingQueue有四个具体的实现类,根据不同需求,选择不同的实现类 
        1)ArrayBlockingQueue:规定大小的BlockingQueue,其构造函数必须带一个int参数来指明其大小.其所含的对象是以FIFO(先入先出)顺序排序的. 
        2)LinkedBlockingQueue:大小不定的BlockingQueue,若其构造函数带一个规定大小的参数,生成的BlockingQueue有大小限制,若不带大小参数,所生成的BlockingQueue的大小由Integer.MAX_VALUE来决定.其所含的对象是以FIFO(先入先出)顺序排序的 
        3)PriorityBlockingQueue:类似于LinkedBlockQueue,但其所含对象的排序不是FIFO,而是依据对象的自然排序顺序或者是构造函数的Comparator决定的顺序. 
        4)SynchronousQueue:特殊的BlockingQueue,对其的操作必须是放和取交替完成的. 
3.LinkedBlockingQueue和ArrayBlockingQueue比较起来,它们背后所用的数据结构不一样,导致LinkedBlockingQueue的数据吞吐量要大于ArrayBlockingQueue,但在线程数量很大时其性能的可预见性低于ArrayBlockingQueue.      


void put(E e) throws InterruptedException
E take() throws InterruptedException
int size()

[Java多线程-工具篇-BlockingQueue](https://www.cnblogs.com/jackyuj/archive/2010/11/24/1886553.html)


## CompletionService 

[Java并发专题 带返回结果的批量任务执行 CompletionService ExecutorService.invokeAll](https://blog.csdn.net/lmj623565791/article/details/27250059)

已知子类
- ExecutorCompletionService

		/**
		 * 内部维护11个线程的线程池
		 */
		ExecutorService exec = Executors.newFixedThreadPool(11);
		/**
		 * 容量为10的阻塞队列
		 */
		final BlockingQueue<Future<Integer>> queue = new LinkedBlockingDeque<Future<Integer>>(
				10);
		//实例化CompletionService
		final CompletionService<Integer> completionService = new ExecutorCompletionService<Integer>(
				exec, queue);

ConcurrentLinkedQueue 使用例子
并发队列ConcurrentLinkedQueue与阻塞队列LinkedBlockingQueue的区别
https://my.oschina.net/go4it/blog/1532435
https://www.infoq.cn/article/ConcurrentLinkedQueue

对比
| queue | 阻塞与否 | 是否有界 | 线程安全保障 | 适用场景 | 注意事项 |
|-------|---------|---------| -----------| --------| --------|
|ArrayBlockingQueue | 阻塞 | 有界| 一把全局锁 | 生产消费模型，平衡两边处理速度 | -- |
|LinkedBlockingQueue | 阻塞 | 可配置 | 存取采用2把锁 | 生产消费模型，平衡两边处理速度 | 无界的时候注意内存溢出问题 |
|ConcurrentLinkedQueue | 非阻塞 | 无界 | CAS | 对全局的集合进行操作的场景 | size() 是要遍历一遍集合，慎用 |

Java 线程池 拒绝策略 RejectedExecutionHandler介绍
https://blog.csdn.net/u010723709/article/details/50377543
https://blog.csdn.net/qq_28740207/article/details/73087442

下面提供了四种预定义的处理程序策略：
(1) 默认的ThreadPoolExecutor.AbortPolicy   处理程序遭到拒绝将抛出运行时RejectedExecutionException;
(2) ThreadPoolExecutor.CallerRunsPolicy 线程调用运行该任务的 execute 本身。此策略提供简单的反馈控制机制，能够减缓新任务的提交速度
(3) ThreadPoolExecutor.DiscardPolicy  不能执行的任务将被删除;
(4) ThreadPoolExecutor.DiscardOldestPolicy  如果执行程序尚未关闭，则位于工作队列头部的任务将被删除，然后重试执行程序（如果再次失败，则重复此过程）。



百度脑图


## guava源码分析

https://github.com/google/guava/wiki
https://crossoverjie.top/2018/06/13/guava/guava-cache/
https://blog.csdn.net/boling_cavalry/article/details/75174486
http://einverne.github.io/post/2017/07/google-guava.html
http://ifeve.com/guava-ratelimiter/
https://blog.csdn.net/top_code/article/details/51281203
https://blog.csdn.net/Lili429/article/details/79236819

RateLimiter

常用的限流算法有两种：漏桶算法和令牌桶算法。
漏桶算法思路很简单，水（请求）先进入到漏桶里，漏桶以一定的速度出水，当水流入速度过大会直接溢出，可以看出漏桶算法能强行限制数据的传输速率。
对于很多应用场景来说，除了要求能够限制数据的平均传输速率外，还要求允许某种程度的突发传输。这时候漏桶算法可能就不合适了，令牌桶算法更为适合。
令牌桶算法的原理是系统会以一个恒定的速度往桶里放入令牌，而如果请求需要被处理，则需要先从桶里获取一个令牌，当桶里没有令牌可取时，则拒绝服务。

guava也有注解
- acquire()
- reserve()
- reserveEarliestAvailable()

RateLimiter通常用于限制访问某些物理或逻辑资源的速率。这与jdk并发包中的Semaphore相反，它限制并发访问的数量而不是速率(注意，并发和速率是密切相关的)。


https://github.com/LitePalFramework/LitePal 注解

 Map | Corresponding Multiset | Supports null elements ——————|————————-|————————— HashMap | HashMultiset |
 Yes TreeMap | TreeMultiset | Yes (if the comparator does) LinkedHashMap | LinkedHashMultiset |
 Yes ConcurrentHashMap | ConcurrentHashMultiset | No ImmutableMap | ImmutableMultiset | No

 
collections, caching, primitives support, concurrency libraries, common annotations, string processing, I/O

https://blog.csdn.net/aya19880214/article/details/50549979


ExecutorCompletionService构造函数
public ExecutorCompletionService(Executor executor)


注解的处理：
可以用Class Field来判断注解

java.lang.reflect.Field
public boolean isAnnotationPresent
java.lang.reflect.Parameter

使用@interface自定义注解时，自动继承了java.lang.annotation.Annotation接口。



AtomicReferenceFieldUpdater
public abstract boolean compareAndSet(T obj, V expect, V update);


AtomicBoolean
- public AtomicBoolean()
- public AtomicBoolean(boolean initialValue)
- public final boolean get()
- public final void set(boolean newValue)
- public final boolean getAndSet(boolean newValue)
- public final boolean compareAndSet(boolean expect, boolean update)


AtomicIntegerArray
- public final int length()
- public final void set(int i, int newValue)
- public final int get(int i)
- public final int incrementAndGet(int i)
- public final boolean compareAndSet(int i, int expect, int update)



- public AtomicReference()
- public AtomicReference(V initialValue)
- public final void set(V newValue)
- public final boolean compareAndSet(V expect, V update)






