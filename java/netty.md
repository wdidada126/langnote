# netty

- doc
- 书籍netty实战
- netty权威指南
- 闪电侠netty源码课
- [netty 4 guide](https://github.com/waylau/netty-4-user-guide)

应用场景：

pop stmp协议发送邮件

websocket

dubbo netty



DirectByteBuf





ByteBuf又分为两种，DirectByteBuf和HeapByteBuf。简而言之就是一种是分配在Direct Memory上的，一种是分配在Heap Memory上的。



这里稍微解释一下direct memory。直接内存（Direct Memory）并不是虚拟机运行时数据区的一部分，也不是Java虚拟机规范中定义的内存区域，但是这部分内存也被频繁地使用，而且也可能导致异常出现。它是在JDK 1.4 中新加入了NIO（New Input/Output）类，引入了一种基于通道（Channel）与缓冲区（Buffer）的I/O 方式，它可以使用Native 函数库直接分配堆外内存，然通过一个存储在Java 堆里面的DirectByteBuffer 对象作为这块内存的引用进行操作。这样能在一些场景中显著提高性能，因为避免了在Java 堆和Native 堆中来回复制数据。



https://www.jianshu.com/p/5f029d89a605

直接内存的好处就是利用的是native库，读写快速。但是它不在虚拟机的管理范围之内，这部分内存只有在进行full gc时才会进行回收，而他的容量如果没有明确限制，随着数据的不断读写势必造成内存中可利用的空间不断变小。所以netty做了引用计数机制来处理direct memory上的数据。





netty3是jboss的

netty4是io.netty的



https://github.com/edidada/Netty-study



https://github.com/edidada/testnetty



[DUBBO底层高并发RPC原理Netty高性能源码分析](https://www.hellojava.com/a/213.html)



[Netty线程模型](https://www.cnblogs.com/songxh-scse/p/6692301.html)





看知识星球 netty源码解读





闪电侠netty源码课

https://coding.imooc.com/class/230.html




netty org.jboss
netty-all io.netty

nety参看资料
https://github.com/waylau/netty-4-user-guide

https://waylau.com/netty-4-user-guide/





在 Netty5 中，基于 AIO 改造和支持，最后发现，性能并没有想象中这么强悍，所以 Netty5 被废弃，而是继续保持 Netty4 为主版本，使用 NIO 为主。
连接逻辑组件( ChannelHander 中顺序处理消息 )以及组件复用( 一个 ChannelHandel 可以被多个ChannelPipeLine 复用 )


[Netty实现WebSocket通信](https://blog.csdn.net/naruto_Mr/article/details/81452640)

[netty实现websocket（二）----实例](https://blog.csdn.net/ouyang111222/article/details/51063295)



Readhat主导



Reactor模式

单机



[Java NIO Channel示例](https://blog.csdn.net/lianggx3/article/details/89297720)



Netty实现http

[netty核心解析](https://blog.csdn.net/qq_32370913/article/details/105408027)
