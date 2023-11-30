# brpc


cmake -B build && cmake --build build -j6


git checkout 0.9.7

https://github.com/apache/incubator-brpc/blob/master/docs/cn/getting_started.md

brpc交流QQ群，committer在
498837325

0.9.5

https://blog.csdn.net/wxj1992/article/details/95249044#comments


[Linux下内存检测工具：asan](http://www.cppblog.com/markqian86/archive/2018/06/14/215728.html)


open-falcon

brpc-open-falcon github

brpc的监控方案
http

你可以使用它：

搭建能在一个端口支持多协议的服务, 或访问各种服务
restful http/https, h2/h2c (与grpc兼容, 即将开源). 使用brpc的http实现比libcurl方便多了。
redis和memcached, 线程安全，比官方client更方便。
rtmp/flv/hls, 可用于搭建直播服务.
hadoop_rpc(可能开源)
支持rdma(即将开源)
各种百度内使用的协议: baidu_std, streaming_rpc, hulu_pbrpc, sofa_pbrpc, nova_pbrpc, public_pbrpc, ubrpc和使用nshead的各种协议.
从其他语言通过HTTP+json访问基于protobuf的协议.
基于工业级的RAFT算法实现搭建高可用分布式系统，已在braft开源。
Server能同步或异步处理请求。
Client支持同步、异步、半同步，或使用组合channels简化复杂的分库或并发访问。
通过http界面调试服务, 使用cpu, heap, contention profilers.
获得更好的延时和吞吐.
把你组织中使用的协议快速地加入brpc，或定制各类组件, 包括名字服务 (dns, zk, etcd), 负载均衡 (rr, random, consistent hashing)

在用redis的时候，发现每隔20s就有一次“刺探”redis：连接redis然后马上释放连接。这有时候会导致超时。
不知道这在框架里哪里可以调整？

目前正在使用 brpc，brpc 在一些地方确实给人了一些小惊喜，比如内置的调试页面等等一些小工具确实都不错，方便了开发。但是作为一个 rpc 框架最重要的应该是能够和已有的系统结合以及良好的扩展性，brpc 在这个方面做的就很差，比如缺少多语言支持，没有 Middleware 之类的功能，内置的 bvar 监控没办法和 Prometheus 结合（ bvar 支持导出 Prometheus 格式的数据但是没有 label 支持，基本不可用），rpc 框架应该是个架子，而不是一个已经装满的架子

[核心组件bvar ](https://blog.csdn.net/wxj1992/article/details/105134641/)

bvar是Brpc使用的多线程环境下的计数器类库，作为一个完善的rpc框架，在实际生产环境中统计诸如qps、连接数等各种数值是必须的，也是服务监控的很重要的一部分，但在多线程环境下，计数器被多线程访问，容易出现cache bouncing影响性能，bvar最核心的思想就是利用thread local变量来减少cache bouncing，本质上是将写的竞争转移到了读，但在诸如监控这种场景下，通常读是远远小于写的，因此这种转移的正向效果是显著的。
bvar的官方文档对于bvar的使用介绍已经很详细，我这边打算接下来用几篇文章从源码层面入手介绍这个优秀的数值统计类库，学习下优秀的设计思想。本篇主要会根据源码先整体分析bvar的组织和实现方式，后续将会深入各个类的实现。

以前一直用 grpc，最近重新看了一下百度的 brpc，对比了一下优缺点。
brpc 优点，支持 status,lb,bvar,sessionlocal，threadlocal,logging,redis,http 等。 感觉这些是一个工程应用必须有的，比如状态监控，负载均衡，日志，常用的传输协议支持。

brpc 缺点，上手难度大，文档写的二流，很多功能要边猜边验证，支持的语言就要是 c++。
grpc 优点，支持的语言非常全，文档写的非常完善。
grpc 缺点，各种传输协议不支持（ http/2，reids ）之类的    //grpc支持http2



戈君 知乎

Brpc



深入浅出java虚拟机

李国

极客时间

前陌陌、京东高级架构师。负责过京东金融调用链系统 SGM，以及数据库中间件 CDS 的开发工作；曾负责陌陌基础社交业务线的整体架构工作，对高并发下的 JVM 调优有丰富的经验。

在用redis的时候，发现每隔20s就有一次“刺探”redis：连接redis然后马上释放连接。这有时候会导致超时。
不知道这在框架里哪里可以调整？

目前正在使用 brpc，brpc 在一些地方确实给人了一些小惊喜，比如内置的调试页面等等一些小工具确实都不错，方便了开发。但是作为一个 rpc 框架最重要的应该是能够和已有的系统结合以及良好的扩展性，brpc 在这个方面做的就很差，比如缺少多语言支持，没有 Middleware 之类的功能，内置的 bvar 监控没办法和 Prometheus 结合（ bvar 支持导出 Prometheus 格式的数据但是没有 label 支持，基本不可用），rpc 框架应该是个架子，而不是一个已经装满的架子

[核心组件bvar ](https://blog.csdn.net/wxj1992/article/details/105134641/)

bvar是Brpc使用的多线程环境下的计数器类库，作为一个完善的rpc框架，在实际生产环境中统计诸如qps、连接数等各种数值是必须的，也是服务监控的很重要的一部分，但在多线程环境下，计数器被多线程访问，容易出现cache bouncing影响性能，bvar最核心的思想就是利用thread local变量来减少cache bouncing，本质上是将写的竞争转移到了读，但在诸如监控这种场景下，通常读是远远小于写的，因此这种转移的正向效果是显著的。
bvar的官方文档对于bvar的使用介绍已经很详细，我这边打算接下来用几篇文章从源码层面入手介绍这个优秀的数值统计类库，学习下优秀的设计思想。本篇主要会根据源码先整体分析bvar的组织和实现方式，后续将会深入各个类的实现。

以前一直用 grpc，最近重新看了一下百度的 brpc，对比了一下优缺点。

brpc 优点，支持 status,lb,bvar,sessionlocal，threadlocal,logging,redis,http 等。 感觉这些是一个工程应用必须有的，比如状态监控，负载均衡，日志，常用的传输协议支持。

brpc 缺点，上手难度大，文档写的二流，很多功能要边猜边验证，支持的语言就要是 c++。

grpc 优点，支持的语言非常全，文档写的非常完善。

grpc 缺点，各种传输协议不支持（ http/2，reids ）之类的    //grpc支持http2