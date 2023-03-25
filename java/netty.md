# netty

- api doc
- 书籍


- netty实战
- netty权威指南
- 闪电侠netty源码课
- [netty 4 guide](https://github.com/waylau/netty-4-user-guide)
- netty-example


应用场景：

pop stmp协议发送邮件

websocket

dubbo netty


### jar包

- 

### 核心类

DirectByteBuf

ByteBuf
ByteBuffer


ByteBuf又分为两种，DirectByteBuf和HeapByteBuf。简而言之就是一种是分配在Direct Memory上的，一种是分配在Heap Memory上的。



这里稍微解释一下direct memory。直接内存（Direct Memory）并不是虚拟机运行时数据区的一部分，也不是Java虚拟机规范中定义的内存区域，但是这部分内存也被频繁地使用，而且也可能导致异常出现。它是在JDK 1.4 中新加入了NIO（New Input/Output）类，引入了一种基于通道（Channel）与缓冲区（Buffer）的I/O 方式，它可以使用Native 函数库直接分配堆外内存，然通过一个存储在Java 堆里面的DirectByteBuffer对象作为这块内存的引用进行操作。这样能在一些场景中显著提高性能，因为避免了在Java堆和Native堆中来回复制数据。



[netty之DirectByteBuf和HeapByteBuf浅谈](https://www.jianshu.com/p/5f029d89a605)

直接内存的好处就是利用的是native库，读写快速。但是它不在虚拟机的管理范围之内，这部分内存只有在进行full gc时才会进行回收，而他的容量如果没有明确限制，随着数据的不断读写势必造成内存中可利用的空间不断变小。所以netty做了引用计数机制来处理direct memory上的数据。




### netty版本
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

netty可以用作客户端client

### netty 日志

```shell
2021-04-12 21:19:50.087 [main] DEBUG i.n.util.internal.logging.InternalLoggerFactory - Using SLF4J as the default logging framework
```

[netty 打印 log 日志](https://blog.csdn.net/weixin_40516936/article/details/80181890)

Netty是一个简化Java NIO编程的网络框架。就像人要吃饭一样，框架也要打日志。
Netty不像大多数框架，默认支持某一种日志实现。相反，Netty本身实现了一套日志机制，但这套日志机制并不会真正去打日志。相反，Netty自身的日志机制更像一个日志包装层。

先检查是否有slf4j，如果没有则检查是否有Log4j，如果上面两个都没有，则默认使用JDK自带的日志框架JDK Logging。
JDK的Logging就不用费事去检测了，直接拿来用了，因为它是JDK自带的。

io.netty.bootstrap.Bootstrap
源码：
`private static final InternalLogger logger = InternalLoggerFactory.getInstance(Bootstrap.class);`

### netty api doc

https://netty.io/4.1/api/index.html
io.netty.bootstrap
AbstractBootstrap
Bootstrap, ServerBootstrap



io.netty.channel
EventLoopGroup 接口
EventLoop next()
ChannelFuture register(Channel channel)
ChannelFuture register(ChannelPromise promise)


AbstractEventLoop, AbstractEventLoopGroup, DefaultEventLoop, DefaultEventLoopGroup, EpollEventLoopGroup, KQueueEventLoopGroup, LocalEventLoopGroup, MultithreadEventLoopGroup, NioEventLoop, NioEventLoopGroup, OioEventLoopGroup, SingleThreadEventLoop, ThreadPerChannelEventLoop, ThreadPerChannelEventLoopGroup

Boss/workers线程池
        EventLoopGroup bossGroup = new NioEventLoopGroup(1);//线程池
        EventLoopGroup workerGroup = new NioEventLoopGroup();//线程池

```java
    try {
        ServerBootstrap b = new ServerBootstrap();
        b.group(bossGroup, workerGroup)
```


在netty的架构这块我们使用一种bossGroup加workerGroup的方式，bossGroup只负责请求的转发，workerGroup是具体的数据处理，其实netty整个框架使用的是Reactor(响应器)的设计模式。

boss parent
work children

EventLoop是Netty Server用于处理IO事件的事件轮询处理器，职责上类似于Redis的eventLoop，EventLoop通常是由EventLoopGroup来管理的，EventLoopGroup负责调度指派EventLoop，而EventLoop负责具体的执行。
https://segmentfault.com/a/1190000038227963

可以这么说，ServerBootstrap监听的一个端口对应一个boss线程，它们一一对应。比如你需要netty监听80和443端口，那么就会有两个boss线程分别负责处理来自两个端口的socket请求。在boss线程接受了socket连接求后，会产生一个channel（一个打开的socket对应一个打开的channel），并把这个channel交给ServerBootstrap初始化时指定的ServerSocketChannelFactory来处理，boss线程则继续处理socket的请求。
https://blog.csdn.net/liao49/article/details/84397668



io.netty.channel.ChannelInboundHandlerAdapter 继承 ChannelHandlerAdapter类

AbstractRemoteAddressFilter, ApplicationProtocolNegotiationHandler, ByteToMessageDecoder, ChannelDuplexHandler, ChannelInitializer, HttpServerExpectContinueHandler, InboundHttpToHttp2Adapter, MessageToMessageDecoder, OcspClientHandler, SimpleChannelInboundHandler, SimpleUserEventChannelHandler, SslMasterKeyHandler, Utf8FrameValidator

ChannelHandlerAdapter
方法
 public boolean isSharable()
 public void handlerAdded(ChannelHandlerContext ctx)
 public void handlerRemoved(ChannelHandlerContext ctx)
 public void exceptionCaught(ChannelHandlerContext ctx, Throwable cause)
备注：这里就是事件驱动

ChannelHandler 接口
    void handlerAdded(ChannelHandlerContext var1) throws Exception;

    void handlerRemoved(ChannelHandlerContext var1) throws Exception;



io.netty.bootstrap.AbstractBootstrap#handler(io.netty.channel.ChannelHandler)





java.nio.channels.spi.SelectorProvider#provider

SelectorProvider (java.nio.channels.spi)
    SelectorProviderUDT (com.barchart.udt.nio)
    SelectorProviderImpl (sun.nio.ch)
        WindowsSelectorProvider (sun.nio.ch)

MultithreadEventLoopGroup
    private static final int DEFAULT_EVENT_LOOP_THREADS = Math.max(1, SystemPropertyUtil.getInt("io.netty.eventLoopThreads", NettyRuntime.availableProcessors() * 2));


EventLoopGroup是一组EventLoop的抽象，由于Netty对Reactor模式进行了变种，实际上为更好的利用多核CPU资源，Netty实例中一般会有多个EventLoop同时工作，每个EventLoop维护着一个Selector实例，类似单线程Reactor模式地工作着。至于多少线程可有用户决定，Netty也根据实际上的处理器核数提供了一个默认的数字，我们也建议使用这个数字

io.netty.channel.ChannelFuture io.netty.channel.MultithreadEventLoopGroup#register(io.netty.channel.Channel)


ChannelPromise接口
https://jiuaidu.com/jianzhan/985094/

DefaultChannelPromise实现类


[抓到 Netty 一个隐藏很深的内存泄露 Bug | 详解 Recycler 对象池的精妙设计与实现](https://xie.infoq.cn/article/ea5c220d79a131a2fbe57f142)



