# innodb_read_view
一致性读视图，即 consistent read view

MVCC模型在MySQL中的具体实现则是由 三个隐式字段，undo日志 ，Read View 等去完成的

这里说的 read view 是InnoDB 在实现 MVCC 时用到的一致性读视图，即 consistent read view，用于支持 RC(Read Committed，读提交)和 RR(Repeatable Read,可重复读)隔离级别的实现。 
read view 并没有物理结构,作用是事务执行期间用来定义"我能看到什么数据"。

MySQL_read_view在RR和RC隔离级别下的异同-一只阿木木-博客园.mhtml


InnoDB里面每个事务有一个唯一的事务ID,叫做transaction id。它是在事务开始的时候向InnoDB的事务系统申请的，是按申请顺序严格递增的。 
在innodb存储引擎下，聚簇索引记录中都包含两个必要的隐藏列: 
trx_id：每次对某条记录进行改动时,对会把对应的事务id赋值给trx_id隐藏列; 
roll_pointer：每次对某条记录进行改动时,这个隐藏列会存一个指针,可以通过这个指针找到该记录修改前的信息,也就是undo回滚段中的内容。

一文搞懂Undo_Log版本链与ReadView机制如何让事务读取到该读的数据.mhtml
注意看roll_pointer

ReadView  可见性规则

a
c
i 
d redo log

MySQL事务的特性也是基于某些底层的功能来实现的，这些特性的实现如下：


【原子性】通过undo log（回滚日志）来保证的
【一致性】则是通过持久性+原子性+隔离性来保证
【隔离性】通过MVCC（多版本并发控制+读写锁）来保证的
【持久性】通过redo log （重做日志）来保证的


