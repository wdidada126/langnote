# gc

- GC算法
　　　 引用计数法（无法解决循环引用的问题，不被java采纳）
  　　根搜索算法
  　　现代虚拟机中的垃圾搜集算法：
　　　　　　标记-清除
　　　　　　复制算法（新生代）
　　　　　　标记-压缩（老年代）
  　　分代收集

Java虚拟机详解04----GC算法和种类
https://www.cnblogs.com/qianguyihao/p/4744233.html

jdk7 cms g1 笨神 内存70G 反射原理
https://www.sohu.com/a/124124072_494943

https://www.jianshu.com/p/43c1b262d36b

GC之ParNew收集器

ParNew 收集器

CMS 收集器

https://www.jianshu.com/p/477fe3e21a74

使用方式：-XX:+UseParNewGC，打开该开关后，使用ParNew(年轻代)+Serial Old(老年代)组合进行GC。另外，ParNew是CMS收集器的默认年轻代收集器。

JVM之ParNew和CMS日志分析

https://www.jianshu.com/p/8ccab4c10da2

```
2018-04-12T13:48:26.134+0800: 15578.050: [GC2018-04-12T13:48:26.135+0800: 15578.050: [ParNew: 3412467K->59681K(3774912K), 0.0971990 secs] 9702786K->6354533K(24746432K), 0.0974940 secs] [Times: user=0.95 sys=0.00, real=0.09 secs]
```

依次分析一下上面日志信息的含义：

2018-04-12T13:48:26.134+0800：Mirror GC 发生的时间；

15578.050：GC 开始时，相对 JVM 启动的相对时间，单位时秒，这里是4h+；

ParNew：收集器名称，这里是 ParNew 收集器，它使用的是并行的 mark-copy 算法，GC 过程也会 Stop the World；

3412467K->59681K：收集前后年轻代的使用情况，这里是 3.25G->58.28M；

3774912K：整个年轻代的容量，这里是 3.6G；

0.0971990 secs：Duration for the collection w/o final cleanup.

9702786K->6354533K：收集前后整个堆的使用情况，这里是 9.25G->6.06G;

24746432K：整个堆的容量，这里是 23.6G；

0.0974940 secs：ParNew 收集器标记和复制年轻代活着的对象所花费的时间（包括和老年代通信的开销、对象晋升到老年代开销、垃圾收集周期结束一些最后的清理对象等的花销）；

对于 [Times: user=0.95 sys=0.00, real=0.09 secs]，这里面涉及到三种时间类型，含义如下：

user：GC 线程在垃圾收集期间所使用的 CPU 总时间；

sys：系统调用或者等待系统事件花费的时间；

real：应用被暂停的时钟时间，由于 GC 线程是多线程的，导致了 real 小于 (user+real)，如果是 gc 线程是单线程的话，real 是接近于 (user+real) 时间。

