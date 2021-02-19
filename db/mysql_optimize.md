# mysql optimize

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
