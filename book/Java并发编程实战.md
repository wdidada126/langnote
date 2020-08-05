# Java并发编程实战



[Java并发编程实战](https://book.douban.com/subject/10484692/)

本书作者都是Java Community Process JSR 166专家组（并发工具）的主要成员，并在其他很多JCP专家组里任职。Brian Goetz有20多年的软件咨询行业经验，并著有至少75篇关于Java开发的文章。Tim Peierls是“现代多处理器”的典范，他在BoxPop.biz、唱片艺术和戏剧表演方面也颇有研究。Joseph Bowbeer是一个Java ME专家，他对并发编程的兴趣始于Apollo计算机时代。David Holmes是《The Java Programming Language》一书的合著者，任职于Sun公司。Joshua Bloch是Google公司的首席Java架构师，《Effective Java》一书的作者，并参与著作了《Java Puzzlers》。Doug Lea是《Concurrent Programming》一书的作者，纽约州立大学 Oswego分校的计算机科学教授。




javax.annotation.concurrent.ThreadSafe



看不懂，现在看懂了



### 第1章　简介



### 第2章 线程安全性


非原子的64位操作
高低两个32位操作

对象的共享 可见性
举例：



### 第3章 对象的共享


final修饰变量 只能赋值一次
static修饰的变量 java内存模型里面有同步机制，确保线程安全



### 第4章 对象的组合



### 第5章 基础构建模块



同步工具类
Latch FutchTask
Semaphere
ConcurrentHashMap
size()
isEmpty()方法不一定准确
可以任意读
有限数量个写


CompleteService


ES

### 第6章 任务执行

CompleteService

### 第7章 取消与关闭
ES

Future

shutdownNow的局限性

### 第8章 线程池的使用



### 第9章 图形用户界面应用程序



### 第10章



### 第11章



### 第12章



### 第13章



### 第14章

