# raft


https://www.bilibili.com/video/BV1CK4y127Lj


https://github.com/RedisLabs/redisraft


2pc
3pc
共识算法？
pax
paxos

图示

[raft论文中文翻译](https://www.infoq.cn/article/raft-paper/)



[Raft 分布式系统 一致性协议](https://blog.csdn.net/LU_ZHAO/article/details/104934220)
time out信号



 [braft]( https://github.com/baidu/braft ) 
SOFAJRaft
https://gitee.com/sofastack/sofa-jraft

https://github.com/Tencent/phxpaxos

[腾讯开源的Paxos库PhxPaxos代码解读---Prepare阶段]( https://www.cnblogs.com/lijingshanxi/p/10165802.html ) 


https://www.zhihu.com/question/266834707 
作者：我做分布式系统





作者提供了几个文档和benchmark数据，简单看了下，较忙没有看代码：

- 没有WAN高延迟环境数据，没有读的性能，没有延迟数据。实测的是log从propose到commit的性能，这不是通常的做法。文档提到类似的库粗糙不适合支持大量raft实例，但文档和benchmark中都看不到多个raft实例的实测性能或者具体设计。
- 作者提到了多组，但这库并不带调度、管理、监控修复多组raft的组件。没看代码，也不确定多组，比如数千组的时候，线程模型是怎么样。
- 22万qps的单组性能不算高，且测的方法只测到commit。损失单组为多组优化的系统，也应该能跑类似成绩。**后台服务跑分不是目的，但跑分从一个侧面体现系统从设计到实现的质量。**
- 作者认为batching是跑分的手段，是等特定的时间间隔、或等N个proposal然后合并处理，是显著的延迟换吞吐。显然，事实不是这样。请参考etcd raft的batching做法。
- 测试方法没有在文档中提到。和一般项目不同，共识库必须有近乎严酷加无聊的测试。代码中看到有内空的jepsen目录。Jepsen是系统成熟的必要非充分条件，因为它伸展不开，建议类似jepsen的测试，跑百万数量级的raft组，注入数亿规模随机异常事件，然后测linearizability。test目录有少许测试，测试的规模较小，自己的raft库测试代码就2万行，超过braft整个库大小。测试代码规模差数倍，说明问题的。
- 单语言支持，不带其它语言的binding。

在做多组raft库，近期开源。上述所有问题都有具体涵盖，非空谈。



上述提到的库已经开源，每秒千万级别的吞吐，欢迎试用，欢迎点Star





 https://github.com/sofastack/sofa-jraft 



整体源码都看过，功能完备程度很高，看这个特性列表

- Leader election.
- Replication and recovery.
- Snapshot and log compaction.      日志压缩
- Membership management.
- Fully concurrent replication.
- Fault tolerance.
- Asymmetric network partition tolerance.
- Workaround when quorate peers are dead.

并非虚言，特别是 Cli tools 这个接口和工具设计，对于运维管理是非常方便的。各个模块的分层也很清楚，存储部分都可以替换（LogStorage/MetaStorage/SnapshotStorage etc.)，灵活性很高。

测试方面，官方后来增加了 jepsen 的测试用例，覆盖了当机、配置变更、网络分区等场景，jepsen 确实是分布式测试神器。单元测试覆盖相对还是比较完善的。

关于性能，官方 [benchmark](https://link.zhihu.com/?target=https%3A//github.com/brpc/braft/blob/master/docs/cn/benchmark.md) 文档提到的关于 batch 和 pipeline 的观点，说是纯粹为了跑分过于偏激了。batch 和 pipeline 本质都是为了提高吞吐量，充分地利用 CPU 和带宽，况且 braft 内部其实也有多级的 batch：

- LogManager  的批量日志存储
- Leader Node  apply task 的批量处理
- Leader 到 follower 的日志批量发送等。
- 日志批量应用到状态机等。

> 而这时候工程师往往会沉浸在优化超时、batch size等调参工作，从而忽略了分析系统瓶颈这类真正有意义的事情



这一点理论上没有错，就像很多人解决性能问题就是加一层缓存一样，没有去分析根本性的性能瓶颈。但是，关于batch size 之类的调整，目前业界也有很多自适应的算法，例如 《[Adaptive Batching for Replicated Servers](https://link.zhihu.com/?target=https%3A//ieeexplore.ieee.org/stamp/stamp.jsp%3Farnumber%3D4032492)》，利用探针检测或者线程切换自适应累计等。braft 完全没有实现 pipeline，我个人认为是一个缺陷。要不要用是一个问题，有没有是另一个问题。

 RAFT 协议优化看多很多资料，除了基本的 batch + pipeline 之外，就是在三个环节：

- 日志复制
- 日志提交
- 日志应用到状态机

尝试做并行和异步化，有了 batch 和 pipeline 的能力，针对应用的存储类型，在满足业务语义的情况下做这三个阶段的并行优化。这一点可以看 PorlarDB 最近发在 VLDB2018 的论文。



---------------------------------update-----------------

我们开源了使用 java 重写的 jraft 项目 [alipay/sofa-jraft](https://link.zhihu.com/?target=https%3A//github.com/alipay/sofa-jraft)，基于  braft 移植而来，并且做了 pipeline 优化、线性一致读实现等。



Raft协议详解

https://zhuanlan.zhihu.com/p/27207160



开源实现非常多。这里有个列表，百八十种，各种语言

有一个raft的在线动画演示，可以点击节点控制宕机和重启

https://raft.github.io/



关于Raft算法，有两篇经典的论文，一篇是《In search of an Understandable Consensus Algorithm》，这是作者最开始讲述Raft算法原理的论文，但是这篇论文太简单了，很多算法的细节没有涉及到。更详细的论文是《CONSENSUS: BRIDGING THEORY AND PRACTICE》，除了包括第一篇论文的内容以外，还加上了很多细节的描述。在我阅读完etcd raft算法库的实现之后，发现这个库的代码基本就是按照后一篇论文来写的，甚至有部分测试用例的注释里也写明了是针对这篇论文的某一个小节的情况做验证。



https://www.codedump.info/post/20180921-raft/



Raft一致性算法流程描述

https://www.jianshu.com/p/37877e046132

https://zhuanlan.zhihu.com/p/91288179