# 第 5 章 Netty 核心原理与基础实战（卷1）

> Netty 架构：`Channel`/`EventLoop`/`ChannelPipeline`/`ChannelHandler`/`Bootstrap`、ByteBuf、入站/出站、粘包半包。本书把 Netty「为什么快」讲透，是后续 IM/HTTP 的底座。

## 一、本章地图

| 组件 | 角色 |
| --- | --- |
| Channel | 连接抽象（SocketChannel/NioSocketChannel） |
| EventLoop | Reactor 线程，绑一个 Selector |
| Pipeline | 责任链，Inbound/Outbound Handler |
| ByteBuf | 读写索引分离的缓冲（取代 ByteBuffer） |
| Bootstrap | 客户端/服务端启动器 |

## 二、核心精讲

### 2.1 🔧 ByteBuf 双索引
- `readerIndex`/`writerIndex` 分离，无需 `flip`；`slice`/`duplicate` 零拷贝视图（🔧 引用计数 `ReferenceCounted`，`release()` 不当会泄漏或提前释放；Netty 4.1+ 配 `ResourceLeakDetector`）。

### 2.2 Pipeline 责任链
- 入站（解码/业务）从头到尾，出站（编码）从尾到头（🔧 半包黏包在 `ByteToMessageDecoder` 处理；业务 Handler 别阻塞 EventLoop）。

### 2.3 虚拟线程承载
- Netty 4.1.90+ 支持 `EventLoop` 用虚拟线程跑 Handler，简化同步写法（🔧 但 `channelRead` 内阻塞仍要小心，pin 问题见《之美》08 章）。

## 三、版本演进 / 论文 / 前沿

- 论文：Schmidt Reactor（POSA2'96）；Netty 源自 Apache MINA，由 Trustin Lee 重写。
- 工业界：Netty（34k）、gRPC-Java（Netty 传输）、Dubbo、RocketMQ 底层均 Netty。
- 开源 stars（2026-09）：netty 34k / grpc-java 11k / dubbo 41k。

## 四、常见误区 / 本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "ByteBuf 用 flip" | 双索引，不用 flip |
| 2 | "Handler 里阻塞" | 丢业务线程池/虚拟线程 |
| 3 | "忘记 release" | 引用计数泄漏 |
| 4 | "2026 还全异步 Handler" | 可虚拟线程承载 |
