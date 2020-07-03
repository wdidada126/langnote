# 高性能MySQL

[高性能MySQL豆瓣链接](https://book.douban.com/subject/23008813/)



https://www.jianshu.com/p/52ffbadf6b12





1、基于测试结果 进行性能提高

2、数据库 值类型优化

3、使用索引

4、查询优化

5、服务器设置

6、os 硬件优化

7、高可用 主从 避免单点失效



mysql 历史

2010 5.5

innodb

5.6

5.7

8.0



<<<<<<< HEAD
=======
explain 解释 说明

>>>>>>> afe522da082020e5ece0b75c43067644b2edb768


MySQL-8.0执行器及其改进
https://cloud.tencent.com/developer/article/1461353





MySQL Internals Manual.pdf

Understanding Mysql Internals(老外写的MySQL核心内幕).pdf

MySQL核心内幕(国人写的).pdf

MySQL技术内幕InnoDB存储引擎.pdf







### Chap. 1 连接器





mysql的内部架构



连接器

一个连接有一个线程

线程池 线程重用



死锁

事务日志

事务是由存储引擎实现的



mysql server 服务器层也实现表锁

select  ... lock in share mode

select ... for update



mysql 事务性数据引擎实现的都不是简单的行级锁，提升并发，使用mvcc

oracle pgsql 都实现了mvcc

可以认为mvcc是行级锁的一个变种




#### 1.5  schema 与数据类型优化
windows

mysql新建一个数据库

D:\mysql-5.7.17-winx64\data

新建一个文件夹，文件夹名称是数据库名称



数据字典保存在 .frm文件中





数据库 schema

performance_schema



### Chap.2 

sysbench





### Chap.4 schema 与数据类型优化



 

### Chap. 5 index



前缀索引和索引选择性

聚簇索引



### Chap. 9

硬件



### Chap. 12

HA

提升平均失效时间（mtbf）

降低平均恢复时间（mttr）



### Chap. 13

Cloud & MySQL



15.3.4 存储引擎和一致性



索引和实际的数据是分开的，只不过是用索引指向了实际的数据，这种索引就是所谓的非聚集索引

