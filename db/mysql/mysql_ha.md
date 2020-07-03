# mysql ha

读写分离
keeplived
heartbeat

Heartbeat+MySQL+NFS 实现高可用(HA)的MySQL集群
https://blog.51cto.com/feilong0663/1531806





[heartbeat](http://www.linux-ha.org/doc/users-guide/_introduction_to_heartbeat.html)





我们用到的集群系统主要就2种:

高可用(High Availability)HA集群, 使用Heartbeat实现;也会称为”双机热备”, “双机互备”, “双机”。
负载均衡群集(Load Balance Cluster)，使用Linux Virtual Server(LVS)实现;

heartbeat （Linux-HA）的工作原理：heartbeat最核心的包括两个部分，心跳监测部分和资源接管部分，心跳监测可以通过网络链路和串口进行，而且支持冗 余链路，它们之间相互发送报文来告诉对方自己当前的状态，如果在指定的时间内未受到对方发送的报文，那么就认为对方失效，这时需启动资源接管模块来接管运 行在对方主机上的资源或者服务。







MMM（Master-Master replication manager for MySQL）是一套支持双主故障切换和双主日常管理的脚本程序。MMM使用Perl语言开发，主要用来监控和管理MySQL Master-Master（双主）复制，虽然叫做双主复制，但是业务上同一时刻只允许对一个主进行写入，另一台备选主上提供部分读服务，以加速在主主切换时刻备选主的预热，可以说MMM这套脚本程序一方面实现了故障切换的功能，另一方面其内部附加的工具脚本也可以实现多个slave的read负载均衡。

MMM提供了自动和手动两种方式移除一组服务器中复制延迟较高的服务器的虚拟ip，同时它还可以备份数据，实现两节点之间的数据同步等。由于MMM无法完全的保证数据一致性，所以MMM适用于对数据的一致性要求不是很高，但是又想最大程度的保证业务可用性的场景。对于那些对数据的一致性要求很高的业务，非常不建议采用MMM这种高可用架构。



[MySQL-MMM实现MySQL高可用](https://www.cnblogs.com/panwenbin-logs/p/8284593.html)



MySQL高可用工具drbd





双主高可用



多主多从高可用集群自动切换