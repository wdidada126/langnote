# mysql

https://dev.mysql.com/doc/refman/8.3/en/

数据事务并发带来的问题：
脏读(Drity Read)：事务A更新记录但未提交，事务B查询出A未提交记录。
不可重复读(Non-repeatable read): 事务A读取一次，此时事务B对数据进行了更新或删除操作，事务A再次查询数据不一致。
幻读(Phantom Read): 事务A读取一次，此时事务B插入一条数据事务A再次查询，记录多了。
不可重复读和幻读区别：不可重复读在于记录的值，幻读在于记录的数量。

大多数聚合（聚集）函数也可以用作窗口函数；

流程控制函数和操作
CASE	Case operator
IF()	If/else construct
IFNULL()	Null if/else construct
NULLIF()	Return NULL if expr1 = expr2

数字函数和操作
Name	Description
%, MOD	Modulo operator

* Multiplication operator

+ Addition operator

- Minus operator
- Change the sign of the argument
/	Division operator
ABS()	Return the absolute value
ACOS()	Return the arc cosine
ASIN()	Return the arc sine
ATAN()	Return the arc tangent
ATAN2(), ATAN()	Return the arc tangent of the two arguments
CEIL()	Return the smallest integer value not less than the argument
CEILING()	Return the smallest integer value not less than the argument
CONV()	Convert numbers between different number bases
COS()	Return the cosine
COT()	Return the cotangent
CRC32()	Compute a cyclic redundancy check value
DEGREES()	Convert radians to degrees
DIV	Integer division
EXP()	Raise to the power of
FLOOR()	Return the largest integer value not greater than the argument
LN()	Return the natural logarithm of the argument
LOG()	Return the natural logarithm of the first argument
LOG10()	Return the base-10 logarithm of the argument
LOG2()	Return the base-2 logarithm of the argument
MOD()	Return the remainder
PI()	Return the value of pi
POW()	Return the argument raised to the specified power
POWER()	Return the argument raised to the specified power
RADIANS()	Return argument converted to radians
RAND()	Return a random floating-point value
ROUND()	Round the argument
SIGN()	Return the sign of the argument
SIN()	Return the sine of the argument
SQRT()	Return the square root of the argument
TAN()	Return the tangent of the argument
TRUNCATE()	Truncate to specified number of decimal places

日期时间函数 DATE_FORMAT DATE_ADD DATEDIFF 用的多
Name	Description
ADDDATE()	Add time values (intervals) to a date value
ADDTIME()	Add time
CONVERT_TZ()	Convert from one time zone to another
CURDATE()	Return the current date
CURRENT_DATE(), CURRENT_DATE	Synonyms for CURDATE()
CURRENT_TIME(), CURRENT_TIME	Synonyms for CURTIME()
CURRENT_TIMESTAMP(), CURRENT_TIMESTAMP	Synonyms for NOW()
CURTIME()	Return the current time
DATE()	Extract the date part of a date or datetime expression
DATE_ADD()	Add time values (intervals) to a date value
DATE_FORMAT()	Format date as specified
DATE_SUB()	Subtract a time value (interval) from a date
DATEDIFF()	Subtract two dates
DAY()	Synonym for DAYOFMONTH()
DAYNAME()	Return the name of the weekday
DAYOFMONTH()	Return the day of the month (0-31)
DAYOFWEEK()	Return the weekday index of the argument
DAYOFYEAR()	Return the day of the year (1-366)
EXTRACT()	Extract part of a date
FROM_DAYS()	Convert a day number to a date
FROM_UNIXTIME()	Format Unix timestamp as a date
GET_FORMAT()	Return a date format string
HOUR()	Extract the hour
LAST_DAY	Return the last day of the month for the argument
LOCALTIME(), LOCALTIME	Synonym for NOW()
LOCALTIMESTAMP, LOCALTIMESTAMP()	Synonym for NOW()
MAKEDATE()	Create a date from the year and day of year
MAKETIME()	Create time from hour, minute, second
MICROSECOND()	Return the microseconds from argument
MINUTE()	Return the minute from the argument
MONTH()	Return the month from the date passed
MONTHNAME()	Return the name of the month
NOW()	Return the current date and time
PERIOD_ADD()	Add a period to a year-month
PERIOD_DIFF()	Return the number of months between periods
QUARTER()	Return the quarter from a date argument
SEC_TO_TIME()	Converts seconds to 'hh:mm:ss' format
SECOND()	Return the second (0-59)
STR_TO_DATE()	Convert a string to a date
SUBDATE()	Synonym for DATE_SUB() when invoked with three arguments
SUBTIME()	Subtract times
SYSDATE()	Return the time at which the function executes
TIME()	Extract the time portion of the expression passed
TIME_FORMAT()	Format as time
TIME_TO_SEC()	Return the argument converted to seconds
TIMEDIFF()	Subtract time
TIMESTAMP()	With a single argument, this function returns the date or datetime expression; with two arguments, the sum of the arguments
TIMESTAMPADD()	Add an interval to a datetime expression
TIMESTAMPDIFF()	Return the difference of two datetime expressions, using the units specified
TO_DAYS()	Return the date argument converted to days
TO_SECONDS()	Return the date or datetime argument converted to seconds since Year 0
UNIX_TIMESTAMP()	Return a Unix timestamp
UTC_DATE()	Return the current UTC date
UTC_TIME()	Return the current UTC time
UTC_TIMESTAMP()	Return the current UTC date and time
WEEK()	Return the week number
WEEKDAY()	Return the weekday index
WEEKOFYEAR()	Return the calendar week of the date (1-53)
YEAR()	Return the year
YEARWEEK()	Return the year and week

字符串函数

聚集函数
窗口函数

tidb大量使用mysql8中的函数，聚集函数，窗口函数

COALESCE() coalesce 合并 coalesce coalesce coalesce
https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#function_coalesce

Miscellaneous Functions 其他函数
ipv4 字符串 整形相互转换
uuid
uuid_short

order子句语法 多个用逗号连接
order_clause:
    ORDER BY expr [ASC|DESC] [, expr [ASC|DESC]] ...

MySQL四大排名函数(MySQL8版本支持)
一、ROW_NUMBER ()
二、RANK()
三、DENSE_RANK()
四、NTILE()
常用的使用场景： 取每个学科的前3名

这里得区分和ROW_NUMBER()不一样的地方，ROW_NUMBER()是排序，当存在相同成绩的学生时，ROW_NUMBER()会依次进行排序，他们序号不相同，而使用Rank()时，出现相同成绩时，他们的排名是一样的。

centos 7安装mysql server并且修改root密码，ip访问权限
sudo rpm -Uvh https://dev.mysql.com/get/mysql57-community-release-el7-11.noarch.rpm
sudo yum update -y
sudo rpm --import https://repo.mysql.com/RPM-GPG-KEY-mysql-2022
sudo yum install mysql-community-server -y
sudo systemctl enable mysqld
sudo systemctl start mysqld
sudo grep 'temporary password' /var/log/mysqld.log
mysql -u root -p
GwkgoB8Udo(o
UKzuUZIZw4=s
ALTER USER 'root'@'localhost' IDENTIFIED BY '5%Edidadas';
ALTER USER 'root'@'%' IDENTIFIED BY '5%Edidadas';
FLUSH PRIVILEGES;
exit;

CREATE USER 'wdidada'@'*' IDENTIFIED BY '5%Edidadas';
GRANT ALL PRIVILEGES ON *.* TO 'wdidada'@'*';

GRANT ALL PRIVILEGES ON *.* TO 'wdidada'@'%' IDENTIFIED BY '5%Edidadas' WITH GRANT OPTION;
FLUSH   PRIVILEGES;

GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY '5%Edidadas' WITH GRANT OPTION;
FLUSH   PRIVILEGES;

https://blog.csdn.net/qq_37502106/article/details/80207052

如何查看mysql数据库
blob数据的值

navicat 点击
“文本”

aggregate functions ignore NULL values

https://dev.mysql.com/doc/refman/5.7/en/string-functions.html

## 窗口函数 聚集函数

窗口函数概念和语法
窗口函数（Window Functions）是 SQL 中的一个重要概念，用于在数据查询的结果集上执行计算，而这些计算是基于一组相关的行（称为窗口）来进行的，而不是单独地基于每一行。窗口函数允许用户执行诸如运行总计、移动平均等计算，这些计算需要跨越多行数据。
窗口函数通常与 OVER() 子句一起使用，以定义窗口的范围和顺序。OVER() 子句可以包含 PARTITION BY 和 ORDER BY 子句，用于将数据分成不同的分区，并在每个分区内定义行的顺序。
以下是一些常见的窗口函数及其用途：
ROW_NUMBER()：为结果集的每一行分配一个唯一的序号。
RANK() 和 DENSE_RANK()：为结果集的每一行分配一个排名。RANK() 在遇到相同值时会跳过下一个排名，而 DENSE_RANK() 则不会。
NTILE(n)：将结果集分成大致相等的 n 个部分，并为每一行分配一个桶号。
SUM(), AVG(), MIN(), MAX()：这些聚合函数也可以作为窗口函数使用，以计算窗口内行的聚合值。
LEAD() 和 LAG()：访问结果集中当前行的前一行或后一行的值。
FIRST_VALUE() 和 LAST_VALUE()：返回窗口内第一行或最后一行的值。
CUME_DIST()：返回当前行在窗口内的相对位置（作为 0 到 1 之间的值）。
使用窗口函数时，需要注意以下几点：
窗口函数通常与 SELECT 语句一起使用，并且经常与 GROUP BY 子句结合使用，以在分组数据上执行计算。
窗口函数的结果不会改变结果集中的行数，每一行都会有一个对应的窗口函数值。
窗口函数的结果通常依赖于行的顺序，因此在使用窗口函数时，需要确保数据的顺序是正确的，通常通过使用 ORDER BY 子句来实现。
窗口函数为数据分析师和数据库管理员提供了强大的工具，使他们能够执行复杂的计算并深入了解数据的特性和趋势。

https://dev.mysql.com/doc/refman/8.0/en/window-functions-usage.html

SELECT A.USER_ID, A.MONTH,A.STATUS, ROW_NUMBER() over (PARTITION BY USER_ID ORDER BY MONTH DESC,STATUS) RN
                    FROM xxx;

```sql
SELECT
    A.USER_ID,
    A.MONTH,
    A.STATUS,
    ROW_NUMBER() over (PARTITION BY USER_ID
ORDER BY
    MONTH DESC,
    STATUS) RN
FROM
    xxx;
```

```sql
SELECT
    A.USER_ID,
    A.MONTH,
    A.STATUS,
    ROW_NUMBER ( ) over ( PARTITION BY USER_ID
ORDER BY
    MONTH DESC,
    STATUS ) RN
FROM
    (
    SELECT
        USER_ID,
        DATE_FORMAT(CONCAT(MONTH, '-', '01'), '%Y-%m') MONTH,
        STATUS
    FROM
        ${defaultSchema}.T_RECORD_FUND_TD
    WHERE
        ETP_ID =
        #{enterpriseId} ) A
```
给临时表起名字

https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html
MySQL中的窗口函数有很多，以下是一些常见的窗口函数：

ROW_NUMBER()：为每个窗口中的行分配一个唯一的序号，通常用于对窗口中的行进行排序。
RANK()：为每个窗口中的行分配一个排名值，根据窗口中的排序规则进行排名。
DENSE_RANK()：与RANK()相似，但在并列排名时，Dense_Rank()将为并列排名分配相同的排名，而RANK()将为并列排名分配不同的排名。
NTILE()：将窗口中的行分成指定数量的组，并为每个组分配一个百分比值。
LAG()：返回窗口中当前行的前一行（或指定行）的值。
LEAD()：返回窗口中当前行的下一行（或指定行）的值。
SUM()、AVG()、MAX()、MIN()等聚合函数：可以与OVER()子句一起使用，对窗口中的行执行聚合计算。
COALESCE()：用于在窗口函数中指定默认值，以便在计算中处理NULL值。
AVG_IF()、SUM_IF()等条件聚合函数：这些函数允许您在聚合计算中添加条件。
GROUP_CONCAT()：将窗口中的值连接成一个字符串，并使用指定的分隔符进行分隔。
这些只是MySQL窗口函数的一部分，还有很多其他的窗口函数可用。如果您想了解所有可用的窗口函数，可以参考MySQL官方文档。

## QEP

QEP是MySQL的一个术语,全称是Query Execution Plan,即查询执行计划。
QEP描述了MySQL服务器如何解析和执行特定的SQL查询语句的计划。

当MySQL收到SQL语句时,它会做以下工作:
1. 解析和验证SQL语句的语法
2. 生成查询执行计划(QEP)
3. 根据QEP执行查询操作
4. 返回查询结果

其中生成QEP是关键步骤。
QEP决定了MySQL将会如何执行查询:
- 是否使用索引
- 访问的表顺序
- 针对每个表使用的访问类型
- 需要多少行扫描

这些信息都包含在QEP中。
所以QEP实际上就是MySQL如何最有效利用资源执行查询的蓝图。
通过一个叫 `EXPLAIN`的SQL语句,我们可以查看MySQL的执行计划,了解它的QEP。

例如:
```sql
EXPLAIN SELECT * FROM users WHERE id = 1;
```

EXPLAIN会返回QEP相关信息,从中我们可以分析出:
- MySQL将使用哪个索引
- 预计需要扫描的行数
- 访问类型等等

通过分析QEP,我们就能分析查询性能,进而优化查询。
mysql查看所有表的所有字段

```sql
SELECT 
    COLUMNS .column_name, 
    COLUMNS .column_comment, 
    COLUMNS .TABLE_NAME, 
    TABLES .table_comment 
FROM 
    information_schema. COLUMNS COLUMNS 
LEFT JOIN information_schema. TABLES TABLES ON TABLES .TABLE_NAME = COLUMNS .TABLE_NAME 
WHERE 
    COLUMNS .table_schema = 'paps' 
AND COLUMNS .table_name LIKE 'paps%';
```

聚合函数
max 没有group by的情况下使用
MySQL中提供了多种聚合函数，包括：

- AVG()：计算平均值。
- SUM()：计算总和。
- MAX()：返回最大值。
- MIN()：返回最小值。
- COUNT()：计算指定字段在查询结构中出现的个数。

MySQL的AVG()函数在计算平均值时，会将NULL和0等值视为无效值，不会纳入计算范围。如果需要包括这些无效值，可以使用IFNULL()或COALESCE()函数将这些无效值转换为0或其他有效值。例如：

```
SELECT AVG(IFNULL(column_name, 0)) FROM table_name;
```

或者

```
SELECT AVG(COALESCE(column_name, 0)) FROM table_name;
```

这样可以将NULL和0等无效值转换为0，然后再计算平均值。

这个说法是正确的。在SQL中，聚合函数（如MAX()、MIN()、SUM()等）通常与GROUP BY子句一起使用，以便对查询结果进行分组和汇总。
当使用聚合函数时，如果没有指定GROUP BY子句，则会出现错误。这是因为聚合函数的目的是将数据按照指定的列进行分组，并对每个组应用相应的聚合函数。
以下是一个示例，展示了在GROUP BY子句中使用聚合函数的情况：

```sql
SELECT category, MAX(price) AS max_price
FROM products
GROUP BY category;
```

在这个例子中，我们选择了"category"列，并使用MAX()函数计算了每个类别中的最高价格。通过GROUP BY子句，我们将结果按照"category"列进行了分组。
如果你尝试在没有GROUP BY子句的情况下直接使用MAX()函数，就会出现错误。因此，在使用聚合函数之前，请确保你的查询中包含了适当的GROUP BY子句，以指定数据的分组方式。

select max(sell_qty) from fi_jm_wholesale_accountcheck where cancelsign = 'N';
聚合函数MAX()用于返回查询结果中指定列的最大值。

dual
DUAL是MySQL中的一个虚拟表，用于在没有表的情况下指定一个虚拟的表名。DUAL表的作用主要有以下几点：
1. 用于计算表达式。在使用SELECT语句时，我们可以在FROM子句中使用dual表来计算一些简单的表达式。
2. 用于生成一个单行数据。可以使用SELECT语句从dual表中选择一条记录，这对于测试和调试非常有用。
3. 用于生成一个常量值。可以使用SELECT语句从dual表中选择一个常量值，这对于生成随机数或种子值非常有用。

sql，用于运维
select version()
select version() from dual

在Mysql和SQL Server中可以直接select 1不需要加from表名就可以执行
mysql是支持Dual的

select 1
select 1 from dual

## MySQL CAST() Function

cast as int
cast as s 字符串

cast as decimal

https://dev.mysql.com/doc/refman/5.7/en/cast-functions.html

MySQL CAST() Function
https://www.w3schools.com/sql/func_mysql_cast.asp

MySQL字符串转int/double CAST与CONVERT函数的用法
https://blog.csdn.net/m0_37479246/article/details/79077143

CAST(value as type);
CONVERT(value, type);
MySQL的CAST()和CONVERT()函数可用来获取一个类型的值，并产生另一个类型的值。两者具体的语法如下：
MySQL软件支持的字符串函数表如下：

| 函数                       | 功能                                                          |
| -------------------------- | ------------------------------------------------------------- |
| CONCAT(str1,str2,...,strn) | 将str1,str2,...,strn连接为一个完整的字符串                    |
| INSERT(str,x,y,instr)      | 将字符串str从第x开始，y个字符串长度的子串替换为字符串instr    |
| LOWER(str)                 | 将字符串str中的所有字母变成小写                               |
| UPPER(str)                 | 将字符串str中的所有字母变成大写                               |
| LEFT(str,x)                | 返回字符串最左边的x个字符                                     |
| RIGHT(str,x)               | 返回字符串最右边的x个字符                                     |
| LPAD(str,n,pad)            | 使用字符串pad对字符串str最左边进行填充，直到长度为n个字符长度 |
| RPAD(str,n,pad)            | 使用字符串pad对字符串str最右边进行填充，直到长度为n个字符长度 |
| LTRIM(str)                 | 去掉str左边的空格                                             |
| RTRIM(str)                 | 去掉str右边的空格                                             |
| REPEAT(str,x)              | 返回字符串str重复x次的结果                                    |
| REPLACE(str,a,b)           | 使用字符串b替换字符串str中所有出现的字符串a                   |
| STRCMP(str1,str2)          | 比较字符串str1和str2                                          |
| TRIM(str)                  | 去掉字符串行头和行尾的空格                                    |
| SUBSTRING(str,x,y)         | 返回字符串str中从x位置起y个字符串长度的字符串                 |

华为ddm
5.6.29_ddm_3.0.6.3_f02d9f07a301c1eca1e666f4840badfc6458c89e_20211127

## mysql支持的数据类型 5.7为例

11.1 Numeric Data Types
11.2 Date and Time Data Types
11.3 String Data Types
11.4 Spatial Data Types
11.5 The JSON Data Type
11.6 Data Type Default Values
11.7 Data Type Storage Requirements
11.8 Choosing the Right Type for a Column
11.9 Using Data Types from Other Database Engines

数字
日期和时间
字符
空间数据
json
默认值

11.1 Numeric Data Types

11.1.1 Numeric Data Type Syntax
11.1.2 Integer Types (Exact Value) - INTEGER, INT, SMALLINT, TINYINT, MEDIUMINT, BIGINT
11.1.3 Fixed-Point Types (Exact Value) - DECIMAL, NUMERIC
11.1.4 Floating-Point Types (Approximate Value) - FLOAT, DOUBLE
11.1.5 Bit-Value Type - BIT
11.1.6 Numeric Type Attributes
11.1.7 Out-of-Range and Overflow Handling

INTEGER, INT, SMALLINT, TINYINT, MEDIUMINT, BIGINT
DECIMAL, NUMERIC
FLOAT, DOUBLE
BIT

11.2 Date and Time Data Types

11.2.1 Date and Time Data Type Syntax
11.2.2 The DATE, DATETIME, and TIMESTAMP Types
11.2.3 The TIME Type
11.2.4 The YEAR Type
11.2.5 2-Digit YEAR(2) Limitations and Migrating to 4-Digit YEAR
11.2.6 Automatic Initialization and Updating for TIMESTAMP and DATETIME
11.2.7 Fractional Seconds in Time Values
11.2.8 What Calendar Is Used By MySQL?
11.2.9 Conversion Between Date and Time Types
11.2.10 2-Digit Years in Dates

DATE, DATETIME, and TIMESTAMP
TIME
YEAR

11.3 String Data Types

11.3.1 String Data Type Syntax
11.3.2 The CHAR and VARCHAR Types
11.3.3 The BINARY and VARBINARY Types
11.3.4 The BLOB and TEXT Types
11.3.5 The ENUM Type
11.3.6 The SET Type

CHAR
VARCHAR
BINARY
VARBINARY
BLOB
TEXT
ENUM
SET

https://dev.mysql.com/doc/refman/5.7/en/data-types.html

## 核心概念

### 存储引擎

innodb myasam

### mvcc
innodb自带的，不能舍弃不要

### MVCC的两种读形式 当前读 快照读

### Query Execution Plan,即查询执行计划。

### 幻读
幻读（Phantom Read）是一种在事务执行过程中，由于其他事务的插入或删除操作，导致当前事务读取到的行数发生了变化的现象。幻读通常发生在范围查询（如SELECT * FROM table WHERE column BETWEEN value1 AND value2）中。

### 间隙锁(Next-Key Locking)
Gap Lock确实是一种锁的算法。它是InnoDB存储引擎在行级锁定中使用的三种算法之一，另外两种是Record Lock和Next-Key Lock。
Gap Lock主要锁定一个范围，但不包含记录本身。它的主要作用是阻止多个事务将记录插入到同一范围内，从而防止幻读现象的发生。当查询的索引为辅助索引时，InnoDB会对前一个辅助索引节点加Next Key Lock，对索引下一个键值加Gap Lock。
因此，Gap Lock是InnoDB用于实现高并发性和数据一致性的重要机制之一。需要注意的是，正确理解和使用这些锁算法对于优化数据库性能和避免并发问题至关重要。
Gap Lock、Record Lock和Next-Key Lock的汉语翻译分别为：
Gap Lock：间隙锁
Record Lock：记录锁
Next-Key Lock：临键锁
这些术语是InnoDB存储引擎在行级锁定中使用的锁算法。间隙锁主要锁定一个范围，但不包含记录本身，用于防止幻读现象的发生。记录锁则是锁定单个记录。临键锁是记录锁与间隙锁的结合，它锁定一个记录以及该记录前的间隙。这些锁算法有助于确保并发事务中的数据一致性和正确性。

### 执行计划
MySQL执行计划对应的英文是"Execution Plan"。
### Phantom Problem 幻读

### 意向锁

### 存储引擎

myisam
innodb

### 隐式事务 显式事务

对于单条SQL语句，数据库系统自动将其作为一个事务执行，这种事务被称为隐式事务。
要手动把多条SQL语句作为一个事务执行，使用BEGIN开启一个事务，使用COMMIT提交一个事务，这种事务被称为显式事务

sql 统计 体系 优化查询时间
避免用null
https://dzone.com/articles/how-to-optimize-mysql-queries-for-speed-and-perfor

MySQL
sysbench测试 腾讯云主机

mysql

varchar 字符串长度需要注意
索引 char like %xx%看执行计划 不走

架构之路 raod5858
mysql 毛剑相关的文章

MySQL MongoDB慢SQL分析，尝试提出解决方案

pt
mongod.log

mysql vip 两个mysql节点，互为主从
java程序连接其中一个
keepalived

https://blog.csdn.net/yabingshi_tech/article/details/50721841

两个mysql程序端口都是3307

KeepAlive VIP 配置高可用 Nginx 主备集群
https://blog.csdn.net/shida_csdn/article/details/80739859
https://www.cnblogs.com/yuanermen/p/3735263.html

## 书籍

Effective MySQL之SQL语句最优化
Understanding MySQL Internals
千金良方mysql性能优化
深入理解MySQL
深入理解MySQL核心技术
https://blog.souche.com/mysql_optimize/

## xa

TP 事务处理
DTP 分布式事务处理
MySQL从5.0.3版本开始支持XA分布式事务，并且只有InnoDB存储引擎支持。XA是X/Open分布式事务处理(DTP)模型的一部分，在MySQL中，XA事务基本语法包括XA START、XA END、XA PREPARE、XA COMMIT和XA ROLLBACK等命令。

请注意，以上信息仅涵盖了MySQL对XA的支持，并不包括其他数据库或存储系统的支持情况。如果您在使用不同的数据库系统或存储引擎，建议您查阅相应文档以获取准确信息。

MySQL join
图解MySQL 内连接、外连接、左连接、右连接、全连接
https://blog.csdn.net/plg17/article/details/78758593

mysql索引使用b+树实现，或者用hash实现
mysql为什么使用B+树实现，不用b树实现？
B+树 可以实现范围查询

MySQL 使用 B+ 树作为索引结构，而不是 B 树，主要是因为 B+ 树更适合数据库中的大规模数据存储和检索。以下是 B+ 树相比 B 树在数据库应用中的主要优势：

1. 磁盘友好：B+ 树相比于 B 树更磁盘友好。B 树在更新时可能需要移动大量数据，而 B+ 树由于其特性，更新时只需移动少量的数据。因此，B+ 树更适合磁盘读写操作，这在数据库系统中非常重要。
2. 数据压缩：由于 B+ 树的叶子节点是顺序存储的，因此它们可以通过指针相连，形成一个链表结构。这个特性使得 B+ 树的叶子节点可以在内存中进行压缩，从而节省存储空间并减少 I/O 操作。
3. 高查询性能：B+ 树的查询性能通常比 B 树更高。在 B+ 树中，数据按照键值顺序存储，这使得查找和范围查询操作更加高效。特别是在范围查询中，B+ 树只需遍历叶子节点链表即可，而 B 树可能需要多次查找和遍历。
4. 数据稳定性：B+ 树相比于 B 树具有更好的数据稳定性。由于 B+ 树的叶子节点是顺序存储的，并且每个节点包含指向下一个和上一个叶子节点的指针，因此即使发生崩溃或断电等意外情况，数据也可以更快地恢复。

总之，MySQL 选择使用 B+ 树而不是 B 树来实现索引，主要是因为B+树更适合数据库系统中的大规模数据存储和检索，具有更好的磁盘友好性、数据压缩能力、高查询性能以及数据稳定性。

子节点 关键字

在B+树中，度（degree）是指每个非根节点（除了叶子节点）所包含的子节点的最小数量。度是B+树的一个重要参数，它决定了B+树的分支因子和节点的容量。
具体来说，对于一个度为 `d`的B+树：

1. 非根节点（除了叶子节点）至少有 `d` 个子节点。
2. 非根节点的关键字个数（除了叶子节点）可以是 `d-1` 到 `2d-1` 之间。
3. 叶子节点可以包含 0 到 `2d-1` 个关键字。
   度的选择会影响 B+ 树的高度、磁盘访问次数和节点的利用率。较大的度可以减少树的高度，从而减少磁盘访问次数，但会增加节点的大小和内存开销。较小的度可以提高节点的利用率，减少内存开销，但会增加树的高度和磁盘访问次数。
   通常，在实际应用中，度的选择需要根据具体的场景和数据量进行权衡。常见的度取值为50、100或更大，但具体的最佳取值需要根据实际需求和性能测试来确定。

## 表支持的数据类型

tinyint
int
bitint
varchar
text
date
datetime
timestamp

约束
int你输入汉字会报错
正数，负数

oracle数据库是个平台，你可以在上面写存储过程来对数据进行处理
plsql pljson框架

## mysql datetime如何比较大小？

在MySQL中，可以使用比较运算符（<、>、<=、>=、==、!=）来比较datetime值的大小。
例如，假设有两个datetime列date1和date2，可以使用以下语句比较它们的大小：

```sql
SELECT * FROM table_name WHERE date1 > date2;
```

这将返回table_name表中所有date1大于date2的记录。
还可以使用其他比较运算符进行比较，例如：

```
SELECT * FROM table_name WHERE date1 < date2; -- 返回所有date1小于date2的记录  
SELECT * FROM table_name WHERE date1 >= date2; -- 返回所有date1大于等于date2的记录  
SELECT * FROM table_name WHERE date1 <= date2; -- 返回所有date1小于等于date2的记录  
SELECT * FROM table_name WHERE date1 == date2; -- 返回所有date1等于date2的记录  
SELECT * FROM table_name WHERE date1 != date2; -- 返回所有date1不等于date2的记录
```

请注意，datetime比较是基于时间戳进行的，因此在进行比较时，需要考虑时间戳的位置。

时间的精度

时分秒 毫秒 微秒 纳秒

date_format()

quanyi 公司java源代码里面有

```sql
AND ? = DATE_FORMAT(day,'%Y-%m-%d')
sql.append(" and create_dtme<= DATE_FORMAT('" + request.getEDate() + " 23:59:59" + "','%Y-%m-%d %H:%i:%s') ");

```

在MySQL 5.7中，可以使用以下日期格式：

- DATE：格式为'YYYY-MM-DD'，例如'2023-02-27'
- DATETIME：格式为'YYYY-MM-DD HH:MM:SS'，例如'2023-02-27 12:30:45'
- TIMESTAMP：格式为'YYYY-MM-DD HH:MM:SS'，例如'2023-02-27 12:30:45'
- YEAR：格式为'YYYY'，例如'2023'

另外，MySQL还提供了一些日期函数来操作和格式化日期，例如：

- DATE_FORMAT(date,format)：将日期格式化为指定的格式。
- NOW()：返回当前日期和时间。
- CURDATE()：返回当前日期。
- CURTIME()：返回当前时间。

例如，可以使用以下查询来获取当前日期和时间的格式化值：

SELECT DATE_FORMAT(NOW(), '%Y-%m-%d %H:%i:%s');

m代表month 月份

https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_date-format

mysql_5_7_date_format.xlsx

注意 月份 M m的区别 M是月份的英文字母 m是数字

小时 H h的区别 H 0-23 h 0-12

## sql中 count() sum() avg() max() min()是不是函数？

group by才能使用的函数

聚合函数不能嵌套调用。比如不能出现类似“AVG(SUM(字段名称))”形式的调用。

使用GROUP BY关键字结合聚合函数将数据进行分组
聚合函数作用于一组数据，并对一组数据返回一个值。

MySQL提供了许多聚合函数，包括AVG()，COUNT()，SUM()，MIN()，MAX()等。除COUNT函数外，其它聚合函数在执行计算时会忽略NULL值。
聚合函数是多对一函数。它们使用来自多个记录的值作为输入，并将这些值转换为一个值来汇总所有记录。Sum(),Count(),Avg(),Min(),和Only()都是聚合函数。

https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html
https://blog.51cto.com/xdr630/5104122

非法使用聚合函数：不能在WHERE子句中使用聚合函数。

select veresion() from dual;
select now() from dual;

聚集函数
窗口函数

如果想要在表中使用自动更新时间戳功能，可以将TIMESTAMP类型字段的默认值设置为CURRENT_TIMESTAMP，每次插入或更新记录时都会自动更新该字段的值。

表字段设计是数据库设计中的一个重要方面，它决定了表的结构和数据存储的方式。以下是一些表字段设计的考虑因素：
数据类型：每个字段都需要选择合适的数据类型，以确保存储和检索数据的效率和正确性。常用的数据类型包括整型、浮点型、日期型、字符型等。
字段长度：对于字符型数据，需要确定其长度，以便在存储和检索时节省空间和时间。
空值处理：对于一些字段，可能存在空值的情况，需要考虑如何处理空值。一般有两种处理方式：允许空值或者不允许空值。
默认值：可以为表中的字段设置默认值，当插入数据时如果未给出该字段的值，则会使用默认值。
索引：对于经常用于查询的字段，可以为其创建索引，以加速查询。
主键：每个表需要有一个主键，以确保每行数据都能够唯一标识。
外键：如果一个表中的字段需要引用另一个表中的字段，需要使用外键来建立关联关系。
命名规范：为了保证代码的可读性和可维护性，需要为每个字段选择一个合适的名称，并遵循一定的命名规范。
数据一致性：需要确保表中的字段设计和应用程序代码中的使用保持一致，以避免数据不一致的问题。
综上所述，表字段设计需要考虑多个因素，以保证数据的存储和检索效率和正确性，并且确保数据的一致性和可维护性。

在MySQL中，使用EXPLAIN关键字可以查看一个查询语句的执行计划，从而分析查询语句的性能问题。其中，EXPLAIN中的type列反映了MySQL在查询过程中选择了何种访问方式，MySQL的访问方式可以分为以下几种：

ALL：全表扫描，遍历全表进行查找。
index：全索引扫描，遍历索引表进行查找。
range：范围查询，使用索引查找指定范围内的记录。
ref：使用非唯一索引查找单个值。
eq_ref：使用唯一索引查找单个值。
const：使用主键索引查找单个值，一般是在主键或唯一索引上的查询。
system：特殊情况下使用的访问方式，例如查询mysql库的信息_schema表。
其中，type列的值越优越好。而当查询语句的执行计划中type列为range时，表示使用了范围查询。这种情况下，我们可以采取以下优化措施：

创建索引：在查询语句的WHERE条件中包含索引列，使用最左前缀原则创建索引，或者创建覆盖索引，可以提高查询效率。
减少查询范围：通过调整WHERE条件、使用限制查询的子句如LIMIT、使用索引覆盖查询等方式，缩小查询范围，提高查询效率。
优化查询语句：在保证查询结果正确的前提下，尽可能的精简查询语句，减少不必要的JOIN操作等，提高查询效率。
总之，针对MySQL中慢查询的优化，我们需要结合具体的业务场景和查询语句的特点，采取合适的优化策略。

MySQL慢查询优化一般有以下思路：
使用合适的索引：对于经常查询的字段，可以通过创建适当的索引来提高查询性能。索引可以加速查询，但是过多的索引也会影响更新和写入操作的性能。
优化查询语句：尽可能使用简单的查询语句，避免使用复杂的连接和子查询，同时要避免使用SELECT *。
减少扫描行数：尽可能使用覆盖索引来减少需要扫描的行数。同时可以通过LIMIT、分页、缓存等手段来减少扫描行数。
拆分大表：如果一个表数据量过大，可以将其拆分为多个小表，每个表的数据量更小，查询速度更快。
合理分配硬件资源：在优化查询性能时，还需要考虑系统的硬件资源。如果服务器硬件资源不足，即使对查询进行优化也无法提高查询速度。
定期维护数据库：对于大型的数据库系统，需要定期进行维护，包括备份、优化、压缩、重建索引等操作。

MySQL 5.7自带了一些优化工具，包括：
MySQL Workbench：可以通过可视化界面分析查询性能和优化数据库架构；
MySQL Enterprise Monitor：可以监控和分析MySQL数据库的性能和运行状况，以及自动化管理和调整数据库；
MySQL Enterprise Backup：可以进行完全备份和增量备份，并支持恢复到特定的时间点；
MySQL Query Analyzer：可以在生产环境中进行实时查询性能分析，以及进行SQL优化建议；
MySQL Performance Schema：可以提供丰富的性能统计信息，包括锁定、I/O、CPU、内存、网络等方面的数据；
MySQL sys schema：提供了更加简洁易读的性能统计信息，可以帮助用户更快速地找到慢查询和优化方案；
MySQL Tuner：一个开源的脚本工具，可以帮助用户快速找到MySQL配置和运行中的问题，并给出优化建议。
除此之外，还有很多第三方的MySQL优化工具，例如Percona Toolkit、pt-query-digest、Mytop等等。

Phantom Problem 幻读

mysql索引实现方式，根据存储引擎的不同而不同
myisam hash
innodb b+

正确，InnoDB引擎确实支持B+树索引，但并不支持哈希索引。

InnoDB是MySQL的默认存储引擎，它使用B+树作为索引模型，主要原因在于B+树的特性能够有效地支持数据库的各项操作，如范围查询、排序等。
B+树索引可以按照特定的顺序遍历索引中的内容，对于排序和范围查询等操作，相比于哈希索引，B+树能带来更好的性能。因为哈希函数的主要目的是将数据尽可能分散到不同的桶中进行存储，所以在遇到可能存在相同键值或者需要排序以及范围查询的情况时，哈希索引可能需要全表扫描，这在数据库查询中可能会产生性能瓶颈。

mysql没有主键自动加列

如何保证redis缓存后端db的数据一致性
消息队列，保证接收者按照一定顺序消费消息
慢索引优化

B树和B+树都是常用的数据库索引结构，它们主要的区别在于节点存储的键值数和指向子节点的指针数。
B树的节点中既存储着关键字，也存储着指向子节点的指针。一个节点可以存储多个关键字和对应的子节点指针，且节点的大小可以根据需要进行调整。B树的节点可以存储的关键字数范围为t-1到2t-1，其中t是B树的阶（即节点中指针的最大数量）。B树的查找性能较高，因为在一个节点中可能会包含要查找的关键字，从而减少了磁盘I/O操作的次数。
B+树的节点中仅存储着关键字，而指向子节点的指针都保存在叶子节点上。叶子节点形成了一个单向链表，通过链表连接起来的所有叶子节点可以直接访问整个B+树中的所有数据。B+树的内部节点只用于索引，不保存真正的数据，因此可以更大更稠密地存储关键字。B+树的叶子节点可以存储的关键字数范围为t到2t，其中t是B+树的阶。B+树的查找性能比B树更好，因为在查找数据时只需要遍历叶子节点即可。
因此，B+树在大型数据库中得到广泛应用，特别是在需要支持高效范围查询的场景中，而B树则更适合存储少量数据的场景。

从dba或者源码的角度，各种排查

好在从MySQL 5.7版本开始提供了performance_schema.metadata_locks表，该表记录了各种Server层的锁信息（包括全局读锁和MDL锁等信息）

MySQL源代码：从SQL语句到MySQL内部对象
https://www.orczhou.com/index.php/2012/11/mysql-innodb-source-code-optimization-1/

mysql sql_yacc.yy 命令行生成代码

如何在修改mysql代码添加新SQL命令

flex/bison与antlr的联系与区别

可执行程序
flex bison
anltr.bat

.l .y
.g4

c、c++代码嵌入.y文件，自定义头文件。各种内置函数
l y .a库

yyparse
localytext

listener visit模式
antlr-runtime 库

antlr flex/bison都可以实现计算器

### IDEA gateway

你和答主说的不是同一个东西 答主说的是新的gateway 你说的是deployment

unicoude云服务器错误，没有4G剩余空间

## 源代码sql解析

miniob ob数据库跟华中科技合作的数据库竞赛 使用了flex bison

mysql使用 .yy .ll

sql_yacc.yy
sql_hints.yy
MySQL内核源码解读-SQL解析一
https://blog.51cto.com/wangwei007/2300217

京东商城数据库技术部傅志宇
MySQL内核源码解读-SQL解析之解析器浅析
https://blog.51cto.com/wangwei007/2300959
京东商城数据库技术部郭光欣

编译原理 极客时间 宫

mvcc 多版本并发控制
java代码实现
https://blog.csdn.net/weixin_29132813/article/details/114537588

https://github.com/edidada/MYDB

yes的练级攻略

mysql 锁的
https://zhuanlan.zhihu.com/p/393683080

    CREATE TABLE`yes` (
	  `id` bigint(20) NOT NULL AUTO_INCREMENT,
	  `name` varchar(45) DEFAULT NULL,
	  `address` varchar(45) DEFAULT NULL,
	  PRIMARY KEY (`id`)
	) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4

查看事务隔离级别 mysql5.7.20 之后
show variables like 'transaction_isolation';
SELECT @@transaction_isolation;

mysql5.7.20 之前
SELECT @@tx_isolation;
show variables like 'tx_isolation';

https://blog.csdn.net/weixin_40964170/article/details/114958297

CREATE TABLE `yes`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `address` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

INSERT INTO `yes` VALUES (1, 'yes', 'hz');
INSERT INTO `yes` VALUES (2, 'xx', 'hz');
INSERT INTO `yes` VALUES (3, 'aa', 'd');

select * from yes where name = 'yes' for update;
select * from yes where name = 'xx' for update;

开启事务？

## mysql 日志

redo log
undo log
bin log

又一个是存储改变之前的数据，改变之后的数据
区别如下： redo log 是InnoDB 引擎特有的；binlog 是MySQL 的Server 层实现的，所有引擎都可以使用。 redo log 是物理日志，记录的是“在某个数据页上做了什么修改”；binlog 是逻辑日志，记录的是这个语句的原始逻辑。
https://segmentfault.com/a/1190000023827696

[MySQL]源码角度看redo log
https://www.dazhuanlan.com/alaskawind/topics/1167481

自己实现innodb wal机制？
总的来说，MySQL中事务的原子性是通过 undo log 来实现的，事务的持久性性是通过 redo log 来实现的，事务的隔离性是通过读写锁+MVCC来实现的。

https://www.modb.pro/db/234350
http://catkang.github.io/2020/02/27/mysql-redo.html

实验课
https://gitee.com/edidada/naivedb
https://www.writebug.com/git/goodwill/NaiveDB
NaiveDB 是一个关系数据库管理系统，采用客户端/服务器架构。主要分为存储模块、查询模块、元数据管理模块、事务模块(https://www.writebug.com/git/goodwill/NaiveDB)
NaiveDB:清华软院大三下《数据库原理》大作业
找测试用例

https://github.com/cmu-db/bustub
https://github.com/duckdb/duckdb

##### 事务模块

* 服务器支持多客户端并发
* 实现 begin transaction 和 commit。
* 使用二级锁协议，实现 read committed 隔离级别。
* 实现单一事务的 WAL 机制，可以读写 log 并恢复数据。
* 完善数据库存储模块与 bug 修改。

## MySQL中有7种日志文件

1. 重做日志（redo log）
2. 回滚日志（undo log)
3. 二进制日志（bin log）
4. 错误日志（error log）
5. 慢查询日志（slow query log）
6. 一般查询日志（general log）
7. 中继日志（relay log）

https://github.com/bingoohuang/blog/issues/137

redo日志文件名格式为 ib_logfile0或ib_logfile1
可使用find命令模糊查找
在Apache Ratis项目中，实现了一种更为高效的WAL机制
WAL会被删除吗
如果WAL内的transaction已经被成功apply到状态机里去了，就可以被删除掉了

[Rocksdb的WAL实现底层探索](https://blog.csdn.net/Z_Stand/article/details/108025338)

update 一次更新多条数据，或者不是一条数据
根据主键来更新
方案1，先查询，只有一条再更新

mysql server日志，显示封锁

数据库4种隔离级别与3级封锁协议
MySQL事务提出了4个不同的隔离级别，而这些隔离级别的实现本质上就是通过加锁，解锁来实现的。
https://blog.csdn.net/weixin_44795128/article/details/119825139

lock in share mode
for update
说到共享锁和排他锁，就会想到悲观锁，这两个都属于数据库带的悲观锁，乐观锁不是数据库带的。

乐观锁：可以给表加一个version字段，先查询version字段放在缓存里，每次修改之前，在查询一次version字段，若跟缓存里的数值不一致，则回滚。

https://zhuanlan.zhihu.com/p/372090999

https://blog.csdn.net/gklifg/article/details/38752691

意向锁
对任何一个结点加锁时，必须先对它的上层结点加意向锁。

三种常用的意向锁：
1）意向共享锁（IS锁）：
对一个数据对象加IS锁，表示它的后裔结点拟（意向）加S锁。
事务T1对数据对象A加上IS锁后，事务T2可以继续加除X锁以外的锁。
2）意向排他锁（IX锁）：
对一个数据对象加IX锁，表示它的后裔结点拟（意向）加X锁。
事务T1对数据对象A加上IX锁后，事务T2只能继续加IS或IX锁。
3）共享意向排他锁（SIX = S+IX锁）：
对一个数据对象先加S锁，再加IX锁。例如对某个表加SIX锁，则表示该事务要读（S）整个表，同时会更新（IX
）个别元组。
https://blog.csdn.net/Ha1f_Awake/article/details/84994697

X > SIX > S / IX > IS

Mysql 插入意向锁
https://blog.csdn.net/u010648194/article/details/123659594

三、锁的分类。
数据库里有的锁有很多种，为了方面理解，所以我根据其相关性"人为"的对锁进行了一个分类，分别如下
基于锁的属性分类：共享锁、排他锁。
基于锁的粒度分类：表锁、行锁、记录锁、间隙锁、临键锁。
基于锁的状态分类：意向共享锁、意向排它锁。
1、属性锁
共享锁(Share Lock)
共享锁又称读锁，简称S锁；当一个事务为数据加上读锁之后，其他事务只能对该数据加读锁，而不能对数据加写锁，直到所有的读锁释放之后其他事务才能对其进行加持写锁。
共享锁的特性主要是为了支持并发的读取数据，读取数据的时候不支持修改，避免出现重复读的问题。
排他锁(eXclusive Lock)
排他锁又称写锁，简称X锁；当一个事务为数据加上写锁时，其他请求将不能再为数据加任何锁，直到该锁释放之后，其他事务才能对数据进行加锁。
排他锁的目的是在数据修改时候，不允许其他人同时修改，也不允许其他人读取。避免了出现脏数据和脏读的问题。
2、粒度锁
表锁
表锁是指上锁的时候锁住的是整个表，当下一个事务访问该表的时候，必须等前一个事务释放了锁才能进行对表进行访问；
特点： 粒度大，加锁简单，容易冲突；
行锁
行锁是指上锁的时候锁住的是表的某一行或多行记录，其他事务访问同一张表时，只有被锁住的记录不能访问，其他的记录可正常访问；
特点：粒度小，加锁比表锁麻烦，不容易冲突，相比表锁支持的并发要高；
记录锁(Record Lock)
记录锁也属于行锁中的一种，只不过记录锁的范围只是表中的某一条记录，记录锁是说事务在加锁后锁住的只是表的某一条记录。
触发条件：精准条件命中，并且命中的条件字段是唯一索引；
例如：update user_info set name=’张三’ where id=1 ,这里的id是唯一索引。
记录锁的作用：加了记录锁之后数据可以避免数据在查询的时候被修改的重复读问题，也避免了在修改的事务未提交前被其他事务读取的脏读问题。

间隙锁(Gap Lock)
间隙锁属于行锁中的一种，间隙锁是在事务加锁后其锁住的是表记录的某一个区间，当表的相邻ID之间出现空隙则会形成一个区间，遵循左开右闭原则。
比如下面的表里面的数据ID 为 1,4,5,7,10 ,那么会形成以下几个间隙区间，-n-1区间，1-4区间，7-10区间，10-n区间 (-n代表负无穷大，n代表正无穷大)
触发条件：范围查询并且查询未命中记录，查询条件必须命中索引、间隙锁只会出现在REPEATABLE_READ(重复读)的事务级别中。
例如：对应上图的表执行select * from user_info where id>1 and id<4(这里的id是唯一索引) ，这个SQL查询不到对应的记录，那么此时会使用间隙锁。
间隙锁作用：防止幻读问题，事务并发的时候，如果没有间隙锁，就会发生如下图的问题，在同一个事务里，A事务的两次查询出的结果会不一样。

临键锁(Next-Key Lock)
临键锁也属于行锁的一种，并且它是INNODB的行锁默认算法，总结来说它就是记录锁和间隙锁的组合，临键锁会把查询出来的记录锁住，同时也会把该范围查询内的所有间隙空间也会锁住，再之它会把相邻的下一个区间也会锁住。
例如：下面表的数据执行 select * from user_info where id>1 and id<=13 for update ;
会锁住ID为 1,5,10的记录；同时会锁住，1至5,5至10,10至15的区间。
触发条件：范围查询并命中，查询命中了索引。
临键锁的作用：结合记录锁和间隙锁的特性，临键锁避免了在范围查询时出现脏读、重复读、幻读问题。加了临键锁之后，在范围区间内数据不允许被修改和插入。

3、状态锁
状态锁包括意向共享锁和意向排它锁，把他们区分为状态锁的一个核心逻辑，是因为这两个锁都是都是描述是否可以对某一个表进行加表锁的状态。
意向锁的解释：当一个事务试图对整个表进行加锁(共享锁或排它锁)之前，首先需要获得对应类型的意向锁(意向共享锁或意向共享锁)
意向共享锁
当一个事务试图对整个表进行加共享锁之前，首先需要获得这个表的意向共享锁。
意向排他锁
当一个事务试图对整个表进行加排它锁之前，首先需要获得这个表的意向排它锁。
为什么我们需要意向锁？
意向锁光从概念上可能有点难理解，所以我们有必要从一个案例来分析其作用，这里首先我们先要有一个概念那就是innodb加锁的方式是基于索引，并且加锁粒度是行锁，然后我们来看下面的案例。

第一步：
事务A对user_info表执行一个SQL:update user_info set name =”张三” where id=6 加锁情况如下图;
第二步：
与此同时数据库又接收到事务B修改数据的请求：SQL: update user_info set name =”李四”；
1、因为事务B是对整个表进行修改操作，那么此SQL是需要对整个表进行加排它锁的(update加锁类型为排他锁)；
2、我们首先做的第一件事是先检查这个表有没有被别的事务锁住，只要有事务对表里的任何一行数据加了共享锁或排他锁我们就无法对整个表加锁(排他锁不能与任何属性的锁兼容)。
3、因为INNODB锁的机制是基于行锁，那么这个时候我们会对整个索引每个节点一个个检查，我们需要检查每个节点是否被别的事务加了共享锁或排它锁。
4、最后检查到索引ID为6的节点被事务A锁住了，最后导致事务B只能等待事务A锁的释放才能进行加锁操作。

思考：
在A事务的操作过程中，后面的每个需要对user_info加持表锁的事务都需要遍历整个索引树才能知道自己是否能够进行加锁，这种方式是不是太浪费时间和损耗数据库性能了？
所以就有了意向锁的概念：如果当事务A加锁成功之后就设置一个状态告诉后面的人，已经有人对表里的行加了一个排他锁了，你们不能对整个表加共享锁或排它锁了，那么后面需要对整个表加锁的人只需要获取这个状态就知道自己是不是可以对表加锁，避免了对整个索引树的每个节点扫描是否加锁，而这个状态就是我们的意向锁。
https://blog.csdn.net/weixin_36372610/article/details/113300372

Innodb存储引擎支持多粒度的锁定，换句话说，允许事务在表级和行级上同时持有锁。意向锁是一种表级锁，它是由存储引擎自己维护的，不需要用户手动命令干预。如果事务想要给表中几行数据加上行级共享锁，那么需要先在表级别加上意向共享锁（IS）；如果事务想要给表中几行数据加上行级排他锁，那么需要先在表级别加上意向排他锁（IX）

https://blog.csdn.net/Chasing__Dreams/article/details/108847570

锁 隔离级别 出现的问题 脏读，不可重复读 幻读

```sql
SELECT 
        COLUMNS .column_name, 
        COLUMNS .column_comment, 
        COLUMNS .TABLE_NAME, 
        TABLES .table_comment 
FROM 
        information_schema. COLUMNS COLUMNS 
LEFT JOIN information_schema. TABLES TABLES ON TABLES .TABLE_NAME = COLUMNS .TABLE_NAME 
WHERE 
        COLUMNS .table_schema = 'paps' 
AND COLUMNS .table_name LIKE 'paps%';
```

Mybatis插入时返回自增主键（selectKey和useGeneratedKeys）
https://blog.csdn.net/qq_34122822/article/details/79254361

GROUP BY关键字与WITH ROLLUP一起使用
https://www.cnblogs.com/caicaizi/p/4988390.html

MySQLfunction.xmind

https://gitee.com/edidada/test-my-sqlbuilt-in-function

https://dev.mysql.com/doc/refman/8.0/en/built-in-function-reference.html

Flow Control Functions
Name     Description
CASE     Case operator
IF()     If/else construct
IFNULL() Null if/else construct
NULLIF() Return NULL if expr1 = expr2

cast as char
COALESCE()
GREATEST()
IN()
INTERVAL()
IS
IS NOT
IS NOT NULL

CASE
IF()
IFNULL()
NULLIF()

ABS()
ACOS()
ASIN()
ATAN()
CEIL()
CEILING()
CONV()
COS()
COT()
CRC32()
DEGREES()

Arithmetic Operators
%, MOD
DIV

12.6.2 Mathematical Functions
12.7 Date and Time Functions
DATE_FORMAT()
NOW()
12.8 String Functions and Operators

CONCAT()

12.8.1 String Comparison Functions and Operators

LIKE
NOT LIKE
STRCMP()

12.20 Aggregate Functions
sum avg min max count

12.20.1 Aggregate Function Descriptions
12.20.2 GROUP BY Modifiers

新特性解读 | GROUPING() 函数用法解析
https://zhuanlan.zhihu.com/p/178817990

12.20.3 MySQL Handling of GROUP BY
12.20.4 Detection of Functional Dependence

AVG()
COUNT()
MAX()
MIN()
SUM()

工作流
掌握Activiti，camunda等工作流框架中的至少一种

stored procedure

```
CREATE PROCEDURE p ()
BEGIN
  DECLARE i INT DEFAULT 0;
  DECLARE d DECIMAL(10,4) DEFAULT 0;
  DECLARE f FLOAT DEFAULT 0;
  WHILE i < 10000 DO
    SET d = d + .0001;
    SET f = f + .0001E0;
    SET i = i + 1;
  END WHILE;
  SELECT d, f;
END;
```

mysql explain 优化sql
type
https://dev.mysql.com/doc/refman/5.7/en/explain.html

在MySQL的EXPLAIN结果中，select_type和type是两个不同的列，它们提供了有关查询执行计划的一些重要信息。

select_type：这个列描述了查询中的特殊查询类型。以下是select_type可能的值：

SIMPLE：这是最简单的情况，当查询只包含一个简单的SELECT语句，没有子查询或联合查询。
PRIMARY：当查询包含子查询，并且子查询不能与主查询分开时，主查询被标记为PRIMARY。
SUBQUERY：当主查询作为子查询的一部分，且子查询不能与主查询分开时，主查询被标记为SUBQUERY。
UNION：当两个或更多的SELECT语句合并在一起时，每个SELECT语句的查询计划都会被列出，并且这个查询被标记为UNION。
UNION ALL：类似于UNION，但是它不会去除重复的结果行。
DEPENDENT UNION：当UNION或UNION ALL的任何一个子查询依赖于主查询中的列或常量时，这个查询被标记为DEPENDENT UNION。
DEPENDENT UNION ALL：当UNION ALL的任何一个子查询依赖于主查询中的列或常量时，这个查询被标记为DEPENDENT UNION ALL。
NULL：当没有从主查询返回任何结果行时，这个查询被标记为NULL。
type：这个列描述了MySQL如何执行查询，给出了执行计划的详细信息。以下是type可能的值：

ALL：全表扫描。MySQL将检查整个表来寻找匹配的结果行。
index：全索引扫描。MySQL将扫描整个索引来寻找匹配的结果行。这通常比全表扫描快，但可能会增加内存使用。
range：范围扫描。MySQL将使用索引来查找满足某个范围的行。这是在你知道结果行在一个范围内时最常用的方法。
ref：索引引用。MySQL将使用索引来查找匹配某个单个列或多列的行。它通常比范围扫描和全表扫描快。
eq_ref：唯一索引引用。这表示MySQL使用一个唯一索引来查找一个精确匹配的行。这是最快的查找方法，但仅适用于唯一索引或PRIMARY KEY。
const、system和NULL：这些类型表示在执行查询时没有任何表或索引的读取操作。
这些类型的主要区别在于它们描述了MySQL是如何访问和查找数据的。理解这些类型可以帮助你优化查询性能，特别是当你注意到查询执行得非常慢时。

是的，MySQL 5.7对SQL语句是大小写敏感的。这意味着如果你在SQL语句中使用大写或小写字母，它们将被视为不同的字符。

例如，以下两个SQL语句在MySQL 5.7中是不同的：

sql
SELECT * FROM mytable;
SELECT * FROM MYTABLE;
第一个SQL语句将选择"mytable"表中的所有行，而第二个SQL语句将选择"MYTABLE"表中的所有行（如果存在）。这是因为MySQL将大写和小写视为不同的字符。

然而，在某些情况下，MySQL对表和数据库的名称不区分大小写。例如，以下两个SQL语句在MySQL 5.7中是等效的：

sql
USE mydatabase;
USE MYDATABASE;
这因为在MySQL中，表名和数据库名不区分大小写。但是，请注意，表的列名和函数名是区分大小写的。

需要注意的是，MySQL的默认设置是不区分大小写，但也可以通过设置适当的配置参数来更改大小写敏感性。

mysql查看所有表的所有字段

```sql
SELECT 
    COLUMNS .column_name, 
    COLUMNS .column_comment, 
    COLUMNS .TABLE_NAME, 
    TABLES .table_comment 
FROM 
    information_schema. COLUMNS COLUMNS 
LEFT JOIN information_schema. TABLES TABLES ON TABLES .TABLE_NAME = COLUMNS .TABLE_NAME 
WHERE 
    COLUMNS .table_schema = 'paps' 
AND COLUMNS .table_name LIKE 'paps%';
```

[mysql查看执行sql语句的记录日志 ](https://www.cnblogs.com/xcsn/p/11485939.html)

```sql
SET GLOBAL log_output = 'TABLE';
SET GLOBAL general_log = 'ON';
```

mysql内置函数

ifnull
date_format

需要整理，写demo

product_name

select id from tableA where columnA = ''

select * from tableb where XXid = 上面查出来的id

select curdate() into @today;

select @today;

https://www.cnblogs.com/Fengge518/p/13451919.html

https://www.cnblogs.com/bingco/p/11381107.html

中国银行协同项目cims

大量使用临时表

select max (substr(columnName,13)) +1 from tableName where columnName like concat()

mysql中的instr()函数的用法
https://www.cnblogs.com/qingmuchuanqi48/articles/15418961.html

`SELECT INSTR("abcd",'b');`
INSTR(STR,SUBSTR) 在一个字符串(STR)中搜索指定的字符(SUBSTR),返回发现指定的字符的位置(INDEX);
STR 被搜索的字符串
SUBSTR 希望搜索的字符串
结论：在字符串STR里面,字符串SUBSTR出现的第一个位置(INDEX)，INDEX是从1开始计算，如果没有找到就直接返回0，没有返回负数的情况

MySQL软件支持的字符串函数表如下：

| 函数                       | 功能                                                          |
| -------------------------- | ------------------------------------------------------------- |
| CONCAT(str1,str2,...,strn) | 将str1,str2,...,strn连接为一个完整的字符串                    |
| INSERT(str,x,y,instr)      | 将字符串str从第x开始，y个字符串长度的子串替换为字符串instr    |
| LOWER(str)                 | 将字符串str中的所有字母变成小写                               |
| UPPER(str)                 | 将字符串str中的所有字母变成大写                               |
| LEFT(str,x)                | 返回字符串最左边的x个字符                                     |
| RIGHT(str,x)               | 返回字符串最右边的x个字符                                     |
| LPAD(str,n,pad)            | 使用字符串pad对字符串str最左边进行填充，直到长度为n个字符长度 |
| RPAD(str,n,pad)            | 使用字符串pad对字符串str最右边进行填充，直到长度为n个字符长度 |
| LTRIM(str)                 | 去掉str左边的空格                                             |
| RTRIM(str)                 | 去掉str右边的空格                                             |
| REPEAT(str,x)              | 返回字符串str重复x次的结果                                    |
| REPLACE(str,a,b)           | 使用字符串b替换字符串str中所有出现的字符串a                   |
| STRCMP(str1,str2)          | 比较字符串str1和str2                                          |
| TRIM(str)                  | 去掉字符串行头和行尾的空格                                    |
| SUBSTRING(str,x,y)         | 返回字符串str中从x位置起y个字符串长度的字符串                 |

mysql架构
连接管理器
缓存
存储引擎
文件系统

innodb如何实现join操作
InnoDB是MySQL的默认存储引擎，它支持事务、行级锁定和外键等特性。在InnoDB中，join操作主要通过以下几种方式实现：

嵌套循环连接（Nested Loop Join）：这是最基本的连接方式，适用于小表和结果集较小的场景。在嵌套循环连接中，驱动表（outer table）的每一行都会与目标表（inner table）的每一行进行比较，直到找到匹配的记录。
哈希连接（Hash Join）：哈希连接利用哈希表的特性，通过将两个表中的某个字段哈希，然后在哈希表中进行匹配。哈希连接适用于两个表按照一个共同的字段进行连接，并且这两个表的行数都比较大。
排序合并连接（Sort-Merge Join）：对于两个已经按照连接字段排好序的表，可以使用排序合并连接。这种方式会先遍历两个表中的第一行，选择最小的那一行作为结果集的第一行，然后继续遍历两个表，选择下一个最小的行作为结果集的第二行，以此类推。
索引连接（Index Join）：在InnoDB中，可以利用覆盖索引（Covering Index）来实现join操作。覆盖索引是指包含所有查询需要的数据的索引，不需要回表查询原表。通过在索引上执行join操作，可以避免访问原表的数据，从而提高查询效率。
需要注意的是，InnoDB的join操作性能还受到其他因素的影响，如表的行数、索引的选择和使用、查询语句的优化等。在实际应用中，需要根据具体的业务场景和数据特点来选择适合的join方式，并进行相应的优化。
frm
ibd
文件读写

mvcc是个概念，不同rdbms实现不同，核心目的是提高软件系统并发量
java里面也需要自己去实现

数据库表外键，删除表的时候不方便

实现了四个标准的隔离级别，默认级别是可重复读(REPEATABLE READ)。在可重复读隔离级别下，通过多版本并发控制(MVCC)+ 间隙锁(Next-Key Locking)防止幻影读。
在可重复读（REPEATABLE READ）隔离级别下，MySQL通过多版本并发控制（MVCC）和间隙锁（Gap Locking）以及临键锁（Next-Key Locking）来防止不可重复读和幻读。但需要注意，对于幻读的防止，仅仅依赖间隙锁是不够的。

MVCC保证了在同一个事务内多次读取同一行数据时，看到的是一致的版本，这有助于防止不可重复读。然而，MVCC并不能直接防止幻读，因为幻读是指由于其他事务的插入或删除操作，导致满足某些条件的数据行数发生了变化。

为了防止幻读，InnoDB在可重复读隔离级别下使用了临键锁（Next-Key Locking）。临键锁是记录锁和间隙锁的结合，它锁定一个索引记录以及该记录前的间隙。这种锁定策略确保了在一个事务内，按照相同的条件进行范围查询时，得到的结果集是一致的，从而防止了幻读的发生。

因此，上面的说法“通过多版本并发控制(MVCC)+间隙锁(Next-Key Locking)防止幻影读”是不准确的。应该是“通过多版本并发控制(MVCC)和临键锁(Next-Key Locking)防止不可重复读和幻读”。间隙锁本身只是临键锁的一个组成部分，它主要用于锁定一个范围但不包括记录本身，而临键锁则结合了记录锁和间隙锁的功能来防止幻读。

是的，间隙锁（Gap Lock）本身是临键锁（Next-Key Lock）的一个组成部分。临键锁是InnoDB在行级锁定中使用的锁算法之一，它结合了记录锁（Record Lock）和间隙锁的功能。
具体来说，临键锁锁定一个索引记录以及该记录前的间隙。这意味着它不仅锁定一个具体的索引记录，还锁定一个范围，以防止其他事务在这个范围内插入新的记录。这种锁定策略有助于防止幻读的发生，因为幻读是由于其他事务的插入或删除操作导致满足某些条件的数据行数发生了变化。
间隙锁作为临键锁的一部分，主要用于锁定一个范围但不包括记录本身。它确保在这个范围内不会有新的记录被插入，从而保持了数据的一致性。
因此，可以说间隙锁是临键锁的一个组件，而临键锁则是结合了记录锁和间隙锁的功能来提供更全面的锁定策略，以防止不可重复读和幻读的发生。

mysql
varchar 字符串长度需要注意
索引 char like %xx%看执行计划 不走

mysql 共享锁 排他锁

s锁

x锁
mysql的相关技术细节，需要搞清楚是mysql server的还是存储引擎的

mysql
pgsql如何实现sql join
https://www.cnblogs.com/flying-tiger/p/8331425.html

matlab 关系运算

a left join b on a.id = b.id
a left join b on a.id > b.id

mysql关闭ssl

D:\Mysql\mysql-5.7.31-winx64\data
private_key.pem
public_key.pem
server-cert.pem
server-key.pem

net stop mysql

skipssl

useSSL=false

通配符的分类:
%百分号通配符: 表示任何字符出现任意次数(可以是0次).
_下划线通配符:表示只能匹配单个字符,不能多也不能少,就是一个字符.

like操作符:
LIKE作用是指示mysql后面的搜索模式是利用通配符而不是直接相等匹配进行比较.
注意: 如果在使用like操作符时,后面的没有使用通用匹配符效果是和=一致的,SELECT * FROM products WHERE products.prod_name like '1000';只能匹配的结果为1000,而不能匹配像JetPack 1000这样的结果.
1)%通配符使用:
匹配以"yves"开头的记录:(包括记录"yves")
SELECT * FROM products WHERE products.prod_name like 'yves%';
匹配包含"yves"的记录(包括记录"yves")
SELECT * FROM products WHERE products.prod_name like '%yves%';
匹配以"yves"结尾的记录(包括记录"yves",不包括记录"yves ",也就是yves后面有空格的记录,这里需要注意)
SELECT * FROM products WHERE products.prod_name like '%yves';
2)_通配符使用:
SELECT * FROM products WHERE products.prod_name like '_yves';
匹配结果为: 像"yyves"这样记录.
SELECT * FROM products WHERE products.prod_name like 'yves__';
匹配结果为: 像"yvesHe"这样的记录.(一个下划线只能匹配一个字符,不能多也不能少)
注意事项:
注意大小写,在使用模糊匹配时,也就是匹配文本时,mysql是可能区分大小的,也可能是不区分大小写的,这个结果是取决于用户对MySQL的配置方式.如果是区分大小写,那么像YvesHe这样记录是不能被"yves__"这样的匹配条件匹配的.
注意尾部空格,"%yves"是不能匹配"heyves "这样的记录的.
注意NULL,%通配符可以匹配任意字符,但是不能匹配NULL,也就是说SELECT * FROM products WHERE products.prod_name like '%;是匹配不到products.prod_name为NULL的的记录.
技巧与建议:
正如所见， MySQL的通配符很有用。但这种功能是有代价的：通配符搜索的处理一般要比前面讨论的其他搜索所花时间更长。这里给出一些使用通配符要记住的技巧。
不要过度使用通配符。如果其他操作符能达到相同的目的，应该 使用其他操作符。
在确实需要使用通配符时，除非绝对有必要，否则不要把它们用 在搜索模式的开始处。把通配符置于搜索模式的开始处，搜索起 来是最慢的。
仔细注意通配符的位置。如果放错地方，可能不会返回想要的数.

expain出来的信息有10列，分别是id、select_type、table、type、possible_keys、key、key_len、ref、rows、extra
下面对这些字段出现的可能进行解释：
一、 id
     我的理解是SQL执行的顺序的标识,SQL从大到小的执行

1. id相同时，执行顺序由上至下
2. 如果是子查询，id的序号会递增，id值越大优先级越高，越先被执行
   3.id如果相同，可以认为是一组，从上往下顺序执行；在所有组中，id值越大，优先级越高，越先执行
   二、select_type
   示查询中每个select子句的类型
   (1) SIMPLE(简单SELECT,不使用UNION或子查询等)
   (2) PRIMARY(查询中若包含任何复杂的子部分,最外层的select被标记为PRIMARY)
   (3) UNION(UNION中的第二个或后面的SELECT语句)
   (4) DEPENDENT UNION(UNION中的第二个或后面的SELECT语句，取决于外面的查询)
   (5) UNION RESULT(UNION的结果)
   (6) SUBQUERY(子查询中的第一个SELECT)
   (7) DEPENDENT SUBQUERY(子查询中的第一个SELECT，取决于外面的查询)
   (8) DERIVED(派生表的SELECT, FROM子句的子查询)
   (9) UNCACHEABLE SUBQUERY(一个子查询的结果不能被缓存，必须重新评估外链接的第一行)
   三、table
   显示这一行的数据是关于哪张表的，有时不是真实的表名字,看到的是derivedx(x是个数字,我的理解是第几步执行的结果)
   四、type
   表示MySQL在表中找到所需行的方式，又称“访问类型”。
   常用的类型有： ALL, index,  range, ref, eq_ref, const, system, NULL（从左到右，性能从差到好）
   ALL：Full Table Scan， MySQL将遍历全表以找到匹配的行
   index: Full Index Scan，index与ALL区别为index类型只遍历索引树
   range:只检索给定范围的行，使用一个索引来选择行
   ref: 表示上述表的连接匹配条件，即哪些列或常量被用于查找索引列上的值
   eq_ref: 类似ref，区别就在使用的索引是唯一索引，对于每个索引键值，表中只有一条记录匹配，简单来说，就是多表连接中使用primary key或者 unique key作为关联条件
   const、system: 当MySQL对查询某部分进行优化，并转换为一个常量时，使用这些类型访问。如将主键置于where列表中，MySQL就能将该查询转换为一个常量,system是const类型的特例，当查询的表只有一行的情况下，使用system
   NULL: MySQL在优化过程中分解语句，执行时甚至不用访问表或索引，例如从一个索引列里选取最小值可以通过单独索引查找完成。
   五、possible_keys
   指出MySQL能使用哪个索引在表中找到记录，查询涉及到的字段上若存在索引，则该索引将被列出，但不一定被查询使用
   六、Key
   key列显示MySQL实际决定使用的键（索引）
   七、key_len
   表示索引中使用的字节数，可通过该列计算查询中使用的索引的长度（key_len显示的值为索引字段的最大可能长度，并非实际使用长度，即key_len是根据表定义计算而得，不是通过表内检索出的）
   八、ref
   表示上述表的连接匹配条件，即哪些列或常量被用于查找索引列上的值
   九、rows
   表示MySQL根据表统计信息及索引选用情况，估算的找到所需的记录所需要读取的行数
   十、Extra
   该列包含MySQL解决查询的详细信息,有以下几种情况：
   Using where:列数据是从仅仅使用了索引中的信息而没有读取实际的行动的表返回的，这发生在对表的全部的请求列都是同一个索引的部分的时候，表示mysql服务器将在存储引擎检索行后再进行过滤
   Using temporary：表示MySQL需要使用临时表来存储结果集，常见于排序和分组查询
   Using filesort：MySQL中无法利用索引完成的排序操作称为“文件排序”
   Using join buffer：改值强调了在获取连接条件时没有使用索引，并且需要连接缓冲区来存储中间结果。如果出现了这个值，那应该注意，根据查询的具体情况可能需要添加索引来改进能。
   Impossible where：这个值强调了where语句会导致没有符合条件的行。
   Select tables optimized away：这个值意味着仅通过使用索引，优化器可能仅从聚合函数结果中返回一行

Heal表的大小可通过称为 max_heap_table_size 的 Mysql 配置变量来控制。

mysql gtid
https://www.cnblogs.com/zhang-ding-1314/p/15125188.html

家人们mysql每天几十万的数据同步，从一个库到另一个库，有没有什么好的方案
canal也行
直接kettle
阿里愚公也是java写的

自建mysql数据库主从同步(GTID方式)
https://www.cnblogs.com/zhang-ding-1314/p/15125188.html

https://baijiahao.baidu.com/s?id=1741371045827915061

关系数据库事务四大特性

ACID

- 原子性
- 一致性
- 隔离性
- 持久性

隔离级别
在MySQL 中,可以通过
`show variables like '%tx_isolation%'`
或
`select @@tx_isolation;`
语句来查看当前事务隔离级别。

读未提交 RU
读已提交 RC
可重复读 RR
串行化 S

在MySQL中，MVCC（多版本并发控制）是InnoDB存储引擎的核心特性之一，它用于支持高并发访问，同时保持数据的一致性。由于MVCC是InnoDB存储引擎内置的一部分，因此你不能直接“关闭”MVCC。它是InnoDB用来管理事务并发访问的基础机制，没有MVCC，InnoDB就无法正常工作。
如果你不希望使用MVCC或InnoDB的其他特性，你可以选择使用MySQL的其他存储引擎，比如MyISAM。但是，请注意，MyISAM存储引擎不支持事务和行级锁定，这可能会限制你的应用程序的并发性和数据一致性能力。
总之，MVCC是InnoDB存储引擎的基础特性，你不能直接关闭它。如果你对数据库的性能或特性有特定的需求，你应该选择合适的存储引擎和配置选项来满足这些需求。

现象

脏读。读到的是另一个事物未提交的事物

不可重复读  不可重复读，是指在数据库访问中，一个事务范围内两个相同的查询却返回了不同数据。

幻读
幻读（Phantom Read），是指当事务不是独立执行时发生的一种现象。
幻读问题在 “当前读” 下才会出现。

MySQL的当前读和快照读这些概念的产生背景主要源于数据库并发控制的需求。在多个事务同时访问和修改数据库的情况下，为了确保数据的一致性和完整性，需要采用适当的并发控制机制。
快照读的概念是基于多版本并发控制（MVCC，Multi-Version Concurrency Control）的。MVCC是数据库管理系统中的一种并发控制方法，它通过保存数据的多个版本来实现并发读取，从而避免了读操作和写操作之间的锁竞争。在MVCC机制下，当事务读取数据时，它实际上读取的是数据的某个历史版本，而不是最新的数据。这个历史版本就像是数据的一个“快照”，因此被称为快照读。这种读取方式不需要等待其他事务完成，因此可以提高并发性能。
与快照读相对的是当前读。当前读是读取数据的最新版本，并且会加上锁，保证其他事务不会并发的修改这条记录。这种读取方式通常用于需要确保数据一致性的场景，比如修改数据或进行需要精确数据的查询。
这些概念的产生背景是数据库在处理并发操作时需要解决数据一致性和并发性能之间的权衡。通过引入快照读和当前读等机制，MySQL可以在保证数据一致性的同时，提高并发性能，从而更好地支持高并发的应用场景。

什么是当前读、什么是快照读。
快照读：读取快照中的数据，不需要进行加锁。看到快照这两个字，各位肯定马上就想到MVCC了，是这样，MVCC 作用于读取已提交和可重复读（默认）这两个隔离级别，这俩隔离级别下的普通select操作就是快照读。
当前读：读取的是最新版本的数据, 并且对读取的记录加锁, 阻塞其他事务同时改动相同记录，避免出现安全问题。
当前读，读取效率高

除了读取已提交和可重复读这俩隔离级别下的普通 select 操作，其余操作都是当前读：

```sql
select...lock in share mode (共享读锁)
select...for update
update, delete, insert
```

mysql脏读和幻读区别
Mysql之脏读、不可重复读、幻读的区别
MySQL中的脏读、不可重复读和幻读是三种不同的并发读取问题，它们之间的主要区别如下：
脏读（Dirty Read）：
脏读发生在当一个事务正在访问并修改数据，但这种修改还没有提交到数据库时，另一个事务访问了这些数据并使用了它们。简单来说，就是读取到了另一个事务还未提交的数据。这种情况下，如果第一个事务回滚，那么第二个事务就读取到了“脏”数据，即不正确或不一致的数据。
不可重复读（Non-repeatable Read）：
不可重复读是指在一个事务内，多次读取同一数据，但由于在此期间有其他事务修改了该数据，导致每次读取的结果可能不一致。这意味着，在同一个事务中，同样的查询条件，可能会得到不同的结果。
幻读（Phantom Read）：
幻读发生在当事务不是独立执行时，它涉及到在一个事务内，按照某个条件查询数据，但在查询之间，另一个事务插入了或删除了满足这个条件的数据，导致第一个事务在再次执行相同的查询时，发现数据的数量发生了变化。即数据的行数发生了改变，好像出现了“幻影”一样。
总结来说，脏读涉及读取未提交的数据，不可重复读涉及同一事务中多次读取同一数据但结果不一致，而幻读则涉及满足特定条件的数据行数在事务执行期间发生变化。这三种问题都是MySQL进行事务并发控制时可能遇到的问题，需要采取相应的隔离级别来避免或解决。

数据库在在高并发时，事务会出现三种异常问题。

脏读：在事物还没有提交前，修改的数据可以被其他事物所看到。
不可重复读：在一个事物中使用相同的条件查询一条数据，前后两次查询所得到的数据不同，这是因为同时其他事物对这条数据进行了修改（已提交事物），第二次查询返回了其他事物修改的数据。
幻读：在一个事物A中使用相同的条件查询了多条数据，同时其他事物添加或删除了符合事物A中查询条件的数据，这时候当事物A再次查询时候会发现数据多了或者少了，与前一次查询的结果不相同。

注意：不可重复读与幻读很容易搞混，他们的区别在于：
不可重复读：是同一条记录（一条数据）的内容被其他事物修改了，关注的是update、delete操作一条数据的操作.
幻读：是查询某个范围（多条数据）的数据行变多或变少了，在于insert、delete的操作。

修改隔离级别
有两种方法可以改变当前会话的隔离级别

SET session TRANSACTION ISOLATION LEVEL Serializable;
SET @@tx_isolation='read-committed';
参数可以为：

Read uncommitted
Read committed
Repeatable Read
Serializable
查看当前会话的隔离级别

select @@tx_isolation;
https://www.jianshu.com/p/fb312164f03d

### 共享锁

select a from t where id = 1 lock in share mode;

### 排他锁

select a from t where id = 1 for update;

可以认为 多版本并发控制（MVCC） 是行级锁的一个变种
MySQL中的MDL锁
MDL锁，全称为Metadata Lock，即元数据锁，是从MySQL 5.5版本开始引入的一种锁机制。其主要目的是为了解决DDL（数据定义语言，如CREATE、ALTER等）操作和DML（数据操作语言，如SELECT、INSERT等）操作之间的一致性问题，以及处理不同线程操作同一元数据对象的同步与互斥问题。
MDL锁是一种表级锁，也是一个server层的锁。其加锁过程是系统自动控制，无法直接干预。当我们对一个表做增删改查操作时，系统会自动加上MDL读锁；而当我们需要更新表结构时，系统会自动加上MDL写锁。
在MDL锁的机制下，读锁是共享的，意味着可以多个线程同时对一张表进行增删改查的操作；而写锁是独占的，当要对表进行结构修改时，需要先等待其他所有的MDL锁释放，获取到MDL写锁后才能进行。在写锁释放前，其他线程无法获取到MDL读锁和写锁，即修改表结构的过程中会阻塞其他线程对表的操作。
总的来说，MDL锁的存在是为了保证数据的一致性，避免在数据操作过程中发生错误或冲突。如需更多关于MDL锁的信息，建议查阅数据库相关书籍或咨询数据库管理员。

S锁和X锁。

S锁，英文为Shared Lock，中文译作共享锁，有时候我们也称之为读锁，即Read Lock。S 锁之间是共享的，或者说是互不阻塞的。
X锁，英文为Exclusive Lock，中文译作排他锁，有时候我们也称之为写锁，即Write Lock。如同它的名字，X锁是具有排他性的，即一个写锁会阻塞其他的X锁和S锁。

MySQL是server和engine分离的
Driver的engine是？

Cluster index聚集索引
Unclusrer index 非聚集索引

covering index 覆盖索引
覆盖索引 covering index
https://blog.csdn.net/yinni11/article/details/81812309

https://www.hollischuang.com/archives/3818

最左匹配

select where 的and条件 mysql会优化

MYSQL binlog优化几点思考
https://zhuanlan.zhihu.com/p/147459036

WAL机制
redo log顺序追加写入。事务提交时，只需要保证事务的redo log落盘即可，通过redo log的顺序写代替页面的随机写提升数据库系统的性能。

问题1：如何解决事务提交时flush redo log带来的性能损失
Redo log组提交技术
问题2：binlog和引擎层事务提交的顺序问题
内部XA事务

my.cnf配置
log_bin
bin_alive 大致

### mysql 源码编译

ubuntu 16
centos 7/8

cmake组织的

MySQL Benchmark Tool
DBT2 dbt2是一款免费的TPC-C测试工具,用于模拟复杂的OLTP系统。
SysBench
flexAsynch MySQL集群的flexAsynch测试工具

mysql支持的数据类型 json
text
varchar
date
timestamp

https://dev.mysql.com/doc/refman/5.7/en/json.html

索引下推和覆盖索引都是优化MySQL查询性能的方法
索引下推和覆盖索引都是优化MySQL查询性能的方法
索引下推和覆盖索引都是优化MySQL查询性能的方法，但它们的实现方式有所不同。
索引下推是指MySQL在执行查询时，尽可能地利用索引来减少需要扫描的行数，从而提高查询性能。具体来说，当MySQL使用一个覆盖索引来执行一个查询时，它会首先扫描索引，然后只返回满足查询条件的索引列，而不需要再去检查数据行，因为索引列已经包含了需要的数据。这种方法可以减少磁盘I/O和CPU开销，从而提高查询性能。
覆盖索引是指一个索引包含了查询所需要的所有列，因此MySQL可以直接从索引中获取需要的数据，而不需要再去检查数据行。这种方法可以减少磁盘I/O和CPU开销，从而提高查询性能。覆盖索引通常用于查询只需要返回少量列数据的情况下，例如只需要返回某些列的值或者只需要计算总数的情况下。
虽然索引下推和覆盖索引都能提高查询性能，但它们适用于不同的查询场景。索引下推通常适用于需要返回大量列数据的查询，而覆盖索引通常适用于需要返回少量列数据的查询。

05 如何设计高性能的索引

## icp 索引下推

索引下推的一个简单例子是使用SELECT语句查询一个包含多列的表，但只需要返回其中的一列数据。
假设有一个包含以下列的表：

```
CREATE TABLE my_table (
  id INT NOT NULL,
  name VARCHAR(50) NOT NULL,
  age INT NOT NULL,
  address VARCHAR(100) NOT NULL,
  PRIMARY KEY (id),
  INDEX idx_age (age)
);
```

现在需要查询年龄大于等于20岁的所有用户的姓名，可以使用以下查询语句：

```
SELECT name FROM my_table WHERE age >= 20;
```

在执行该查询时，MySQL会使用索引idx_age来定位符合条件的行，然后再到数据行中获取需要的name列数据。但是，如果使用索引下推的话，MySQL会在索引中就获取需要的name列数据，而不需要再到数据行中获取，从而减少了不必要的磁盘I/O和CPU开销，提高了查询性能。可以使用以下查询语句来启用索引下推：

```
SELECT name FROM my_table WHERE age >= 20 AND name IS NOT NULL;
```

在这个查询语句中，增加了一个额外的条件name IS NOT NULL，这个条件的作用是强制MySQL在使用索引idx_age定位符合条件的行时，检查name列是否为NULL，从而在索引中获取需要的name列数据。这样，MySQL就可以使用索引下推来提高查询性能。

MySQL查看和修改事务隔离级别
http://c.biancheng.net/view/7266.html

银行 建议隔离级别 RC
默认 RR
引擎是innodb

查看活跃连接数
https://www.cnblogs.com/caoshousong/p/10845396.html

show processlist;

677277  fuyao_costcontrol_dev   172.16.10.16    fuyao_costcontrol_dev   Sleep   1073    2
678077  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   178 2
677262  fuyao_costcontrol_dev   172.16.10.16    fuyao_costcontrol_dev   Sleep   1101    2
678190  fuyao_approval_dev  172.16.10.16    fuyao_approval_dev  Sleep   94  2
677904  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   335 2
678216  fuyao_approval_dev  172.16.10.16    fuyao_approval_dev  Sleep   94  2
677979  fuyao_approval_dev  172.16.10.17    fuyao_approval_dev  Sleep   280 2
676781  fuyao_approval_dev  172.16.10.17    fuyao_approval_dev  Sleep   1729    2
677565  ent_fserver_env 172.16.10.16    ent_fserver_env_fuyao   Sleep   720 2
677933  hrbase  172.16.10.18    nacos_test  Sleep   315 2
677257  fuyao_pursale_dev   172.16.10.16    fuyao_pursale_dev   Sleep   1105    2
678283  fuyao_approval_dev  172.16.10.17    fuyao_approval_dev  Sleep   14  2
678152  ares_ent_service_cloud  172.16.10.17    ares_ent_service_cloud  Sleep   97  2
677317  fuyao_costcontrol_dev   172.16.10.16    fuyao_costcontrol_dev   Sleep   1048    2
678171  fuyao_approval_dev  172.16.10.16    fuyao_approval_dev  Sleep   3   2
608972  ares_ent_service_cloud  172.16.10.17    ares_ent_service_cloud  Sleep   159 2
678198  fuyao_approval_dev  172.16.10.16    fuyao_approval_dev  Sleep   94  2
678148  ytfs    172.16.2.111    YTFS    Sleep   102 2
676981  eolinker_os 172.16.10.16    eolinker_os Sleep   1473    2
678057  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   207 2
677206  ent_fserver_env 172.16.10.16    ent_fserver_env_fuyao   Sleep   177 2
677479  fuyao_pursale_dev   172.16.10.16    fuyao_pursale_dev   Sleep   844 2
676761  fuyao_approval_dev  172.16.10.17    fuyao_approval_dev  Sleep   7   2
677321  fuyao_costcontrol_dev   172.16.10.16    fuyao_costcontrol_dev   Sleep   1041    2
677222  root    172.16.10.70    dmcp    Sleep   1128    2
677897  root    172.16.10.16    ares_ent_service_dev    Sleep   343 2
677978  fuyao_application_dev   172.16.10.17    fuyao_application_dev   Sleep   280 2
677434  fuyao_pursale_dev   172.16.10.16    fuyao_pursale_dev   Sleep   894 2
676959  fuyao_pursale_dev   172.16.10.16    fuyao_pursale_dev   Sleep   1500    2
677949  fuyao_user_dev  172.16.10.16    fuyao_user_dev  Sleep   299 2
674958  root    192.168.10.114  app_market_dev  Sleep   3822    2
674548  root    192.168.10.121  ares_ent_service_dev    Sleep   4254    2
677850  fuyao_pursale_dev   172.16.10.16    fuyao_pursale_dev   Sleep   387 2
678252  hrbase  172.16.10.18    HRBASE_UAT2 Sleep   51  2
677584  ent_fserver_env 172.16.10.16    ent_fserver_env_fuyao   Sleep   695 2
677047  ent_fserver_env 172.16.10.16    ent_fserver_env_fuyao   Sleep   116 2
677700  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   557 2
677118  fuyao_pursale_dev   172.16.10.16    fuyao_pursale_dev   Sleep   1292    2
677274  fuyao_costcontrol_dev   172.16.10.16    fuyao_costcontrol_dev   Sleep   1080    2
676950  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   1512    2
678289  hrbase  172.16.10.16    HRBASE_UAT2 Sleep   0   2
677953  fuyao_invoice_dev   172.16.10.17    fuyao_invoice_dev   Sleep   296 2
677951  fuyao_application_dev   172.16.10.17    fuyao_application_dev   Sleep   298 2
677541  ent_fserver_env 172.16.10.16    ent_fserver_env_fuyao   Sleep   745 2
677559  fuyao_invoice_dev   172.16.10.17    fuyao_invoice_dev   Sleep   724 2
676770  fuyao_invoice_dev   172.16.10.17    fuyao_invoice_dev   Sleep   1742    2
677336  fuyao_costcontrol_dev   172.16.10.16    fuyao_costcontrol_dev   Sleep   1022    2
678267  fuyao_approval_dev  172.16.10.16    fuyao_approval_dev  Sleep   36  2
677619  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   661 2
677996  fuyao_application_dev   172.16.10.17    fuyao_application_dev   Sleep   270 2
677744  fuyao_invoice_dev   172.16.10.17    fuyao_invoice_dev   Sleep   506 2
678062  fuyao_application_dev   172.16.10.17    fuyao_application_dev   Sleep   203 2
648645  ares_ent_service_cloud  172.16.10.17    ares_ent_service_cloud  Sleep   19535   2
678255  app_market_dev  172.16.10.17    app_market_dev  Sleep   49  2
677800  fuyao_invoice_dev   172.16.10.17    fuyao_invoice_dev   Sleep   436 2
677183  fuyao_pursale_dev   172.16.10.16    fuyao_pursale_dev   Sleep   1184    2
677830  fuyao_invoice_dev   172.16.10.17    fuyao_invoice_dev   Sleep   408 2
678013  fuyao_invoice_dev   172.16.10.17    fuyao_invoice_dev   Sleep   251 2
676864  fuyao_pursale_dev   172.16.10.16    fuyao_pursale_dev   Sleep   1626    2
676858  fuyao_pursale_dev   172.16.10.16    fuyao_pursale_dev   Sleep   1635    2
677381  fuyao_costcontrol_dev   172.16.10.16    fuyao_costcontrol_dev   Sleep   979 2
678173  fuyao_approval_dev  172.16.10.16    fuyao_approval_dev  Sleep   35  2
388803  root    172.16.10.70    dmcp    Sleep   369786  2
677466  fuyao_invoice_dev   172.16.10.17    fuyao_invoice_dev   Sleep   866 2
676779  fuyao_approval_dev  172.16.10.17    fuyao_approval_dev  Sleep   1734    2
677567  ent_fserver_env 172.16.10.16    ent_fserver_env_fuyao   Sleep   716 2
678123  fuyao_approval_dev  172.16.10.17    fuyao_approval_dev  Sleep   131 2
678041  ytfs_console    172.16.10.17    ytfs_console    Sleep   216 2
677283  fuyao_costcontrol_dev   172.16.10.16    fuyao_costcontrol_dev   Sleep   1062    2
677715  fuyao_invoice_dev   172.16.10.17    fuyao_invoice_dev   Sleep   531 2
677890  fuyao_user_dev  172.16.10.16    fuyao_user_dev  Sleep   349 2
677589  ent_fserver_env 172.16.10.16    ent_fserver_env_fuyao   Sleep   692 2
677169  eolinker_os 172.16.10.16    eolinker_os Sleep   1216    2
677711  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   535 2
677913  fuyao_application_dev   172.16.10.17    fuyao_application_dev   Sleep   333 2
677264  fuyao_costcontrol_dev   172.16.10.16    fuyao_costcontrol_dev   Sleep   1094    2
641059  ares_ent_service_cloud  172.16.10.17    ares_ent_service_cloud  Sleep   6741    2
388810  root    172.16.10.70    dmcp    Sleep   527 2
677923  hrbase  172.16.10.70    nacos_test  Sleep   327 2
1215    ares_ent_service_cloud  172.16.10.17    ares_ent_service_cloud  Sleep   1013    2
677574  ent_fserver_env 172.16.10.16    ent_fserver_env_fuyao   Sleep   709 2
678186  fuyao_approval_dev  172.16.10.16    fuyao_approval_dev  Sleep   94  2
678184  fuyao_approval_dev  172.16.10.16    fuyao_approval_dev  Sleep   94  2
677901  ytfs_console    172.16.10.17    ytfs_console    Sleep   339 2
677980  fuyao_application_dev   172.16.10.17    fuyao_application_dev   Sleep   278 2
639874  ares_ent_service_cloud  172.16.10.17    ares_ent_service_cloud  Sleep   34  2
677533  ent_fserver_env 172.16.10.16    ent_fserver_env_fuyao   Sleep   761 2
677398  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   951 2
677234  fuyao_costcontrol_dev   172.16.10.16    fuyao_costcontrol_dev   Sleep   22  2
677562  ent_fserver_env 172.16.10.16    ent_fserver_env_fuyao   Sleep   721 2
675594  root    172.16.10.16    cloud_gateway_console   Sleep   94  2
677957  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   295 2
676847  fuyao_approval_dev  172.16.10.17    fuyao_approval_dev  Sleep   1647    2
677639  fuyao_pursale_dev   172.16.10.16    fuyao_pursale_dev   Sleep   632 2
640245  root    192.168.10.110  HRBASE_UAT2 Sleep   40899   2
677863  fuyao_pursale_dev   172.16.10.16    fuyao_pursale_dev   Sleep   376 2
676936  eolinker_os 172.16.10.16    eolinker_os Sleep   1532    2
678195  fuyao_approval_dev  172.16.10.16    fuyao_approval_dev  Sleep   94  2
677709  fuyao_invoice_dev   172.16.10.17    fuyao_invoice_dev   Sleep   538 2
677900  fuyao_application_dev   172.16.10.17    fuyao_application_dev   Sleep   339 2
677631  fuyao_pursale_dev   172.16.10.16    fuyao_pursale_dev   Sleep   648 2
678275  hrbase  172.16.10.18    HRBASE_UAT2 Sleep   26  2
678147  ytfs    172.16.1.70 YTFS_OP Sleep   104 2
677298  fuyao_costcontrol_dev   172.16.10.16    fuyao_costcontrol_dev   Sleep   1055    2
677606  fuyao_pursale_dev   172.16.10.16    fuyao_pursale_dev   Sleep   673 2
677591  ent_fserver_env 172.16.10.16    ent_fserver_env_fuyao   Sleep   691 2
677955  fuyao_application_dev   172.16.10.17    fuyao_application_dev   Sleep   295 2
678239  fuyao_approval_dev  172.16.10.17    fuyao_approval_dev  Sleep   67  2
677251  fuyao_costcontrol_dev   172.16.10.16    fuyao_costcontrol_dev   Sleep   22  2
677854  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   384 2
677462  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   873 2
677540  ent_fserver_env 172.16.10.16    ent_fserver_env_fuyao   Sleep   748 2
678086  ytfs    172.16.2.111    YTFS    Sleep   171 2
677338  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   1020    2
678241  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   63  2
678253  fuyao_approval_dev  172.16.10.17    fuyao_approval_dev  Sleep   51  2
677922  fuyao_application_dev   172.16.10.17    fuyao_application_dev   Sleep   329 2
677963  fuyao_application_dev   172.16.10.17    fuyao_application_dev   Sleep   291 2
676771  fuyao_invoice_dev   172.16.10.17    fuyao_invoice_dev   Sleep   1742    2
677962  fuyao_application_dev   172.16.10.17    fuyao_application_dev   Sleep   291 2
677034  fuyao_approval_dev  172.16.10.17    fuyao_approval_dev  Sleep   1395    2
678210  fuyao_approval_dev  172.16.10.16    fuyao_approval_dev  Sleep   94  2
678180  fuyao_approval_dev  172.16.10.16    fuyao_approval_dev  Sleep   94  2
677945  fuyao_application_dev   172.16.10.17    fuyao_application_dev   Sleep   303 2
677851  fuyao_invoice_dev   172.16.10.17    fuyao_invoice_dev   Sleep   387 2
678215  fuyao_approval_dev  172.16.10.16    fuyao_approval_dev  Sleep   94  2
641620  hrbase  112.26.202.18   HRBASE_UAT2 Sleep   9883    2
677382  fuyao_costcontrol_dev   172.16.10.16    fuyao_costcontrol_dev   Sleep   979 2
678211  fuyao_approval_dev  172.16.10.16    fuyao_approval_dev  Sleep   94  2
678268  hrbase  192.168.10.110  HRBASE_UAT2 Sleep   35  2
677248  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   1114    2
677478  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   845 2
678055  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   211 2
677254  fuyao_costcontrol_dev   172.16.10.16    fuyao_costcontrol_dev   Sleep   1108    2
676794  fuyao_approval_dev  172.16.10.17    fuyao_approval_dev  Sleep   1712    2
677888  fuyao_user_dev  172.16.10.16    fuyao_user_dev  Sleep   8   2
677145  ytfs    172.16.2.110    YTFS    Sleep   1239    2
678217  fuyao_approval_dev  172.16.10.16    fuyao_approval_dev  Sleep   94  2
676827  fuyao_approval_dev  172.16.10.17    fuyao_approval_dev  Sleep   1671    2
678158  ares_ent_service_cloud  172.16.10.17    ares_ent_service_cloud  Sleep   97  2
677340  fuyao_costcontrol_dev   172.16.10.16    fuyao_costcontrol_dev   Sleep   1018    2
677999  ytfs    172.16.1.70 YTFS_OP Sleep   269 2
677801  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   436 2
678183  fuyao_approval_dev  172.16.10.16    fuyao_approval_dev  Sleep   94  2
676822  fuyao_approval_dev  172.16.10.17    fuyao_approval_dev  Sleep   1678    2
677857  fuyao_application_dev   172.16.10.17    fuyao_application_dev   Sleep   24  2
677227  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   1124    2
678265  fuyao_approval_dev  172.16.10.16    fuyao_approval_dev  Sleep   36  2
678207  fuyao_approval_dev  172.16.10.16    fuyao_approval_dev  Sleep   94  2
642502  root    192.168.10.143  fuyao_application_dev   Sleep   27582   2
678269  hrbase  192.168.10.110  HRBASE_UAT2 Sleep   35  2
678228  root    172.16.10.16    ares_ent_service_dev    Sleep   81  2
677747  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   502 2
388808  root    172.16.10.70    dmcp    Sleep   72856   2
677362  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   997 2
678273  hrbase  192.168.10.110  HRBASE_UAT2 Sleep   33  2
678091  fuyao_invoice_dev   172.16.10.17    fuyao_invoice_dev   Sleep   162 2
588744  hrbase  172.16.10.18    HRBASE_UAT2 Sleep   1095    2
678166  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   95  2
677504  fuyao_invoice_dev   172.16.10.17    fuyao_invoice_dev   Sleep   813 2
677725  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   520 2
678277  hrbase  172.16.10.16    HRBASE_UAT2 Sleep   21  2
677971  fuyao_application_dev   172.16.10.17    fuyao_application_dev   Sleep   284 2
676814  fuyao_pursale_dev   172.16.10.16    fuyao_pursale_dev   Sleep   1684    2
677811  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   419 2
677480  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   839 2
641531  root    192.168.10.9    ent_fserver_env_fuyao   Sleep   22075   2
637444  ares_ent_service_cloud  172.16.10.17    ares_ent_service_cloud  Sleep   13684   2
678223  ytfs    172.16.10.17    YTFS    Sleep   89  2
677966  fuyao_application_dev   172.16.10.17    fuyao_application_dev   Sleep   288 2
678248  fuyao_approval_dev  172.16.10.16    fuyao_approval_dev  Sleep   54  2
677476  fuyao_invoice_dev   172.16.10.17    fuyao_invoice_dev   Sleep   847 2
678278  hrbase  172.16.10.16    HRBASE_UAT2 Sleep   19  2
678039  fuyao_invoice_dev   172.16.10.17    fuyao_invoice_dev   Sleep   219 2
388809  root    172.16.10.70    dmcp    Sleep   72856   2
675492  root    192.168.10.114      Sleep   3199    2
678251  hrbase  172.16.10.18    HRBASE_UAT2 Sleep   52  2
641537  root    192.168.10.9    ent_fserver_env_fuyao   Sleep   22075   2
674954  root    192.168.10.114  app_market_dev  Query   0   2   show processlist
677907  fuyao_invoice_dev   172.16.10.17    fuyao_invoice_dev   Sleep   335 2
677358  fuyao_costcontrol_dev   172.16.10.16    fuyao_costcontrol_dev   Sleep   999 2
676889  fuyao_approval_dev  172.16.10.17    fuyao_approval_dev  Sleep   1593    2
678245  hrbase  172.16.10.18    HRBASE_UAT2 Sleep   58  2
677379  fuyao_costcontrol_dev   172.16.10.16    fuyao_costcontrol_dev   Sleep   982 2
677080  root    192.168.11.188  fuyao_user_dev  Sleep   1337    2
677623  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   655 2
677164  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   1231    2
677807  fuyao_invoice_dev   172.16.10.17    fuyao_invoice_dev   Sleep   430 2
678124  fuyao_user_dev  172.16.10.16    fuyao_user_dev  Sleep   126 2
677506  fuyao_pursale_dev   172.16.10.16    fuyao_pursale_dev   Sleep   809 2
677208  ytfs    172.16.10.17    YTFS    Sleep   1152    2
677534  app_market_dev  172.16.10.16    app_market_dev  Sleep   50  2
677703  fuyao_invoice_dev   172.16.10.17    fuyao_invoice_dev   Sleep   553 2
678280  hrbase  172.16.10.16    HRBASE_UAT2 Sleep   18  2
678279  hrbase  172.16.10.16    HRBASE_UAT2 Sleep   18  2
657740  root    192.168.10.143  fuyao_approval_dev  Sleep   23095   2
677325  fuyao_pursale_dev   172.16.10.16    fuyao_pursale_dev   Sleep   1034    2
589554  ares_ent_service_cloud  172.16.10.17    ares_ent_service_cloud  Sleep   23421   2
677273  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   1082    2
677808  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   430 2
676753  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   1757    2
673612  root    172.16.10.18    cloud_gateway_console   Sleep   46  2
677615  ent_fserver_env 172.16.10.16    ent_fserver_env_fuyao   Sleep   665 2
678093  fuyao_user_dev  172.16.10.16    fuyao_user_dev  Sleep   160 2
676941  eolinker_os 172.16.10.16    eolinker_os Sleep   1532    2
677423  fuyao_costcontrol_dev   172.16.10.16    fuyao_costcontrol_dev   Sleep   921 2
671425  root    192.168.11.157  HRBASE_UAT2 Sleep   7503    2
671428  root    192.168.11.157  HRBASE_UAT2 Sleep   7503    2
676911  fuyao_pursale_dev   172.16.10.16    fuyao_pursale_dev   Sleep   1562    2
677525  fuyao_invoice_dev   172.16.10.17    fuyao_invoice_dev   Sleep   770 2
677374  fuyao_pursale_dev   172.16.10.16    fuyao_pursale_dev   Sleep   988 2
676762  fuyao_approval_dev  172.16.10.17    fuyao_approval_dev  Sleep   1752    2
677867  fuyao_invoice_dev   172.16.10.17    fuyao_invoice_dev   Sleep   372 2
677968  ytfs    172.16.1.70 YTFS_OP Sleep   286 2
588745  hrbase  172.16.10.18    HRBASE_UAT2 Sleep   2633    2
671859  root    192.168.10.131  fuyao_approval_dev  Sleep   1332    2
678286  hrbase  172.16.10.18    HRBASE_UAT2 Sleep   4   2
677424  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   917 2
677527  fuyao_invoice_dev   172.16.10.17    fuyao_invoice_dev   Sleep   768 2
678174  fuyao_approval_dev  172.16.10.16    fuyao_approval_dev  Sleep   35  2
44624   ares_ent_service_cloud  172.16.10.17    ares_ent_service_cloud  Sleep   814 2
677727  ytfs    172.16.0.100    YTFS    Sleep   514 2
678072  ytfs    172.16.2.111    YTFS    Sleep   190 2
678081  root    172.16.10.16    cloud_gateway_console   Sleep   34  2
676764  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   1752    2
677343  fuyao_costcontrol_dev   172.16.10.16    fuyao_costcontrol_dev   Sleep   1014    2
677522  eolinker_os 172.16.10.16    eolinker_os Sleep   773 2
678003  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   262 2
641619  hrbase  112.26.202.18   HRBASE_UAT2 Sleep   9883    2
677921  fuyao_invoice_dev   172.16.10.17    fuyao_invoice_dev   Sleep   331 2
677602  ent_fserver_env 172.16.10.16    ent_fserver_env_fuyao   Sleep   677 2
601102  ares_ent_service_cloud  172.16.10.17    ares_ent_service_cloud  Sleep   5707    2
672520  hrbase  172.16.10.18    HRBASE_UAT2 Sleep   415 2
677563  ent_fserver_env 172.16.10.16    ent_fserver_env_fuyao   Sleep   720 2
678006  fuyao_application_dev   172.16.10.17    fuyao_application_dev   Sleep   258 2
677245  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   1115    2
677616  ent_fserver_env 172.16.10.16    ent_fserver_env_fuyao   Sleep   665 2
677389  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   967 2
675495  root    192.168.10.114  HRBASE_UAT2 Sleep   3198    2
677429  fuyao_costcontrol_dev   172.16.10.16    fuyao_costcontrol_dev   Sleep   910 2
677033  fuyao_pursale_dev   172.16.10.16    fuyao_pursale_dev   Sleep   1395    2
674547  root    192.168.10.121  app_market_dev  Sleep   2187    2
641644  root    192.168.10.132  cloud_gateway_console   Sleep   18367   2
678125  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   124 2
671427  root    192.168.11.157  HRBASE_UAT2 Sleep   7502    2
678016  fuyao_application_dev   172.16.10.17    fuyao_application_dev   Sleep   248 2
678203  fuyao_approval_dev  172.16.10.16    fuyao_approval_dev  Sleep   94  2
676829  fuyao_approval_dev  172.16.10.17    fuyao_approval_dev  Sleep   1670    2
677668  fuyao_invoice_dev   172.16.10.17    fuyao_invoice_dev   Sleep   592 2
677182  fuyao_costcontrol_dev   172.16.10.16    fuyao_costcontrol_dev   Sleep   36  2
677903  fuyao_application_dev   172.16.10.17    fuyao_application_dev   Sleep   335 2
676839  root    112.26.202.18   ent_fserver_env_fuyao   Sleep   1652    2
678007  fuyao_invoice_dev   172.16.10.17    fuyao_invoice_dev   Sleep   258 2
677107  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   1296    2
677519  eolinker_os 172.16.10.16    eolinker_os Sleep   778 2
678029  fuyao_pursale_dev   172.16.10.16    fuyao_pursale_dev   Sleep   234 2
678218  fuyao_approval_dev  172.16.10.16    fuyao_approval_dev  Sleep   94  2
677376  fuyao_costcontrol_dev   172.16.10.16    fuyao_costcontrol_dev   Sleep   985 2
588742  hrbase  172.16.10.18    HRBASE_UAT2 Sleep   2633    2
678025  fuyao_approval_dev  172.16.10.17    fuyao_approval_dev  Sleep   237 2
677995  ytfs    172.16.10.17    YTFS    Sleep   271 2
677780  fuyao_approval_dev  172.16.10.17    fuyao_approval_dev  Sleep   454 2
657082  root    192.168.10.143  fuyao_application_dev   Sleep   24198   2
678044  fuyao_application_dev   172.16.10.17    fuyao_application_dev   Sleep   216 2
678000  fuyao_application_dev   172.16.10.17    fuyao_application_dev   Sleep   264 2
678213  fuyao_approval_dev  172.16.10.16    fuyao_approval_dev  Sleep   94  2
677835  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   399 2
677876  ytfs    172.16.1.70 YTFS_OP Sleep   359 2
678177  fuyao_approval_dev  172.16.10.16    fuyao_approval_dev  Sleep   35  2
678257  hrbase  172.16.10.18    HRBASE_UAT2 Sleep   39  2
677832  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   406 2
677422  fuyao_costcontrol_dev   172.16.10.16    fuyao_costcontrol_dev   Sleep   924 2
678199  fuyao_approval_dev  172.16.10.16    fuyao_approval_dev  Sleep   94  2
677282  ent_fserver_env 172.16.10.16    ent_fserver_env_fuyao   Sleep   1066    2
677868  hrbase  172.16.10.18    PIECE_WORK_UAT  Sleep   104 2
676835  fuyao_approval_dev  172.16.10.17    fuyao_approval_dev  Sleep   1656    2
676837  root    112.26.202.18   ent_fserver_env_fuyao   Sleep   1654    2
678282  hrbase  172.16.10.16    HRBASE_UAT2 Sleep   15  2
678250  hrbase  172.16.10.18    HRBASE_UAT2 Sleep   52  2
677261  fuyao_costcontrol_dev   172.16.10.16    fuyao_costcontrol_dev   Sleep   1101    2
677367  fuyao_pursale_dev   172.16.10.16    fuyao_pursale_dev   Sleep   995 2
678153  ares_ent_service_cloud  172.16.10.17    ares_ent_service_cloud  Sleep   97  2
678212  fuyao_approval_dev  172.16.10.16    fuyao_approval_dev  Sleep   94  2
677646  fuyao_pursale_dev   172.16.10.16    fuyao_pursale_dev   Sleep   621 2
677853  ytfs    172.16.0.100    YTFS    Sleep   385 2
677959  fuyao_application_dev   172.16.10.17    fuyao_application_dev   Sleep   293 2
678263  hrbase  192.168.10.110  HRBASE_UAT2 Sleep   36  2
677202  ent_fserver_env 172.16.10.16    ent_fserver_env_fuyao   Sleep   177 2
641645  root    192.168.10.132  ares_ent_service_cloud  Sleep   18371   2
677547  fuyao_invoice_dev   172.16.10.17    fuyao_invoice_dev   Sleep   735 2
677342  fuyao_pursale_dev   172.16.10.16    fuyao_pursale_dev   Sleep   1018    2
677642  fuyao_invoice_dev   172.16.10.17    fuyao_invoice_dev   Sleep   631 2
388811  root    172.16.10.70    dmcp    Sleep   0   2
677940  eolinker_os 172.16.10.16    eolinker_os Sleep   305 2
678015  app_market_dev  172.16.10.16    app_market_dev  Sleep   250 2
678009  fuyao_application_dev   172.16.10.17    fuyao_application_dev   Sleep   255 2
677561  ent_fserver_env 172.16.10.16    ent_fserver_env_fuyao   Sleep   722 2
677681  fuyao_pursale_dev   172.16.10.16    fuyao_pursale_dev   Sleep   578 2
677778  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   455 2
677733  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   511 2
678111  fuyao_approval_dev  172.16.10.17    fuyao_approval_dev  Sleep   145 2
677741  root    172.16.10.70    dmcp    Sleep   510 2
677723  fuyao_pursale_dev   172.16.10.16    fuyao_pursale_dev   Sleep   521 2
678075  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   181 2
677596  ent_fserver_env 172.16.10.16    ent_fserver_env_fuyao   Sleep   686 2
677550  ent_fserver_env 172.16.10.16    ent_fserver_env_fuyao   Sleep   733 2
388807  root    172.16.10.70    dmcp    Sleep   6   2
639871  ares_ent_service_cloud  172.16.10.17    ares_ent_service_cloud  Sleep   177 2
678208  fuyao_approval_dev  172.16.10.16    fuyao_approval_dev  Sleep   94  2
677915  ytfs    172.16.2.110    YTFS    Sleep   332 2
678129  root    172.16.10.16    ares_ent_service_dev    Sleep   122 2
678272  hrbase  192.168.10.110  HRBASE_UAT2 Sleep   34  2
671660  root    192.168.11.161      Sleep   614 2
677178  fuyao_approval_dev  172.16.10.17    fuyao_approval_dev  Sleep   1194    2
676899  fuyao_approval_dev  172.16.10.17    fuyao_approval_dev  Sleep   1580    2
678201  fuyao_approval_dev  172.16.10.16    fuyao_approval_dev  Sleep   94  2
677956  fuyao_application_dev   172.16.10.17    fuyao_application_dev   Sleep   295 2
678168  fuyao_approval_dev  172.16.10.16    fuyao_approval_dev  Sleep   21  2
677633  root    172.16.10.70    dmcp    Sleep   646 2
676841  root    112.26.202.18   ent_fserver_env_fuyao   Sleep   1654    2
676730  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   1780    2
678018  fuyao_application_dev   172.16.10.17    fuyao_application_dev   Sleep   245 2
677675  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   587 2
677255  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   1108    2
677544  ent_fserver_env 172.16.10.16    ent_fserver_env_fuyao   Sleep   738 2
677564  fuyao_invoice_dev   172.16.10.17    fuyao_invoice_dev   Sleep   720 2
388804  root    172.16.10.70    dmcp    Sleep   7   2
677383  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   975 2
677774  fuyao_invoice_dev   172.16.10.17    fuyao_invoice_dev   Sleep   466 2
676954  fuyao_approval_dev  172.16.10.17    fuyao_approval_dev  Sleep   1504    2
678270  hrbase  192.168.10.110  HRBASE_UAT2 Sleep   35  2
639872  ares_ent_service_cloud  172.16.10.17    ares_ent_service_cloud  Sleep   5706    2
388802  root    172.16.10.70    dmcp    Sleep   369786  2
671661  root    192.168.11.161      Sleep   5200    2
677319  fuyao_pursale_dev   172.16.10.16    fuyao_pursale_dev   Sleep   1046    2
588751  hrbase  172.16.10.18    HRBASE_UAT2 Sleep   2081    2
677882  fuyao_application_dev   172.16.10.17    fuyao_application_dev   Sleep   28  2
678065  fuyao_pursale_dev   172.16.10.16    fuyao_pursale_dev   Sleep   200 2
677794  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   447 2
677607  fuyao_invoice_dev   172.16.10.17    fuyao_invoice_dev   Sleep   671 2
677132  hrbase  172.16.10.18    nacos_test  Sleep   0   2
677081  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   1337    2
678027  fuyao_pursale_dev   172.16.10.16    fuyao_pursale_dev   Sleep   237 2
677765  fuyao_invoice_dev   172.16.10.17    fuyao_invoice_dev   Sleep   475 2
677998  fuyao_application_dev   172.16.10.17    fuyao_application_dev   Sleep   270 2
674629  root    172.16.10.16    cloud_gateway_console   Sleep   27  2
678222  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   93  2
676862  fuyao_approval_dev  172.16.10.17    fuyao_approval_dev  Sleep   1632    2
668057  root    192.168.10.158  ares_ent_service_cloud  Sleep   6922    2
677972  fuyao_application_dev   172.16.10.17    fuyao_application_dev   Sleep   284 2
677287  fuyao_costcontrol_dev   172.16.10.16    fuyao_costcontrol_dev   Sleep   1060    2
677776  fuyao_invoice_dev   172.16.10.17    fuyao_invoice_dev   Sleep   464 2
677621  ent_fserver_env 172.16.10.16    ent_fserver_env_fuyao   Sleep   657 2
678237  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   72  2
677349  ytfs    172.16.10.17    YTFS    Sleep   1004    2
677493  fuyao_application_dev   172.16.10.17    fuyao_application_dev   Sleep   28  2
677377  ytfs    172.16.0.100    YTFS    Sleep   983 2
677977  fuyao_application_dev   172.16.10.17    fuyao_application_dev   Sleep   282 2
676778  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   1736    2
677656  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   603 2
678155  ares_ent_service_cloud  172.16.10.17    ares_ent_service_cloud  Sleep   97  2
678274  hrbase  172.16.10.16    HRBASE_UAT2 Sleep   27  2
388805  root    172.16.10.70    dmcp    Sleep   5816    2
676993  app_market_dev  172.16.10.70    app_market_dev  Sleep   142 2
677974  fuyao_application_dev   172.16.10.17    fuyao_application_dev   Sleep   283 2
677941  fuyao_application_dev   172.16.10.17    fuyao_application_dev   Sleep   305 2
678160  ares_ent_service_cloud  172.16.10.17    ares_ent_service_cloud  Sleep   50  2
678261  fuyao_approval_dev  172.16.10.17    fuyao_approval_dev  Sleep   38  2
677569  ent_fserver_env 172.16.10.16    ent_fserver_env_fuyao   Sleep   714 2
678281  fuyao_approval_dev  172.16.10.17    fuyao_approval_dev  Sleep   17  2
677613  ent_fserver_env 172.16.10.16    ent_fserver_env_fuyao   Sleep   668 2
675590  root    172.16.10.16    cloud_gateway_console   Sleep   49  2
676964  fuyao_approval_dev  172.16.10.17    fuyao_approval_dev  Sleep   1492    2
677598  fuyao_pursale_dev   172.16.10.16    fuyao_pursale_dev   Sleep   682 2
588749  hrbase  172.16.10.18    HRBASE_UAT2 Sleep   1948    2
677973  fuyao_invoice_dev   172.16.10.17    fuyao_invoice_dev   Sleep   284 2
677332  fuyao_costcontrol_dev   172.16.10.16    fuyao_costcontrol_dev   Sleep   1028    2
678058  hrbase  112.26.202.18   ares_ent_service_dev    Sleep   205 2
678219  fuyao_approval_dev  172.16.10.16    fuyao_approval_dev  Sleep   94  2
677879  fuyao_application_dev   172.16.10.17    fuyao_application_dev   Sleep   28  2
677926  fuyao_application_dev   172.16.10.17    fuyao_application_dev   Sleep   322 2
678108  root    172.16.10.16    cloud_gateway_console   Sleep   149 2
678204  fuyao_approval_dev  172.16.10.16    fuyao_approval_dev  Sleep   94  2
677520  fuyao_invoice_dev   172.16.10.17    fuyao_invoice_dev   Sleep   777 2
678189  fuyao_approval_dev  172.16.10.16    fuyao_approval_dev  Sleep   94  2
677463  fuyao_pursale_dev   172.16.10.16    fuyao_pursale_dev   Sleep   870 2
676805  fuyao_pursale_dev   172.16.10.16    fuyao_pursale_dev   Sleep   1699    2
676826  fuyao_approval_dev  172.16.10.17    fuyao_approval_dev  Sleep   1673    2
677852  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   386 2
675494  root    192.168.10.114      Sleep   3198    2
678235  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   75  2
639858  ares_ent_service_cloud  172.16.10.17    ares_ent_service_cloud  Sleep   5706    2
677899  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   340 2
677627  ent_fserver_env 172.16.10.16    ent_fserver_env_fuyao   Sleep   650 2
678243  fuyao_costcontrol_dev   172.16.10.16    fuyao_costcontrol_dev   Sleep   62  2
676831  fuyao_invoice_dev   172.16.10.17    fuyao_invoice_dev   Sleep   1669    2
678056  fuyao_pursale_dev   172.16.10.16    fuyao_pursale_dev   Sleep   209 2
676907  fuyao_approval_dev  172.16.10.17    fuyao_approval_dev  Sleep   1570    2
676925  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   1536    2
677671  fuyao_pursale_dev   172.16.10.16    fuyao_pursale_dev   Sleep   590 2
677028  fuyao_approval_dev  172.16.10.17    fuyao_approval_dev  Sleep   1404    2
677762  fuyao_pursale_dev   172.16.10.16    fuyao_pursale_dev   Sleep   482 2
677161  fuyao_approval_dev  172.16.10.17    fuyao_approval_dev  Sleep   1233    2
676898  fuyao_approval_dev  172.16.10.17    fuyao_approval_dev  Sleep   1580    2
677745  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   504 2
677855  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   384 2
678226  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   83  2
677752  fuyao_pursale_dev   172.16.10.16    fuyao_pursale_dev   Sleep   500 2
678256  fuyao_approval_dev  172.16.10.17    fuyao_approval_dev  Sleep   45  2
677328  fuyao_costcontrol_dev   172.16.10.16    fuyao_costcontrol_dev   Sleep   1032    2
677791  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   451 2
677944  fuyao_application_dev   172.16.10.17    fuyao_application_dev   Sleep   304 2
675593  root    172.16.10.16    cloud_gateway_console   Sleep   177 2
677323  fuyao_costcontrol_dev   172.16.10.16    fuyao_costcontrol_dev   Sleep   1036    2
677452  eolinker_os 172.16.10.16    eolinker_os Sleep   878 2
678254  hrbase  172.16.10.18    HRBASE_UAT2 Sleep   49  2
677252  root    172.16.10.70    dmcp    Sleep   1111    2
676873  fuyao_approval_dev  172.16.10.17    fuyao_approval_dev  Sleep   1618    2
678038  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   226 2
676807  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   1695    2
677810  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   422 2
677570  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   712 2
678023  fuyao_invoice_dev   172.16.10.17    fuyao_invoice_dev   Sleep   239 2
676951  hrbase  172.16.10.18    PIECE_WORK_UAT  Sleep   73  2
677893  fuyao_pursale_dev   172.16.10.16    fuyao_pursale_dev   Sleep   347 2
677938  hrbase  172.16.10.18    PIECE_WORK_UAT  Sleep   127 2
677213  ent_fserver_env 172.16.10.16    ent_fserver_env_fuyao   Sleep   1147    2
639875  ares_ent_service_cloud  172.16.10.17    ares_ent_service_cloud  Sleep   6742    2
677753  eolinker_os 172.16.10.16    eolinker_os Sleep   499 2
657053  hrbase  192.168.10.122  HRBASE_UAT2 Sleep   7868    2
677779  fuyao_invoice_dev   172.16.10.17    fuyao_invoice_dev   Sleep   455 2
677997  fuyao_application_dev   172.16.10.17    fuyao_application_dev   Sleep   270 2
388806  root    172.16.10.70    dmcp    Sleep   7   2
677392  fuyao_costcontrol_dev   172.16.10.16    fuyao_costcontrol_dev   Sleep   965 2
677680  ytfs    172.16.2.111    YTFS    Sleep   580 2
677394  fuyao_costcontrol_dev   172.16.10.16    fuyao_costcontrol_dev   Sleep   962 2
677345  fuyao_costcontrol_dev   172.16.10.16    fuyao_costcontrol_dev   Sleep   1011    2
677748  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   502 2
677990  app_market_dev  172.16.10.70    app_market_dev  Sleep   28  2
677870  fuyao_pursale_dev   172.16.10.16    fuyao_pursale_dev   Sleep   366 2
677743  fuyao_pursale_dev   172.16.10.16    fuyao_pursale_dev   Sleep   507 2
674727  root    172.16.10.18    cloud_gateway_console   Sleep   106 2
678229  fuyao_pursale_dev   172.16.10.16    fuyao_pursale_dev   Sleep   80  2
677749  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   501 2
677898  hrbase  172.16.10.18    PIECE_WORK_UAT  Sleep   100 2
677361  fuyao_costcontrol_dev   172.16.10.16    fuyao_costcontrol_dev   Sleep   998 2
677044  fuyao_approval_dev  172.16.10.17    fuyao_approval_dev  Sleep   1372    2
678079  root    172.16.10.16    cloud_gateway_console   Sleep   177 2
677512  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   791 2
678036  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   227 2
677943  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   304 2
677620  ent_fserver_env 172.16.10.16    ent_fserver_env_fuyao   Sleep   657 2
677769  fuyao_invoice_dev   172.16.10.17    fuyao_invoice_dev   Sleep   471 2
677763  fuyao_invoice_dev   172.16.10.17    fuyao_invoice_dev   Sleep   480 2
678130  fuyao_costcontrol_dev   172.16.10.16    fuyao_costcontrol_dev   Sleep   122 2
677320  ent_fserver_env 172.16.10.16    ent_fserver_env_fuyao   Sleep   1042    2
678233  fuyao_invoice_dev   172.16.10.17    fuyao_invoice_dev   Sleep   77  2
671662  root    192.168.11.161  smart_hro   Sleep   6999    2
678014  fuyao_application_dev   172.16.10.17    fuyao_application_dev   Sleep   250 2
678034  app_market_dev  172.16.10.17    app_market_dev  Sleep   229 2
677649  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   617 2
678133  fuyao_approval_dev  172.16.10.17    fuyao_approval_dev  Sleep   121 2
678170  fuyao_approval_dev  172.16.10.16    fuyao_approval_dev  Sleep   3   2
677862  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   377 2
677149  fuyao_approval_dev  172.16.10.17    fuyao_approval_dev  Sleep   1238    2
588748  hrbase  172.16.10.18    HRBASE_UAT2 Sleep   2633    2
677579  ent_fserver_env 172.16.10.16    ent_fserver_env_fuyao   Sleep   705 2
677946  fuyao_application_dev   172.16.10.17    fuyao_application_dev   Sleep   302 2
678287  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   3   2
676380  hrbase  172.16.10.18    PIECE_WORK_UAT  Sleep   93  2
677588  ent_fserver_env 172.16.10.16    ent_fserver_env_fuyao   Sleep   692 2
677976  fuyao_application_dev   172.16.10.17    fuyao_application_dev   Sleep   283 2
678206  fuyao_approval_dev  172.16.10.16    fuyao_approval_dev  Sleep   94  2
678159  ares_ent_service_cloud  172.16.10.17    ares_ent_service_cloud  Sleep   49  2
678161  ares_ent_service_cloud  172.16.10.17    ares_ent_service_cloud  Sleep   49  2
678156  ares_ent_service_cloud  172.16.10.17    ares_ent_service_cloud  Sleep   97  2
678214  fuyao_approval_dev  172.16.10.16    fuyao_approval_dev  Sleep   94  2
678185  fuyao_approval_dev  172.16.10.16    fuyao_approval_dev  Sleep   94  2
638779  ares_ent_service_cloud  172.16.10.17    ares_ent_service_cloud  Sleep   177 2
588747  hrbase  172.16.10.18    HRBASE_UAT2 Sleep   2627    2
677952  fuyao_application_dev   172.16.10.17    fuyao_application_dev   Sleep   297 2
678284  root    172.16.10.16    ares_ent_service_dev    Sleep   11  2
677931  root    172.16.10.16    ares_ent_service_dev    Sleep   317 2
657904  ares_ent_service_cloud  172.16.10.17    ares_ent_service_cloud  Sleep   3326    2
678066  fuyao_pursale_dev   172.16.10.16    fuyao_pursale_dev   Sleep   199 2
678260  hrbase  172.16.10.16    HRBASE_UAT2 Sleep   38  2
677538  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   750 2
677628  ent_fserver_env 172.16.10.16    ent_fserver_env_fuyao   Sleep   649 2
677860  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   379 2
678109  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   149 2
677682  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   576 2
677556  ent_fserver_env 172.16.10.16    ent_fserver_env_fuyao   Sleep   729 2
638493  ares_ent_service_cloud  172.16.10.17    ares_ent_service_cloud  Sleep   7261    2
677352  fuyao_costcontrol_dev   172.16.10.16    fuyao_costcontrol_dev   Sleep   1003    2
677618  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   662 2
677468  eolinker_os 172.16.10.16    eolinker_os Sleep   859 2
677226  fuyao_approval_dev  172.16.10.17    fuyao_approval_dev  Sleep   1125    2
676919  fuyao_costcontrol_dev   172.16.10.16    fuyao_costcontrol_dev   Sleep   20  2
678157  ares_ent_service_cloud  172.16.10.17    ares_ent_service_cloud  Sleep   97  2
677304  ent_fserver_env 172.16.10.16    ent_fserver_env_fuyao   Sleep   1053    2
677396  fuyao_pursale_dev   172.16.10.16    fuyao_pursale_dev   Sleep   953 2
678117  root    172.16.10.16    ares_ent_service_dev    Sleep   139 2
677599  ent_fserver_env 172.16.10.16    ent_fserver_env_fuyao   Sleep   681 2
676890  fuyao_approval_dev  172.16.10.17    fuyao_approval_dev  Sleep   1588    2
677594  ent_fserver_env 172.16.10.16    ent_fserver_env_fuyao   Sleep   689 2
676846  fuyao_approval_dev  172.16.10.17    fuyao_approval_dev  Sleep   1648    2
677697  fuyao_pursale_dev   172.16.10.16    fuyao_pursale_dev   Sleep   563 2
677086  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   1327    2
677906  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   335 2
678276  hrbase  172.16.10.16    HRBASE_UAT2 Sleep   22  2
677535  fuyao_pursale_dev   172.16.10.16    fuyao_pursale_dev   Sleep   759 2
678078  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   178 2
677291  ent_fserver_env 172.16.10.16    ent_fserver_env_fuyao   Sleep   1058    2
677930  fuyao_application_dev   172.16.10.17    fuyao_application_dev   Sleep   318 2
678017  fuyao_application_dev   172.16.10.17    fuyao_application_dev   Sleep   245 2
677344  fuyao_costcontrol_dev   172.16.10.16    fuyao_costcontrol_dev   Sleep   1014    2
678024  fuyao_application_dev   172.16.10.17    fuyao_application_dev   Sleep   238 2
677278  root    172.16.10.70    dmcp    Sleep   1072    2
678060  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   204 2
677324  fuyao_costcontrol_dev   172.16.10.16    fuyao_costcontrol_dev   Sleep   1035    2
678179  fuyao_approval_dev  172.16.10.16    fuyao_approval_dev  Sleep   94  2
678172  fuyao_approval_dev  172.16.10.16    fuyao_approval_dev  Sleep   33  2
678073  root    172.16.10.16    ares_ent_service_dev    Sleep   190 2
588743  hrbase  172.16.10.18    HRBASE_UAT2 Sleep   2633    2
678288  hrbase  172.16.10.16    HRBASE_UAT2 Sleep   3   2
677985  fuyao_application_dev   172.16.10.17    fuyao_application_dev   Sleep   274 2
677928  fuyao_pursale_dev   172.16.10.16    fuyao_pursale_dev   Sleep   320 2
677726  fuyao_invoice_dev   172.16.10.17    fuyao_invoice_dev   Sleep   518 2
676790  ytfs_console    172.16.10.17    ytfs_console    Sleep   1714    2
677448  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   881 2
677306  ytfs    172.16.2.110    YTFS    Sleep   1050    2
677871  ytfs    172.16.2.110    YTFS    Sleep   364 2
677339  fuyao_costcontrol_dev   172.16.10.16    fuyao_costcontrol_dev   Sleep   1019    2
678063  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   202 2
677077  root    192.168.11.188  app_market_dev  Sleep   1337    2
677259  fuyao_costcontrol_dev   172.16.10.16    fuyao_costcontrol_dev   Sleep   1103    2
588750  hrbase  172.16.10.18    HRBASE_UAT2 Sleep   2627    2
676844  fuyao_pursale_dev   172.16.10.16    fuyao_pursale_dev   Sleep   1650    2
678176  fuyao_approval_dev  172.16.10.16    fuyao_approval_dev  Sleep   35  2
678209  fuyao_approval_dev  172.16.10.16    fuyao_approval_dev  Sleep   94  2
677516  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   789 2
677249  fuyao_costcontrol_dev   172.16.10.16    fuyao_costcontrol_dev   Sleep   35  2
677840  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   393 2
676942  fuyao_approval_dev  172.16.10.17    fuyao_approval_dev  Sleep   1531    2
678019  fuyao_approval_dev  172.16.10.17    fuyao_approval_dev  Sleep   245 2
678192  fuyao_approval_dev  172.16.10.16    fuyao_approval_dev  Sleep   94  2
678106  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   153 2
678266  fuyao_approval_dev  172.16.10.16    fuyao_approval_dev  Sleep   36  2
677947  fuyao_application_dev   172.16.10.17    fuyao_application_dev   Sleep   302 2
677337  fuyao_costcontrol_dev   172.16.10.16    fuyao_costcontrol_dev   Sleep   1022    2
660877  hrbase  192.168.10.122  HRBASE_UAT2 Sleep   19515   2
677593  ent_fserver_env 172.16.10.16    ent_fserver_env_fuyao   Sleep   690 2
676772  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   1740    2
678200  fuyao_approval_dev  172.16.10.16    fuyao_approval_dev  Sleep   94  2
678022  root    172.16.10.16    ares_ent_service_dev    Sleep   239 2
677643  ent_fserver_env 172.16.10.16    ent_fserver_env_fuyao   Sleep   626 2
677551  ent_fserver_env 172.16.10.16    ent_fserver_env_fuyao   Sleep   731 2
677872  fuyao_invoice_dev   172.16.10.17    fuyao_invoice_dev   Sleep   363 2
677970  fuyao_invoice_dev   172.16.10.17    fuyao_invoice_dev   Sleep   284 2
668058  root    192.168.10.158  app_market_dev  Sleep   7207    2
677902  root    172.16.10.16    ares_ent_service_dev    Sleep   337 2
677597  ent_fserver_env 172.16.10.16    ent_fserver_env_fuyao   Sleep   683 2
657054  hrbase  192.168.10.122  HRBASE_UAT2 Sleep   6198    2
677065  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   1346    2
677276  fuyao_costcontrol_dev   172.16.10.16    fuyao_costcontrol_dev   Sleep   1076    2
677894  fuyao_approval_dev  172.16.10.17    fuyao_approval_dev  Sleep   346 2
677399  ytfs    172.16.0.100    YTFS    Sleep   950 2
677260  fuyao_costcontrol_dev   172.16.10.16    fuyao_costcontrol_dev   Sleep   1102    2
677560  ent_fserver_env 172.16.10.16    ent_fserver_env_fuyao   Sleep   722 2
678246  root    172.16.10.16    ares_ent_service_dev    Sleep   54  2
677878  fuyao_pursale_dev   172.16.10.16    fuyao_pursale_dev   Sleep   357 2
677443  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   883 2
677225  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   1126    2
677207  ent_fserver_env 172.16.10.16    ent_fserver_env_fuyao   Sleep   177 2
677258  fuyao_costcontrol_dev   172.16.10.16    fuyao_costcontrol_dev   Sleep   1104    2
640238  root    192.168.10.110  HRBASE_UAT2 Sleep   984 2
677795  fuyao_pursale_dev   172.16.10.16    fuyao_pursale_dev   Sleep   445 2
678194  fuyao_approval_dev  172.16.10.16    fuyao_approval_dev  Sleep   94  2
678187  fuyao_approval_dev  172.16.10.16    fuyao_approval_dev  Sleep   94  2
674546  root    192.168.10.121  ares_ent_service_dev    Sleep   4254    2
678202  fuyao_approval_dev  172.16.10.16    fuyao_approval_dev  Sleep   94  2
657746  root    192.168.10.143  fuyao_approval_dev  Sleep   23095   2
655942  root    192.168.10.110  HRBASE_UAT2 Sleep   19377   2
677875  fuyao_pursale_dev   172.16.10.16    fuyao_pursale_dev   Sleep   360 2
678196  fuyao_approval_dev  172.16.10.16    fuyao_approval_dev  Sleep   94  2
677078  root    192.168.11.188  app_market_dev  Sleep   1338    2
678247  hrbase  172.16.10.18    HRBASE_UAT2 Sleep   54  2
671857  root    192.168.10.131      Sleep   1416    2
640236  root    192.168.10.110  HRBASE_UAT2 Sleep   46011   2
677761  ytfs    172.16.2.110    YTFS    Sleep   483 2
677885  fuyao_application_dev   172.16.10.17    fuyao_application_dev   Sleep   28  2
677644  fuyao_pursale_dev   172.16.10.16    fuyao_pursale_dev   Sleep   626 2
678154  ares_ent_service_cloud  172.16.10.17    ares_ent_service_cloud  Sleep   97  2
677360  fuyao_costcontrol_dev   172.16.10.16    fuyao_costcontrol_dev   Sleep   998 2
677553  ent_fserver_env 172.16.10.16    ent_fserver_env_fuyao   Sleep   730 2
677638  ent_fserver_env 172.16.10.16    ent_fserver_env_fuyao   Sleep   636 2
678259  hrbase  192.168.10.110  HRBASE_UAT2 Sleep   38  2
677614  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   666 2
678175  fuyao_approval_dev  172.16.10.16    fuyao_approval_dev  Sleep   35  2
678205  fuyao_approval_dev  172.16.10.16    fuyao_approval_dev  Sleep   94  2
676793  fuyao_invoice_dev   172.16.10.17    fuyao_invoice_dev   Sleep   1713    2
676786  ytfs_console    172.16.10.17    ytfs_console    Sleep   1722    2
677975  fuyao_application_dev   172.16.10.17    fuyao_application_dev   Sleep   283 2
674817  hrbase  172.16.10.18    PIECE_WORK_UAT  Sleep   213 2
676970  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   1480    2
678262  hrbase  192.168.10.110  HRBASE_UAT2 Sleep   38  2
677007  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   1429    2
677419  fuyao_costcontrol_dev   172.16.10.16    fuyao_costcontrol_dev   Sleep   929 2
678238  hrbase  112.26.202.18   ares_ent_service_dev    Sleep   70  2
678271  hrbase  192.168.10.110  HRBASE_UAT2 Sleep   34  2
677942  fuyao_application_dev   172.16.10.17    fuyao_application_dev   Sleep   304 2
639873  ares_ent_service_cloud  172.16.10.17    ares_ent_service_cloud  Sleep   5706    2
677595  ent_fserver_env 172.16.10.16    ent_fserver_env_fuyao   Sleep   687 2
676967  fuyao_approval_dev  172.16.10.17    fuyao_approval_dev  Sleep   1487    2
678181  fuyao_approval_dev  172.16.10.16    fuyao_approval_dev  Sleep   94  2
677189  ytfs_console    172.16.10.17    ytfs_console    Sleep   1177    2
677708  fuyao_invoice_dev   172.16.10.17    fuyao_invoice_dev   Sleep   542 2
677102  hrbase  172.16.10.18    ares_ent_service_dev    Sleep   236 2
676744  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   1770    2
677934  fuyao_application_dev   172.16.10.17    fuyao_application_dev   Sleep   315 2
677873  fuyao_approval_dev  172.16.10.17    fuyao_approval_dev  Sleep   361 2
671858  root    192.168.10.131      Sleep   1416    2
676824  fuyao_approval_dev  172.16.10.17    fuyao_approval_dev  Sleep   1678    2
677006  fuyao_approval_dev  172.16.10.17    fuyao_approval_dev  Sleep   1430    2
677683  fuyao_invoice_dev   172.16.10.17    fuyao_invoice_dev   Sleep   573 2
677754  ytfs    172.16.2.111    YTFS    Sleep   498 2
677836  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   396 2
677881  hrbase  192.168.10.136  ares_ent_service_dev    Sleep   356 2
676737  fuyao_invoice_dev   172.16.10.17    fuyao_invoice_dev   Sleep   1773    2
677546  ent_fserver_env 172.16.10.16    ent_fserver_env_fuyao   Sleep   736 2
678285  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   4   2
677031  fuyao_pursale_dev   172.16.10.16    fuyao_pursale_dev   Sleep   1397    2
677239  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   1116    2
676785  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   1722    2
677436  ytfs    172.16.1.70 YTFS_OP Sleep   891 2
677874  fuyao_application_dev   172.16.10.17    fuyao_application_dev   Sleep   20  2
677286  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   1061    2
676947  fuyao_approval_dev  172.16.10.17    fuyao_approval_dev  Sleep   1516    2
677831  ytfs    172.16.10.17    YTFS    Sleep   408 2
676990  fuyao_approval_dev  172.16.10.17    fuyao_approval_dev  Sleep   1466    2
678193  fuyao_approval_dev  172.16.10.16    fuyao_approval_dev  Sleep   94  2
677891  fuyao_application_dev   172.16.10.17    fuyao_application_dev   Sleep   349 2
678178  fuyao_approval_dev  172.16.10.16    fuyao_approval_dev  Sleep   35  2
678112  root    172.16.10.17    ares_ent_service_dev    Sleep   144 2
678249  hrbase  172.16.10.18    HRBASE_UAT2 Sleep   54  2
677600  fuyao_invoice_dev   172.16.10.17    fuyao_invoice_dev   Sleep   680 2
678197  fuyao_approval_dev  172.16.10.16    fuyao_approval_dev  Sleep   94  2
677079  root    192.168.11.188  fuyao_user_dev  Sleep   1337    2
678107  root    172.16.10.16    cloud_gateway_console   Sleep   149 2
677543  ent_fserver_env 172.16.10.16    ent_fserver_env_fuyao   Sleep   738 2
678040  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   217 2
677378  fuyao_costcontrol_dev   172.16.10.16    fuyao_costcontrol_dev   Sleep   983 2
678264  hrbase  192.168.10.110  HRBASE_UAT2 Sleep   36  2
676801  fuyao_invoice_dev   172.16.10.17    fuyao_invoice_dev   Sleep   1703    2
678092  hrbase  192.168.10.136  ares_ent_service_dev    Sleep   161 2
677939  root    172.16.10.17    ares_ent_service_dev    Sleep   309 2
678138  fuyao_approval_dev  172.16.10.17    fuyao_approval_dev  Sleep   115 2
677485  ytfs    172.16.0.100    YTFS    Sleep   828 2
678258  ent_fserver_env 172.16.10.17    ent_fserver_env Sleep   39  2
677554  ent_fserver_env 172.16.10.16    ent_fserver_env_fuyao   Sleep   730 2
678191  fuyao_approval_dev  172.16.10.16    fuyao_approval_dev  Sleep   94  2
678145  fuyao_invoice_dev   172.16.10.17    fuyao_invoice_dev   Sleep   108 2
588746  hrbase  172.16.10.18    HRBASE_UAT2 Sleep   2527    2
638495  ares_ent_service_cloud  172.16.10.17    ares_ent_service_cloud  Sleep   43  2
677617  ent_fserver_env 172.16.10.16    ent_fserver_env_fuyao   Sleep   664 2
677236  fuyao_costcontrol_dev   172.16.10.16    fuyao_costcontrol_dev   Sleep   21  2
676819  hrbase  172.16.10.70    nacos_test  Sleep   1   2
678182  fuyao_approval_dev  172.16.10.16    fuyao_approval_dev  Sleep   94  2
678134  fuyao_costcontrol_dev   172.16.10.16    fuyao_costcontrol_dev   Sleep   120 2

+------+------+----------------------+---------+---------+------+----------+------------------+
| Id   | User | Host                 | db      | Command | Time | State    | Info             |
+------+------+----------------------+---------+---------+------+----------+------------------+
| 6288 | root | 58.243.43.2:14387    | db_blog | Sleep   | 1852 |          | NULL             |
| 6289 | root | 58.243.43.2:14388    | db_blog | Sleep   | 1852 |          | NULL             |
| 6290 | root | 118.182.97.157:33162 | db_blog | Sleep   |    0 |          | NULL             |
| 6291 | root | 118.182.97.157:33164 | db_blog | Sleep   |    0 |          | NULL             |
| 6292 | root | 118.182.97.157:33166 | db_blog | Sleep   |    0 |          | NULL             |
| 6293 | root | 118.182.97.157:33168 | db_blog | Sleep   |    0 |          | NULL             |
| 6294 | root | 118.182.97.157:33170 | db_blog | Sleep   |    1 |          | NULL             |
| 6295 | root | 118.182.97.157:33172 | db_blog | Sleep   |    0 |          | NULL             |
| 6296 | root | 118.182.97.157:33176 | db_blog | Sleep   |    0 |          | NULL             |
| 6297 | root | 118.182.97.157:33178 | db_blog | Sleep   |    0 |          | NULL             |
| 6298 | root | 118.182.97.157:33180 | db_blog | Sleep   |    0 |          | NULL             |
| 6299 | root | 118.182.97.157:33182 | db_blog | Sleep   |    0 |          | NULL             |
| 6300 | root | 58.243.43.2:14391    | db_blog | Query   |    0 | starting | show processlist |
| 6301 | root | 58.243.43.2:14392    | NULL    | Sleep   |  136 |          | NULL             |
+------+------+----------------------+---------+---------+------+----------+------------------+
14 rows in set (0.12 sec)

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

```sql
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
```

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

内置函数
String相关函数
https://dev.mysql.com/doc/refman/5.7/en/string-functions.html
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
国际数据工程会议（International Conference on Data Engineering，简称ICDE）是全球范围内顶级三大数据库学术会议之一

（1）*.frm--表定义，是描述表结构的文件。
（2）*.MYD--"D"数据信息文件，是表的数据文件。
（3）*.MYI--"I"索引信息文件，是表数据文件中任何索引的数据树。

ibd InnoDB存储数据的物理文件通常以ibd作为其文件名后缀

cvs

8.1 优化概述
https://www.kancloud.cn/baoguoxiao0538/mysql-8-0-chinese-doc/1117563

mysql 存储过程 源码实现
.ibd

开启 general log 将所有到达MySQL Server的SQL语句记录下来。存储方式有两种，一种是file ，一种是table
一般不会开启开功能，因为log的量会非常庞大。但个别情况下可能会临时的开一会儿general log以供排障使用。
相关参数一共有3：general_log、log_output、general_log_file

https://blog.csdn.net/intelrain/article/details/80451120

mysql 日志 查看select的结果

MYSQL-DBA书籍推荐
https://blog.csdn.net/qq_35254185/article/details/95341993

MySQL查询日志介绍
https://www.cnblogs.com/kerrycode/p/7130403.html

desc mysql.general_log;
select * from mysql.general_log order by event_time desc limit 0,11;

Available parameters are [collection, list]
决解Mybatis传递List集合报错 Available parameters are [collection, list]
https://blog.csdn.net/sinat_28978689/article/details/79406832

只有输入的sql，没有查询到的结果

mysqlbinlog

两个最重要的使用场景:
其一：MySQL Replication在Master端开启binlog，Mster把它的二进制日志传递给slaves来达到master-slave数据一致的目的。
其二：自然就是数据恢复了，通过使用mysqlbinlog工具来使恢复数据。

二进制日志包括两类文件：
二进制日志索引文件（文件名后缀为.index）用于记录所有的二进制文件；
二进制日志文件（文件名后缀为.00000*）记录数据库所有的DDL和DML(除了数据查询语句)语句事件。

show variables like 'log_bin';

log_bin 0

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

MySQL索引
https://blog.csdn.net/weixin_43844718/article/details/128225216

空间索引（spatial index）
MySQL在5.7版本以后 MyISAM 和 InnoDB 中都支持了空间索引，对空间数据类型的字段建立的索引，底层可通过 R树 实现，R树索引 用于多维信息的空间索引，使用较少。

添加空间索引（空间类型的字段必须为非空 字段的数字类型必须是geometry）：

```sql
alter table 表名 add 列 geometry;
alter table 表名 add spatial index 索引名 (列名);
```

聚簇索引（clustered index）
聚簇索引只有 InnoDB 支持，InnoDB 中的主键索引就是一种聚簇索引。

聚簇索引就是一个正常的B+树结构，其叶子节点中的data存放数据表中所有每一行的完整数据。
非聚簇索引其叶子节点的 data 中存的不是完整的数据，而是主键值。

因索引结构会产生两个情况：索引覆盖和回表。

索引覆盖：创建一个索引，该索引包含查询中用到的所有字段，只需要通过索引就可以查找和返回查询所需要的数据。
可以一次性完成查询工作，有效减少IO，提高查询效率。
covering index
https://dev.mysql.com/doc/refman/8.3/en/glossary.html#glos_covering_index

索引覆盖
结合上面的知识储备，我们进一步来优化一下刚才的SQL

select * from lyb_test where age = 12

当这条语句执行时，我们知道会进行两次索引树查询，第一次在二级索引上查询到主键索引的引用，然后到主键索引树中查询到所需要的数据，这个过程我们称之为回表。那为什么要有回表操作呢？由于查询的结果是所有字段，所需要的数据只有主键上才有，所以不得不回表。我们如果将sql改造为下面这种方式：

select id from lyb_test where age = 12

由于查询的值是ID，而id的值已经在age索引树上了，因此可以直接提供查询结果，不需要回表。也就是说，当SQL语句的所有查询字段(select列)和查询条件字段(where子句)全都包含在一个索引中，便可以直接使用索引查询而不需要回表。即在这个查询里，索引age已经“覆盖了”我们的查询需求，故称为索引覆盖。

select * from user_table where username like 'b%' and age >= 13
语句的执行过程有两种可能性：
根据(username，age)联合索引查询所有满足名称以"b"开头的索引，然后回表查询出相应的全行数据，再筛选出满足年龄大于等于13的用户数据。如果表中user_name以b开头的数据有n条，则需要回表n次
根据(username,age)联合索引查询所有满足名称以"b"开头的索引，然后直接再筛选出年龄大于等于13的索引，之后再回表查询全行数据。经过两次筛选之后，回表次数一定小于上述第一种情况
我们把第二种语句执行的过程称之为索引下推
在MySQL中，索引下推是默认启用的状态。在使用InnoDB存储引擎的数据表中，索引下推只能用于二级索引。我们可以通过修改MySQL系统变量来控制索引下推是否开启。设置如下：
SET optimizer_switch = 'index_condition_pushdown=off';// 关闭
SET optimizer_switch = 'index_condition_pushdown=on';// 开启
索引下推一般可用于所求查询字段(select列)不是/不全是联合索引的字段，查询条件为多条件查询且查询条件子句(where/order by)字段全是联合索引。

回表：顾名思义就是回到表中重新查询一次，也就是先通过二级索引查找到主键ID，然后在通过主键ID去查询聚簇索引找到一行的完整数据。
所以回表的产生也是需要一定条件的，如果一次索引查询就能获得所有的select 记录就不需要回表，如果select 所需获得列中有其他的非索引列，就会发生回表动作。即基于非主键索引的查询需要多扫描一棵索引树。

hash 索引
平衡树
b-树
b+树

InnoDB支持外键，而MyISAM不支持。
3，InnoDB是聚集索引，使用B+Tree作为索引结构，数据文件是和（主键）索引绑在一起的（表数据文件本身就是按B+Tree组织的一个索引结构），必须要有主键，通过主键索引效率很高。MyISAM是非聚集索引，也是使用B+Tree作为索引结构，索引和数据文件是分离的，索引保存的是数据文件的指针。主键索引和辅助索引是独立的。
4，InnoDB不保存表的具体行数，执行select count(*) from table时需要全表扫描。而MyISAM用一个变量保存了整个表的行数，执行上述语句时只需要读出该变量即可，速度很快。
5，Innodb不支持全文索引，而MyISAM支持全文索引，查询效率上MyISAM要高；5.7以后的InnoDB支持全文索引了。
6，InnoDB支持表、行级锁(默认)，而MyISAM支持表级锁。；
7，InnoDB表必须有主键（用户没有指定的话会自己找或生产一个主键），而Myisam可以没有。
8，Innodb存储文件有frm、ibd，而Myisam是frm、MYD、MYI。
Innodb：frm是表定义文件，ibd是数据文件。
Myisam：frm是表定义文件，myd是数据文件，myi是索引文件。

在 InnoDB 存储引擎中，索引文件不是以单独的文件形式存在，而是与数据文件（.ibd 文件）一起存储在表空间（tablespace）中。
InnoDB 使用表空间来组织和管理数据和索引。每个 InnoDB 表都有一个对应的表空间，其中包含了表的数据和索引。
在 InnoDB 存储引擎中，数据和索引是按照 B+ 树的结构组织的。B+ 树索引的数据存储在数据文件（.ibd 文件）中，而索引结构本身被存储在共享的表空间中。
因此，索引文件并不是独立存在的文件，而是与数据文件一同存储在表空间中。这种设计可以提高数据和索引之间的一致性，并提供更好的性能和可管理性。
需要注意的是，InnoDB 存储引擎还支持压缩表和分区表等特性，这些特性可能会对数据和索引的存储方式有所影响。但无论如何，索引文件都是与数据文件一起存储在表空间中。

阿里 P8 架构师谈:MySQL 慢查询优化、索引优化、以及表等优化总结
https://www.bilibili.com/video/av583428536/?vd_source=71b9c2a5f966942c83677c2110efde22

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

具体到Java代码，Connection对象不能随便新建，需要池化复用

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

https://blog.csdn.net/soonfly/article/details/70677138

XA的性能很低。一个数据库的事务和多个数据库间的XA事务性能对比可发现，性能差10倍左右。因此要尽量避免XA事务，例如可以将数据写入本地，用高性能的消息系统分发数据。或使用数据库复制等技术。只有在这些都无法实现，且性能不是瓶颈时才应该使用XA。

MySQL XA 的限制
在MySQL 5.7.7 之前，MySQL一直存在一个"bug"。在事务达到PREPARED状态后，客户端断开与MySQL的连接，MySQL 会自动回滚该事务，这个行为不符合分布式事务的规范，MySQL将PREPARED的事务丢失了。之所以MySQL这么实现是因为MySQL 5.7.7 之前PREPARED的事务并不会记录到binlog中。客户端退出后会丢失该信息，如果允许再提交，那么binlog缺少事务信息，会造成主从不一致。
在MySQL5.7.7之后，MySQL新增了一个XA_prepare_log_event的事件，会把xa start到xa prepare中间的操作记录到Binlog中。Slave读取Relay log 进行回放，当SQL Thread读取到PREPARED的事务后，在读取xa commit或者xa rollback前，会进行一个类似客户端断开的操作，继续读取后续的事务信息，不会阻塞SQL Thread的执行。从以上的结果看，Oracle在MySQL 5.7.7 上确实完美的解决了MySQL XA一直存在的一个"bug"。

MySQL XA 的实践
本人曾在某公司的分布式数据库项目组中实践过基于MySQL XA的分布式事务。MySQL XA 要满足线上高并发的访问要求，在使用时还需要解决两个问题：分布式死锁问题和分布式读一致性问题。分布式死锁问题是指MySQL Server 是可以检测和解决单个MySQL实例中的死锁问题，但涉及到跨越多个MySQL 实例的分布式事务时候，需要程序层面实现死锁的检测和解决。分布式读一致性问题是指MySQL的read view 也是实例级别的，对于全局分布式事务来说无法实现读一致，只能通过select ... lock in share mode在读请求上加锁的串行化隔离级别来实现，这必然会带来并发性能的下降。这就需要在程序层面构建全局的read view来实现全局的MVCC 。当然这两个问题，当时团队的大牛们都已经解决了，我也很有幸参与其中。

MySQL_XA介绍.mhtml
https://www.jianshu.com/p/7003d58ea182

MySQL书籍
http://mingxinglai.com/cn/2015/12/material-of-mysql/

MySQL索引背后的数据结构及算法原理.mhtml
http://blog.codinglabs.org/articles/theory-of-mysql-index.html

MySQL网络协议分析.mhtml
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

[MySQL查看InnoDB表中每个索引的高度](https://www.cnblogs.com/waterystone/p/6638531.html)

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

insert，返回值是：新插入行的主键（primary key）；需要包含`<selectKey>`语句，才会返回主键，否则返回值为null。
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

## 聚集索引

clustered index
https://dev.mysql.com/doc/refman/8.0/en/innodb-index-types.html

https://dev.mysql.com/doc/refman/8.0/en/glossary.html#glos_clustered_index

每个InnoDB表有一个特殊的指数称为聚集索引所在的行的数据存储。通常，聚集索引是主键的同义词。从查询，插入性能最好，和其他的数据库操作，必须了解InnoDB使用聚集索引来优化每个表最常见的查询和DML操作。 当你定义你的表的主键，InnoDB使用它作为聚集索引。为您创建的每个表定义一个主键。如果没有逻辑唯一的和非空的列或列集，添加一个新的自动增量列，它的值自动填充。 如果你不确定你的表的主键、唯一索引，MySQL定位第一所有键列不为空，InnoDB使用它作为聚集索引。 如果表没有主键或唯一索引InnoDB。

非聚集（unclustered）索引。
定义：该索引中索引的逻辑顺序与磁盘上行的物理存储顺序不同，一个表中可以拥有多个非聚集索引。
其实按照定义，除了聚集索引以外的索引都是非聚集索引，只是人们想细分一下非聚集索引，分成普通索引，唯一索引，全文索引。如果非要把非聚集索引类比成现实生活中的东西，那么非聚集索引就像新华字典的偏旁字典，他结构顺序与实际存放顺序不一定一致。

非聚集索引，分成普通索引，唯一索引，全文索引
非聚集索引（Non-clustered Index）是指不按照物理存储顺序进行索引的数据库索引。与聚集索引（Clustered Index）不同，非聚集索引不改变表中数据的物理顺序，而是创建一个单独的数据结构（通常是B-Tree）来存储索引的值和行数据的位置信息。

非聚集索引可以根据索引列的值进行排序，并且可以包含重复的值和空值。非聚集索引可以提高查询性能，因为它们可以帮助数据库引擎快速定位到表中满足特定条件的行数据，而不必扫描整个表。

非聚集索引可以分为以下几种类型：
普通索引（Normal Index）：这是最常见的非聚集索引类型，允许在索引列中包含重复的值和空值。
唯一索引（Unique Index）：唯一索引要求索引列中的值是唯一的，但允许有空值。如果试图在唯一索引中插入重复的值，则数据库会报错并阻止插入操作。
全文索引（Full-Text Index）：全文索引是一种特殊类型的非聚集索引，专门用于全文搜索。全文索引可以支持自然语言查询、布尔查询和查询扩展等高级搜索功能。与普通索引和唯一索引不同，全文索引不是基于B-Tree数据结构，而是基于倒排索引（Inverted Index）实现。
需要注意的是，不同类型的非聚集索引在数据库中的实现方式和使用场景可能会有所不同。具体选择哪种类型的非聚集索引取决于具体的业务需求和数据特征。

information_schema mysql元数据数据库 权限 密码 表引擎

## 面试题

数据库的acid属性分别由什么实现？
原子性 undo log
一致性 undo log
隔离性 mvcc 锁(悲观锁 乐观锁)
持久性 redo log

面试题1 ：为什么用B/B+树这种结构来实现索引呢？
红黑树等结构也可以用来实现索引，但是文件系统及数据库系统普遍使用B/B+树结构来实现索引。MySQL是基于磁盘的数据库，索引是以索引文件的形式存在于磁盘中的，索引的查找过程就会涉及到磁盘IO消耗，磁盘IO的消耗相比较于内存IO的消耗要高好几个数量级，所以索引的组织结构要设计得在查找关键字时要尽量减少磁盘IO的次数。为什么要使用B/B+树，跟磁盘的存储原理有关。
这里，局部性原理与磁盘预读。为了提升效率，要尽量减少磁盘IO的次数。实际过程中，磁盘并不是每次严格按需读取，而是每次都会预读。磁盘读取完需要的数据后，会按顺序再多读一部分数据到内存中，这样做的理论依据是计算机科学中注明的局部性原理：当一个数据被用到时，其附近的数据也通常会马上被使用。程序运行期间所需要的数据通常比较集中。（1）由于磁盘顺序读取的效率很高(不需要寻道时间，只需很少的旋转时间)，因此对于具有局部性的程序来说，预读可以提高I/O效率.预读的长度一般为页(page)的整倍数。（2）MySQL(默认使用InnoDB引擎),将记录按照页的方式进行管理,每页大小默认为16K(这个值可以修改)。Linux默认页大小为4K。
B-Tree借助计算机磁盘预读的机制，并使用如下技巧：每次新建节点时，直接申请一个页的空间，这样就保证一个节点物理上也存储在一个页里，加之计算机存储分配都是按页对齐的，就实现了一个结点只需一次I/O。假设B-Tree的高度为 h, B-Tree 中一次检索最多需要 h-1 次 I/O（根节点常驻内存），渐进复杂度为 O(h)=O(logdN)O(h)=O(logdN)。一般实际应用中，出度 d 是非常大的数字，通常超过 100，因此 h 非常小（通常不超过3，也即索引的 B+ 树层次一般不超过三层，所以查找效率很高）。而红黑树这种结构，h 明显要深的多。由于逻辑上很近的节点（父子）物理上可能很远，无法利用局部性，所以红黑树的 I/O 渐进复杂度也为 O(h)，效率明显比 B-Tree 差很多。

面试题2 ：为什么 MySQL 的索引使用 B+ 树而不是 B 树呢？
（1）B+ 树更适合外部存储(一般指磁盘存储),由于内节点(非叶子节点)不存储 data，所以一个节点可以存储更多的内节点，每个节点能索引的范围更大更精确。也就是说使用 B+ 树单次磁盘 IO 的信息量相比较 B 树更大，IO 效率更高。
（2）MySQL 是关系型数据库，经常会按照区间来访问某个索引列，B+ 树的叶子节点间按顺序建立了链指针，加强了区间访问性，所以B+树对索引列上的区间范围查询很友好。而 B 树每个节点的key和data在一起，无法进行区间查找。

官方文档

菜鸟教程
视频
书籍

https://dev.mysql.com/doc/refman/5.7/en/innodb-storage-engine.html

25-MySQL数据库多实例的多种配置方案介绍
同一台主机，3306 3307端口都用

docker

```shell
docker run -p 3306:3306 --name mysql --restart=always --privileged=true -v /usr/local/mysql/log:/var/log/mysql -v /usr/local/mysql/data:/var/lib/mysql -v /usr/local/mysql/conf:/etc/mysql -v /etc/localtime:/etc/localtime:ro -e MYSQL_ROOT_PASSWORD=123456 -d mysql:latest
```

`docker run -p 3306:3306 --name mysql -e MYSQL_ROOT_PASSWORD=123456 -d mysql:latest`

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

dbeaver可以格式化sql

## 源码的文件

深入理解MySQL核心技术
对源码的文件对应的功能有讲解
分模块

SELECT
    p1.name,
    p1.sex,
    p2.name,
    p2.sex,
    p1.species
FROM
    pet AS p1
INNER JOIN pet AS p2 ON
    p1.species = p2.species
    AND p1.sex = 'f'
    AND p1.death IS NULL
    AND p2.sex = 'm'
    AND p2.death IS NULL;

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

innodb_support_xa   1
min_examined_row_limit  0

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
`mysql>ALTER TABLE `table_name `ADD INDEX index_name (`column ` )`

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
4，添加索引

ALTER TABLE table_name ADD INDEX index_name (column_list)
ALTER TABLE table_name ADD UNIQUE (column_list)
ALTER TABLE table_name ADD PRIMARY KEY (column_list)

refence：https://blog.csdn.net/sddh1988/article/details/78611949

refence：https://blog.csdn.net/sddh1988/article/details/78611949

https://blog.csdn.net/sddh1988/article/details/78611949

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
屹通：
5.7.25-TiDB-v4.0.16

[MySQL内核源码解读-SQL解析之解析器浅析](https://blog.51cto.com/wangwei007/2300959)

先登录mysql数据库
mysql -u root
进入到mysql的目录下载进行操作
use mysql
select host, user from user;

[MySQL内核源码解读-SQL解析之解析器浅析](https://blog.51cto.com/wangwei007/2300959)

SQL规范与性能优化
1.2.1、先提前声明，博主工作用到是MySQL，可能有些场景只针对MySQL。说到SQL优化，一些概念必须要理解，不然死记硬背一两天就忘记了。特别是执行计划的概念。
1.2.2、什么是执行计划：
a.决定如何访问表数据，是否通过索引，是否排序等。
b.多表关联是先访问哪个表。
c.多表关联时，使用哪种连接方式，不过现在MySQL只有嵌套连接（嵌套循环，顾名思义就是将一个表为出发点，将该表全部记录逐条去遍历另外一张表的记录）。
1.2.3、SQL执行顺序：
a.检查语法是否正确。
b.检查表是否存在、权限是否满足等。
c.根据统计信息(如data length,rows,index length、索引唯一度)，生成较优的执行计划。
d.根据执行计划，进行数据检索、过滤、合并、排序等操作。访问数据时，内存中如存在表数据，则直接进行操作；否则，从磁带读取表数据，放入内存，再进行操作；如内存不足，则内存中较冷数据涮出内存，再从内存中读取数据。
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
1.2.9、最后一点，如何看执行计划，分析SQL的性能。这个吧，三言两语说不清楚，直接看其他博主的博文吧：[mysql explain执行计划详解](https://link.zhihu.com/?target=http%3A//www.cnblogs.com/xiaoboluo768/p/5400990.html)。

[启用mysql的sql日志](https://blog.csdn.net/aochijing0046/article/details/101493526)

[如何在MySql中记录SQL日志](https://www.cnblogs.com/liuliu/archive/2009/09/04/1560327.html)

如何在MySql中记录SQL日志（例如Sql Server Profiler)
https://www.cnblogs.com/liuliu/archive/2009/09/04/1560327.html

在mysql命令行或者客户端管理工具中执行：SHOW VARIABLES LIKE "general_log%";

结果：
general_log 0
general_log_file    /usr/local/mysql/data/localhost.log

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
MySQL日志查看详解
https://www.cnblogs.com/mungerz/p/10442791.html

show variables like 'general_log_file';
查看本地日志路径

show variables like 'slow_query_log_file';

/usr/local/mysql/data/localhost-slow.log

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

登录mysql后
select version() from dual;
centos 7
mysql -V

mysql 命令行
`status;`
`select version();`
