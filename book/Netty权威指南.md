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
ChannelHandlerContext


粘包
LineBasedFrameDecoder StringDecoder
组合就是按行切换的文本解码器,它被设计用来支持TCP的粘包与拆包


io.netty.handler.codec.LineBasedFrameDecoder


io.netty.handler.codec.string.StringDecoder


MessageToMessageDecoder
MessageToByteEncoder
这两个抽象类


