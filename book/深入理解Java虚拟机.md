# 深入理解Java虚拟机

[深入理解Java虚拟机](https://book.douban.com/subject/34907497/)

1、走近Java
2、自动内存管理

## 3、虚拟机执行子系统
## 4、程序编译与代码优化

结合编译原理来学

5、高效并发

3

java模型

jvm模型

回收器 cms g1 zgc



回收算法
标记清楚
标记整理
可达性分析

debug

java模型
heap
method no-heap
stack
native stack
主要回收heap区域





运行时数据区域
程序计数器
Java虚拟机栈
本地方法栈
Java堆
方法区
运行时常量池
直接内存

[JVM内存模型、Java内存模型 和 Java对象模型](https://www.cnblogs.com/wenxiangchen/p/11478767.html)

https://www.cnblogs.com/wenxiangchen/p/11478767.html

总结
 1.JVM内存模型，和Java虚拟机的运行时区域有关。
 2.Java内存模型，和Java的并发编程有关。
 3.Java对象模型，和Java对象在虚拟机中的表现形式有关。

1.标记/清除算法【最基础】
2.复制算法
3.标记/整理算法
jvm采用`分代收集算法`对不同区域采用不同的回收算法。
https://www.jianshu.com/p/76959115d486

