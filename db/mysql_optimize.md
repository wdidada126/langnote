# mysql optimize

子查询改写为连接

Join关联、in和exsits优化、count(*)查询优化
https://blog.csdn.net/nmjhehe/article/details/113825736

千万级表JOIN 语句的优化原则
-- mysql JOIN 语句的优化原则-- mysql JOIN 语句的优化原则
-- 1.小表驱动大表（EXPLAIN的第一行是驱动表）,WHERE 条件驱动表的筛选j出尽量少的数
-- 2.where里有筛选条件，而且可以使用索引,并对驱动表晒选出尽量少的行数
-- 3.非驱动表连接join字段最好是主键索引，无法建立索引的时候，设置足够的Join Buffer Size
-- 4.尽量避免联表数量，避免尽量少返回字段，避免返回字段有计算，越多，嵌套循环算法越慢，
-- 5.join连接表的语句不能再用子查询，COUNT(1) 分页统计返回字段要尽量少。
-- 6.扫描行数必须控制在百万级别，返回行数控制在千级别，且要分页处理.
-- 7.必须遵循以上原则，否则不用join，改单表查询在拼接，或者用es查询在拼接

-- mysql JOIN 语句study
-- 1.小表驱动大表（EXPLAIN的第一行是驱动表）,WHERE 条件驱动表的筛选小行数
-- 2.NestedLoopJoin实际上就是通过驱动表的结果集作为循环基础数据，然后一条一条的通过该结果集中的数据作为过滤条件到下一个表中查询数据，https://blog.csdn.net/qq_27529917/article/details/87904179（细节参考）
-- 3.a.无order by条件时，根据实际情况，使用left/right/inner join即可，根据explain优化；
-- 4.b.有order by a.col条件时，所有join必须为left join，且每个join字段都创建索引，同时where条件中只能有a表的条件，即将其它表的数据关联到a中形成一张大表，再对a的全集进行过滤；
-- 5.通过where预估结果行数，遵循以下规则：https://blog.csdn.net/qq_27529917/article/details/87904179（细节参考）
--    如果where里没有相应表的筛选条件，无论on里是否有相关条件，默认为全表
--      如果where里有筛选条件，但是不能使用索引来筛选，那么默认为全表
--      如果where里有筛选条件，而且可以使用索引，那么会根据索引来预估返回的记录行数
-- 6.mysql只支持一种join算法：Nested-Loop Join（嵌套循环连接），但Nested-Loop Join有三种变种：https://cloud.tencent.com/developer/article/1373839（细节参考）
--     6.1非驱动表走主键索引不用回表，最快，
--     6.2没有所以索引，默认情况下join_buffer_size=256K，在查找的时候MySQL会将所有的需要的列缓存到join buffer当中
--     6.3对s表进行了rn次访问，对数据库开销大
-- select *  from  a  left join b on a.id = b.id left join a.id = c.id，这时是怎么顺序进行执行的呢？
-- 我们得知是a表先和b表进行连接，会生成一张中间临时表，然后这张表的数据再和c表进行连接，最后生成的表的数据就是a left join b left join c 的。
-- EXPLAIN  ALL, index,  range, ref, eq_ref, const, system, NULL

学习Mysql的join算法：Index Nested-Loop Join和Block Nested-Loop Join
https://blog.csdn.net/u010841296/article/details/89790399

在Mysql的实现中，Nested-Loop Join有3种实现的算法：
Simple Nested-Loop Join：SNLJ，简单嵌套循环连接
Index Nested-Loop Join：INLJ，索引嵌套循环连接
Block Nested-Loop Join：BNLJ，缓存块嵌套循环连接

简单嵌套循环连接实际上就是简单粗暴的嵌套循环，如果table1有1万条数据，table2有1万条数据，那么数据比较的次数=1万 * 1万 =1亿次，这种查询效率会非常慢。
只有内层表join的列有索引时，才能用到Index Nested-LoopJoin进行连接。
原来的匹配次数 = 外层表行数 * 内层表行数
优化后的匹配次数= 外层表的行数 * 内层表索引的高度

Block Nested-Loop Join（减少内层表数据的循环次数）
1、缓存块嵌套循环连接通过一次性缓存多条数据，把参与查询的列缓存到Join Buffer 里，然后拿join buffer里的数据批量与内层表的数据进行匹配，从而减少了内层循环的次数（遍历一次内层表就可以批量匹配一次Join Buffer里面的外层表数据）。
2、当不使用Index Nested-Loop Join的时候，默认使用Block Nested-Loop Join。
什么是Join Buffer？
（1）Join Buffer会缓存所有参与查询的列而不是只有Join的列。
（2）可以通过调整join_buffer_size缓存大小
（3）join_buffer_size的默认值是256K，join_buffer_size的最大值在MySQL 5.1.22版本前是4G-1，而之后的版本才能在64位操作系统下申请大于4G的Join Buffer空间。
（4）使用Block Nested-Loop Join算法需要开启优化器管理配置的optimizer_switch的设置block_nested_loop为on，默认为开启。

如何优化Join速度
- 用小结果集驱动大结果集，减少外层循环的数据量，从而减少内层循环次数：
如果小结果集和大结果集连接的列都是索引列，mysql在内连接时也会选择用小结果集驱动大结果集，因为索引查询的成本是比较固定的，这时候外层的循环越少，join的速度便越快。
- 为匹配的条件增加索引：争取使用INLJ，减少内层表的循环次数
- 增大join buffer size的大小：当使用BNLJ时，一次缓存的数据越多，那么内层表循环的次数就越少
- 减少不必要的字段查询：
（1）当用到BNLJ时，字段越少，join buffer 所缓存的数据就越多，内层表的循环次数就越少；
（2）当用到INLJ时，如果可以不回表查询，即利用到覆盖索引，则可能可以提示速度。（未经验证，只是一个推论）

MySQL 8 Query Performance Tuning
A Systematic Method for Improving Execution Speeds

Biography
Jesper Wisborg Krogh has worked with MySQL databases since 2006 both as an SQL developer, a database administrator, and for more than eight years as part of the Oracle MySQL Support team. He currently works as a database reliability engineer for Okta. He has spoken at MySQL Connect and Oracle OpenWorld on several occasions, and addition to his books, he regularly blogs on MySQL topics and has authored around 800 documents in the Oracle Knowledge Base. He has contributed to the sys schema and four Oracle Certified Professional (OCP) exams for MySQL 5.6 to 8.0.
He earned a PhD in computational chemistry before changing to work with MySQL and other software development in 2006. Jesper lives in Sydney, Australia, and enjoys spending time outdoors walking, traveling, and reading. His areas of expertise include MySQL Cluster, MySQL Enterprise Backup, performance tuning, and the Performance and sys schemas.

https://www.amazon.com/dp/1484255836?tag=uuid10-20

mysql 官方文档就有优化相关的章节
http://dev.mysql.com/doc/refman/5.7/en/optimization.html

Query Execution Plan 查询执行计划

SQL Tuning 2003出版的书籍
SQL Server Query Performance Tuning,Fourth Edition
2014 ms sql server的

google query
mysql server query sql optimize

https://shashwat-creator.medium.com/mysql-query-optimizer-fc158b3de623
https://www.dnsstuff.com/mysql-optimize-database
https://www.eversql.com/sql-performance-tuning-tips-for-mysql-query-optimization/

D:\git\gitlab\langnote\MySQL性能调优与架构设计.pdf  对应的mysql版本是5.1 5.2的？

## 第八章

8.5 Join 的实现原理及优化思路
 MySQL 中，只有一种 Join 算法，就是大名鼎鼎的 Nested Loop Join

high-performance-mysql/9780596101718/ch04.html
高性能mysql第四章

mysql server query sql optimize




分析如何优化 MySQL Query 之前，我们需要先了解一下 Query 语句优化的基本思路和原则。一
般来说， Query 语句的优化思路和原则主要提现在以下几个方面：
1. 优化更需要优化的 Query；
2. 定位优化对象的性能瓶颈；
3. 明确的优化目标；
4. 从 Explain 入手；
5. 多使用 profile
6. 永远用小结果集驱动大的结果集；
7. 尽可能在索引中完成排序；
8. 只取出自己需要的 Columns；
9. 仅仅使用最有效的过滤条件；
10. 尽可能避免复杂的 Join 和子查询


要想优化一条 Query，我们就需要清楚的知道这条 Query 的性能瓶颈到底在哪里，是消耗的 CPU
计算太多，还是需要的的 IO 操作太多
MySQL 的 Query Profiler 是一个使用非常方便的 Query 诊断分析工具，通过该工具可以获取一条
Query 在整个执行过程中多种资源的消耗情况，如 CPU， IO， IPC， SWAP 等，以及发生的 PAGE FAULTS，CONTEXT SWITCHE 等等，同时还能得到该 Query 执行过程中 MySQL 所调用的各个函数在源文件中的位
置。下面我们看看 Query Profiler 的具体用法。




三种物理连接操作(Nested Loop Join、Merge Join、Hash Join)
https://blog.csdn.net/u010841296/article/details/89790399

在Mysql的实现中，Nested-Loop Join有3种实现的算法：
Simple Nested-Loop Join：SNLJ，简单嵌套循环连接
Index Nested-Loop Join：INLJ，索引嵌套循环连接
Block Nested-Loop Join：BNLJ，缓存块嵌套循环连接
在选择Join算法时，会有优先级，理论上会优先判断能否使用INLJ、BNLJ：
Index Nested-LoopJoin > Block Nested-Loop Join > Simple Nested-Loop Join



1、简单嵌套循环连接实际上就是简单粗暴的嵌套循环，如果table1有1万条数据，table2有1万条数据，那么数据比较的次数=1万 * 1万 =1亿次，这种查询效率会非常慢。
2、所以Mysql继续优化，然后衍生出Index Nested-LoopJoin、Block Nested-Loop Join两种NLJ算法。在执行join查询时mysql会根据情况选择两种之一进行join查询。

soar 在测试环境优化没用，因为测试环境表数据量跟开发环境不一样
数据库 两千万
测试环境没有这么多


[记一次mysql优化 not in, not exits, left join 子查询](https://blog.csdn.net/qq_39504351/article/details/100051523)

t_block_count AS bc
t_block_blacklist_device AS bbd2
t_block_count AS bc


```sql
	SELECT
		SUM( bc.c_count ) AS blockNum
	FROM
		t_block_count AS bc
	WHERE
		bc.c_school_code = '****' 
		AND bc.c_block_id NOT IN (
		SELECT
			bbd2.c_blacklist_id 
		FROM
			t_block_blacklist_device AS bbd2 
		WHERE
			bbd2.c_school_code = '****' 
			AND bbd2.c_enabled = 1 
			AND bbd2.c_type IN ( 1, 4 ) 
		) 
	GROUP BY
		bc.c_block_id 
	ORDER BY
		blockNum DESC;
	SELECT
		SUM( bc.c_count ) AS blockNum
	FROM
		t_block_count AS bc
		LEFT JOIN t_block_blacklist AS bb ON bc.c_block_id = bb.c_id 
	WHERE
		bc.c_school_code = '****'
		AND NOT EXISTS (
		SELECT
			bbd2.c_blacklist_id 
		FROM
			t_block_blacklist_device AS bbd2 
		WHERE
			bbd2.c_school_code = '****'
			AND bbd2.c_enabled = 1 
			AND bbd2.c_type IN ( 1, 4 ) 
			AND bc.c_block_id = bbd2.c_blacklist_id
		) 
	GROUP BY
		bc.c_block_id 
	ORDER BY
		blockNum DESC;
SELECT
	SUM( bc.c_count ) AS blockNum
FROM
	t_block_count AS bc
	LEFT JOIN (
	SELECT
		bbd2.c_blacklist_id 
	FROM
		t_block_blacklist_device AS bbd2 
	WHERE
		bbd2.c_school_code = '****' 
		AND bbd2.c_enabled = 1 
		AND bbd2.c_type IN ( 1, 4 ) 
	) AS t ON t.c_blacklist_id = bc.c_block_id 
WHERE
	bc.c_school_code = '****' 
	AND t.c_blacklist_id IS NULL 
GROUP BY
	bc.c_block_id 
ORDER BY
	blockNum DESC;
```

DBA的五款优秀SQL查询优化工具
https://blog.csdn.net/benben683280/article/details/97761837

1.Solarwinds数据库性能分析器
2.Redgate SQL Monitor
3.Idera DB Optimizer
4.EverSQL
5.dbForge Studio

- soar
- SQLAdvisor
- EverSQL

https://www.eversql.com/sql-syntax-check-validator/

谷歌登录

Inception: 去哪儿网开源，提供SQL语句审核、执行、回滚功能
SQLAdvisor: 美团开源，提供分析SQL中的where条件、聚合条件、多表Join关系，输出索引优化建议
SOAR: 小米开源，提供SQL启发式算法的语句优化、多列索引优化等功能



https://blog.csdn.net/qq_40026782/article/details/105772421
今天我们分享了 show profile 和 trace 的使用方法，我们来对比一下三种分析 SQL 方法的特点：
explain：获取 MySQL 中 SQL 语句的执行计划，比如语句是否使用了关联查询、是否使用了索引、扫描行数等；
profile：可以清楚了解到SQL到底慢在哪个环节；
trace：查看优化器如何选择执行计划，获取每个可能的索引选择的代价。
三种方法各有其适用场景，如果你有其它分析 SQL 的工具，欢迎在留言区分享。
最后推荐大家一款小米开源的sql分析工具：soar-web



show variables like "%profi%";
+------------------------+-------+
| Variable_name          | Value |
+------------------------+-------+
| have_profiling         | YES   |
| profiling              | OFF   |
| profiling_history_size | 15    |
+------------------------+-------+
3 rows in set (0.06 sec)


Mysql所有的profile都被记录到了information_schema.profiling表。
Profiling是从 mysql5.0.3版本以后才开放的。
“show profiles”已弃用，SHOW PROFILES将来会被Performance Schema替换掉，但是现在还是非常非常实用的，8.0目前还在支持中。


 启动profile之后，所有
 查询包括错误的语句都会记录在内。

查看执行时间
1 show profiles;
2 show variables;查看profiling 是否是on状态；
3 如果是off，则 set profiling = 1；
4 执行自己的sql语句；
5 show profiles；就可以查到sql语句的执行时间；

show variables like "profiling";
set profiling = 1;

show profile for query 1;
show profile cpu, block io, memory,swaps,context switches,source for query 1;

```shell
show profile for query 1;
+----------------------+----------+
| Status               | Duration |
+----------------------+----------+
| starting             | 0.000061 |
| checking permissions | 0.000009 |
| Opening tables       | 0.000047 |
| init                 | 0.000012 |
| System lock          | 0.000005 |
| optimizing           | 0.000007 |
| statistics           | 0.000013 |
| preparing            | 0.000011 |
| executing            | 0.000291 |
| Sending data         | 0.000018 |
| end                  | 0.000005 |
| query end            | 0.000004 |
| closing tables       | 0.000003 |
| removing tmp table   | 0.000006 |
| closing tables       | 0.000004 |
| freeing items        | 0.000041 |
| cleaning up          | 0.000011 |
+----------------------+----------+
17 rows in set (0.10 sec)

mysql> show profile cpu, block io, memory,swaps,context switches,source for query 1;
+----------------------+----------+----------+------------+-------------------+---------------------+--------------+---------------+-------+-----------------------+------------------+-------------+
| Status               | Duration | CPU_user | CPU_system | Context_voluntary | Context_involuntary | Block_ops_in | Block_ops_out | Swaps | Source_function       | Source_file      | Source_line |
+----------------------+----------+----------+------------+-------------------+---------------------+--------------+---------------+-------+-----------------------+------------------+-------------+
| starting             | 0.000061 | 0.000030 | 0.000018   |                 0 |                   0 |            0 |             0 |     0 | NULL                  | NULL             | NULL        |
| checking permissions | 0.000009 | 0.000006 | 0.000003   |                 0 |                   0 |            0 |             0 |     0 | check_access          | sql_parse.cc     |        5347 |
| Opening tables       | 0.000047 | 0.000030 | 0.000017   |                 0 |                   0 |            0 |             0 |     0 | open_tables           | sql_base.cc      |        5095 |
| init                 | 0.000012 | 0.000007 | 0.000004   |                 0 |                   0 |            0 |             0 |     0 | mysql_prepare_select  | sql_select.cc    |        1051 |
| System lock          | 0.000005 | 0.000003 | 0.000002   |                 0 |                   0 |            0 |             0 |     0 | mysql_lock_tables     | lock.cc          |         304 |
| optimizing           | 0.000007 | 0.000004 | 0.000002   |                 0 |                   0 |            0 |             0 |     0 | optimize              | sql_optimizer.cc |         139 |
| statistics           | 0.000013 | 0.000008 | 0.000005   |                 0 |                   0 |            0 |             0 |     0 | optimize              | sql_optimizer.cc |         365 |
| preparing            | 0.000011 | 0.000008 | 0.000004   |                 0 |                   0 |            0 |             0 |     0 | optimize              | sql_optimizer.cc |         488 |
| executing            | 0.000291 | 0.000185 | 0.000107   |                 0 |                   0 |            0 |             0 |     0 | exec                  | sql_executor.cc  |         110 |
| Sending data         | 0.000018 | 0.000011 | 0.000007   |                 0 |                   0 |            0 |             0 |     0 | exec                  | sql_executor.cc  |         190 |
| end                  | 0.000005 | 0.000003 | 0.000001   |                 0 |                   0 |            0 |             0 |     0 | mysql_execute_select  | sql_select.cc    |        1106 |
| query end            | 0.000004 | 0.000002 | 0.000002   |                 0 |                   0 |            0 |             0 |     0 | mysql_execute_command | sql_parse.cc     |        5046 |
| closing tables       | 0.000003 | 0.000002 | 0.000001   |                 0 |                   0 |            0 |             0 |     0 | mysql_execute_command | sql_parse.cc     |        5094 |
| removing tmp table   | 0.000006 | 0.000004 | 0.000002   |                 0 |                   0 |            0 |             0 |     0 | free_tmp_table        | sql_tmp_table.cc |        1870 |
| closing tables       | 0.000004 | 0.000002 | 0.000001   |                 0 |                   0 |            0 |             0 |     0 | free_tmp_table        | sql_tmp_table.cc |        1899 |
| freeing items        | 0.000041 | 0.000026 | 0.000015   |                 0 |                   0 |            0 |             0 |     0 | mysql_parse           | sql_parse.cc     |        6521 |
| cleaning up          | 0.000011 | 0.000007 | 0.000004   |                 0 |                   0 |            0 |             0 |     0 | dispatch_command      | sql_parse.cc     |        1812 |
+----------------------+----------+----------+------------+-------------------+---------------------+--------------+---------------+-------+-----------------------+------------------+-------------+
17 rows in set (0.12 sec)
```


timestampdiff查看执行时间
set @d=now();
select * from employees.employees where emp_no=10001;
select timestampdiff(second,@d,now());
返回整数的单位是？


第1种: datediff函数
datediff函数返回两个日期之间的天数
语法：DATEDIFF(date1,date2)
SELECT DATEDIFF('2018-07-01','2018-07-04');
运行结果:-3
所以，datediff函数对时间差值的计算方式为date1-date2的差值。
第2种: timestampdiff函数
timestampdiff函数日期或日期时间表达式之间的整数差。
语法：TIMESTAMPDIFF(interval，datetime1，datetime2)，比较的单位interval可以为以下数值
FRAC_SECOND。表示间隔是毫秒
SECOND。秒
MINUTE。分钟
HOUR。小时
DAY。天
WEEK。星期
MONTH。月
QUARTER。季度
YEAR。年
select TIMESTAMPDIFF(DAY,'2018-07-01 09:00:00','2018-07-04 12:00:00');
运行结果:3
所以，timestampdiff函数对日期差值的计算方式为datetime2-datetime1的差值。
请注意：DATEDIFF，TIMESTAMPDIFF对日期差值的计算方式刚好是相反的。

mysql sql
select
where in是否走索引

查询的CPU消耗：or>in>union

mysql where in 优化建议

改为union

mybatis xml怎么写？
https://blog.csdn.net/nangeali/article/details/80767662


MySQL深入学习笔记及实战指南
http://www.notedeep.com/note/38/page/329


一、数据库设计
一般都使用 INNODB 存储引擎，除非读写比率 < 1%, 才考虑使用 MYISAM 存储引擎；其 他存储引擎请在 DBA 的建议下使用。
Stored procedure (包括存储过程，函数，触发器) 对于 MYSQL 来说还不是很成熟， 没有完善的出错记录处理，不建议使用。
UUID ()，USER () 这样的 MySQL INSIDE 函数对于复制来说是很危险的，会导致主备数据不一致，所以请不要使用。如果一定要使用 UUID 作为主键，让应用程序来产生。
不要使用外键约束，如果数据存在外键关系，请在程序层面实现。
采用 UTF8 编码。

视图？
语法
作用

https://learnku.com/articles/25116

阿里新零售数据库设计与实战 （升级版）
https://ctc.koogua.com/course/1208
百度云下载

菜鸟也能飞：SQL数据库实战专业教程（二）
https://developer.aliyun.com/article/135597


MySQL8.0实战(二) - 数据库设计
https://cloud.tencent.com/developer/article/1450563


项目实战：数据库设计精选视频课程-架构师必修课-肖海鹏-专题视频课程
https://blog.csdn.net/XiaoGong1688/article/details/83574283


【实战演练】数据库基本知识与原理系列02-数据库设计与开发的范式
https://zhuanlan.zhihu.com/p/104183969

项目实战：数据库设计精选视频课程-架构师课
https://edu.51cto.com/course/7127.html


阿里新零售数据库设计与实战 （升级版）
https://coding.imooc.com/class/353.html


MySQL8.0实战(二) - 数据库设计
https://juejin.cn/post/6844903873933475848


同一表中，所有 varchar 字段的长度加起来，不能大于 65535. 如果有这样的需求，请使用 TEXT/LONGTEXT 类型。

TINYTEXT	256 bytes	 
TEXT	65,535 bytes	~64kb               最大2147483647个字符
MEDIUMTEXT	 16,777,215 bytes	~16MB
LONGTEXT	4,294,967,295 bytes	~4GB        4294967295

-----------       + -------------------------------------
TINYTEXT      | 255（2 8 -1）个字节
TEXT          | 65,535（2 16 -1）个字节= 64个KiB
MEDIUMTEXT | 16,777,215（2 24 -1）字节= 16 MiB
LONGTEXT    | 4,294,967,295（2 32 -1）个字节= 4个GiB
需要注意的是数目将取决于字符编码。




https://cloud.tencent.com/developer/ask/26839





软件层面 硬件层面

存储引擎选择是否正确

压缩表数据

Compression is available for all kinds of workloads with `InnoDB` tables, and for read-only `MyISAM` tables.



各种缓存大小是否设置正确

join cache

The main memory areas to configure are the `InnoDB` buffer pool, the `MyISAM` key cache, and the MySQL query cache.





bottleneck 瓶颈

[`NDB`](https://dev.mysql.com/doc/refman/5.7/en/mysql-cluster.html) storage engine



range 优化

https://blog.csdn.net/weixin_39805119/article/details/113318763

RangeAccess使用单个索引的方式来检索包含在一个或多个索引值区间内的表行的子集。它也适用于单列或复合(组合)索引...



IN，恐怖如斯，在 IN中每个内容就会视为一个 OR，如果有多个IN，那么该占用的指数是乘积(M×N)



sort-union algorithm

union algorithm



icp 索引下推

SET optimizer_switch = 'index_condition_pushdown=off'; 

SET optimizer_switch = 'index_condition_pushdown=on';



优化 硬件优化

软件优化



不同的存储引擎



8 ndb

5.6 5.6

select where条件 范围查询 索引下推  join优化 is null， order by group by，distinct limit  子查询 

insert

update

delete



看不下去了



