# NWR

paxos raft类似



CAP、BASEd、二阶段提交协议、三阶段提交协议、拜占庭将军问题、paxos、Raft、ZAB

https://www.cnblogs.com/Mike_Chang/p/13045343.html



nwr机制



分布式系统中有副本控制

让我们先来看看这三个字母的含义：
N：在分布式存储系统中，有多少份备份数据
W：代表一次成功的更新操作要求至少有w份数据写入成功
R： 代表一次成功的读数据操作要求至少有R份数据成功读取



当N是3，W是2、R是2的时候，W+R>N，这种情况对于客户端就是强一致性的。

https://www.cnblogs.com/liyulong1982/p/5999169.html



https://blog.csdn.net/wolf_love666/article/details/93034314

https://blog.csdn.net/lin819747263/article/details/106341033





[NWR算法](https://blog.csdn.net/wolf_love666/article/details/93034314)



[分布式Quorum机制,NWR策略读写模型](https://blog.csdn.net/bigtree_3721/article/details/76805103)



N：在分布式存储系统中，有多少份备份数据
W：代表依次成功的更新操作要求至少要w份数据写入成功
R : 代表依次成功的读数据操作要求至少有R份数据成功读取。
NWR值的不同组合会产生不同一致性结果，当W+R>N的时候，整个系统对于客户端来讲能保证强一致性。如果W+R<N则无法保证一致性。下面举个例子：
N=3，W=2,R=2.
N=3表示有3个副本数据，W=2代表队数据修改操作写入成功2个，R=2代表读取成功2个。




