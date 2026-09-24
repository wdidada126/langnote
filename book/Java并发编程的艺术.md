# Java并发编程的艺术

https://book.douban.com/subject/26591326/

并发编程领域的扛鼎之作，作者是阿里和1号店的资深Java技术专家，对并发编程有非常深入的研究，《Java并发编程的艺术》是他们多年一线开发经验的结晶。本书的部分内容在出版早期发表在Java并发编程网和InfoQ等技术社区，得到了非常高的评价。它选取了Java并发编程中最核心的技术进行讲解，从JDK源码、JVM、CPU等多角度全面剖析和讲解了Java并发编程的框架、工具、原理和方法，对Java并发编程进行了最为深入和透彻的阐述。

《Java并发编程的艺术》内容涵盖Java并发编程机制的底层实现原理、Java内存模型、Java并发编程基础、Java中的锁、并发容器和框架、原子类、并发工具类、线程池、Executor框架等主题，每个主题都做了深入的讲解，同时通过实例介绍了如何应用这些技术。


方腾飞（花名清英，英文名kiral），

蚂蚁金服集团技术专家，从事Java开发近10年。5年以上的团队管理、项目管理和敏捷开发经验，崇尚团队合作。曾参与CMS、电子海图、SOC、ITIL、电子商务网站和信贷管理系统等项目。目前在蚂蚁金服网商银行贷款管理团队负责数据采集平台开发工作。与同事合作开发了tala code Review插件，深受阿里数千名工程师拥趸，并开发过开源工具jdbcutil（https://github.com/kiral/utils）。创办了并发编程网，组织翻译了百余篇国外优秀技术文章，并曾为InfoQ撰写“聊聊并发”专栏，在《程序员》杂志撰写敏捷实践系列文章

魏　鹏，
阿里巴巴集团技术专家，在阿里巴巴中国网站技术部工作多年，曾担任中国网站交易平台架构师，主导了交易系统服务化工作，设计实现的数据迁移系统高效地完成了阿里巴巴中国网站交易数据到阿里巴巴集团的迁移工作。目前在阿里巴巴共享业务事业部从事Java应用容器Pandora和服务框架HSF的相关工作，其中Java应用容器Pandora是阿里巴巴中间件运行的基础，而服务框架HSF则是阿里巴巴集团实现服务化的主要解决方案，二者在阿里巴巴拥有最为广泛的使用量。个人平时喜欢阅读技术书籍，翻译一些国外优秀文档，喜欢总结、乐于分享，对Java应用容器、多线程编程以及分布式系统感兴趣。

程晓明，
1号店资深架构师，从事1号店交易平台系统的开发，技术上关注并发与NIO。因5年前遇到的一个线上故障，解决过程中对Java并发编程产生了浓厚的兴趣，从此开始了漫长的探索之旅：从底层实现机制、内存模型到Java同步。纵观我自己对Java并发的学习过程，是一个从高层到底层再到高层的一个反复迭代的过程，我估计很多读者的学习过程应该与我类似。文章多见诸《IBM developerWorks》、InfoQ和《程序员》杂志。


方腾飞 ifeve
魏鹏
程晓明 IBM developerWorks

jvm
cpu

cpu
L123 缓存

手册
intel

栅栏 锁 内存屏

翻译的不错.大部分内容来自于jsr-133和Doug Lea的jsr-133 Cookbook,如果想深入研究这方面的问题,推荐仔细研究一下上面的两个文献和本书里提及到的引用文献(当然还有Lea的另外两本书),本书文献的引用只提及于书的正文,末尾并没有参考文献.也许是书名的"著"导致的这个问题.

从网站下载了示例代码, 排版风格不一致, 勉强可以接受, 毕竟是多个人写的, 但是文件的编码格式五花八门, 有的是UTF-8, 有的是 ANSI, 有的是 GB2312 等等.

### 第1章　并发编程的挑战

### 第2章　Java并发机制的底层实现原理

volatile、synchronized和原子操作的实现原理

### 第3章　Java内存模型
Java内存模型跟jvm内存模型区别开来

### 第4章　Java并发编程基础

volitale cas更新一个标量

### 第5章　Java中的锁

### 第6章　Java并发容器和框架

ConcurrentHashMap

HashTable容器使用synchronized来保证线程安全

JDK 7提供了7个阻塞队列，如下。
·ArrayBlockingQueue：一个由数组结构组成的有界阻塞队列。
·LinkedBlockingQueue：一个由链表结构组成的有界阻塞队列。
·PriorityBlockingQueue：一个支持优先级排序的无界阻塞队列。
·DelayQueue：一个使用优先级队列实现的无界阻塞队列。
·SynchronousQueue：一个不存储元素的阻塞队列。
·LinkedTransferQueue：一个由链表结构组成的无界阻塞队列。
·LinkedBlockingDeque：一个由链表结构组成的双向阻塞队列。

工作窃取（work-stealing）算法

### 第7章　Java中的13个原子操作类

Atomic包里的类基本都是使用Unsafe实现的包装类。

### 第8章　Java中的并发工具类

CountDownLatch、CyclicBarrier和

Semaphore工具类提供了一种并发流程控制的手段，Exchanger工具类则提供了在线程间交换数

据的一种手段



`CountDownLatch`和`CyclicBarrier`都是Java中用于多线程协作的工具类，它们的作用是在多个线程之间同步执行，以实现一些复杂的场景。虽然它们的作用有些相似，但它们的实现方式和使用场景有很大的区别。

1. `CountDownLatch`

`CountDownLatch`是一种简单的同步工具，它用于等待一个或多个线程完成某些操作后再继续执行。具体来说，`CountDownLatch`维护一个计数器，该计数器初始化为一个正整数，当一个或多个线程调用`countDown()`方法时，计数器的值减1，当计数器的值变为0时，等待的线程将被唤醒继续执行。

`CountDownLatch`的主要作用是在多个线程之间协调执行顺序。例如，可以使用`CountDownLatch`来等待多个线程完成初始化操作后再开始执行其他操作。`CountDownLatch`的使用场景比较单一，它适用于一次性等待多个线程完成某个操作，而且这些线程之间的协作方式比较简单。

1. `CyclicBarrier`

`CyclicBarrier`也是一种同步工具，它用于等待多个线程到达某个屏障点后再继续执行。具体来说，`CyclicBarrier`维护一个计数器和一个屏障点，当多个线程都调用`await()`方法时，计数器的值增加1，当计数器的值达到屏障点时，所有等待的线程将被唤醒继续执行。

`CyclicBarrier`的主要作用是在多个线程之间协调执行顺序，并且这些线程之间的协作方式比较复杂。例如，可以使用`CyclicBarrier`来等待多个线程执行完某个阶段的任务后再开始执行下一个阶段的任务。`CyclicBarrier`还支持自定义回调函数，在所有线程到达屏障点后执行特定的操作。

1. 区别
`CountDownLatch`和`CyclicBarrier`的主要区别可以总结如下：

- 计数器的初始值不同：`CountDownLatch`的计数器初始值为一个正整数，`CyclicBarrier`的计数器初始值为一个正整数和一个屏障点。
- 计数器的变化方式不同：`CountDownLatch`的计数器通过`countDown()`方法递减，`CyclicBarrier`的计数器通过`await()`方法递增。
- 等待的线程数量不同：`CountDownLatch`可以等待一个或多个线程完成某个操作，`CyclicBarrier`必须等待多个线程到达屏障点。
- 作用的场景不同：`CountDownLatch`适用于一次性等待多个线程完成某个操作，`CyclicBarrier`适用于多个线程之间协调执行顺序，并且这些线程之间的协作方式比较复杂。

需要注意的是，`CountDownLatch`和`CyclicBarrier`都是一次性的同步工具，一旦计数器的值变为0，就不能再用它们来等待其他线程的到来或执行。如果需要多次等待，则需要使用`Semaphore`或`ReentrantLock`等可重入的同步工具。



### 第9章　Java中的线程池

全局锁



### 第10章　Executor框架
10.4节对FutureTask的使用完全错误


### 第11章　Java并发编程实践
## 跨年摘录（2020–2026 日常笔记聚合，2026-09-23 整理）

### 2020-09
> 《Java并发编程的艺术》中描述类的静态成员变量并不准确，这是因为该作者同Java的虚拟机规范一样把方法区看作了Java堆的一个逻辑部分，所以才把静态成员变量说是堆中的。
> 方法区的别名叫做Non-Heap，即非堆，你从这里就可以理解《Java并发编程的艺术》和《深入理解JVM》之间对类的静态成员变量的解释有所差别了。
> - 20200915：垃圾回收的算法与实现；Java类的静态成员变量是放在方法区中，并不是堆。；《Java并发编程的艺术》中描述类的静态成员变量并不准确，这是因为该作者同Java的虚拟机规范一样把方法区看作了Java堆的一个逻辑部分，所以才把静态成员变量说是堆中的。
> - 20200915：垃圾回收的算法与实现；Java类的静态成员变量是放在方法区中，并不是堆。；《Java并发编程的艺术》中描述类的静态成员变量并不准确，这是因为该作者同Java的虚拟机规范一样把方法区看作了Java堆的一个逻辑部分，所以才把静态成员变量说是堆中的。
> - 202009_week3：- 20200915：垃圾回收的算法与实现；Java类的静态成员变量是放在方法区中，并不是堆。；《Java并发编程的艺术》中描述类的静态成员变量并不准确，这是因为该作者同Java的虚拟机规范一样把方法区看作了Java堆的一个逻辑部分，所以才把静态成员变量说是堆中的。
> - 202009_week3：- 20200915：垃圾回收的算法与实现；Java类的静态成员变量是放在方法区中，并不是堆。；《Java并发编程的艺术》中描述类的静态成员变量并不准确，这是因为该作者同Java的虚拟机规范一样把方法区看作了Java堆的一个逻辑部分，所以才把静态成员变量说是堆中的。

### 2026-03
> 2. 《Java并发编程的艺术》
> 4. 底层优化：补充《Java并发编程的艺术》+《深入理解Java虚拟机》（周志明），理解JVM线程调度、内存屏障，实现并发程序性能优化。


## 精读补写（系统整理，2026-09-23）

### 版本与 ISBN
- **第2版**（最新）：方腾飞、魏鹏、程晓明 著，机械工业出版社，2023-12，**ISBN `978-7-111-73797-1`**（Java核心技术系列，382 页，¥109）。第2版新增/修订超 50%，补充了分布式编程范式。
- 第1版（2015）：**ISBN `978-7-111-50824-3`**，累计印刷 23 次、销量超 10 万册。若笔记中的章节与源码行号与第2版对不上，多半引自第1版（基于 JDK 7/8）。
- 知识主线：并发基础（线程生命周期、中断、ThreadLocal）→ 并发挑战（上下文切换、死锁、资源限制）→ **底层实现原理**（volatile 的 CPU 语义、`synchronized` 在字节码/JVM/CPU 三层如何实现、原子操作的 CAS 与缓存一致性）→ **Java 内存模型**（happens-before、as-if-serial、volatile 与锁的内存语义、final 语义）→ **锁与同步组件**（AQS、ReentrantLock、读写锁、Condition）→ **并发容器**（ConcurrentHashMap、阻塞队列、CopyOnWrite）→ 原子类与工具类 → **线程池与 Executor** → 分布式并发（分布式锁、常见分布式架构）。

### 经典论文与原始文献根基
- **Manson, Pugh, Adve《The Java Memory Model》**(POPL 2005)——JMM 的形式化定义，书中"内存语义"章节的学术源头；配套 **JSR-133**。
- Lamport《Time, Clocks, and the Ordering of Events in a Distributed System》(CACM 1978)——happened-before 概念的最初提出（JMM 借用其名）。
- Michael & Scott《Simple, Fast, and Practical Non-Blocking and Blocking Concurrent Queue Algorithms》(PODC 1996)——`ConcurrentLinkedQueue` 的实现依据。
- Herlihy & Shavit《The Art of Multiprocessor Programming》(2008/2012)——线性一致性、CAS 原语与无锁数据结构的系统教材。
- Doug Lea《Concurrent Programming in Java》(1999) 与 `java.util.concurrent` 的 Javadoc/源码——AQS 与线程池的设计说明（`AbstractQueuedSynchronizer` 论文由 Lea 自述于 Javadoc）。
- **硬件内存模型**：Sewell 等《x86-TSO: A Rigorous and Usable Programmer's Model for x86 Multiprocessors》(CACM 2010)；Alglave/Maranget/Tautschnig《Herding Cats》(TOPLAS 2014)——解释为何 x86 强内存模型下某些重排序"看不到"、ARM/POWER 下会暴露。

### 最新研究与产业进展
- **虚拟线程（Project Loom）**：JDK 21 GA（JEP 444）——平台线程 vs 虚拟线程，"一个请求一线程"重新可行；**结构化并发**（JEP 453 预览）与 Scoped Values（JEP 506）改造并发代码组织方式。这是本书第1/2版尚未覆盖的范式变化。
- **锁优化现状**：偏向锁在 JDK 15 起弃用并移除（JEP 374），笔记中" synchronized 默认走偏向锁"需修正；现代 HotSpot 依赖轻量级锁 + 自适应自旋 + 锁消除/粗化。
- **无锁与内存序**：`VarHandle`（JDK 9+）取代 `Unsafe` 成为内存序控制的官方手段（opaque/acquire/release），对应 C++ 的 memory_order 体系。
- **硬件与语言交叉**：NUMA 感知调度、JDK 21 的 `Generational ZGC` 降低 GC 对并发停顿的影响；Rust/C++ 的内存模型对比有助于理解 release/acquire 语义。

### 常见误区 / 纠错
- "volatile 保证原子性"**错误**——volatile 只保证可见性与单变量读写的原子性（除 long/double 之外在 JDK 5+ 已保证），`i++` 仍非原子；需用 `AtomicInteger` 或锁。
- "synchronized 一定比 Lock 慢"**过时**——JDK 1.6 后两者性能接近，选择依据是功能（可中断、超时、公平性、多条件队列）而非性能神话。
- "happens-before 即时间先后"**错误**——happens-before 是偏序关系，允许重排序，只约束可见性与顺序一致性（对正确同步的程序）。
- 线程池"越大越好"**错误**——受限于 CPU 核数、内存与下游资源；书中第 8/9 章给出的线程池参数化公式应结合压测而非照抄。
