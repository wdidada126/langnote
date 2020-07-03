# 

CAS算法
Lmbench3 linux平台下的性能测试工具
vmstat Linux监控工具介绍系列——vmstat

chap 2
volatile关键字修饰的变量所有线程在任何时候读到的数据是一致的。
相反的，如果不用volatile关键字，就会发生一个线程写，另外一个线程读，因为写入操作不是原子操作，读线程读取的结果有两个可能，发生脏读。

2.2 synchronized的实现原理与应用
synchronized是重量级锁，但Java SE 1.6对synchronized进行优化。
对于普通同步方法，锁是当前实例对象
对于静态同步方法，锁是当前类的Class对象
对于同步方法块，锁是Synchonized括号里配置的对象

JVM基于进入和退出Monitor对象来实现方法同步和代码块同步，但两者的实现细节不一样。代码块同步是使用monitorenter和monitorexit指令实现的，而方法同步是使用另外一种方式实现的，细节在JVM规范里并没有详细说明

