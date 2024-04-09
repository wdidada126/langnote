# javaguide

https://javaguide.cn/home.html#%E5%BF%85%E7%9C%8B%E4%B8%93%E6%A0%8F

https://github.com/Snailclimb/JavaGuide

https://javaguide.cn/open-source-project/

1、PDF面试资料汇总: https://www.aliyundrive.com/s/5CdbBZ8yYuS 提取码: 26zv

2、《Java面试指北》：https://mp.weixin.qq.com/s/YE9-G8Klsl3EmM-uaGA_NQ


准备技术面试的同学一定要定期复习（自测的方式非常好）



对于技术八股文来说，尽量不要死记硬背，这种方式非常枯燥且对自身能力提升有限！但是！想要一点不背是不太现实的，只是说要结合实际应用场景和实战来理解记忆。

我一直觉得面试八股文最好是和实际应用场景和实战相结合。很多同学现在的方向都错了，上来就是直接背八股文，硬生生学成了文科，那当然无趣了。

举个例子：你的项目中需要用到Redis来做缓存，你对照着官网简单了解并实践了简单使用Redis之后，你去看了Redis对应的八股文。你发现Redis可以用来做限流、分布式锁，于是你去在项目中实践了一下并掌握了对应的八股文。紧接着，你又发现Redis内存不够用的情况下，还能使用Redis Cluster来解决，于是你就又去实践了一下并掌握了对应的八股文。

而且，面试中有水平的面试官都是根据你的项目经历来顺带着问一些技术八股文。

举个例子：你的项目用到了消息队列，那面试官可能就会问你：为什么使用消息队列？项目中什么模块用到了消息队列？如何保证消息不丢失？如何保证消息的顺序性?（结合你使用的具体的消息队列来准备）……。

一定要记住你的主要目标是理解和记关键词，而不是像背课文一样一字一句地记下来！


Java语言并没有直接实现CAS，CAS相关的实现是通过C++内联汇编的形式实现的（JNI调用）。因此，CAS的具体实现和操作系统以及CPU都有关系。

# 并发编程

## Java并发常见面试题总结（上）


## Java并发常见面试题总结（中）

### synchronized
构造方法不能使用 synchronized 关键字修饰。

## Java并发常见面试题总结（下）



### 乐观锁和悲观锁详解
像 Java 中synchronized和ReentrantLock等独占锁就是悲观锁思想的实现。


具体方法可以使用版本号机制或 CAS 算法。
像 Java 中java.util.concurrent.atomic包下面的原子变量类（比如AtomicInteger、LongAdder）就是使用了乐观锁的一种实现方式 CAS 实现的。

### JMM（Java 内存模型）详解
### Java 线程池详解
### Java 线程池最佳实践
### Java 常见并发容器总结
### AQS 详解
### Atomic 原子类总结
### ThreadLocal 详解
### CompletableFuture 详解
### 虚拟线程极简入门



mysql索引下推原理
server过滤，改成enginer层过滤
https://javaguide.cn/database/mysql/mysql-index.html#%E7%B4%A2%E5%BC%95%E4%B8%8B%E6%8E%A8



Redis 5 种基本数据类型对应的底层数据结构
https://javaguide.cn/database/redis/redis-data-structures-01.html


https://javaguide.cn/database/mysql/mysql-questions-01.html#datetime-%E5%92%8C-timestamp-%E7%9A%84%E5%8C%BA%E5%88%AB%E6%98%AF%E4%BB%80%E4%B9%88

sql里面，null跟''


https://javaguide.cn/cs-basics/operating-system/operating-system-basic-questions-01.html#%E8%BF%9B%E7%A8%8B%E9%97%B4%E7%9A%84%E9%80%9A%E4%BF%A1%E6%96%B9%E5%BC%8F%E6%9C%89%E5%93%AA%E4%BA%9B

