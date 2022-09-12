# gossip

https://zhuanlan.zhihu.com/p/457098784

Gossip最终一致性算法，适用于去中心化，容忍时延，读多写少的分布式集群场景。

两个节点（A、B）之间存在三种通信方式，要么A最新，要么B最新，要么A/B一样新：

push: A将数据和版本号push给B，B更新本地

pull：比push多一步：B更新本地后，将数据push back给A，A更新本地

push/pull：比pull多一步：A更新本地后，再将数据push back B，B更新本地



gossip协议



维基百科

https://en.wikipedia.org/wiki/Gossip_protocol



作为Redis官方出品，Redis-Cluster有很多优点，但是，当集群规模超过百级别后，Gossip协议的效率将会显著下降，通信成本越来越高。此外，Redis-Cluster模式下，16384个slot中只要有任意一个slot不可用，整个集群都将不可用，换言之，任何一个被指派slot的主节点故障，在其恢复期间，集群都是不可用的。鉴于此，Redis-Cluster并不适合超大规模商用场景，国内IT巨头基本上采用的都是自研的集群方案，如阿里云ApsaraDB for Redis/ApsaraCache，腾讯的CRS；当然，Redis-Cluster也有很成功的商用案例：亚马逊采用的就是Redis-Cluster。

https://blog.csdn.net/Jin_Kwok/article/details/90111631







想要了解什么是 `Gossip` 协议，建议从 `Redis` 集群的架构中去学习，往往使用 `Gossip` 协议的集群实现都比较复杂，而且容易出错，另外 `Gossip` 协议本身由于数据包庞大，也极易造成性能抖动问题。



es也是使用了gossip协议



先debug吧

搜开源实现

https://github.com/hashicorp/memberlist

http://vearne.cc/archives/584



jgossip 1.1.0 已经发布。jgossip 是一个使用 java 开发的 gossip 协议的实现，已经在一些大公司内部使用，支撑大量的服务正常运行。

https://sourceforge.net/projects/jgossipforum/files/

jgossip maven？

https://mvnrepository.com/artifact/net.lvsq/jgossip

https://github.com/monkeymq/jgossip



##### 使用场景
[分布式原理：一文了解 Gossip 协议](https://www.iteblog.com/archives/2505.html)

[《redis设计与实现》-17 集群 gossip协议](https://blog.csdn.net/bohu83/article/details/86507369)

[深入浅出理解分布式一致性协议Gossip和Redis集群原理](https://blog.csdn.net/Jin_Kwok/article/details/90111631)





[P2P 网络核心技术：Gossip 协议](https://zhuanlan.zhihu.com/p/41228196)



Gossip protocol 也叫 Epidemic Protocol （流行病协议），实际上它还有很多别名，比如：“流言算法”、“疫情传播算法”等。



Gossip protocol 最早是在 1987 年发表在 ACM 上的论文 《Epidemic Algorithms for Replicated Database Maintenance》中被提出。主要用在分布式数据库系统中各个副本节点同步数据之用，这种场景的一个最大特点就是组成的网络的节点都是对等节点，是非结构化网络，这区别与之前介绍的用于结构化网络中的 DHT 算法 Kadmelia。

我们知道，很多知名的 P2P 网络或区块链项目，比如 IPFS，Ethereum 等，都使用了 Kadmelia 算法，而大名鼎鼎的 Bitcoin 则是使用了 Gossip 协议来传播交易和区块信息。



https://zhuanlan.zhihu.com/p/130332285





关于Gossip协议，我们需要了解最终一致的达成过程，同时我们需要知道当前已落地的应用为Cassandra缓存中间件、Consul等。

关于Raft，我们要明确两个要素: 选主以及日志复制，目前落地Raft协议的中间件有：Etcd、consul等。





首先Consul支持多数据中心，在上图中有两个DataCenter，他们通过Internet互联，同时请注意为了提高通信效率，只有Server节点才加入跨数据中心的通信。

在单个数据中心中，Consul分为Client和Server两种节点（所有的节点也被称为Agent），Server节点保存数据，Client负责健康检查及转发数据请求到Server；Server节点有一个Leader和多个Follower，Leader节点会将数据同步到Follower，Server的数量推荐是3个或者5个，在Leader挂掉的时候会启动选举机制产生一个新的Leader。

集群内的Consul节点通过gossip协议（流言协议）维护成员关系，也就是说某个节点了解集群内现在还有哪些节点，这些节点是Client还是Server。单个数据中心的流言协议同时使用TCP和UDP通信，并且都使用8301端口。跨数据中心的流言协议也同时使用TCP和UDP通信，端口使用8302。

集群内数据的读写请求既可以直接发到Server，也可以通过Client使用RPC转发到Server，请求最终会到达Leader节点，在允许数据轻微陈旧的情况下，读请求也可以在普通的Server节点完成，集群内数据的读写和复制都是通过TCP的8300端口完成。

Consul 集群间使用了 `Gossip` 协议通信和 raft 一致性算法





https://www.slidestalk.com/u5096/p2p_gossip_protocol

Gossip协议又被称为流行病协议（Epidemic Protocol），也有人叫它反熵（Anti-Entropy）。Gossip协议于1987年在ACM上发表的论文 《Epidemic Algorithms for Replicated Database Maintenance》中被提出，主要用在分布式数据库系统中各个副本节点间的数据同步，这种场景的一个最大特点就是组成网络的节点都是对等的，网络中即使有的节点因宕机而重启，或有新节点加入，但经过一段时间后，这些节点的状态也会与其他节点达成一致，也就是说，Gossip天然具有分布式容错的优点。它是一个带冗余的容错算法，是一个最终一致性算法。虽然无法保证在某个时刻所有节点状态一致，但可以保证在”最终“所有节点一致，”最终“是一个现实中存在，但理论上无法证明的时间点。 大名鼎鼎的 Bitcoin 则是使用了 Gossip 协议来传播交易和区块信息，实际上Gossip可以用于众多能接受“最终一致性”的领域：失败检测、路由同步、Pub/Sub、动态负载均衡。 但Gossip的缺点也很明显，冗余通信会对网路带宽、CPU资源造成很大的负载，而这些负载又受限于通信频率，该频率又影响着算法收敛的速度，因此，针对不同的应用场景，也有很多的优化方法。

