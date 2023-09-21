# SQL

select ifnull(字段,0) from 表名

sql解析
https://github.com/andialbrecht/sqlparse python语言的

SQL面试题升级打怪
https://www.zhihu.com/column/c_1284848724921765888

注意分组 实际上是把单个表搞成多个表
join 表join本身
临时表

ifnull函数处理null

今天我们分享了 show profile和trace的使用方法，我们来对比一下三种分析 SQL 方法的特点：
explain：获取 MySQL 中 SQL 语句的执行计划，比如语句是否使用了关联查询、是否使用了索引、扫描行数等；
profile：可以清楚了解到SQL到底慢在哪个环节；
trace：查看优化器如何选择执行计划，获取每个可能的索引选择的代价。
explain语法
https://dev.mysql.com/doc/refman/8.0/en/explain.html
EXPLAIN是MySQL中的一个关键字，用于模拟优化器执行SQL查询语句，从而知道MySQL是如何处理你的SQL语句的。
EXPLAIN 是 MySQL 中用于获取查询语句执行计划的命令。它可以帮助你理解 MySQL 如何执行查询，从而优化查询性能。

EXPLAIN 语句的基本语法如下：
EXPLAIN SELECT column_name FROM table_name;
你可以将任何有效的 SELECT 语句替换为上述语法中的 SELECT 语句。

EXPLAIN 语句返回的结果集包含以下字段：
id: 查询的标识符
select_type: 查询的类型（例如 SIMPLE, SUBQUERY, UNION 等）
table: 查询涉及的表名
type: 访问类型，表示 MySQL 如何查找表中的行
possible_keys: 可能使用的索引
key: 实际使用的索引
key_len: 使用的索引长度
ref: 与索引比较的列或常量
rows: MySQL 认为需要检查的行数
Extra: 关于查询的额外信息
通过分析 EXPLAIN 的结果，你可以确定查询是否使用了合适的索引，是否进行了全表扫描，以及是否需要优化查询等。

以下是一个示例：

EXPLAIN SELECT * FROM users WHERE id = 1;
这将返回一个描述查询执行计划的表。

set profiling=1;  				//打开分析
show profiles;					//查看sql1,sql2的语句分析
show profile for query 1;		//查看sql1的具体分析
show profile ALL for query 1;	//查看sql1相关的所有分析【主要看i/o与cpu,下边分析中有各项意义介绍】


Mysql分析-profile详解_mysql profiles_时而宁靜的博客-CSDN博客.mhtml
https://blog.csdn.net/ty_hf/article/details/54895026

set profiling=1;  				//打开分析
run your sql1;
run your sql2;
show profiles;					//查看sql1,sql2的语句分析
show profile for query 1;		//查看sql1的具体分析
show profile ALL for query 1;	//查看sql1相关的所有分析【主要看i/o与cpu,下边分析中有各项意义介绍】
set profiling=0;  				//关闭分析

Profiling是从 mysql5.0.3版本以后才开放的。 

从MySQL5.6开始，可以使用trace查看优化器如何选择执行计划。
通过trace，能够进一步了解为什么优化器选择A执行计划而不是选择B执行计划，或者知道某个排序使用的排序模式，帮助我们更好地理解优化器行为。
如果需要使用，先开启trace，设置格式为JSON，再执行需要分析的SQL，最后查看trace分析结果（在information_schema.OPTIMIZER_TRACE中）。
https://blog.csdn.net/qq_40026782/article/details/105772421



```sql
SET OPTIMIZER_TRACE="enabled=on",END_MARKERS_IN_JSON=on;
SET OPTIMIZER_TRACE_MAX_MEM_SIZE=1000000;
```
大致步骤如下：

开启trace分析器执行要查询的sql查看分析结果关闭trace分析器
NO.1 开启trace分析器
MySQL [test]> set session optimizer_trace="enabled=on";
NO.2 执行要查询的SQL
MySQL [test]> select * from test_table where a=90000 and b=90000 order by a;
NO.3 查询分析结果
MySQL [test]> SELECT * FROM information_schema.OPTIMIZER_TRACE\G

注意：在返回的steps数组中可以查看详细mysql都干了什么。
不好意思，因为排版导致内容太长大家可以百度一下参数含义。
NO.4 关闭trace分析器
mysql> set session optimizer_trace="enabled=off";
TRACE 字段中整个文本大致分为三个过程
准备阶段：对应文本中的 join_preparation优化阶段：对应文本中的 join_optimization执行阶段：对应文本中的 join_execution

使用时，重点关注优化阶段和执行阶段。
https://blog.csdn.net/qq_40026782/article/details/105772421

知乎上有复杂sql的教程
sql联系
w3c
牛客网
leetcode
临时表的使用

找dba圈子

知乎 sql优化收藏夹
https://www.zhihu.com/collection/632564599


in不走索引
避免全表扫描

quayi公司自己写Dao层代码的时候，sql in 要判断集合是否为null

join on 可以有多个条件，用and 连接

update 不能直接使用set


## 慢sql例子
slowsqldetails(6).xlsx

用<set></set>
[SQL中笛卡尔积－cross join的用法](https://blog.csdn.net/weixin_30883777/article/details/95208805)

Sql优化挑战赛
https://zhuanlan.zhihu.com/p/27934308

玄惭，真名罗龙九，阿里云DBA专家，负责阿里云RDS线上稳定以及专家服务团队，人称“大师”！他，经历阿里历年双11考验，积累了6年对阿里云数据库用户的运维、调优、诊断等丰富的经验。他，就是本次挑战赛的出题人！

sql commont

[MySQL 添加注释 comment](https://blog.csdn.net/weixin_40169642/article/details/82562183)

在MySQL数据库中， 字段或列的注释是用属性comment来添加。 
创建新表的脚本中， 可在字段定义脚本中添加comment属性来添加注释。 
示例代码如下：**

```sql
create table test( 
    id int not null default 0 comment '用户id' ) 
```


如果是已经建好的表， 也可以用修改字段的命令，然后加上comment属性定义，就可以添加上注释了。

示例代码如下：
```sql
alter table test 
modify column id id int not null default 0 comment '测试表id'
```
查看已有表的所有字段的注释呢？ 
可以用命令：show full columns from table 来查看， 示例如下：

`show full columns from test;`

创建表的时候写注释
create table test1 ( 
    field_name int comment '字段的注释' 
)comment='表的注释'; 
1
2
3
修改表的注释
alter table test1 comment '修改后的表的注释';
1
修改字段的注释
alter table test1 modify column field_name int comment '修改后的字段注释'; 

--注意：字段名和字段类型照写就行

查看表注释的方法
--在生成的SQL语句中看 
    show  create  table  test1; 
--在元数据的表里面看
    use information_schema; 
    select * from TABLES where TABLE_SCHEMA='my_db' and TABLE_NAME='test1'

查看字段注释的方法
--show 
    show  full  columns  from  test1; 
--在元数据的表里面看 
    select * from COLUMNS where TABLE_SCHEMA='my_db' and TABLE_NAME='test1'

mybatis xml文件
org.apache.commons.lang3.StringUtils

select id,countryname,countrycode from country where countryname like '*中*'
错误
MySQL字符类型通配符是 _ %

## 刷sql的网站
SQL在线刷题神器,强推SQLZOO呀

sql行转列
在SQL中，可以使用Pivot操作将行转换为列。下面是一个例子：

假设我们有一个名为"sales"的表，它包含以下列：

region（地区）
year（年份）
sales_amount（销售额）
我们想要将该表中的数据按照年份进行转置，以便每个年份成为列，地区成为行。

以下是实现这个需求的SQL代码：

```sql
SELECT  
  region,  
  MAX(CASE WHEN year = 2020 THEN sales_amount END) AS '2020',  
  MAX(CASE WHEN year = 2021 THEN sales_amount END) AS '2021',  
  MAX(CASE WHEN year = 2022 THEN sales_amount END) AS '2022'  
FROM  
  sales  
GROUP BY  
  region;
```

在这个例子中，我们使用了CASE语句来根据年份选择相应的销售金额，然后使用MAX函数将它们汇总到每个地区的一行。通过这种方式，我们成功地将行转换为列。
请注意，具体的列名（'2020'、'2021'和'2022'）需要根据您的实际情况进行调整。如果需要更多的年份，需要添加相应的列。此外，如果有多个地区，需要将GROUP BY子句中的"region"替换为适当的列，以便对所有地区进行分组。

课程号 成绩号

现在要查看语文课程成绩 数学成绩
case c_no 1 语文
case c_no 2 数学

多列组合不重复

SQL中的DISTINCT关键字用于返回唯一的数据记录，即不重复的记录。DISTINCT关键字可以应用于一个或多个列，它将对所有列进行比较以确定是否为重复记录。
如果你使用DISTINCT修饰第一个列，它将确保第一个列的数据不重复。例如，假设你有一个名为"employees"的表，其中包含"first_name"和"last_name"两列，你可以使用以下查询来返回不重复的"first_name"值：
sql
SELECT DISTINCT first_name FROM employees;
如果你想限制所有列的数据都不重复，可以在SELECT子句中列出所有列，并使用DISTINCT关键字。例如，以下查询将返回不重复的"first_name"和"last_name"组合：
sql
SELECT DISTINCT first_name, last_name FROM employees;
这将确保在结果中没有重复的组合（即相同的"first_name"和"last_name"组合）

select 里面套 case when
https://www.cnblogs.com/dshore123/p/8126418.html?ivk_sa=1024320u

case 列 when 1 then 2 when 3 then 4

对列数据作判断

case when可以用在 select
group by

order by下面

where 判断 xxx is not null

select 查询的列 case when as xxx


navicate 查询 美化SQL，格式化sql，很有用

sql 条件判断 is null
is not null

select id ,user_name ,password ,name,age,sex from tb_user where user_name like '%${userName}%'
正确

```sql
select id as id,user_name as userName,password as password,name,age,sex from tb_user where user_name like '%#{userName}%'
```
错误 

## SQL经典50题
https://blog.csdn.net/u010226597/article/details/106334861/

SQL中EXISTS的用法
https://www.cnblogs.com/xuanhai/p/5810918.html

比如在Northwind数据库中有一个查询为
```sql
SELECT c.CustomerId,CompanyName FROM Customers c
WHERE EXISTS(
SELECT OrderID FROM Orders o WHERE o.CustomerID=c.CustomerID) 
```
这里面的EXISTS是如何运作呢？子查询返回的是OrderId字段，可是外面的查询要找的是CustomerID和CompanyName字段，这两个字段肯定不在OrderID里面啊，这是如何匹配的呢？ 

order by 子句 后面跟 case when
https://blog.csdn.net/qianyuanruqu/article/details/87617517

select 超过4张表join

select结果作为一张表，参与join

where a.xxx = b.xxx
一旦a b的xxx yyy为空，就查不出来

格式化sql
navicat 查询 新建查询 ->  美化sql

date_format(,'%Y-%m-%d %H:%:%s')

常见的SQL面试题：经典50题 - 知乎 https://zhuanlan.zhihu.com/p/38354000 
SQL面试必会50题 - 知乎 https://zhuanlan.zhihu.com/p/43289968
强制索引 FORCE INDEX
SELECT * FROM TABLE1 FORCE INDEX (FIELD1) …

知乎 sql优化收藏夹

in不走索引

避免全表扫描

sql 统计 体系 优化查询时间

避免用null
https://dzone.com/articles/how-to-optimize-mysql-queries-for-speed-and-perfor

在where中可以包含任意数目的and和or操作符，在没有任何其他符号的时候，例如括号，SQL会首先执行and条件，然后才执行or语句

表设计：主键，默认值，check
https://blog.csdn.net/qq_61122628/article/details/123738200

where后面的列要注意隐式转换，会导致索引失效
当where后面的列需要隐式转换时，会导致索引失效。例如，如果where后面的列是字符串类型，而查询条件是数字类型，则 MySQL 将数字转换为浮点数，然后执行全表扫描，这将导致索引失效12。
为了避免这种情况，你可以尽可能让 where 后面的列与查询条件的类型相同，或者将查询条件转换为与 where 后面的列相同的类型。这样可以避免隐式转换并确保索引有效。

https://dev.mysql.com/doc/refman/5.7/en/type-conversion.html

当操作符与不同类型的操作数一起使用时，会发生类型转换以使操作数兼容。某些转换是隐式发生的。例如，MySQL会根据需要自动将字符串转换为数字，反之亦然。以下规则描述了比较操作的转换方式：

两个参数至少有一个是NULL时，比较的结果也是NULL，特殊的情况是使用<=>对两个NULL做比较时会返回1，这两种情况都不需要做类型转换
两个参数都是字符串，会按照字符串来比较，不做类型转换
两个参数都是整数，按照整数来比较，不做类型转换
十六进制的值和非数字做比较时，会被当做二进制串
有一个参数是TIMESTAMP或DATETIME，并且另外一个参数是常量，常量会被转换为timestamp
有一个参数是decimal类型，如果另外一个参数是decimal或者整数，会将整数转换为decimal后进行比较，如果另外一个参数是浮点数，则会把decimal转换为浮点数进行比较
所有其他情况下，两个参数都会被转换为浮点数再进行比较

分析和总结
通过上面的测试我们发现MySQL使用操作符的一些特性：
当操作符左右两边的数据类型不一致时，会发生隐式转换。
当where查询操作符左边为数值类型时发生了隐式转换，那么对效率影响不大，但还是不推荐这么做。
当where查询操作符左边为字符类型时发生了隐式转换，那么会导致索引失效，造成全表扫描效率极低。
字符串转换为数值类型时，非数字开头的字符串会转化为0，以数字开头的字符串会截取从第一个字符到第一个非数字内容为止的值为转化结果。
所以，我们在写SQL时一定要养成良好的习惯，查询的字段是什么类型，等号右边的条件就写成对应的类型。特别当查询的字段是字符串时，等号右边的条件一定要用引号引起来标明这是一个字符串，否则会造成索引失效触发全表扫描。
https://www.cnblogs.com/guitu18/p/12113495.html

drop     删除表（包括表结构和数据
trunacte 无条件全部删除数据
delete   有条件的删除数据

[SQL速学速练](https://www.zhihu.com/column/c_1352655958959734784)

题目（1）有用户表行为记录表t_act_records表，包含两个字段：uid（用户ID），imp_date（日期）
1. 计算2020年每个月，每个用户连续签到的最多天数
2. 计算2020年每个月，连续2天都有登陆的用户名单
3. 计算2020年每个月，连续5天都有登陆的用户数难度：★★★★★
<1> 计算2020年每个月，每个用户连续签到的最多天数考点：
1. 连续时间问题；
2. 时间限定；
3. 聚类第一步：从时间上限定出2020年数据where imp_date between 20200101 and 20201231第二步：解决连续时间问题排序：row_number() over (partition by month(imp_date), uid) as rank 相减：date_diff(imp_date, rank) as sign 第三步：按月聚类求出最大连续签到天数组装构成答案

```sql
select month
    ,uid
    ,max(cnt) 
from (
        select month(imp_date) as month
            ,imp_date
            ,uid
            ,date_sub(imp_date, rank) as sign
            ,count(1) as cnt
        from(
                select uid
                    ,imp_date
                    ,row_number() over (partition by month(imp_date), uid order by imp_date) as rank 
                from t_act_records
                where imp_date between 20200101 and 20201231
            )
            group by month(imp_date)
                ,imp_date
                ,uid
                ,date_sub(imp_date, rank)
        )
group by month
    ,uid
```

<2> 计算2020年每个月，连续2天都有登陆的用户名单考点：1. 连续时间问题；2. 时间限定；3. 聚类不同点：与上题考点相似，唯一不同点为要求连续两天都有登陆count(diff)>=2组装构成答案

```sql
SELECT MONTH
	( imp_date ) AS MONTH,
	uid 
FROM
	(
	SELECT
		uid,
		imp_date,
		date_sub( imp_date, rank ) AS diff 
	FROM
		(
		SELECT
			uid,
			imp_date,
			row_number() over ( PARTITION BY MONTH ( imp_date ), uid ) AS rank 
		FROM
			t_act_records 
		WHERE
			imp_date BETWEEN 20200101 
			AND 20201231 
		) 
	) 
GROUP BY
	MONTH ( imp_date ),
	uid 
HAVING
	count( diff )>= 2;
```

## DATE_SUB()
在 SQL 中，DATE_SUB() 函数用于从给定日期减去指定的时间间隔，生成一个新的日期。它的语法如下：


DATE_SUB(date, INTERVAL value unit)
参数说明：

date：要进行减法运算的日期。
value：要减去的时间间隔的值。
unit：时间间隔的单位，可以是以下值之一：MICROSECOND，SECOND，MINUTE，HOUR，DAY，WEEK，MONTH，QUARTER，YEAR。
这个函数会返回一个新的日期，该日期是通过从给定日期减去指定的时间间隔得到的。如果减去的时间间隔超过给定日期的范围，则返回的结果是 NULL。

以下是一些示例：

减去指定天数：

SELECT DATE_SUB('2023-07-19', INTERVAL 5 DAY);
输出：'2023-07-14'

减去指定月数：

SELECT DATE_SUB('2023-07-19', INTERVAL 3 MONTH);
输出：'2023-04-19'

减去指定年数：

SELECT DATE_SUB('2023-07-19', INTERVAL 1 YEAR);
输出：'2022-07-19'

通过使用 DATE_SUB() 函数，您可以方便地在 SQL 查询中对日期进行减法运算。

sql子查询的例子
1、单行子查询
```sql
select ename,deptno,sal
from emp
where deptno=(select deptno from dept where loc='NEW YORK')；
```
2、多行子查询
```sql
SELECT ename,job,sal
FROM EMP
WHERE deptno in ( SELECT deptno FROM dept WHERE dname LIKE 'A%')；
```
3、多列子查询
```sql
SELECT deptno,ename,job,sal
FROM EMP
WHERE (deptno,sal) IN (SELECT deptno,MAX(sal) FROM EMP GROUP BY deptno)；
```
4、内联视图子查询
(1)SELECT ename,job,sal,rownum
    FROM (SELECT ename,job,sal FROM EMP ORDER BY sal)；
(2)SELECT ename,job,sal,rownum
    FROM ( SELECT ename,job,sal FROM EMP ORDER BY sal)
    WHERE rownum<=5；
5、在HAVING子句中使用子查询
SELECT deptno,job,AVG(sal) FROM EMP GROUP BY deptno,job HAVING AVG(sal)>(SELECT sal FROM EMP WHERE ename='MARTIN')；



## sql标准

SQL92
SQL99
SQL标准是由国际标准化组织（ISO）和美国国家标准学会（ANSI）共同制定的。SQL标准的发展经历了多个版本，以下是其中一些重要的版本：

SQL-86：最初的SQL标准，于1986年发布。
SQL-89：于1989年发布，增加了对视图（views）和域（domains）的支持。
SQL-92（SQL2）：于1992年发布，增加了对事务处理、触发器（triggers）、存储过程（stored procedures）和嵌套子查询的支持。SQL-92是广泛使用的SQL标准版本之一。
SQL-99（SQL3）：于1999年发布，增加了对对象关系特性、XML支持、OLAP操作、递归查询和通用表表达式（Common Table Expressions）的支持。
SQL:2003（SQL4）：于2003年发布，进一步扩展了SQL-99的功能，包括窗口函数（Window Functions）、同义词（Synonyms）和XML相关的增强功能。
SQL:2008（SQL5）：于2008年发布，增加了对行列转换、递归公共表表达式（Recursive Common Table Expressions）、条件表达式（Conditional Expressions）和窗口函数的增强支持。
SQL:2011（SQL6）：于2011年发布，增加了对事务处理、全文搜索、数组和多维数组的支持。
SQL:2016（SQL7）：于2016年发布，增加了对JSON支持、多分区表、并行查询和窗口函数的进一步增强。
这些标准版本中的某些特性可能会随着时间的推移被其他标准或数据库系统采用或弃用。因此，特定的数据库管理系统可能不完全遵循某个特定的SQL标准版本，而是根据自己的需求和实现来选择支持哪些特性和功能。

sqlzoo sql练习网站

```sql
mysql> select * from 't_blog' limit 1;
1064 - You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near ''t_blog' limit 1' at line 1
mysql> select * from "t_blog" limit 1;
1064 - You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '"t_blog" limit 1' at line 1
```

## SQL注释

多行注释
/*

*/

在SQL中，可以使用两个连续的减号（--）来编写单行注释。注释内容应放在两个减号后面，直到该行结束。

以下是一个示例：

```sql
SELECT column1, column2  
FROM table1  
-- 这是一个单行注释  
WHERE condition;
```
在上面的示例中，"-- 这是一个单行注释"是注释，它不会对查询产生任何影响，只是用于说明或解释代码的用途。

REPLACE语句：替代已有的行
INSERT语句的一个变种；
当添加新行时：
1、如果主键值重复，那么就覆盖表中已有的行
2、如果没有主键值重复，则插入该行

[自己实现一个SQL解析引擎](https://blog.csdn.net/kxjrzyk/article/details/79341657)

功能：将用户输入的SQL语句序列转换为一个可执行的操作序列，并返回查询的结果集。 
SQL的解析引擎包括查询编译与查询优化和查询的运行，主要包括3个步骤：

查询分析：
制定逻辑查询计划（优化相关）
制定物理查询计划（优化相关）
查询分析： 将SQL语句表示成某种有用的语法树.
制定逻辑查询计划： 把语法树转换成一个关系代数表达式或者类似的结构，这个结构通常称作逻辑计划。
制定物理查询计划：把逻辑计划转换成物理查询计划，要求指定操作执行的顺序，每一步使用的算法，操作之间的传递方式等。
查询分析各模块主要函数间的调用关系: 

[SQL中Truncate的用法](https://www.cnblogs.com/zhoufangcheng04050227/p/7991759.html)

DQL、DML、DDL、DCL、TCL和MySQL的部分DAL
DQL
select

DML
1) 插入：INSERT
2) 更新：UPDATE
3) 删除：DELETE（删除表中的数据不删除表结构，可以回滚）

DDL
CREATE：创建
ALTER：修改表结构
RENAME：修改表名或列名
DROP：删除表中的数据和结构，删除后不能回滚
TRUNCATE：删除表中的数据不删除表结构，删除后不能回滚，效率比DELETE高

DCL
1) GRANT：授权
2) REVOKE ：回收权限

TCL语句 : 事物控制语句
- 用来维护数据一致性的语句
- 包括：
  - Commit：提交，确认已经进行的数据改变
  - RollBack：回滚，取消已经进行的数据改变
  - SavePoint：保存点，使当前的事务可以回退到指定的保存点，便于取消部分改变


主键可以重复吗?
不可以
关系型数据库的主键是唯一且不能重复的。主键是用于标识表中每一行数据唯一性的字段，它的值在整张表中必须是唯一的，不能有重复。
主键必须满足以下条件：
主键的值不能重复。
主键不能为NULL（即主键字段必须包含数据，不能为空）。
如果在数据库表中主键重复，会导致以下两个主要问题：
数据冲突：数据库中有重复的主键值，这将导致数据混乱，无法正确区分不同的数据，影响数据的准确性。
索引异常：主键是一种特殊的索引，如果主键重复，将无法构建唯一的索引结构，导致索引查询时出现异常，并且会降低查询效率。
因此，正确设置主键可以提高数据库的性能和数据安全性。在创建表时，可以使用PRIMARY KEY关键字来设置主键，例如：CREATE TABLE table_name (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, name VARCHAR(20) NOT NULL);。这将创建一个唯一的主键字段"id"，并且每当插入新记录时，该字段的值会自动递增。

在MySQL中，主键（Primary Key）是唯一标识表中每一行数据的字段。主键的值在表中必须是唯一的，不能有重复。这意味着，如果您尝试插入一个与已存在的主键值相同的新记录，MySQL将会报错并阻止该操作。
如果您需要在表中存储可以重复的值，可以考虑使用唯一索引（Unique Index）或者普通索引（Index）。唯一索引可以包含重复的值，但不允许有空值（NULL）。而普通索引则允许包含重复的值和空值。
另外，如果您需要创建一个可以包含重复主键值的表，可以考虑使用复合主键（Composite Primary Key），它由多个字段组成，并且这些字段的组合值在表中必须是唯一的。
