# SQL必知必会

个人总结，


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

实际上，SQL-92 标准中已经对 3 种异常情况进行了定义，这些异常情况级别分别为脏读（Dirty Read）、不可重复读（Nonrepeatable Read）和幻读（Phantom Read）。
这四种隔离级别从低到高分别是：读未提交（READ UNCOMMITTED ）、读已提交（READ COMMITTED）、可重复读（REPEATABLE READ）和可串行化（SERIALIZABLE）。

使用MySQL客户端来模拟三种异常

![dddd	](https://static001.geekbang.org/resource/image/aa/fb/aa2ae6682a571676b686509623a2a7fb.jpg)
脏读
幻读
不可重复读

读未提价
读已提交
可重复读
序列化

### 16 游标


### 20丨当我们思考数据库调优的时候，都有哪些维度可以选择？

今天的课程你需要掌握以下几个方面的内容：数据库调优的目标是什么？如果要进行调优，都有哪些维度可以选择？如何思考和分析数据库调优这件事？数据库调优的目标简单来说，数据库调优的目的就是要让数据库运行得更快，也就是说响应的时间更快，吞吐量更大。
用户的反馈
日志分析
服务器资源使用监控
数据库内部状况监控


对数据库进行调优，都有哪些维度可以进行选择？
第一步，选择适合的 DBMS
第二步，优化表设计
第三步，优化逻辑查询
第四步，优化物理查询
第五步，使用 Redis 或 Memcached 作为缓存
第六步，库级优化




我们该如何思考和分析数据库调优这件事
首先，选择比努力更重要。
另外，你可以把 SQL 查询优化分成两个部分，逻辑查询优化和物理查询优化。
最后，我们可以通过外援来增强数据库的性能。
![房东](https://static001.geekbang.org/resource/image/d3/b0/d3bc10314c3532f053304a00765183b0.jpg）


### 21丨范式设计：数据表的范式有哪些，3NF指的是什么

今天的课程你需要掌握以下几个方面的内容：数据库的设计范式都有哪些？数据表的键都有哪些？1NF、2NF和3NF指的是什么？
目前关系型数据库一共有6种范式，按照范式级别，从低到高分别是：1NF（第一范式）、2NF（第二范式）、3NF（第三范式）、BCNF（巴斯-科德范式）、4NF（第四范式）和5NF（第五范式，又叫做完美范式）。

数据表中的那些键
https://static001.geekbang.org/resource/image/42/9b/4299e5030169710d5b1d29fd0729879b.jpg
从1NF到3NF
1NF指的是数据库表中的任何属性都是原子性的，不可再分。
2NF指的数据表里的非主属性都要和这个数据表的候选键有完全依赖关系。
3NF在满足2NF的同时，对任何非主属性都不传递依赖于候选键。

![房东](https://static001.geekbang.org/resource/image/e7/11/e775113e733020a7810196afd4f58711.jpg）

### 22丨反范式设计：3NF有什么不足，为什么有时候需要反范式设计

BCNF（巴斯范式）
https://static001.geekbang.org/resource/image/8b/17/8b543855d7c005b3e1b0ee3fbb308b17.png
BCNF，也叫做巴斯-科德范式，它在3NF的基础上消除了主属性对候选键的部分依赖或者传递依赖关系。
反范式设计

### 23丨索引的概览：用还是不用索引，这是一个问题

### 24丨索引的原理：我们为什么用B+树来做索引

b+树索引?
磁盘读取效率低
b+树只有叶子节点存储数据

### 25丨Hash索引的底层原理是什么

### 26丨索引的使用原则：如何通过索引让SQL查询效率最大化

### 27丨从数据页的角度理解B+树查询

### 28丨从磁盘I/O的角度理解SQL查询的成本

### 29丨为什么没有理想的索引
