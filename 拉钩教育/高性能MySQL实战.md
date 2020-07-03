# 高性能MySQL实战



周彦伟



分为五大部分。

第一部分主要介绍 MySQL 的体系架构与存储引擎，也会介绍一些事务与锁的机制。从整体到细节地帮助你比较深入地去了解 MySQL 的内部机制和原理，这也是在面试过程中面试官比较喜欢问的。

在第二部分里，我们会用两个课时来介绍 MySQL 库表设计和索引设计的一些思路。

第三部分，我们会介绍 MySQL 的架构设计和查询优化，这也是在工作中最常碰到的。

在第四部分，我们会来介绍 MySQL 的高可用架构方案和一些要点，同时，也会讲解一下 MySQL 自动化运维体系构建的一些思路和知识点。

最后一部分，我们会通过一个亿级数据库的项目，用实战的方式来讲解怎么去规划或设计一个可扩展的 MySQL 架构。



![db_type](..\imgs\lagou_edu\db_type.png)





MySQL 常见的坑 .png



MySQL 知识点全景图.png



MySQL推荐书籍.png





第07讲：如何做到MySQL的高可用



企业初期使用较多的高可用架构，一类是基于 Keepalived + VIP + MySQL 主从/双主，一类是封装好的 MMM 集群，两者本质是一样的，MMM 相比前者多了一套工具集来帮助运维。



MHA



去哪儿网 QMHA



PXC/MGR





第08讲：搭建稳固的MySQL运维体系

Arkcontrol 的备份恢复中心就是一个 MySQL 自动化备份恢复系统





10



数据库架构又可以分为三大类：主从架构、集群架构和分布式架构。在主从架构类别中，又可以分 7 小类，分别是。

传统主从复制，有时候也称为：异步复制（希望大家再复习下 MySQL 中的各种存储引擎，要注意它们的特性）。

基于 GTID 的主从复制，从 MySQL 5.6 版本后，推荐使用这种方式的复制，原因前面的课程中已经有讲解。

主主复制，这个还有不少传统企业仍在使用。

级连复制，面试的时候特别容易问到关于复制的各种变换，用的就是级连复制，注意技巧，工作中也经常用。

多源复制，MySQL 5.7 版本的一个特性，在某些特殊场景中会用到。

延迟复制，备份中会用到，尤其是当数据量特别大的情况。

半同步复制，对数据一致性要求比较高的业务场景，可以考虑用。



在集群架构类别中，又可以分为 6 小类，分别是：

MySQL Group Replication；

Percona XtraDB Cluster；

MySQL Galera Cluster；

MySQL NDB Cluster，有时候也称为 MySQL Cluster；

MySQL + 共享存储方案；

MySQL + DRBD 方案。



在分布式架构类别中，又可以分为 2 小类，分别是：

基于分布式事务的数据库，如 Google Cloud Spanner 和 TiDB。

基于分布式存储的数据库，如极数云舟的 ArkDB、Aurora、PolarDB。

数据库高可用
在前面第 7 课时中，我们详细介绍了几种常用的 MySQL 数据库高可用解决方案，这里再给大家罗列出来了，如果这里列的在前面的课程中没有介绍到，大家可以自行去学习。主要有下面 6 种：

Keepalive、Heartbeat、Haproxy；

MMM；

MHA；

Orchestrator、Raft；

极数云舟的 Arksentinel；

Zookeeper、Consul、Etcd。