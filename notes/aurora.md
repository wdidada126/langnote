# aurora

在2017年5月芝加哥举办的世界顶级数据库会议SIGMOD/PODS上，作为全球最大的公有云服务提供商，Amazon首次系统的总结了新一代云端关系数据库Aurora的设计实现。Aurora是Amazon在2014 AWS re:Invent大会上推出的一款全新关系数据库，提供商业级的服务可用性和数据可靠性，相比MySQL有5倍的性能提升，并基于RDS 提供自动化运维和管理；

房晓乐（葱头巴巴），PingCAP 资深解决方案架构师，前美团数据库专家、美团云 CDS 架构师、前搜狗、百度资深 DBA，擅长研究各种数据库架构，NewSQL 布道者。

https://dbaplus.cn/news-160-1748-1.html

2017年，Amazon 在 SIGMOD 上发表了论文《Amazon Aurora: Design Considerations for High Throughput CloudNative Relational Databases》

https://www.cnblogs.com/cchust/p/7476876.html
aurora改写MySQL的Innodb存储引擎

https://www.cnblogs.com/163yun/p/9020693.html


https://www.zhihu.com/question/66715254

云数据库有很多。包括：AWS的Amazon Aurora，阿里的PolarDB、华为的云数据库MySQL等。


整个分布式数据库的技术方向现在分成两个流派，一个是类似的 Aurora 的「共享存储」型（具体就不展开了，资料很多），还有一个流派是 Spanner 为代表的纯 Share nothing 的架构

我觉得并没有谁比谁高级和落后，Share nothing 的架构在单集群更大规模下的使用场景我觉得会更好，而 Aurora 的架构更适合云（多租户 + 更好的兼容性）。

整个分布式数据库的技术方向现在分成两个流派，一个是类似的 Aurora 的「共享存储」型（具体就不展开了，资料很多），还有一个流派是 Spanner 为代表的纯 Share nothing 的架构，我觉得并没有谁比谁高级和落后，Share nothing 的架构在单集群更大规模下的使用场景我觉得会更好，而 Aurora 的架构更适合云（多租户 + 更好的兼容性）。

Amazon Aurora 是一种与 MySQL 和 PostgreSQL 兼容的关系数据库，专为云而打造，既具有传统企业数据库的性能和可用性，又具有开源数据库的简单性和成本效益。
Amazon Aurora 的速度最高可以达到标准 MySQL 数据库的五倍、标准 PostgreSQL 数据库的三倍。它可以实现商用数据库的安全性、可用性和可靠性，而成本只有商用数据库的 1/10。Amazon Aurora 由 Amazon Relational Database Service (RDS) 完全托管，RDS 可以自动执行各种耗时的管理任务，例如硬件预置以及数据库设置、修补和备份。
Amazon Aurora 采用一种有容错能力并且可以自我修复的分布式存储系统，这一系统可以把每个数据库实例扩展到最高 64TB。它具备高性能和高可用性，支持最多 15 个低延迟读取副本、时间点恢复、持续备份到 Amazon S3，还支持跨三个可用区 (AZ) 复制。
https://zhuanlan.zhihu.com/p/30159571

Amazon Aurora: Design Considerations for High Throughput Cloud-Native Relational Databases

[Amazon Aurora解读(SIGMOD 2017)](https://www.cnblogs.com/cchust/p/7476876.html)

Quorum协议
