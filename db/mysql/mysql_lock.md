# mysql lock

MySQL InnoDB 中的 Gap Lock（间隙锁）和 Next-Key Lock（临键锁 / 下一键锁）是专门为了在 Repeatable Read（可重复读）隔离级别下防止幻读（Phantom Read）而设计的锁机制。 它们是 InnoDB 行级锁的重要补充，MVCC 只能解决脏读和不可重复读，但无法完全防止幻读（尤其是当前读场景）。1. 三种核心锁的对比（InnoDB 行锁家族）锁类型
英文名称
锁定对象
是否包含记录本身
主要目的
典型场景
是否防止幻读
Record Lock
记录锁
单条索引记录（索引上的点）
是
防止当前记录被修改/删除
等值查询命中记录（如 WHERE id=5）
否
Gap Lock
间隙锁
索引记录之间的“间隙”（开区间）
否
防止其他事务在间隙中插入新记录
范围查询、非唯一索引、记录不存在等
是（核心防插入）
Next-Key Lock
临键锁 / 下一键锁
记录 + 记录前面的间隙（左开右闭区间）
是
同时防修改/删除 + 防插入（最常用）
范围扫描、非唯一索引范围查询
是（最完整）

Next-Key Lock = Record Lock + Gap Lock（官方定义：一个 Next-Key Lock 就是索引记录上的记录锁 + 该记录前面间隙的间隙锁）。
默认情况下，InnoDB 在 Repeatable Read 隔离级别下，对当前读（SELECT ... FOR UPDATE / LOCK IN SHARE MODE / UPDATE / DELETE）使用 Next-Key Lock 策略，从而有效防止幻读。

2. 核心概念详解Record Lock（记录锁）最基础的行锁，只锁住已经存在的具体一行（其实锁的是索引记录）。
即使是主键/唯一索引，也只锁点，不锁范围。
例子：SELECT * FROM t WHERE id = 10 FOR UPDATE; → 只锁 id=10 这一行。
不能防幻读：因为别人仍可以在 id=10 前后插入新行。

Gap Lock（间隙锁）锁的是两个相邻索引记录之间的空隙（不包括两端的记录本身）。
纯粹为了阻止插入（insert intention lock 与之冲突）。
多个事务的 Gap Lock 之间不互斥（可以共存），只要不插入就行。
例子：假设表中 id 有 5、10、15 三条记录。Gap Lock 可以锁 (5,10)、(10,15)、(-∞,5)、(15,+∞) 等间隙。

唯一作用：防止幻读中的“插入新幻影行”。

Next-Key Lock（临键锁）左开右闭区间：(前一个记录, 当前记录] 锁住当前记录（Record Lock） + 当前记录前面的间隙（Gap Lock）。

举例（id 升序索引，现有记录 5、10、15）：对 id=10 加 Next-Key Lock → 实际锁住 (5,10] 整个区间。
别人不能插入 6、7、8、9，也不能修改/删除 id=10。

当进行范围查询或非唯一索引查询时，InnoDB 会自动把扫描到的每个记录都加上 Next-Key Lock，从而把整个范围的间隙都保护起来。

3. 防止幻读的原理（为什么能防幻读）幻读场景：事务 A 两次执行相同范围查询，中间事务 B 插入新行，导致 A 第二次看到“幻影行”。InnoDB 解决方案（RR 级别 + 当前读）：第一次当前读 → 扫描范围，对命中的每行加 Record Lock。
同时对每行前面间隙加 Gap Lock（组合成 Next-Key Lock）。
事务 B 想在这些间隙插入 → 被 Gap Lock 阻塞，直到 A 提交。
事务 A 第二次读 → 由于间隙被锁住，B 插不进来 → 结果一致 → 无幻读。

注意：普通快照读（普通 SELECT）靠 MVCC 快照 → 不加 Gap/Next-Key Lock（读不阻塞写）。
只有当前读才会加这些锁。
唯一索引 + 等值查询 + 记录存在 → 退化为纯 Record Lock（不加 Gap），因为不可能有“插入到等值位置”的幻读。
唯一索引 + 等值查询 + 记录不存在 → 只加 Gap Lock（锁住可能的插入点）。
非唯一索引 / 范围查询 → 大量 Next-Key Lock（锁范围更大，并发下降）。

4. 常见误区与注意点Gap Lock / Next-Key Lock 只在 Repeatable Read 及以上生效（Read Committed 通常只用 Record Lock）。
会导致死锁风险增加（尤其是反向扫描、插入意向锁冲突）。
大范围扫描（如全表 UPDATE WHERE 非索引列）可能锁住大量间隙 → 并发很差。
可通过 innodb_locks_unsafe_for_binlog=1 或 Read Committed 级别关闭大部分 Gap Lock（但会牺牲幻读保护）。
SHOW ENGINE INNODB STATUS / performance_schema.data_locks 可查看实际锁区间。

简单一句话总结：Record Lock 锁点，防改删。
Gap Lock 锁缝，防插入。
Next-Key Lock 锁点+缝（最常用），InnoDB RR 级别防幻读的核心武器。

如果需要具体 SQL 示例、死锁案例、锁查看命令或与 PostgreSQL 等对比，可以继续补充！



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