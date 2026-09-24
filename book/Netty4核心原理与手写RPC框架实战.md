# Netty4核心原理与手写RPC框架实战

https://github.com/gupaoedu-tom/netty4-samples

https://book.douban.com/subject/35013508/

9787121385063

鼓泡学院
根本就没有手写RPC框架

Java并发编程深度解析与实战
Netty4核心原理与手写RPC框架实战 : 4核心原理与手写RPC框架实战
设计模式就该这样学：基于经典框架源码和真实业务场景
Spring5核心原理与30个类手写实战
SpringCloudAlibaba微服务原理与实战

第1篇 I/O 基础篇
第1章 网络通信原理 2
1.1 网络基础架构 2
1.1.1 C/S 架构 2
1.1.2 C/S 信息传输流程 2
1.2 TCP/IP 五层模型详解 3
1.2.1 物理层 3
1.2.2 数据链路层 4
1.2.3 网络层 5
1.2.4 传输层 10
1.2.5 应用层 15
1.2.6 小结 16
1.3 网络通信实现原理 18
1.4 向浏览器输入 URL 后发生了什么 19
1.5 网络通信之“魂”——Socket 21
第2章 Java I/O 演进之路 23
2.1 I/O 的问世 23
2.1.1 什么是 I/O 23
2.1.2 I/O 交互流程 24
2.2 五种 I/O 通信模型 25
2.2.1 阻塞 I/O 模型 25
2.2.2 非阻塞 I/O 模型 26
2.2.3 多路复用 I/O 模型 27
2.2.4 信号驱动 I/O 模型 28
2.2.5 异步 I/O 模型 28
2.2.6 易混淆的概念澄清 29
2.2.7 各 I/O 模型的对比与总结 32
2.3 从 BIO 到 NIO 的演进 33
2.3.1 面向流与面向缓冲 33
2.3.2 阻塞与非阻塞 33
2.3.3 选择器在 I/O 中的应用 34
2.3.4 NIO 和 BIO 如何影响应用程序的设计 34
2.4 Java AIO 详解 37
2.4.1 AIO 基本原理 37
2.4.2 AIO 初体验 38
第2篇 Netty 初体验
第3章 Netty 与 NIO 之前世今生 44
3.1 Java NIO 三件套 44
3.1.1 缓冲区 44
3.1.2 选择器 54
3.1.3 通道 58
3.2 NIO 源码初探 63
3.3 反应堆 69
3.4 Netty 与 NIO 70
3.4.1 Netty 支持的功能与特性 70
3.4.2 Netty 采用 NIO 而非 AIO 的理由 71
第4章 基于 Netty 手写 Tomcat 72
4.1 环境准备 72
4.1.1 定义 GPServlet 抽象类 72
4.1.2 创建用户业务代码 73
4.1.3 完成 web.properties 配置 74
4.2 基于传统 I/O 手写 Tomcat 74
4.2.1 创建 GPRequest 对象 74
4.2.2 创建 GPResponse 对象 76
4.2.3 创建 GPTomcat 启动类 77
4.3 基于 Netty 重构 Tomcat 实现 80
4.3.1 重构 GPTomcat 逻辑 80
4.3.2 重构 GPRequest 逻辑 83
4.3.3 重构 GPResponse 逻辑 84
4.3.4 运行效果演示 85
第5章 基于 Netty 重构 RPC 框架 87
5.1 RPC 概述 87
5.2 环境预设 88
5.3 代码实战 91
5.3.1 创建 API 模块 91
5.3.2 创建自定义协议 91
5.3.3 实现 Provider 业务逻辑 92
5.3.4 完成 Registry 服务注册 93
5.3.5 实现 Consumer 远程调用 97
5.3.6 Monitor 监控 101
5.4 运行效果演示 102
第3篇 Netty 核心篇
第6章 Netty 高性能之道 104
6.1 背景介绍 104
6.1.1 Netty 惊人的性能数据 104
6.1.2 传统 RPC 调用性能差的“三宗罪” 104
6.1.3 Netty 高性能的三个主题 105
6.2 Netty 高性能之核心法宝 106
6.2.1 异步非阻塞通信 106
6.2.2 零拷贝 108
6.2.3 内存池 112
6.2.4 高效的 Reactor 线程模型 116
6.2.5 无锁化的串行设计理念 118
6.2.6 高效的并发编程 119
6.2.7 对高性能的序列化框架的支持 119
6.2.8 灵活的 TCP 参数配置能力 120
第7章 揭开 Bootstrap 的神秘面纱 124
7.1 客户端 Bootstrap 124
7.1.1 Channel 简介 124
7.1.2 NioSocketChannel 的创建 125
7.1.3 客户端 Channel 的初始化 127
7.1.4 Unsafe 属性的初始化 130
7.1.5 ChannelPipeline 的初始化 131
7.1.6 EventLoop 的初始化 132
7.1.7 将 Channel 注册到 Selector 137
7.1.8 Handler 的添加过程 139
7.1.9 客户端发起连接请求 141
7.2 服务端 ServerBootstrap 144
7.2.1 NioServerSocketChannel 的创建 146
7.2.2 服务端 Channel 的初始化 146
7.2.3 服务端 ChannelPipeline 的初始化 149
7.2.4 将服务端 Channel 注册到 Selector 149
7.2.5 bossGroup 与 workerGroup 149
7.2.6 服务端 Selector 事件轮询 152
7.2.7 Netty 解决 JDK 空轮询 Bug 154
7.2.8 Netty 对 Selector 中 KeySet 的优化 157
7.2.9 Handler 的添加过程 160
第8章 大名鼎鼎的 EventLoop 164
8.1 EventLoopGroup 与 Reactor 164
8.1.1 再谈 Reactor 线程模型 164
8.1.2 EventLoopGroup 与 Reactor 关联 166
8.1.3 EventLoopGroup 的实例化 167
8.2 任务执行者 EventLoop 169
8.2.1 NioEventLoop 的实例化过程 170
8.2.2 EventLoop 与 Channel 的关联 171
8.2.3 EventLoop 的启动 172
第9章 Netty 大动脉 Pipeline 176
9.1 Pipeline 设计原理 176
9.1.1 Channel 与 ChannelPipeline 176
9.1.2 再谈 ChannelPipeline 的初始化 177
9.1.3 ChannelInitializer 的添加 178
9.1.4 自定义 ChannelHandler 的添加过程 181
9.1.5 给 ChannelHandler 命名 184
9.1.6 ChannelHandler 的默认命名规则 185
9.2 Pipeline 的事件传播机制 186
9.2.1 Outbound 事件传播方式 194
9.2.2 Inbound 事件传播方式 196
9.2.3 小结 199
9.3 Handler 的各种“姿势” 200
9.3.1 ChannelHandlerContext 200
9.3.2 Channel 的生命周期 201
9.3.3 ChannelHandler 常用的 API 201
9.3.4 ChannelInboundHandler 202
第10章 异步处理双子星 Future 与 Promise 204
10.1 异步结果 Future 204
10.2 异步执行 Promise 205
第11章 Netty 内存分配 ByteBuf 209
11.1 初识 ByteBuf 209
11.1.1 ByteBuf 的基本结构 209
11.1.2 ByteBuf 的重要 API 210
11.1.3 ByteBuf 的基本分类 213
11.2 ByteBufAllocator 内存管理器 214
11.3 非池化内存分配 218
11.3.1 堆内内存的分配 218
11.3.2 堆外内存的分配 221
11.4 池化内存分配 224
11.4.1 PooledByteBufAllocator 简述 224
11.4.2 DirectArena 内存分配流程 229
11.4.3 内存池的内存规格 231
11.4.4 命中缓存的分配 231
11.4.5 Page 级别的内存分配 241
11.4.6 SubPage 级别的内存分配 254
11.4.7 内存池 ByteBuf 的内存回收 268
11.4.8 SocketChannel 读取 ByteBuf 的过程 273
第12章 Netty 编解码的艺术 281
12.1 什么是拆包、粘包 281
12.1.1 TCP 拆包、粘包 281
12.1.2 粘包问题的解决策略 282
12.2 什么是编解码 282
12.2.1 编解码技术 282
12.2.2 Netty 为什么要提供编解码框架 283
12.3 Netty 中常用的解码器 284
12.3.1 ByteToMessageDecoder 抽象解码器 284
12.3.2 LineBasedFrameDecoder 行解码器 289
12.3.3 DelimiterBasedFrameDecoder 分隔符解码器 296
12.3.4 FixedLengthFrameDecoder 固定长度解码器 302
12.3.5 LengthFieldBasedFrameDecoder 通用解码器 303
12.4 Netty 编码器原理和数据输出 307
12.4.1 WriteAndFlush 事件传播 307
12.4.2 MessageToByteEncoder 抽象编码器 311
12.4.3 写入 Buffer 队列 312
12.4.4 刷新 Buffer 队列 316
12.4.5 数据输出回调 322
12.5 自定义编解码 335
12.5.1 MessageToMessageDecoder 抽象解码器 335
12.5.2 MessageToMessageEncoder 抽象编码器 336
12.5.3 ObjectEncoder 序列化编码器 337
12.5.4 LengthFieldPrepender 通用编码器 338
第4篇 Netty 实战篇
第13章 基于 Netty 手写消息推送系统 342
13.1 环境搭建 342
13.2 多协议通信设计 343
13.2.1 自定义协议规则 343
13.2.2 自定义编解码器 346
13.2.3 对 HTTP 的支持 349
13.2.4 对自定义协议的支持 351
13.2.5 对 WebSocket 协议的支持 351
13.3 服务端逻辑处理 352
13.3.1 多协议串行处理 352
13.3.2 服务端用户中心 354
13.4 客户端控制台处理 359
13.4.1 控制台接入代码 359
13.4.2 控制台消息处理 360
13.5 客户端 Web 页面交互实现 363
13.5.1 Web 页面设计 363
13.5.2 WebSocket 接入 365
13.5.3 登录和退出 366
13.5.4 发送文字信息 367
13.5.5 发送图片表情 368
13.5.6 发送鲜花雨特效 369
第14章 Netty 高性能调优工具类解析 371
14.1 多线程共享 FastThreadLocal 371
14.1.1 FastThreadLocal 的使用和创建 371
14.1.2 FastThreadLocal 的设值 379
14.2 Recycler 对象回收站 381
14.2.1 Recycler 的使用和创建 381
14.2.2 从 Recycler 中获取对象 386
14.2.3 相同线程内的对象回收 389
14.2.4 不同线程间的对象回收 391
14.2.5 获取不同线程间释放的对象 397
第15章 单机百万连接性能调优 405
15.1 模拟 Netty 单机连接瓶颈 405
15.2 单机百万连接调优解决思路 410
15.2.1 突破局部文件句柄限制 410
15.2.2 突破全局文件句柄限制 412
15.3 Netty 应用级别的性能调优 413
15.3.1 Netty 应用级别的性能瓶颈复现 413
15.3.2 Netty 应用级别的性能调优方案 420
第16章 设计模式在 Netty 中的应用 422
16.1 单例模式源码举例 422
16.2 策略模式源码举例 423
16.3 装饰者模式源码举例 424
16.4 观察者模式源码举例 426
16.5 迭代器模式源码举例 427
16.6 责任链模式源码举例 428
16.7 工厂模式源码举例 430
第17章 Netty 经典面试题集锦 432
17.1 基础知识部分 432
17.1.1 TCP 和 UDP 的根本区别 432
17.1.2 TCP 如何保证可靠传输 433
17.1.3 Netty 能解决什么问题 433
17.1.4 选用 Netty 作为通信组件框架的举例 433
17.1.5 Netty 有哪些主要组件，它们之间有什么关联 433
17.2 高级特性部分 434
17.2.1 相较同类框架，Netty 有哪些优势 434
17.2.2 Netty 的高性能体现在哪些方面 434
17.2.3 默认情况下 Netty 起多少线程，何时启动 434
17.2.4 Netty 有几种发送消息的方式 434
17.2.5 Netty 支持哪些心跳类型设置 435
17.2.6 Netty 和 Tomcat 的区别 435
17.2.7 在实际应用中，如何确定要使用哪些编解码器 435
## 跨年摘录（2020–2026 日常笔记聚合，2026-09-23 整理）

### 2023-04
> 《netty4核心原理与手写RPC框架》

