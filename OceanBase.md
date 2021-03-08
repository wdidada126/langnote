# OceanBase


OceanBase | 试用版安装初体验
https://blog.csdn.net/daiyejava/article/details/109379738

ob docker centos 7
https://www.oceanbase.com/docs/oceanbase-database-trial/oceanbase-database-trial/V2.2.50/fbgwds


https://www.zhihu.com/question/19841579/answer/131853733

为什么OceanBase架构特别适合双十一
感谢所有同学的共同努力，OceanBase分布式关系数据库渡过了一个成功的双十一：支持了支付宝核心的交易、支付、会员和账务等，并且创造了新的纪录：交易创建17.5万笔/秒、交易支付12万笔/秒、全天累计支付10.5亿笔！
其实，虽然不是刻意设计的，但OceanBase确实比传统数据库更适合像双十一、聚划算、秒杀以及银行国库券销售等短时间突发大流量的场景：·短时间内大量用户涌入·短时间内业务流量非常大，数据库系统压力非常大·一段时间（几秒钟、几分钟、或半个小时等）后业务流量迅速或明显回落
虽然2010年设计OceanBase架构时，其实并没有特别考虑到这个突发大流量的因素。让我们从OceanBase的架构说起。OceanBase是“基线数据（硬盘）”+“修改增量（内存）”的架构，如下图所示：
<img src="https://pic1.zhimg.com/v2-8b26e58eba0a0d0f5ead3e397b20fe78_b.png" data-rawwidth="604" data-rawheight="126" class="origin_image zh-lightbox-thumb" width="604" data-original="https://pic1.zhimg.com/v2-8b26e58eba0a0d0f5ead3e397b20fe78_r.jpg"/>
即整个数据库以硬盘（通常是SSD）为载体，新近的增、删、改数据（“修改增量”）在内存，而基线数据在保存在硬盘上，因此OceanBase可以看成一个准内存数据库。这样的好处是：·写事务在内存（除事务日志必须落盘外），性能大大提升·没有随机写硬盘，硬盘随机读不受干扰，高峰期系统性能提升明显；对于传统数据库，业务高峰期通常也是大量随机写盘（刷脏页）的高峰期，大量随机写盘消耗了大量的IO，特别是考虑到SSD的写入放大，对于读写性能都有较大的影响·基线数据只读，缓存（cache）简单且效果提升·线上OceanBase的内存配置是支撑平常两天的修改增量（从OceanBase 1.0开始，每台OceanBase都可以写入，都承载着部分的修改增量），因此即使突发大流量为平日的10-20倍，也可支撑1~2个小时以上。
<img src="https://pic1.zhimg.com/v2-a9b596591401543db10953f18f4802c8_b.png" data-rawwidth="873" data-rawheight="257" class="origin_image zh-lightbox-thumb" width="873" data-original="https://pic1.zhimg.com/v2-a9b596591401543db10953f18f4802c8_r.jpg"/>
一个问题是：修改增量在内存，大概需要多大的内存？即使按双11全天的支付笔数10.5亿笔，假设每笔1KB，总共需要的内存大约是1TB，平均到10台服务器，100GB/台。另一个问题是：在类似双十一这种流量特别大的场景中，就像前面说到的，OceanBase内存能够支持峰值业务写入1~2个小时以上，之后OceanBase必须把内存中的增删改数据（“修改增量”）尽快整合到硬盘并释放内存，以便业务的持续写入。整合内存中的修改增量到硬盘，OceanBase称为每日合并，必然涉及到大量的硬盘读写（IO），因此可能对业务的吞吐量和事务响应时间（RT）产生影响。如何避免每日合并对业务的影响呢？OceanBase通过“轮转合并”解决了这个问题。众所周知，出于高可用的考虑，OceanBase是三机群（zone）部署：
<img src="https://pic4.zhimg.com/v2-739bc65497010958be4c5d81db78a42b_b.png" data-rawwidth="353" data-rawheight="302" class="content_image" width="353"/>
根据配置和部署的不同，业务高峰时可以一个机群（zone）、两个机群（zone）或者三个机群（zone）提供读写服务。OceanBase的轮转合并就是对每个机群（zone）轮转地进行每日合并，在对一个机群（zone）进行每日合并之前，先把该机群（zone）上的业务读写流量切换到另外的一个或两个机群（zone），然后对该机群（zone）进行全速的每日合并。因此在每日合并期间，合并进行中的机群（zone）没有业务流量，仅仅接收事务日志并且参与Paxos投票，业务访问OceanBase的事务响应时间完全不受每日合并的影响，仅仅是OceanBase的总吞吐量有所下降：如果先前是三个机群（zone）都提供服务则总吞吐量下降1/3，如果先前只有一个或两个机群（zone）提供服务则总吞吐量没有变化。轮转合并使得OceanBase对SSD十分友好，避免了大量随机写盘对SSD寿命的影响，因此OceanBase可以使用相对廉价的“读密集型”SSD来代替传统数据库使用的相对昂贵的“读写型”SSD，而不影响性能。此外由于轮转合并对服务器的CPU使用、硬盘IO使用以及耗时长短都不敏感（高峰期的传统数据库在刷脏页的同时还要优先保证业务访问的吞吐量和事务响应时间，刷脏页的CPU及IO资源都非常受限），因此OceanBase在每日合并时可以采用更加高效的压缩或者编码算法（比如压缩或编码速度略慢，但压缩率较高、解压缩很快的算法），从而进一步降低存储成本并提升性能。



这里需要澄清的一点是OceanBase根本就不是什么nosql数据库。OB将会100%兼容MySQL，所以OB就是纯纯的关系型（SQL)数据库，而且是纯纯的分布式关系型(SQL)数据库。这里就不跟nosql数据库做对比了，直接对比MySQL吧。比MySQL强的几点1. OB的redolog是使用分布式一致性算法paxos实现的。所以在CAP理论中，虽然OB使用的是强一致模型，但是OB能在一定网络分区的情况下做到高可用（通俗点讲就是多余半数机器还活着的时候就能干活）。官方的MySQL目前做不到这一点2. OB的存储结构使用的是两级的LSM-tree。其中内存中的C0 Btree叶节点不需要和磁盘上的btree一样大小，所以能做得比较小，对cpu的cache比较友好，并且不会有写入放大的问题。使得OB的写性能有极大的提升。同时磁盘上的C1 tree不是一个传统意义上的btree（btree未经压缩可能浪费一半空间）。空间利用率大大提高。简单来说就是速度快，省成本。这里说的比较粗略，想详细理解自己去看LSM-tree的论文。3. 数据库自动分片功能（支持hash/range，一级二级等等分片方式），提供独立的proxy路由写入查询等操作到对应的分片。这意味着数据量再大也不需要手动分库分表了。并且分片能在线的在各个server之间迁移，解决热点问题（资源分配不均的问题，做到弹性加机器和减机器）。每个分片（确切的说是被选为主的分片）都支持读写，做到多点写入（高吞吐量，性能可线性扩展）。4. 数据库内部实现的无阻塞的两阶段提交（跨机事务）。参见论文Consensus on Transaction Commit 5. 数据库原生的多租户支持。能直接隔离租户之间的cpu，mem，io等资源。6. 基于代价的SQL查询优化和改写功能，对于复杂的分析型SQL做得比MySQL好（目前比Oracle差，正在努力追赶中）。支持各种类型的join算法（nestloop, merge, hash），优化器会自动选择最优的join类型。支持类似Oracle的SPM功能，用户能很轻松自如的管理查询计划。7. 自动化的集群管理，包括机器上下线，自动下故障盘等等。总之OB的设计理念就是只要是数据库需要解决的问题就不让用户操心。



https://blog.csdn.net/michaelyang_yz/article/details/50821721
Oracle SPM（SQL Plan Management）介绍及演示SQL
