# Effective MySQL之SQL语句最优化

https://zh.zlibrary-east.se/book/12156500/538abe

https://book.douban.com/subject/20438822/

作者: (美) 布拉德福(Bradford，R.)
ISBN: 9787302304296
出版年: 2013-1

https://effectivemysql.com/book/optimizing-sql-statements/

随书代码
https://github.com/effectiveMySQL/OptimizingSQLStatements/

《Effective MySQL之SQL语句最优化》是由MySQL专家Ronald Bradford撰著，书
中提供了很多可以用于改进数据库和应用程序性能的最佳实践技巧，并对这些技巧
做了详细的解释。本书希望能够通过一步步详细介绍SQL优化的方法，帮助读者分
析和调优有问题的SQL语句。
主要内容
●　找出收集和诊断问题必备的分析命令
●　创建MySQL索引来改进查询性能
●　掌握MySQL的查询执行计划
●　找出影响查询执行和性能的关键配置变量
●　用SQL语句优化的生命周期来识别、确
认、分析然后优化SQL语句，并检查优化的结果
●　学习使用不为常人所知的一些性能技巧
来改进索引效率并简化SQL语句

Ronald Bradford是一位在关系型数据库领域拥有20多年丰富经验的专家。他拥有深厚的专业背景以及10年以上Ingres和Oracle系统的工作知识，在过去12年中他致力于MySQL——世界上最流行的开源数据库的发展。他曾在2009年被提名为MySQL社区成员和2010年的Oracle ACE Director，其咨询领域的专家背景以及多次在国际会议上的发言也为他赢得了广泛的国际知名度。他还是Planet MySQL(2010)最受欢迎的个人MySQL技术博客作者，并且是清华大学出版社引进并出版的《PHP+MySQL专家编程》一书的作者之一。

MySQL在被Oracle公司收购之后成为主要的数据库解决方案，并获得了更多社区推广的机会。Ronald是世界范围的Oracle用户组中最受欢迎的MySQL的受邀发言人，该用户组的范围遍及北美、南美、欧洲以及亚太地区。

## 第1章 DBA五分钟速成

## 第2章 基本的分析命令
2.1 EXPLAIN命令 12
2.1.1 EXPLAIN PARTITIONS命令 14
2.1.2 EXPLAIN EXTENDED命令 15
2.2 SHOW CREATE TABLE命令 16
2.3 SHOW INDEXES命令 18
2.4 SHOW TABLE STATUS命令 19
2.5 SHOW STATUS命令 22
2.6 SHOW VARIABLES命令 25
2.7 INFORMATION_SCHEMA 26


SHOW CREATE TABLE xxxTableName

## 第3章 深入理解MySQL的索引

https://github.com/effectiveMySQL/OptimizingSQLStatements/blob/master/sql/chapter01.sql

## 第4章 创建MySQL索引

尽管EXPLAIN命令不会执行SQL语句，但当执行计划确定时它会执行FROM语句中的子查询。

QEP

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

通过一个叫`EXPLAIN`的SQL语句,我们可以查看MySQL的执行计划,了解它的QEP。

例如:

```sql
EXPLAIN SELECT * FROM users WHERE id = 1;
```

EXPLAIN会返回QEP相关信息,从中我们可以分析出:

- MySQL将使用哪个索引
- 预计需要扫描的行数
- 访问类型等等

通过分析QEP,我们就能分析查询性能,进而优化查询。

## 第5章 创建更好的MySQL索引





## 第6章 MySQL配置选项



