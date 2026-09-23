# 高性能MySQL

[高性能MySQL 第三版豆瓣链接](https://book.douban.com/subject/23008813/)
mysql 5.5
现在
8
5.6
5.7

Windows电脑
高性能MySQL（第3版）.pdf

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

#### 1.5 schema与数据类型优化
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
a.frm ：描述表结构文件，字段长度等
a.MYD(MYData)：数据信息文件，存储数据信息(如果采用独立表存储模式)
a.MYI(MYIndex)：索引信息文件。
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

sysbench压力测试工具简介: sysbench是一个开源的、模块化的、跨平台的多线程性能测试工具,可以用来进行CPU、内存、磁盘I/O、线程、数据库的性能测试。

https://github.com/akopytov/sysbench


### Chap.4 schema与数据类型优化

 

### Chap. 5 index

hint表达式可以指定索引

前缀索引和索引选择性

聚簇索引
聚簇索引是一种数据的存储方式，它描述的是数据的一种存储方式。
在InnoDB中，数据以B+Tree的形式存储，聚簇索引的数据行都存储在索引的叶子节点中，非叶子节点上只存索引信息。
这种索引和数据的存储方式就叫做聚簇索引，“聚簇”的意思是数据行和相邻的关键字挨着。
InnoDB通过主键来聚集数据，聚簇索引的B+Tree上的叶子结点所存储的key总是主键，如果没有定义主键，InnoDB会选择一个唯一的非空索引代替，如果没有这样的索引，InnoDB会隐式地定义一个主键来聚集（存储）数据，这个隐式的主键被称为rowID。

聚簇索引也叫簇类索引，是一种对磁盘上实际数据重新组织以按指定的一个或多个列的值排序。由于聚簇索引的索引页面指针指向数据页面，所以使用聚簇索引查找数据几乎总是比使用非聚簇索引快。每张表只能建一个聚簇索引，并且建聚簇索引需要至少相当该表120%的附加空间，以存放该表的副本和索引中间页。

mysql表默认使用聚簇索引
如果没有主键，mysql表会新建一个影藏列

非聚簇索引
聚簇索引的叶子节点就是数据节点，而非聚簇索引的叶子节点仍然是索引节点，只不过有指向对应数据块的指针。

1. 聚集索引（聚簇索引）：以innodb作为存储引擎的表，表中的数据都会有一个主键，即使你不创建主键，系统也会帮你创建一个隐式的主键。这是因为innodb是把数据存放在B+树中的，而B+树的键值就是主键，在B+树的叶子节点中，存储了表中所有的数据。这种以主键作为B+树索引的键值而构建的B+树索引，我们称之为聚集索引。 
2. 非聚集索引（非聚簇索引）：以主键以外的列值作为键值构建的B+树索引，我们称之为非聚集索引。非聚集索引与聚集索引的区别在于非聚集索引的叶子节点不存储表中的数据，而是存储该列对应的主键，想要查找数据我们还需要根据主键再去聚集索引中进行查找，这个再根据聚集索引查找数据的过程，我们称为回表。

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
定义：该索引中索引的逻辑顺序与磁盘上行的物理存储顺序不同，一个表中可以拥有多个非聚集索引。
spatial index

https://cloud.tencent.com/developer/news/199266
MySQL5.7对于GIS进行了大幅重构和优化，InnoDB引擎原生支持地理空间数据类型，内部通过R-树来实现空间索引。MySQL5.7还提供了原生的st_geohash函数，可将地理空间坐标转化为Geohash格式，通过SPATIAL KEY添加空间索引。
优点：5.7新版功能，未来值得期待
缺点：数据库版本升级较复杂，对于现有业务系统来讲是个巨大的挑战。另外对于大数据量下的空间索引支持有待线上系统检验。
API：http://mysqlserverteam.com/mysql-5-7-and-gis-an-example/
## 跨年摘录（2020–2026 日常笔记聚合，2026-09-23 整理）

### 2020-12
> 《高性能Mysql》


## 精读补写（系统整理，2026-09-23）

### 版本与 ISBN
- **《高性能 MySQL（第 4 版）》**（*High Performance MySQL, 4th ed.*，Silvia Botros、Jeremy Tinley 著，宁海元、周振兴、张新铭 译），电子工业出版社，2022-10，**ISBN `978-7-121-44257-5`**（344 页，¥100）。第 4 版以 **MySQL 8.0 + 云环境 + 可靠性工程**为主线，新增云端 MySQL、合规性、Kubernetes 部署等章节。
- 前作：第 3 版（2013，Baron Schwartz 等，中文 ISBN `978-7-121-19112-1`）仍是许多调优经验的出处，但**复制、优化器与云化内容已大幅过时**，笔记引用时须注明版本。

### 主线脉络
**架构**（连接管理、解析器/优化器、存储引擎、并发控制与锁）→ **监控**（Performance Schema、可靠性工程视角的指标）→ **操作系统与硬件优化**（CPU/内存/存储/文件系统/网络）→ **服务器设置优化**（缓冲池、日志、IO 配置）→ **Schema 设计与管理**（数据类型选择、范式与反范式、在线 DDL）→ **索引**（B+Tree、聚簇/二级索引、覆盖索引、联合索引最左前缀、索引选择性）→ **查询性能优化**（慢查询、EXPLAIN、优化器成本模型、重写查询）→ **复制**（binlog 格式、GTID、半同步、组复制、延迟与故障切换）→ **备份与恢复**（逻辑/物理备份、PITR）→ **扩展**（读写分离、分库分表、中间件、缓存）→ **云端 MySQL** → **合规性**。

### 经典论文与原始文献根基
- **Bayer & McCreight**《Organization and Maintenance of Large Ordered Indices》(1972)——B+ 树索引的理论来源，InnoDB 索引结构的基础。
- **Mohan 等《ARIES: A Transaction Recovery Method》**(TODS 1992)——**WAL 与崩溃恢复**；InnoDB 的 redo log / undo log / checkpoint 与 doublewrite 均可视为 ARIES 的工程实现。
- **Jim Gray & Reuter《Transaction Processing: Concepts and Techniques》**(1993)——事务、隔离级别与两阶段锁（2PL）的经典体系；MySQL InnoDB 的 MVCC 与隔离级别（RR/RC）由此理解。
- **Bernstein & Hadzilacos & Goodman《Concurrency Control and Recovery in Database Systems》**(1987)——可恢复性与隔离性的形式化基础。
- 工程文献：Facebook《Online Schema Change》(2010) 与 `gh-ost`(GitHub, 2016)——在线 DDL 的现实方案；Google/Facebook 关于 row-based replication 一致性的实践文章。

### 最新研究与产业进展
- **MySQL 8.0 重要能力**：原子 DDL(8.0)、直方图统计(8.0.2+)、CTE 与窗口函数、不可见索引、资源组、Clone Plugin、EXPLAIN ANALYZE 与 `EXPLAIN FORMAT=JSON`、并行扫描改进、JSON 多值索引(8.0.17+)。
- **版本节奏变化**：**8.4 LTS（2024）成为新的长期支持主线**，随后是 9.x 创新版（2024-2025）；升级时应区分 LTS 与创新版的定位差异，并注意 8.4 起若干默认参数与权限模型的变化。
- **Oracle 方向**：MySQL **HeatWave**（列存 + 向量检索 + 生成式 AI 能力，2023 起持续增强）把 OLTP/OLAP/向量检索合并到同一服务，是官方最重要的新形态。
- **生态分支与替代**：MariaDB、Percona Server；国产与云原生方向 **PolarDB**（共享存储一写多读）、**Aurora**（日志即数据库）、**TiDB**（HTAP + Raft）、**OceanBase**。
- 运维现代化：Performance Schema + `sys` schema + `pt-*` 工具链；**可观测性转向 OpenTelemetry/Prometheus**，与书中以 `SHOW STATUS`/慢日志为中心的方法互补。

### 常见误区 / 纠错
- **"分库分表是性能银弹"错误**：正确顺序是**优化索引与 SQL → 优化参数与硬件 → 读写分离/缓存 → 最后才考虑分片**；分片会带来分布式事务、跨片查询与运维复杂度的数量级增长。
- **最左前缀与索引下推**：MySQL 5.6+ 的 **ICP（Index Condition Pushdown）**、MRR、BKA 改变了联合索引的行为，不能只按最左前缀机械判断；应结合 `EXPLAIN` 的 `Using index condition` 等字段解读。
- **"count(*) 一定慢"需分情况**：取决于引擎（MyISAM vs InnoDB）、是否有合适的小索引、以及 8.0 的并行扫描改进；应实测而非照搬结论。
- **"MySQL 8 移除了查询缓存"**：查询缓存（Query Cache）在 **5.7 弃用、8.0 彻底移除**，调优笔记中若仍建议"开启 query cache"须删除；替代方案是应用层/中间件缓存（Redis）或 Proxy 层缓存。
