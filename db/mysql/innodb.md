# innode

数据库知识整理 - 并发控制（封锁、两段锁协议、意向锁）
https://blog.csdn.net/Ha1f_Awake/article/details/84994697

配合MIT 6.830 Lab，加强理解

两种基本封锁类型
1）排他锁（exclusive locks，X锁）：
2）共享锁（share locks，S锁）：

封锁协议
1）一级封锁协议
2）二级封锁协议
3）三级封锁协议

两段锁协议
为了保证并发调度的正确性，DBMS的并发控制机制必须提供一定的手段来保证调度是可串行化的。
目前DBMS普遍采用两段锁协议（TwoPhase Locking，2PL）来实现，所有事务遵守两段锁协议是可串行化调度的充分条件，但不是必要条件。
两段锁的含义：
1）第一阶段（扩展阶段）：所有事务对数据加锁，但不能解锁；
2）第二阶段（收缩阶段）：所有事务对数据解锁，但不能加锁。
需要注意的是，不同事务对同一数据的加锁仍遵循两种锁的特性以及封锁协议。
预防死锁的一次封锁法遵守两段锁协议；但是两段锁协议并不要求事务必须一次将所有要使用的数据全部加锁，因此遵守两段锁协议的事务可能发生死锁。

意向锁
对任何一个结点加锁时，必须先对它的上层结点加意向锁。
三种常用的意向锁：
1）意向共享锁（IS锁）
2）意向排他锁（IX锁）
3）共享意向排他锁（SIX = S+IX锁）

锁的强度
锁的强度是指它对其他锁的排斥程度。
一个事务在申请封锁时，以强锁代替弱锁是安全的，反之不然。
强度排序：
X > SIX > S / IX > IS

https://github.com/duanjunxiao/Note-1/blob/master/doc/database/01-MySQL-Lock.md

行锁 表锁
锁，不同的存储引擎，锁不同

显示判断锁
for update  排他锁

in share mod


InnoDB 支持 `多粒度锁（multiple granularity locking）`，它允许 `行级锁`与 `表级锁`共存，而意向锁就是其中的一种 `表锁`。

https://juejin.cn/post/6844903666332368909


Thus, intention locks do not block anything except full table requests (for example, `LOCK TABLES ... WRITE`). The main purpose of `<i>IX</i>` and `<i>IS</i>` locks is to show that someone is locking a row, or going to lock a row in the table.

https://www.zhihu.com/question/51513268/answer/34



需要强调一下，意向锁是一种 `不与行级锁冲突表级锁`，这一点非常重要。意向锁分为两种：
* 意向共享锁 （intention shared lock, IS）：事务有意向对表中的某些行加 共享锁 （S锁）

```
  -- 事务要获取某些行的 S 锁，必须先获得表的 IS 锁。
  SELECT column FROM table ... LOCK IN SHARE MODE;
```
* 意向排他锁 （intention exclusive lock, IX）：事务有意向对表中的某些行加 排他锁 （X锁）

```
  -- 事务要获取某些行的 X 锁，必须先获得表的 IX 锁。
  SELECT column FROM table ... FOR UPDATE;
```

https://juejin.cn/post/6844903666332368909

意向锁是 放置在资源层次结构的一个级别上的锁，以保护较低级别资源上的共享锁或排它 。 例如，在SQL Server 2000 数据库引擎任务应用表内的共享或排它行锁之前，在该表上放置意向锁。 如果另一个任务试图在该表级别上应用共享或排它锁，则受到由第一个任务控制的表级别意向锁的阻塞。

目 的：保护较低级别资源上的共享
简 介： 在资源层次结构的一个级别上的锁
外文名：Intention Lock

InnoDB的并发控制，锁，事务模型

[InnoDB并发如此高，原因竟然在这 架构师之路](https://mp.weixin.qq.com/s?__biz=MjM5ODYxMDA5OQ==&mid=2651961444&idx=1&sn=830a93eb74ca484cbcedb06e485f611e&chksm=bd2d0db88a5a84ae5865cd05f8c7899153d16ec7e7976f06033f4fbfbecc2fdee6e8b89bb17b&scene=21#wechat_redirect)

[innodb-locking](https://dev.mysql.com/doc/refman/5.7/en/innodb-locking.html)

root数据常驻内存

Treenode

isRoot()
pre
next
Children[]
isLeaf()

![B+ Tree](../../imgs/mysql/bplustree.png)

推荐的书籍太多了。除了几本业内的神书外，姜老师的书也非常推荐大家食用，还有就是阿里的数据库月报。

http://dimitrik.free.fr/blog/index.html

B+树 java实现
github.com/edidada/testalgorithm

所有的树结构都有Node
B+树
插入 更新 删除 查找效率平衡

innodb默认的页大小是16kb

各种索引实现

组合索引
