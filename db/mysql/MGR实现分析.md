# mgr



MGR实现分析 - 成员管理与故障恢复实现
MySQL Group Replication（MGR）框架让MySQL具备了自动主从切换和故障恢复能力，举single primary（单主）模式为例，primary作为主节点对外提供读写服务，是唯一的可写节点，其他节点均为secondary节点，可提供读服务。在传统的master-slave主从复制模式下，如果master发生了crash，MySQL DBA需要手动将slave升级为新master（比如关闭只读开关等），旧的master重启后需执行change master to进行复制关系重建，并执行start slave开启复制。如果是semi-sync半同步复制，还需要进行半同步参数配置。但在MGR模式下MySQL能自动发现primary crash，通过选主产生新的primary节点对外提供读写服务。旧的primary节点重启后，DBA只需要执行start group_replication即可将crash节点重新加入到Group中，在运维便利性和系统健壮性上有极大的提升。

[MySQL Group Replication（MGR）框架让MySQL具备了自动主从切换和故障恢复能力](https://www.cnblogs.com/andy6/p/10784721.html)

