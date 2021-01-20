# mysql lock



MySQL锁机制

https://zhuanlan.zhihu.com/p/75673270



explain + 查询SQL - 用于显示SQL执行信息参数，根据参考信息可以进行SQL优化



[何登成的博客](https://www.cnblogs.com/jhj117/p/6028715.html)

http://hedengcheng.com/

专注于 mysql数据库的专家。

MySQL 加锁处理分析（何登成）
网易杭研-何登成
https://blog.csdn.net/seven_3306/article/details/17303039

MVCC (Multi-Version Concurrency Control) (注：与MVCC相对的，是基于锁的并发控制，Lock-Based Concurrency Control)
lbcc mvcc


MVCC最大的好处，相信也是耳熟能详：读不加锁，读写不冲突。

在读多写少的OLTP应用中，读写不冲突是非常重要的，极大的增加了系统的并发性能，这也是为什么现阶段，几乎所有的RDBMS，都支持了MVCC。

在MVCC并发控制中，读操作可以分成两类：快照读 (snapshot read)与当前读 (current read)。


索引类型 
索引方法 


MySQL目前主要有以下几种索引类型：
1.普通索引
2.唯一索引
	3.主键索引
	4.组合索引
5.全文索引


索引方法
btree
hash
