# Effective MySQL之SQL语句最优化





https://book.douban.com/subject/20438822/






第1章 DBA五分钟速成

第2章 基本的分析命令
2.1 EXPLAIN命令 12
2.1.1 EXPLAIN PARTITIONS命令 14
2.1.2 EXPLAIN EXTENDED命令 15
2.2 SHOW CREATE TABLE命令 16
2.3 SHOW INDEXES命令 18
2.4 SHOW TABLE STATUS命令 19
2.5 SHOW STATUS命令 22
2.6 SHOW VARIABLES命令 25
2.7 INFORMATION_SCHEMA 26




第3章 深入理解MySQL的索引


第4章 创建MySQL索引

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



第5章 创建更好的MySQL索引





第6章 MySQL配置选项



