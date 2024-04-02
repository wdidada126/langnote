# java aqs

`java.util.concurrent.Phaser` 和 `java.util.concurrent.Exchanger` 是 Java 并发包中提供的两个工具类，它们用于协调线程之间的同步和通信。虽然它们并没有直接使用 `AbstractQueuedSynchronizer`（AQS），但它们仍然能够进行线程同步和等待操作，这是因为它们采用了其他的并发控制机制。
`Phaser` 类是一种用于控制多个线程分阶段共同执行的同步器。它内部使用了基于 CAS 操作的整数变量来控制不同阶段的到达。`Exchanger` 类则是一种用于两个线程间进行数据交换的同步器。它利用了 CAS 和自旋等待的方式来实现线程之间的数据交换。
尽管它们没有直接使用AQS，但它们仍然借鉴了AQS的一些设计原则和思想，利用了并发编程中的其他机制来实现线程间的同步和等待。Java 并发包提供了多种工具和类来实现不同的并发控制需求，`Phaser` 和 `Exchanger` 是其中的两个例子，它们通过不同的机制实现了线程的同步和通信功能。

在AQS中维持了一个单一的状态信息state, 可以通过 getState、setState、compareAndSetState 函数修改其值。对于 ReentrantLock 的实现来说，state 可以用来表示当前线程获取锁的可重入次数 ；对于读写锁 ReentrantReadWriteLock 来说，state 的高16位表示读状态，也就是获取该读锁的次数，低16位表示获取到写锁的线程的可重入次数；对于Semaphore来说，state用来表示当前可用信号的个数；对于 CountDownlatch来说，state 用来表示计数器当前的值。

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

java.util.concurrent.locks.AbstractQueuedSynchronizer#setState()
java.util.concurrent.locks.AbstractQueuedSynchronizer#getState()
boolean compareAndSetState(int expect, int update)
java.util.concurrent.locks.AbstractQueuedSynchronizer#acquireSharedInterruptibly()
java.util.concurrent.locks.AbstractQueuedSynchronizer#tryAcquireSharedNanos()

aqs在java标准库中的应用
CountDownLatch cdl
ThreadPoolExecutor tpe
ReentrantLock rl
ReentrantReadWriteLock rrwl

Semaphore 

FairSync unFairSync

```
AbstractOwnableSynchronizer (java.util.concurrent.locks)
    AbstractQueuedSynchronizer (java.util.concurrent.locks)
        Sync in CountDownLatch (java.util.concurrent)
        Worker in ThreadPoolExecutor (java.util.concurrent)
        Sync in ReentrantLock (java.util.concurrent.locks)
            FairSync in ReentrantLock (java.util.concurrent.locks)
            NonfairSync in ReentrantLock (java.util.concurrent.locks)
        Sync in ReentrantReadWriteLock (java.util.concurrent.locks)
            FairSync in ReentrantReadWriteLock (java.util.concurrent.locks)
            NonfairSync in ReentrantReadWriteLock (java.util.concurrent.locks)
        Sync in Semaphore (java.util.concurrent)
            FairSync in Semaphore (java.util.concurrent)
            NonfairSync in Semaphore (java.util.concurrent)
    AbstractQueuedLongSynchronizer (java.util.concurrent.locks)
```

aos
aqls
AbstractQueuedSynchronizer

提供了一个基于FIFO队列，可以用于构建锁或者其他相关同步装置的基础框架。该同步器（以下简称同步器）利用了一个int来表示状态，期望它能够成为实现大部分同步需求的基础。使用的方法是继承，子类通过继承同步器并需要实现它的方法来管理其状态，管理的方式就是通过类似acquire和release的方式来操纵状态。然而多线程环境中对状态的操纵必须确保原子性，因此子类对于状态的把握，需要使用这个同步器提供的以下三个方法对状态进行操作：

- java.util.concurrent.locks.AbstractQueuedSynchronizer.getState()
- java.util.concurrent.locks.AbstractQueuedSynchronizer.setState(int)
- java.util.concurrent.locks.AbstractQueuedSynchronizer.compareAndSetState(int, int)

子类推荐被定义为自定义同步装置的内部类，同步器自身没有实现任何同步接口，它仅仅是定义了若干acquire之类的方法来供使用。该同步器即可以作为排他模式也可以作为共享模式，当它被定义为一个排他模式时，其他线程对其的获取就被阻止，而共享模式对于多个线程获取都可以成功。

https://www.cnblogs.com/leesf456/p/5350186.html

子类
public class java.util.concurrent.locks.AbstractQueuedSynchronizer.ConditionObject

static final class Node

private static final Unsafe unsafe = Unsafe.getUnsafe();
用了

AtomicBoolean是Java中的一个类，用于在多线程环境中安全地处理布尔值的原子操作。它的主要应用场景包括原子性地更新标志位，保证在高并发的情况下只有一个线程能访问或修改这个属性值。由于AtomicBoolean提供了原子操作，它能够确保在并发处理时，状态的改变不会被其他线程打断，从而避免了数据不一致的问题。

然而，尽管AtomicBoolean在并发编程中非常有用，但它并不能替代普通的Boolean类型。原因主要有以下几点：

语义差异：AtomicBoolean和Boolean在语义上有所不同。Boolean是Java的基本数据类型，用于表示逻辑上的真或假。而AtomicBoolean则是一个类，它的主要目的是在多线程环境中提供安全的布尔值操作。使用场景：Boolean类型在Java中被广泛使用，不仅用于逻辑判断，还可以作为方法的返回类型、类的成员变量等。而AtomicBoolean则主要用于需要原子性操作的并发场景，它的使用范围相对狭窄。性能开销：由于AtomicBoolean提供了原子操作，这通常意味着更高的性能开销。在不需要并发控制的场景中，使用AtomicBoolean可能会引入不必要的性能损失。
API限制：AtomicBoolean的API与Boolean的API并不完全相同。虽然它们都有类似的方法来获取和设置值，但AtomicBoolean还提供了额外的原子操作方法，如compareAndSet()。因此，在某些情况下，直接替换可能会导致API使用上的不便。
综上所述，尽管AtomicBoolean在某些特定场景下非常有用，但它并不能完全替代Boolean类型。在编写代码时，应根据具体需求选择合适的类型。在需要处理并发问题时，可以考虑使用AtomicBoolean；而在其他场景下，使用普通的Boolean类型可能更为合适。

private static final long valueOffset;
private volatile int value;
两个成员变量


