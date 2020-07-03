# MySQL实战45讲

林晓斌

https://time.geekbang.org/column/intro/100020801



widnows电脑上

一共45讲



核心概念/专有名词

两阶段锁协议 

覆盖索引 coving index

WAL

redo log

bin log



在整个专栏里面，我们的例子中如果没有特别说明，都是默认autocommit=1。

#### 01 基础架构



![MySQL基础架构](imgs/mysql_45_archi.png)



连接器

查询缓存  8.0开始彻底没有这个功能了

分析器

优化器

执行器





select * from T where k=1 报错k列不存在 分析器报错的



##### 02 日志系统



重要的日志模块：redo log

重要的日志模块：binlog

两阶段提交





##### 03讲事务隔离

当数据库上有多个事务同时执行的时候，就可能出现脏读（dirty read）、不可重复读（non-repeatable read）、幻读（phantom read）的问题，为了解决这些问题，就有了“隔离级别”的概念。

读未提交（read uncommitted）、读提交（read committed）、可重复读（repeatable read）和串行化（serializable ）

事务隔离的实现

事务的启动方式

##### 04讲深入浅出索引（上）



InnoDB索引的数据结构模型

索引的常见模型

三种常见、也比较简单的数据结构，它们分别是哈希表、有序数组和搜索树

有序数组索引只适用于静态存储引擎

InnoDB 的索引模型

B+树能够很好地配合磁盘的读写特性，减少单次查询的磁盘访问次数。

create table T ( ID int primary key, k int NOT NULL DEFAULT 0,  s varchar(16) NOT NULL DEFAULT '', index k(k)) engine=InnoDB;

insert into T values(100,1, 'aa'),(200,2,'bb'),(300,3,'cc'),(500,5,'ee'),(600,6,'ff'),(700,7,'gg');

select * from T where k between 3 and 5;

覆盖索引

如果执行的语句是select ID from T where k between 3 and 5，这时只需要查ID的值，而ID的值已经在k索引树上了，因此可以直接提供查询结果，不需要回表。也就是说，在这个查询里面，索引k已经“覆盖了”我们的查询需求，我们称为覆盖索引。

由于覆盖索引可以减少树的搜索次数，显著提升查询性能，所以使用覆盖索引是一个常用的性能优化手段。

`CREATE TABLE `tuser` (  `id` int(11) NOT NULL,  `id_card` varchar(32) DEFAULT NULL,  `name` varchar(32) DEFAULT NULL,  `age` int(11) DEFAULT NULL,  `ismale` tinyint(1) DEFAULT NULL,  PRIMARY KEY (`id`),  KEY `id_card` (`id_card`),  KEY `name_age` (`name`,`age`) ) ENGINE=InnoDB;`

问：再建立一个（身份证号、姓名）的联合索引，是不是浪费空间？

如果现在有一个高频请求，要根据市民的身份证号查询他的姓名，这个联合索引就有意义了。它可以在这个高频请求上用到覆盖索引，不再需要回表查整行记录，减少语句的执行时间。
###### 5 索引下
最左前缀原则

name字段是比age字段大的 ，那我就建议你创建一个（name,age)的联合索引和一个(age)的单字段索引。

索引下推

##### 06讲 全局锁和表锁：给表加个字段怎么有这么多阻碍
根据加锁的范围，MySQL里面的锁大致可以分成全局锁、表级锁和行锁三类。

全局锁的典型使用场景是，做全库逻辑备份。也就是把整库每个表都select出来存成文本。

##### 表级锁

MySQL里面表级别的锁有两种：一种是表锁，一种是元数据锁（meta data lock，MDL)。

表锁的语法是 lock tables … read/write。

另一类表级的锁是MDL（metadata lock)。

##### 07讲 行锁功过：怎么减少行锁对性能的影响

从两阶段锁说起

在InnoDB事务中，行锁是在需要的时候才加上的，但并不是不需要了就立刻释放，而是要等到事务结束时才释放。这个就是两阶段锁协议。



死锁和死锁检测

一种头痛医头的方法，就是如果你能确保这个业务一定不会出现死锁，可以临时把死锁检测关掉。

另一个思路是控制并发度

##### 08讲 事务到底是隔离的还是不隔离的

在整个专栏里面，我们的例子中如果没有特别说明，都是默认autocommit=1。


##### 09讲 普通索引和唯一索引，应该怎么选择

change buffer 和 redo log

https://www.cnblogs.com/jamaler/p/12371205.html





##### 10讲 MySQL为什么有时候会选错索引



explain

显示结果的含义



mysql自动选择索引

#### 11讲 怎么给字符串字段加索引



邮箱字段加索引

**使用前缀索引，定义好长度，就可以做到既节省空间，又不用额外增加太多的查询成本。**





前缀索引对覆盖索引的影响



show engines;查看mysql支持的存储引擎

show variables like '%storage_engine%';

查看默认的存储引擎





InnoDB的行锁是针对索引加的锁，不是针对记录加的锁。并且该索引不能失效，否则都会从行锁升级为表锁。索引失效的原因



