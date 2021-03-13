# mysql

MySQL Benchmark Tool
DBT2
SysBench
flexAsynch


05 如何设计高性能的索引

ICP（index condition pushdown）

https://blog.csdn.net/bruce_6/article/details/84997708



MySQL查看和修改事务隔离级别
http://c.biancheng.net/view/7266.html


mysql doc 5.7 中英文版本
https://www.docs4dev.com/docs/zh/mysql/5.7/reference/innodb-benefits.html
没找到索引相关的，看英文原文


mysql 5.0中文翻译
QQ:362606856
http://www.deituicms.com/mysql8cn/cn/web.html



gitbook
https://github.com/mowangjuanzi/mysql-chinese-doc

https://github.com/shlomi-noach/awesome-mysql
https://github.com/jobbole/awesome-mysql-cn
https://github.com/tmcallaghan/iibench-mysql

http://lists.mysql.com/


mysql> select str_to_date('2016-09-09 15:43:28','%Y-%m-%d %H:%i:%s');
+--------------------------------------------------------+
| str_to_date('2016-09-09 15:43:28','%Y-%m-%d %H:%i:%s') |
+--------------------------------------------------------+
| 2016-09-09 15:43:28                                    |
+--------------------------------------------------------+
1 row in set (0.01 sec)

mysql> select date_format(now(), '%Y-%m-%d %h:%i:%s');
+-----------------------------------------+
| date_format(now(), '%Y-%m-%d %h:%i:%s') |
+-----------------------------------------+
| 2021-01-21 04:28:13                     |
+-----------------------------------------+
1 row in set (0.01 sec)



Mysql中字符串互转时间类型,date_format()和str_to_date()函数
字符串 日期对象相互转换

https://blog.csdn.net/lyg1153/article/details/79755768

str_to_date()有两个参数？对
select str_to_date('2016-09-09 15:43:28','%Y-%m-%d %H:%i:%s');
select date_format(now(), '%Y-%m-%d %h:%i:%s');
2016-09-09 15:43:28
2021-01-25 04:26:40

附加：MySQL now()函数
now()函数是通用的
https://www.w3school.com.cn/sql/func_now.asp





SELECT function(列) FROM 表




SQL 函数
- SQL avg()       平均数
- SQL count() 计数
- SQL first() 首个
- SQL last() 最后一个 作用在cloumn_name上
- SQL max() 最大值
- SQL min() 最小值
- SQL sum() 求和
- SQL Group By 分组
- SQL Having 分组条件
- SQL ucase() 全部大写
- SQL lcase() 全部小写
- SQL mid() 
- SQL len()
- SQL round()
- SQL now()
- SQL format()



Mysql关键字和保留字 - 版本5.7
https://blog.csdn.net/qq_15071263/article/details/77985485


MySQL关键字大全
https://blog.csdn.net/benxiaohai888/article/details/77803090

MySQL Aggregate Functions and Grouping
Aggregate Functions and Grouping
AVG()
BIT_AND()
BIT_OR()
BIT_XOR()
COUNT()
GROUP_CONCAT()
MAX()
MIN()
STD()
STDDEV_POP()
STDDEV_SAMP()
STDDEV()
SUM()
VAR_POP()
VAR_SAMP()
VARIANCE()

https://www.w3resource.com/mysql/aggregate-functions-and-grouping/aggregate-functions-and-grouping-group_concat.php
https://www.educative.io/edpresso/what-is-the-groupconcat-function-in-mysql
https://mariadb.com/kb/en/group_concat/

内置函数 聚合函数
https://mariadb.com/kb/en/built-in-functions/
https://mariadb.com/kb/en/aggregate-functions/

不要光盯着mysql，关注下mariadb和percona等其他mysql分支

String相关函数
Date相关函数

李春 mysql
maridb
XtraBackup和pt-Toolkits
innodb Oracle 收紧
用户返回的问题，test case，Oracle不反馈给社区



DB2 大型机
VLDB、SIGMOD
https://www.cnblogs.com/oxspirt/p/6208912.html
清华大学李国良教授写的"大数据下的数据管理领域研究体会"一文。
ICDE
PVLDB指的是VLDB会议论文集，被VLDB会议接受的论文，按期将会刊登在PVLDB中。VLDBJ则是VLDB基金会主管的期刊，其论文篇幅长，审稿周期长。
关于POLARDB的一篇论文《PolarFS： An Ultra-low Latency and Failure Resilient Distributed File System for Shared Storage Cloud Database》就被数据库顶级学术会议VLDB 2018接收
国际数据工程会议（International Conference on Data Engineering，简称ICDE）是全球范围内顶级三大数据 库学术会议之一



（1）*.frm--表定义，是描述表结构的文件。
（2）*.MYD--"D"数据信息文件，是表的数据文件。
（3）*.MYI--"I"索引信息文件，是表数据文件中任何索引的数据树。



ibd InnoDB存储数据的物理文件通常以ibd作为其文件名后缀

cvs

https://dev.mysql.com/doc/refman/8.0/en/explain.html
https://www.kancloud.cn/baoguoxiao0538/mysql-8-0-chinese-doc/1117563

mysql 存储过程 源码实现
.ibd

开启 general log 将所有到达MySQL Server的SQL语句记录下来。存储方式有两种，一种是file ，一种是table
一般不会开启开功能，因为log的量会非常庞大。但个别情况下可能会临时的开一会儿general log以供排障使用。 
相关参数一共有3：general_log、log_output、general_log_file

https://blog.csdn.net/intelrain/article/details/80451120

mysql 日志 查看select的结果


https://blog.csdn.net/qq_35254185/article/details/95341993



https://www.cnblogs.com/kerrycode/p/7130403.html

只有输入的sql，没有查询到的结果	



mysqlbinlog

两个最重要的使用场景: 
其一：MySQL Replication在Master端开启binlog，Mster把它的二进制日志传递给slaves来达到master-slave数据一致的目的。 
其二：自然就是数据恢复了，通过使用mysqlbinlog工具来使恢复数据。

二进制日志包括两类文件： 
二进制日志索引文件（文件名后缀为.index）用于记录所有的二进制文件； 
二进制日志文件（文件名后缀为.00000*）记录数据库所有的DDL和DML(除了数据查询语句)语句事件。



show variables like 'log_bin';
general_log
general_log_file
log_output  FILE
slow_query_log
slow_query_log_file  D:\devtools\mysql-5.7.31-winx64\data\chengwu2-slow.log



高性能MySQL（第3版）
MySQLDBA修炼之道
MySQL王者晋级之路
MySQL运维内参：MySQL、Galera、Inception核心原理与最佳实践
MySQL技术内幕++InnoDB存储引擎（第二版）
MySQL5.7-官方文档

官网上能下载pdf版的，不建议直接读官方文档，怕大家扛不住！！！学到后期，你会发现很多知识网上不好找到了，这时官方文档的作用就出来了。建议都备着一份吧。



X Protocol
[MySQL 数据库的提速器-写缓存（Change Buffer）](https://www.cnblogs.com/jamaler/p/12371205.html)



mysql protocol
https://blog.csdn.net/caisini_vc/article/details/5356136



mysql 存储过程 函数

http://blog.sina.com.cn/s/blog_52d20fbf0100ofd5.html
https://blog.csdn.net/u011983531/article/details/67639678
https://blog.csdn.net/u013488847/article/details/53819976
http://www.cnblogs.com/xuanzhi201111/p/4175635.html



mysql select 查询时间测试



导入数据的方式
1 sql文件 在使用syslog导入
2 写存储过程



https://www.cnblogs.com/1175429393wljblog/p/5918150.html



生成插入数据库的sql备份文件



sqlyog
导出 导入脚本



https://blog.csdn.net/qq_20975027/article/details/78343972



命令行测试select查询效率



https://blog.csdn.net/weixin_37288522/article/details/79710909
https://blog.csdn.net/blueheart20/article/details/51007659



数据库图形工具



navicate 导入失败
sqlyog 数据库必须存在 导入sql文件



[MySQL 索引](https://zhuanlan.zhihu.com/p/90076968)



hash 索引
平衡树
b-树
b+树



根据红黑树的算法来分析TreeMap的实现
https://www.cnblogs.com/coderising/articles/5719517.html



二叉树是不是不能有重复的元素？
没有重复元素


二叉查找树 又叫 二叉排序树，二叉搜索树。Binary Search Tree(BST)

对于二叉查找树中的每一个节点如果存在左节点，左节点的值一定小于该节点的值
对于二叉查找树中的每一个节点如果存在右节点，右节点的值一定大于该节点的值
也就是说对于二叉查找树中的任何一个非叶子节点，左节点值小于当前节点值，右节点值大于当前节点值
二叉查找树的任何一个非叶子节点的左子树中的任何一个节点的值都要小于当前节点值，右子树中的任何一个节点的值都要大于当前节点值。
如果对二叉查找树进行中序遍历，可以得到一个从小到大的序列 ，所以也叫作二叉排序树







一、二叉树-BST  (binary search/sort tree)
二叉树又名二叉查找/搜索/排序树  
或者是一棵空树；
或者是具有下列性质的二叉树：
（1）若它的左子树不空，则左子树上所有结点的值均小于它的父结点的值；
（2）若它的右子树不空，则右子树上所有结点的值均大于它的父结点的值；
（3）它的左、右子树也分别为二叉排序树。

二、平衡二叉树（Self-balancing binary search tree）  
自平衡二叉查找树  又被称为AVL树（有别于AVL算法）  字母是发明者的名字
它是一棵空树或它的左右两个子树的高度差(平衡因子)的绝对值不超过1，并且左右两个子树都是一棵平衡二叉树，平衡二叉树必定是二叉搜索树，反之则不一定

平衡因子（平衡度）：平衡度为1，既每个结点的平衡因子都为 1、－1、0 的二叉排序树。或者说每个结点的左右子树的高度最多差1的二叉排序树。
平衡二叉树的目的是为了减少二叉查找树层次，提高查找速度
平衡二叉树的常用实现方法有AA树、AVL树、红黑树、树堆Treap、伸展树等

三、红黑树-R-B Tree，全称是Red-Black Tree
又称为“红黑树”，它一种平衡二叉树。红黑树的每个节点上都有存储位表示节点的颜色，可以是红(Red)或黑(Black)。
红黑树的特性:
（1）每个节点或者是黑色，或者是红色。
（2）根节点是黑色。
（3）每个叶子节点（NIL）是黑色。 [注意：这里叶子节点，是指为空(NIL或NULL)的叶子节点！]
（4）如果一个节点是红色的，则它的子节点必须是黑色的。（不存在连续的两个红色节点
（5）从一个节点到该节点的子孙节点的所有路径上包含相同数目的黑节点。

注意：
(01) 特性(3)中的叶子节点，是只为空(NIL或null)的节点。
(02) 特性(5)，确保没有一条路径会比其他路径长出俩倍。因而，红黑树是相对是接近平衡的二叉树

B-树是一种多路搜索树（并不一定是二叉的）








单机 索引 实际操作



mysql连接池



下面对一些重要的数据字典表做一些说明：
SCHEMATA表：提供了关于数据库的信息。
TABLES表：给出了关于数据库中的表的信息。
COLUMNS表：给出了表中的列信息。
STATISTICS表：给出了关于表索引的信息。
USER_PRIVILEGES表：给出了关于全程权限的信息。该信息源自mysql.user授权表。
SCHEMA_PRIVILEGES表：给出了关于方案（数据库）权限的信息。该信息来自mysql.db授权表。
TABLE_PRIVILEGES表：给出了关于表权限的信息。该信息源自mysql.tables_priv授权表。
COLUMN_PRIVILEGES表：给出了关于列权限的信息。该信息源自mysql.columns_priv授权表。
CHARACTER_SETS表：提供了关于可用字符集的信息。
COLLATIONS表：提供了关于各字符集的对照信息。
COLLATION_CHARACTER_SET_APPLICABILITY表：指明了可用于校对的字符集。
TABLE_CONSTRAINTS表：描述了存在约束的表。
KEY_COLUMN_USAGE表：描述了具有约束的键列。
ROUTINES表：提供了关于存储子程序（存储程序和函数）的信息。此时，ROUTINES表不包含自定义函数（UDF）。
VIEWS表：给出了关于数据库中的视图的信息。
TRIGGERS表：提供了关于触发程序的信息。



一个read commited下的死锁分析
http://blog.itpub.net/30221425/viewspace-2134433

max.connections.size.per.query=1

Mysql的XA事务分为外部XA和内部XA
https://blog.csdn.net/michaelwubo/article/details/81476591


Caused by: com.mysql.jdbc.exceptions.jdbc4.CommunicationsException: Communications link failure
The last packet sent successfully to the server was 0 milliseconds ago. The driver has not received any packets from the server.




Mysql Server的代码虽然多，但是比较好理解了，我看过下面这些



https://www.zhihu.com/question/22364529






线上业务先和DBA确认服务器磁盘是否是SSD

Mysql 为我们提供了分布式事务解决方案（https://dev.mysql.com/doc/refman/5.7/en/xa.html 这是mysql5.7的文档）
这里先声明两个概念：
资源管理器（resource manager）：用来管理系统资源，是通向事务资源的途径。数据库就是一种资源管理器。资源管理还应该具有管理事务提交或回滚的能力。
事务管理器（transaction manager）：事务管理器是分布式事务的核心管理者。事务管理器与每个资源管理器（resource
manager）进行通信，协调并完成事务的处理。事务的各个分支由唯一命名进行标识。

版权声明：本文为CSDN博主「唐大麦」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/soonfly/article/details/70677138





XA的性能很低。一个数据库的事务和多个数据库间的XA事务性能对比可发现，性能差10倍左右。因此要尽量避免XA事务，例如可以将数据写入本地，用高性能的消息系统分发数据。或使用数据库复制等技术。只有在这些都无法实现，且性能不是瓶颈时才应该使用XA。


MySQL XA 的限制
在MySQL 5.7.7 之前，MySQL一直存在一个"bug"。在事务达到PREPARED状态后，客户端断开与MySQL的连接，MySQL 会自动回滚该事务，这个行为不符合分布式事务的规范，MySQL将PREPARED的事务丢失了。之所以MySQL这么实现是因为MySQL 5.7.7 之前PREPARED的事务并不会记录到binlog中。客户端退出后会丢失该信息，如果允许再提交，那么binlog缺少事务信息，会造成主从不一致。

在MySQL 5.7.7 之后，MySQL 新增了一个XA_prepare_log_event的事件，会把xa start到xa prepare中间的操作记录到Binlog中。Slave读取Relay log 进行回放，当SQL Thread读取到PREPARED的事务后，在读取xa commit或者xa rollback前，会进行一个类似客户端断开的操作，继续读取后续的事务信息，不会阻塞SQL Thread的执行。从以上的结果看，Oracle在MySQL 5.7.7 上确实完美的解决了MySQL XA一直存在的一个"bug"。

MySQL XA 的实践
本人曾在某公司的分布式数据库项目组中实践过基于MySQL XA的分布式事务。MySQL XA 要满足线上高并发的访问要求，在使用时还需要解决两个问题：分布式死锁问题和分布式读一致性问题。分布式死锁问题是指MySQL Server 是可以检测和解决单个MySQL实例中的死锁问题，但涉及到跨越多个MySQL 实例的分布式事务时候，需要程序层面实现死锁的检测和解决。分布式读一致性问题是指MySQL的read view 也是实例级别的，对于全局分布式事务来说无法实现读一致，只能通过select ... lock in share mode在读请求上加锁的串行化隔离级别来实现，这必然会带来并发性能的下降。这就需要在程序层面构建全局的read view来实现全局的MVCC 。当然这两个问题，当时团队的大牛们都已经解决了，我也很有幸参与其中。


ddd：https://www.jianshu.com/p/7003d58ea182


MySQL书籍
http://mingxinglai.com/cn/2015/12/material-of-mysql/

http://blog.codinglabs.org/articles/theory-of-mysql-index.html

https://segmentfault.com/a/1190000012166738

```

查询Mysql最大连接数和当前连接数
最大连接数
`show variables like '%max_connections%'; `
当前连接数
`show full processlist;`
有多少条结果就有多少连接
[mysql: show processlist详解](https://zhuanlan.zhihu.com/p/30743094)

```

[MySQL查看 InnoDB表中每个索引的高度](https://www.cnblogs.com/waterystone/p/6638531.html)

[files-in-innodb-sources](https://dev.mysql.com/doc/internals/en/files-in-innodb-sources.html)

在select窗口中，执行以下语句：

set profiling =1; -- 打开profile分析工具
show variables like '%profil%'; -- 查看是否生效


+------------------------+-------+
| Variable_name          | Value |
+------------------------+-------+
| have_profiling         | YES   |
| profiling              | ON    |
| profiling_history_size | 15    |
+------------------------+-------+


show processlist; -- 查看进程
use cmc; -- 选择数据库
show PROFILE all; -- 全部分析的类型


+----------------+----------+----------+------------+-------------------+---------------------+--------------+---------------+---------------+-------------------+-------------------+-------------------+-------+-----------------------+--------------+-------------+
| Status         | Duration | CPU_user | CPU_system | Context_voluntary | Context_involuntary | Block_ops_in | Block_ops_out | Messages_sent | Messages_received | Page_faults_major | Page_faults_minor | Swaps | Source_function       | Source_file  | Source_line |
+----------------+----------+----------+------------+-------------------+---------------------+--------------+---------------+---------------+-------------------+-------------------+-------------------+-------+-----------------------+--------------+-------------+
| starting       | 0.000175 | 0.000000 | 0.000000   | NULL              | NULL                | NULL         | NULL          | NULL          | NULL              | NULL              | NULL              | NULL  | NULL                  | NULL         | NULL        |
| query end      | 0.000007 | 0.000000 | 0.000000   | NULL              | NULL                | NULL         | NULL          | NULL          | NULL              | NULL              | NULL              | NULL  | mysql_execute_command | sql_parse.cc |        4956 |
| closing tables | 0.000003 | 0.000000 | 0.000000   | NULL              | NULL                | NULL         | NULL          | NULL          | NULL              | NULL              | NULL              | NULL  | mysql_execute_command | sql_parse.cc |        5009 |
| freeing items  | 0.000035 | 0.000000 | 0.000000   | NULL              | NULL                | NULL         | NULL          | NULL          | NULL              | NULL              | NULL              | NULL  | mysql_parse           | sql_parse.cc |        5622 |
| cleaning up    | 0.000011 | 0.000000 | 0.000000   | NULL              | NULL                | NULL         | NULL          | NULL          | NULL              | NULL              | NULL              | NULL  | dispatch_command      | sql_parse.cc |        1931 |
+----------------+----------+----------+------------+-------------------+---------------------+--------------+---------------+---------------+-------------------+-------------------+-------------------+-------+-----------------------+--------------+-------------+


show index from t_log_account; ##查看某个表的索引
show index from t_car_copy; ##查看某个表的索引
-- 使用explain命令查看query语句的性能：
EXPLAIN select * from t_car_copy ; ##查看执行计划中的sql性能
EXPLAIN select * from t_car_copy where org_id = '3';
EXPLAIN select * from t_car_copy where 1=1 and org_id = '3';



```shell

 (B-TREE)


  File Name   What Name Stands For         Size     Comment Inside File
  ---------   --------------------         ------   -------------------
  btr0btr.c   B-tree / B-tree              82,400   B-tree
  btr0cur.c   B-tree / Cursor             103,233   index tree cursor
  btr0sea.c   B-tree / Search              41,788   index tree adaptive search
  btr0pcur.c  B-tree / persistent cursor   16,720   index tree persistent cursor

```


### sql语句执行返回值
insert，返回值是：新插入行的主键（primary key）；需要包含<selectKey>语句，才会返回主键，否则返回值为null。
update/delete，返回值是：更新或删除的行数；无需指明resultClass；但如果有约束异常而删除失败，只能去捕捉异常。


MySQL 添加列，修改列，删除列
ALTER TABLE：添加，修改，删除表的列，约束等表的定义。

查看列：desc 表名;
修改表名：alter table t_book rename to bbb;
添加列：alter table 表名 add column 列名 varchar(30);
删除列：alter table 表名 drop column 列名;
修改列名MySQL： alter table bbb change nnnnn hh int;
修改列名SQLServer：exec sp_rename't_student.name','nn','column';
修改列名Oracle：lter table bbb rename column nnnnn to hh int;
修改列属性：alter table t_book modify name varchar(22);
sp_rename：SQLServer 内置的存储过程，用与修改表的定义。


MySQL 查看约束，添加约束，删除约束 添加列，修改列，删除列

查看表的字段信息：desc 表名;
查看表的所有信息：show create table 表名;
添加主键约束：alter table 表名 add constraint 主键 （形如：PK_表名） primary key 表名(主键字段);
添加外键约束：alter table 从表 add constraint 外键（形如：FK_从表_主表） foreign key 从表(外键字段) references 主表(主键字段);
删除主键约束：alter table 表名 drop primary key;
删除外键约束：alter table 表名 drop foreign key 外键（区分大小写）;
修改表名：alter table t_book rename to bbb;
添加列：alter table 表名 add column 列名 varchar(30);
删除列：alter table 表名 drop column 列名;
修改列名MySQL： alter table bbb change nnnnn hh int;
修改列名SQLServer：exec sp_rename't_student.name','nn','column';
修改列名Oracle：alter table bbb rename column nnnnn to hh int;
修改列属性：alter table t_book modify name varchar(22);


mysql出现unblock with 'mysqladmin flush-hosts'
https://www.cnblogs.com/abclife/p/9469622.html

每个InnoDB表有一个特殊的指数称为聚集索引所在的行的数据存储。通常，聚集索引是主键的同义词。从查询，插入性能最好，和其他的数据库操作，必须了解InnoDB使用聚集索引来优化每个表最常见的查询和DML操作。 当你定义你的表的主键，InnoDB使用它作为聚集索引。为您创建的每个表定义一个主键。如果没有逻辑唯一的和非空的列或列集，添加一个新的自动增量列，它的值自动填充。 如果你不确定你的表的主键、唯一索引，MySQL定位第一所有键列不为空，InnoDB使用它作为聚集索引。 如果表没有主键或唯一索引InnoDB。

information_schema mysql元数据数据库 权限 密码 表引擎

面试题1 ：为什么用 B/B+ 树这种结构来实现索引呢？
红黑树等结构也可以用来实现索引，但是文件系统及数据库系统普遍使用 B/B+ 树结构来实现索引。MySQL 是基于磁盘的数据库，索引是以索引文件的形式存在于磁盘中的，索引的查找过程就会涉及到磁盘 IO 消耗，磁盘 IO 的消耗相比较于内存 IO 的消耗要高好几个数量级，所以索引的组织结构要设计得在查找关键字时要尽量减少磁盘 IO 的次数。为什么要使用 B/B+ 树，跟磁盘的存储原理有关。
这里，局部性原理与磁盘预读。为了提升效率，要尽量减少磁盘 IO 的次数。实际过程中，磁盘并不是每次严格按需读取，而是每次都会预读。磁盘读取完需要的数据后，会按顺序再多读一部分数据到内存中，这样做的理论依据是计算机科学中注明的局部性原理：当一个数据被用到时，其附近的数据也通常会马上被使用。程序运行期间所需要的数据通常比较集中。（1）由于磁盘顺序读取的效率很高(不需要寻道时间，只需很少的旋转时间)，因此对于具有局部性的程序来说，预读可以提高 I/O 效率.预读的长度一般为页(page)的整倍数。（2）MySQL(默认使用InnoDB引擎),将记录按照页的方式进行管理,每页大小默认为16K(这个值可以修改)。Linux 默认页大小为4K。
B-Tree 借助计算机磁盘预读的机制，并使用如下技巧：每次新建节点时，直接申请一个页的空间，这样就保证一个节点物理上也存储在一个页里，加之计算机存储分配都是按页对齐的，就实现了一个结点只需一次 I/O。假设 B-Tree 的高度为 h, B-Tree 中一次检索最多需要 h-1 次 I/O（根节点常驻内存），渐进复杂度为 O(h)=O(logdN)O(h)=O(logdN)。一般实际应用中，出度 d 是非常大的数字，通常超过 100，因此 h 非常小（通常不超过3，也即索引的 B+ 树层次一般不超过三层，所以查找效率很高）。而红黑树这种结构，h 明显要深的多。由于逻辑上很近的节点（父子）物理上可能很远，无法利用局部性，所以红黑树的 I/O 渐进复杂度也为 O(h)，效率明显比 B-Tree 差很多。

面试题2 ：为什么 MySQL 的索引使用 B+ 树而不是 B 树呢？
（1）B+ 树更适合外部存储(一般指磁盘存储),由于内节点(非叶子节点)不存储 data，所以一个节点可以存储更多的内节点，每个节点能索引的范围更大更精确。也就是说使用 B+ 树单次磁盘 IO 的信息量相比较 B 树更大，IO 效率更高。（2）MySQL 是关系型数据库，经常会按照区间来访问某个索引列，B+ 树的叶子节点间按顺序建立了链指针，加强了区间访问性，所以B+树对索引列上的区间范围查询很友好。而 B 树每个节点的 key 和 data 在一起，无法进行区间查找。

官方文档

菜鸟教程

视频

书籍

https://dev.mysql.com/doc/refman/5.7/en/innodb-storage-engine.html

25-MySQL数据库多实例的多种配置方案介绍

同一台主机，3306 3307端口都用

docker

ng Redis都可以用

mysql只能改表名，不能改数据库名称

`help alter table`

mysql cluster是分布式集群吗？
试用

doc
3.6.2 
select max
left join
limit

如果max有多个，limit只有一个


深入理解MySQL核心技术
对源码的文件对应的功能有讲解
分模块

SELECT p1.name, p1.sex, p2.name, p2.sex, p1.species FROM pet AS p1 INNER JOIN pet AS p2         ON p1.species = p2.species AND p1.sex = 'f' AND p1.death IS NULL  AND p2.sex = 'm' AND p2.death IS NULL;
+--------+------+-------+------+---------+ 
| name   | sex  | name  | sex  | species 
| +--------+------+-------+------+---------+ 
| Fluffy | f    | Claws | m    | cat     | 
| Buffy  | f    | Fang  | m    | dog     
| +--------+------+-------+------+---------+

```
mysql your-database-name

```

线程管理器 入口
sql/mysqld.cc
static void create_new_thread(THD *thd)


sql/sql_class.h
THD类定义

连接管理器
sql/mysqld.cc

void handle_connections_sockets();



XA 分布式事务

```mysql

SHOW VARIABLES LIKE '%xa%';

```


后台开发中经常需要给前端提供接口，返回的字段为null的时候需要设置字段的默认值。

select ifnull(字段,0) from 表名

[java se transactions](https://docs.oracle.com/javase/tutorial/jdbc/basics/transactions.html)

```java

Connection conn = DriverManager.getConnection(...);
try{
  con.setAutoCommit(false);
  Statement stmt = con.createStatement();

   //1 or more queries or updates

   con.commit();
}catch(Exception e){
   con.rollback();
}finally{
   con.close();
}

```


[mysql transaction](https://www.runoob.com/mysql/mysql-transaction.html)

```shell

mysql> use RUNOOB;
Database changed
mysql> CREATE TABLE runoob_transaction_test( id int(5)) engine=innodb;  # 创建数据表
Query OK, 0 rows affected (0.04 sec)
 
mysql> select * from runoob_transaction_test;
Empty set (0.01 sec)
 
mysql> begin;  # 开始事务
Query OK, 0 rows affected (0.00 sec)
 
mysql> insert into runoob_transaction_test value(5);
Query OK, 1 rows affected (0.01 sec)
 
mysql> insert into runoob_transaction_test value(6);
Query OK, 1 rows affected (0.00 sec)
 
mysql> commit; # 提交事务
Query OK, 0 rows affected (0.01 sec)
 
mysql>  select * from runoob_transaction_test;
+------+
| id   |
+------+
| 5    |
| 6    |
+------+
2 rows in set (0.01 sec)
 
mysql> begin;    # 开始事务
Query OK, 0 rows affected (0.00 sec)
 
mysql>  insert into runoob_transaction_test values(7);
Query OK, 1 rows affected (0.00 sec)
 
mysql> rollback;   # 回滚
Query OK, 0 rows affected (0.00 sec)
 
mysql>   select * from runoob_transaction_test;   # 因为回滚所以数据没有插入
+------+
| id   |
+------+
| 5    |
| 6    |
+------+
2 rows in set (0.01 sec)

```





 在MYSQL 8以前，写日志被保护在一把大锁之下，本来并行事务日志写入被人为串行化处理。虽简化了逻辑，但也极大限制了整体的性能表现。8.0很大的一部分工作便是将日志系统并行化。 





mysql -u用户名 -p --default-character-set=utf-8



[mysql中的文件排序(filesort)](https://www.cnblogs.com/chafanbusi/p/10648026.html)





mysql是server和存储引擎分离的

mysql是一个c实现的客户端

mysqld

mysqld_safe

自动开启事务，默认是开启的

刚安装之后

命名管道      ---------      Windows

Unix套接字  ---------      nux



授权的功能

user pwd



还有数据库 表权限控制

访问来源（ip）控制





默认的表：

- mysql

user表

- perfermance_scheme

- information_schema



innodb存储的文件

.frm

.bgd



.frm是表结构文件

.bgd是数据文件



Unix/Linus文件是区分大小写（大小写敏感）

Windows Mac默认是不区分大小写的





INDEX(普通索引)
`mysql>ALTER TABLE `table_name` ADD INDEX index_name ( `column` )`

```
create table test1(
     id int(11) NOT NULL AUTO_INCREMENT COMMENT  '主键id',
     username VARCHAR(25) DEFAULT NULL COMMENT  '用户名',
     password VARCHAR(25) NOT NULL COMMENT  '密码',
     birthday DATE NOT NULL COMMENT  '生日',
     telephone VARCHAR(25) DEFAULT NULL COMMENT  '手机号码',
     PRIMARY KEY (id),
     INDEX  t_tel  (telephone)
 ) 
 COMMENT = '记录用户表';
```

3，删除索引

DROP INDEX index_name ON talbe_name

ALTER TABLE table_name DROP INDEX index_name
1
2
3
4
4，添加索引

ALTER TABLE table_name ADD INDEX index_name (column_list)

ALTER TABLE table_name ADD UNIQUE (column_list)

ALTER TABLE table_name ADD PRIMARY KEY (column_list)
————————————————


refence：https://blog.csdn.net/sddh1988/article/details/78611949


refence：https://blog.csdn.net/sddh1988/article/details/78611949

版权声明：本文为CSDN博主「song_suo」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/sddh1988/article/details/78611949






mysql执行.sql文件



导入sql文件前，如果不存在数据库，一定要新建数据库.



mysql -u root -pxxx database < xxx.sql



```shell
mysql -u root -e 'CREATE DATABASE stockmarket;'
mysql -u root -e "CREATE USER 'makler'@'localhost' IDENTIFIED BY 'makler';"
mysql -u root -e "GRANT ALL ON stockmarket.* TO 'makler'@'localhost';"
```



tidb

5.7.25-TiDB-v3.0.3





[MySQL内核源码解读-SQL解析之解析器浅析](https://blog.51cto.com/wangwei007/2300959)



先登录mysql数据库

mysql -u root

进入到mysql的目录下载进行操作

use mysql

select host, user from user;



[MySQL内核源码解读-SQL解析之解析器浅析](https://blog.51cto.com/wangwei007/2300959)



SQL规范与性能优化

1.2.1、先提前声明，博主工作用到是MySQL，可能有些场景只针对MySQL。说到SQL优化，一些概念必须要理解，不然死记硬背一两天就忘记了。特别是执行计划的概念。

1.2.2、什么是执行计划：a.决定如何访问表数据，是否通过索引，是否排序等。b.多表关联是先访问哪个表。c.多表关联时，使用哪种连接方式，不过现在MySQL只有嵌套连接（嵌套循环，顾名思义就是将一个表为出发点，将该表全部记录逐条去遍历另外一张表的记录）。

1.2.3、SQL执行顺序：a.检查语法是否正确。b.检查表是否存在、权限是否满足等。c.根据统计信息(如data length,rows,index length、索引唯一度)，生成较优的执行计划。d.根据执行计划，进行数据检索、过滤、合并、排序等操作。访问数据时，内存中如存在表数据，则直接进行操作；否则，从磁带读取表数据，放入内存，再进行操作；如内存不足，则内存中较冷数据涮出内存，再从内存中读取数据。

1.2.4、索引：查询的时候如果使用上了索引，可以提高效率，因为建立了索引后，可以理解为数据字典的结构存储，因此根据条件查询的时候更加高效。下面看一下MySQL常用的索引类型的概念。 

a．普通索引：在创建普通索引时，不附加任何限制条件。这类索引可以创建在任何数据类型中，其值是否唯一和非空由字段本身的完整性约束条件决定。建立索引以后，查询时可以通过索引进行查询。例如，在student表的stu_id字段上建立一个普通索引。查询记录时，就可以根据该索引进行查询。

b．唯一性索引:使用UNIQUE参数可以设置索引为唯一性索引。在创建唯一性索引时，限制该索引的值必须是唯一的。例如，在student表的stu_name字段中创建唯一性索引，那么stu_name字段的值就必需是唯一的。通过唯一性索引，可以更快速地确定某条记录。主键就是一种特殊唯一性索引。

c．单列索引:在表中的单个字段上创建索引。单列索引只根据该字段进行索引。单列索引可以是普通索引，也可以是唯一性索引，还可以是全文索引。只要保证该索引只对应一个字段 即可。

d．多列索引：多列索引是在表的多个字段上创建一个索引。该索引指向创建时对应的多个字段，可以通过这几个字段进行查询。但是，只有查询条件中使用了这些字段中第一个字段时，索引才会被使用。例如，在表中的id、name和sex字段上建立一个多列索引，那么，只有查询条件使用了id字段时该索引才会被使用。

e . 全文索引：使用FULLTEXT参数可以设置索引为全文索引。全文索引只能创建在CHAR、VARCHAR或TEXT类型的字段上。查询数据量较大的字符串类型的字段时，使用全文索引可以提高查询速度。例如，student表的information字段是TEXT类型，该字段包含了很多的文字信息。在information字段上建立全文索引后，可以提高查询information字段的速度。MySQL数据库从3.23.23版开始支持全文索引，但只有MyISAM存储引擎支持全文检索。在默认情况下，全文索引的搜索执行方式不区分大小写。但索引的列使用二进制排序后，可以执行区分大小写的全文索引。

还有空间索引，平时也比较少用。目前只有MyISAM存储引擎支持空间检索。目前博主也只接触过InnoDB存储引擎。

1.2.5、一般一张表索引不要超过5个，而且避免重复索引，而且也不是建了索引，根据索引字段条件查询，索引就会起作用。

1.2.6、一般哪些场景会导致索引失效：a.使用like关键字匹配字符串第一个为”%”的场景。b.条件中包含or、in、not in、<>关键字，默认不走索引的。c.访问表上的数据行超出表总记录数30%，变成全表扫描。d.查询条件使用函数在索引列上，或者对索引列进行运算。e.多列索引中，第一个索引列使用范围查询，只能用到部份或无法使用索引。f.多列索引中，第一个查询条件不是最左索引列，上面多列索引概念中也有提到。肯定还有更多的场景，但是博主现在能想到的场景就这些了。

1.2.7、不能同时使用两个索引，一个过滤数据，一个用于排序（主键除外）。

1.2.8、DML语句如果使用索引，会导致lock全表；如果使用了非唯一索引，可能只是锁住一定范围。对此，建议更新/删除数据尽量用上索引，如果可以最好用上主键或唯一索引，另外事务要及时提交。

1.2.9、最后一点，如何看执行计划，分析SQL的性能。这个吧，三言两语说不清楚，直接看其他博主的博文吧：[mysql explain执行计划详解](https://link.zhihu.com/?target=http%3A//www.cnblogs.com/xiaoboluo768/p/5400990.html)。一定要看！

[启用mysql的sql日志](https://blog.csdn.net/aochijing0046/article/details/101493526)


[如何在MySql中记录SQL日志](https://www.cnblogs.com/liuliu/archive/2009/09/04/1560327.html)





https://www.cnblogs.com/liuliu/archive/2009/09/04/1560327.html



在mysql命令行或者客户端管理工具中执行：SHOW VARIABLES LIKE "general_log%";

结果：

general_log OFF
general_log_file /var/lib/mysql/localhost.log

OFF说明没有开启日志记录

分别执行开启日志以及日志路径和日志文件名

SET GLOBAL general_log_file = '/var/lib/mysql/localhost.log';
SET GLOBAL general_log = 'ON';

还要注意

这时执行的所有sql都会别记录下来，方便查看，但是如果重启mysql就会停止记录需要重新设置

 

SHOW VARIABLES LIKE "log_output%";

查询结果FILE



[Mysql 配置慢查询日志（SlowQueryLog）以及使用日志分析工具](https://www.cnblogs.com/codelife1988/p/4159964.html)

MySQL

检查配置文件是否正确？？？



MySQL日志主要包含：错误日志、查询日志、慢查询日志、事务日志、二进制日志。
https://www.cnblogs.com/mungerz/p/10442791.html

show variables like 'general_log_file';
查看本地日志路径

show variables like 'slow_query_log_file';
慢查询日志



错误日志： -log-err
查询日志： -log
慢查询日志: -log-slow-queries
更新日志: -log-update
二进制日志： -log-bin




[windows下启动mysql服务的命令行启动和手动启动方法](https://www.cnblogs.com/xuyou551/p/7998365.html)

1、图形界面下启动mysql服务。
在图形界面下启动mysql服务的步骤如下：
（1）打开控制面板->管理工具->服务，如下图所示：
下面讲通过命令行的方式启动mysql服务：
2、命令行下启动mysql服务。
（1）先找到mysql的安装位置，如我的电脑的安装位置是：D:\Program Files\MySQL\MySQL Server 5.0，我就执行下面的操作：
开始->运行->输入“cmd”开启命令行，然后输入“D:”定位到D盘符。如图
进入Mysql目录下的bin目录中，如图：
（2）输入mysql命令行的服务启用命令：

net start mysql （对应的服务关闭命令为 net stop mysql）





#### 查看mysql版本

centos 7

mysql -V



mysql 命令行

`status;`

`select version();`

net start mysql （对应的服务关闭命令为 net stop mysql）

