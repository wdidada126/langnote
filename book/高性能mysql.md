# 高性能MySQL

[高性能MySQL 第三版豆瓣链接](https://book.douban.com/subject/23008813/)
mysql 5.5
现在
8
5.6
5.7



Baron Schwartz  https://www.xaprb.com/blog/
https://www.jianshu.com/p/52ffbadf6b12


Peter Zaitsev，曾经是MySQLAB公司高性能来组的经理，目前源在运作 baimysqlperformanceblog.com



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




explain 解释 说明
show profile
需要百度例子，做实验


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
myasma 不支持事务
innodb实现事务


mysql server 服务器层也实现表锁

select  ... lock in share mode
select ... for update



mysql 事务性数据引擎实现的都不是简单的行级锁，提升并发，使用mvcc
oracle pgsql 都实现了mvcc
可以认为mvcc是行级锁的一个变种
mvcc没有规范，不同数据库厂商自己实现



#### 1.5  schema 与数据类型优化
windows

mysql新建一个数据库

D:\mysql-5.7.17-winx64\data

新建一个文件夹，文件夹名称是数据库名称



数据字典保存在 .frm文件中
ibd保存数据，索引
innodb不支持hash索引




数据库 schema

performance_schema



### Chap.2 mysql基准测试

sysbench

### Chap.3 服务器性能剖析



### Chap.4 schema 与数据类型优化



 

### Chap. 5 index



前缀索引和索引选择性

聚簇索引





### Chap. 6 查询性能优化

MVCC

加了三个字段 隐藏的


### 第7章 mysql 高级特性

### 第8章 优化服务器设置

### Chap. 9 操作系统和硬件优化

硬件

### 第10章 复制


### 第11章 可扩展的mysql

### Chap. 12 高可用性
HA

提升平均失效时间（mtbf）
降低平均恢复时间（mttr）



### Chap. 13 云端的mysql

Cloud & MySQL

### 第14章 应用层优化

### 第15章 备份与恢复

15.3.4 存储引擎和一致性



索引和实际的数据是分开的，只不过是用索引指向了实际的数据，这种索引就是所谓的非聚集索引

