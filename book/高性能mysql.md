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

execute plan 执行计划




MySQL-8.0执行器及其改进
https://cloud.tencent.com/developer/article/1461353





MySQL Internals Manual.pdf
Understanding Mysql Internals(老外写的MySQL核心内幕).pdf
MySQL核心内幕(国人写的).pdf
MySQL技术内幕InnoDB存储引擎.pdf


show variables xxx
都有哪些变量




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

mysql，提到事务，最先想到innodb存储引擎


mysql server 服务器层也实现表锁

select  ... lock in share mode
select ... for update



mysql 事务性数据引擎实现的都不是简单的行级锁，提升并发，使用mvcc



oracle pgsql 等rdbms都实现了mvcc


rdbms和nosql的区别包括事务支持与否

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


.idb
索引 数据保存在哪儿？ .ibd





[mysql之frm,MYD,MYI.idb,par文件说明](https://www.cnblogs.com/jdbeyond/p/11373802.html)

如数据库a，表b。
1、如果表b采用MyISAM，data\a中会产生3个文件：
b.frm ：描述表结构文件，字段长度等
b.MYD(MYData)：数据信息文件，存储数据信息(如果采用独立表存储模式)
b.MYI(MYIndex)：索引信息文件。
2、如果表b采用InnoDB，data\a中会产生1个或者2个文件：
b.frm ：描述表结构文件，字段长度等
如果采用独立表存储模式，data\a中还会产生b.ibd文件（存储数据信息和索引信息）
如果采用共存储模式的，数据信息和索引信息都存储在ibdata1中
如果采用分区存储，data\a中还会有一个b.par文件（用来存储分区信息）







### mysql之 共享表空间与独立表空间

https://blog.csdn.net/zhang123456456/article/details/72802056



独立表空间：
在配置文件（my.cnf）中设置： innodb_file_per_table 为 On



数据库 schema

performance_schema



### Chap.2 mysql基准测试

sysbench

千金良方：MySQL性能优化金字塔法则.pdf
上有例子



### Chap.3 服务器性能剖析



*sysbench*压力测试工具简介: *sysbench*是一个开源的、模块化的、跨平台的多线程性能测试工具,可以用来进行CPU、内存、磁盘I/O、线程、数据库的性能测试。

https://github.com/akopytov/sysbench


### Chap.4 schema 与数据类型优化



 

### Chap. 5 index

hint表达式可以指定索引

前缀索引和索引选择性

聚簇索引





### Chap. 6 查询性能优化


MVCC

MVCC 不是mvvc，mvvc是前端的概念

mvcc对应的是lock base version control


mvcc 加了三个隐藏的字段 

事务id roll指针 行id

1.DB_TRX_ID：一个6byte的标识，每处理一个事务，其值自动+1
下面提到的“创建时间”和“删除时间”记录的就是这个DB_TRX_ID的值
如insert、update、delete操作时，删除操作用1个bit表示。 
DB_TRX_ID是最重要的一个，可以通过语句“show engine innodb status”来查找 
2.DB_ROLL_PTR: 大小是7byte,指向写到rollback segment（回滚段）的一条undo log记录
（update操作的话，记录update前的ROW值）
3.DB_ROW_ID: 大小是6byte,该值随新行插入单调增加。
当由innodb自动产生聚集索引时聚集索引(即没有主键时,因为MYSQL默认聚簇表,会自动生成一个ROWID)
包括这个DB_ROW_ID的值，
不然的话聚集索引中不包括这个值,这个用于索引当中。

### 第7章 mysql 高级特性

### 第8章 优化服务器设置


### Chap. 9 操作系统和硬件优化



https://www.cnblogs.com/zzq-include/p/13532019.html

### Chap. 9

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





SQL Sever索引类型有：唯一索引，主键索引，聚集索引，非聚集索引。
MySQL 索引类型有：唯一索引，主键（聚集）索引，非聚集索引，全文索引。
聚集（clustered）索引，也叫聚簇索引。
> 定义：数据行的物理顺序与列值（一般是主键的那一列）的逻辑顺序相同，一个表中只能拥有一个聚集索引。



非聚集（unclustered）索引。

> 定义：该索引中索引的逻辑顺序与磁盘上行的物理存储顺序不同，一个表中可以拥有多个非聚集索引。
spatial index

https://cloud.tencent.com/developer/news/199266
MySQL5.7对于GIS进行了大幅重构和优化，InnoDB引擎原生支持地理空间数据类型，内部通过R-树来实现空间索引。MySQL5.7还提供了原生的st_geohash函数，可将地理空间坐标转化为Geohash格式，通过SPATIAL KEY添加空间索引。
优点：5.7新版功能，未来值得期待
缺点：数据库版本升级较复杂，对于现有业务系统来讲是个巨大的挑战。另外对于大数据量下的空间索引支持有待线上系统检验。
API：http://mysqlserverteam.com/mysql-5-7-and-gis-an-example/