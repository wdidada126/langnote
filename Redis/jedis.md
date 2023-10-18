# jedis

lettuce

Lettuce是一个高级Redis客户端，它为Redis提供了全面的支持，包括事务、流、发布/订阅、Lua脚本、分片和集群等。对于分布式锁的封装和防止锁执行超时，Lettuce提供了相关的机制。

使用RedisMutex进行分布式锁封装: Lettuce中RedisMutex是一个可重入锁，它基于Redis的SETNX实现。这是一个简单的使用例子：

可重入锁  "Reentrant Lock"。，又被称为递归锁，是一种同步辅助类。其核心特性是，当一个线程已经获取了某个锁，它仍然可以再次获取该锁而不会被阻塞。换言之，拥有该锁的线程可以多次进入自己已经拥有的锁的同步代码块儿。

在Java中，我们可以通过Lock接口中的lock()、lockInterruptibly()和tryLock()等方法来操作锁。这三种方法在处理锁的获取时各有不同的行为表现：
- 当锁空闲时，线程可以直接获取锁并返回，同时设置锁持有者数量为1；
- 如果当前线程已经持有锁，那么它可以直接获取锁并返回，同时锁持有者数量递增1；
- 如果其他线程已经持有锁，那么当前线程会进入等待状态，直至获取到锁为止。

值得注意的是，可重入锁的操作粒度是“线程”，而不是调用。这就意味着，如果一个线程在执行一个方法时已经获取了该锁，那么在这个方法中尝试再次获取该锁时，是可以成功的。这样的设计可以降低锁的开销，提高程序的并发性能。

```java
RedisMutex redisMutex = new RedisMutex(redisClient, "my_lock");  
  
// 获取锁  
redisMutex.lock();  
try {  
    // 在此处执行需要同步的代码  
} finally {  
    // 最后不要忘记释放锁  
    redisMutex.unlock();  
}
```
设置锁的超时时间：在Lettuce中，你可以通过setLockTimeout方法来设置获取锁的超时时间。如果超过这个时间还获取不到锁，那么将会抛出TimeoutException。

```java
redisMutex.setLockTimeout(5000); // 设置超时时间为5秒
```
watch功能：Lettuce中的RedisMutex有一个watch方法，这个方法可以在你尝试获取锁的时候，同时对一些key进行watch。如果这些key的值在持有锁的过程中发生了改变，那么在释放锁的时候，会抛出MutationDetectedException。你可以通过这个异常来感知到锁所保护的资源发生了变化。这是一个简单的使用例子：

```java
RedisMutex redisMutex = new RedisMutex(redisClient, "my_lock");  
redisMutex.watch("my_lock_data".getBytes());  
  
redisMutex.lock();  
try {  
    // 在此处执行需要同步的代码，如果这个过程中"my_lock_data"的值发生了改变，那么在释放锁的时候将会抛出MutationDetectedException  
} finally {  
    redisMutex.unlock();  
}
```
需要注意的是，Lettuce的RedisMutex并没有提供直接的watch功能（即观察者模式，主动通知观察者），它只能在你尝试获取锁的时候watch一些key。如果这些key的值在持有锁的过程中发生了改变，那么它会抛出一个异常。如果你需要实现一个真正的观察者模式，你可能需要在你的代码中自行实现。


Jedis操作主要涉及到的类：JedisPool、Jedis、Client、BinaryClient、Connection等，下面是对其处理过程的简要记录。
1、Connection类是使用原生的Socket进行连接
https://blog.csdn.net/meaijojo/article/details/82903553





Jedis
客户端三类
Sentinel
Cluster

