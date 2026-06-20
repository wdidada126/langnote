# percona-xtradb-cluster

https://www.percona.com/doc/percona-xtradb-cluster/8.0/index.html

https://www.cnblogs.com/markLogZhu/p/11463125.html

PXC 是一套 MySQL 高可用集群解决方案，与传统的基于主从复制模式的集群架构相比 PXC 最突出特点就是解决了诟病已久的数据复制延迟问题，基本上可以达到实时同步。而且节点与节点之间，他们相互的关系是对等的。PXC 最关注的是数据的一致性，对待事物的行为时，要么在所有节点上执行，要么都不执行，它的实现机制决定了它对待一致性的行为非常严格，这也能非常完美的保证 MySQL 集群的数据一致性；

MySQL
Replication
主从 

- 数据卷挂载
- 目录挂载

https://github.com/percona/percona-xtradb-cluster
