# netty


Trustin Lee的作品
https://twitter.com/trustin
https://speakerdeck.com/trustin

Netty boss线程池大小不为1时候咋用，干什么用，有这么用过的吗?
netty 中 bossgroup 线程池 大小为 1吗

netty 中reactor主从多线程模型，bossgroup 线程池大小默认应该为1， 那大于1有没有用呢，具体干什么用。 网上两种说法：1：说是监听多个服务器端口用； 2： Main Reactor Thread Pool(Accept Pool) 做Auth/login/shake-hand/SLA用 这两种说法哪个是正确的？ 如果2是正确的， 有没有具体的代码示例，怎么用的，在addLast那块怎么添加handler? 是跟添加业务线程池一样吗（addLast(EventExcutorGroup group,String name, ChannleHandler handler）?



bossgroup 对应使用的是主reactor吗？ workgroup对应使用的是从reactor吗


bossGroup也是new NioEventLoopGroup，而NioEventLoopGroup默认的线程数量是cpu核心数*2还是+1我忘了。所以bossGroup本来就是多线程。一个eventLoop可以处理多个客户端链接，而一个客户端链接只能注册在同一个eventLoop上，这才是netty的实现。什么默认大小应该为1，看看源码，不要章口就来

作者：太上玄元道君
 https://www.zhihu.com/question/330317976/answer/723690201



嗯，看源码了。默认那个我弄错了，nioeventloopgroup，默认是cpu*2。作为服务器端bossgroup线程池,会选取一个线程来作为acceptor获取客户端连接。
我想请教的是，作为开一个监听端口的服务器端来说，boss线程池其他的线程做什么去了，是不是就没用了(前提是bossgroup没再绑定别的serverbootstrap,服务端只开一个服务端口)。
外网查了下，stackoverflow上有个说法是多个serverbootstrap共用一个bossgroup线程池时，应该是指服务端开多个端口情况。这个应该仔细研究下源码就能知道了。


你后面说的确实没错。server启动一个端口确实只绑定一个boss线程。它是借用了线程池的execute提交一个bind任务新启动一个线程（未到达设置的上限的时候），线程池的初始化是懒加载的，即使你设置boss大小为10，在只绑定一个端口的情况下也只是新启动了一个线程。

而由于select方法是一个死循环，当前线程不会退出，所以我认为boss线程池的最大线程数量等于能绑定的端口数（EpollEventLoopGroup不确定是不是这样，因为以前学习的时候mac不支持epoll，所以当时也没再去测试）。

所以如果你想多线程去accept，那就只能多绑定几个端口了





- api doc https://netty.io/4.1/api/
- 书籍


- netty实战
- netty权威指南
- Netty原理剖析与实战
- 闪电侠netty源码课
- [netty 4 guide](https://github.com/waylau/netty-4-user-guide)
- netty-example
- Netty4核心原理与手写RPC框架实战 https://github.com/gupaoedu-tom/netty4-samples

Dubbo是如何使用Netty的
使用netty实现telnet

netty是如何实现http协议的，重点分析下



应用场景：

pop stmp协议发送邮件

websocket

dubbo netty


## jar包

- netty
- netty-all
- netty-bom
- netty-buffer
- netty-build                                                                                     
- netty-build-common
- netty-codec
- netty-codec-dns
- netty-codec-haproxy
- netty-codec-http
- netty-codec-http2
- netty-codec-memcache
- netty-codec-mqtt
- netty-codec-redis
- netty-codec-smtp
- netty-codec-socks
- netty-codec-stomp
- netty-codec-xml
- netty-common
- netty-dev-tools
- netty-handler                                                                                   
- netty-handler-proxy
- netty-handler-ssl-ocsp
- netty-jni-util
- netty-parent
- netty-resolver
- netty-resolver-dns
- netty-resolver-dns-classes-macos
- netty-resolver-dns-native-macos
- netty-tcnative                                                                                  
- netty-tcnative-boringssl-static
- netty-tcnative-classes
- netty-tcnative-parent
- netty-testsuite
- netty-transport                                                                                 
- netty-transport-classes-epoll
- netty-transport-classes-kqueue
- netty-transport-native-epoll
- netty-transport-native-kqueue
- netty-transport-native-unix-common
- netty-transport-native-unix-common-tests
- netty-transport-rxtx                                                                            
- netty-transport-sctp
- netty-transport-udt

  <modules>
    <module>all</module>
    <module>dev-tools</module>
    <module>common</module>
    <module>buffer</module>
    <module>codec</module>
    <module>codec-dns</module>
    <module>codec-haproxy</module>
    <module>codec-http</module>
    <module>codec-http2</module>
    <module>codec-memcache</module>
    <module>codec-mqtt</module>
    <module>codec-redis</module>
    <module>codec-smtp</module>
    <module>codec-socks</module>
    <module>codec-stomp</module>
    <module>codec-xml</module>
    <module>resolver</module>
    <module>resolver-dns</module>
    <module>resolver-dns-native-macos</module>
    <module>tarball</module>
    <module>transport</module>
    <module>transport-native-unix-common-tests</module>
    <module>transport-native-unix-common</module>
    <module>transport-native-epoll</module>
    <module>transport-native-kqueue</module>
    <module>transport-rxtx</module>
    <module>transport-sctp</module>
    <module>transport-udt</module>
    <module>handler</module>
    <module>handler-proxy</module>
    <module>example</module>
    <module>testsuite</module>
    <module>testsuite-autobahn</module>
    <module>testsuite-http2</module>
    <module>testsuite-osgi</module>
    <module>testsuite-shading</module>
    <module>testsuite-native-image</module>
    <module>transport-blockhound-tests</module>
    <module>microbench</module>
    <module>bom</module>
  </modules>



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
在Netty中，通常会使用两类线程来处理来自客户端的请求，一类是boss线程，另一类是worker线程。它们各自的作用如下：
boss线程
负责监听客户端连接请求，当有新的连接请求时，会创建一个新的SocketChannel，并将其注册到一个worker线程上。
boss线程的数量通常设置为1。
worker线程
负责处理客户端连接请求，处理读写事件，以及执行ChannelPipeline中的各个Handler。
通常有多个worker线程，线程的数量根据实际情况和硬件配置进行调整。
在Netty中，boss线程和worker线程都是EventLoop的实例。EventLoop是Netty的核心组件之一，它负责监听并处理IO事件，并且提供了定时调度、异步任务执行等能力。

SingleThreadEventExecutor是Netty中的一个抽象类，用于表示只有一个线程的EventExecutor实现。它继承了ScheduledFutureTaskQueue和SingleThreadEventLoop两个类，并提供了线程执行器的基本逻辑实现，包括线程池的创建、任务执行、定时任务处理等等。在Netty中，boss线程和worker线程都是基于SingleThreadEventExecutor实现的。



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



## 使用netty的框架
- dubbo
- vert.x


## 核心类


- Buffer
- SingleThreadEventExecutor
- ChannelInboundHandlerAdapter

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




## netty版本
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

## netty 日志

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

## netty api doc
https://javadoc.io/doc/io.netty/netty-all/4.1.52.Final/overview-summary.html

https://netty.io/4.1/api/index.html
## io.netty.bootstrap



| io.netty.bootstrap                           | 类型 |                     |
| -------------------------------------------- | ---- | ------------------- |
| Interfaces                                   |      |                     |
|                                              |      |                     |
| ChannelFactory                               |      |                     |
|                                              |      |                     |
| Classes                                      |      |                     |
|                                              |      |                     |
| AbstractBootstrap                            |      |                     |
| AbstractBootstrap.PendingRegistrationPromise |      |                     |
| AbstractBootstrapConfig                      |      |                     |
| Bootstrap                                    |      |                     |
| BootstrapConfig                              |      |                     |
| FailedChannel                                |      | AbstractChannel子类 |
| ServerBootstrap                              |      |                     |
| ServerBootstrapConfig                        |      |                     |



## io.netty.buffer





| io.netty.buffer                 | 类型      |                            |
| ------------------------------- | --------- | -------------------------- |
| Interfaces                      |           |                            |
|                                 |           |                            |
| ByteBufAllocator                | interface |                            |
| ByteBufAllocatorMetric          | interface |                            |
| ByteBufAllocatorMetricProvider  | interface |                            |
| ByteBufConvertible              | interface |                            |
| ByteBufHolder                   | interface | ReferenceCounted接口子接口 |
| ByteBufProcessor                | interface |                            |
| PoolArenaMetric                 | interface |                            |
| PoolChunkListMetric             | interface |                            |
| PoolChunkMetric                 | interface |                            |
| PoolSubpageMetric               | interface |                            |
| SizeClassesMetric               | interface |                            |
|                                 |           |                            |
| Classes                         |           |                            |
|                                 |           |                            |
| AbstractByteBuf                 | abstract  |                            |
| AbstractByteBufAllocator        | abstract  |                            |
| AbstractDerivedByteBuf          |           |                            |
| AbstractReferenceCountedByteBuf | abstract  |                            |
| ByteBuf                         | abstract  |                            |
| ByteBufInputStream              |           | DataInput接口实现类        |
| ByteBufOutputStream             |           |                            |
| ByteBufUtil                     |           |                            |
| CompositeByteBuf                |           |                            |
| DefaultByteBufHolder            |           |                            |
| DuplicatedByteBuf               |           |                            |
| EmptyByteBuf                    |           |                            |
| PooledByteBufAllocator          |           |                            |
| PooledByteBufAllocatorMetric    |           |                            |
| ReadOnlyByteBuf                 |           |                            |
| SlicedByteBuf                   |           |                            |
| SwappedByteBuf                  |           |                            |
| Unpooled                        |           |                            |
| UnpooledByteBufAllocator        |           |                            |
| UnpooledDirectByteBuf           |           |                            |
| UnpooledHeapByteBuf             |           |                            |
| UnpooledUnsafeDirectByteBuf     |           |                            |
| UnpooledUnsafeHeapByteBuf       |           |                            |





ByteBuf 抽象类 子类

ByteBuf (io.netty.buffer)
    AbstractByteBuf (io.netty.buffer)
        AbstractDerivedByteBuf (io.netty.buffer)
            ReadOnlyByteBuf (io.netty.buffer)
            ReadOnlyByteBuf (io.netty.buffer)
            DuplicatedByteBuf (io.netty.buffer)
                UnpooledDuplicatedByteBuf (io.netty.buffer)
                UnpooledDuplicatedByteBuf (io.netty.buffer)
            DuplicatedByteBuf (io.netty.buffer)
                UnpooledDuplicatedByteBuf (io.netty.buffer)
            AbstractUnpooledSlicedByteBuf (io.netty.buffer)
                UnpooledSlicedByteBuf (io.netty.buffer)
                UnpooledSlicedByteBuf (io.netty.buffer)
                SlicedByteBuf (io.netty.buffer)
                SlicedByteBuf (io.netty.buffer)
            AbstractUnpooledSlicedByteBuf (io.netty.buffer)
                UnpooledSlicedByteBuf (io.netty.buffer)
                SlicedByteBuf (io.netty.buffer)
        AbstractDerivedByteBuf (io.netty.buffer)
            ReadOnlyByteBuf (io.netty.buffer)
            DuplicatedByteBuf (io.netty.buffer)
            AbstractUnpooledSlicedByteBuf (io.netty.buffer)
        AbstractReferenceCountedByteBuf (io.netty.buffer)
            AbstractPooledDerivedByteBuf (io.netty.buffer)
            AbstractPooledDerivedByteBuf (io.netty.buffer)
            CompositeByteBuf (io.netty.buffer)
            CompositeByteBuf (io.netty.buffer)
            ReadOnlyByteBufferBuf (io.netty.buffer)
            ReadOnlyByteBufferBuf (io.netty.buffer)
            FixedCompositeByteBuf (io.netty.buffer)
            FixedCompositeByteBuf (io.netty.buffer)
            PooledByteBuf (io.netty.buffer)
            PooledByteBuf (io.netty.buffer)
            UnpooledDirectByteBuf (io.netty.buffer)
            UnpooledDirectByteBuf (io.netty.buffer)
            UnpooledHeapByteBuf (io.netty.buffer)
            UnpooledHeapByteBuf (io.netty.buffer)
        AbstractReferenceCountedByteBuf (io.netty.buffer)
            AbstractPooledDerivedByteBuf (io.netty.buffer)
            CompositeByteBuf (io.netty.buffer)
            ReadOnlyByteBufferBuf (io.netty.buffer)
            FixedCompositeByteBuf (io.netty.buffer)
            PooledByteBuf (io.netty.buffer)
            UnpooledDirectByteBuf (io.netty.buffer)
            UnpooledHeapByteBuf (io.netty.buffer)
    AbstractByteBuf (io.netty.buffer)
        AbstractDerivedByteBuf (io.netty.buffer)
            ReadOnlyByteBuf (io.netty.buffer)
            DuplicatedByteBuf (io.netty.buffer)
            AbstractUnpooledSlicedByteBuf (io.netty.buffer)
        AbstractReferenceCountedByteBuf (io.netty.buffer)
            AbstractPooledDerivedByteBuf (io.netty.buffer)
            CompositeByteBuf (io.netty.buffer)
            ReadOnlyByteBufferBuf (io.netty.buffer)
            FixedCompositeByteBuf (io.netty.buffer)
            PooledByteBuf (io.netty.buffer)
            UnpooledDirectByteBuf (io.netty.buffer)
            UnpooledHeapByteBuf (io.netty.buffer)
    EmptyByteBuf (io.netty.buffer)
    EmptyByteBuf (io.netty.buffer)
    ReplayingDecoderByteBuf (io.netty.handler.codec)
    ReplayingDecoderByteBuf (io.netty.handler.codec)
    WrappedByteBuf (io.netty.buffer)
        UnreleasableByteBuf (io.netty.buffer)
        UnreleasableByteBuf (io.netty.buffer)
        Component in FixedCompositeByteBuf (io.netty.buffer)
        Component in FixedCompositeByteBuf (io.netty.buffer)
        SimpleLeakAwareByteBuf (io.netty.buffer)
            AdvancedLeakAwareByteBuf (io.netty.buffer)
            AdvancedLeakAwareByteBuf (io.netty.buffer)
        SimpleLeakAwareByteBuf (io.netty.buffer)
            AdvancedLeakAwareByteBuf (io.netty.buffer)
    WrappedByteBuf (io.netty.buffer)
        UnreleasableByteBuf (io.netty.buffer)
        Component in FixedCompositeByteBuf (io.netty.buffer)
        SimpleLeakAwareByteBuf (io.netty.buffer)
            AdvancedLeakAwareByteBuf (io.netty.buffer)
    SwappedByteBuf (io.netty.buffer)
        AbstractUnsafeSwappedByteBuf (io.netty.buffer)
            UnsafeHeapSwappedByteBuf (io.netty.buffer)
            UnsafeHeapSwappedByteBuf (io.netty.buffer)
            UnsafeDirectSwappedByteBuf (io.netty.buffer)
            UnsafeDirectSwappedByteBuf (io.netty.buffer)
        AbstractUnsafeSwappedByteBuf (io.netty.buffer)
            UnsafeHeapSwappedByteBuf (io.netty.buffer)
            UnsafeDirectSwappedByteBuf (io.netty.buffer)
    SwappedByteBuf (io.netty.buffer)
        AbstractUnsafeSwappedByteBuf (io.netty.buffer)
            UnsafeHeapSwappedByteBuf (io.netty.buffer)
            UnsafeDirectSwappedByteBuf (io.netty.buffer)




### io.netty.buffer.search

| Interfaces                                 | 类型      |      |
| ------------------------------------------ | --------- | ---- |
|                                            |           |      |
| MultiSearchProcessor                       | interface |      |
| MultiSearchProcessorFactory                | interface |      |
| SearchProcessor                            | interface |      |
| SearchProcessorFactory                     | interface |      |
|                                            |           |      |
| Classes                                    |           |      |
|                                            |           |      |
| AbstractMultiSearchProcessorFactory        | abstract  |      |
| AbstractSearchProcessorFactory             | abstract  |      |
| AhoCorasicSearchProcessorFactory           |           |      |
| AhoCorasicSearchProcessorFactory.Processor |           |      |
| AhoCorasicSearchProcessorFactory.Context   |           |      |
| BitapSearchProcessorFactory                |           |      |
| BitapSearchProcessorFactory.Processor      |           |      |
| KmpSearchProcessorFactory                  |           |      |
| KmpSearchProcessorFactory.Processor        |           |      |





核心类是 SearchProcessor接口





io.netty.buffer.search.SearchProcessor接口

Processor in KmpSearchProcessorFactory (io.netty.buffer.search)
Processor in KmpSearchProcessorFactory (io.netty.buffer.search)
Processor in BitapSearchProcessorFactory (io.netty.buffer.search)
Processor in BitapSearchProcessorFactory (io.netty.buffer.search)
MultiSearchProcessor (io.netty.buffer.search)
    Processor in AhoCorasicSearchProcessorFactory (io.netty.buffer.search)
    Processor in AhoCorasicSearchProcessorFactory (io.netty.buffer.search)
MultiSearchProcessor (io.netty.buffer.search)
    Processor in AhoCorasicSearchProcessorFactory (io.netty.buffer.search)



## io.netty.channel





| io.netty.channel                               | 类型      |      |
| ---------------------------------------------- | --------- | ---- |
|                                                |           |      |
| AddressedEnvelope                              | interface |      |
| Channel                                        | interface |      |
| Channel.Unsafe                                 | interface |      |
| ChannelConfig                                  | interface |      |
| ChannelFactory                                 | interface |      |
| ChannelFuture                                  | interface |      |
| ChannelFutureListener                          | interface |      |
| ChannelHandler                                 | interface |      |
| ChannelHandlerContext                          | interface |      |
| ChannelId                                      | interface |      |
| ChannelInboundHandler                          | interface |      |
| ChannelInboundInvoker                          | interface |      |
| ChannelOutboundBuffer.MessageProcessor         | interface |      |
| ChannelOutboundHandler                         | interface |      |
| ChannelOutboundInvoker                         | interface |      |
| ChannelPipeline                                | interface |      |
| ChannelProgressiveFuture                       | interface |      |
| ChannelProgressiveFutureListener               | interface |      |
| ChannelProgressivePromise                      | interface |      |
| ChannelPromise                                 | interface |      |
| EventLoop                                      | interface |      |
| EventLoopGroup                                 | interface |      |
| EventLoopTaskQueueFactory                      | interface |      |
| FileRegion                                     | interface |      |
| MaxBytesRecvByteBufAllocator                   | interface |      |
| MaxMessagesRecvByteBufAllocator                | interface |      |
| MessageSizeEstimator                           | interface |      |
| MessageSizeEstimator.Handle                    | interface |      |
| RecvByteBufAllocator                           | interface |      |
| RecvByteBufAllocator.ExtendedHandle            | interface |      |
| RecvByteBufAllocator.Handle                    | interface |      |
| SelectStrategy                                 | interface |      |
| SelectStrategyFactory                          | interface |      |
| ServerChannel                                  | interface |      |
|                                                |           |      |
| Classes                                        |           |      |
|                                                |           |      |
| AbstractChannel                                | abstract  |      |
| AbstractCoalescingBufferQueue                  | abstract  |      |
| AbstractEventLoop                              | abstract  |      |
| AbstractEventLoopGroup                         | abstract  |      |
| AbstractServerChannel                          | abstract  |      |
| AdaptiveRecvByteBufAllocator                   |           |      |
| ChannelDuplexHandler                           |           |      |
| ChannelFlushPromiseNotifier                    |           |      |
| ChannelHandlerAdapter                          |           |      |
| ChannelInboundHandlerAdapter                   |           |      |
| ChannelInitializer                             |           |      |
| ChannelMetadata                                |           |      |
| ChannelOption                                  |           |      |
| ChannelOutboundBuffer                          |           |      |
| ChannelOutboundHandlerAdapter                  |           |      |
| ChannelPromiseAggregator                       |           |      |
| ChannelPromiseNotifier                         |           |      |
| CoalescingBufferQueue                          |           |      |
| CombinedChannelDuplexHandler                   |           |      |
| DefaultAddressedEnvelope                       |           |      |
| DefaultChannelConfig                           |           |      |
| DefaultChannelId                               |           |      |
| DefaultChannelPipeline                         |           |      |
| DefaultChannelProgressivePromise               |           |      |
| DefaultChannelPromise                          |           |      |
| DefaultEventLoop                               |           |      |
| DefaultEventLoopGroup                          |           |      |
| DefaultFileRegion                              |           |      |
| DefaultMaxBytesRecvByteBufAllocator            |           |      |
| DefaultMaxMessagesRecvByteBufAllocator         |           |      |
| DefaultMessageSizeEstimator                    |           |      |
| DefaultSelectStrategyFactory                   |           |      |
| DelegatingChannelPromiseNotifier               |           |      |
| FixedRecvByteBufAllocator                      |           |      |
| MultithreadEventLoopGroup                      |           |      |
| PendingWriteQueue                              |           |      |
| PreferHeapByteBufAllocator                     |           |      |
| RecvByteBufAllocator.DelegatingHandle          |           |      |
| ReflectiveChannelFactory                       |           |      |
| ServerChannelRecvByteBufAllocator              |           |      |
| SimpleChannelInboundHandler                    |           |      |
| SimpleUserEventChannelHandler                  |           |      |
| SingleThreadEventLoop                          |           |      |
| SingleThreadEventLoop.ChannelsReadOnlyIterator |           |      |
| ThreadPerChannelEventLoop                      |           |      |
| ThreadPerChannelEventLoopGroup                 |           |      |
| VoidChannelPromise                             |           |      |
| WriteBufferWaterMark                           |           |      |
|                                                |           |      |
| Exceptions                                     |           |      |
|                                                |           |      |
| ChannelException                               | exception |      |
| ChannelPipelineException                       | exception |      |
| ConnectTimeoutException                        | exception |      |
| EventLoopException                             | exception |      |
|                                                |           |      |
| Annotation Types                               |           |      |
|                                                |           |      |
| ChannelHandler.Sharable                        |           |      |






### io.netty.channel.embedded

EmbeddedChannel

### io.netty.channel.epoll



| io.netty.channel.epoll           | 类型     |      |
| -------------------------------- | -------- | ---- |
| Classes                          |          |      |
|                                  |          |      |
| AbstractEpollServerChannel       | abstract |      |
| AbstractEpollStreamChannel       | abstract |      |
| Epoll                            |          |      |
| EpollChannelConfig               |          |      |
| EpollChannelOption               |          |      |
| EpollDatagramChannel             |          |      |
| EpollDatagramChannelConfig       |          |      |
| EpollDomainDatagramChannel       |          |      |
| EpollDomainDatagramChannelConfig |          |      |
| EpollDomainSocketChannel         |          |      |
| EpollDomainSocketChannelConfig   |          |      |
| EpollEventArray                  |          |      |
| EpollEventLoop                   |          |      |
| EpollEventLoopGroup              |          |      |
| EpollServerChannelConfig         |          |      |
| EpollServerDomainSocketChannel   |          |      |
| EpollServerSocketChannel         |          |      |
| EpollServerSocketChannelConfig   |          |      |
| EpollSocketChannel               |          |      |
| EpollSocketChannelConfig         |          |      |
| EpollTcpInfo                     |          |      |
| LinuxSocket                      |          |      |
| Native                           |          |      |
| SegmentedDatagramPacket          |          |      |
| VSockAddress                     |          |      |
|                                  |          |      |
| Enums                            |          |      |
|                                  |          |      |
| EpollMode                        |          |      |





### io.netty.channel.group

| io.netty.channel.group     | 类型      |      |
| -------------------------- | --------- | ---- |
| Interfaces                 |           |      |
|                            |           |      |
| ChannelGroup               | interface |      |
| ChannelGroupFuture         | interface |      |
| ChannelGroupFutureListener | interface |      |
| ChannelMatcher             | interface |      |
|                            |           |      |
| Classes                    |           |      |
|                            |           |      |
| ChannelMatchers            |           |      |
| DefaultChannelGroup        |           |      |
|                            |           |      |
| Exceptions                 |           |      |
|                            |           |      |
| ChannelGroupException      |           |      |



### io.netty.channel.internal

ChannelUtils



### io.netty.channel.kqueue





| io.netty.channel.kqueue           | 类型 |      |
| --------------------------------- | ---- | ---- |
| Classes                           |      |      |
|                                   |      |      |
| AbstractKQueueServerChannel       |      |      |
| AbstractKQueueStreamChannel       |      |      |
| AcceptFilter                      |      |      |
| KQueue                            |      |      |
| KQueueChannelConfig               |      |      |
| KQueueChannelOption               |      |      |
| KQueueDatagramChannel             |      |      |
| KQueueDatagramChannelConfig       |      |      |
| KQueueDomainDatagramChannel       |      |      |
| KQueueDomainDatagramChannelConfig |      |      |
| KQueueDomainSocketChannel         |      |      |
| KQueueDomainSocketChannelConfig   |      |      |
| KQueueEventLoopGroup              |      |      |
| KQueueServerChannelConfig         |      |      |
| KQueueServerDomainSocketChannel   |      |      |
| KQueueServerSocketChannel         |      |      |
| KQueueServerSocketChannelConfig   |      |      |
| KQueueSocketChannel               |      |      |
| KQueueSocketChannelConfig         |      |      |



### io.netty.channel.local





| io.netty.channel.local | 类型 |      |
| ---------------------- | ---- | ---- |
| Classes                |      |      |
|                        |      |      |
| LocalAddress           |      |      |
| LocalChannel           |      |      |
| LocalEventLoopGroup    |      |      |
| LocalServerChannel     |      |      |



### io.netty.channel.nio

| io.netty.channel.nio         | 类型      |      |
| ---------------------------- | --------- | ---- |
| Interfaces                   |           |      |
|                              |           |      |
| AbstractNioChannel.NioUnsafe | interface |      |
| NioTask                      | interface |      |
|                              |           |      |
| Classes                      |           |      |
|                              |           |      |
| AbstractNioByteChannel       |           |      |
| AbstractNioChannel           |           |      |
| AbstractNioMessageChannel    |           |      |
| NioEventLoop                 |           |      |
| NioEventLoopGroup            |           |      |



### io.netty.channel.oio



| io.netty.channel.oio      | 类型 |      |
| ------------------------- | ---- | ---- |
| Classes                   |      |      |
|                           |      |      |
| AbstractOioByteChannel    |      |      |
| AbstractOioChannel        |      |      |
| AbstractOioMessageChannel |      |      |
| OioByteStreamChannel      |      |      |
| OioEventLoopGroup         |      |      |



### io.netty.channel.pool

|                                       | 类型      |      |
| ------------------------------------- | --------- | ---- |
| Interfaces                            |           |      |
|                                       |           |      |
| ChannelHealthChecker                  | interface |      |
| ChannelPool                           | interface |      |
| ChannelPoolHandler                    | interface |      |
| ChannelPoolMap                        | interface |      |
|                                       |           |      |
| Classes                               |           |      |
|                                       |           |      |
| AbstractChannelPoolHandler            |           |      |
| AbstractChannelPoolMap                |           |      |
| FixedChannelPool                      |           |      |
| SimpleChannelPool                     |           |      |
|                                       |           |      |
| Enums                                 |           |      |
|                                       |           |      |
| FixedChannelPool.AcquireTimeoutAction |           |      |

### io.netty.channel.rxtx

|                             | 类型      |      |
| --------------------------- | --------- | ---- |
| Interfaces                  |           |      |
|                             |           |      |
| RxtxChannelConfig           | interface |      |
|                             |           |      |
| Classes                     |           |      |
|                             |           |      |
| RxtxChannel                 |           |      |
| RxtxChannelOption           |           |      |
| RxtxDeviceAddress           |           |      |
|                             |           |      |
| Enums                       |           |      |
|                             |           |      |
| RxtxChannelConfig.Databits  |           |      |
| RxtxChannelConfig.Paritybit |           |      |
| RxtxChannelConfig.Stopbits  |           |      |



### io.netty.channel.sctp



| Interfaces                     | 类型      |      |
| ------------------------------ | --------- | ---- |
|                                |           |      |
| SctpChannel                    | interface |      |
| SctpChannelConfig              | interface |      |
| SctpServerChannel              | interface |      |
| SctpServerChannelConfig        | interface |      |
|                                |           |      |
| Classes                        |           |      |
|                                |           |      |
| DefaultSctpChannelConfig       |           |      |
| DefaultSctpServerChannelConfig |           |      |
| SctpChannelOption              |           |      |
| SctpMessage                    |           |      |
| SctpNotificationHandler        |           |      |



### io.netty.channel.sctp.nio



|                      | 类型 |      |
| -------------------- | ---- | ---- |
| Classes              |      |      |
|                      |      |      |
| NioSctpChannel       |      |      |
| NioSctpServerChannel |      |      |





### io.netty.channel.sctp.oio





| io.netty.channel.sctp.oio | 类型 |      |
| ------------------------- | ---- | ---- |
| Classes                   |      |      |
|                           |      |      |
| OioSctpChannel            |      |      |
| OioSctpServerChannel      |      |      |



### io.netty.channel.socket

| io.netty.channel.socket          | 类型      |      |
| -------------------------------- | --------- | ---- |
| Interfaces                       |           |      |
|                                  |           |      |
| DatagramChannel                  | interface |      |
| DatagramChannelConfig            | interface |      |
| DuplexChannel                    | interface |      |
| DuplexChannelConfig              | interface |      |
| ServerSocketChannel              | interface |      |
| ServerSocketChannelConfig        | interface |      |
| SocketChannel                    | interface |      |
| SocketChannelConfig              | interface |      |
|                                  |           |      |
| Classes                          |           |      |
|                                  |           |      |
| ChannelInputShutdownEvent        |           |      |
| ChannelInputShutdownReadComplete |           |      |
| ChannelOutputShutdownEvent       |           |      |
| DatagramPacket                   |           |      |
| DefaultDatagramChannelConfig     |           |      |
| DefaultServerSocketChannelConfig |           |      |
| DefaultSocketChannelConfig       |           |      |
|                                  |           |      |
| Enums                            |           |      |
|                                  |           |      |
| InternetProtocolFamily           |           |      |
|                                  |           |      |
| Exceptions                       |           |      |
|                                  |           |      |
| ChannelOutputShutdownException   |           |      |







#### io.netty.channel.socket.nio



| io.netty.channel.socket.nio | 类型 |      |
| --------------------------- | ---- | ---- |
| Classes                     |      |      |
|                             |      |      |
| NioChannelOption            |      |      |
| NioDatagramChannel          |      |      |
| NioServerSocketChannel      |      |      |
| NioSocketChannel            |      |      |



#### io.netty.channel.socket.oio



| io.netty.channel.socket.oio         | 类型      |      |
| ----------------------------------- | --------- | ---- |
| Interfaces                          |           |      |
|                                     |           |      |
| OioDatagramChannelConfig            | interface |      |
| OioServerSocketChannelConfig        | interface |      |
| OioSocketChannelConfig              | interface |      |
|                                     |           |      |
| Classes                             |           |      |
|                                     |           |      |
| DefaultOioServerSocketChannelConfig |           |      |
| DefaultOioSocketChannelConfig       |           |      |
| OioDatagramChannel                  |           |      |
| OioServerSocketChannel              |           |      |
| OioSocketChannel                    |           |      |



### io.netty.channel.udt



| io.netty.channel.udt          | 类型      |      |
| ----------------------------- | --------- | ---- |
| Interfaces                    |           |      |
|                               |           |      |
| UdtChannel                    | interface |      |
| UdtChannelConfig              | interface |      |
| UdtServerChannel              | interface |      |
| UdtServerChannelConfig        | interface |      |
|                               |           |      |
| Classes                       |           |      |
|                               |           |      |
| DefaultUdtChannelConfig       |           |      |
| DefaultUdtServerChannelConfig |           |      |
| UdtChannelOption              |           |      |
| UdtMessage                    |           |      |



#### io.netty.channel.udt.nio



| io.netty.channel.udt.nio       | 类型 |      |
| ------------------------------ | ---- | ---- |
| Classes                        |      |      |
|                                |      |      |
| NioUdtAcceptorChannel          |      |      |
| NioUdtByteAcceptorChannel      |      |      |
| NioUdtByteConnectorChannel     |      |      |
| NioUdtByteRendezvousChannel    |      |      |
| NioUdtMessageAcceptorChannel   |      |      |
| NioUdtMessageConnectorChannel  |      |      |
| NioUdtMessageRendezvousChannel |      |      |
| NioUdtProvider                 |      |      |



### io.netty.channel.unix



| io.netty.channel.unix           | 类型      |      |
| ------------------------------- | --------- | ---- |
| Interfaces                      |           |      |
|                                 |           |      |
| DomainDatagramChannel           | interface |      |
| DomainDatagramChannelConfig     | interface |      |
| DomainSocketChannel             | interface |      |
| DomainSocketChannelConfig       | interface |      |
| ServerDomainSocketChannel       | interface |      |
| UnixChannel                     | interface |      |
|                                 |           |      |
| Classes                         |           |      |
|                                 |           |      |
| Buffer                          |           |      |
| DatagramSocketAddress           |           |      |
| DomainDatagramPacket            |           |      |
| DomainDatagramSocketAddress     |           |      |
| DomainSocketAddress             |           |      |
| Errors                          |           |      |
| FileDescriptor                  |           |      |
| GenericUnixChannelOption        |           |      |
| IntegerUnixChannelOption        |           |      |
| IovArray                        |           |      |
| Limits                          |           |      |
| NativeInetAddress               |           |      |
| PeerCredentials                 |           |      |
| PreferredDirectByteBufAllocator |           |      |
| RawUnixChannelOption            |           |      |
| SegmentedDatagramPacket         |           |      |
| Socket                          |           |      |
| SocketWritableByteChannel       |           |      |
| Unix                            |           |      |
| UnixChannelOption               |           |      |
| UnixChannelUtil                 |           |      |
|                                 |           |      |
| Enums                           |           |      |
|                                 |           |      |
| DomainSocketReadMode            |           |      |
|                                 |           |      |
| Exceptions                      |           |      |
|                                 |           |      |
| Errors.NativeIoException        |           |      |



## io.netty.handler











| io.netty.handler.address     | 类型 |      |
| ---------------------------- | ---- | ---- |
| Classes                      |      |      |
|                              |      |      |
| DynamicAddressConnectHandler |      |      |
| ResolveAddressHandler        |      |      |





#### io.netty.handler.codec



| io.netty.handler.codec            | 类型      |      |
| --------------------------------- | --------- | ---- |
|                                   |           |      |
| Interfaces                        |           |      |
|                                   |           |      |
| ByteToMessageDecoder.Cumulator    | interface |      |
| DecoderResultProvider             | interface |      |
| DefaultHeaders.NameValidator      | interface |      |
| DefaultHeaders.ValueValidator     | interface |      |
| Headers                           | interface |      |
| ValueConverter                    | interface |      |
|                                   |           |      |
| Classes                           |           |      |
|                                   |           |      |
| AsciiHeadersEncoder               |           |      |
| ByteToMessageCodec                |           |      |
| ByteToMessageDecoder              |           |      |
| CharSequenceValueConverter        |           |      |
| DatagramPacketDecoder             |           |      |
| DatagramPacketEncoder             |           |      |
| DateFormatter                     |           |      |
| DecoderResult                     |           |      |
| DefaultHeaders                    |           |      |
| DefaultHeaders.HeaderEntry        |           |      |
| DefaultHeadersImpl                |           |      |
| DelimiterBasedFrameDecoder        |           |      |
| Delimiters                        |           |      |
| EmptyHeaders                      |           |      |
| FixedLengthFrameDecoder           |           |      |
| HeadersUtils                      |           |      |
| LengthFieldBasedFrameDecoder      |           |      |
| LengthFieldPrepender              |           |      |
| LineBasedFrameDecoder             |           |      |
| MessageAggregator                 |           |      |
| MessageToByteEncoder              |           |      |
| MessageToMessageCodec             |           |      |
| MessageToMessageDecoder           |           |      |
| MessageToMessageEncoder           |           |      |
| ProtocolDetectionResult           |           |      |
| ReplayingDecoder                  |           |      |
| UnsupportedValueConverter         |           |      |
|                                   |           |      |
| Enums                             |           |      |
|                                   |           |      |
| AsciiHeadersEncoder.NewlineType   |           |      |
| AsciiHeadersEncoder.SeparatorType |           |      |
| ProtocolDetectionState            |           |      |
|                                   |           |      |
| Exceptions                        |           |      |
|                                   |           |      |
| CodecException                    | exception |      |
| CorruptedFrameException           | exception |      |
| DecoderException                  | exception |      |
| EncoderException                  | exception |      |
| MessageAggregationException       | exception |      |
| PrematureChannelClosureException  | exception |      |
| TooLongFrameException             | exception |      |
| UnsupportedMessageTypeException   | exception |      |
| UnsupportedMessageTypeException   | exception |      |





#### io.netty.handler.codec.base64



| io.netty.handler.codec.base64 | 类型 |      |
| ----------------------------- | ---- | ---- |
| Classes                       |      |      |
|                               |      |      |
| Base64                        |      |      |
| Base64Decoder                 |      |      |
| Base64Encoder                 |      |      |
|                               |      |      |
| Enums                         |      |      |
|                               |      |      |
| Base64Dialect                 |      |      |



#### io.netty.handler.codec.bytes



| io.netty.handler.codec.bytes | 类型 |      |
| ---------------------------- | ---- | ---- |
| Classes                      |      |      |
|                              |      |      |
| ByteArrayDecoder             |      |      |
| ByteArrayEncoder             |      |      |





io.netty.handler.codec.compression





| io.netty.handler.codec.compression | 类型      |      |
| ---------------------------------- | --------- | ---- |
| Interfaces                         |           |      |
|                                    |           |      |
| CompressionOptions                 | interface |      |
|                                    |           |      |
| Classes                            |           |      |
|                                    |           |      |
| Brotli                             |           |      |
| BrotliDecoder                      |           |      |
| BrotliEncoder                      |           |      |
| BrotliOptions                      |           |      |
| Bzip2Decoder                       |           |      |
| Bzip2Encoder                       |           |      |
| DeflateOptions                     |           |      |
| FastLzFrameDecoder                 |           |      |
| FastLzFrameEncoder                 |           |      |
| GzipOptions                        |           |      |
| JdkZlibDecoder                     |           |      |
| JdkZlibEncoder                     |           |      |
| JZlibDecoder                       |           |      |
| JZlibEncoder                       |           |      |
| Lz4FrameDecoder                    |           |      |
| Lz4FrameEncoder                    |           |      |
| Lz4XXHash32                        |           |      |
| LzfDecoder                         |           |      |
| LzfEncoder                         |           |      |
| LzmaFrameEncoder                   |           |      |
| Snappy                             |           |      |
| SnappyFramedDecoder                |           |      |
| SnappyFrameDecoder                 |           |      |
| SnappyFramedEncoder                |           |      |
| SnappyFrameEncoder                 |           |      |
| StandardCompressionOptions         |           |      |
| ZlibCodecFactory                   |           |      |
| ZlibDecoder                        |           |      |
| ZlibEncoder                        |           |      |
| Zstd                               |           |      |
| ZstdEncoder                        |           |      |
| ZstdOptions                        |           |      |
|                                    |           |      |
| Enums                              |           |      |
|                                    |           |      |
| ZlibWrapper                        |           |      |
|                                    |           |      |
| Exceptions                         |           |      |
|                                    |           |      |
| CompressionException               |           |      |
| DecompressionException             |           |      |



#### io.netty.handler.codec.dns



| io.netty.handler.codec.dns   | 类型      |      |
| ---------------------------- | --------- | ---- |
| Interfaces                   |           |      |
|                              |           |      |
| DnsMessage                   | interface |      |
| DnsOptEcsRecord              | interface |      |
| DnsOptPseudoRecord           | interface |      |
| DnsPtrRecord                 | interface |      |
| DnsQuery                     | interface |      |
| DnsQuestion                  | interface |      |
| DnsRawRecord                 | interface |      |
| DnsRecord                    | interface |      |
| DnsRecordDecoder             | interface |      |
| DnsRecordEncoder             | interface |      |
| DnsResponse                  | interface |      |
|                              |           |      |
| Classes                      |           |      |
|                              |           |      |
| AbstractDnsMessage           |           |      |
| AbstractDnsOptPseudoRrRecord |           |      |
| AbstractDnsRecord            |           |      |
| DatagramDnsQuery             |           |      |
| DatagramDnsQueryDecoder      |           |      |
| DatagramDnsQueryEncoder      |           |      |
| DatagramDnsResponse          |           |      |
| DatagramDnsResponseDecoder   |           |      |
| DatagramDnsResponseEncoder   |           |      |
| DefaultDnsOptEcsRecord       |           |      |
| DefaultDnsPtrRecord          |           |      |
| DefaultDnsQuery              |           |      |
| DefaultDnsQuestion           |           |      |
| DefaultDnsRawRecord          |           |      |
| DefaultDnsRecordDecoder      |           |      |
| DefaultDnsRecordEncoder      |           |      |
| DefaultDnsResponse           |           |      |
| DnsOpCode                    |           |      |
| DnsRecordType                |           |      |
| DnsResponseCode              |           |      |
| TcpDnsQueryDecoder           |           |      |
| TcpDnsQueryEncoder           |           |      |
| TcpDnsResponseDecoder        |           |      |
| TcpDnsResponseEncoder        |           |      |
|                              |           |      |
| Enums                        |           |      |
|                              |           |      |
| DnsSection                   |           |      |





#### io.netty.handler.codec.haproxy





| io.netty.handler.codec.haproxy           | 类型 |      |
| ---------------------------------------- | ---- | ---- |
| Classes                                  |      |      |
|                                          |      |      |
| HAProxyMessage                           |      |      |
| HAProxyMessageDecoder                    |      |      |
| HAProxyMessageEncoder                    |      |      |
| HAProxySSLTLV                            |      |      |
| HAProxyTLV                               |      |      |
|                                          |      |      |
| Enums                                    |      |      |
|                                          |      |      |
| HAProxyCommand                           |      |      |
| HAProxyProtocolVersion                   |      |      |
| HAProxyProxiedProtocol                   |      |      |
| HAProxyProxiedProtocol.AddressFamily     |      |      |
| HAProxyProxiedProtocol.TransportProtocol |      |      |
| HAProxyTLV.Type                          |      |      |
|                                          |      |      |
| Exceptions                               |      |      |
|                                          |      |      |
| HAProxyProtocolException                 |      |      |



#### io.netty.handler.codec.http



| io.netty.handler.codec.http                  | 类型      |      |
| -------------------------------------------- | --------- | ---- |
| Interfaces                                   |           |      |
|                                              |           |      |
| Cookie                                       | interface |      |
| FullHttpMessage                              | interface |      |
| FullHttpRequest                              | interface |      |
| FullHttpResponse                             | interface |      |
| HttpClientUpgradeHandler.SourceCodec         | interface |      |
| HttpClientUpgradeHandler.UpgradeCodec        | interface |      |
| HttpContent                                  | interface |      |
| HttpMessage                                  | interface |      |
| HttpObject                                   | interface |      |
| HttpRequest                                  | interface |      |
| HttpResponse                                 | interface |      |
| HttpServerUpgradeHandler.SourceCodec         | interface |      |
| HttpServerUpgradeHandler.UpgradeCodec        | interface |      |
| HttpServerUpgradeHandler.UpgradeCodecFactory | interface |      |
| LastHttpContent                              | interface |      |
|                                              |           |      |
| Classes                                      |           |      |
|                                              |           |      |
| ClientCookieEncoder                          |           |      |
| CombinedHttpHeaders                          |           |      |
| CookieDecoder                                |           |      |
| DefaultCookie                                |           |      |
| DefaultFullHttpRequest                       |           |      |
| DefaultFullHttpResponse                      |           |      |
| DefaultHttpContent                           |           |      |
| DefaultHttpHeaders                           |           |      |
| DefaultHttpMessage                           |           |      |
| DefaultHttpObject                            |           |      |
| DefaultHttpRequest                           |           |      |
| DefaultHttpResponse                          |           |      |
| DefaultLastHttpContent                       |           |      |
| EmptyHttpHeaders                             |           |      |
| HttpChunkedInput                             |           |      |
| HttpClientCodec                              |           |      |
| HttpClientUpgradeHandler                     |           |      |
| HttpConstants                                |           |      |
| HttpContentCompressor                        |           |      |
| HttpContentDecoder                           |           |      |
| HttpContentDecompressor                      |           |      |
| HttpContentEncoder                           |           |      |
| HttpContentEncoder.Result                    |           |      |
| HttpExpectationFailedEvent                   |           |      |
| HttpHeaderDateFormat                         |           |      |
| HttpHeaderNames                              |           |      |
| HttpHeaders                                  |           |      |
| HttpHeaders.Names                            |           |      |
| HttpHeaders.Values                           |           |      |
| HttpHeaderValidationUtil                     |           |      |
| HttpHeaderValues                             |           |      |
| HttpMessageDecoderResult                     |           |      |
| HttpMethod                                   |           |      |
| HttpObjectAggregator                         |           |      |
| HttpObjectDecoder                            |           |      |
| HttpObjectEncoder                            |           |      |
| HttpRequestDecoder                           |           |      |
| HttpRequestEncoder                           |           |      |
| HttpResponseDecoder                          |           |      |
| HttpResponseEncoder                          |           |      |
| HttpResponseStatus                           |           |      |
| HttpScheme                                   |           |      |
| HttpServerCodec                              |           |      |
| HttpServerExpectContinueHandler              |           |      |
| HttpServerKeepAliveHandler                   |           |      |
| HttpServerUpgradeHandler                     |           |      |
| HttpServerUpgradeHandler.UpgradeEvent        |           |      |
| HttpUtil                                     |           |      |
| HttpVersion                                  |           |      |
| QueryStringDecoder                           |           |      |
| QueryStringEncoder                           |           |      |
| ReadOnlyHttpHeaders                          |           |      |
| ServerCookieEncoder                          |           |      |
|                                              |           |      |
| Enums                                        |           |      |
|                                              |           |      |
| HttpClientUpgradeHandler.UpgradeEvent        |           |      |
| HttpStatusClass                              |           |      |
|                                              |           |      |
| Exceptions                                   |           |      |
|                                              |           |      |
| TooLongHttpContentException                  |           |      |
| TooLongHttpHeaderException                   |           |      |
| TooLongHttpLineException                     |           |      |



##### io.netty.handler.codec.http.cookie

| io.netty.handler.codec.http.cookie | 类型      |      |
| ---------------------------------- | --------- | ---- |
| Interfaces                         |           |      |
|                                    |           |      |
| Cookie                             | interface |      |
|                                    |           |      |
| Classes                            |           |      |
|                                    |           |      |
| ClientCookieDecoder                |           |      |
| ClientCookieEncoder                |           |      |
| CookieDecoder                      |           |      |
| CookieEncoder                      |           |      |
| CookieHeaderNames                  |           |      |
| DefaultCookie                      |           |      |
| ServerCookieDecoder                |           |      |
| ServerCookieEncoder                |           |      |
|                                    |           |      |
| Enums                              |           |      |
|                                    |           |      |
| CookieHeaderNames.SameSite         |           |      |





##### io.netty.handler.codec.http.cors

| io.netty.handler.codec.http.cors | 类型 |      |
| -------------------------------- | ---- | ---- |
| Classes                          |      |      |
|                                  |      |      |
| CorsConfig                       |      |      |
| CorsConfig.Builder               |      |      |
| CorsConfig.DateValueGenerator    |      |      |
| CorsConfigBuilder                |      |      |
| CorsHandler                      |      |      |

##### io.netty.handler.codec.http.multipart

| io.netty.handler.codec.http.multipart                | 类型      |      |
| ---------------------------------------------------- | --------- | ---- |
| Interfaces                                           |           |      |
|                                                      |           |      |
| Attribute                                            | interface |      |
| FileUpload                                           | interface |      |
| HttpData                                             | interface |      |
| HttpDataFactory                                      | interface |      |
| InterfaceHttpData                                    | interface |      |
| InterfaceHttpPostRequestDecoder                      | interface |      |
|                                                      |           |      |
| Classes                                              |           |      |
|                                                      |           |      |
| AbstractDiskHttpData                                 |           |      |
| AbstractHttpData                                     |           |      |
| AbstractMemoryHttpData                               |           |      |
| DefaultHttpDataFactory                               |           |      |
| DiskAttribute                                        |           |      |
| DiskFileUpload                                       |           |      |
| HttpPostMultipartRequestDecoder                      |           |      |
| HttpPostRequestDecoder                               |           |      |
| HttpPostRequestEncoder                               |           |      |
| HttpPostStandardRequestDecoder                       |           |      |
| MemoryAttribute                                      |           |      |
| MemoryFileUpload                                     |           |      |
| MixedAttribute                                       |           |      |
| MixedFileUpload                                      |           |      |
|                                                      |           |      |
| Enums                                                |           |      |
|                                                      |           |      |
| HttpPostRequestDecoder.MultiPartStatus               |           |      |
| HttpPostRequestEncoder.EncoderMode                   |           |      |
| InterfaceHttpData.HttpDataType                       |           |      |
|                                                      |           |      |
| Exceptions                                           |           |      |
|                                                      |           |      |
| HttpPostRequestDecoder.EndOfDataDecoderException     |           |      |
| HttpPostRequestDecoder.ErrorDataDecoderException     |           |      |
| HttpPostRequestDecoder.NotEnoughDataDecoderException |           |      |
| HttpPostRequestEncoder.ErrorDataEncoderException     |           |      |



##### io.netty.handler.codec.http.websocketx







| io.netty.handler.codec.http.websocketx                   | 类型      |      |
| -------------------------------------------------------- | --------- | ---- |
| Interfaces                                               |           |      |
|                                                          |           |      |
| WebSocketFrameDecoder                                    | interface |      |
| WebSocketFrameEncoder                                    | interface |      |
|                                                          |           |      |
| Classes                                                  |           |      |
|                                                          |           |      |
| BinaryWebSocketFrame                                     |           |      |
| CloseWebSocketFrame                                      |           |      |
| ContinuationWebSocketFrame                               |           |      |
| PingWebSocketFrame                                       |           |      |
| PongWebSocketFrame                                       |           |      |
| TextWebSocketFrame                                       |           |      |
| Utf8FrameValidator                                       |           |      |
| WebSocket00FrameDecoder                                  |           |      |
| WebSocket00FrameEncoder                                  |           |      |
| WebSocket07FrameDecoder                                  |           |      |
| WebSocket07FrameEncoder                                  |           |      |
| WebSocket08FrameDecoder                                  |           |      |
| WebSocket08FrameEncoder                                  |           |      |
| WebSocket13FrameDecoder                                  |           |      |
| WebSocket13FrameEncoder                                  |           |      |
| WebSocketChunkedInput                                    |           |      |
| WebSocketClientHandshaker                                |           |      |
| WebSocketClientHandshaker00                              |           |      |
| WebSocketClientHandshaker07                              |           |      |
| WebSocketClientHandshaker08                              |           |      |
| WebSocketClientHandshaker13                              |           |      |
| WebSocketClientHandshakerFactory                         |           |      |
| WebSocketClientProtocolConfig                            |           |      |
| WebSocketClientProtocolConfig.Builder                    |           |      |
| WebSocketClientProtocolHandler                           |           |      |
| WebSocketCloseStatus                                     |           |      |
| WebSocketDecoderConfig                                   |           |      |
| WebSocketDecoderConfig.Builder                           |           |      |
| WebSocketFrame                                           |           |      |
| WebSocketFrameAggregator                                 |           |      |
| WebSocketScheme                                          |           |      |
| WebSocketServerHandshaker                                |           |      |
| WebSocketServerHandshaker00                              |           |      |
| WebSocketServerHandshaker07                              |           |      |
| WebSocketServerHandshaker08                              |           |      |
| WebSocketServerHandshaker13                              |           |      |
| WebSocketServerHandshakerFactory                         |           |      |
| WebSocketServerProtocolConfig                            |           |      |
| WebSocketServerProtocolConfig.Builder                    |           |      |
| WebSocketServerProtocolHandler                           |           |      |
| WebSocketServerProtocolHandler.HandshakeComplete         |           |      |
|                                                          |           |      |
| Enums                                                    |           |      |
|                                                          |           |      |
| WebSocketClientProtocolHandler.ClientHandshakeStateEvent |           |      |
| WebSocketServerProtocolHandler.ServerHandshakeStateEvent |           |      |
| WebSocketVersion                                         |           |      |
|                                                          |           |      |
| Exceptions                                               |           |      |
|                                                          |           |      |
| CorruptedWebSocketFrameException                         |           |      |
| WebSocketClientHandshakeException                        |           |      |
| WebSocketHandshakeException                              |           |      |
| WebSocketServerHandshakeException                        |           |      |



##### io.netty.handler.codec.http.websocketx.extensions

| io.netty.handler.codec.http.websocketx.extensions | 类型      |      |
| ------------------------------------------------- | --------- | ---- |
| Interfaces                                        |           |      |
|                                                   |           |      |
| WebSocketClientExtension                          | interface |      |
| WebSocketClientExtensionHandshaker                | interface |      |
| WebSocketExtension                                | interface |      |
| WebSocketExtensionFilter                          | interface |      |
| WebSocketExtensionFilterProvider                  | interface |      |
| WebSocketServerExtension                          | interface |      |
| WebSocketServerExtensionHandshaker                | interface |      |
|                                                   |           |      |
| Classes                                           |           |      |
|                                                   |           |      |
| WebSocketClientExtensionHandler                   |           |      |
| WebSocketExtensionData                            |           |      |
| WebSocketExtensionDecoder                         |           |      |
| WebSocketExtensionEncoder                         |           |      |
| WebSocketExtensionUtil                            |           |      |
| WebSocketServerExtensionHandler                   |           |      |

##### io.netty.handler.codec.http.websocketx.extensions.compression



| io.netty.handler.codec.http.websocketx.extensions.compression | 类型 |      |
| ------------------------------------------------------------ | ---- | ---- |
| Classes                                                      |      |      |
|                                                              |      |      |
| DeflateFrameClientExtensionHandshaker                        |      |      |
| DeflateFrameServerExtensionHandshaker                        |      |      |
| PerMessageDeflateClientExtensionHandshaker                   |      |      |
| PerMessageDeflateServerExtensionHandshaker                   |      |      |
| WebSocketClientCompressionHandler                            |      |      |
| WebSocketServerCompressionHandler                            |      |      |



##### io.netty.handler.codec.http2



| io.netty.handler.codec.http2                                 | 类型      |      |
| ------------------------------------------------------------ | --------- | ---- |
| Interfaces                                                   |           |      |
|                                                              |           |      |
| Http2Connection                                              | interface |      |
| Http2Connection.Endpoint                                     | interface |      |
| Http2Connection.Listener                                     | interface |      |
| Http2Connection.PropertyKey                                  | interface |      |
| Http2ConnectionDecoder                                       | interface |      |
| Http2ConnectionEncoder                                       | interface |      |
| Http2DataFrame                                               | interface |      |
| Http2DataWriter                                              | interface |      |
| Http2FlowController                                          | interface |      |
| Http2Frame                                                   | interface |      |
| Http2FrameListener                                           | interface |      |
| Http2FrameReader                                             | interface |      |
| Http2FrameReader.Configuration                               | interface |      |
| Http2FrameSizePolicy                                         | interface |      |
| Http2FrameStream                                             | interface |      |
| Http2FrameStreamVisitor                                      | interface |      |
| Http2FrameWriter                                             | interface |      |
| Http2FrameWriter.Configuration                               | interface |      |
| Http2GoAwayFrame                                             | interface |      |
| Http2Headers                                                 | interface |      |
| Http2HeadersDecoder                                          | interface |      |
| Http2HeadersDecoder.Configuration                            | interface |      |
| Http2HeadersEncoder                                          | interface |      |
| Http2HeadersEncoder.Configuration                            | interface |      |
| Http2HeadersEncoder.SensitivityDetector                      | interface |      |
| Http2HeadersFrame                                            | interface |      |
| Http2LifecycleManager                                        | interface |      |
| Http2LocalFlowController                                     | interface |      |
| Http2PingFrame                                               | interface |      |
| Http2PriorityFrame                                           | interface |      |
| Http2PromisedRequestVerifier                                 | interface |      |
| Http2PushPromiseFrame                                        | interface |      |
| Http2RemoteFlowController                                    | interface |      |
| Http2RemoteFlowController.FlowControlled                     | interface |      |
| Http2RemoteFlowController.Listener                           | interface |      |
| Http2ResetFrame                                              | interface |      |
| Http2SettingsAckFrame                                        | interface |      |
| Http2SettingsFrame                                           | interface |      |
| Http2SettingsReceivedConsumer                                | interface |      |
| Http2Stream                                                  | interface |      |
| Http2StreamChannel                                           | interface |      |
| Http2StreamFrame                                             | interface |      |
| Http2StreamVisitor                                           | interface |      |
| Http2UnknownFrame                                            | interface |      |
| Http2WindowUpdateFrame                                       | interface |      |
| StreamByteDistributor                                        | interface |      |
| StreamByteDistributor.StreamState                            | interface |      |
| StreamByteDistributor.Writer                                 | interface |      |
|                                                              |           |      |
| Classes                                                      |           |      |
|                                                              |           |      |
| AbstractHttp2ConnectionHandlerBuilder                        |           |      |
| AbstractHttp2StreamFrame                                     |           |      |
| AbstractInboundHttp2ToHttpAdapterBuilder                     |           |      |
| CharSequenceMap                                              |           |      |
| CleartextHttp2ServerUpgradeHandler                           |           |      |
| CleartextHttp2ServerUpgradeHandler.PriorKnowledgeUpgradeEvent |           |      |
| CompressorHttp2ConnectionEncoder                             |           |      |
| DecoratingHttp2ConnectionDecoder                             |           |      |
| DecoratingHttp2ConnectionEncoder                             |           |      |
| DecoratingHttp2FrameWriter                                   |           |      |
| DefaultHttp2Connection                                       |           |      |
| DefaultHttp2ConnectionDecoder                                |           |      |
| DefaultHttp2ConnectionEncoder                                |           |      |
| DefaultHttp2DataFrame                                        |           |      |
| DefaultHttp2FrameReader                                      |           |      |
| DefaultHttp2FrameWriter                                      |           |      |
| DefaultHttp2GoAwayFrame                                      |           |      |
| DefaultHttp2Headers                                          |           |      |
| DefaultHttp2HeadersDecoder                                   |           |      |
| DefaultHttp2HeadersEncoder                                   |           |      |
| DefaultHttp2HeadersFrame                                     |           |      |
| DefaultHttp2LocalFlowController                              |           |      |
| DefaultHttp2PingFrame                                        |           |      |
| DefaultHttp2PriorityFrame                                    |           |      |
| DefaultHttp2PushPromiseFrame                                 |           |      |
| DefaultHttp2RemoteFlowController                             |           |      |
| DefaultHttp2ResetFrame                                       |           |      |
| DefaultHttp2SettingsFrame                                    |           |      |
| DefaultHttp2UnknownFrame                                     |           |      |
| DefaultHttp2WindowUpdateFrame                                |           |      |
| DelegatingDecompressorFrameListener                          |           |      |
| EmptyHttp2Headers                                            |           |      |
| Http2ChannelDuplexHandler                                    |           |      |
| Http2ClientUpgradeCodec                                      |           |      |
| Http2CodecUtil                                               |           |      |
| Http2ConnectionAdapter                                       |           |      |
| Http2ConnectionHandler                                       |           |      |
| Http2ConnectionHandlerBuilder                                |           |      |
| Http2ConnectionPrefaceAndSettingsFrameWrittenEvent           |           |      |
| Http2DataChunkedInput                                        |           |      |
| Http2EventAdapter                                            |           |      |
| Http2Flags                                                   |           |      |
| Http2FrameAdapter                                            |           |      |
| Http2FrameCodec                                              |           |      |
| Http2FrameCodecBuilder                                       |           |      |
| Http2FrameListenerDecorator                                  |           |      |
| Http2FrameLogger                                             |           |      |
| Http2FrameStreamEvent                                        |           |      |
| Http2FrameTypes                                              |           |      |
| Http2InboundFrameLogger                                      |           |      |
| Http2MultiplexCodec                                          |           |      |
| Http2MultiplexCodecBuilder                                   |           |      |
| Http2MultiplexHandler                                        |           |      |
| Http2OutboundFrameLogger                                     |           |      |
| Http2SecurityUtil                                            |           |      |
| Http2ServerUpgradeCodec                                      |           |      |
| Http2Settings                                                |           |      |
| Http2StreamChannelBootstrap                                  |           |      |
| Http2StreamFrameToHttpObjectCodec                            |           |      |
| HttpConversionUtil                                           |           |      |
| HttpToHttp2ConnectionHandler                                 |           |      |
| HttpToHttp2ConnectionHandlerBuilder                          |           |      |
| InboundHttp2ToHttpAdapter                                    |           |      |
| InboundHttp2ToHttpAdapterBuilder                             |           |      |
| InboundHttpToHttp2Adapter                                    |           |      |
| ReadOnlyHttp2Headers                                         |           |      |
| StreamBufferingEncoder                                       |           |      |
| UniformStreamByteDistributor                                 |           |      |
| WeightedFairQueueByteDistributor                             |           |      |
|                                                              |           |      |
| Enums                                                        |           |      |
|                                                              |           |      |
| Http2Error                                                   |           |      |
| Http2Exception.ShutdownHint                                  |           |      |
| Http2FrameLogger.Direction                                   |           |      |
| Http2FrameStreamEvent.Type                                   |           |      |
| Http2Headers.PseudoHeaderName                                |           |      |
| Http2Stream.State                                            |           |      |
| HttpConversionUtil.ExtensionHeaderNames                      |           |      |
|                                                              |           |      |
| Exceptions                                                   |           |      |
|                                                              |           |      |
| Http2Exception                                               |           |      |
| Http2Exception.ClosedStreamCreationException                 |           |      |
| Http2Exception.CompositeStreamException                      |           |      |
| Http2Exception.HeaderListSizeException                       |           |      |
| Http2Exception.StreamException                               |           |      |
| Http2FrameStreamException                                    |           |      |
| Http2MultiplexActiveStreamsException                         |           |      |
| Http2NoMoreStreamIdsException                                |           |      |
| StreamBufferingEncoder.Http2ChannelClosedException           |           |      |
| StreamBufferingEncoder.Http2GoAwayException                  |           |      |



#### io.netty.handler.codec.json

JsonObjectDecoder

##### io.netty.handler.codec.marshalling



| io.netty.handler.codec.marshalling | 类型      |      |
| ---------------------------------- | --------- | ---- |
| Interfaces                         |           |      |
|                                    |           |      |
| MarshallerProvider                 | interface |      |
| UnmarshallerProvider               | interface |      |
|                                    |           |      |
| Classes                            |           |      |
|                                    |           |      |
| CompatibleMarshallingDecoder       |           |      |
| CompatibleMarshallingEncoder       |           |      |
| ContextBoundUnmarshallerProvider   |           |      |
| DefaultMarshallerProvider          |           |      |
| DefaultUnmarshallerProvider        |           |      |
| MarshallingDecoder                 |           |      |
| MarshallingEncoder                 |           |      |
| ThreadLocalMarshallerProvider      |           |      |
| ThreadLocalUnmarshallerProvider    |           |      |





marshalling是jboss的java对象序列化包,修正了jdk原生序列化存在的问题,保持了对java.io.Serializable接口的兼容



##### io.netty.handler.codec.memcache







| io.netty.handler.codec.memcache  | 类型      |      |
| -------------------------------- | --------- | ---- |
| Interfaces                       |           |      |
|                                  | interface |      |
| FullMemcacheMessage              | interface |      |
| LastMemcacheContent              | interface |      |
| MemcacheContent                  | interface |      |
| MemcacheMessage                  | interface |      |
| MemcacheObject                   | interface |      |
|                                  |           |      |
| Classes                          |           |      |
|                                  |           |      |
| AbstractMemcacheObject           |           |      |
| AbstractMemcacheObjectAggregator |           |      |
| AbstractMemcacheObjectDecoder    |           |      |
| AbstractMemcacheObjectEncoder    |           |      |
| DefaultLastMemcacheContent       |           |      |
| DefaultMemcacheContent           |           |      |



##### io.netty.handler.codec.memcache.binary

| io.netty.handler.codec.memcache.binary | 类型      |      |
| -------------------------------------- | --------- | ---- |
| Interfaces                             |           |      |
|                                        |           |      |
| BinaryMemcacheMessage                  | interface |      |
| BinaryMemcacheRequest                  | interface |      |
| BinaryMemcacheResponse                 | interface |      |
| FullBinaryMemcacheRequest              | interface |      |
| FullBinaryMemcacheResponse             | interface |      |
|                                        |           |      |
| Classes                                |           |      |
|                                        |           |      |
| AbstractBinaryMemcacheDecoder          |           |      |
| AbstractBinaryMemcacheEncoder          |           |      |
| AbstractBinaryMemcacheMessage          |           |      |
| BinaryMemcacheClientCodec              |           |      |
| BinaryMemcacheObjectAggregator         |           |      |
| BinaryMemcacheOpcodes                  |           |      |
| BinaryMemcacheRequestDecoder           |           |      |
| BinaryMemcacheRequestEncoder           |           |      |
| BinaryMemcacheResponseDecoder          |           |      |
| BinaryMemcacheResponseEncoder          |           |      |
| BinaryMemcacheResponseStatus           |           |      |
| BinaryMemcacheServerCodec              |           |      |
| DefaultBinaryMemcacheRequest           |           |      |
| DefaultBinaryMemcacheResponse          |           |      |
| DefaultFullBinaryMemcacheRequest       |           |      |
| DefaultFullBinaryMemcacheResponse      |           |      |





##### io.netty.handler.codec.mqtt



| io.netty.handler.codec.mqtt                   | 类型      |      |
| --------------------------------------------- | --------- | ---- |
| Interfaces                                    |           |      |
|                                               |           |      |
| MqttMessageBuilders.PropertiesInitializer     | interface |      |
|                                               |           |      |
| Classes                                       |           |      |
|                                               |           |      |
| MqttConnAckMessage                            |           |      |
| MqttConnAckVariableHeader                     |           |      |
| MqttConnectMessage                            |           |      |
| MqttConnectPayload                            |           |      |
| MqttConnectVariableHeader                     |           |      |
| MqttConstant                                  |           |      |
| MqttDecoder                                   |           |      |
| MqttEncoder                                   |           |      |
| MqttFixedHeader                               |           |      |
| MqttMessage                                   |           |      |
| MqttMessageBuilders                           |           |      |
| MqttMessageBuilders.AuthBuilder               |           |      |
| MqttMessageBuilders.ConnAckBuilder            |           |      |
| MqttMessageBuilders.ConnAckPropertiesBuilder  |           |      |
| MqttMessageBuilders.ConnectBuilder            |           |      |
| MqttMessageBuilders.DisconnectBuilder         |           |      |
| MqttMessageBuilders.PubAckBuilder             |           |      |
| MqttMessageBuilders.PublishBuilder            |           |      |
| MqttMessageBuilders.SubAckBuilder             |           |      |
| MqttMessageBuilders.SubscribeBuilder          |           |      |
| MqttMessageBuilders.UnsubAckBuilder           |           |      |
| MqttMessageBuilders.UnsubscribeBuilder        |           |      |
| MqttMessageFactory                            |           |      |
| MqttMessageIdAndPropertiesVariableHeader      |           |      |
| MqttMessageIdVariableHeader                   |           |      |
| MqttProperties                                |           |      |
| MqttProperties.BinaryProperty                 |           |      |
| MqttProperties.IntegerProperty                |           |      |
| MqttProperties.MqttProperty                   |           |      |
| MqttProperties.StringPair                     |           |      |
| MqttProperties.StringProperty                 |           |      |
| MqttProperties.UserProperties                 |           |      |
| MqttProperties.UserProperty                   |           |      |
| MqttPubAckMessage                             |           |      |
| MqttPublishMessage                            |           |      |
| MqttPublishVariableHeader                     |           |      |
| MqttPubReplyMessageVariableHeader             |           |      |
| MqttReasonCodeAndPropertiesVariableHeader     |           |      |
| MqttSubAckMessage                             |           |      |
| MqttSubAckPayload                             |           |      |
| MqttSubscribeMessage                          |           |      |
| MqttSubscribePayload                          |           |      |
| MqttSubscriptionOption                        |           |      |
| MqttTopicSubscription                         |           |      |
| MqttUnsubAckMessage                           |           |      |
| MqttUnsubAckPayload                           |           |      |
| MqttUnsubscribeMessage                        |           |      |
| MqttUnsubscribePayload                        |           |      |
|                                               |           |      |
| Enums                                         |           |      |
|                                               |           |      |
| MqttConnectReturnCode                         |           |      |
| MqttMessageType                               |           |      |
| MqttProperties.MqttPropertyType               |           |      |
| MqttQoS                                       |           |      |
| MqttSubscriptionOption.RetainedHandlingPolicy |           |      |
| MqttVersion                                   |           |      |
|                                               |           |      |
| Exceptions                                    |           |      |
|                                               |           |      |
| MqttIdentifierRejectedException               |           |      |
| MqttUnacceptableProtocolVersionException      |           |      |



##### io.netty.handler.codec.protobuf

| io.netty.handler.codec.protobuf      | 类型 |      |
| ------------------------------------ | ---- | ---- |
|                                      |      |      |
| Classes                              |      |      |
|                                      |      |      |
| ProtobufDecoder                      |      |      |
| ProtobufDecoderNano                  |      |      |
| ProtobufEncoder                      |      |      |
| ProtobufEncoderNano                  |      |      |
| ProtobufVarint32FrameDecoder         |      |      |
| ProtobufVarint32LengthFieldPrepender |      |      |



##### io.netty.handler.codec.redis



| io.netty.handler.codec.redis      | 类型      |      |
| --------------------------------- | --------- | ---- |
|                                   |           |      |
| Interfaces                        |           |      |
|                                   |           |      |
| BulkStringRedisContent            | interface |      |
| LastBulkStringRedisContent        | interface |      |
| RedisMessage                      | interface |      |
| RedisMessagePool                  | interface |      |
|                                   |           |      |
| Classes                           |           |      |
|                                   |           |      |
| AbstractStringRedisMessage        |           |      |
| ArrayHeaderRedisMessage           |           |      |
| ArrayRedisMessage                 |           |      |
| BulkStringHeaderRedisMessage      |           |      |
| DefaultBulkStringRedisContent     |           |      |
| DefaultLastBulkStringRedisContent |           |      |
| ErrorRedisMessage                 |           |      |
| FixedRedisMessagePool             |           |      |
| FullBulkStringRedisMessage        |           |      |
| InlineCommandRedisMessage         |           |      |
| IntegerRedisMessage               |           |      |
| RedisArrayAggregator              |           |      |
| RedisBulkStringAggregator         |           |      |
| RedisDecoder                      |           |      |
| RedisEncoder                      |           |      |
| SimpleStringRedisMessage          |           |      |





##### io.netty.handler.codec.rtsp



| io.netty.handler.codec.rtsp | 类型 |      |
| --------------------------- | ---- | ---- |
| Classes                     |      |      |
|                             |      |      |
| RtspDecoder                 |      |      |
| RtspEncoder                 |      |      |
| RtspHeaderNames             |      |      |
| RtspHeaders                 |      |      |
| RtspHeaders.Names           |      |      |
| RtspHeaders.Values          |      |      |
| RtspHeaderValues            |      |      |
| RtspMethods                 |      |      |
| RtspObjectDecoder           |      |      |
| RtspObjectEncoder           |      |      |
| RtspRequestDecoder          |      |      |
| RtspRequestEncoder          |      |      |
| RtspResponseDecoder         |      |      |
| RtspResponseEncoder         |      |      |
| RtspResponseStatuses        |      |      |





##### io.netty.handler.codec.sctp





| io.netty.handler.codec.sctp   | 类型 |      |
| ----------------------------- | ---- | ---- |
| Classes                       |      |      |
|                               |      |      |
| SctpInboundByteStreamHandler  |      |      |
| SctpMessageCompletionHandler  |      |      |
| SctpMessageToMessageDecoder   |      |      |
| SctpOutboundByteStreamHandler |      |      |



##### io.netty.handler.codec.serialization



| io.netty.handler.codec.serialization | 类型 |      |
| ------------------------------------ | ---- | ---- |
|                                      |      |      |
| ClassResolver                        |      |      |
|                                      |      |      |
| Classes                              |      |      |
|                                      |      |      |
| ClassResolvers                       |      |      |
| CompatibleObjectEncoder              |      |      |
| ObjectDecoder                        |      |      |
| ObjectDecoderInputStream             |      |      |
| ObjectEncoder                        |      |      |
| ObjectEncoderOutputStream            |      |      |





##### io.netty.handler.codec.smtp

| io.netty.handler.codec.smtp | 类型 |      |
| --------------------------- | ---- | ---- |
|                             |      |      |
| LastSmtpContent             |      |      |
| SmtpContent                 |      |      |
| SmtpRequest                 |      |      |
| SmtpResponse                |      |      |
|                             |      |      |
| Classes                     |      |      |
|                             |      |      |
| DefaultLastSmtpContent      |      |      |
| DefaultSmtpContent          |      |      |
| DefaultSmtpRequest          |      |      |
| DefaultSmtpResponse         |      |      |
| SmtpCommand                 |      |      |
| SmtpRequestEncoder          |      |      |
| SmtpRequests                |      |      |
| SmtpResponseDecoder         |      |      |



##### io.netty.handler.codec.socks

| io.netty.handler.codec.socks   | 类型 |      |
| ------------------------------ | ---- | ---- |
| Classes                        |      |      |
|                                |      |      |
| SocksAuthRequest               |      |      |
| SocksAuthRequestDecoder        |      |      |
| SocksAuthResponse              |      |      |
| SocksAuthResponseDecoder       |      |      |
| SocksCmdRequest                |      |      |
| SocksCmdRequestDecoder         |      |      |
| SocksCmdResponse               |      |      |
| SocksCmdResponseDecoder        |      |      |
| SocksInitRequest               |      |      |
| SocksInitRequestDecoder        |      |      |
| SocksInitResponse              |      |      |
| SocksInitResponseDecoder       |      |      |
| SocksMessage                   |      |      |
| SocksMessageEncoder            |      |      |
| SocksRequest                   |      |      |
| SocksResponse                  |      |      |
| UnknownSocksRequest            |      |      |
| UnknownSocksResponse           |      |      |
|                                |      |      |
| Enums                          |      |      |
|                                |      |      |
| SocksAddressType               |      |      |
| SocksAuthRequestDecoder.State  |      |      |
| SocksAuthResponseDecoder.State |      |      |
| SocksAuthScheme                |      |      |
| SocksAuthStatus                |      |      |
| SocksCmdRequestDecoder.State   |      |      |
| SocksCmdResponseDecoder.State  |      |      |
| SocksCmdStatus                 |      |      |
| SocksCmdType                   |      |      |
| SocksInitRequestDecoder.State  |      |      |
| SocksInitResponseDecoder.State |      |      |
| SocksMessageType               |      |      |
| SocksProtocolVersion           |      |      |
| SocksRequestType               |      |      |
| SocksResponseType              |      |      |
| SocksSubnegotiationVersion     |      |      |



##### io.netty.handler.codec.socksx



| io.netty.handler.codec.socksx  | 类型 |      |
| ------------------------------ | ---- | ---- |
| Classes                        |      |      |
|                                |      |      |
| SocksAuthRequest               |      |      |
| SocksAuthRequestDecoder        |      |      |
| SocksAuthResponse              |      |      |
| SocksAuthResponseDecoder       |      |      |
| SocksCmdRequest                |      |      |
| SocksCmdRequestDecoder         |      |      |
| SocksCmdResponse               |      |      |
| SocksCmdResponseDecoder        |      |      |
| SocksInitRequest               |      |      |
| SocksInitRequestDecoder        |      |      |
| SocksInitResponse              |      |      |
| SocksInitResponseDecoder       |      |      |
| SocksMessage                   |      |      |
| SocksMessageEncoder            |      |      |
| SocksRequest                   |      |      |
| SocksResponse                  |      |      |
| UnknownSocksRequest            |      |      |
| UnknownSocksResponse           |      |      |
|                                |      |      |
| Enums                          |      |      |
|                                |      |      |
| SocksAddressType               |      |      |
| SocksAuthRequestDecoder.State  |      |      |
| SocksAuthResponseDecoder.State |      |      |
| SocksAuthScheme                |      |      |
| SocksAuthStatus                |      |      |
| SocksCmdRequestDecoder.State   |      |      |
| SocksCmdResponseDecoder.State  |      |      |
| SocksCmdStatus                 |      |      |
| SocksCmdType                   |      |      |
| SocksInitRequestDecoder.State  |      |      |
| SocksInitResponseDecoder.State |      |      |
| SocksMessageType               |      |      |
| SocksProtocolVersion           |      |      |
| SocksRequestType               |      |      |
| SocksResponseType              |      |      |
| SocksSubnegotiationVersion     |      |      |



##### io.netty.handler.codec.socksx.v4

| io.netty.handler.codec.socksx.v4 | 类型      |      |
| -------------------------------- | --------- | ---- |
|                                  |           |      |
| Interfaces                       |           |      |
|                                  |           |      |
| Socks4CommandRequest             | interface |      |
| Socks4CommandResponse            | interface |      |
| Socks4Message                    | interface |      |
|                                  |           |      |
| Classes                          |           |      |
|                                  |           |      |
| AbstractSocks4Message            |           |      |
| DefaultSocks4CommandRequest      |           |      |
| DefaultSocks4CommandResponse     |           |      |
| Socks4ClientDecoder              |           |      |
| Socks4ClientEncoder              |           |      |
| Socks4CommandStatus              |           |      |
| Socks4CommandType                |           |      |
| Socks4ServerDecoder              |           |      |
| Socks4ServerEncoder              |           |      |
|                                  |           |      |
| Enums                            |           |      |
|                                  |           |      |
| Socks4ClientDecoder.State        |           |      |
| Socks4ServerDecoder.State        |           |      |
| Socks4ServerDecoder.State        |           |      |



##### io.netty.handler.codec.socksx.v5



| io.netty.handler.codec.socksx.v5        | 类型      |      |
| --------------------------------------- | --------- | ---- |
| Interfaces                              |           |      |
|                                         |           |      |
| Socks5AddressDecoder                    | interface |      |
| Socks5AddressEncoder                    | interface |      |
| Socks5CommandRequest                    | interface |      |
| Socks5CommandResponse                   | interface |      |
| Socks5InitialRequest                    | interface |      |
| Socks5InitialResponse                   | interface |      |
| Socks5Message                           | interface |      |
| Socks5PasswordAuthRequest               | interface |      |
| Socks5PasswordAuthResponse              | interface |      |
|                                         |           |      |
| Classes                                 |           |      |
|                                         |           |      |
| AbstractSocks5Message                   |           |      |
| DefaultSocks5CommandRequest             |           |      |
| DefaultSocks5CommandResponse            |           |      |
| DefaultSocks5InitialRequest             |           |      |
| DefaultSocks5InitialResponse            |           |      |
| DefaultSocks5PasswordAuthRequest        |           |      |
| DefaultSocks5PasswordAuthResponse       |           |      |
| Socks5AddressType                       |           |      |
| Socks5AuthMethod                        |           |      |
| Socks5ClientEncoder                     |           |      |
| Socks5CommandRequestDecoder             |           |      |
| Socks5CommandResponseDecoder            |           |      |
| Socks5CommandStatus                     |           |      |
| Socks5CommandType                       |           |      |
| Socks5InitialRequestDecoder             |           |      |
| Socks5InitialResponseDecoder            |           |      |
| Socks5PasswordAuthRequestDecoder        |           |      |
| Socks5PasswordAuthResponseDecoder       |           |      |
| Socks5PasswordAuthStatus                |           |      |
| Socks5ServerEncoder                     |           |      |
|                                         |           |      |
| Enums                                   |           |      |
|                                         |           |      |
| Socks5CommandRequestDecoder.State       |           |      |
| Socks5CommandResponseDecoder.State      |           |      |
| Socks5InitialRequestDecoder.State       |           |      |
| Socks5InitialResponseDecoder.State      |           |      |
| Socks5PasswordAuthRequestDecoder.State  |           |      |
| Socks5PasswordAuthResponseDecoder.State |           |      |





##### io.netty.handler.codec.spdy



| io.netty.handler.codec.spdy     | 类型      |      |
| ------------------------------- | --------- | ---- |
| Interfaces                      |           |      |
|                                 |           |      |
| SpdyDataFrame                   | interface |      |
| SpdyFrame                       | interface |      |
| SpdyFrameDecoderDelegate        | interface |      |
| SpdyGoAwayFrame                 | interface |      |
| SpdyHeaders                     | interface |      |
| SpdyHeadersFrame                | interface |      |
| SpdyPingFrame                   | interface |      |
| SpdyRstStreamFrame              | interface |      |
| SpdySettingsFrame               | interface |      |
| SpdyStreamFrame                 | interface |      |
| SpdySynReplyFrame               | interface |      |
| SpdySynStreamFrame              | interface |      |
| SpdyWindowUpdateFrame           | interface |      |
|                                 |           |      |
| Classes                         |           |      |
|                                 |           |      |
| DefaultSpdyDataFrame            |           |      |
| DefaultSpdyGoAwayFrame          |           |      |
| DefaultSpdyHeaders              |           |      |
| DefaultSpdyHeadersFrame         |           |      |
| DefaultSpdyPingFrame            |           |      |
| DefaultSpdyRstStreamFrame       |           |      |
| DefaultSpdySettingsFrame        |           |      |
| DefaultSpdyStreamFrame          |           |      |
| DefaultSpdySynReplyFrame        |           |      |
| DefaultSpdySynStreamFrame       |           |      |
| DefaultSpdyWindowUpdateFrame    |           |      |
| SpdyFrameCodec                  |           |      |
| SpdyFrameDecoder                |           |      |
| SpdyFrameEncoder                |           |      |
| SpdyHeaderBlockDecoder          |           |      |
| SpdyHeaderBlockEncoder          |           |      |
| SpdyHeaderBlockRawDecoder       |           |      |
| SpdyHeaderBlockRawEncoder       |           |      |
| SpdyHeaders.HttpNames           |           |      |
| SpdyHttpCodec                   |           |      |
| SpdyHttpDecoder                 |           |      |
| SpdyHttpEncoder                 |           |      |
| SpdyHttpHeaders                 |           |      |
| SpdyHttpHeaders.Names           |           |      |
| SpdyHttpResponseStreamIdHandler |           |      |
| SpdySessionHandler              |           |      |
| SpdySessionStatus               |           |      |
| SpdyStreamStatus                |           |      |
|                                 |           |      |
| Enums                           |           |      |
|                                 |           |      |
| SpdyVersion                     |           |      |
|                                 |           |      |
| Exceptions                      |           |      |
|                                 |           |      |
| SpdyProtocolException           |           |      |





##### io.netty.handler.codec.stomp





| io.netty.handler.codec.stomp    | 类型      |      |
| ------------------------------- | --------- | ---- |
| Interfaces                      |           |      |
|                                 |           |      |
| LastStompContentSubframe        | interface |      |
| StompContentSubframe            | interface |      |
| StompFrame                      | interface |      |
| StompHeaders                    | interface |      |
| StompHeadersSubframe            | interface |      |
| StompSubframe                   | interface |      |
|                                 |           |      |
| Classes                         |           |      |
|                                 |           |      |
| DefaultLastStompContentSubframe |           |      |
| DefaultStompContentSubframe     |           |      |
| DefaultStompFrame               |           |      |
| DefaultStompHeaders             |           |      |
| DefaultStompHeadersSubframe     |           |      |
| StompSubframeAggregator         |           |      |
| StompSubframeDecoder            |           |      |
| StompSubframeEncoder            |           |      |
|                                 |           |      |
| Enums                           |           |      |
|                                 |           |      |
| StompCommand                    |           |      |
| StompSubframeDecoder.State      |           |      |



##### io.netty.handler.codec.string



| io.netty.handler.codec.string | 类型 |      |
| ----------------------------- | ---- | ---- |
| LineEncoder                   |      |      |
| StringDecoder                 |      |      |
| StringEncoder                 |      |      |



##### io.netty.handler.codec.xml



| io.netty.handler.codec.xml | 类型 |      |
| -------------------------- | ---- | ---- |
| Classes                    |      |      |
|                            |      |      |
| XmlAttribute               |      |      |
| XmlCdata                   |      |      |
| XmlCharacters              |      |      |
| XmlComment                 |      |      |
| XmlContent                 |      |      |
| XmlDecoder                 |      |      |
| XmlDocumentEnd             |      |      |
| XmlDocumentStart           |      |      |
| XmlDTD                     |      |      |
| XmlElement                 |      |      |
| XmlElementEnd              |      |      |
| XmlElementStart            |      |      |
| XmlEntityReference         |      |      |
| XmlFrameDecoder            |      |      |
| XmlNamespace               |      |      |
| XmlProcessingInstruction   |      |      |
| XmlSpace                   |      |      |





io.netty.handler.flow



FlowControlHandler







io.netty.handler.flush





FlushConsolidationHandler





#### io.netty.handler.ipfilter



| io.netty.handler.ipfilter   | 类型      |      |
| --------------------------- | --------- | ---- |
| Interfaces                  |           |      |
|                             |           |      |
| IpFilterRule                | interface |      |
|                             |           |      |
| Classes                     |           |      |
|                             |           |      |
| AbstractRemoteAddressFilter |           |      |
| IpSubnetFilter              |           |      |
| IpSubnetFilterRule          |           |      |
| RuleBasedIpFilter           |           |      |
| UniqueIpFilter              |           |      |
|                             |           |      |
| Enums                       |           |      |
|                             |           |      |
| IpFilterRuleType            |           |      |





#### io.netty.handler.logging



| io.netty.handler.logging | 类型 |      |
| ------------------------ | ---- | ---- |
| Classes                  |      |      |
|                          |      |      |
| LoggingHandler           |      |      |
|                          |      |      |
| Enums                    |      |      |
|                          |      |      |
| ByteBufFormat            |      |      |
| LogLevel                 |      |      |





io.netty.handler.pcap

PcapWriteHandler

PcapWriteHandler.Builder





#### io.netty.handler.proxy



| io.netty.handler.proxy                     | 类型 |      |
| ------------------------------------------ | ---- | ---- |
| Classes                                    |      |      |
|                                            |      |      |
| HttpProxyHandler                           |      |      |
| ProxyConnectionEvent                       |      |      |
| ProxyHandler                               |      |      |
| Socks4ProxyHandler                         |      |      |
| Socks5ProxyHandler                         |      |      |
|                                            |      |      |
| Exceptions                                 |      |      |
|                                            |      |      |
| HttpProxyHandler.HttpProxyConnectException |      |      |
| ProxyConnectException                      |      |      |







#### io.netty.handler.ssl





| io.netty.handler.ssl                                         | 类型      |      |
| ------------------------------------------------------------ | --------- | ---- |
| Interfaces                                                   |           |      |
|                                                              |           |      |
| ApplicationProtocolNegotiator                                | interface |      |
| CipherSuiteFilter                                            | interface |      |
| JdkApplicationProtocolNegotiator                             | interface |      |
| JdkApplicationProtocolNegotiator.ProtocolSelectionListener   | interface |      |
| JdkApplicationProtocolNegotiator.ProtocolSelectionListenerFactory | interface |      |
| JdkApplicationProtocolNegotiator.ProtocolSelector            | interface |      |
| JdkApplicationProtocolNegotiator.ProtocolSelectorFactory     | interface |      |
| JdkApplicationProtocolNegotiator.SslEngineWrapperFactory     | interface |      |
| OpenSslApplicationProtocolNegotiator                         | interface |      |
| OpenSslAsyncPrivateKeyMethod                                 | interface |      |
| OpenSslCertificateCompressionAlgorithm                       | interface |      |
| OpenSslPrivateKeyMethod                                      | interface |      |
|                                                              |           |      |
| Classes                                                      |           |      |
|                                                              |           |      |
| AbstractSniHandler                                           |           |      |
| ApplicationProtocolConfig                                    |           |      |
| ApplicationProtocolNames                                     |           |      |
| ApplicationProtocolNegotiationHandler                        |           |      |
| Ciphers                                                      |           |      |
| CipherSuiteConverter                                         |           |      |
| DelegatingSslContext                                         |           |      |
| IdentityCipherSuiteFilter                                    |           |      |
| JdkAlpnApplicationProtocolNegotiator                         |           |      |
| JdkApplicationProtocolNegotiator.AllocatorAwareSslEngineWrapperFactory |           |      |
| JdkNpnApplicationProtocolNegotiator                          |           |      |
| JdkSslClientContext                                          |           |      |
| JdkSslContext                                                |           |      |
| JdkSslServerContext                                          |           |      |
| OpenSsl                                                      |           |      |
| OpenSslCachingX509KeyManagerFactory                          |           |      |
| OpenSslCertificateCompressionConfig                          |           |      |
| OpenSslCertificateCompressionConfig.AlgorithmConfig          |           |      |
| OpenSslCertificateCompressionConfig.Builder                  |           |      |
| OpenSslClientContext                                         |           |      |
| OpenSslContext                                               |           |      |
| OpenSslContextOption                                         |           |      |
| OpenSslDefaultApplicationProtocolNegotiator                  |           |      |
| OpenSslEngine                                                |           |      |
| OpenSslNpnApplicationProtocolNegotiator                      |           |      |
| OpenSslServerContext                                         |           |      |
| OpenSslServerSessionContext                                  |           |      |
| OpenSslSessionContext                                        |           |      |
| OpenSslSessionStats                                          |           |      |
| OpenSslSessionTicketKey                                      |           |      |
| OpenSslX509KeyManagerFactory                                 |           |      |
| OptionalSslHandler                                           |           |      |
| PemPrivateKey                                                |           |      |
| PemX509Certificate                                           |           |      |
| ReferenceCountedOpenSslClientContext                         |           |      |
| ReferenceCountedOpenSslContext                               |           |      |
| ReferenceCountedOpenSslEngine                                |           |      |
| ReferenceCountedOpenSslServerContext                         |           |      |
| SniCompletionEvent                                           |           |      |
| SniHandler                                                   |           |      |
| SslClientHelloHandler                                        |           |      |
| SslCloseCompletionEvent                                      |           |      |
| SslCompletionEvent                                           |           |      |
| SslContext                                                   |           |      |
| SslContextBuilder                                            |           |      |
| SslContextOption                                             |           |      |
| SslHandler                                                   |           |      |
| SslHandshakeCompletionEvent                                  |           |      |
| SslMasterKeyHandler                                          |           |      |
| SslProtocols                                                 |           |      |
| SupportedCipherSuiteFilter                                   |           |      |
|                                                              |           |      |
| Enums                                                        |           |      |
|                                                              |           |      |
| ApplicationProtocolConfig.Protocol                           |           |      |
| ApplicationProtocolConfig.SelectedListenerFailureBehavior    |           |      |
| ApplicationProtocolConfig.SelectorFailureBehavior            |           |      |
| ClientAuth                                                   |           |      |
| OpenSslCertificateCompressionConfig.AlgorithmMode            |           |      |
| SslProvider                                                  |           |      |
|                                                              |           |      |
| Exceptions                                                   |           |      |
|                                                              |           |      |
| NotSslRecordException                                        |           |      |
| OpenSslCertificateException                                  |           |      |
| SslClosedEngineException                                     |           |      |
| SslHandshakeTimeoutException                                 |           |      |



#### io.netty.handler.ssl.ocsp



| io.netty.handler.ssl.ocsp      | 类型 |      |
| ------------------------------ | ---- | ---- |
| Classes                        |      |      |
|                                |      |      |
| IoTransport                    |      |      |
| OcspClientHandler              |      |      |
| OcspResponse                   |      |      |
| OcspServerCertificateValidator |      |      |
| OcspValidationEvent            |      |      |
|                                |      |      |
| Enums                          |      |      |
|                                |      |      |
| OcspResponse.Status            |      |      |
|                                |      |      |
|                                |      |      |







#### io.netty.handler.ssl.util





| io.netty.handler.ssl.util             | 类型 |      |
| ------------------------------------- | ---- | ---- |
| Classes                               |      |      |
|                                       |      |      |
| FingerprintTrustManagerFactory        |      |      |
| FingerprintTrustManagerFactoryBuilder |      |      |
| InsecureTrustManagerFactory           |      |      |
| KeyManagerFactoryWrapper              |      |      |
| LazyJavaxX509Certificate              |      |      |
| LazyX509Certificate                   |      |      |
| SelfSignedCertificate                 |      |      |
| SimpleKeyManagerFactory               |      |      |
| SimpleTrustManagerFactory             |      |      |
| TrustManagerFactoryWrapper            |      |      |



#### io.netty.handler.stream



| io.netty.handler.stream | 类型      |      |
| ----------------------- | --------- | ---- |
| Interfaces              |           |      |
|                         |           |      |
| ChunkedInput            | interface |      |
|                         |           |      |
| Classes                 |           |      |
|                         |           |      |
| ChunkedFile             |           |      |
| ChunkedNioFile          |           |      |
| ChunkedNioStream        |           |      |
| ChunkedStream           |           |      |
| ChunkedWriteHandler     |           |      |



#### io.netty.handler.timeout





| io.netty.handler.timeout | 类型 |      |
| ------------------------ | ---- | ---- |
| Classes                  |      |      |
|                          |      |      |
| IdleStateEvent           |      |      |
| IdleStateHandler         |      |      |
| ReadTimeoutHandler       |      |      |
| WriteTimeoutHandler      |      |      |
|                          |      |      |
| Enums                    |      |      |
|                          |      |      |
| IdleState                |      |      |
|                          |      |      |
| Exceptions               |      |      |
|                          |      |      |
| ReadTimeoutException     |      |      |
| TimeoutException         |      |      |
| WriteTimeoutException    |      |      |



#### io.netty.handler.traffic



| io.netty.handler.traffic           | 类型 |      |
| ---------------------------------- | ---- | ---- |
| Classes                            |      |      |
|                                    |      |      |
| AbstractTrafficShapingHandler      |      |      |
| ChannelTrafficShapingHandler       |      |      |
| GlobalChannelTrafficCounter        |      |      |
| GlobalChannelTrafficShapingHandler |      |      |
| GlobalTrafficShapingHandler        |      |      |
| TrafficCounter                     |      |      |



## io.netty.resolver




| io.netty.resolver               | 类型      |      |
| ------------------------------- | --------- | ---- |
| Interfaces                      |           |      |
|                                 |           |      |
| AddressResolver                 | interface |      |
| HostsFileEntriesProvider.Parser | interface |      |
| HostsFileEntriesResolver        | interface |      |
| NameResolver                    | interface |      |
|                                 |           |      |
| Classes                         |           |      |
|                                 |           |      |
| AbstractAddressResolver         |           |      |
| AddressResolverGroup            |           |      |
| CompositeNameResolver           |           |      |
| DefaultAddressResolverGroup     |           |      |
| DefaultHostsFileEntriesResolver |           |      |
| DefaultNameResolver             |           |      |
| HostsFileEntries                |           |      |
| HostsFileEntriesProvider        |           |      |
| HostsFileParser                 |           |      |
| InetNameResolver                |           |      |
| InetSocketAddressResolver       |           |      |
| NoopAddressResolver             |           |      |
| NoopAddressResolverGroup        |           |      |
| RoundRobinInetAddressResolver   |           |      |
| SimpleNameResolver              |           |      |
|                                 |           |      |
| Enums                           |           |      |
|                                 |           |      |
| ResolvedAddressTypes            |           |      |





#### io.netty.resolver.dns



| io.netty.resolver.dns                      | 类型      |      |
| ------------------------------------------ | --------- | ---- |
| Interfaces                                 |           |      |
|                                            |           |      |
| AuthoritativeDnsServerCache                | interface |      |
| DnsCache                                   | interface |      |
| DnsCacheEntry                              | interface |      |
| DnsCnameCache                              | interface |      |
| DnsQueryLifecycleObserver                  | interface |      |
| DnsQueryLifecycleObserverFactory           | interface |      |
| DnsServerAddressStream                     | interface |      |
| DnsServerAddressStreamProvider             | interface |      |
| DnsServerResponseFeedbackAddressStream     | interface |      |
|                                            |           |      |
| Classes                                    |           |      |
|                                            |           |      |
| BiDnsQueryLifecycleObserver                |           |      |
| BiDnsQueryLifecycleObserverFactory         |           |      |
| DefaultAuthoritativeDnsServerCache         |           |      |
| DefaultDnsCache                            |           |      |
| DefaultDnsCnameCache                       |           |      |
| DefaultDnsServerAddressStreamProvider      |           |      |
| DnsAddressResolverGroup                    |           |      |
| DnsNameResolver                            |           |      |
| DnsNameResolverBuilder                     |           |      |
| DnsServerAddresses                         |           |      |
| DnsServerAddressStreamProviders            |           |      |
| LoggingDnsQueryLifeCycleObserverFactory    |           |      |
| MultiDnsServerAddressStreamProvider        |           |      |
| NameServerComparator                       |           |      |
| NoopAuthoritativeDnsServerCache            |           |      |
| NoopDnsCache                               |           |      |
| NoopDnsCnameCache                          |           |      |
| NoopDnsQueryLifecycleObserverFactory       |           |      |
| RoundRobinDnsAddressResolverGroup          |           |      |
| SequentialDnsServerAddressStreamProvider   |           |      |
| SingletonDnsServerAddressStreamProvider    |           |      |
| UnixResolverDnsServerAddressStreamProvider |           |      |
|                                            |           |      |
| Exceptions                                 |           |      |
|                                            |           |      |
| DnsNameResolverException                   |           |      |
| DnsNameResolverTimeoutException            |           |      |





##### io.netty.resolver.dns.macos



MacOSDnsServerAddressStreamProvider





## io.netty.util



| io.netty.util                     | 类型      |      |
| --------------------------------- | --------- | ---- |
| Interfaces                        |           |      |
|                                   |           |      |
| AsyncMapping                      | interface |      |
| Attribute                         | interface |      |
| AttributeMap                      | interface |      |
| BooleanSupplier                   | interface |      |
| ByteProcessor                     | interface |      |
| Constant                          | interface |      |
| HashingStrategy                   | interface |      |
| IntSupplier                       | interface |      |
| Mapping                           | interface |      |
| Recycler.Handle                   | interface |      |
| ReferenceCounted                  | interface |      |
| ResourceLeak                      | interface |      |
| ResourceLeakDetector.LeakListener | interface |      |
| ResourceLeakHint                  | interface |      |
| ResourceLeakTracker               | interface |      |
| Timeout                           | interface |      |
| Timer                             | interface |      |
| TimerTask                         | interface |      |
| UncheckedBooleanSupplier          | interface |      |
|                                   |           |      |
| Classes                           |           |      |
|                                   |           |      |
| AbstractConstant                  |           |      |
| AbstractReferenceCounted          |           |      |
| AsciiString                       |           |      |
| AttributeKey                      |           |      |
| ByteProcessor.IndexNotOfProcessor |           |      |
| ByteProcessor.IndexOfProcessor    |           |      |
| CharsetUtil                       |           |      |
| ConstantPool                      |           |      |
| DefaultAttributeMap               |           |      |
| DomainMappingBuilder              |           |      |
| DomainNameMapping                 |           |      |
| DomainNameMappingBuilder          |           |      |
| DomainWildcardMappingBuilder      |           |      |
| HashedWheelTimer                  |           |      |
| NettyRuntime                      |           |      |
| NetUtil                           |           |      |
| Recycler                          |           |      |
| Recycler.EnhancedHandle           |           |      |
| ReferenceCountUtil                |           |      |
| ResourceLeakDetector              |           |      |
| ResourceLeakDetectorFactory       |           |      |
| ThreadDeathWatcher                |           |      |
| Version                           |           |      |
|                                   |           |      |
| Enums                             |           |      |
|                                   |           |      |
| ResourceLeakDetector.Level        |           |      |
|                                   |           |      |
| Exceptions                        |           |      |
|                                   |           |      |
| IllegalReferenceCountException    |           |      |
| ResourceLeakException             |           |      |
|                                   |           |      |
| Errors                            |           |      |
|                                   |           |      |
| Signal                            |           |      |
|                                   |           |      |
| Annotation Types                  |           |      |
|                                   |           |      |
| SuppressForbidden                 |           |      |





### io.netty.util.collection



| io.netty.util.collection      | 类型      |      |
| ----------------------------- | --------- | ---- |
| Interfaces                    |           |      |
|                               |           |      |
| ByteObjectMap                 | interface |      |
| ByteObjectMap.PrimitiveEntry  | interface |      |
| CharObjectMap                 | interface |      |
| CharObjectMap.PrimitiveEntry  | interface |      |
| IntObjectMap                  | interface |      |
| IntObjectMap.PrimitiveEntry   | interface |      |
| LongObjectMap                 | interface |      |
| LongObjectMap.PrimitiveEntry  | interface |      |
| ShortObjectMap                | interface |      |
| ShortObjectMap.PrimitiveEntry | interface |      |
|                               |           |      |
| Classes                       |           |      |
|                               |           |      |
| ByteCollections               |           |      |
| ByteObjectHashMap             |           |      |
| CharCollections               |           |      |
| CharObjectHashMap             |           |      |
| IntCollections                |           |      |
| IntObjectHashMap              |           |      |
| LongCollections               |           |      |
| LongObjectHashMap             |           |      |
| ShortCollections              |           |      |
| ShortObjectHashMap            |           |      |



### io.netty.util.concurrent



| io.netty.util.concurrent                         | 类型      |      |
| ------------------------------------------------ | --------- | ---- |
| Interfaces                                       |           |      |
|                                                  |           |      |
| AbstractEventExecutor.LazyRunnable               | interface |      |
| EventExecutor                                    | interface |      |
| EventExecutorChooserFactory                      | interface |      |
| EventExecutorChooserFactory.EventExecutorChooser | interface |      |
| EventExecutorGroup                               | interface |      |
| Future                                           | interface |      |
| FutureListener                                   | interface |      |
| GenericFutureListener                            | interface |      |
| GenericProgressiveFutureListener                 | interface |      |
| OrderedEventExecutor                             | interface |      |
| ProgressiveFuture                                | interface |      |
| ProgressivePromise                               | interface |      |
| Promise                                          | interface |      |
| RejectedExecutionHandler                         | interface |      |
| ScheduledFuture                                  | interface |      |
| SingleThreadEventExecutor.NonWakeupRunnable      | interface |      |
| ThreadProperties                                 | interface |      |
|                                                  |           |      |
| Classes                                          |           |      |
|                                                  |           |      |
| AbstractEventExecutor                            |           |      |
| AbstractEventExecutorGroup                       |           |      |
| AbstractFuture                                   |           |      |
| AbstractScheduledEventExecutor                   |           |      |
| CompleteFuture                                   |           |      |
| DefaultEventExecutor                             |           |      |
| DefaultEventExecutorChooserFactory               |           |      |
| DefaultEventExecutorGroup                        |           |      |
| DefaultProgressivePromise                        |           |      |
| DefaultPromise                                   |           |      |
| DefaultThreadFactory                             |           |      |
| FailedFuture                                     |           |      |
| FastThreadLocal                                  |           |      |
| FastThreadLocalThread                            |           |      |
| GlobalEventExecutor                              |           |      |
| ImmediateEventExecutor                           |           |      |
| ImmediateExecutor                                |           |      |
| MultithreadEventExecutorGroup                    |           |      |
| NonStickyEventExecutorGroup                      |           |      |
| PromiseAggregator                                |           |      |
| PromiseCombiner                                  |           |      |
| PromiseNotifier                                  |           |      |
| RejectedExecutionHandlers                        |           |      |
| SingleThreadEventExecutor                        |           |  见上面    |
| SucceededFuture                                  |           |      |
| ThreadPerTaskExecutor                            |           |      |
| UnaryPromiseNotifier                             |           |      |
| UnorderedThreadPoolEventExecutor                 |           |      |
|                                                  |           |      |
| Exceptions                                       |           |      |
|                                                  |           |      |
| BlockingOperationException                       |           |      |



### io.netty.util.internal



|                          | 类型      |      |
| ------------------------ | --------- | ---- |
| Interfaces               |           |      |
|                          |           |      |
| LongCounter              | interface |      |
| ObjectPool.Handle        | interface |      |
| ObjectPool.ObjectCreator | interface |      |
| PriorityQueue            | interface |      |
| PriorityQueueNode        | interface |      |
|                          |           |      |
| Classes                  |           |      |
|                          |           |      |
| AppendableCharSequence   |           |      |
| ClassInitializerUtil     |           |      |
| ConcurrentSet            |           |      |
| ConstantTimeUtils        |           |      |
| DefaultPriorityQueue     |           |      |
| EmptyArrays              |           |      |
| EmptyPriorityQueue       |           |      |
| IntegerHolder            |           |      |
| InternalThreadLocalMap   |           |      |
| MacAddressUtil           |           |      |
| MathUtil                 |           |      |
| NativeLibraryLoader      |           |      |
| NoOpTypeParameterMatcher |           |      |
| ObjectCleaner            |           |      |
| ObjectPool               |           |      |
| ObjectUtil               |           |      |
| PendingWrite             |           |      |
| PlatformDependent        |           |      |
| PromiseNotificationUtil  |           |      |
| ReadOnlyIterator         |           |      |
| RecyclableArrayList      |           |      |
| ReferenceCountUpdater    |           |      |
| ReflectionUtil           |           |      |
| ResourcesUtil            |           |      |
| SocketUtils              |           |      |
| StringUtil               |           |      |
| SystemPropertyUtil       |           |      |
| ThreadExecutorMap        |           |      |
| ThreadLocalRandom        |           |      |
| ThrowableUtil            |           |      |
| TypeParameterMatcher     |           |      |
|                          |           |      |
| Errors                   |           |      |
|                          |           |      |
| OutOfDirectMemoryError   |           |      |
|                          |           |      |
| Annotation Types         |           |      |
|                          |           |      |
| SuppressJava6Requirement |           |      |
| UnstableApi              |           |      |





#### io.netty.util.internal.logging



|                        | 类型      |      |
| ---------------------- | --------- | ---- |
| Interfaces             |           |      |
|                        |           |      |
| InternalLogger         | interface |      |
|                        |           |      |
| Classes                |           |      |
|                        |           |      |
| AbstractInternalLogger |           |      |
| CommonsLoggerFactory   |           |      |
| FormattingTuple        |           |      |
| InternalLoggerFactory  |           |      |
| JdkLoggerFactory       |           |      |
| Log4J2LoggerFactory    |           |      |
| Log4JLoggerFactory     |           |      |
| MessageFormatter       |           |      |
| Slf4JLoggerFactory     |           |      |
|                        |           |      |
| Enums                  |           |      |
|                        |           |      |
| InternalLogLevel       |           |      |





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
    }
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



