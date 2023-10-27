# AQS

`java.util.concurrent.Phaser` 和 `java.util.concurrent.Exchanger` 是 Java 并发包中提供的两个工具类，它们用于协调线程之间的同步和通信。虽然它们并没有直接使用 `AbstractQueuedSynchronizer`（AQS），但它们仍然能够进行线程同步和等待操作，这是因为它们采用了其他的并发控制机制。
`Phaser` 类是一种用于控制多个线程分阶段共同执行的同步器。它内部使用了基于 CAS 操作的整数变量来控制不同阶段的到达。`Exchanger` 类则是一种用于两个线程间进行数据交换的同步器。它利用了 CAS 和自旋等待的方式来实现线程之间的数据交换。
尽管它们没有直接使用 AQS，但它们仍然借鉴了 AQS 的一些设计原则和思想，利用了并发编程中的其他机制来实现线程间的同步和等待。Java 并发包提供了多种工具和类来实现不同的并发控制需求，`Phaser` 和 `Exchanger` 是其中的两个例子，它们通过不同的机制实现了线程的同步和通信功能。


在 AQS 中维持了一个单一的状态信息 state, 可以通过 getState、setState、
compareAndSetState 函数修改其值。对于 ReentrantLock 的实现来说，state 可以用来表示
当前线程获取锁的可重入次数 ；对于读写锁 ReentrantReadWriteLock 来说，state 的高16
位表示读状态，也就是获取该读锁的次数，低16位表示获取到写锁的线程的可重入次数；
对于Semaphore来说，state用来表示当前可用信号的个数；对于 CountDownlatch来说，
state 用来表示计数器当前的值。

java.util.concurrent.Phaser
java.util.concurrent.Exchanger<V>

CLH
AQS内部维护着一个FIFO队列,该队列就是CLH同步队列

AQS（AbstractQueuedSynchronizer）和 CLH（Craig, Landin, and Hagersten）队列是Java并发编程中的两个重要概念，用于实现同步器和自旋锁。尽管它们最初是在Java中引入的，但其他编程语言中也可以找到类似的实现或相似的概念。
在其他编程语言中，也有类似的同步器和自旋锁的实现。例如，在C++中，可以使用互斥锁、条件变量和原子操作等机制来实现类似于AQS和CLH队列的功能。在C#中，也可以利用Monitor类、Mutex类和Semaphore类等来实现类似的功能。在其他编程语言中，通常会提供类似的并发控制机制，用于管理线程之间的同步和通信。
尽管具体的实现细节可能有所不同，但这些编程语言通常都提供了一些通用的并发控制机制，用于管理共享资源的访问和操作。具体的实现取决于编程语言本身的特性和设计理念，可能会有不同的接口和语法，但基本的并发编程概念和原理通常是类似的。

AQS子类

AQS子类
ThreadPoolExecutor.Work

java.util.concurrent.locks.AbstractQueuedSynchronizer.Node

ExclusiveNode extends Node
SharedNode extends Node
ConditionNode extends Node

CLH queue

java.util.concurrent.locks.AbstractQueuedSynchronizer#setState

java.util.concurrent.locks.AbstractQueuedSynchronizer#getState

boolean compareAndSetState(int expect, int update)

java.util.concurrent.locks.AbstractQueuedSynchronizer#acquireSharedInterruptibly

java.util.concurrent.locks.AbstractQueuedSynchronizer#tryAcquireSharedNanos

