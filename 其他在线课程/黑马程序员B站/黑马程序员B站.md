# 黑马程序员B站

mysql mvcc
ReadView
两种隔离级别下面有效？

RC
RR

快照读
简单的select(不加锁)就是快照读，快照读，读取的是记录数据的可见版本，有可能是历史数据，不加锁，是非阻塞读。
Read Committed:每次select，都生成一个快照读。
Repeatable Read:开启事务后第一个select语句才是快照读的地方。
