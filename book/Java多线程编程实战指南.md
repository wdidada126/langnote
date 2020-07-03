# Java多线程编程实战指南

https://book.douban.com/subject/27034721/ 核心篇

https://book.douban.com/subject/26642317/ 设计模式篇



## Chap.1

Thread Runnable

void join() 等待相应的线程运行结束 线程A调用线程B的join方法，那么线程A的运行会被暂停，直到线程B运行结束
static void 

#### Chap.2

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



#### Chap.5

线程间协作

#### Chap.6

线程安全

#### Chap.7

线程死锁

#### Chap.8

线程组

#### Chap.9

异步编程

#### Chap.10

多线程调试 findbufgs jcstress

#### Chap.11

Java内存模型

#### Chap.12

多线程调优
