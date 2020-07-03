# Java 7并发编程实战手册



https://book.douban.com/subject/25844475/







### chapter1 线程管理
- java.lang.Runnable
- java.lang.Thread


java.lang.Thread.State


java.lang.Thread#setPriority

java.lang.ThreadGroup

java.lang.Thread#setName
java.lang.Runnable#run

java.util.concurrent.TimeUnit#SECONDS

java.util.concurrent.TimeUnit#sleep

join() 等待线程终止
ThreadFactory接口



Chap. 1

1.2线程的创建

线程的创建

1、 继承Thread重写run()方法

2、创建一个实现Runnable接口的类。使用带参数的Thread构造器来创建Thread对象。

1.3 线程状态的获取

线程的优先级：

Thread.MIN_PRIORITY

Thread.NORM_PRIORITY

Thread.MAX_PRIORITY

java 7并发编程实战 第一章读书笔记

id

name

Thread.Status 枚举

NEW，RUNNABLE，BLOCKED，WAITING，TIMED_WAITING，TERMINATED

1.4 线程的中断

Thread interrupt()

isInterrupted()



### chapter2 线程同步基础

synchronized
Lock
ReadWriteLock

2.8
Condiction

await（）

条件锁
读写锁



### chapter3线程同步辅助类

Semaphore 大多数语言都提供
CountDownLatch java提供
一个线程等待另一个线程执行完
CyclicBarries java提供
Phaser java提供
Exchanger java提供


### chapter4 线程执行器

ES

### chapter5 Fork/Join框架

### chapter6 并发集合 

原子变量

原子数组

### chapter7 定制并发类

定制Lock类

### chapter8 测试并发应用程序

FindBugs

MultithreadedTC





