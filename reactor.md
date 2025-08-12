# reactor

io模型: 支持 reactor(for network) and async-io(for disk)
来源：https://github.com/trpc-group/trpc-cpp/blob/main/README.zh_CN.md

tinywebserver面试题
https://zhuanlan.zhihu.com/p/368154495?utm_id=0

https://github.com/qinguoyi/TinyWebServer

reactor反应堆模式

Netty

语言层面

rxjava2

reactorproject

原理：多核计算机

Java抽象函数有没有构造函数？

    <dependency>
        <groupId>io.projectreactor</groupId>
        <artifactId>reactor-core</artifactId>
        <version>3.4.9</version> <!-- 替换为你需要的版本号 -->
    </dependency>

reactor-core 是 Reactor 框架的核心模块，提供了响应式编程中的 Mono、Flux 等核心类型
reactor.core.publisher.Mono

reactor.core.publisher.Flux
`reactor.core.publisher.Mono` 和 `reactor.core.publisher.Flux` 是 Reactor 框架中两个重要的类，用于支持响应式编程。它们都是 Reactor 框架中的 Publisher（发布者）类型，用于向订阅者（Subscriber）发布事件流。

`Mono` 类表示一个包含单个元素或者空值的响应式数据流。当你需要返回一个异步结果时，可以使用 `Mono` 类型，例如从数据库中获取一条记录、从远程服务中获取一个结果等。`Mono` 类提供了一系列的操作符，可以方便地对异步结果进行处理，例如映射、过滤、合并等。

`Flux` 类表示一个包含多个元素的响应式数据流。当你需要返回一个多个元素的数据流时，可以使用 `Flux` 类型，例如从数据库中获取多条记录、从消息队列中获取多个消息等。`Flux` 类也提供了许多操作符，可以支持数据流的处理、转换、合并和批处理等。

在 Reactor 框架中，`Mono` 和 `Flux` 类型都是 Publisher（发布者）类型，它们都是基于 Reactive Stream 规范的，可以被订阅者（Subscriber）订阅。当一个 `Mono` 或 `Flux` 对象被订阅时，它会在后台执行异步任务，并在任务完成后发出通知，通知订阅者处理结果。在订阅过程中，可以使用操作符对数据流进行处理和转换，例如过滤、映射、合并、聚合等。

需要注意的是，`Mono` 和 `Flux` 类型是不可变的，也就是说，一旦创建就不可修改。这意味着每个操作符都会生成一个新的 `Mono` 或 `Flux` 对象，而不会修改原始的对象。这种不可变性可以确保数据流的稳定性和可靠性，同时也可以方便地进行线程安全的并发处理。

总之，`Mono` 和 `Flux` 类型是 Reactor 框架中的核心类型，用于支持响应式编程，可以方便地处理异步数据流。在使用这些类型时，需要注意处理异常、确保数据流的稳定性和可靠性，并合理使用操作符，以提高应用程序的性能和可维护性。

Reactive Stream 规范旨在定义一组通用的 API，用于支持异步数据流的处理和传输。这个规范由一组主要的 Java 技术公司（包括 Netflix、Pivotal、Lightbend 和 Red Hat）共同制定，旨在为响应式编程提供标准化的接口。

Reactive Stream 规范的官方网站是 https://www.reactive-streams.org/，你可以在该网站上找到有关规范的详细文档、示例代码、实现库和社区支持等资源。在 Reactive Stream 规范中，定义了以下四个核心接口：

1. `Publisher`：表示一个数据流的发布者，可以向订阅者发布数据流。
2. `Subscriber`：表示一个数据流的订阅者，可以从发布者接收数据流，并对数据流进行处理。
3. `Subscription`：表示一个订阅关系，用于管理发布者和订阅者之间的数据流传输。
4. `Processor`：表示一个数据流的处理器，可以同时充当发布者和订阅者的角色，并对数据流进行处理。

这些接口定义了响应式数据流的基本操作和交互方式，可以方便地实现异步数据流的处理和传输。在 Reactive Stream 规范中，还定义了一些标准的操作符和异常处理机制，可以帮助开发者更好地处理异步数据流。
需要注意的是，Reactive Stream 规范只定义了一组通用的接口和规范，没有提供具体的实现。因此，开发者需要使用具体的实现库来支持 Reactive Stream 规范，例如 Reactor、RxJava、Akka Streams 等。这些实现库都提供了符合 Reactive Stream 规范的 Publisher、Subscriber、Subscription 和 Processor 接口的实现，可以方便地进行异步数据流的处理和传输。
总之，Reactive Stream 规范为响应式编程提供了标准化的接口和规范，可以方便地实现异步数据流的处理和传输，并提高应用程序的性能和可维护性。如果你想深入了解 Reactive Stream 规范，可以访问官方网站并参考相关文档、示例和实现库。

spring 5使用

以下是针对游双《Linux高性能服务器编程》中提到的多线程编程模式，结合 Reactor、Netty 和 P开头的模式（如 Proactor）的总结与示例：

### 1. Reactor 模式（核心）
#### 特点：
• 事件驱动：通过事件循环（Event Loop）监听I/O事件（如`epoll`）。

• 非阻塞：主线程不阻塞，事件就绪后分发给工作线程处理。

• Netty 实现：`NioEventLoop` + `ChannelPipeline`。


#### 代码示例（简化版Netty Reactor）：
```java
EventLoopGroup bossGroup = new NioEventLoopGroup(1);  // 主Reactor（处理连接）
EventLoopGroup workerGroup = new NioEventLoopGroup(); // 子Reactor（处理I/O）

ServerBootstrap b = new ServerBootstrap();
b.group(bossGroup, workerGroup)
 .channel(NioServerSocketChannel.class)
 .childHandler(new ChannelInitializer<SocketChannel>() {
     @Override
     protected void initChannel(SocketChannel ch) {
         ch.pipeline().addLast(new MyHandler()); // 业务处理器
     }
 });
ChannelFuture f = b.bind(8080).sync();
```


### 2. Proactor模式
#### 特点：
• 异步I/O：由操作系统完成I/O操作（如Windows IOCP），应用只需处理完成事件。

• 与Reactor对比：

  • Reactor：通知“何时可读写” → 应用自己读写。

  • Proactor：通知“读写已完成” → 直接处理数据。


#### Linux模拟Proactor：
Linux原生不支持Proactor，但可通过 Reactor + 异步I/O（如`aio_read`） 模拟：
1. 主线程调用`aio_read`提交异步读请求。
2. 内核完成读操作后，通知事件循环。
3. 工作线程直接处理已读取的数据。

### 3. Producer-Consumer 模式（P开头）
#### 应用场景：
• 任务队列：生产者线程生成任务，消费者线程处理任务。

• Netty 示例：通过`EventLoop`的任务队列（`execute()`提交任务）。


#### 代码示例：
```java
Channel channel = ...;
channel.eventLoop().execute(() -> {
    System.out.println("异步任务执行");
});
```

### 4. Pipeline 模式
#### 特点：
• 将任务分解为多个阶段，每个阶段由独立线程处理。

• Netty 应用：`ChannelPipeline`中的处理器链（如解码→业务处理→编码）。


#### 示例：
```java
ch.pipeline()
  .addLast(new ByteToMessageDecoder())  // 阶段1：解码
  .addLast(new BusinessHandler())       // 阶段2：业务处理
  .addLast(new MessageToByteEncoder()); // 阶段3：编码
```

### 5. Thread Pool 模式
#### Netty 中的应用：
• `EventLoopGroup`本质是线程池，处理I/O和普通任务。
• 可通过`DefaultEventExecutorGroup`实现业务线程池隔离。


#### 配置示例：
```java
EventExecutorGroup businessGroup = new DefaultEventExecutorGroup(8);
ch.pipeline().addLast(businessGroup, new BusinessHandler()); // 业务逻辑交给独立线程池
```

### 6. 模式对比与选择
| 模式          | 适用场景                          | 优势                          | 劣势                  |
|---------------|-----------------------------------|-------------------------------|-----------------------|
| Reactor   | 高并发I/O（如HTTP服务器）         | 资源消耗低，扩展性强          | 依赖操作系统I/O多路复用 |
| Proactor  | 异步I/O场景（如文件操作）         | 减少应用层线程阻塞            | Linux支持不完善        |
| Producer-Consumer | 任务异步处理          | 解耦生产与消费                | 队列管理复杂度高      |

### 7. 性能优化建议
1. Reactor 线程数：通常设为CPU核心数（避免上下文切换）。
2. 避免阻塞EventLoop：耗时任务交给独立线程池（如数据库查询）。
3. 零拷贝：Netty的`FileRegion`减少内存复制。

### 总结
游双书中提到的多线程模式在Netty中均有体现：
• Reactor 是Netty的核心。
• Proactor 在Linux中需模拟实现。

• Producer-Consumer 和 Pipeline 模式用于任务分解与处理。


建议结合《Linux高性能服务器编程》第6章（I/O复用）和第8章（多线程）深入理解底层原理。

Proactor多线程提高并发

这是一个极其深入、专业且高质量的问题！你不仅关心 如何提升 Spring Boot 嵌入式 Tomcat 的并发性能，还深入到 `tomcat-embed-*` 各模块的 9.0.70 版本源码分析，并提出了一个关键架构问题：Tomcat 是 Reactor 模式还是 Proactor 模式？

我们来系统性地、逐层剖析这个问题。

---

## 🧱 一、Spring Boot 嵌入式 Tomcat 模块概览（9.0.70）

| JAR 包 | 作用 | 是否影响并发 |
|--------|------|-------------|
| `tomcat-embed-core` | 核心：连接器、容器、生命周期、NIO 实现 | ✅ 核心 |
| `tomcat-embed-el` | EL 表达式引擎（JSP 使用） | ❌ 无 |
| `tomcat-embed-jasper` | JSP 编译引擎 | ❌ 无 |
| `tomcat-embed-logging-juli` | JULI 日志适配器（Tomcat 使用 java.util.logging） | ⚠️ 低影响 |
| `tomcat-embed-logging-log4j` | Log4j 支持（已废弃） | ❌ 无 |
| `tomcat-embed-websocket` | WebSocket 支持（基于 NIO） | ✅ 高并发场景相关 |

> ✅ 真正影响并发性能的是 `tomcat-embed-core` 和 `tomcat-embed-websocket`。

---

## 🚀 二、如何提高嵌入式 Tomcat 的并发性能？

### ✅ 1. 调整线程池参数（最有效）

```yaml
# application.yml
server:
  tomcat:
    max-threads: 800          # 默认 200，建议 500~1000
    min-spare-threads: 100     # 避免频繁创建线程
    accept-count: 100          # 队列长度，超过则拒绝
    connection-timeout: 20000  # 连接超时
    max-connections: 10000     # 最大连接数
```

> 🔍 源码位置：`org.apache.tomcat.util.net.NioEndpoint`

---

### ✅ 2. 启用异步处理（Async Servlet）

避免阻塞工作线程：

```java
@GetMapping("/async")
public Callable<String> async() {
    return () -> {
        Thread.sleep(2000);
        return "Done";
    };
}
```

> ✅ 释放 Tomcat 线程，提升吞吐量。

---

### ✅ 3. 使用 GZIP 压缩减少传输量

```yaml
server:
  compression:
    enabled: true
    mime-types: text/html,text/xml,text/plain,text/css,application/json
    min-response-size: 1024
```

---

### ✅ 4. 调整 JVM 参数

```bash
-Xms2g -Xmx2g
-XX:+UseG1GC
-XX:MaxGCPauseMillis=200
```

避免 GC 停顿影响响应时间。

---

### ✅ 5. 使用 NIO2（AIO）或 APR（可选）

- NIO2（AIO）：Linux 上使用 `epoll`，性能更高
- APR：基于本地库（如 `libtcnative`），支持 `sendfile`、`OpenSSL`

```xml
<!-- 需要引入 APR 库 -->
<Connector protocol="org.apache.coyote.http11.Http11AprProtocol" ... />
```

---

## 🔍 三、`tomcat-embed-core` 9.0.70 源码关键分析

### 1. 核心类结构

```
Tomcat
└── Connector (Http11NioProtocol)
    └── ProtocolHandler
        └── AbstractHttp11Protocol
            └── AbstractHttp11JsseProtocol
                └── Http11NioProtocol
                    └── NioEndpoint
                        ├── Acceptor（接收连接）
                        ├── Poller（事件轮询）
                        └── Worker（执行任务）
```

---

### 2. `NioEndpoint`：NIO 的核心实现

路径：`org.apache.tomcat.util.net.NioEndpoint`

#### 关键组件：

| 组件 | 作用 |
|------|------|
| `Acceptor` | 接收新连接，注册到 `Poller` |
| `Poller` | 使用 `Selector` 监听 I/O 事件（读/写） |
| `Worker` | 从线程池中取出线程处理请求（`SocketProcessor`） |

#### 源码片段（简化）：

```java
// NioEndpoint.java
public void startInternal() {
    // 创建多个 Poller 线程
    for (int i = 0; i < pollerThreadCount; i++) {
        pollers[i] = new Poller();
        Thread pollerThread = new Thread(pollers[i], "Poller-" + i);
        pollerThread.start();
    }

    // 创建 Acceptor 线程
    acceptor = new Acceptor();
    Thread acceptorThread = new Thread(acceptor, "Acceptor");
    acceptorThread.start();
}
```

> 🔥 `pollerThreadCount` 默认是 `Math.min(2, Runtime.getRuntime().availableProcessors())`

---

### 3. `Poller` 类：事件驱动核心

```java
// Poller.java
public boolean events() {
    for (SelectionKey key : selector.keys()) {
        NioChannel channel = (NioChannel) key.attachment();
        int readyOps = key.readyOps();
        if ((readyOps & SelectionKey.OP_READ) != 0) {
            // 提交任务到线程池
            executor.execute(new SocketProcessor(channel, SocketEvent.OPEN_READ));
        }
    }
}
```

> ✅ 事件触发后，将任务提交给线程池处理，非阻塞。

---

## 🧠 四、Tomcat 是 Reactor 模式还是 Proactor 模式？

这是本问题的核心！

### ✅ 结论：

> Tomcat 使用的是 Reactor 模式（反应器模式），不是 Proactor。

---

### 1. Reactor 模式 vs Proactor 模式

| 特性 | Reactor 模式 | Proactor 模式 |
|------|--------------|---------------|
| I/O 操作谁做 | 用户线程自己读写 | 内核完成 I/O，回调通知 |
| 数据是否就绪 | 通知“数据可读”，需主动读 | 通知“数据已读完” |
| 代表框架 | Netty、Tomcat、Redis | Windows IOCP、Linux AIO（有限） |
| 模型 | 同步 I/O 多路复用 | 异步 I/O |

---

### 2. Tomcat 的工作流程（Reactor 模式）

```mermaid
graph TD
    A[Acceptor] -->|接收连接| B[Poller]
    B -->|监听 OP_READ| C{Selector}
    C -->|事件就绪| D[Worker Thread]
    D -->|read() 读取数据| E[业务处理]
    D -->|write() 发送响应| F[Client]
```

1. Reactor（Poller）：监听 I/O 事件（`OP_READ`、`OP_WRITE`）
2. 事件就绪后：通知线程池中的 Worker 线程
3. Worker 线程：主动调用 `read()` 和 `write()` 完成 I/O 操作

> 🔍 这正是 Reactor 模式的典型特征：I/O 操作由用户线程完成，内核只通知“可以读写了”。

---

### 3. 为什么不是 Proactor？

- Proactor 要求操作系统支持 真正的异步 I/O（AIO）
- Linux 的 `aio_read`/`aio_write` 仅对 文件 I/O 有效，对 网络 I/O 实际上是用线程池模拟的（伪异步）
- Tomcat 的 `NioEndpoint` 使用的是 Java NIO 的 `Selector` + `SocketChannel`，属于 同步非阻塞 I/O（Reactor）
- 即使使用 `Nio2Endpoint`（基于 `AsynchronousChannel`），Java 的 AIO 也是通过线程池实现，不是真正的 Proactor

> 📌 所以：Tomcat 是 Reactor 模式。

---

## 🧩 五、`tomcat-embed-websocket` 如何支持高并发？

- 基于 `NioEndpoint`，共享同一套 I/O 线程
- WebSocket 连接注册为 `SelectionKey.OP_READ` 事件
- 消息到达时，由 `Poller` 触发，`WebSocketProcessor` 处理
- 支持 `@ServerEndpoint` 和 `Session.getAsyncRemote()` 异步发送

> ✅ 高并发 WebSocket 场景下，Tomcat 表现良好。

---

## 📊 六、性能调优建议总结

| 优化项 | 推荐值 | 说明 |
|--------|--------|------|
| `max-threads` | 500~1000 | 根据 CPU 核心数和业务耗时调整 |
| `min-spare-threads` | 50~100 | 避免线程创建开销 |
| `accept-count` | 100~500 | 队列长度 |
| `pollerThreadCount` | 2~4 | 默认 `Math.min(2, cores)`，可适当增加 |
| 使用 `GZIP` | ✅ 开启 | 减少网络传输 |
| 异步处理 | ✅ 使用 | 避免阻塞 I/O 线程 |
| JVM GC | G1GC | 低延迟 |

---

## 🧠 七、延伸思考：Netty vs Tomcat

| 框架 | 模式 | 适用场景 |
|------|------|----------|
| Netty | Reactor（多线程） | 高性能 RPC、网关、自定义协议 |
| Tomcat | Reactor（线程池） | HTTP 服务、Spring Web MVC、传统 Web 应用 |

> ✅ Tomcat 更“重”，但功能完整；Netty 更“轻”，但需自行实现 HTTP 协议。

---

## ✅ 总结

1. 提高并发：调优线程池、启用异步、GZIP、JVM 优化。
2. 核心模块：`tomcat-embed-core` 是并发性能的关键。
3. 设计模式：Tomcat 使用的是 Reactor 模式，基于 `Selector` 实现事件驱动。
4. 不是 Proactor：Java 的 AIO 并非真正的异步 I/O，Tomcat 本质是同步非阻塞。
5. 源码位置：`NioEndpoint`、`Poller`、`SocketProcessor` 是核心类。

---

如果你想看：
- `NioEndpoint` 如何处理 `OP_WRITE` 事件
- `SocketProcessor` 的状态机设计
- Spring Boot 如何自动配置 `TomcatServletWebServerFactory`
- Tomcat 10+ 的 `Http2Protocol` 源码分析

在C和C++中，确实存在多个高性能的服务端库或框架实现了Reactor模式。此外，关于Qt是否实现Reactor模式的问题，下面将详细解答。

C/C++中的Reactor模式服务端库/框架
Boost.Asio
Boost.Asio是一个跨平台的C++库，主要用于网络和底层I/O编程。它提供了一个强大的异步模型，支持Reactor模式。Boost.Asio允许开发者编写高效的、可移植的网络应用。
它不仅限于TCP/IP协议，还支持UDP和其他传输层协议，以及串行端口通信等。
libevent
libevent是一个事件通知库，其API为各种I/O事件提供了抽象层。它使用了Reactor模式，并且可以自动选择最合适的后端（如epoll, kqueue, /dev/poll, select等）来处理事件。
libevent非常适合构建高并发的服务端应用，因为它能够有效地管理大量的连接。
libuv
libuv最初是为Node.js开发的，但现在也被广泛用于其他需要高效异步I/O的应用程序中。它采用了Reactor模式，并且支持异步文件系统操作、DNS查询、网络等功能。
libuv的一个主要优点是它的跨平台能力，使得相同的代码可以在不同操作系统上运行而无需修改。
Poco C++ Libraries
Poco也提供了一套全面的网络库，其中包括对Reactor模式的支持。Poco的设计目标之一就是简化复杂网络应用的开发过程，同时保持良好的性能。

以下是 Go、Rust、C#、Dart 和 Swift 中实现 Reactor 模式 的高性能服务端框架或库，按语言分类整理：

1. Go

标准库 net（基于Reactor模式）

• 特点：Go 的 net 包底层使用 I/O 多路复用（如 Linux 的 epoll），协程（Goroutine）处理连接，天然适合高并发。

• 示例：
  ln, _ := net.Listen("tcp", ":8080")
  for {
      conn, _ := ln.Accept()
      go handleConn(conn) // 每个连接一个Goroutine
  }
  
• 高性能框架：

  • https://github.com/panjf2000/gnet：基于事件驱动的轻量级网络库，类似 Netty。
    type echoServer struct{ gnet.EventHandler }
    func (es *echoServer) React(frame []byte, c gnet.Conn) (out []byte, action gnet.Action) {
        out = frame // Echo逻辑
        return
    }
    gnet.Serve(&echoServer{}, "tcp://:8080")
    

2. Rust

标准库 std::net + mio

• mio：底层I/O多路复用库（支持 epoll/kqueue）。
  use mio::{Events, Poll, Token, Interest};
  let mut poll = Poll::new()?;
  poll.registry().register(&mut socket, Token(0), Interest::READABLE)?;
  let mut events = Events::with_capacity(1024);
  poll.poll(&mut events, None)?; // Reactor核心循环
  
• 高性能框架：

  • https://tokio.rs/：异步运行时，基于Reactor模式。
    #[tokio::main]
    async fn main() {
        let listener = TcpListener::bind("127.0.0.1:8080").await.unwrap();
        while let Ok((socket, _)) = listener.accept().await {
            tokio::spawn(async move { /* 处理连接 */ });
        }
    }
    
  • https://actix.rs/：基于Tokio的Actor框架（常用于Web服务）。

3. C# (.NET)

SocketAsyncEventArgs（基于Proactor/Reactor混合）

• 底层：Windows 使用 IOCP（Proactor），Linux 使用 epoll（Reactor）。

• 高性能框架：

  • https://learn.microsoft.com/en-us/aspnet/core/fundamentals/servers/kestrel：ASP.NET Core 的默认服务器，基于事件驱动。
    WebHost.CreateDefaultBuilder().UseKestrel().Configure(...).Build().Run();
    
  • https://github.com/chronoxor/NetCoreServer：纯Reactor模式库。
    var server = new EchoServer("127.0.0.1", 8080);
    server.Start();
    

4. Dart

dart:io 事件循环

• 特点：Dart VM 使用事件循环（类似Reactor），单线程异步I/O。

• 高性能框架：

  • https://pub.dev/packages/shelf：轻量级HTTP服务器（底层基于 dart:io）。
    var server = await serve((request) => Response.ok('Hello'), 'localhost', 8080);
    
  • https://aqueduct.io/（已归档）：类似Flask的异步框架。

5. Swift

SwiftNIO（核心Reactor实现）

• https://github.com/apple/swift-nio：苹果官方的高性能网络框架，类似Netty。
  let group = MultiThreadedEventLoopGroup(numberOfThreads: System.coreCount)
  let bootstrap = ServerBootstrap(group: group)
      .childChannelInitializer { channel in
          channel.pipeline.addHandler(MyHandler())
      }
  let channel = try bootstrap.bind(host: "127.0.0.1", port: 8080).wait()
  try channel.closeFuture.wait() // Reactor事件循环
  
• 衍生框架：

  • https://vapor.codes/：基于SwiftNIO的Web框架。

横向对比（性能与适用场景）

语言 推荐框架 底层机制 适用场景

Go gnet epoll + Goroutine 高频连接（如游戏服务器）

Rust Tokio epoll/kqueue 低延迟微服务

C# Kestrel IOCP/epoll Web API

Dart Shelf 事件循环 轻量级HTTP服务

Swift SwiftNIO kqueue/epoll macOS/iOS后端服务

关键点总结

1. Reactor本质：所有框架均基于 I/O多路复用 + 事件分发。
2. 语言特性影响：
   • Go 的 Goroutine 简化了并发编程。

   • Rust 的 Tokio 强调零成本抽象。

   • SwiftNIO 与 Netty 设计高度相似。

3. 选择建议：
   • 需要极致性能：Rust（Tokio）或 Go（gnet）。

   • 跨平台需求：C#（Kestrel）或 Swift（SwiftNIO）。

以下是关于 Reactor 模式 的经典论文、书籍和权威资料推荐，涵盖设计原理、实现细节和实际应用场景：

1. 经典论文

(1) 《Reactor: An Object Behavioral Pattern for Concurrent Event Demultiplexing and Event Handler Dispatching》

• 作者: Douglas C. Schmidt（ACE框架作者，模式大师）

• 出处: Pattern Languages of Program Design (PLoP) 1995

• 核心内容:

  • 首次提出 Reactor 模式的定义，描述其核心组件（事件多路复用器、事件处理器、分发器）。

  • 对比 Reactor 与 Proactor 的适用场景。

• 获取: https://www.dre.vanderbilt.edu/~schmidt/PDF/Reactor.pdf

(2) 《Scalable I/O: Event-Driven Architectures》

• 作者: Dan Kegel（C10K问题提出者）

• 出处: 1999年

• 核心内容:

  • 分析高并发服务器的设计挑战，提出事件驱动架构（包括 Reactor）的解决方案。

• 获取: https://keegansl.com/c10k.pdf

2. 书籍推荐

(1) 《Linux高性能服务器编程》
• 作者: 游双
• 章节: 第5章（I/O复用）、第6章（Reactor模式实现）

• 亮点:

  • 结合 Linux 的 epoll 实现 Reactor 模型，代码示例清晰（C++实现）。

  • 对比多线程、多进程与事件驱动的性能差异。

(2) 《Java NIO》

• 作者: Ron Hitchens

• 章节: 第4章（Selector与异步I/O）

• 亮点:

  • 解释 Java NIO 如何实现 Reactor 模式（Selector 即事件多路复用器）。

(3) 《Pattern-Oriented Software Architecture, Volume 2: Patterns for Concurrent and Networked Objects》

• 作者: Douglas C. Schmidt 等

• 章节: Reactor 和 Proactor 模式详解

• 亮点:

  • 从模式语言的角度分析 Reactor 的设计哲学，附带C++实现案例。

(4) 《Netty权威指南》

• 作者: 李林锋
• 亮点:
  • 深入剖析 Netty 的 Reactor 实现（主从 Reactor 线程模型）。

3. 开源项目参考

(1) Netty 源码
• 关键类: NioEventLoop（事件循环）、ChannelPipeline（事件处理链）
• 学习点:
  • 如何将 Reactor 模式与业务逻辑解耦（如 ChannelHandler 设计）。

(2) Redis 源码

• 文件: ae.c（事件驱动核心）
• 亮点:
  • 单线程 Reactor 模型的高效实现（基于 epoll/kqueue）。

(3) libuv（Node.js底层）
• 设计:
  • 跨平台 Reactor 实现（Windows 用 IOCP，Linux 用 epoll）。

4. 在线资源

(1) Reactor Pattern - Wikipedia

• 链接: https://en.wikipedia.org/wiki/Reactor_pattern
• 内容:
  • 简洁的模式定义与组件图。

(2) Douglas C. Schmidt 的课程讲义
• 课程: Pattern-Oriented Software Architecture
• 链接: https://www.dre.vanderbilt.edu/~schmidt/
• 亮点:
  • 包含 Reactor 与 Proactor 的对比幻灯片。

5. 进阶研究

(1) 《The Art of Scalability》
• 作者: Martin L. Abbott, Michael T. Fisher
• 相关章节:
  • 讨论事件驱动架构在大型系统中的应用（如 Netflix）。

(2) 《Systems Performance: Enterprise and the Cloud》
• 作者: Brendan Gregg
• 亮点:
  • 如何通过性能工具（如 perf）分析 Reactor 模式的瓶颈。

学习路径建议

1. 入门: 先读游双的《Linux高性能服务器编程》或 Douglas Schmidt 的论文。
2. 实践: 通过 Netty/Redis 源码理解工业级实现。
3. 深入: 阅读 POSA 卷2，研究模式语言的设计思想。

这些资源将帮助你从理论到实践全面掌握 Reactor 模式。


在 POCO C++ Libraries 中，Reactor 模式主要通过其 Foundation 模块中的 `Poco::Net` 命名空间下的类来实现。特别是 `ServerSocket`, `Socket`, `SocketReactor` 和 `SocketNotifier` 等类，在处理网络通信时体现了 Reactor 模式的应用。以下是与 Reactor 模式相关的几个关键组件及其简要描述：

### 1. SocketReactor

`SocketReactor` 是 POCO 中直接体现 Reactor 模式的核心类之一。它负责管理多个 Socket 的事件监听，并根据不同的事件（如可读、可写等）调用相应的处理器。

- 位置: `Poco/Net/SocketReactor.h`
- 功能: 监听一组 `Socket` 对象的事件，当某个事件发生时，它会通知对应的 `SocketHandler` 进行处理。
- 示例代码:

```cpp
#include "Poco/Net/SocketReactor.h"
#include "Poco/Net/SocketAcceptor.h"
#include "Poco/Net/StreamSocket.h"
#include "Poco/Net/ServerSocket.h"

using Poco::Net::ServerSocket;
using Poco::Net::SocketReactor;
using Poco::Net::SocketAcceptor;

class MyRequestHandlerFactory : public Poco::Net::HTTPRequestHandlerFactory {
    // 实现必要的方法
};

int main(int argc, char argv) {
    ServerSocket svs(8080);
    SocketReactor reactor;
    SocketAcceptor<MyRequestHandlerFactory> acceptor(svs, reactor);

    reactor.run();
}
```

### 2. SocketAcceptor

`SocketAcceptor` 用于接受新的连接请求，并为每个新连接创建一个对应的 `SocketHandler` 实例。

- 位置: `Poco/Net/SocketAcceptor.h`
- 功能: 接受来自客户端的连接请求，并将这些连接交给 `SocketReactor` 来管理。

### 3. SocketNotifier

`SocketNotifier` 用于监视特定文件描述符上的事件，并在事件发生时触发回调函数。

- 位置: `Poco/Net/SocketNotifier.h`
- 功能: 当指定的文件描述符上有事件发生时，`SocketNotifier` 会通知 `SocketReactor`，进而调用相应的处理逻辑。

### 4. Socket

虽然 `Socket` 类本身并不直接与 Reactor 模式相关联，但它提供了底层的套接字操作，是构建基于 Reactor 模式的应用程序的基础。

- 位置: `Poco/Net/Socket.h`
- 功能: 提供了对 TCP/IP 和 UDP 套接字的基本操作接口。

### 5. SocketImpl

`SocketImpl` 是 `Socket` 类的一个内部实现细节，定义了许多具体的套接字操作方法。

- 位置: `Poco/Net/SocketImpl.h`
- 功能: 提供了具体的套接字操作实现，如连接、发送和接收数据等。

### 使用示例

以下是一个简单的例子，演示如何使用 `SocketReactor` 来创建一个基本的服务器端程序，该程序可以接受客户端连接并回显收到的消息。

```cpp
#include "Poco/Net/SocketReactor.h"
#include "Poco/Net/SocketAcceptor.h"
#include "Poco/Net/StreamSocket.h"
#include "Poco/Net/ServerSocket.h"
#include "Poco/Thread.h"

using namespace Poco::Net;
using namespace Poco;

class EchoServiceHandler {
public:
    EchoServiceHandler(StreamSocket& socket, SocketReactor& reactor):
        _socket(socket),
        _reactor(reactor)
    {
        _reactor.addEventHandler(_socket, NObserver<EchoServiceHandler, ReadableNotification>(*this, &EchoServiceHandler::onReadable));
    }

    void onReadable(const AutoPtr<ReadableNotification>& pNf)
    {
        char buffer[256];
        int n = _socket.receiveBytes(buffer, sizeof(buffer));
        if (n > 0)
        {
            _socket.sendBytes(buffer, n);
        }
        else
        {
            _reactor.removeEventHandler(_socket, NObserver<EchoServiceHandler, ReadableNotification>(*this, &EchoServiceHandler::onReadable));
            _socket.close();
        }
    }

private:
    StreamSocket _socket;
    SocketReactor& _reactor;
};

class EchoService {
public:
    EchoService():
        _reactor(),
        _acceptor(ServerSocket(9999), _reactor)
    {
        _thread.start(_reactor);
    }

    ~EchoService()
    {
        _reactor.stop();
        _thread.join();
    }

private:
    SocketReactor _reactor;
    SocketAcceptor<EchoServiceHandler> _acceptor;
    Thread _thread;
};

int main(int argc, char argv) {
    try {
        EchoService echoService;
        std::cout << "Echo server started on port 9999." << std::endl;
        for (;;) FastMutex::sleep(1000);
    }
    catch (Exception& exc) {
        std::cerr << exc.displayText() << std::endl;
        return 1;
    }
    return 0;
}
```

这段代码展示了如何使用 `SocketReactor` 和 `SocketAcceptor` 来设置一个简单的回声服务器。每当有新的客户端连接时，都会创建一个新的 `EchoServiceHandler` 实例来处理这个连接上的所有通信。

以下是 MySQL Server、Redis、Kafka 的 I/O 模型分析，明确它们是否使用 Reactor 模式，并对比其设计差异：

1. MySQL Server
I/O 模型：混合模式（Reactor + 线程池）

• 连接管理：  
  • 主线程 使用 Reactor 模式（通过 poll/epoll/kqueue 监听客户端连接请求）。  
  • 接收到新连接后，交给 线程池 处理 SQL 解析、存储引擎操作等耗时任务。  

• 存储引擎层：  
  • InnoDB 使用后台线程处理刷盘、日志等操作（非事件驱动）。  

• 结论：  
  前端连接管理是 Reactor，后端业务处理是线程池。

2. Redis

I/O 模型：单线程 Reactor 模式（核心网络模块）

• 事件循环：  
  • 基于 epoll/kqueue（Linux/macOS）或 select（旧版本）实现 Reactor。  
  • 单线程处理所有客户端请求（避免锁竞争）。  

• 异步任务：  

  • 持久化（RDB/AOF）由子进程或后台线程完成，不阻塞主 Reactor。  

• 关键代码（ae.c）：  
  void aeMain(aeEventLoop *eventLoop) {
      while (!eventLoop->stop) {
          aeProcessEvents(eventLoop, AE_ALL_EVENTS); // Reactor核心循环
      }
  }
  
• 结论：  
  纯 Reactor 模式（单线程事件驱动），但持久化等操作例外。

3. Kafka

I/O 模型：多线程 Reactor 模式
• 网络层：  
  • 基于 Java NIO 的 Selector（Reactor 模式）监听 Socket 事件。  
  • 主 Reactor 接收连接，子 Reactor 处理 I/O 读写（类似 Netty 的主从模型）。  
• 业务处理：  
  • 生产者/消费者请求由 线程池 处理（解耦网络 I/O 与业务逻辑）。  
• 关键设计：  
  • SocketServer 类管理 Reactor 线程，KafkaRequestHandler 处理业务。  
• 结论：  
  Reactor 模式（网络层） + 线程池（业务层）。

4. 对比总结
组件 I/O 模型 线程模型 适用场景
MySQL Reactor（连接） + 线程池（SQL） 多线程 高并发事务处理
Redis 单线程 Reactor 单线程（网络） + 后台线程 低延迟、高吞吐缓存
Kafka 多线程 Reactor + 线程池 多线程 高吞吐消息队列

5. 常见误解澄清
1. Redis 是“单线程”：  
   • 仅指 网络 I/O 和命令执行 是单线程，持久化、集群通信等仍用多线程/多进程。  
2. Kafka 的“异步”：  
   • 网络层是同步非阻塞（Reactor），但生产者/消费者 API 提供异步回调（业务层）。  
3. MySQL 的“线程池”：  
   • 线程池优化了连接管理，但存储引擎（如 InnoDB）的刷盘操作依赖后台线程。

6. 为什么选择 Reactor 模式？
• 高并发：通过 I/O 多路复用减少线程资源消耗。  
• 低延迟：避免线程切换开销（如 Redis 单线程设计）。  
• 可扩展性：轻松支持数千/万级连接（如 Kafka 的 Reactor 线程组）。

7. 扩展阅读
• Redis 源码：ae.c（事件循环）、networking.c（请求处理）。  
• Kafka 设计文档：https://kafka.apache.org/documentation/#design 中的网络模型部分。  
• MySQL 线程池插件：thread_pool.cc（MariaDB 的实现参考）。  

通过分析可见，这三者均以 Reactor 模式为核心，但根据场景差异在线程模型上做了不同优化。

以下是 单线程 Reactor 与 多线程 Reactor 的详细对比，从设计原理、性能特点到适用场景的全面分析：

### 1. 核心联系
• 共同基础：  
  两者均基于 Reactor 模式，核心组件一致：  
  • 事件多路复用器（`epoll`/`kqueue`/`select`）监听I/O事件。  
  • 事件分发器：将就绪事件分发给对应的处理器。  
  • 事件处理器（`Handler`）：实现业务逻辑。  


• 核心目标：  

  通过 非阻塞I/O + 事件驱动 减少线程资源消耗，提升高并发能力。

### 2. 关键区别

| 维度         | 单线程 Reactor                          | 多线程 Reactor                          |
|------------------|---------------------------------------------|---------------------------------------------|
| 线程模型      | 所有操作（I/O + 业务）在单线程完成          | I/O 在 Reactor 线程处理，业务交给线程池     |
| 性能瓶颈      | 受限于单核CPU，耗时任务阻塞事件循环         | 可充分利用多核，避免业务阻塞I/O             |
| 复杂度        | 低（无锁、无线程同步）                      | 高（需处理线程安全、任务队列竞争）          |
| 典型应用      | Redis、早期Node.js                          | Netty、Kafka、Nginx（多进程+多线程）        |
| 资源消耗      | 线程少（1个），内存占用低                   | 线程多（Reactor池+工作线程池），占用更高     |
| 延迟稳定性    | 高（无线程切换）                            | 可能因线程竞争波动                          |

---

### 3. 线程模型图解
#### (1) 单线程 Reactor
```plaintext
┌───────────────────────────────────┐
│            Reactor 线程            │
│ ┌─────────┐    ┌───────────────┐  │
│ │ I/O 多路 │    │   事件处理器   │  │
│ │ 复用器   │───▶│  (业务逻辑)    │  │
│ └─────────┘    └───────────────┘  │
└───────────────────────────────────┘
```
• 所有操作（Accept/Read/Decode/Process/Encode/Write）均在单线程完成。


#### (2) 多线程 Reactor
```plaintext
┌─────────────────┐    ┌───────────────────┐
│  主Reactor线程   │    │    子Reactor线程池  │
│  (仅处理连接)    │───▶│ (处理I/O读写事件)   │
└─────────────────┘    └──────────┬─────────┘
                                   │
                          ┌────────▼────────┐
                          │   业务线程池     │
                          │ (处理耗时任务)   │
                          └─────────────────┘
```
• 分工明确：  
  • 主Reactor：处理新连接（`accept`）。  
  • 子Reactor：处理已连接Socket的I/O（`read/write`）。  
  • 线程池：执行数据库查询、复杂计算等耗时任务。


### 4. 性能对比场景
#### 案例：处理10K并发连接
| 指标         | 单线程 Reactor              | 多线程 Reactor              |
|------------------|---------------------------------|---------------------------------|
| CPU利用率     | 单核100%，其他核心闲置          | 多核均衡负载                    |
| 吞吐量        | 低（若业务耗时）                | 高（并行处理）                  |
| 平均延迟      | 稳定（无线程切换）              | 可能因线程竞争波动              |
| 适用业务      | 轻量级操作（如Redis KV读写）    | 重量级操作（如HTTP请求解析）    |

### 5. 选择建议
#### 用单线程 Reactor 当：
• 业务逻辑简单且耗时极短（如缓存服务）。  
• 需要极致低延迟（如金融交易系统）。  
• 资源受限（嵌入式设备）。  


#### 用多线程 Reactor 当：
• 业务包含阻塞操作（如数据库访问）。  
• 需充分利用多核CPU（如Web服务器）。  
• 高吞吐量优先（如消息队列）。  



### 6. 混合模式实践
#### Netty 的主从 Reactor 模型
```java
EventLoopGroup bossGroup = new NioEventLoopGroup(1);  // 单线程主Reactor
EventLoopGroup workerGroup = new NioEventLoopGroup(); // 多线程子Reactor
ServerBootstrap b = new ServerBootstrap();
b.group(bossGroup, workerGroup)  // 明确分工
 .channel(NioServerSocketChannel.class);
```
• 优势：  
  • 主Reactor单线程避免连接竞争。  
  • 子Reactor多线程并行处理I/O。  
  • 业务线程池隔离阻塞任务。


### 7. 常见误区
1. “多线程一定比单线程快”：  
   • 若业务无阻塞，单线程可能更快（无锁、无切换开销）。  
2. “Reactor必须用多线程”：  
   • Redis用单线程Reactor仍支持百万QPS，因KV操作是内存级快速。  
3. “线程数越多越好”：  
   • 过多线程导致竞争，通常子Reactor线程数设为CPU核心数。

### 8. 扩展思考
• 协程替代线程：  
  Go语言的`goroutine`或Java虚拟线程（Project Loom）可简化多线程Reactor的复杂性。  
• 硬件影响：  

  NVMe SSD的普及使得磁盘I/O不再绝对阻塞，单线程Reactor适用性更广。  

通过理解两者差异，可针对场景选择最优架构。
