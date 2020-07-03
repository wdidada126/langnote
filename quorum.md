# quorum



[分布式系统理论之Quorum机制](https://www.cnblogs.com/hapjin/p/5626889.html)



[Quorum一致性协议](https://www.cnblogs.com/renolei/p/5398574.html)



[分布式系统之Quorum机制](https://blog.csdn.net/tb3039450/article/details/80249664)


https://www.cnblogs.com/hapjin/p/5626889.html





当需要修改数据时，就需要更新所有的副本数据，这样才能保证数据的一致性（Consistency）。因此，就需要在 C(Consistency) 和 A(Availability) 之间权衡。

而Quorum机制，就是这样的一种权衡机制，一种将“读写转化”的模型


在介绍Quorum之前，先看一个极端的情况：WARO机制

 WARO(Write All Read one)是一种简单的副本控制协议，当Client请求向某副本写数据时(更新数据)，只有当所有的副本都更新成功之后，这次写操作才算成功，否则视为失败。

从这里可以看出两点：①写操作很脆弱，因为只要有一个副本更新失败，此次写操作就视为失败了。②读操作很简单，因为，所有的副本更新成功，才视为更新成功，从而保证所有的副本一致。这样，只需要读任何一个副本上的数据即可。假设有N个副本，N-1个都宕机了，剩下的那个副本仍能提供读服务；但是只要有一个副本宕机了，写服务就不会成功。


Quorum机制应用实例

HDFS高可用性实现



抽屉原理