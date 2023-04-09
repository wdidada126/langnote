# Netty权威指南



netty，不是写代码炫技，是为了解决问题



https://book.douban.com/subject/26373138/



[林锋](https://book.douban.com/search/李林锋)



Java 1.4 NIO


NIO 2.0

AsynchronousServerSocketChannel

    public abstract <A> void accept(A attachment,
                                    CompletionHandler<AsynchronousSocketChannel,? super A> handler);




java.nio.channels.CompletionHandler 接口 两个枚举值

java.nio.channels.AsynchronousSocketChannel类
public static AsynchronousSocketChannel open()静态方法
public abstract <A> void connect(SocketAddress remote,
                                     A attachment,
                                     CompletionHandler<Void,? super A> handler)



CountDownLatch
- .await()
- countDown()



public interface CompletionHandler<V,A> {
	void completed(V result, A attachment);
	void failed(Throwable exc, A attachment);
}



 TimeServer 开发
   在开始使用Netty开发TimeServer之前，先回顾一下使用NIO进行服务端开发的步骤。
   (1)创建ServerSocketChannel,配置它为非阻塞模式；
   (2)绑定监听，配置TCP参数，例如backlog大小：
   (3)创建一个独立的I/O线程，用于轮询多路复用器Selector；
   (4)创建Selector,将之前创建的ServerSocketChannel注册到Selector上，监听 SelectionKey. ACCEPT ：
   (5)启动I/O线程，在循环体中执行Selector.select()方法，轮询就绪的Channel：
   (6)当轮询到了处于就绪状态的Channel时，需要对其进行判断，如果是OP_ACCEPT 状态，说明是新的客户端接入，则调用ServerSocketChannel.accept。方法接受新的客户端；
   (7)设置新接入的客户端链路Socketchannel为非阻塞模式，配置其他的一些TCP参数；
   (8)将 SocketChannel 注册到 Selector,监听 OP READ 操作位；
   (9)如果轮询的Channel为OP_READ,则说明SocketChannel中有新的就绪的数据包 需要读取，则构造ByteBuffer对象，读取数据包：
   (10)如果轮询的Channel为OP WRITE,说明还有数据没有发送完成，需要继续发送。


### Chap. 4

继承ChannelHandlerAdapter，实现业务读写操作
ChannelHandlerContext   io.netty.channel.ChannelHandlerContext 接口

writeAndFlush(Object o)


粘包
LineBasedFrameDecoder StringDecoder
组合就是按行切换的文本解码器,它被设计用来支持TCP的粘包与拆包


io.netty.handler.codec.LineBasedFrameDecoder


io.netty.handler.codec.string.StringDecoder


MessageToMessageDecoder
MessageToByteEncoder
这两个抽象类


### Chap. 5

FixedLengthFrameDecoder

DelimiterBasedFrameDecoder

delimiter 分隔符 定界符

### 6序列化方案

pb
thrift
jboss  Marshalling

### 7

io.netty.handler.codec.serialization.ObjectDecoder

ObjectEncoder

第8 章Google Protobuf 编解码

第9 章JBoss Marshalling 编解码




请求方法有多种，各方法的作用如下。
GET：请求获取Request-URI所标识的资源；
POST：在Request-URI所标识的资源后附加新的提交数据；
HEAD：请求获取由Request-URI所标识的资源的响应消息报头；
PUT：请求服务器存储一个资源，并用Request・URI作为其标识；
DELETE：请求服务器删除Request-URI所标识的资源；
TRACE：请求服务器回送收到的请求信息，主要用于测试或诊断：
CONNECT：保留将来使用；
OPTIONS：请求查询服务器的性能，或者查询与资源相关的选项和需求。

### 10

http实现文件服务器handler继承抽象类
SimpleChannelInboundHandler


FullHttpRequest


			    ChannelPipeline pipeline = ch.pipeline();
			    pipeline.addLast("http-codec",
				    new HttpServerCodec());
			    pipeline.addLast("aggregator",
				    new HttpObjectAggregator(65536));
			    ch.pipeline().addLast("http-chunked",
				    new ChunkedWriteHandler());

public final class HttpServerCodec extends ChannelHandlerAppender

io.netty.handler.codec.http.HttpServerCodec

io.netty.handler.codec.http.HttpObjectAggregator

io.netty.handler.stream.ChunkedWriteHandler

### 11
ws


WebSocketFrame




源码分析篇 Netty 功能介绍和源码分析

第15 章ByteBuf 和相关辅助

16 章Channel 和Unsafe

17 章ChannelPipeline 和ChannelHandler

18 章EventLoop 和EventLoopGroup

19 章Future 和Promise

20 章Netty 架构剖析


