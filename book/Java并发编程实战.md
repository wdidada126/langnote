# Java并发编程实战

[Java并发编程实战](https://book.douban.com/subject/10484692/)
本书作者都是Java Community Process JSR 166专家组（并发工具）的主要成员，并在其他很多JCP专家组里任职。Brian Goetz有20多年的软件咨询行业经验，并著有至少75篇关于Java开发的文章。Tim Peierls是“现代多处理器”的典范，他在BoxPop.biz、唱片艺术和戏剧表演方面也颇有研究。Joseph Bowbeer是一个Java ME专家，他对并发编程的兴趣始于Apollo计算机时代。David Holmes是《The Java Programming Language》一书的合著者，任职于Sun公司。Joshua Bloch是Google公司的首席Java架构师，《Effective Java》一书的作者，并参与著作了《Java Puzzlers》。Doug Lea是《Concurrent Programming》一书的作者，纽约州立大学 Oswego分校的计算机科学教授。



javax.annotation.concurrent.ThreadSafe

### 第1章　简介

## 第一部分　基础知识

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

线程封闭是一种设计模式，用于确保数据在多线程环境中的安全访问。它通过限制数据的可见性范围，使得数据只能由特定的线程进行访问和修改，从而避免了多线程竞争和数据不一致的问题。以下是线程封闭的三种常见方式：

1. Ad-hoc线程封闭（非结构化封闭）：
   Ad-hoc线程封闭是一种基于编程约定的方式，没有明确的封闭机制。在这种方式下，开发人员通过编码的方式确保数据只在特定的线程中访问和修改。例如，可以使用局部变量来保存数据，将数据限定在方法或线程的作用域内，使其只能在该线程中访问。

2. 栈封闭：
   栈封闭是一种通过将数据保存在线程栈（Thread Stack）中的方式来实现线程封闭的机制。数据存储在线程栈上，只能由拥有该线程栈的线程进行访问。通常，栈封闭用于方法内部创建的局部变量或参数，这些数据在方法执行完毕后会被自动销毁，从而保证了数据的封闭性。

3. ThreadLocal封闭：
   ThreadLocal封闭是一种使用ThreadLocal类的机制来实现线程封闭。ThreadLocal提供了一种将数据与线程关联的方式，使得每个线程都有自己独立的数据副本。线程之间的数据不会相互影响，从而实现了线程封闭。通过ThreadLocal类，可以在当前线程中创建和访问数据，而其他线程无法访问该数据。

这三种线程封闭方式各有优劣，并适用于不同的应用场景。Ad-hoc线程封闭适用于简单的封闭需求，栈封闭适用于方法内部的局部数据，而ThreadLocal封闭适用于需要在线程之间共享数据，但又要保证线程安全的场景。

需要注意的是，线程封闭并不是解决所有多线程并发问题的通用解决方案。在设计多线程应用时，还需要考虑线程间的通信、共享数据的同步和一致性等问题，以确保多线程环境下的正确性和性能。





在Linux下使用C++语言实现ThreadLocal封闭，可以利用pthread库提供的线程特定数据（Thread-Specific Data，TSD）机制。以下是一个示例代码：

```cpp
#include <pthread.h>
#include <iostream>

// 定义线程特定数据的键
pthread_key_t key;

// 线程启动函数
void* threadFunction(void* arg) {
    // 从线程特定数据中获取数据
    int* data = (int*)pthread_getspecific(key);

    // 检查数据是否为NULL
    if (data == NULL) {
        // 创建新的数据并存储到线程特定数据中
        data = new int(0);
        pthread_setspecific(key, data);
    }

    // 修改数据
    (*data)++;

    // 打印数据
    std::cout << "Thread ID: " << pthread_self() << ", Data: " << *data << std::endl;

    return NULL;
}

int main() {
    // 初始化线程特定数据的键
    pthread_key_create(&key, NULL);

    // 创建多个线程
    pthread_t threads[3];
    for (int i = 0; i < 3; i++) {
        pthread_create(&threads[i], NULL, threadFunction, NULL);
    }

    // 等待线程退出
    for (int i = 0; i < 3; i++) {
        pthread_join(threads[i], NULL);
    }

    // 销毁线程特定数据的键
    pthread_key_delete(key);

    return 0;
}
```

在上述代码中，我们首先使用`pthread_key_create`函数创建了一个线程特定数据的键`key`。然后，在线程启动函数`threadFunction`中，我们使用`pthread_getspecific`函数从线程特定数据中获取数据，如果数据为NULL，则创建新的数据并使用`pthread_setspecific`函数存储到线程特定数据中。接着，修改数据并打印出来。最后，我们在主函数中创建多个线程，并等待线程退出后，使用`pthread_key_delete`函数销毁线程特定数据的键。

通过使用线程特定数据的机制，我们可以实现在每个线程中都有独立的数据副本，从而实现了ThreadLocal封闭的效果。

需要注意的是，线程特定数据在C++中也有其他实现方式，如C++11标准中引入的`thread_local`关键字。`thread_local`关键字可以用于定义线程局部存储的变量，从而实现了类似ThreadLocal的功能。不过，`thread_local`关键字的使用可能会受到编译器和标准库的限制，因此在使用时需要根据具体情况进行考虑。





栈封闭 java代码如何实现

在Java中，可以通过在方法内部定义局部变量来实现栈封闭。下面是一个简单的示例代码：

```java
public class StackEncapsulationExample {
    public void doWork() {
        int data = 10; // 定义局部变量

        // 在方法内部进行操作
        // ...

        // 仅在当前方法内部可见，其他线程无法访问该变量
    }
}
```

在上述示例中，`data`是一个局部变量，它被定义在`doWork()`方法内部。该变量的作用域仅限于`doWork()`方法，其他线程无法直接访问该变量。

通过这种方式，确保了`data`变量的封闭性，只有在`doWork()`方法的执行过程中才能访问和修改该变量。当`doWork()`方法执行完毕后，`data`变量会被自动销毁，不再对其他线程可见。

需要注意的是，栈封闭仅适用于局部变量或方法参数等在方法内部定义的数据。如果需要在多个方法之间共享数据，并保证线程安全，可能需要考虑其他的线程封闭机制，如使用`ThreadLocal`或其他同步机制。



Ad-hoc线程封闭是一种基于编程约定的方式，它不依赖于特定的语言支持，而是通过开发人员的编码实践来实现。因此，Java是支持Ad-hoc线程封闭的，开发人员可以通过编码约定来实现线程封闭。

在Java中，可以使用以下方式实现Ad-hoc线程封闭：

1. 方法内部的局部变量：在方法内部定义的局部变量仅在该方法的执行期间可见，不会被其他线程访问到。通过将数据存储在局部变量中，可以实现线程封闭。

2. 方法参数：将数据作为方法的参数传递给方法，方法的参数也是在方法内部的局部变量。只有调用该方法的线程能够访问到方法参数，实现了线程封闭。

通过以上方式，可以在Java中实现Ad-hoc线程封闭。例如：

```java
public class AdHocThreadEncapsulationExample {
    public void doWork() {
        int data = 10; // 定义局部变量

        // 在方法内部进行操作
        // ...

        // 仅在当前方法内部可见，其他线程无法访问该变量
    }
}
```

在上述示例中，`data`变量是在`doWork()`方法内部定义的局部变量，只有在`doWork()`方法的执行过程中才能访问和修改该变量。其他线程无法直接访问该变量，从而实现了线程封闭。

需要注意的是，Ad-hoc线程封闭依赖于开发人员的约定和编码实践，不提供语言级别的保障。因此，在使用Ad-hoc线程封闭时，开发人员需要遵循一致的编码规范，确保数据的封闭性和线程安全性。





https://www.cnblogs.com/gnivor/p/4913132.html

在多线程编程中，为了确保线程安全，通常需要采用一些技术来保证线程之间的数据隔离。下面是三种常见的线程封闭技术：
1. Ad-hoc 线程封闭（临时线程封闭）：这种技术通常用于短时间的任务。它基于一个假设：在一个线程中，一个对象只能被单个方法使用，因此不需要考虑多线程访问。例如，在一个方法中创建一个临时对象，并在同一个方法中使用它，这个对象就是 Ad-hoc 线程封闭的。
2. 栈封闭：这种技术通常用于方法局部变量。它基于一个假设：每个线程都有自己的方法调用栈，方法中的局部变量只能在该方法的执行期间被访问。因此，将数据保存在方法局部变量中，就可以保证线程安全。例如，在一个方法中创建一个对象并将其存储在局部变量中，在方法的执行期间，其他线程无法访问这个对象。
3. ThreadLocal 封闭：ThreadLocal 是 Java 中的一个类，用于在每个线程中存储数据。使用 ThreadLocal 封闭技术，可以将数据存储在 ThreadLocal 对象中，并且每个线程只能访问其自己的数据，从而保证线程安全。例如，在一个方法中，将数据存储在 ThreadLocal 对象中，以便每个线程都可以访问其自己的数据。
这些线程封闭技术都可以用来保证线程安全，但是需要根据具体的应用场景来选择合适的技术。在选择线程封闭技术时，需要考虑数据的访问范围、数据的生命周期以及线程的数量等因素。

20210406评注：自定义ThreadLocal
内存回收
remove方法主要是为了防止内存溢出和内存泄露，使用的时机一般是在线程运行结束之后使用，也就是「un。方法结束之后。下面介绍一下内存泄漏和内存溢的基本概念：
内存泄露(Memory Leak):是指程序中己动态分配的堆内存由于某种原因程序未释放或无法释放，造成系统内存的浪费，导致程序运行速度减慢甚至系统崩溃等严重后果。
内存溢出(Out Of Memory,简称OOM):是指应用系统中存在无法回收的内存或使用的内存过多，最终使得程序运行要用到的内存大于系统能提供的最大内存。此时程序就运行不了，系统会提示内存溢出。
https://www.cnblogs.com/east7/p/13893633.html

### 第4章 对象的组合



### 第5章 基础构建模块



同步工具类
Latch
FutchTask
Semaphere  -> Semaphore
ConcurrentHashMap
size()
isEmpty()方法不一定准确
可以任意读
有限数量个写

FutchTask（也称为 FutureTask）是 Java 中的一个类，它实现了 Future 接口和 Runnable 接口，可以用来表示一个异步计算任务的结果。FutchTask 可以在一个线程中执行，也可以提交给 ExecutorService 等线程池来执行。
FutchTask 的主要作用是在异步计算完成后获取计算结果。通过调用 FutchTask 的 get() 方法，可以阻塞当前线程直到异步计算完成，并返回计算结果。如果异步计算还没有完成，调用 get() 方法会阻塞当前线程，直到计算完成并返回结果。如果异步计算出现异常，调用 get() 方法会抛出相应的异常。
除了获取计算结果，FutchTask 还可以用来取消异步计算任务。通过调用 FutchTask 的 cancel() 方法，可以请求取消异步计算任务。如果任务已经完成或已经被取消，调用 cancel() 方法将不会产生任何影响。如果任务正在执行，调用 cancel() 方法将会中断任务的执行。
总之，FutchTask 是一种非常有用的工具，可以方便地进行异步计算，并在计算完成后获取计算结果或取消计算任务。它在 Java 并发编程中经常被使用。

CompleteService
ES



## 第二部分　结构化并发应用程序



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
           - CallerRunsPolicy 哪个线程提交的任务哪个线程就地执行任务
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





## 第三部分　活跃性、性能与测试
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

### 第11章 性能与可伸缩性

Amdahl定律


### 第12章 并发程序测试



### 第13章 显示锁



### 第14章 构建自定义的同步工具

Condiction -> Condition接口

ReentrantLock
Sephtere    -> Semaphore
Countdownlock  -> CountDownLatch
FutureTask

ReentrantReadWriteLock





CountDownLatch(int count) 构造方法
countDownLatch.countDown()//通知线程本任务执行完毕
countDownLatch.await();//开始暂停，等待其他线程完毕后继续执行



Condition接口

await()
signal()

备注：

Pharse

CyclicBarier



### 第15章 原子变量与非阻塞同步机制

CAS   AtomicInteger Array Reference
ABA

### 第16章 Java内存模型

Java内存模型简介
重排序
