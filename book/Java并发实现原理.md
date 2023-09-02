Java并发实现原理

https://book.douban.com/subject/35013531/
ISBN: 9787121379727
出版年: 2020-4
《Java并发实现原理：JDK源码剖析》全面而系统地剖析了Java Concurrent包中的每一个部分，对并发的实现原理进行了深刻的探讨。全书分为8章，第1章从最基础的多线程知识讲起，理清多线程中容易误解的知识点，探究背后的原理，包括内存重排序、happen-before、内存屏障等；第2~8章，从简单到复杂，逐个剖析Concurrent包的每个部分，包括原子类、锁、同步工具类、并发容器、线程池、ForkJoinPool、CompletableFuture共7个部分。本书遵循层层递进的逻辑，后一章建立在前一章的知识点基础之上，建议读者由浅入深，逐步深入阅读。
《Java并发实现原理：JDK源码剖析》适合有一定Java开发经验的工程师、架构师阅读。通过本书，读者可以对多线程编程形成一个“深刻而直观”的认识，而不是再仅仅停留在概念和理论层面。


第1章 多线程基础 / 1
1.1 线程的优雅关闭 / 1
1.1.1 stop与destory函数 / 1
1.1.2 守护线程 / 1
1.1.3 设置关闭的标志位 / 2
1.2 InterruptedException与interrupt()函数 / 3
1.2.1 什么情况下会抛出Interrupted异常 / 3
1.2.2 轻量级阻塞与重量级阻塞 / 4
1.2.3 t.isInterrupted()与Thread.interrupted()的区别 / 5
1.3 synchronized关键字 / 5
1.3.1 锁的对象是什么 / 5
1.3.2 锁的本质是什么 / 6
1.3.3 synchronized实现原理 / 7
1.4 wait与notify / 7
1.4.1 生产者−消费者模型 / 7
1.4.2 为什么必须和synchronized一起使用 / 8
1.4.3 为什么wait()的时候必须释放锁 / 9
1.4.4 wait()与notify()的问题 / 10
1.5 volatile关键字 / 11
1.5.1 64位写入的原子性（Half Write） / 11
1.5.2 内存可见性 / 11
1.5.3 重排序：DCL问题 / 12
1.6 JMM与happen-before / 13
1.6.1 为什么会存在“内存可见性”问题 / 13
1.6.2 重排序与内存可见性的关系 / 15
1.6.3 as-if-serial语义 / 16
1.6.4 happen-before是什么 / 17
1.6.5 happen-before的传递性 / 18
1.6.6 C++中的volatile关键字 / 19
1.6.7 JSR-133对volatile语义的增强 / 20
1.7 内存屏障 / 20
1.7.1 Linux中的内存屏障 / 21
1.7.2 JDK中的内存屏障 / 23
1.7.3 volatile实现原理 / 24
1.8 final关键字 / 25
1.8.1 构造函数溢出问题 / 25
1.8.2 final的happen-before语义 / 26
1.8.3 happen-before规则总结 / 26
1.9 综合应用：无锁编程 / 27
1.9.1 一写一读的无锁队列：内存屏障 / 27
1.9.2 一写多读的无锁队列：volatile关键字 / 27
1.9.3 多写多读的无锁队列：CAS / 28
1.9.4 无锁栈 / 28
1.9.5 无锁链表 / 28
第2章 Atomic类 / 29
2.1 AtomicInteger和AtomicLong / 29
2.1.1 悲观锁与乐观锁 / 31
2.1.2 Unsafe 的CAS详解 / 31
2.1.3 自旋与阻塞 / 32
2.2 AtomicBoolean和AtomicReference / 33
2.2.1 为什么需要AtomicBoolean / 33
2.2.2 如何支持boolean和double类型 / 33
2.3 AtomicStampedReference和AtomicMarkable Reference / 34
2.3.1 ABA问题与解决办法 / 34
2.3.2 为什么没有AtomicStampedInteger或AtomictStampedLong / 35
2.3.3 AtomicMarkableReference / 36
2.4 AtomicIntegerFieldUpdater、AtomicLongFieldUpdater和AtomicReferenceField Updater / 37
2.4.1 为什么需要AtomicXXXFieldUpdater / 37
2.4.2 限制条件 / 38
2.5 AtomicIntegerArray、AtomicLongArray和AtomicReferenceArray / 38
2.5.1 使用方式 / 38
2.5.2 实现原理 / 39
2.6 Striped64与LongAdder / 40
2.6.1 LongAdder原理 / 40
2.6.2 最终一致性 / 41
2.6.3 伪共享与缓存行填充 / 42
2.6.4 LongAdder核心实现 / 43
2.6.5 LongAccumulator / 47
2.6.6 DoubleAdder与DoubleAccumulator / 47
第3章 Lock与Condition / 49
3.1 互斥锁 / 49
3.1.1 锁的可重入性 / 49
3.1.2 类继承层次 / 49
3.1.3 锁的公平性vs.非公平性 / 51
3.1.4 锁实现的基本原理 / 51
3.1.5 公平与非公平的lock()实现差异 / 53
3.1.6 阻塞队列与唤醒机制 / 55
3.1.7 unlock()实现分析 / 58
3.1.8 lockInterruptibly()实现分析 / 59
3.1.9 tryLock()实现分析 / 60
3.2 读写锁 / 60
3.2.1 类继承层次 / 60
3.2.2 读写锁实现的基本原理 / 61
3.2.3 AQS的两对模板方法 / 62
3.2.4 WriteLock公平vs.非公平实现 / 65
3.2.5 ReadLock公平vs.非公平实现 / 67
3.3 Condition / 68
3.3.1 Condition与Lock的关系 / 68
3.3.2 Condition的使用场景 / 69
3.3.3 Condition实现原理 / 71
3.3.4 await()实现分析 / 72
3.3.5 awaitUninterruptibly()实现分析 / 73
3.3.6 notify()实现分析 / 74
3.4 StampedLock / 75
3.4.1 为什么引入StampedLock / 75
3.4.2 使用场景 / 75
3.4.3 “乐观读”的实现原理 / 77
3.4.4 悲观读/写：“阻塞”与“自旋”策略实现差异 / 78
第4章 同步工具类 / 83
4.1 Semaphore / 83
4.2 CountDownLatch / 84
4.2.1 CountDownLatch使用场景 / 84
4.2.2 await()实现分析 / 85
4.2.3 countDown()实现分析 / 85
4.3 CyclicBarrier / 86
4.3.1 CyclicBarrier使用场景 / 86
4.3.2 CyclicBarrier实现原理 / 87
4.4 Exchanger / 90
4.4.1 Exchanger使用场景 / 90
4.4.2 Exchanger 实现原理 / 91
4.4.3 exchange(V x)实现分析 / 92
4.5 Phaser / 94
4.5.1 用Phaser替代CyclicBarrier和CountDownLatch / 94
4.5.2 Phaser新特性 / 95
4.5.3 state变量解析 / 96
4.5.4 阻塞与唤醒（Treiber Stack） / 98
4.5.5 arrive()函数分析 / 99
4.5.6 awaitAdvance()函数分析 / 101
第5章 并发容器 / 104
5.1 BlockingQueue / 104
5.1.1 ArrayBlockingQueue / 105
5.1.2 LinkedBlockingQueue / 106
5.1.3 PriorityBlockingQueue / 109
5.1.4 DelayQueue / 111
5.1.5 SynchronousQueue / 113
5.2 BlockingDeque / 121
5.3 CopyOnWrite / 123
5.3.1 CopyOnWriteArrayList / 123
5.3.2 CopyOnWriteArraySet / 124
5.4 ConcurrentLinkedQueue/ Deque / 125
5.5 ConcurrentHashMap / 130
5.5.1 JDK 7中的实现方式 / 130
5.5.2 JDK 8中的实现方式 / 138
5.6 ConcurrentSkipListMap/Set / 152
5.6.1 ConcurrentSkipListMap / 153
5.6.2 ConcurrentSkipListSet / 162
第6章 线程池与Future / 163
6.1 线程池的实现原理 / 163
6.2 线程池的类继承体系 / 164
6.3 ThreadPoolExecutor / 165
6.3.1 核心数据结构 / 165
6.3.2 核心配置参数解释 / 165
6.3.3 线程池的优雅关闭 / 167
6.3.4 任务的提交过程分析 / 172
6.3.5 任务的执行过程分析 / 174
6.3.6 线程池的4种拒绝策略 / 179
6.4 Callable与Future / 180
6.5 ScheduledThreadPool Executor / 183
6.5.1 延迟执行和周期性执行的原理 / 184
6.5.2 延迟执行 / 184
6.5.3 周期性执行 / 185
6.6 Executors工具类 / 188
第7章 ForkJoinPool / 190
7.1 ForkJoinPool用法 / 190
7.2 核心数据结构 / 193
7.3 工作窃取队列 / 195
7.4 ForkJoinPool状态控制 / 198
7.4.1 状态变量ctl解析 / 198
7.4.2 阻塞栈Treiber Stack / 200
7.4.3 ctl变量的初始值 / 201
7.4.4 ForkJoinWorkerThread状态与个数分析 / 201
7.5 Worker线程的阻塞-唤醒机制 / 202
7.5.1 阻塞–入栈 / 202
7.5.2 唤醒–出栈 / 204
7.6 任务的提交过程分析 / 205
7.6.1 内部提交任务pushTask / 206
7.6.2 外部提交任务addSubmission / 206
7.7 工作窃取算法：任务的执行过程分析 / 207
7.7.1 顺序锁 SeqLock / 209
7.7.2 scanGuard解析 / 210
7.8 ForkJoinTask的fork/join / 212
7.8.1 fork / 213
7.8.2 join的层层嵌套 / 213
7.9 ForkJoinPool的优雅关闭 / 222
7.9.1 关键的terminate变量 / 222
7.9.2 shutdown()与shutdownNow()的区别 / 223
第8章 CompletableFuture / 226
8.1 CompletableFuture用法 / 226
8.1.1 最简单的用法 / 226
8.1.2 提交任务：runAsync与supplyAsync / 226
8.1.3 链式的CompletableFuture：thenRun、thenAccept和thenApply / 227
8.1.4 CompletableFuture的组合：thenCompose与thenCombine / 229
8.1.5 任意个CompletableFuture的组合 / 231
8.2 四种任务原型 / 233
8.3 CompletionStage接口 / 233
8.4 CompletableFuture内部原理 / 234
8.4.1 CompletableFuture的构造：ForkJoinPool / 234
8.4.2 任务类型的适配 / 235
8.4.3 任务的链式执行过程分析 / 237
8.4.4 thenApply与thenApplyAsync的区别 / 241
8.5 任务的网状执行：有向无环图 / 242
8.6 allOf内部的计算图分析 / 244