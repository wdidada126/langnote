# Java并发编程之美

独占锁ReentrantLock

https://book.douban.com/subject/30351286/
ISBN: 9787121349478
出版年: 2018-10

6.2 抽象同步队列AQS 概述
StampedLock类是Java 8中引入的一个用于替代synchronized关键字的锁机制，它提供了更高的并发性能和更灵活的锁定操作。StampedLock的主要作用是在多线程环境下实现读写锁的功能，同时避免了synchronized关键字带来的性能开销。
java.util.concurrent.locks.StampedLock


## 第一部分 Java 并发编程基础篇
### 第1 章 并发编程线程基础 2
#### 1.1 什么是线程 2
#### 1.2 线程创建与运行 3
#### 1.3 线程通知与等待 6
#### 1.4 等待线程执行终止的join 方法 16
#### 1.5 让线程睡眠的sleep 方法 19
#### 1.6 让出CPU 执行权的yield 方法 23
#### 1.7 线程中断 24
#### 1.8 理解线程上下文切换 30
#### 1.9 线程死锁 30
1.9.1 什么是线程死锁 30
1.9.2 如何避免线程死锁 33
#### 1.10 守护线程与用户线程 35
#### 1.11 ThreadLocal 39
1.11.1 ThreadLocal使用示例 40
1.11.2 ThreadLocal的实现原理 42
1.11.3 ThreadLocal不支持继承性 45
1.11.4 InheritableThreadLocal 类 46
### 第2 章 并发编程的其他基础知识 50
#### 2.1 什么是多线程并发编程 50
#### 2.2 为什么要进行多线程并发编程 51
#### 2.3 Java 中的线程安全问题 51
#### 2.4 Java 中共享变量的内存可见性问题 52
#### 2.5 Java 中的synchronized 关键字 54
2.5.1 synchronized 关键字介绍 54
2.5.2 synchronized 的内存语义 55
#### 2.6 Java 中的volatile 关键字 55
#### 2.7 Java 中的原子性操作 57
#### 2.8 Java 中的CAS 操作 59
cpu指令，无锁，提高并发量
JDK中的AtomicStampedReference类给每个变量的状态值都配备了一个时间戳，从而避免了ABA问题的产生。

#### 2.9 Unsafe 类 59
2.9.1 Unsafe 类中的重要方法 59
2.9.2 如何使用Unsafe 类 61
#### 2.10 Java 指令重排序 65
Java 内存模型允许编译器和处理器对指令重排序以提高运行性能，并且只会对不存在数据依赖性的指令重排序。在单线程下重排序可以保证最终执行的结果与程序顺序执行的结果一致，但是在多线程下就会存在问题。

#### 2.11 伪共享 67
2.11.1 什么是伪共享 67
2.11.2 为何会出现伪共享 68
2.11.3 如何避免伪共享 70
2.11.4 小结 72
#### 2.12 锁的概述 72
2.12.1 乐观锁与悲观锁 72
乐观锁和悲观锁是在数据库中引入的名词，但是在并发包锁里面也引入了类似的思想。

2.12.2 公平锁与非公平锁 75
2.12.3 独占锁与共享锁 75
根据锁只能被单个线程持有还是能被多个线程共同持有，锁可以分为独占锁和共享锁。

2.12.4 什么是可重入锁 76
2.12.5 自旋锁 77
2.13 总结 77
## 第二部分 Java 并发编程高级篇
### 第3 章 Java 并发包中ThreadLocalRandom 类原理剖析 80
3.1 Random类及其局限性 80
3.2 ThreadLocalRandom 82
3.3 源码分析 84
3.4 总结 87
### 第4 章 Java 并发包中原子操作类原理剖析 88
4.1 原子变量操作类 88
4.2 JDK 8新增的原子操作类LongAdder 93
4.2.1 LongAdder简单介绍 93
4.2.2 LongAdder代码分析 95
4.2.3 小结 101
4.3 LongAccumulator类原理探究 102
4.4 总结 104
### 第5 章 Java并发包中并发List源码剖析 105
5.1 介绍 105
5.2 主要方法源码解析 106
5.2.1 初始化 106
5.2.2 添加元素 106
5.2.3 获取指定位置元素 108
5.2.4 修改指定元素 109
5.2.5 删除元素 110
5.2.6 弱一致性的迭代器 111
5.3 总结 114
### 第6 章 Java并发包中锁原理剖析 115
l 锁

rl 可重入锁
rrwl
sl 
#### 6.1 LockSupport工具类 115
#### 6.2 抽象同步队列AQS概述 122
6.2.1 AQS——锁的底层支持 122
6.2.2 AQS——条件变量的支持 128
6.2.3 基于AQS 实现自定义同步器 131
NonReentrantLock

java.util.concurrent.locks.Condition 接口
    void await() throws InterruptedException;
    void signal();

跟Object类的
    public final native void notify();
    public final native void wait(long timeout) throws InterruptedException;


c++里面是 condiction_variable
condition_variable
    cv.notify_all();
    cv.wait(lck);

在C++中，条件变量（condition_variable）是一种同步原语，用于在多线程环境中实现线程间的同步。而在Java中，条件变量被称为`Condition`对象。

以下是C++和Java中条件变量的示例：

C++示例：
```cpp
#include <iostream>
#include <thread>
#include <mutex>
#include <condition_variable>

std::mutex mtx;
std::condition_variable cv;
bool ready = false;

void print_id(int id) {
    std::unique_lock<std::mutex> lck(mtx);
    while (!ready) {
        cv.wait(lck);
    }
    // 当ready为true时，打印线程ID
    std::cout << "thread " << id << '
';
}

void go() {
    std::unique_lock<std::mutex> lck(mtx);
    ready = true;
    cv.notify_all();
}

int main() {
    std::thread threads[10];
    // 启动10个线程
    for (int i = 0; i < 10; ++i) {
        threads[i] = std::thread(print_id, i);
    }

    std::cout << "10 threads ready to race...
";
    go(); // 通知所有线程开始竞争

    for (auto& th : threads) {
        th.join();
    }

    return 0;
}
```

Java示例：
```java
import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public class ConditionExample {
    private final Lock lock = new ReentrantLock();
    private final Condition condition = lock.newCondition();
    private boolean ready = false;

    public void printId(int id) throws InterruptedException {
        lock.lock();
        try {
            while (!ready) {
                condition.await();
            }
            // 当ready为true时，打印线程ID
            System.out.println("Thread " + id);
        } finally {
            lock.unlock();
        }
    }

    public void go() {
        lock.lock();
        try {
            ready = true;
            condition.signalAll();
        } finally {
            lock.unlock();
        }
    }

    public static void main(String[] args) throws InterruptedException {
        ConditionExample example = new ConditionExample();
        Thread[] threads = new Thread[10];
        // 启动10个线程
        for (int i = 0; i < 10; ++i) {
            threads[i] = new Thread(() -> {
                try {
                    example.printId(Thread.currentThread().getId());
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            });
            threads[i].start();
        }

        System.out.println("10 threads ready to race...");
        example.go(); // 通知所有线程开始竞争

        for (Thread thread : threads) {
            thread.join();
        }
    }
}
```

见NonReentrantLock.java
#### 6.3 独占锁ReentrantLock的原理 136
6.3.1 类图结构 136
6.3.2 获取锁 137
6.3.3 释放锁 142
6.3.4 案例介绍 143
6.3.5 小结 145
ReentrantLock是可重入的独占锁
 void lock() void lockInterruptibly() boolean tryLock()

#### 6.4 读写锁ReentrantReadWriteLock 的原理 145
6.4.1 类图结构 145
6.4.2 写锁的获取与释放 147
6.4.3 读锁的获取与释放 151
6.4.4 案例介绍 156
6.4.5 小结 158

ReentrantReadWriteLock是Java中的一个可重入读写锁，它允许多个线程同时读取共享资源，但只允许一个线程写入共享资源。以下是一个简单的ReentrantReadWriteLock API例子：

```java
import java.util.concurrent.locks.ReadWriteLock;
import java.util.concurrent.locks.ReentrantReadWriteLock;

public class ReentrantReadWriteLockExample {
    private final ReadWriteLock readWriteLock = new ReentrantReadWriteLock();

    public void read() {
        readWriteLock.readLock().lock();
        try {
            System.out.println(Thread.currentThread().getName() + " 正在读取数据");
            // 模拟读取数据操作
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            readWriteLock.readLock().unlock();
        }
    }

    public void write() {
        readWriteLock.writeLock().lock();
        try {
            System.out.println(Thread.currentThread().getName() + " 正在写入数据");
            // 模拟写入数据操作
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            readWriteLock.writeLock().unlock();
        }
    }

    public static void main(String[] args) {
        ReentrantReadWriteLockExample example = new ReentrantReadWriteLockExample();

        // 创建多个线程进行读操作
        for (int i = 0; i < 5; i++) {
            new Thread(() -> example.read(), "读线程" + (i + 1)).start();
        }

        // 创建一个线程进行写操作
        new Thread(() -> example.write(), "写线程").start();
    }
}
```

在这个例子中，我们创建了一个ReentrantReadWriteLock实例，并定义了两个方法：read()和write()。read()方法用于读取数据，write()方法用于写入数据。在这两个方法中，我们分别使用了readLock()和writeLock()方法来获取锁，并在finally块中释放锁。在main方法中，我们创建了多个读线程和一个写线程，以演示ReentrantReadWriteLock的用法。

#### 6.5 JDK 8中新增的StampedLock锁探究 158
6.5.1 概述 158
6.5.2 案例介绍 160
6.5.3 小结 164
api注意跟ReentrantReadWriteLock对比

public StampedLock()
        long stamp = lock.writeLock();
            lock.unlockWrite(stamp);
        long stamp = lock.readLock();
            lock.unlockRead(stamp);

public long tryWriteLock() 
public long tryWriteLock(long time, TimeUnit unit)

StampedLock类是Java 8中引入的一个用于替代synchronized关键字的锁机制，它提供了更高的并发性能和更灵活的锁定操作。StampedLock的主要作用是在多线程环境下实现读写锁的功能，同时避免了synchronized关键字带来的性能开销。

下面是一个使用StampedLock的例子：

```java
import java.util.concurrent.locks.StampedLock;

public class StampedLockExample {
    private int value;
    private final StampedLock lock = new StampedLock();

    public void increment() {
        long stamp = lock.writeLock();
        try {
            value++;
        } finally {
            lock.unlockWrite(stamp);
        }
    }

    public int getValue() {
        long stamp = lock.readLock();
        try {
            return value;
        } finally {
            lock.unlockRead(stamp);
        }
    }

    public static void main(String[] args) throws InterruptedException {
        StampedLockExample example = new StampedLockExample();

        Thread writer = new Thread(() -> {
            for (int i = 0; i < 1000; i++) {
                example.increment();
            }
        });

        Thread reader = new Thread(() -> {
            for (int i = 0; i < 1000; i++) {
                System.out.println(example.getValue());
            }
        });

        writer.start();
        reader.start();

        writer.join();
        reader.join();
    }
}
```

在这个例子中，我们创建了一个名为StampedLockExample的类，其中有一个整数值value和一个StampedLock对象lock。我们定义了两个方法：increment()用于递增value的值，getValue()用于获取value的值。在这两个方法中，我们都使用了StampedLock的写锁和读锁来确保线程安全。

在main方法中，我们创建了两个线程：一个用于写入数据，另一个用于读取数据。通过使用StampedLock，我们可以确保在多线程环境下对value的操作是线程安全的。

### 第7章 Java并发包中并发队列原理剖析 165

三个阻塞队列
ArrayBlockingQueue
LinkedBlockingQueue
PriorityBlockingQueue

    boolean add(E e);
    boolean offer(E e);
    E remove();
    E poll();
    E element();
    E peek();

#### 7.1 ConcurrentLinkedQueue原理探究 165
7.1.1 类图结构 165
7.1.2 ConcurrentLinkedQueue原理介绍 166
7.1.3 小结 181
#### 7.2 LinkedBlockingQueue原理探究 182
7.2.1 类图结构 182
7.2.2 LinkedBlockingQueue 原理介绍 185
7.2.3 小结 194
7.3 ArrayBlockingQueue原理探究 195
7.3.1 类图结构 195
7.3.2 ArrayBlockingQueue原理介绍 197
7.3.3 小结 202
#### 7.4 PriorityBlockingQueue原理探究 203
7.4.1 介绍 203
7.4.2 PriorityBlockingQueue类图结构 203
7.4.3 原理介绍 205
7.4.4 案例介绍 214
7.4.5 小结 216
#### 7.5 DelayQueue原理探究 217
7.5.1 DelayQueue 类图结构 217
7.5.2 主要函数原理讲解 219
7.5.3 案例介绍 222
7.5.4 小结 224
### 第8章 Java并发包中线程池ThreadPoolExecutor原理探究 225
#### 8.1 介绍 225
#### 8.2 类图介绍 225
#### 8.3 源码分析 230
8.3.1 public void execute(Runnable command) 230
8.3.2 工作线程Worker 的执行 235
8.3.3 shutdown 操作 238
8.3.4 shutdownNow 操作 240
8.3.5 awaitTermination 操作 241
#### 8.4 总结 242

ThreadPoolExecutor 线程池执行器

定时线程池执行器
public class ScheduledThreadPoolExecutor
        extends ThreadPoolExecutor
        implements ScheduledExecutorService

### 第9 章 Java 并发包中ScheduledThreadPoolExecutor 原理探究 243
#### 9.1 介绍 243
#### 9.2 类图介绍 243
9.3 原理剖析 245
9.3.1 schedule(Runnable command, long delay,TimeUnit unit) 方法 246
9.3.2 scheduleWithFixedDelay(Runnable command,long initialDelay, long delay,TimeUnit unit) 方法 252
9.3.3 scheduleAtFixedRate(Runnable command,long initialDelay,long period,TimeUnit unit) 方法 254
9.4 总结 255
### 第10 章 Java并发包中线程同步器原理剖析 256
#### 10.1 CountDownLatch 原理剖析 256
10.1.1 案例介绍 256
10.1.2 实现原理探究 259
10.1.3 小结 263

countDown();
await()

#### 10.2 回环屏障CyclicBarrier原理探究 264
10.2.1 案例介绍 264
10.2.2 实现原理探究 268
10.2.3 小结 272
#### 10.3 信号量Semaphore原理探究 272
10.3.1 案例介绍 272
10.3.2 实现原理探究 276
10.3.3 小结 281
#### 10.4 总结 281
public CyclicBarrier(int parties, Runnable barrierAction)
public int await() 
public void reset() 可以复用


public Semaphore(int permits, boolean fair)
public void acquire()
public void release()


## 第三部分 Java 并发编程实践篇
### 第11 章 并发编程实践 284
#### 11.1 ArrayBlockingQueue 的使用 284
11.1.1 异步日志打印模型概述 284
11.1.2 异步日志与具体实现 285
11.1.3 小结 293
#### 11.2 Tomcat的NioEndPoint中ConcurrentLinkedQueue的使用 293
11.2.1 生产者——Acceptor线程 294
11.2.2 消费者——Poller线程 298
11.2.3 小结 300
#### 11.3 并发组件ConcurrentHashMap使用注意事项 300
#### 11.4 SimpleDateFormat是线程不安全的 304
11.4.1 问题复现 304
11.4.2 问题分析 305
11.4.3 小结 309
#### 11.5 使用Timer时需要注意的事情 309
11.5.1 问题的产生 309
11.5.2 Timer实现原理分析 310
11.5.3 小结 313
#### 11.6 对需要复用但是会被下游修改的参数要进行深复制 314
11.6.1 问题的产生 314
11.6.2 问题分析 316
11.6.3 小结 318
#### 11.7 创建线程和线程池时要指定与业务相关的名称 319
11.7.1 创建线程需要有线程名 319
11.7.2 创建线程池时也需要指定线程池的名称 321
11.7.3 小结 325
#### 11.8 使用线程池的情况下当程序结束时记得调用shutdown关闭线程池 325
11.8.1 问题复现 325
11.8.2 问题分析 327
11.8.3 小结 329
#### 11.9 线程池使用FutureTask时需要注意的事情 329
11.9.1 问题复现 329
11.9.2 问题分析 332
11.9.3 小结 335
#### 11.10 使用ThreadLocal不当可能会导致内存泄漏 336
11.10.1 为何会出现内存泄漏 336
11.10.2 在线程池中使用ThreadLocal导致的内存泄漏 339
11.10.3 在Tomcat的Servlet中使用ThreadLocal导致内存泄漏 341
11.10.4 小结 344
#### 11.11 总结 344
