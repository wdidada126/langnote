# reactor


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