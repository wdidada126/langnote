# Java编程方法论 响应式Spring_Reactor3设计与实现

https://book.douban.com/subject/35217472/

ISBN: 9787121394768
出版年: 2020-9

《Java编程方法论：响应式Spring Reactor 3设计与实现》主要专注于解读Spring Reactor 3的代码设计与实现。全书共10章，其中第1、2章将从接口的设计入手，逐渐深入介绍Reactor中Flux源与订阅者Subscriber的诸多交互实现细节；第3章将通过对调度器的研究来向读者展示其中的优秀设计，可以帮助读者更好地掌握Java并发库，同时可以使读者对使用Reactor进行异步编程有更好的认识；第4章将接触到一些常用的Reactor操作，方便读者写出可重用度高、逻辑清晰的代码；第5、6、7章将着重分析Reactor中Processor的设计实现，不仅讲述了它的使用场景，还讲解了其中的内在原理，以及如何应对未来项目开发过程中可能遇到的种种问题；第8章将介绍并分析Reactor特别提供的Context，这是Reactor为了应对生产-订阅模式下的响应式编程在异步环境中对订阅关系上下文进行管理所产生的问题而给出的解决方案，Spring Framework 5.2中的响应式事务也是基于它实现的；第9章将主要介绍Reactor中的测试，同时带着读者一步一步设计实现一个针对Reactor项目的测试库；第10章将主要介绍Reactor中的调试，可以教会读者根据不同的需求采取不同的调试方式。

本书适合有Java编程基础的中高级Java开发工程师、想要学习代码设计思路与技巧的读者、对响应式编程感兴趣的读者阅读。

知秋
本名李飞飞，simviso团队创始人，曾长期致力于基础代码库研发工作，对JDK、Spring、RxJava、SpringReactor、Netty、Reactor-Netty、RSocket等有深刻的研究和独到的见解，并以此打造“Java编程方法论系列丛书”。一直通过博客与视频平台bilibili（B站），结合自己的经验进行大量源码解读分享。现在主要致力于带领simviso的小伙伴引进、翻译国外知名高校计算机科学相关课程及国外知名Java开发者的技术分享内容。

第1章 响应式编程概述 1
1.1 并发与并行的关系 1
1.2 如何理解响应式编程中的背压 2
1.3 源码接口设计启示 3
1.4 如何看待众多函数表达式 11
1.5 Reactor与RxJava的对比 12
1.6 小结 14
第2章 对Flux的探索 15
2.1 对Flux.subscribe订阅逻辑的解读 16
2.1.1 对CoreSubscriber的解读 17
2.1.2 对LambdaSubscriber的解读 22
2.1.3 AtomicXxxFieldUpdater的技法应用 24
2.2 用Flux.create创建源 30
2.2.1 FluxCreate细节探索 31
2.2.2 Flux的快速包装方法 36
2.2.3 Reactor 3中的generate方法 38
2.3 蛇行走位的QueueSubscription 43
2.3.1 无界队列SpscLinkedArrayQueue 44
2.3.2 QueueSubscription.requestFusion的催化效应 47
2.4 Mono的二三事 50
2.5 通过BaseSubscriber自定义订阅者 51
2.6 将常见的监听器改造成响应式结构 53
2.7 Flux.push的特殊使用场景及细节探索 56
2.8 对Flux.handle的解读 58
2.9 小结 63
第3章 调度器 64
3.1 深入理解Schedulers.elastic 65
3.1.1 CachedScheduler的启示 66
3.1.2 ElasticScheduler的类定义思路 68
3.1.3 对Schedulers.decorateExecutorService的解读 69
3.1.4 对ElasticScheduler.schedule的解读 70
3.1.5 对ElasticScheduler.DirectScheduleTask的解读 71
3.1.6 对Schedulers.directSchedule的解读 73
3.1.7 对ElasticScheduler.ElasticWorker的解读 74
3.1.8 ElasticScheduler小结 82
3.2 深入解读publishOn 82
3.2.1 publishOn流程概述 82
3.2.2 对FluxPublishOn的解读 85
3.3 深入解读subscribeOn 98
3.4 Flux.parallel&Flowable.parallel的并行玩法 108
3.5 ParallelFlux.runOn&ParallelFlowable.runOn的调度实现 117
3.6 小结 122
第4章 对Reactor操作的解读 123
4.1 filter操作 123
4.2 transform操作 124
4.3 compose与transformDeferred操作 127
4.4 批处理操作 129
4.4.1 buffer操作 130
4.4.2 window 操作 132
4.4.3 groupBy 操作 139
4.5 merge和mergeSequential操作 140
4.6 flatMap和flatMapSequential操作 142
4.7 concatMap操作 144
4.8 combineLatest操作 145
4.9 ConnectableFlux的二三事及对reactor-bug的分析 146
4.10 小结 158
第5章 对Processor的探索 159
5.1 UnicastProcessor详解 160
5.2 DirectProcessor详解 164
5.3 EmitterProcessor详解 169
5.4 ReplayProcessor详解 174
5.5 小结 188
第6章 TopicProcessor及Reactor中匹配Disruptor的实现代码 189
6.1 初识TopicProcessor 190
6.2 TopicProcessor构造器 195
6.3 对RingBuffer中publish方法的解读 205
6.4 对MultiProducerRingBuffer的解读 208
6.4.1 RingBuffer中的UnsafeSupport 210
6.4.2 RingBuffer中的next与publish操作 216
6.5 TopicProcessor.onSubscribe及类BossEventLoopGroup的设计 221
6.6 TopicProcessor.subscribe及类WorkerEventLoopGroup的设计 225
6.7 小结 241
第7章 对WorkQueueProcessor的解读 242
7.1 WorkQueueProcessor的requestTask 244
7.2 WorkQueueProcessor的subscribe 247
7.3 冷热数据源的区别 251
7.4 实例详解 252
7.5 小结 255
第8章 Reactor中特供的Context 256
8.1 Context的设计缘由 256
8.2 对Context的解读 258
8.3 小结 265
第9章 Reactor中的测试 267
9.1 StepVerifier测试源码解析 267
9.1.1 接口定义 267
9.1.2 接口实现 269
9.1.3 验证 274
9.2 StepVerifier测试应用 275
9.3 操作时间测试 278
9.4 使用StepVerifier进行后置验证 286
9.5 关于Context的测试 289
9.6 使用TestPublisher对自定义中间操作进行测试 296
9.7 使用PublisherProbe检查执行路径 305
9.8 小结 310
第10章 Reactor中的调试 311
10.1 启用调试模式 311
10.2 在调试模式下读取堆栈跟踪信息 315
10.3 通过checkpoint方式进行调试 325
10.4 记录订阅关系下与操作流程相关的日志 326
10.5 小结 326

## 笔记
## 第1章 响应式编程概述 1
1.1 并发与并行的关系 1
1.2 如何理解响应式编程中的背压 2
1.3 源码接口设计启示 3
1.4 如何看待众多函数表达式 11
1.5 Reactor与RxJava的对比 12
1.6 小结 14
## 第2章 对Flux的探索 15
2.1 对Flux.subscribe订阅逻辑的解读 16
2.1.1 对CoreSubscriber的解读 17
2.1.2 对LambdaSubscriber的解读 22
2.1.3 AtomicXxxFieldUpdater的技法应用 24
2.2 用Flux.create创建源 30
2.2.1 FluxCreate细节探索 31
2.2.2 Flux的快速包装方法 36
2.2.3 Reactor 3中的generate方法 38
2.3 蛇行走位的QueueSubscription 43
2.3.1 无界队列SpscLinkedArrayQueue 44
2.3.2 QueueSubscription.requestFusion的催化效应 47
2.4 Mono的二三事 50
2.5 通过BaseSubscriber自定义订阅者 51
2.6 将常见的监听器改造成响应式结构 53
2.7 Flux.push的特殊使用场景及细节探索 56
2.8 对Flux.handle的解读 58
2.9 小结 63
## 第3章 调度器 64
3.1 深入理解Schedulers.elastic 65
3.1.1 CachedScheduler的启示 66
3.1.2 ElasticScheduler的类定义思路 68
3.1.3 对Schedulers.decorateExecutorService的解读 69
3.1.4 对ElasticScheduler.schedule的解读 70
3.1.5 对ElasticScheduler.DirectScheduleTask的解读 71
3.1.6 对Schedulers.directSchedule的解读 73
3.1.7 对ElasticScheduler.ElasticWorker的解读 74
3.1.8 ElasticScheduler小结 82
3.2 深入解读publishOn 82
3.2.1 publishOn流程概述 82
3.2.2 对FluxPublishOn的解读 85
3.3 深入解读subscribeOn 98
3.4 Flux.parallel&Flowable.parallel的并行玩法 108
3.5 ParallelFlux.runOn&ParallelFlowable.runOn的调度实现 117
3.6 小结 122
## 第4章 对Reactor操作的解读 123
4.1 filter操作 123
4.2 transform操作 124
4.3 compose与transformDeferred操作 127
4.4 批处理操作 129
4.4.1 buffer操作 130
4.4.2 window 操作 132
4.4.3 groupBy 操作 139
4.5 merge和mergeSequential操作 140
4.6 flatMap和flatMapSequential操作 142
4.7 concatMap操作 144
4.8 combineLatest操作 145
4.9 ConnectableFlux的二三事及对reactor-bug的分析 146
4.10 小结 158
## 第5章 对Processor的探索 159
5.1 UnicastProcessor详解 160
5.2 DirectProcessor详解 164
5.3 EmitterProcessor详解 169
5.4 ReplayProcessor详解 174
5.5 小结 188
## 第6章 TopicProcessor及Reactor中匹配Disruptor的实现代码 189
6.1 初识TopicProcessor 190
6.2 TopicProcessor构造器 195
6.3 对RingBuffer中publish方法的解读 205
6.4 对MultiProducerRingBuffer的解读 208
6.4.1 RingBuffer中的UnsafeSupport 210
6.4.2 RingBuffer中的next与publish操作 216
6.5 TopicProcessor.onSubscribe及类BossEventLoopGroup的设计 221
6.6 TopicProcessor.subscribe及类WorkerEventLoopGroup的设计 225
6.7 小结 241
## 第7章 对WorkQueueProcessor的解读 242
7.1 WorkQueueProcessor的requestTask 244
7.2 WorkQueueProcessor的subscribe 247
7.3 冷热数据源的区别 251
7.4 实例详解 252
7.5 小结 255
## 第8章 Reactor中特供的Context 256
8.1 Context的设计缘由 256
8.2 对Context的解读 258
8.3 小结 265
## 第9章 Reactor中的测试 267
9.1 StepVerifier测试源码解析 267
9.1.1 接口定义 267
9.1.2 接口实现 269
9.1.3 验证 274
9.2 StepVerifier测试应用 275
9.3 操作时间测试 278
9.4 使用StepVerifier进行后置验证 286
9.5 关于Context的测试 289
9.6 使用TestPublisher对自定义中间操作进行测试 296
9.7 使用PublisherProbe检查执行路径 305
9.8 小结 310
## 第10章 Reactor中的调试 311
10.1 启用调试模式 311
10.2 在调试模式下读取堆栈跟踪信息 315
10.3 通过checkpoint方式进行调试 325
10.4 记录订阅关系下与操作流程相关的日志 326
10.5 小结 326
## 跨年摘录（2020–2026 日常笔记聚合，2026-09-23 整理）

### 2025-07
> - 《JavaScript 高级程序设计》（俗称“红宝书”）

