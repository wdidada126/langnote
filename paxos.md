# paxos



一种基于消息传递的分布式一致性算法



- paxos解决了分布式系统中的什么问题
- paxos中的关键概念
- Proposer           提议者;提出者;投保人;提名人;议者
- Acceptor



github repo

https://github.com/edidada/JavaPaxos



[如何浅显易懂地解说 Paxos 的算法](https://www.zhihu.com/question/19787937/answer/107750652)



paxos解决了分布式系统中的什么问题

和一个有真正paxos工程经验的人讨论一下paxos，paxos现在大多是应用于replication的一致性，用来实现一个 多节点一致的日志，和他 的讨论让我觉得要想真正的精确掌握paxos和它对应的强一致性领域，也许只有真正的在工程中实现过才行。



首先需要解释一下什么是一致性（consensus）,它是构建具有容错性（fault-tolerant）的分布式系统的基础。 在一个具有一致性的性质的集群里面，同一时刻所有的结点对存储在其中的某个值都有相同的结果，即对其共享的存储保持一致。集群具有自动恢复的性质，当少数结点失效的时候不影响集群的正常工作，当大多数集群中的结点失效的时候，集群则会停止服务（不会返回一个错误的结果）。

​       一致性协议就是用来干这事的，用来保证即使在部分(确切地说是小部分)副本宕机的情况下，系统仍然能正常对外提供服务。一致性协议通常基于replicated state machines，即所有结点都从同一个state出发，都经过同样的一些操作序列（log），最后到达同样的state。



[Paxos算法详解](https://zhuanlan.zhihu.com/p/31780743)



[Paxos Made Simple](https://www.jianshu.com/p/47849d8eeb4b)



自Paxos问世以来就持续垄断了分布式一致性算法，Paxos这个名词几乎等同于分布式一致性。Google的很多大型分布式系统都采用了Paxos算法来解决分布式一致性问题，如Chubby、Megastore以及Spanner等。开源的ZooKeeper，以及MySQL 5.7推出的用来取代传统的主从复制的MySQL Group Replication等纷纷采用Paxos算法解决分布式一致性问题。





Basic Paxos
理论研究


Multi-Paxos算法



原始的Paxos算法（Basic Paxos）只能对一个值形成决议，决议的形成至少需要两次网络来回，在高并发情况下可能需要更多的网络来回，极端情况下甚至可能形成活锁。如果想连续确定多个值，Basic Paxos搞不定了。因此Basic Paxos几乎只是用来做理论研究，并不直接应用在实际工程中。

实际应用中几乎都需要连续确定多个值，而且希望能有更高的效率。Multi-Paxos正是为解决此问题而提出。Multi-Paxos基于Basic Paxos做了两点改进：

1. 针对每一个要确定的值，运行一次Paxos算法实例（Instance），形成决议。每一个Paxos实例使用唯一的Instance ID标识。
2. 在所有Proposers中选举一个Leader，由Leader唯一地提交Proposal给Acceptors进行表决。这样没有Proposer竞争，解决了活锁问题。在系统中仅有一个Leader进行Value提交的情况下，Prepare阶段就可以跳过，从而将两阶段变为一阶段，提高效率





[朴素Paxos（Basic Paxos）算法java简易实现](https://my.oschina.net/u/2541538/blog/807185)





[Paxos算法实现](https://www.cnblogs.com/RedHandLM/p/6780698.html?utm_source=itdadao&utm_medium=referral)





[Paxos算法实现](https://www.cnblogs.com/RedHandLM/p/6780698.html)



[Paxos算法实现](http://www.mamicode.com/info-detail-1779969.html)



[深入浅出理解Paxos算法](https://blog.csdn.net/21aspnet/article/details/50700123)





在 Paxos 中，负责创建议案的角色叫“Proposer”，负责投票的角色叫“Acceptor”。

http://yojoe.cn/archives/73.html





Paxos 算法Paxos 算法，是莱斯利·兰伯特（Lesile Lamport）于 1990 年提出来的一种基于消息传递且具有高度容错特性的一致性算法。但是这个算法太过于晦涩，所以，一直以来都属于理论上的论文性质的东西。其进入工程圈的源头在于 Google 的 Chubby lock——一个分布式的锁服务，用在了 Bigtable 中。直到 Google 发布了下面的这两篇论文，Paxos 才进入到工程界的视野中来。



