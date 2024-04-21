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


ReadView

ReadView（也称为一致性读视图）是数据库系统中的一个重要概念，主要用于多版本并发控制（MVCC）机制中，特别是在InnoDB存储引擎中。

ReadView的本质是一个快照，它记录了数据库在某个时刻的数据信息，包括系统当前活跃事务的ID数组及相关信息。ReadView的主要作用是帮助事务在执行读操作时确定它们能看到哪个版本的数据记录，这可能不是最新版本的数据，也可能是最新版本的数据。
在事务开始时，根据事务的隔离级别，ReadView决定事务能看到什么数据信息。例如，在可重复读（Repeatable Read）和读已提交（Read Committed）隔离级别中，ReadView都发挥着关键作用。通过使用ReadView，事务可以访问到正确的数据版本，确保了事务的隔离性和一致性。
