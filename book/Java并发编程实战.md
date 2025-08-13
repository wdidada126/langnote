# Java并发编程实战

java8是2014年3月
书籍是2012年

作者: [美] Brian Goetz / [美] Tim Peierls / [美] Joshua Bloch / [美] Joseph Bowbeer / [美] David Holmes / [美] Doug Lea
出版社: 机械工业出版社
原作名: Java Concurrency in Practice
译者: 童云兰
出版年: 2012-2
页数: 293
定价: 69.00元
装帧: 平装
丛书: 华章专业开发者丛书
ISBN: 9787111370048

关于《Java Concurrency in Practice》（中文译名：《Java并发编程实战》）是否有针对 Java 8 的版本，情况如下：

没有官方发布的、内容全面更新至 Java 8 的新版《Java Concurrency in Practice》。

这本书的原始英文版首次出版于 2006 年，主要基于 Java 5 和 Java 6 的并发特性编写。

### 为什么说“没有”Java 8 版本？

1.  作者和出版社未推出新版：该书的作者 Brian Goetz 等人以及出版社 Addison-Wesley 没有发布过一个名为 "Java Concurrency in Practice, 2nd Edition" 或类似、专门针对 Java 8 进行全面修订的版本。
2.  核心内容依然经典：这本书的核心价值在于它深入阐述的并发原理、设计模式、最佳实践和潜在陷阱（如线程安全、死锁、性能、可伸缩性等）。这些基础理论和原则在 Java 8 及以后的版本中依然是完全适用的，甚至更加重要。

### 但它仍然包含 Java 8 的相关内容

   `java.util.concurrent` 包的演进：虽然书的核心是 Java 5/6，但它详细讲解的 `java.util.concurrent` 包是 Java 并发的基石。Java 8 在这个包的基础上进行了增强（例如 `CompletableFuture` 的大量新方法、`ConcurrentHashMap` 的新函数式方法等），但这些是建立在书中所讲的 `Executor`、`Future`、`ConcurrentMap` 等基础之上的。
   后续讨论和补充：作者 Brian Goetz 等人（特别是 Doug Lea）深度参与了 Java 8 中并发 API 的设计（如 `CompletableFuture`, `LongAdder`, `StampedLock` 等）。你可以通过阅读他们的论文、JEP (JDK Enhancement Proposal) 或后续的博客文章来了解 Java 8 新特性的设计思想，这些思想与《Java Concurrency in Practice》中的原则一脉相承。

### 结论

   《Java Concurrency in Practice》没有官方的“Java 8 版本”。
   但它仍然是学习 Java 并发的“圣经”和最佳起点。即使你主要使用 Java 8+，这本书提供的基础理论和思维方式是无可替代的。
   在掌握了这本书的核心内容后，你可以再学习 Java 8 引入的新工具，如：
       `CompletableFuture` (用于异步编程和流式调用)
       `LongAdder` / `DoubleAdder` (高性能计数器)
       `StampedLock` (更灵活的读写锁)
       `java.util.concurrent` 中集合类的 `Stream` API 和 `forEach`/`compute`/`merge` 等方法。

简单来说：这本书是“道”（原理），Java 8 的新特性是“术”（工具）。先学“道”，再学“术”，效果最佳。

[Java并发编程实战](https://book.douban.com/subject/10484692/)
本书作者都是Java Community Process JSR 166专家组（并发工具）的主要成员，并在其他很多JCP专家组里任职。Brian Goetz有20多年的软件咨询行业经验，并著有至少75篇关于Java开发的文章。Tim Peierls是“现代多处理器”的典范，他在BoxPop.biz、唱片艺术和戏剧表演方面也颇有研究。Joseph Bowbeer是一个Java ME专家，他对并发编程的兴趣始于Apollo计算机时代。David Holmes是《The Java Programming Language》一书的合著者，任职于Sun公司。Joshua Bloch是Google公司的首席Java架构师，《Effective Java》一书的作者，并参与著作了《Java Puzzlers》。Doug Lea是《Concurrent Programming》一书的作者，纽约州立大学 Oswego分校的计算机科学教授。

javax.annotation.concurrent.ThreadSafe
对本书的赞誉
译者序
前　言
第1章　简介1
1.1　并发简史1
1.2　线程的优势2
1.2.1　发挥多处理器的强大能力2
1.2.2　建模的简单性3
1.2.3　异步事件的简化处理3
1.2.4　响应更灵敏的用户界面4
1.3　线程带来的风险4
1.3.1　安全性问题5
1.3.2　活跃性问题7
1.3.3　性能问题7
1.4　线程无处不在7
第一部分　基础知识
第2章　线程安全性11
2.1　什么是线程安全性13
2.2　原子性14
2.2.1　竞态条件15
2.2.2　示例：延迟初始化中的竞态条件16
2.2.3　复合操作17
2.3　加锁机制18
2.3.1　内置锁20
2.3.2　重入21
2.4　用锁来保护状态22
2.5　活跃性与性能23
第3章　对象的共享27
3.1　可见性27
3.1.1　失效数据28
3.1.2　非原子的64位操作29
3.1.3　加锁与可见性30
3.1.4　Volatile变量 30
3.2　发布与逸出32
3.3　线程封闭35
3.3.1　Ad-hoc线程封闭35
3.3.2　栈封闭36
3.3.3　ThreadLocal类37
3.4　不变性38
3.4.1　Final域39
3.4.2　示例：使用Volatile类型来发布不可变对象40
3.5　安全发布41
3.5.1　不正确的发布：正确的对象被破坏42
3.5.2 　不可变对象与初始化安全性42
3.5.3　安全发布的常用模式43
3.5.4　事实不可变对象44
3.5.5　可变对象44
3.5.6　安全地共享对象44
第4章　对象的组合46
4.1　设计线程安全的类46
4.1.1　收集同步需求47
4.1.2　依赖状态的操作48
4.1.3　状态的所有权48
4.2　实例封闭49
4.2.1　Java监视器模式51
4.2.2　示例：车辆追踪51
4.3　线程安全性的委托53
4.3.1　示例：基于委托的车辆追踪器54
4.3.2　独立的状态变量55
4.3.3　当委托失效时56
4.3.4　发布底层的状态变量57
4.3.5　示例：发布状态的车辆追踪器58
4.4　在现有的线程安全类中添加功能59
4.4.1　客户端加锁机制60
4.4.2　组合62
4.5　将同步策略文档化62
第5章　基础构建模块66
5.1　同步容器类66
5.1.1　同步容器类的问题66
5.1.2　迭代器与Concurrent-ModificationException68
5.1.3　隐藏迭代器69
5.2　并发容器70
5.2.1　ConcurrentHashMap71
5.2.2　额外的原子Map操作72
5.2.3　CopyOnWriteArrayList72
5.3　阻塞队列和生产者-消费者模式73
5.3.1　示例：桌面搜索75
5.3.2　串行线程封闭76
5.3.3　双端队列与工作密取77
5.4　阻塞方法与中断方法77
5.5　同步工具类78
5.5.1　闭锁79
5.5.2　FutureTask80
5.5.3　信号量82
5.5.4　栅栏83
5.6　构建高效且可伸缩的结果缓存85
第二部分　结构化并发应用程序
第6章　任务执行93
6.1　在线程中执行任务93
6.1.1　串行地执行任务94
6.1.2　显式地为任务创建线程94
6.1.3　无限制创建线程的不足95
6.2　Executor框架96
6.2.1　示例：基于Executor的Web服务器97
6.2.2　执行策略98
6.2.3　线程池98
6.2.4　Executor的生命周期99
6.2.5　延迟任务与周期任务101
6.3　找出可利用的并行性102
6.3.1　示例：串行的页面渲染器102
6.3.2　携带结果的任务Callable与Future103
6.3.3　示例：使用Future实现页面渲染器104
6.3.4　在异构任务并行化中存在的局限106
6.3.5　CompletionService:Executor与BlockingQueue106
6.3.6　示例：使用CompletionService实现页面渲染器107
6.3.7　为任务设置时限108
6.3.8　示例：旅行预定门户网站109
第7章　取消与关闭111
7.1　任务取消111
7.1.1　中断113
7.1.2　中断策略116
7.1.3　响应中断117
7.1.4　示例：计时运行118
7.1.5　通过Future来实现取消120
7.1.6　处理不可中断的阻塞121
7.1.7　采用newTaskFor来封装非标准的取消122
7.2　停止基于线程的服务124
7.2.1　示例：日志服务124
7.2.2　关闭ExecutorService127
7.2.3　“毒丸”对象128
7.2.4　示例：只执行一次的服务129
7.2.5　shutdownNow的局限性130
7.3　处理非正常的线程终止132
7.4　JVM关闭135
7.4.1　关闭钩子135
7.4.2　守护线程136
7.4.3　终结器136
第8章　线程池的使用138
8.1　在任务与执行策略之间的隐性耦合138
8.1.1　线程饥饿死锁139
8.1.2　运行时间较长的任务140
8.2　设置线程池的大小140
8.3　配置ThreadPoolExecutor141
8.3.1　线程的创建与销毁142
8.3.2　管理队列任务142
8.3.3　饱和策略144
8.3.4　线程工厂146
8.3.5　在调用构造函数后再定制ThreadPoolExecutor147
8.4　扩展 ThreadPoolExecutor148
8.5　递归算法的并行化149
第9章　图形用户界面应用程序156
9.1　为什么GUI是单线程的156
9.1.1　串行事件处理157
9.1.2　Swing中的线程封闭机制158
9.2　短时间的GUI任务160
9.3　长时间的GUI任务161
9.3.1　取消162
9.3.2　进度标识和完成标识163
9.3.3　SwingWorker165
9.4　共享数据模型165
9.4.1　线程安全的数据模型166
9.4.2　分解数据模型166
9.5　其他形式的单线程子系统167
第三部分　活跃性、性能与测试
第10章　避免活跃性危险169
10.1　死锁169
10.1.1　锁顺序死锁170
10.1.2　动态的锁顺序死锁171
10.1.3　在协作对象之间发生的死锁174
10.1.4　开放调用175
10.1.5　资源死锁177
10.2　死锁的避免与诊断178
10.2.1　支持定时的锁178
10.2.2　通过线程转储信息来分析死锁178
10.3　其他活跃性危险180
10.3.1　饥饿180
10.3.2　糟糕的响应性181
10.3.3　活锁181
### 第11章　性能与可伸缩性183
11.1　对性能的思考183
11.1.1　性能与可伸缩性184
11.1.2　评估各种性能权衡因素185
11.2　Amdahl定律186
11.2.1　示例：在各种框架中隐藏的串行部分188
11.2.2　Amdahl定律的应用189
11.3　线程引入的开销189
11.3.1　上下文切换190
11.3.2　内存同步190
11.3.3　阻塞192
11.4　减少锁的竞争192
11.4.1　缩小锁的范围（“快进快出”）193
11.4.2　减小锁的粒度195
11.4.3　锁分段196
11.4.4　避免热点域197
11.4.5　一些替代独占锁的方法198
11.4.6　监测CPU的利用率199
11.4.7　向对象池说“不”200
11.5　示例：比较Map的性能200
11.6　减少上下文切换的开销201
### 第12章　并发程序的测试204
12.1　正确性测试205
12.1.1　基本的单元测试206
12.1.2　对阻塞操作的测试207
12.1.3　安全性测试208
12.1.4　资源管理的测试212
12.1.5　使用回调213
12.1.6　产生更多的交替操作214
12.2　性能测试215
12.2.1　在PutTakeTest中增加计时功能215
12.2.2　多种算法的比较217
12.2.3　响应性衡量218
12.3　避免性能测试的陷阱220
12.3.1　垃圾回收220
12.3.2　动态编译220
12.3.3　对代码路径的不真实采样222
12.3.4　不真实的竞争程度222
12.3.5　无用代码的消除223
12.4　其他的测试方法224
12.4.1　代码审查224
12.4.2　静态分析工具224
12.4.3　面向方面的测试技术226
12.4.4　分析与监测工具226
## 第四部分　高级主题
### 第13章　显式锁227
13.1　Lock与 ReentrantLock227
13.1.1　轮询锁与定时锁228
13.1.2　可中断的锁获取操作230
13.1.3　非块结构的加锁231
13.2　性能考虑因素231
13.3　公平性232
13.4　在synchronized和ReentrantLock之间进行选择234
13.5　读-写锁235
### 　构建自定义的同步工具238
14.1　状态依赖性的管理238
14.1.1　示例：将前提条件的失败传递给调用者240
14.1.2　示例：通过轮询与休眠来实现简单的阻塞241
14.1.3　条件队列243
14.2　使用条件队列244
14.2.1　条件谓词244
14.2.2　过早唤醒245
14.2.3　丢失的信号246
14.2.4　通知247
14.2.5　示例：阀门类248
14.2.6　子类的安全问题249
14.2.7　封装条件队列250
14.2.8　入口协议与出口协议250
14.3　显式的Condition对象251
14.4　Synchronizer剖析253
14.5　AbstractQueuedSynchronizer254
14.6　java.util.concurrent同步器类中的 AQS257
14.6.1　ReentrantLock257
14.6.2　Semaphore与CountDownLatch258
14.6.3　FutureTask259
14.6.4　ReentrantReadWriteLock259
### 第15章　原子变量与非阻塞同步机制261
15.1　锁的劣势261
15.2　硬件对并发的支持262
15.2.1　比较并交换263
15.2.2　非阻塞的计数器264
15.2.3　JVM对CAS的支持265
15.3　原子变量类265
15.3.1　原子变量是一种“更好的volatile”266
15.3.2　性能比较：锁与原子变量267
15.4　非阻塞算法270
15.4.1　非阻塞的栈270
15.4.2　非阻塞的链表272
15.4.3　原子的域更新器274
15.4.4　ABA问题275
### 第16章　Java内存模型277
16.1　什么是内存模型，为什么需要它277
16.1.1　平台的内存模型278
16.1.2　重排序278
16.1.3　Java内存模型简介280
16.1.4　借助同步281
16.2　发布283
16.2.1　不安全的发布283
16.2.2　安全的发布284
16.2.3　安全初始化模式284
16.2.4　双重检查加锁286
16.3　初始化过程中的安全性287
附录A　并发性标注289
## 笔记
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
