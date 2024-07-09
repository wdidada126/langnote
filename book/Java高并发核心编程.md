# Java高并发核心编程

https://book.douban.com/subject/35446284/  卷1
https://book.douban.com/subject/35446285/ 卷2

微信读书

尼恩

Windows电脑上有

Netty Reactor
nginx
redis都是

https://gitee.com/edidada/Java-high-concurrency-core-Programming-Volume-2-source-code


前言
自序
第1章 高并发时代的必备技能 1
1.1 Netty为何这么火 1
1.1.1 Netty火热的程度 1
1.1.2 Netty是面试的必杀器 2
1.2 高并发利器Redis 2
1.2.1 什么是Redis 2
1.2.2 Redis成为缓存事实标准的原因 3
1.3 分布式利器ZooKeeper 3
1.3.1 什么是ZooKeeper 3
1.3.2 ZooKeeper的优势 4
1.4 高性能HTTP通信技术 4
1.4.1 十万级以上高并发场景中的高并发HTTP通信技术 5
1.4.2 微服务之间的高并发RPC技术 6
1.5 高并发IM的综合实战 7
1.5.1 高并发IM的学习价值 8
1.5.2 庞大的应用场景 8
第2章 高并发IO的底层原理 10
2.1 IO读写的基本原理 10
2.1.1 内核缓冲区与进程缓冲区 11
2.1.2 典型的系统调用流程 11
2.2 四种主要的IO模型 13
2.2.1 同步阻塞IO 14
2.2.2 同步非阻塞IO 15
2.2.3 IO多路复用 16
2.2.4 异步IO 17
2.3 通过合理配置来支持百万级并发连接 18
第3章 Java NIO核心详解 21
3.1 Java NIO简介 21
3.1.1 NIO和OIO的对比 21
3.1.2 通道 22
3.1.3 选择器 22
3.1.4 缓冲区 23
3.2 详解NIO Buffer类及其属性 23
3.2.1 Buffer类 23
3.2.2 Buffer类的重要属性 23
3.3 详解NIO Buffer类的重要方法 26
3.3.1 allocate() 26
3.3.2 put() 27
3.3.3 flip() 27
3.3.4 get() 29
3.3.5 rewind() 30
3.3.6 mark()和reset() 32
3.3.7 clear() 33
3.3.8 使用Buffer类的基本步骤 34
3.4 详解NIO Channel类 34
3.4.1 FileChannel 35
3.4.2 使用FileChannel完成文件复制的实战案例 37
3.4.3 SocketChannel 39
3.4.4 使用SocketChannel发送文件的实战案例 41
3.4.5 DatagramChannel 43
3.4.6 使用DatagramChannel发送数据的实战案例 45
3.5 详解NIO Selector 47
3.5.1 选择器与注册 47
3.5.2 SelectableChannel 48
3.5.3 SelectionKey 48
3.5.4 选择器使用流程 48
3.5.5 使用NIO实现Discard服务器的实战案例 50
3.5.6 使用SocketChannel在服务端接收文件的实战案例 53
第4章 鼎鼎大名的Reactor模式 59
4.1 Reactor模式的重要性 59
4.1.1 为什么首先学习Reactor模式 59
4.1.2 Reactor模式简介 60
4.1.3 多线程OIO的致命缺陷 60
4.2 单线程Reactor模式 62
4.2.1 什么是单线程Reactor 62
4.2.2 单线程Reactor的参考代码 63
4.2.3 单线程Reactor模式的EchoServer的实战案例 66
4.2.4 单线程Reactor模式的缺点 69
4.3 多线程Reactor模式 69
4.3.1 多线程版本的Reactor模式演进 69
4.3.2 多线程版本Reactor的实战案例 69
4.3.3 多线程版本Handler的实战案例 72
4.4 Reactor模式的优缺点 74
第5章 Netty核心原理与基础实战 76
5.1 第一个Netty实战案例DiscardServer 76
5.1.1 创建第一个Netty项目 76
5.1.2 第一个Netty服务端程序 77
5.1.3 业务处理器NettyDiscardHandler 79
5.1.4 运行NettyDiscardServer 80
5.2 解密Netty中的Reactor模式 80
5.2.1 回顾Reactor模式中IO事件的处理流程 81
5.2.2 Netty中的Channel 81
5.2.3 Netty中的Reactor 82
5.2.4 Netty中的Handler 83
5.2.5 Netty中的Pipeline 84
5.3 详解Bootstrap 86
5.3.1 父子通道 86
5.3.2 EventLoopGroup 87
5.3.3 Bootstrap启动流程 88
5.3.4 ChannelOption 91
5.4 详解Channel 93
5.4.1 Channel的主要成员和方法 93
5.4.2 EmbeddedChannel 94
5.5 详解Handler 95
5.5.1 ChannelInboundHandler入站处理器 96
5.5.2 ChannelOutboundHandler出站处理器 97
5.5.3 ChannelInitializer通道初始化处理器 99
5.5.4 ChannelInboundHandler的生命周期的实战案例 99
5.6 详解Pipeline 103
5.6.1 Pipeline入站处理流程 103
5.6.2 Pipeline出站处理流程 104
5.6.3 ChannelHandlerContext 106
5.6.4 HeadContext与TailContext 107
5.6.5 Pipeline入站和出站的双向链接操作 109
5.6.6 截断流水线的入站处理传播过程 112
5.6.7 在流水线上热插拔Handler 114
5.7 详解ByteBuf 117
5.7.1 ByteBuf的优势 117
5.7.2 ByteBuf的组成部分 117
5.7.3 ByteBuf的重要属性 118
5.7.4 ByteBuf的方法 118
5.7.5 ByteBuf基本使用的实战案例 120
5.7.6 ByteBuf的引用计数 122
5.7.7 ByteBuf的分配器 124
5.7.8 ByteBuf缓冲区的类型 126
5.7.9 两类ByteBuf使用的实战案例 127
5.7.10 ByteBuf的自动创建与自动释放 130
5.7.11 ByteBuf浅层复制的高级使用方式 136
5.8 Netty的零拷贝 138
5.8.1 通过CompositeByteBuf实现零拷贝 139
5.8.2 通过wrap操作实现零拷贝 141
5.9 EchoServer的实战案例 142
5.9.1 NettyEchoServer 142
5.9.2 NettyEchoServerHandler 143
5.9.3 NettyEchoClient 144
5.9.4 NettyEchoClientHandler 146
第6章 Decoder与Encoder核心组件 148
6.1 Decoder原理与实战 148
6.1.1 ByteToMessageDecoder解码器处理流程 148
6.1.2 自定义Byte2IntegerDecoder整数解码器 149
6.1.3 ReplayingDecoder解码器 152
6.1.4 整数的分包解码器的实战案例 153
6.1.5 字符串的分包解码器的实战案例 156
6.1.6 MessageToMessageDecoder解码器 161
6.2 常用的内置Decoder 161
6.2.1 LineBasedFrameDecoder解码器 162
6.2.2 DelimiterBasedFrameDecoder解码器 163
6.2.3 LengthFieldBasedFrameDecoder解码器 164
6.2.4 多字段Head-Content协议数据包解析的实战案例 167
6.3 Encoder原理与实战 170
6.3.1 MessageToByteEncoder编码器 170
6.3.2 MessageToMessageEncoder编码器 171
6.4 解码器和编码器的结合 173
6.4.1 ByteToMessageCodec编解码器 173
6.4.2 CombinedChannelDuplexHandler组合器 174
第7章 序列化与反序列化：JSON和Protobuf 176
7.1 详解粘包和拆包 177
7.1.1 半包问题的实战案例 177
7.1.2 什么是半包问题 179
7.1.3 半包问题的根因分析 179
7.2 使用JSON协议通信 180
7.2.1 JSON的核心优势 180
7.2.2 JSON序列化与反序列化开源库 181
7.2.3 JSON序列化与反序列化的实战案例 182
7.2.4 JSON传输的编码器和解码器 184
7.2.5 JSON传输的服务端的实战案例 185
7.2.6 JSON传输的客户端的实战案例 186
7.3 使用Protobuf协议通信 188
7.3.1 一个简单的proto文件的实战案例 188
7.3.2 通过控制台命令生成POJO和Builder 189
7.3.3 通过Maven插件生成POJO和Builder 190
7.3.4 Protobuf序列化与反序列化的实战案例 191
7.4 Protobuf编解码的实战案例 194
7.4.1 Netty内置的Protobuf基础编码器/解码器 194
7.4.2 Protobuf传输的服务端的实战案例 195
7.4.3 Protobuf传输的客户端的实战案例 197
7.5 详解Protobuf协议语法 198
7.5.1 proto文件的头部声明 199
7.5.2 Protobuf的消息结构体与消息字段 200
7.5.3 Protobuf字段的数据类型 201
7.5.4 proto文件的其他语法规范 202
第8章 基于Netty单体IM系统的开发实战 204
8.1 自定义Protobuf编解码器 204
8.1.1 自定义Protobuf编码器 205
8.1.2 自定义Protobuf解码器 206
8.1.3 IM系统中Protobuf消息格式的设计 207
8.2 IM的登录流程 209
8.2.1 图解登录/响应流程的环节 209
8.2.2 客户端涉及的主要模块 210
8.2.3 服务端涉及的主要模块 210
8.3 客户端的登录处理的实战案例 211
8.3.1 LoginConsoleCommand和User POJO 212
8.3.2 LoginSender 213
8.3.3 ClientSession 216
8.3.4 LoginResponseHandler 218
8.3.5 客户端流水线的装配 219
8.4 服务端的登录响应的实战案例 220
8.4.1 服务端流水线的装配 220
8.4.2 LoginRequestHandler 221
8.4.3 LoginProcesser 223
8.4.4 EventLoop线程和业务线程相互隔离 224
8.5 详解Session服务器会话 227
8.5.1 通道的容器属性 227
8.5.2 ServerSession服务端会话类 229
8.5.3 SessionMap会话管理器 230
8.6 点对点单聊的实战案例 230
8.6.1 单聊的端到端流程 231
8.6.2 客户端的ChatConsoleCommand收集聊天内容 231
8.6.3 客户端的CommandController发送POJO 232
8.6.4 服务端的ChatRedirectHandler进行消息转发 233
8.6.5 服务端的ChatRedirectProcesser进行异步消息转发 234
8.6.6 客户端的ChatMsgHandler聊天消息处理器 235
8.7 详解心跳检测 236
8.7.1 网络连接的假死现象 236
8.7.2 服务端的空闲检测 237
8.7.3 客户端的心跳发送 238
第9章 HTTP原理与Web服务器实战 241
9.1 高性能Web应用架构 241
9.1.1 十万级并发的Web应用架构 241
9.1.2 千万级高并发的Web应用架构 243
9.2 详解HTTP应用层协议 246
9.2.1 HTTP简介 247
9.2.2 HTTP的请求URL 248
9.2.3 HTTP的请求报文 248
9.2.4 HTTP的响应报文 251
9.2.5 HTTP中GET和POST的区别 254
9.3 HTTP的演进 254
9.3.1 HTTP的1.0版本 255
9.3.2 HTTP的1.1版本 258
9.3.3 HTTP的2.0版本 261
9.4 基于Netty实现简单的Web服务器 263
9.4.1 基于Netty的HTTP服务器演示实例 263
9.4.2 基于Netty的HTTP请求的处理流程 264
9.4.3 Netty内置的HTTP报文解码流程 266
9.4.4 基于Netty的HTTP响应编码流程 268
9.4.5 HttpEchoHandler回显业务处理器的实战案例 269
9.4.6 使用Postman发送多种类型的请求体 273
第10章 高并发HTTP通信的核心原理 278
10.1 需要进行HTTP连接复用的高并发场景 278
10.1.1 反向代理Nginx与Java Web应用服务之间的HTTP 高并发通信 278
10.1.2 微服务网关与微服务Provider实例之间的HTTP高并发通信 279
10.1.3 分布式微服务Provider实例之间的RPC的HTTP高并发通信 280
10.1.4 Java通过HTTP客户端访问REST接口服务的HTTP 高并发通信 280
10.2 详解传输层TCP 281
10.2.1 TCP/IP的分层模型 281
10.2.2 HTTP报文传输原理 283
10.2.3 TCP的报文格式 285
10.2.4 TCP的三次握手 288
10.2.5 TCP的四次挥手 290
10.2.6 三次握手、四次挥手的常见面试题 292
10.3 TCP连接状态的原理与实验 293
10.3.1 TCP/IP连接的11种状态 293
10.3.2 通过netstat指令查看连接状态 295
10.4 HTTP长连接原理 297
10.4.1 HTTP长连接和短连接 297
10.4.2 不同HTTP版本中的长连接选项 298
10.5 服务端HTTP长连接技术 299
10.5.1 应用服务器Tomcat的长连接配置 299
10.5.2 Nginx承担服务端角色时的长连接配置 302
10.5.3 服务端长连接设置的注意事项 304
10.6 客户端HTTP长连接技术原理与实验 306
10.6.1 HttpURLConnection短连接技术 306
10.6.2 HTTP短连接的通信实验 309
10.6.3 Apache HttpClient客户端的HTTP长连接技术 311
10.6.4 Apache HttpClient客户端长连接实验 319
10.6.5 Nginx承担客户端角色时的长连接技术 323
第11章 WebSocket原理与实战 326
11.1 WebSocket协议简介 326
11.1.1 Ajax短轮询和Long Poll长轮询的原理 327
11.1.2 WebSocket与HTTP之间的关系 327
11.2 WebSocket回显演示程序开发 328
11.2.1 WebSocket回显程序的客户端代码 328
11.2.2 WebSocket相关的Netty内置处理类 331
11.2.3 WebSocket的回显服务器 333
11.2.4 WebSocket的业务处理器 335
11.3 WebSocket协议通信的原理 337
11.3.1 抓取WebSocket协议的本机数据包 337
11.3.2 WebSocket 握手过程 338
11.3.3 WebSocket通信报文格式 341
第12章 SSL/TLS核心原理与实战 344
12.1 什么是SSL/TLS 344
12.1.1 SSL/TLS协议的版本演进 344
12.1.2 SSL/TLS协议的分层结构 346
12.2 加密算法原理与实战 347
12.2.1 哈希单向加密算法原理与实战 347
12.2.2 对称加密算法原理与实战 349
12.2.3 非对称加密算法原理与实战 351
12.2.4 数字签名原理与实战 356
12.3 SSL/TLS运行过程 361
12.3.1 SSL/TLS第一阶段握手 361
12.3.2 SSL/TLS第二阶段握手 363
12.3.3 SSL/TLS第三阶段握手 367
12.3.4 SSL/TLS第四阶段握手 369
12.4 详解Keytool工具 370
12.4.1 数字证书与身份识别 370
12.4.2 存储密钥与证书文件格式 373
12.4.3 使用Keytool工具管理密钥和证书 374
12.5 使用Java程序管理密钥与证书 377
12.5.1 使用Java操作数据证书所涉及的核心类 378
12.5.2 使用Java程序创建密钥与仓库 378
12.5.3 使用Java程序导出证书文件 383
12.5.4 使用Java程序将数字证书导入信任仓库 385
12.6 OIO通信中的SSL/TLS使用实战 389
12.6.1 JSSE安全套接字扩展核心类 390
12.6.2 JSSE安全套接字的创建过程 391
12.6.3 OIO安全通信的Echo服务端实战 393
12.6.4 OIO安全通信的Echo客户端实战 395
12.7 单向认证与双向认证 396
12.7.1 SSL/TLS 单向认证 396
12.7.2 使用证书信任管理器 399
12.7.3 SSL/TLS 双向认证 402
12.8 Netty通信中的SSL/TLS使用实战 405
12.8.1 Netty安全通信演示实例 405
12.8.2 Netty内置SSLEngine处理器详解 406
12.8.3 Netty的简单安全聊天器服务端程序 409
12.9 HTTPS协议安全通信实战 412
12.9.1 使用Netty实现HTTPS回显服务端程序 412
12.9.2 通过HttpsURLConnection发送HTTPS请求 414
12.9.3 HTTPS服务端与客户端的测试用例 415
第13章 ZooKeeper分布式协调 417
13.1 ZooKeeper伪集群安装和配置 417
13.1.1 创建数据目录和日志目录 417
13.1.2 创建myid文本文件 419
13.1.3 创建和修改配置文件 419
13.1.4 配置文件示例 421
13.1.5 启动ZooKeeper伪集群 422
13.2 使用ZooKeeper 进行分布式存储 423
13.2.1 详解ZooKeeper存储模型 424
13.2.2 zkCli客户端指令清单 424
13.3 ZooKeeper应用开发实战 426
13.3.1 ZkClient开源客户端 427
13.3.2 Curator开源客户端 427
13.3.3 准备Curator开发环境 428
13.3.4 创建Curator客户端实例 429
13.3.5 通过Curator创建节点 431
13.3.6 通过Curator读取节点 432
13.3.7 通过Curator更新节点 433
13.3.8 通过Curator删除节点 435
13.4 分布式命名服务实战 436
13.4.1 ID生成器 437
13.4.2 ZooKeeper分布式ID生成器的实战案例 438
13.4.3 集群节点的命名服务的实战案例 440
13.4.4 结合ZooKeeper实现SnowFlake ID算法 442
13.5 分布式事件监听的重点 447
13.5.1 Watcher标准的事件处理器 448
13.5.2 NodeCache节点缓存的监听 451
13.5.3 PathCache子节点监听 454
13.5.4 TreeCache节点树缓存 457
13.6 分布式锁原理与实战 461
13.6.1 公平锁和可重入锁的原理 461
13.6.2 ZooKeeper分布式锁的原理 463
13.6.3 分布式锁的基本流程 464
13.6.4 加锁的实现 465
13.6.5 释放锁的实现 471
13.6.6 分布式锁的使用 472
13.6.7 Curator的InterProcessMutex可重入锁 473
13.6.8 ZooKeeper分布式锁的优缺点 474
第14章 分布式缓存Redis实战 476
14.1 Redis入门 476
14.1.1 Redis的安装和配置 476
14.1.2 Redis客户端命令 479
14.1.3 Redis键的命名规范 480
14.2 Redis数据类型 481
14.2.1 String 481
14.2.2 List 482
14.2.3 Hash 484
14.2.4 Set 485
14.2.5 ZSet 486
14.3 Jedis基础编程的实战案例 487
14.3.1 Jedis操作String 488
14.3.2 Jedis操作List 490
14.3.3 Jedis操作Hash 491
14.3.4 Jedis操作Set 493
14.3.5 Jedis操作ZSet 494
14.4 JedisPool连接池的实战案例 497
14.4.1 JedisPool的配置 497
14.4.2 JedisPool的创建和预热 499
14.4.3 JedisPool的使用 501
14.5 使用spring-data-redis完成CRUD的实战案例 502
14.5.1 CRUD中应用缓存的场景 502
14.5.2 配置spring-redis.xml 504
14.5.3 RedisTemplate模板API 506
14.5.4 使用RedisTemplate模板API完成CRUD的实战案例 509
14.5.5 使用RedisCallback回调完成CRUD的实战案例 511
14.6 Spring的Redis缓存注解 513
14.6.1 使用Spring缓存注解完成CRUD的实战案例 514
14.6.2 spring-redis.xml中配置的调整 515
14.6.3 @CachePut和@Cacheable注解 517
14.6.4 @CacheEvict注解 518
14.6.5 @Caching组合注解 519
14.7 详解SpEL 520
14.7.1 SpEL运算符 521
14.7.2 缓存注解中的SpEL表达式 524
第15章 亿级高并发IM架构与实战 526
15.1 支撑亿级流量的高并发IM架构的理论基础 526
15.1.1 亿级流量的系统架构的开发实战 527
15.1.2 高并发架构的技术选型 527
15.1.3 详解IM消息的序列化协议选型 528
15.1.4 详解长连接和短连接 528
15.2 分布式IM的命名服务的实战案例 529
15.2.1 IM节点的POJO类 530
15.2.2 IM节点的ImWorker类 531
15.3 Worker集群的负载均衡的实战案例 534
15.3.1 ImLoadBalance负载均衡器 535
15.3.2 与WebGate的整合 537
15.4 即时通信消息的路由和转发的实战案例 538
15.4.1 IM路由器WorkerRouter 538
15.4.2 IM转发器PeerSender 541
15.5 在线用户统计的实战案例 543
15.5.1 Curator的分布式计数器 543
15.5.2 用户上线和下线的统计 545

## 笔记
### 第3章 CAS原理与JUC原子类

面试会问

其他语言也会用cas c++ go php？

### 第4章 可见性与有序性的原理

### 第5章 JUC显式锁的原理与实战

Semaphore

![Semaphore](..\imgs\javase\Semaphore.png)

### 第6章 AQS抽象同步器的核心原理



### 第7章 JUC容器类



### 第8章 高并发设计模式



### 第9章 高并发核心模式之异步回调模式



### 第10章 CompletableFuture异步回调

