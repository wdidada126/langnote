# javase

https://blog.csdn.net/ye17186/article/details/89467919

从源码中可以看出，线程池的构造函数有7个参数，分别是corePoolSize、maximumPoolSize、keepAliveTime、unit、workQueue、threadFactory、handler。下面会对这7个参数一一解释。
一、corePoolSize 线程池核心线程大小
线程池中会维护一个最小的线程数量，即使这些线程处理空闲状态，他们也不会被销毁，除非设置了allowCoreThreadTimeOut。这里的最小线程数量即是corePoolSize。任务提交到线程池后，首先会检查当前线程数是否达到了corePoolSize，如果没有达到的话，则会创建一个新线程来处理这个任务。
二、maximumPoolSize 线程池最大线程数量
当前线程数达到corePoolSize后，如果继续有任务被提交到线程池，会将任务缓存到工作队列（后面会介绍）中。如果队列也已满，则会去创建一个新线程来出来这个处理。线程池不会无限制的去创建新线程，它会有一个最大线程数量的限制，这个数量即由maximunPoolSize指定。
三、keepAliveTime 空闲线程存活时间
一个线程如果处于空闲状态，并且当前的线程数量大于corePoolSize，那么在指定时间后，这个空闲线程会被销毁，这里的指定时间由keepAliveTime来设定
四、unit 空闲线程存活时间单位
keepAliveTime的计量单位
五、workQueue 工作队列
新任务被提交后，会先进入到此工作队列中，任务调度时再从队列中取出任务。jdk中提供了四种工作队列：
六、threadFactory 线程工厂
创建一个新线程时使用的工厂，可以用来设定线程名、是否为daemon线程等等
七、handler 拒绝策略
当工作队列中的任务已到达最大限制，并且线程池中的线程数量也达到最大限制，这时如果有新任务提交进来，该如何处理呢。这里的拒绝策略，就是解决这个问题的，jdk中提供了4中拒绝策略：
①CallerRunsPolicy
该策略下，在调用者线程中直接执行被拒绝任务的run方法，除非线程池已经shutdown，则直接抛弃任务。
②AbortPolicy
该策略下，直接丢弃任务，并抛出RejectedExecutionException异常。

③DiscardPolicy
该策略下，直接丢弃任务，什么都不做。

④DiscardOldestPolicy
该策略下，抛弃进入队列最早的那个任务，然后尝试把这次拒绝的任务放入队列


Java并发编程中的JUC（java.util.concurrent）包含了一些用于处理并发的类，包括：
1. Locks（锁）：提供了比使用synchronized关键字更加灵活的锁实现，包括ReentrantLock、ReentrantReadWriteLock、StampedLock等。
2. Atomic variables（原子变量）：提供了在多线程环境下进行原子操作的方式，包括AtomicBoolean、AtomicInteger、AtomicLong等。
3. Concurrent collections（并发集合）：提供了一些线程安全的集合类，包括ConcurrentHashMap、ConcurrentSkipListMap、ConcurrentSkipListSet等。
4. Synchronizers（同步器）：提供了一些基础的同步工具类，包括CountDownLatch、CyclicBarrier、Semaphore等。
5. Executors（线程池）：提供了一些创建和管理线程池的工具类，包括Executor、ExecutorService、ThreadPoolExecutor、ScheduledExecutorService等。
6. Others（其他）：还包括一些其他的并发编程相关的类，如CompletableFuture、ForkJoinPool、LockSupport等。

AQS，即AbstractQueuedSynchronizer，是Java中用于构建锁和同步器的一个基础框架，它提供了一个底层的、基于FIFO队列的同步器，开发者可以使用AQS构建基于锁、信号量、计数器等的同步器。
AQS框架的基本思想是，将一个线程的操作转化为一个或多个状态的操作，状态变更后，再将其它线程的操作进行阻塞或唤醒。AQS使用一个FIFO队列来存储等待线程，当线程请求访问某个资源时，如果该资源已经被占用，则将该线程加入到FIFO队列的末尾，然后进入阻塞状态。
AQS框架包含两种同步模式：独占模式和共享模式。独占模式指的是同一时间只能有一个线程获得锁，而共享模式则允许多个线程同时访问同一资源。
AQS框架中的重要类包括：
* AbstractQueuedSynchronizer：AQS的核心类，提供了同步器的核心逻辑和状态管理。
* ReentrantLock：可重入锁，基于AQS实现，支持独占模式。
* ReentrantReadWriteLock：读写锁，基于AQS实现，支持共享模式和独占模式。
* CountDownLatch：计数器，基于AQS实现，用于等待一个或多个操作完成。
* Semaphore：信号量，基于AQS实现，用于限制并发访问的数量。
* Condition：条件变量，基于AQS实现，用于线程间的通信。
使用AQS框架可以构建出高效、灵活、可重入、可中断的同步器，是Java中并发编程的基础之一。


Java 7引入了Fork/Join框架，是一种基于工作窃取算法的任务执行框架，用于处理递归式的并行问题。其核心是在一个大任务中递归地将其拆分成小任务，然后将每个小任务加入到一个队列中等待处理。当一个工作线程处理完自己的任务后，会从其它工作线程的队列中随机挑选一个任务进行处理，这个过程就是工作线程的“窃取”行为。这种工作线程之间的任务相互窃取的算法能够确保各个工作线程的负载基本平衡，提高并发处理能力。
Fork/Join框架主要由下面几个类组成：
1. ForkJoinTask：任务抽象类，实现了future和work-stealing算法；
2. RecursiveTask：继承ForkJoinTask，有返回值的任务；
3. RecursiveAction：继承ForkJoinTask，没有返回值的任务；
4. ForkJoinPool：工作线程的线程池；
5. ForkJoinWorkerThread：工作线程。

Fork/Join框架的使用步骤大致如下：
1. 创建ForkJoinPool；
2. 创建ForkJoinTask（RecursiveTask或RecursiveAction）；
3. 调用ForkJoinPool的submit()方法将任务提交给线程池；
4. 调用ForkJoinTask的join()方法等待任务执行完毕并获取执行结果。

## java17新增api

https://docs.oracle.com/en/java/javase/17/
https://www.oracle.com/cn/news/announcement/oracle-releases-java-17-2021-09-14/

Java 17 是 JDK 17 版本的正式发布，它引入了一些新的 API 和功能。以下是 Java 17 中的一些新增 API 的概述：
1. Sealed Classes (密封类)：Java 17 引入了密封类的概念。密封类用于限制哪些类可以继承或实现它，从而提供更严格的类型层次结构控制。
2. Pattern Matching for Switch (Switch 表达式的模式匹配)：Java 17 扩展了 Switch 表达式，使其支持基于模式的匹配。这使得在 Switch 表达式中可以更方便地进行模式匹配和提取。
3. Sealed Interfaces (密封接口)：除了密封类，Java 17 还引入了密封接口。密封接口可以限制哪些类可以实现它，提供更严格的接口实现控制。
4. Strong Encapsulation for JDK Internals (JDK 内部的强封装)：Java 17 引入了一些机制，以进一步增强 JDK 内部的封装性，减少对内部 API 的直接访问。
5. Sealed JVM (密封的 JVM)：Java 17 引入了密封的 JVM 特性，允许在 JVM 层面对类加载和访问控制进行更严格的限制。
6. Foreign Function & Memory API (外部函数和内存 API)：Java 17 引入了 Foreign Function & Memory API，用于与本地代码进行交互，包括直接访问内存和调用外部函数。
7. Deprecating and Removing Features：Java 17 标记了一些过时（Deprecated）的 API，并删除了一些不再建议使用的功能。
请注意，以上只是 Java 17 中一些新增 API 的概述，并不是完整的列表。对于更详细和全面的信息，建议查阅 Java 17 的官方文档和发布说明。
Java 17 的官方文档和发布说明。
Java 18于2022年3月发布,主要新增了以下几个方面的API:

1. 并发 - Structured Concurrency 提供了结构化并发模型的支持,可以通过Scope控制异步任务的生命周期。
2. 集合 - Map和Set新增了toMap/toSet/toUnmodifiableMap/toUnmodifiableSet等集合转换方法。
3. 字符串 - String新增了isBlank/lines/strip/stripLeading/stripTrailing等字符串处理方法。
4. I/O - FileSystems新增了读取文件树的walkFileTree方法。
5. 工具类 - Records提供了方便创建只有getter方法的记录类的支持。
6. JVM - 增强了对 Foreign Memory Access 和虚拟线程的支持。
7. HTTP客户端 - HttpClient API更新到9.1版本。
8. 预览特性 - 新增Vector API和Foreign Linker API等。
此外还包含大量的安全、稳定性和bug修复等改进。

综上,Java 18对并发、集合、字符串、I/O等方面都有很实用的增强,以及对未来特性的预览支持。这些新API可以帮助开发者编写更清晰、高效的Java程序。


### sql



## Objects

java.util.Objects#isNull
![java_se_Objects](../imgs/javase/java_se_Objects.png)



ResultSetMetaData  缩写rsmd

java.sql.ResultSetMetaData

是接口



## Collectors

java.util.stream.Collectors



toCollection()

toList()

toSet()

counting()





Collectors.toCollection(TreeSet::new)

Collectors.joining(", ")

Collectors.summingInt(Employee::getSalary)

Collectors.groupingBy(Employee::getDepartment)



Map<Department, Integer> totalByDept      = employees.stream()                 .collect(Collectors.groupingBy(Employee::getDepartment,                                                Collectors.summingInt(Employee::getSalary)));



Map<Boolean, List<Student>> passingFailing =      students.stream().collect(Collectors.partitioningBy(s -> s.getGrade() >= PASS_THRESHOLD));



`Collection.toList()` 方法是 `java.util.stream.Collectors` 类中的一个静态方法，它用于将流（Stream）中的元素收集到一个列表中。

`java.util.stream.Collectors` 类是 Java 8 引入的，它提供了许多用于收集流元素的静态方法。这些方法可以与流的 `collect()` 操作一起使用，用于执行各种集合操作，如收集到列表、集合、映射等。

要使用 `toList()` 方法，需要在代码中导入 `Collectors` 类：

```java
import java.util.stream.Collectors;
```

然后，可以将流中的元素收集到列表中，如下所示：

```java
List<String> list = stream.collect(Collectors.toList());
```

在上述示例中，`stream` 是一个流对象，通过调用 `collect()` 方法并传递 `Collectors.toList()`，将流中的元素收集到一个名为 `list` 的列表中。

需要注意的是，`toList()` 方法返回的是一个 `List` 实现类的实例，具体的实现类取决于流的来源和上下文。一般情况下，返回的是 `ArrayList` 或 `LinkedList` 的实例。

这种方式可以将流中的元素转换为列表，方便进行后续的操作和处理。
