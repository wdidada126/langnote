# 分布式 ds

[工商银行引入网易 分布式事务](https://www.zhihu.com/question/353308256/answer/943015137)

分布式系统 入门容易，深入难

云环境

网络调用耗时

200ms

内网

10ms

分布式策略，比如故障检测中的复制

[分布式软件工程](https://zhuanlan.zhihu.com/p/68387244)

因为单机的性能已经到瓶颈了
jmeter是分布式

mysql 读写分离

binlog

https://blog.csdn.net/JackLiu16/article/details/79189831

做个实验

分布式存储系统有一系列的理论、算法、技术作为支撑：例如 *Paxos*, *CAP*, *Consistent Hash*, *Timing (时钟)*, *2PC, 3PC* 等等。那么如何掌握好这些技术呢？以我个人的经验，掌握这些内容一定要理解其对应的上下文。什么意思呢？就是一定要去思考为什么在当下环境需要某项技术，如果没有这个技术用其它技术替代是否可行，而不是一味的陷入大量的细节之中。例如：如何掌握好 Paxos?  Paxos本质上来说是一个三阶段提交，更 high level 讲是一个分布式锁。理解paxos必须一步一步从最简单的场景出发，比如从最简单的 master-backup 出发，发现不行，衍生出多数派读写，发现还是不行，再到 paxos.  之后再了解其变种，比如 fast paxos, multi-paxos.

同理为什么需要 Consistent Hash, 我们可以先思考如果用简单range partition 划分数据有什么问题。再比如学习 2pc, 3pc 这样的技术时，可以想想他们和paxos 有什么关系，能否替代 paxos。

分布式存储系统有一系列的理论、算法、技术作为支撑：例如 *Paxos*, *CAP*, *Consistent Hash*, *Timing (时钟)*, *2PC, 3PC* 等等。那么如何掌握好这些技术呢？以我个人的经验，掌握这些内容一定要理解其对应的上下文。什么意思呢？就是一定要去思考为什么在当下环境需要某项技术，如果没有这个技术用其它技术替代是否可行，而不是一味的陷入大量的细节之中。例如：如何掌握好 Paxos?  Paxos本质上来说是一个三阶段提交，更 high level 讲是一个分布式锁。理解paxos必须一步一步从最简单的场景出发，比如从最简单的 master-backup 出发，发现不行，衍生出多数派读写，发现还是不行，再到 paxos.  之后再了解其变种，比如 fast paxos, multi-paxos. 同理为什么需要 Consistent Hash, 我们可以先思考如果用简单range partition 划分数据有什么问题。再比如学习 2pc, 3pc 这样的技术时，可以想想他们和paxos 有什么关系，能否替代 paxos。

https://www.zhihu.com/question/23645117/answer/124708083

https://www.jianshu.com/p/dcb3b48d6211

分布式系统与云计算之概述

理清分布式系统中会遇到的各种技术、理论、协议，以及展示上述组件之间相互协作的例子

https://blog.csdn.net/yuandong_d/article/details/83759494

[分布式学习最佳实践：从分布式系统的特征开始](https://www.cnblogs.com/xybaby/p/8544715.html)

分布式学习最佳实践：从分布式系统的特征开始
https://www.cnblogs.com/xybaby/p/8544715.html

刘杰：今天好友说我好多年前写的《分布式系统原理介绍》是他们公司新人培训的教材，让我觉得过去做的工作还是很有意义。...推荐一本好书《Designing Data-Intensive Applications》 

分布式系统知识体系
https://www.cnblogs.com/zhaowei121/p/11714273.html

朱一聪
https://www.zhihu.com/people/zhu-yicong/collections

我做分布式系统
https://www.zhihu.com/people/wo-zuo-fen-bu-shi-xi-tong

https://github.com/lni

这个问题可以看做是 lsm 和 btree 相比有什么优势。 sqllite 作者尝试了一把，觉得也没啥优势

TerarkDB 超高性能存储引擎

哈哈，承蒙夸奖，很多角度来看我都是没啥经验。刚粗略看了全文，确实如你所说软件问题硬件玩。看标题以为是 say no to paxos,原来重点在 overload,刚开始看前言感觉实在碉堡，粗看完全文的感觉它原理上还是 paxos, 相比于传统的 paxos-like 协议的工程实现，它独立出了 sequencer,sequencer 和服务器的链路比服务器间的链路快，或者放在了一个原本就绕不开的网络硬件节点上，工程上近似优化掉了一次延时。独立出 sequencer 的好处是复制协议 replication 的 可以直接 reply 给客户端，客户端判断多数集的逻辑(其实不确定传统的实现这么做必然不行？这确实是得益于 sequencer 的独立)，坏处是要处理 sequencer 的失败，看起来实现更复杂了。 sequencer 的失败，sessionnumber 唯一自增看到了 paxos 的影子，controller 更是直接 paxos replication 。最疑惑的地方是 实验部分单协议的吞吐量相比 batch 的 paxos 优势也就20%左右，怎么到了应用高几倍了…有时间再精读，还是值得一看的文章了。不知道老鸟怎么看这文？

我没有看NOPaxos的协议本身（section 5），别的看了。是把sequencer放必经的地方，协议复杂了。最后那个kv store的应用没有讲清楚具体怎么搭建的试验，图片下提到了10ms Service Level Objective，是在10ms内能完成的txn数？
感觉和你类似，abstract貌似很牛，读了感觉：
1. group是静态的，没谈改变membership。会是和一般的协议一样自己跑一次一致性定值改membership？
2. 只能一个数据中心内用
3. 如果大家都玩硬件方法，Speculative Paxos似乎可以硬件算那个hash提高吞吐量，或者干脆不管，本来也不差多少。而数据中心丢包率从微软数据中心的统计来看，主要是短暂的峰值引起的。图九丢包率带来的Speculative Paxos的吞吐下降是不持续的。也就是说，这个NOPaxos不比Speculative Paxos实际厉害多少。
4. 实际生产环境，没有办法真的用前两种硬件实现，他们都要和网络设置一起用，部署起来太麻烦。只能用第三种endhost实现，这样延迟就没有那么好看了。
改天我再学习学习Speculative Paxos ;)



上面 “10ms内能完成的txn” 是想说响应速度小过10ms的txn数。


确实总体的感觉比摘要的冲击要逊，Speculative Paxos 这个也不会，不过看5.3介绍一大弊端是quorum 比例更高。nopaxos它的普通 replica的membership可以用一般协议的办法 ，5节有讲，所以文中略过。nopaxos 协议本身就没啥大特别了，leader 失败时文中直接用了 ViewStamp 的 view change,一个独特的地方是 收到不连续的包leader 要用 no op 填 gap 来达到一致，因为client 重发的请求分配到的序列号会和原来不同,丢包了等不来一个真正一样的。还有一个不实用的地方是非主leader不执行 op(因为就协议本身而言replica不含 learner,文中也提到了作为优化可以后台加一个).题外话：实验 paxos batch 的吞吐都到200k 了，硬盘参数未介绍，这么一想微信的实现性能是在有点过不去。坐等老鸟 spec paxos 心得


如果是这样…我的感觉略无耻，以已之长击敌之短


viewstamp我从来没有看过，刚才看了nopaxos文章，果然没有注意到spec paxos要3n/4的super majority quorum。如果这样，至少就要4个机器，这就没有办法玩了，代价更大。 ;)
硬盘没有提，但他们试验结果显示和unreplicated性能基本一样，那估计两个可能1）nopaxos和unreplicated测的时候都没有用实际落盘操作，2）都落盘了，ops/sec都受限于硬盘iops极限了。一次操作一次落盘看，240k ops/sec左右对应240k iops，基本很接近是现在服务器上常见ssd的极限。
Samsung SM961 SSD
微信的phxpaxos的实现我读了一编，很好的了解国内工程水平的机会，然后又刚发现了百度的raft实现，是做jieba那哥们儿做的。
GitHub - baidu/ins: iNexus, coordinate large scale services
性能都不行，都是10k ops/sec级别的。raft我协议也没有看过，但听人说一大简化是不允许log gap，是不是就类似微信paxos的实现，只能一个个定值。有意思的是包括raft 的thesis，都是跳不出10k ops/sec这个级别。





raft 和微信那个不同，虽然不允许 log gap,但是可以连续顺序落盘，不需要等前一个 commit.这个和zookeeper 实现类似。raft 是个我挺喜欢的协议，手把手教工程实现 paxos。当初看了 paxos 一脸懵比这有什么用，直到看了 raft.raft最大的亮点主 宕 选主相比于之前的实现 无比简洁，不冲突的话一轮消息即可。raft 的 thesis ，主向备发消息是同步的，收到回复再发下一轮，不过一次性会发多个，这个可能是一个瓶颈。我总觉得最优的实现是可以压满磁盘吞吐量的，不过暂时只能纸上谈兵。有机会去测下 zookeeper，感觉它的性能要优些，多年前机械盘是 10k 水准。



planetlab



分布式事务一直没有搞明白

在2016年初的时候 我写了一个小的软件 希望和微信一样可以分布式，水平扩展，可靠的数据安全。所以从理论开始 我设计了这样一款软件的原型。但是这款软件是否可以达到100万 或者1000万在线没有测试之前是没有实际意义的。所以我利用aws做了完整的100万用户，建立了2000万相互关系，发送了1.4亿条消息。证明了系统通过增加主机 性能可以线性的增加。系统本身可靠性也是可以认证的。这大概可以算分布式项目的一个简单实验吧！wiki https://github.com/xiaojiaqi/fakewechat/wiki
压力测试全过程
https://github.com/xiaojiaqi/fa



Mola(https://developer.baidu.com/platform/s60)、Armor(分布式Key-Value系统)、Big Pipe(百度的消息传输系统)


分布式架构之 数据分布
https://www.wzxaini9.cn/article/363


Apache Doris – 在线分析型分布式数据库

赵纯，百度，资深研发工程师，研究生毕业以来一直在百度从事分布式数据库系统设计与研发。作为核心人员开发百度Palo系统，当前已经贡献给Apache社区并改名叫做Apache Doris(incubating)

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
