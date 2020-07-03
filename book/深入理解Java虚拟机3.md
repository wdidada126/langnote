# 深入理解Java虚拟机（第3版）

https://book.douban.com/subject/34907497/





周志明（博士）

资深Java技术专家-机器学习技术专家和企业级开发技术专家，现任远光软件研究院院长。

开源技术的积极倡导者和推动者，对计算机科学相关的多个领域都有深刻的见解，尤其是人工智能-Java技术和敏捷开发等，对虚拟机技术有非常深入的研究。

撰写了《深入理解Java虚拟机》《深入理解OSGi》《智慧的疆界》等多本著作，翻译了《Java虚拟机规范》等著作。其中《深入理解Java虚拟机》已累计印刷逾36次，总销超过30万册，成为原创计算机专业图书领域难以逾越的丰碑。



windows上下载了，百度网盘上有




hotspot虚拟机日志

jdk9以前乱

jdk8

对于4G/6G内存的，选CMS垃圾回收器





```plain
-XX:+PrintGCDetails
-Xms30M
-Xmx30M
-Xmn10M
-XX:SurvivorRatio=8
```

参数含义分别是：

打印GC日志

最小堆内存

最大堆内存

堆中新生代内存

新生代内存中Eden和Survivor大小之比，如果为8表示Eden占80%，另外两个Survivor各占10%



[jdk1.8 Hotspot虚拟机参数通用配置](https://blog.csdn.net/weixin_43532530/article/details/83548082)



只能去找hotspot相关的书籍 论文 博文 开发者文档



##### 3.7  jdk1.8 Hotspot虚拟机参数通用配置



新生代 egen + 1s

老年代 1s



mingc fullgc

要多看，多做实验


jit编译器





aot编译器



Apache Harmony



Azul VM

IBM J9 VM



#### Java内存模型（Java Memory Mode，JMM）

https://www.jianshu.com/p/07f5fceb6f12



Java内存模型定义了线程和主内存之间的抽象关系，具体如下：

- 共享变量存储于主内存之中，每个线程都可以访问。
- 每个线程都有私有的工作内存或者称为本地内存。
- 工作内存只存储该线程对共享变量的副本。
- 线程不能直接操作主内存，只有先操作本地内存之后才能写入主内存。
- 工作内存和Java内存模型一样也是一个抽象的概念，它其实并不存在，它涵盖了缓存、寄存器、编译器优化以及硬件等。

![jmm png](imgs/jmm.png)

#### JVM内存模型



1、**Class Loader**（类加载器）就是将Class文件加载到内存，再说的详细一点就是，把描述类的数据从Class文件加载到内存，并对数据进行校验、转换解析和初始化，最终形成可以被虚拟机直接使用的Java类型，这就是类加载器的作用。
 2、**Run Data Area**（运行时数据区） 就是我们常说的JVM管理的内存了，也是我们这里主要讨论的部分。运行数据区是整个JVM的重点。我们所有写的程序都被加载到这里，之后才开始运行。这部分也是我们这里将要讨论的重点。

3、**Execution engine**（执行引擎） 是Java虚拟机最核心的组成部分之一。执行引擎用于执行指令，不同的java虚拟机内部实现中，执行引擎在执行Java代码的时候可能有解释执行（解释器执行）和编译执行（通过即时编译器产生本地代码执行，例如BEA JRockit），也有可能两者兼备。任何JVM specification实现(JDK)的核心都是Execution engine，不同的JDK例如Sun 的JDK 和IBM的JDK好坏主要就取决于他们各自实现的Execution engine的好坏。
 4、**Native interface** 与native libraries交互，是其它编程语言交互的接口。当调用native方法的时候，就进入了一个全新的并且不再受虚拟机限制的世界，所以也很容易出现JVM无法控制的native heap OutOfMemory。



作者：沉淀之际
链接：https://www.jianshu.com/p/07f5fceb6f12
来源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

![jvm png](img/jvm.png)



Chap. 7 虚拟机类加载机制 

