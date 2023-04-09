# Netty实战

Netty权威指南（第2版）
https://book.douban.com/subject/26373138/

- - EventLoop—控制流、多线程处理、并发
- Channel—Socket
- ChannelFuture—异步通知


- 新的Channel已被接受并且就绪； 
- Channel连接已经完成； 
- Channel有已经就绪的可供读取的数据； 
- Channel可用于写数据



[Netty实战](https://book.douban.com/subject/27038538/)



https://github.com/edidada/Netty-study

netty版本
4.1.17.Final


Shujifenwei四篇



插值器设计模式

第一部分 Netty的概念及体系结构

第一部分 Netty的概念及体系结构
### Chap. 1  Netty——异步和事件驱动

java.net

java.nio

Socker

ServerSocker是阻塞的

nio会有什么问题来着？


### Chap. 2 你的第一款Netty应用程序
NIO

BIO

epoll

？？？

embeded

### Chap. 3 Netty的组件和设计
e
### Chap. 4 传输
Bytebuf
BytebufHandler



### Chap. 5 ByteBuf
ChannelHandler
ChannelFuture
ChannelxxxContext
ChannelPinpile  责任链模式

### Chap. 6 ChannelHandler 和ChannelPipeline
EventLoop
线程池

### Chap. 7 EventLoop 和线程模型




编码器

解码器

### Chap. 8 引导



### Chap. 9 单元测试

EmbededChannel 单元测试


## 第二部分 编解码器

### Chap.10 解码器框架

编码器解码器



### Chap.11 预置的ChannelHandler和编解码器

http封装



请求：httprequest httpcontent htpcontext lastmodifycontent

响应：httprequest httpcontent htpcontext lastmodifycontent



ChannelHandler

addLast

addFirst encode decode

ChannelInitianl

第三部分 网络协议

### Chap.12 WebSocket 

### Chap.13 使用UDP 广播事件

## 第四部分 案例研究
### Chap.14 案例研究，第一部分

### Chap.15 案例研究，第二部分

