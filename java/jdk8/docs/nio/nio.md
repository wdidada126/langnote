# nio


Java nio

SPI

Windows上
Xxx-Provider


since 1.4
Java.nio下面直接的类为一堆的Buffer缓冲类，后面的各种Channel都是基于Buffer类进行操作的。

揭开Java.nio的最后块神秘的知识点，Charset编码类，他的功能主要是实现字节与Unicode之间的转码转换。同样先来看看他的包结构。，结构比较单一和简单。

java.nio包的分析(三)---Charset的理解
https://blog.csdn.net/Androidlushangderen/article/details/39754551

- java.nio.charset
- java.nio.file
- java.nio


```java

Buffer
CharBuffer

SelectorProvider (java.nio.channels.spi)
    SelectorProviderImpl (sun.nio.ch)
        WindowsSelectorProvider (sun.nio.ch)

```

[ibm java nio2](https://www.ibm.com/developerworks/cn/java/j-nio2-1/index.html)

[ifeve nio](http://ifeve.com/java-nio-all/)

http://svip.iocoder.cn/Netty/nio-2-channel/
java.nio.channels.Channel ，定义了 IO 操作的连接与关闭
Channel 有非常多的实现类，最为重要的四个 Channel 实现类如下：

- SocketChannel ：一个客户端用来发起 TCP 的 Channel 。
- ServerSocketChannel ：一个服务端用来监听新进来的连接的 TCP 的 Channel 。对于每一个新进来的连接，都会创建一个对应的 SocketChannel 。
- DatagramChannel ：通过 UDP 读写数据。
- FileChannel ：从文件中，读写数据。


java.nio.channels.SocketChannel 抽象类
java.nio.channels.ServerSocketChannel 抽象类

我们可以将 Buffer 理解为一个数组的封装，例如 IntBuffer、CharBuffer、ByteBuffer 等分别对应 int[]、char[]、byte[] 等。

Buffer 中有 4 个非常重要的属性：capacity、limit、position、mark


nio编程Server端

```java

        SocketChannel socketChannel = null;
        Selector selector = null;
        try {
            socketChannel = SocketChannel.open();//调用SelectorProvider，用了SPI
            socketChannel.configureBlocking(false);
            socketChannel.connect(new InetSocketAddress("127.0.0.1", 1234));

            selector = Selector.open();
            socketChannel.register(selector, SelectionKey.OP_CONNECT);
```

java.nio.channels.Pipe  一组channel


Selector

java nio与OS并发库
linux epoll
Windows iocp


