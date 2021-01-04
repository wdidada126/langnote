# SQL必知必会

陈旸
清华大学计算机博士
前IBM中国研究院工程师。IEEE & ACM Member，中国人工智能协会成员，中国计算机协会CCF大数据专委。

专栏模块
专栏分为4大模块。
基础篇
以NBA球队球员数据和王者荣耀数据为案例基础，全面讲解SQL语言的基础语法知识，在实际操作中加深理解。
进阶篇
不同的SQL语句，为什么执行的效率就是不一样？本模块从实际出发，拆解日常工作中常见的SQL性能问题，教你写出高效率的SQL语句。
高级篇
SQL语言是关系型数据库管理系统（RDBMS）的通用语言。在工作中，我们就是通过各种各样的DBMS处理数据的。本模块将重点介绍使用频率较高的DBMS，带你了解SQL语言的使用场景和平台。
实战篇
从实战角度出发，将前几个模块的内容系统整合，讲解如何用SQL完成数据分析中具体的项目，比如数据清洗、数据集成等。





### 07 SQL函数

常用的 SQL 函数有哪些

- 算术函数
- 字符串函数
- 日期函数
- 转换函数





![算术函数](https://static001.geekbang.org/resource/image/19/e1/193b171970c90394576d3812a46dd8e1.png)





SELECT ABS(-2)，运行结果为 2。SELECT MOD(101,3)，运行结果 2。SELECT ROUND(37.25,1)，运行结果 37.3。



![顶顶顶](https://static001.geekbang.org/resource/image/c1/4d/c161033ebeeaa8eb2436742f0f818a4d.png)



SELECT CONCAT('abc', 123)，运行结果为 abc123。SELECT LENGTH('你好')，运行结果为 6。SELECT CHAR_LENGTH('你好')，运行结果为 2。SELECT LOWER('ABC')，运行结果为 abc。SELECT UPPER('abc')，运行结果 ABC。SELECT REPLACE('fabcd', 'abc', 123)，运行结果为 f123d。SELECT SUBSTRING('fabcd', 1,3)，运行结果为 fab。



![顶顶顶顶顶](https://static001.geekbang.org/resource/image/3d/45/3dec8d799b1363d38df34ed3fdd29045.png)





SELECT CURRENT_DATE()，运行结果为 2019-04-03。SELECT CURRENT_TIME()，运行结果为 21:26:34。SELECT CURRENT_TIMESTAMP()，运行结果为 2019-04-03 21:26:34。SELECT EXTRACT(YEAR FROM '2019-04-03')，运行结果为 2019。SELECT DATE('2019-04-01 12:00:05')，运行结果为 2019-04-01。





![顶顶顶](https://static001.geekbang.org/resource/image/5d/59/5d977d747ed1fddca3acaab33d29f459.png)



SELECT CAST(123.123 AS INT)，运行结果会报错。SELECT CAST(123.123 AS DECIMAL(8,2))，运行结果为 123.12。SELECT COALESCE(null,1,2)，运行结果为 1。








SQL必知必会 极客时间

https://time.geekbang.org/column/intro/100029501



不过在 SQL 中，你还是要确定大小写的规范，因为在 Linux 和 Windows 环境下，你可能会遇到不同的大小写问题。比如 MySQL 在 Linux 的环境下，数据库名、表名、变量名是严格区分大小写的，而字段名是忽略大小写的。而 MySQL 在 Windows 的环境下全部不区分大小写。



但是数据库名、表名和字段名在 Linux MySQL 环境下是区分大小写的



CONCAT()是字符串拼接函数，在 MySQL 和 Oracle 中都有这个函数，但是在这两个 DBMS 中作用却不一样，CONCAT函数在 MySQL 中可以连接多个字符串，而在 Oracle 中CONCAT函数只能连接两个字符串，如果要连接多个字符串就需要用（||）连字符来解决。



![ddd](https://static001.geekbang.org/resource/image/8c/c9/8c5e316b466e8fa65789a9c6a220ebc9.jpg)

### 08 SQL的聚集函数

聚集函数，它是对一组数据进行汇总的函数，输入的是一组数据的集合，输出的是单个值。通常我们可以利用聚集函数汇总表的数据，如果稍微复杂一些，我们还需要先对数据做筛选，然后再进行聚集，比如先按照某个条件进行分组，对分组条件进行筛选，然后得到筛选后的分组的汇总信息。



聚集函数都有哪些

![聚集函数列表](https://static001.geekbang.org/resource/image/d1/15/d101026459ffa96504ba3ebb85054415.png)



COUNT(role_assist)会忽略值为 NULL 的数据行，而 COUNT(*) 只是统计数据行数，不管某个字段是否为 NULL。

```sql
SELECT MAX(hp_max) FROM heros WHERE role_main = '射手' or role_assist = '射手';
SELECT COUNT(*), AVG(hp_max), MAX(mp_max), MIN(attack_max), SUM(defense_max) FROM heros WHERE role_main = '射手' or role_assist = '射手';
SELECT MIN(CONVERT(name USING gbk)), MAX(CONVERT(name USING gbk)) FROM heros;
```



HAVING 的作用和 WHERE 一样，都是起到过滤的作用，只不过 WHERE 是用于数据行，而 HAVING 则作用于分组。



你要记住，在 SELECT 查询中，关键字的顺序是不能颠倒的，它们的顺序是：

SELECT ... FROM ... WHERE ... GROUP BY ... HAVING ... ORDER BY ...limit



![dd](https://static001.geekbang.org/resource/image/3a/de/3aa2b0626f5cfc64b4a7175de938d1de.png)





### 09 子查询



子查询可以分为关联子查询和非关联子查询

```
SELECT player_name, height FROM player WHERE height = (SELECT max(height) FROM player);
```



![dddd	](https://static001.geekbang.org/resource/image/67/48/67dffabba0619fa4d311929c5d1c0f48.png)



### 10 SQL标准





LEFT JOIN 和 RIGHT JOIN 只存在于 SQL99 及以后的标准中，在 SQL92 中不存在，只能用（+）表示。

- 笛卡尔积
- 非等值连接
- 外连接
- 自连接
- 等值连接

笛卡尔乘积是一个数学运算。假设我有两个集合 X 和 Y，那么 X 和 Y 的笛卡尔积就是 X 和 Y 的所有可能组合，也就是第一个对象来自于 X，第二个对象来自于 Y 的所有可能。



### 12 视图
### 13 存储过程
### 14 事务处理





