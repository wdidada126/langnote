# netty


Trustin Lee的作品
https://twitter.com/trustin
https://speakerdeck.com/trustin

Netty boss线程池大小不为1时候咋用，干什么用，有这么用过的吗?
netty 中 bossgroup 线程池 大小为 1吗

netty 中reactor主从多线程模型，bossgroup 线程池大小默认应该为1， 那大于1有没有用呢，具体干什么用。 网上两种说法：1：说是监听多个服务器端口用； 2： Main Reactor Thread Pool(Accept Pool) 做Auth/login/shake-hand/SLA用 这两种说法哪个是正确的？ 如果2是正确的， 有没有具体的代码示例，怎么用的，在addLast那块怎么添加handler? 是跟添加业务线程池一样吗（addLast(EventExcutorGroup group,String name, ChannleHandler handler）?



bossgroup 对应使用的是主reactor吗？ workgroup对应使用的是从reactor吗


bossGroup也是new NioEventLoopGroup，而NioEventLoopGroup默认的线程数量是cpu核心数*2还是+1我忘了。所以bossGroup本来就是多线程。一个eventLoop可以处理多个客户端链接，而一个客户端链接只能注册在同一个eventLoop上，这才是netty的实现。什么默认大小应该为1，看看源码，不要章口就莱

作者：太上玄元道君
 https://www.zhihu.com/question/330317976/answer/723690201



嗯，看源码了。默认那个我弄错了，nioeventloopgroup，默认是cpu*2。作为服务器端bossgroup线程池,会选取一个线程来作为acceptor获取客户端连接。
我想请教的是，作为开一个监听端口的服务器端来说，boss线程池其他的线程做什么去了，是不是就没用了(前提是bossgroup没再绑定别的serverbootstrap,服务端只开一个服务端口)。
外网查了下，stackoverflow上有个说法是多个serverbootstrap共用一个bossgroup线程池时，应该是指服务端开多个端口情况。这个应该仔细研究下源码就能知道了。


你后面说的确实没错。server启动一个端口确实只绑定一个boss线程。它是借用了线程池的execute提交一个bind任务新启动一个线程（未到达设置的上限的时候），线程池的初始化是懒加载的，即使你设置boss大小为10，在只绑定一个端口的情况下也只是新启动了一个线程。

而由于select方法是一个死循环，当前线程不会退出，所以我认为boss线程池的最大线程数量等于能绑定的端口数（EpollEventLoopGroup不确定是不是这样，因为以前学习的时候mac不支持epoll，所以当时也没再去测试）。

所以如果你想多线程去accept，那就只能多绑定几个端口了





- api doc
- 书籍


- netty实战
- netty权威指南
- Netty原理剖析与实战
- 闪电侠netty源码课
- [netty 4 guide](https://github.com/waylau/netty-4-user-guide)
- netty-example


Dubbo是如何使用Netty的
使用netty实现telnet

netty是如何实现http协议的，重点分析下



应用场景：

pop stmp协议发送邮件

websocket

dubbo netty


### jar包

- 


Java NIO（New I/O）是Java 1.4版本引入的一个新的I/O API，可以用来替换原来的Java I/O API（即Java 1.0到Java 1.3版本所使用的I/O API），提供了异步非阻塞的高效数据传输方式，适用于处理高并发、高吞吐量的应用场景。Java NIO的核心类主要包括以下几种：

Buffer：缓冲区，提供了读写数据的操作，底层使用数组实现。
Channel：通道，提供了底层传输数据的接口，可以是文件、网络套接字等。
Selector：选择器，可以轮询多个通道的状态，进行高效的事件驱动型操作。
Charset：字符集，提供了编码和解码的功能。
FileChannel：文件通道，用于对文件进行读写操作。
SocketChannel：套接字通道，用于对TCP连接进行读写操作。
ServerSocketChannel：服务器套接字通道，用于监听TCP连接请求，并创建相应的SocketChannel。
DatagramChannel：数据报通道，用于对UDP连接进行读写操作。


Netty是一款高性能的网络编程框架，其核心类主要包括：

Channel：表示一个网络连接的实体，类似于Java NIO中的SocketChannel。通过Channel可以读取和写入数据，注册Channel感兴趣的事件，以及获取Channel的配置等信息。

EventLoop：表示一个事件循环，用于处理IO操作和事件通知。一个EventLoop通常绑定到一个或多个Channel，可以处理多个Channel上的IO操作。Netty使用了一种线程模型，即每个EventLoop都绑定到一个线程上，在该线程上运行EventLoop中的任务。

ChannelPipeline：表示一个ChannelHandler的链表，用于处理Channel上的事件。每个Channel都会有一个对应的ChannelPipeline，当Channel上发生事件时，事件会从Pipeline的头部开始依次被ChannelHandler处理。

ChannelHandlerContext：表示ChannelHandler和ChannelPipeline之间的上下文关系。ChannelHandler可以通过ChannelHandlerContext访问到ChannelPipeline和其他ChannelHandler，并调用相关方法。

ChannelHandler：表示一个Channel的处理器，用于处理Channel上的事件。ChannelHandler通常被添加到ChannelPipeline中，并被顺序执行，以完成一系列的业务逻辑处理。

Bootstrap：表示一个用于启动和连接网络连接的辅助类。通过Bootstrap可以配置Channel类型、EventLoop类型、ChannelHandler、连接超时时间等信息。

ServerBootstrap：表示一个用于启动和监听网络连接的辅助类。通过ServerBootstrap可以配置Channel类型、EventLoop类型、ChannelHandler、连接超时时间、端口号等信息，并启动服务器。

ByteBuf：表示一个字节缓冲区，用于在网络中传输数据。ByteBuf支持读写、引用计数、池化等操作，并提供了一些方便的方法，如get/set/read/write等。




SingleThreadEventExecutor



在 Netty 中，通常会使用两类线程来处理来自客户端的请求，一类是 boss 线程，另一类是 worker 线程。它们各自的作用如下：

boss 线程
负责监听客户端连接请求，当有新的连接请求时，会创建一个新的 SocketChannel，并将其注册到一个 worker 线程上。
boss 线程的数量通常设置为 1。
worker 线程
负责处理客户端连接请求，处理读写事件，以及执行 ChannelPipeline 中的各个 Handler。
通常有多个 worker 线程，线程的数量根据实际情况和硬件配置进行调整。
在 Netty 中，boss 线程和 worker 线程都是 EventLoop 的实例。EventLoop 是 Netty 的核心组件之一，它负责监听并处理 IO 事件，并且提供了定时调度、异步任务执行等能力。

SingleThreadEventExecutor 是 Netty 中的一个抽象类，用于表示只有一个线程的 EventExecutor 实现。它继承了 ScheduledFutureTaskQueue 和 SingleThreadEventLoop 两个类，并提供了线程执行器的基本逻辑实现，包括线程池的创建、任务执行、定时任务处理等等。在 Netty 中，boss 线程和 worker 线程都是基于 SingleThreadEventExecutor 实现的。



SingleThreadEventExecutor是一个抽象类，它的实现类有以下几个：

NioEventLoop：使用Java NIO实现的EventLoop，它是SingleThreadEventExecutor的子类。
EpollEventLoop：使用Linux epoll实现的EventLoop，它也是SingleThreadEventExecutor的子类。
KQueueEventLoop：使用BSD kqueue实现的EventLoop，同样也是SingleThreadEventExecutor的子类。


是的，EpollEventLoop是Netty在Linux平台上使用的事件循环实现类。它利用了Linux内核中的Epoll机制来提高网络IO事件的处理效率，相比于传统的Select机制有更好的性能表现。因此，在Linux平台上，Netty默认使用EpollEventLoop来实现事件循环。而在Windows平台上，则使用另外一种实现类，即NioEventLoop。



```java
import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.ServerSocketChannel;
import java.nio.channels.SocketChannel;
import java.nio.charset.Charset;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class NioServer {
    public static void main(String[] args) throws Exception {
        // 创建一个线程池
        ExecutorService executorService = Executors.newFixedThreadPool(10);

        // 创建一个 ServerSocketChannel
        ServerSocketChannel serverSocketChannel = ServerSocketChannel.open();

        // 绑定端口
        serverSocketChannel.socket().bind(new InetSocketAddress(8000));

        // 设置非阻塞模式
        serverSocketChannel.configureBlocking(false);

        System.out.println("NioServer started on port 8000");

        while (true) {
            // 接受连接
            SocketChannel socketChannel = serverSocketChannel.accept();

            if (socketChannel != null) {
                // 打印客户端地址
                System.out.println("Client connected from " + socketChannel.getRemoteAddress());

                // 创建一个新的客户端处理线程
                ClientHandler clientHandler = new ClientHandler(socketChannel);

                // 将线程提交到线程池中执行
                executorService.submit(clientHandler);
            }
        }
    }

    static class ClientHandler implements Runnable {
        private SocketChannel socketChannel;

        public ClientHandler(SocketChannel socketChannel) {
            this.socketChannel = socketChannel;
        }

        @Override
        public void run() {
            ByteBuffer buffer = ByteBuffer.allocate(1024);
            Charset charset = Charset.forName("UTF-8");

            try {
                while (socketChannel.read(buffer) > 0) {
                    buffer.flip();
                    String request = charset.decode(buffer).toString();
                    System.out.println("Received message from client: " + request);

                    // Echo the request back to the client
                    socketChannel.write(charset.encode("Echo: " + request));

                    buffer.clear();
                }
            } catch (IOException e) {
                e.printStackTrace();
            } finally {
                try {
                    socketChannel.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }
}

```




### 核心类


ChannelInboundHandlerAdapter ChannelHandlerAdapter区别
ChannelInboundHandlerAdapter我们通常会继承此类，覆写上面的channelRead方法，加入自己的逻辑处理。

SimpleChannelInboundHandler是有泛型参数的。

DirectByteBuf

ByteBuf    netty的类
ByteBuffer   java se的类

 （1）   ByteBuffer长度固定，一旦分配完成，它的容量不能动态扩展和收缩，当需要编 码的POJO对象大于ByteBuffer的容量时，会发生索引越界异常；
  （2）   ByteBuffer只有一个标识位置的指针position,读写的时候需要手工调用flip。和 rewind。等，使用者必须小心谨慎地处理这些API,否则很容易导致程序处理失败；
  （3）   ByteBuffer的API功能有限，一些高级和实用的特性它不支持，需要使用者自己 编程实现。
  为了弥补这些不足，Netty提供了自己的ByteBuffer实现-ByteBuf,下面我们一起
学习ByteBuf的原理和主要功能。


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



