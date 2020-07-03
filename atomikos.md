# atomikos

<<<<<<< HEAD
Spring提供了JTA介入方式，但是没有提供JTA实现，目前JTA实现：

Java Open Transaction Manager (JOTM)

JBoss TS

Bitronix Transaction Manager (BTM)

Atomikos。
=======
Spring提供了JTA介入方式，但是没有提供JTA实现，目前JTA实现： Java Open Transaction Manager (JOTM), JBoss TS, Bitronix Transaction Manager (BTM), 和 Atomikos。
>>>>>>> afe522da082020e5ece0b75c43067644b2edb768



api jar

\javax\transaction\jta\1.1\jta-1.1-sources.jar



[2PC之JTA原理与实现](https://www.cnblogs.com/junzi2099/p/7889938.html)

[关于分布式事务、两阶段提交协议、三阶提交协议](https://www.hollischuang.com/archives/681)



2PC,是Two Phase Commit的缩写，即二阶段提交，就是将事务的提交过程分成了两个阶段来处理



- **阶段****1****：准备阶段**



**3PC****，三阶段提交协议，是****2PC****的改进版本，即将事务的提交过程分为CanCommit****、****PreCommit****、****do Commit****三个阶段来进行处理。****阶段****1****：****CanCommit** 





相对于2PC，3PC主要解决的单点故障问题，并减少阻塞，因为一旦参与者无法及时收到来自协调者的信息之后，他会默认执行commit。而不会一直持有事务资源并处于阻塞状态。但是这种机制也会导致数据一致性问题，因为，由于网络原因，协调者发送的abort响应没有及时被参与者接收到，那么参与者在等待超时之后执行了commit操作。这样就和其他接到abort命令并执行回滚的参与者之间存在数据不一致的情况。