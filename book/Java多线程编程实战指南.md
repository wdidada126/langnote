# Java多线程编程实战指南

https://book.douban.com/subject/27034721/ 核心篇

https://book.douban.com/subject/26642317/ 设计模式篇

黄文海，2004年开始从事软件开发工作，近几年从事软件项目管理工作。在其工作过程中积累了丰富的技术指导经验和企业内部培训经验。曾在InfoQ中文站和IBM developerWorks上发表过十几篇技术、项目管理文章。

## 第一部分 多线程编程基础

## Chap.1

Thread Runnable

void join() 等待相应的线程运行结束 线程A调用线程B的join方法，那么线程A的运行会被暂停，直到线程B运行结束
static void 

#### Chap.2 多线程编程的目标与挑战

串行并发并行

二维表分析法 线程安全性 原子性 可见性 有序性


- 原子性
- 可见性
- 有序性


控制访问
锁 lock
cas（基于硬件的 内存和CPU）

共享变量更新后，其他线程不知道（对更新后的值不可见）

UseCompressedOops
http://shzhangji.com/cnblogs/2015/06/25/compressed-oops-in-the-hotspot-jvm/

#### Chap.3 线程同步



### Chap. 4 玩转线程

#### Chap.5 线程间协作

线程间协作



wait

notify

notifyAll



CountDownLatch 



CyclicBarrier

构造函数传入int，等待整数个await()

需要注意的是，`CyclicBarrier`只能被使用一次，一旦所有线程都通过了栅栏，栅栏就会被重置。如果需要多次使用栅栏，需要创建多个`CyclicBarrier`对象。



Semaphore





Exchanger 





#### Chap.6 保障线程安全的设计技术



#### Chap.7  线程的活性故障

线程死锁

#### Chap.8  线程管理

线程组



线程池监控

#### Chap.9 Java异步编程

异步编程



实用工具类Executors



CompletionService 



FutureTask 





#### Chap.10

多线程调试 findbufgs jcstress



## 第二部分 多线程编程进阶

#### Chap.11 多线程编程的硬件基础与Java内存模型

Java内存模型

#### Chap.12 Java多线程程序的性能调校

多线程调优

锁消除

 锁粗化

偏向锁

适应性锁