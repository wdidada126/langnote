gitee.com/edidada/juc

[java.util.concurrent - Java Concurrency Utilities](http://tutorials.jenkov.com/java-util-concurrent/index.html)


BlockingDeque 双端队列

[BlockingDeque 双端队列](https://www.jianshu.com/p/250da025e7cd)

[并发编程- java.util.concurrent用户指南](https://www.jianshu.com/p/8cb5d816cb69)


BlockingQueue既然是Queue的子接口

[Queue api](https://docs.oracle.com/javase/7/docs/api/java/util/Queue.html)
    	Throws exception	Returns special value
Insert	add(e)				offer(e)
Remove	remove()			poll()
Examine	element()			peek()

看一下BlockingQueue中特有的方法：
（1）void put(E e) throws InterruptedException
把e添加进BlockingQueue中，如果BlockingQueue中没有空间，则调用线程被阻塞，进入等待状态，直到BlockingQueue中有空间再继续
（2）void take() throws InterruptedException
取走BlockingQueue里面排在首位的对象，如果BlockingQueue为空，则调用线程被阻塞，进入等待状态，直到BlockingQueue有新的数据被加入
（3）int drainTo(Collection<? super E> c, int maxElements)
一次性取走BlockingQueue中的数据到c中，可以指定取的个数。通过该方法可以提升获取数据效率，不需要多次分批加锁或释放锁


BlockingQueue是个接口，你需要使用它的实现之一来使用 BlockingQueue。java.util.concurrent 具有以下 BlockingQueue 接口的实现(Java 6)：
- ArrayBlockingQueue
- DelayQueue
- LinkedBlockingQueue
- PriorityBlockingQueue
- SynchronousQueue


TimeUnit 枚举将会取以下值：
DAYS
HOURS
MINUTES
SECONDS
MILLISECONDS
MICROSECONDS
NANOSECONDS


public interface CompletionService<V>

CompletionService是接口
Java线程之CompletionService批处理任务

[Java线程之CompletionService批处理任务](https://www.cnblogs.com/xubiao/p/5463283.html)

[CompletionService和ExecutorCompletionService详解](https://www.jianshu.com/p/cfda708a3478)

- CompletionService(ExecutorService es) 构造函数
- submit() - 提交任务
- take() - 获取任务结果
- poll() - 获取任务结果







https://blog.csdn.net/CringKong/article/details/79994511



https://www.bilibili.com/video/BV1sJ411L7ZB







