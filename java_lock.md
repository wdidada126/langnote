# java lock



同步器

AbstractOwnableSynchronizer (java.util.concurrent.locks)
    AbstractQueuedSynchronizer (java.util.concurrent.locks)
        NonReentrantLock (org.jboss.netty.util.internal)
        Sync in CountDownLatch (java.util.concurrent)
        Worker in ThreadPoolExecutor (java.util.concurrent)
        Sync in ReentrantLock (java.util.concurrent.locks)
        Sync in ReentrantReadWriteLock (java.util.concurrent.locks)
        Sync in Semaphore (java.util.concurrent)
    AbstractQueuedLongSynchronizer (java.util.concurrent.locks)


java.util.concurrent.locks.Lock
java 5新增

lock
lockInterruptibly
tryLock
tryLock
unlock
newCondition



Condition
await
awaitUninterruptibly
awaitNanos
await
awaitUntil
signal
signalAll

实现类
ConditionObject in AbstractQueuedLongSynchronizer (java.util.concurrent.locks)
ConditionObject in AbstractQueuedSynchronizer (java.util.concurrent.locks)


ReentrantLock


自旋锁
自旋锁是采用让当前线程不停地的在循环体内执行实现的，当循环的条件被其他线程改变时才能进入临界区。

JDK里面自旋锁的实现有 SynchronousQueue  和 LinkedTransferQueue。  本文只是自己对源码的简单理解。

先说公平锁，先等待的线程先获得数据。SynchronousQueue的内部类TransferQueue实现了公平锁。


TransferQueue接口

继承阻塞队列接口

tryTransfer
transfer
tryTransfer
hasWaitingConsumer

实现类LinkedTransferQueue


