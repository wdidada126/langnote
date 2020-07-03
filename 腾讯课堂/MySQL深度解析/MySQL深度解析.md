# MySQL深度解析



腾讯课堂 马士兵

https://ke.qq.com/course/465858#term_id=101680006



mysql四层



连接器 ----->>  控制用户的连接 ---------------  两个问题

分析器 ----->>  词法分析 语法分析 --------------- calcite 开源框架

优化器 ----->>  优化sql语句，规定执行流程 --------------- 1、cbo 2、rbo。查看sql执行计划

执行器 ----->>  SQL语句的实际执行组件 --------------- 跟执行引擎io 问题3 



备注：mysql8 移除了缓存，缓存命中率低 低版本 常量表数据可以放缓存



再下面就是

存储引擎：不同的存放位置，不同的文件格式



问题：mysql -uroot -p

连接器



问：能查看链接数个数吗？

`show processlist;`



问题3:为什么不用select *

当年房即可被问到了

覆盖索引 耗内存 回表



show engines



innode

myasd

memory





集群 nbd



存储引擎插件架构

innodb



frm myd myi



myd data

myi index



视频39min innodb myasam 区别



NDBCluster





提锁，一定要提存储引擎



共享锁

排他锁

独占锁

自增锁

间隙锁



表锁   页锁

行锁



加锁之后，还能加锁吗？



意向锁

面试问的问题，工作中用不到



原子性 持久性 依赖日志



日志的分类：

redo innode

undo innodb

binlog  sever层

慢查询日志 





一致性锁定读

一致性非锁定读



ACID



非一致性的例子？



mvcc 多版本并发控制

不是mvvc

事务隔离级别



脏读

幻读

不可重复读

举例



redis

rdb

aof 文件格式

string hash string set zset geoip？

如何实现

c写的

关键名词不能说错



### 原子性实现原理

undolog



undolog --mvcc



undolog



delete 记录一条insert



一个页面

针对页面的一行积累 逻辑日志

整个页全都记录 物理日志

逻辑日志 

物理日志



undolog逻辑日志

redolog物理日志



binlog三种格式

row mix 



扇区 512字节

页 逻辑概念 4k 8k 16k

innodb是16k



innodb ibd





https://blog.csdn.net/sryan/article/details/80278885





### 持久性原理：redolog

用生活中记账的例子来理解redolog 白板临时账 章三消费xx元 白板满了 持久化到磁盘

WAL write ahead log 预写日志

redolog 新数据写进日志 日志持久化

事务没有持久化，数据可以根据redolog持久化 





kafka zero copy



innodb_flush_log_at_trx_commit

默认是1

工作中可能设置成2



mysql 隔离级别



读微提交

读已提交





脏读

幻读

不可用幅度



演示

对概念进一步理解



隔离型的实现原理 锁

读锁/写锁

共享锁/排除锁 跟存储引擎有关





innodb一定加的是行锁吗？

默认是表锁

支持表锁 行锁



局促索引 6字节 rowid



for update

lock in share module



如何演示思索



排他锁 共享锁 兼容性



​                排他锁          共享锁

排他锁   错                    错

共享锁  错                   对 





deadlock



间隙锁

区间锁

其他区间不加锁



间隙锁 退化为行锁



高性能mysql



除了锁可以实现并发控制，还有其他技术：

基于时间戳的并发控制

基于时效性检查的并发控制

基于快照的并发控制





一致性非锁定度 默认

一致性锁定读





索引的数据结构

索引的分类

索引的技术名词

回表

最左匹配

索引覆盖

索引下推



索引的优化





mysql数据结构选择

假设有1T的数据，肯定不能直接放到内存

涉及到磁盘的存储



sql like between 范围查询



1T大数据量 内存相对小 选一部分













索引是什么？

索引是帮助mysql高效获取数据的数据结构

索引存储在文件系统中 备注：索引的跟节点

索引的文件存储形式与存储引擎有关

索引文件的结构

hash 二叉树

b数

b+数



memory hash 实现索引



bst  ---- avl树 发明人名字缩写





减少io的方法

减少io次数

减少io的数据量





为什么索引用b+树

二叉树 bst avl b tree b+ tree



innodb myasim 索引存储不一样





主键索引

辅助索引

唯一索引

全文索引

组合索引



辅助索引

叶子结点存储的是主键值



回表



查询了2个B+树 4次IO



id name age

id 主键

name 辅助索引



select age from table wjhere name = zhangsan

select id from table wjhere name = zhangsan      --- 覆盖索引



覆盖索引也叫索引覆盖

使用辅助索引进行查找时，叶子结点刚好保存的是查询的字段



查询计划看到useing index condition



最左匹配原则



组合索引

id ，name age sex

（name age）

1、 select id name age sex frpm table where name = ？ and age = ?

2、 select id name age sex frpm table where name = ？

3、 select id name age sex frpm table where age = ?

4、 select id name age sex frpm table where age = ？ and name = ?



1 2 4 and 优化器





索引下推



icp

谓词下推





