# juc

Java Collections Framework

全局变量存储

text data

方法区

永久代元数据区  思考，元数据描述数据的数据，这个元数据区是干啥的

堆
栈

堆内存回收

年轻代 老年代

Edan

Link load 初始化

load verify prepare

AQS Status

CompareAndSet

Synchronized

AtomicBoolean
AtomicInteger
AtomicLong
LongAddr

Lock Condiction
lock.readLock
writeLock

Es
ThreadLocal
remove()

### doc

独占锁和共享锁

[java并发-独占锁与共享锁](https://blog.csdn.net/wojiushiwo945you/article/details/42292999)

锁的独占与共享

java并发包提供的加锁模式分为独占锁和共享锁，独占锁模式下，每次只能有一个线程能持有锁，ReentrantLock就是以独占方式实现的互斥锁。

共享锁，则允许多个线程同时获取锁，并发访问共享资源，如：ReadWriteLock。

AQS的内部类Node定义了两个常量SHARED和EXCLUSIVE，他们分别标识AQS队列中等待线程的锁获取模式。
很显然，独占锁是一种悲观保守的加锁策略，它避免了读/读冲突，如果某个只读线程获取锁，则其他读线程都只能等待，这种情况下就限制了不必要的并发性，因为读操作并不会影响数据的一致性。共享锁则是一种乐观锁，它放宽了加锁策略，允许多个执行读操作的线程同时访问共享资源。 java的并发包中提供了ReadWriteLock，读-写锁。它允许一个资源可以被多个读操作访问，或者被一个写操作访问，但两者不能同时进行。

[不可不说的Java“锁”事](https://tech.meituan.com/2018/11/15/java-lock.html)

[java 多线程总结图](https://www.processon.com/view/link/5b71947ce4b0be50eadcdad0)





Object类

构造函数调用父类

this

super

java.utils.concurrent

java并发包提供的加锁模式分为独占锁和共享锁，独占锁模式下，每次只能有一个线程能持有锁，ReentrantLock就是以独占方式实现的互斥锁。共享锁，则允许多个线程同时获取锁，并发访问?共享资源，如：ReadWriteLock。AQS的内部类Node定义了两个常量SHARED和EXCLUSIVE，他们分别标识?AQS队列中等待线程的锁获取模式。
很显然，独占锁是一种悲观保守的加锁策略，它避免了读/读冲突，如果某个只读线程获取锁，则其他读线程都只能等待，这种情况下就限制了不必要的并发性，因为读操作并不会影响数据的一致性。共享锁则是一种乐观锁，它放宽了加锁策略，允许多个执行读操作的线程同时访问共享资源。 java的并发包中提供了ReadWriteLock，读-写锁。它允许一个资源可以被多个读操作访问，或者被一个?写操作访问，但两者不能同时进行。

[不可不说的Java“锁”事](https://tech.meituan.com/2018/11/15/java-lock.html)

[java 多线程总结图](https://www.processon.com/view/link/5b71947ce4b0be50eadcdad0#map)

https://blog.csdn.net/luoweifu/article/details/46495045

Java?Logging?API提供了七个日志级别用来控制输出。这七个级别分别是：

级别
SEVERE-WARNING-INFO-CONFIG-FINE-FINER-FINEST
调用方法
severe()-warning()-info()-config()-fine()-finer()-finest()
含意 严重 警告 信息 配置 良好 较好 最好