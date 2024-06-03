# 分布式

Distributed System: Lease && Master

https://zhuanlan.zhihu.com/p/340246214

分布式系统
https://www.zhihu.com/question/35420101/answer/904773724

分布式系统领域经典论文翻译集
https://zhuanlan.zhihu.com/p/91434149

概论
https://zhuanlan.zhihu.com/p/92668988

后端架构师技术图谱
https://github.com/xingshaocheng/architect-awesome

Java书籍
https://github.com/sorenduan/awesome-java-books

Cluster：发表于2003年，主要介绍Google的集群架构，对Google搜索系统的架构也进行了简单介绍
GFS：发表于2003年，介绍了Google分布式文件系统的设计及实现。Hadoop中与之对应的是HDFS
MapReduce：发表于2004年，介绍了分布式的编程模型MapReduce。Hadoop中与之对应的是Hadoop MapReduce
BigTable：发表于2006，介绍了建立在GFS之上的结构化数据存储系统，Hadoop中与之对应的是HBase
Chubby：发表于2006年，分布式锁服务系统，利用了很多现有的思想，尤其是分布式系统中的很多基础理论。Hadoop中与之对应的是Zookeeper
Sawzall：发表于2006年，建立在MapReduce之上的分布式查询脚本语言。Hadoop中与之对应的是Pig Hive等

分布式任务处理服务：负责具体的业务逻辑处理

分布式节点注册和查询：负责管理所有分布式节点的命名和物理信息的注册与查询，是节点之间联系的桥梁
分布式DB：分布式结构化数据存取
分布式Cache：分布式缓存数据（非持久化）存取
分布式文件：分布式文件存取
网络通信：节点之间的网络数据通信
监控管理：搜集、监控和诊断所有节点运行状态
分布式编程语言：用于分布式环境下的专有编程语言，比如Elang、Scala
分布式算法：为解决分布式环境下一些特有问题的算法，比如解决一致性问题的Paxos算法

如何评价 TAPIR 分布式事务协议

论文地址：[http://syslab.cs.washington.edu/papers/tapir-tr14.pdf](http://syslab.cs.washington.edu/papers/tapir-tr14.pdf)
通过区分 inconsistent 和 consensus 两种操作来放宽对事务中操作顺序的要求，另外通过一个 sync 过程来同步各副本间的记录。似乎有很多的限制条件，有很多 corner case 需要考虑。
有没有哪个已知生产系统使用了这个协议？

https://www.youtube.com/watch?v=yE3eMxYJDiE
我个人是这么理解的, 没 leader 的强一致复制协议(如经典 Paxos)是不保证多少次 RTT 才能达成一致的, 好巧, 分布式事务也是不保证的. 那么无穷大 + 无穷大还是等于无穷大.
那么就干脆别搞强一致了, client 直接广播请求到那个 shard 下所有 replicas, 让分布式事务层辛苦点可能要多重试几次. 确定性的收益是最优情况下, RTT 从 2 降低到了 1, 最差情况反正是无穷大, 不差再多几个 RTT.
没想得很明白的是 abort 要怎么做, 总感觉哪里有问题. 求教

[如何评价 TAPIR 分布式事务协议](https://www.zhihu.com/question/56763641/answer/1016947765)

https://www.douban.com/doulist/42740061/

seata
servicecomb
rocketmp

正本清源，答主说的好。其实很多分布式系统的概念并不新，尤其是在数据中心操作系统的各个组件上，无论是资源管理，存储计算网络，还是上层的数据库应用，很多概念依然是从传统操作系统的功能划分上自然发展出来的。盲目跟风容易出现旧概念当个宝追捧的问题
关于事务的部分，<数据库系统实现>略有些晦涩，可以看看<Principles of transaction processing>2e

[数据库系统实现](https://book.douban.com/subject/4838430/)

讨论了数据库管理系统的三个主要成分——存储管理器、查询处理器和事务管理器的实现技术

[Principles of Transaction Processing, Second Edition](https://book.douban.com/subject/3734011/)

中译本： [事务处理原理](https://book.douban.com/subject/5412835/)

#### 
说的很好, 关系数据库的WAL, 事务太重要了.建议看stonebraker的architecture of a database system. 和Jim gray的Transaction.   回头看dynamo和gfs, 收获很多.  理解会更加深入. 其实学习完全可以按照这样的roadmap

1. WAL + RSM
2. RSM(分布式共识): TOB协议, Quorum-based协议, 和Primary-backup协议.
3. partitioning & replication + local storage engine.
4. local storage engine: bdb, innodb, leveldb.
5. 磁盘和网络优化技术.
6. 分布式一致性(隔离性).
7. 分布式事务: stm, mvcc,  乐观锁.
8. 分布式查询优化

[常见开源分布式存储系统](https://blog.csdn.net/wujin8589/article/details/70300066)

Team Foundation Server

分布式锁
https://github.com/code4wt/distributed_lock

zk实现
redis实现

分布式面试题
一、谈谈业务中使用分布式的场景
二、分布式事务产生原因应用场景解决方案
三、负载均衡的算法与实现算法实现
四、分布式锁使用场景实现方式
五、分布式 Session1. 粘性 Session2. 服务器 Session 复制3. Session 共享机制4. Session 持久化到数据库5. Terracotta 实现 Session 复制
六、分库与分表带来的分布式困境与应对之策事务问题查询问题ID 唯一性参考资料

一、谈谈业务中使用分布式的场景分布式主要是为了提供可扩展性以及高可用性，业务中使用分布式的场景主要有分布式存储以及分布式计算。分布式存储中可以将数据分片到多个节点上，不仅可以提高性能（可扩展性），同时也可以使用多个节点对同一份数据进行备份。至于分布式计算，就是将一个大的计算任务分解成小任务分配到多台节点上去执行，再汇总每个小任务的执行结果得到最终结果。

MapReduce 是分布式计算的最好例子。
- 分布式计算
- 分布式存储
- 分布式管理系统

相对于机器学习，不需要太多数学基础
入门容易，深入难

结构化存储
非结构存储
半结构化存储
in-memory存储

[MIT分布式 6.824 lab01](https://zhuanlan.zhihu.com/p/109293321)

https://baijiahao.baidu.com/s?id=1593710529411735919

[分布式 mit 中文翻译](https://www.bilibili.com/video/av91748150)

知乎 分布式简介
https://www.zhihu.com/question/35420101/answer/904773724

数据库和分布式 学习路线
https://www.zhihu.com/question/62464757/answer/202312500
