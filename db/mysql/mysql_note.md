# mysql

共享锁：select * from tableName where ... + lock in share more
排他锁：select * from tableName where ... + for update

执行计划，执行计划


MySQL提供explain/desc命令输出执行计划

问：MySQL数据库，desc如何查看执行计划

如何创建组合索引
语法：CREATE UNIQUE INDEX index ON table( col1, col2, col3 )
实例：CREATE UNIQUE INDEX index_unique ON app(pkgName,version,device,osver)


SQL中函数REPLACE()的用法及实例
https://blog.csdn.net/lanxingbudui/article/details/83854735
MySQL的replace方法
https://www.cnblogs.com/libin6505/p/10422910.html

MySQL执行计划
https://www.cnblogs.com/sunjingwu/p/10755823.html


SELECT CONNECTION_ID();


```shell
mysql> SELECT CONNECTION_ID();
+-----------------+
| CONNECTION_ID() |
+-----------------+
|           14709 |
+-----------------+
1 row in set (0.06 sec)

mysql> explain for connection 14709;
3012 - EXPLAIN FOR CONNECTION command is supported only for SELECT/UPDATE/INSERT/DELETE/REPLACE
```


mysql 锁表，锁行
https://www.cnblogs.com/itdragon/p/8194622.html

https://github.com/ITDragonBlog/daydayup

mysql optimization
https://dev.mysql.com/doc/refman/8.0/en/optimization.html
Query Execution Plan
https://dev.mysql.com/doc/refman/8.0/en/execution-plan-information.html

MySQL主键索引 层数
微信收藏


MySQL连接池 连接数有关


XA 
数据库

MySQL
命令行可以执行


show status

```
#!/bin/bash
while true
do
mysqladmin -uroot -p "密码" ext | awk 
'/Queries/{q=$4}/Threads_connected/{c=$4}/Threads_running/{r=$4}END{printf("%d %d %d\n",q,c,r)}' >> status.txt
sleep 
1
done
```

Converting HEAP to MyISAM
##### 查询结果太大时，把结果放到磁盘，严重
Create tmp table 
#创建临时表，严重
Copying to tmp table on disk  
#把内存临时表复制到磁盘，严重
locked 
#被其他查询锁住，严重
loggin slow query 
#记录慢查询
Sorting result #排序





