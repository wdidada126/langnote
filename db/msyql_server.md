# mysql server

https://www.yisu.com/zixun/4014.html

MySQL 事务 做实验
https://www.runoob.com/mysql/mysql-transaction.html


mysql server 查看事务历史记录


事务事件

查看正在执行的事务
`select * from information_schema.innodb_trx;`

mysql客户端连接池 java库 druid可以查看java程序发起的事务记录吗？
MYSQL的事务开始前先关闭AUTOCOMMIT

https://blog.51cto.com/wujianwei/2470974 重点 ，需要做实验
虽然我们可以通过查询慢查询日志查询到一条语句的执行总时长，但是如果数据库中存在一些大事务在执行过程中回滚了，，或者在执行过程中异常终止了，这个时候慢查询日志中是不会记录的，这时需要借助
performance_schema的 eventstransactions—的表来查看与事务相关的记录，在这些表中详细记录了是否有事务被回滚，活跃（长时间未提交的事务也属于活跃事务）活已提交等信息。

```sql
use performance_schema;
select * from setup_instruments where name like '%transaction%' limit 0,1;
```

没有结果，不对，是不是该文章版本号不对





mysql bin log
有可执行工具 binlog文件

mysql查看执行的sql历史记录
SELECT * from mysql.general_log ORDER BY event_time DESC;
query
init db两种


从MySQL5.1.6版开始，general query log和slow query log开始支持写到文件或者数据库表两种方式。


https://blog.51cto.com/net881004/2087130
更改my.cnf配置文件

vi /usr/local/kkmail/config/mysql/my.cnf
将下面注释取消掉，然后重启mysql
#general_log = 1

方式一：更改my.cnf配置文件
grep general_log /etc/my.cnf
general_log = 1
general_log_file = /tmp/general.log
重新启动mysql，这个操作相当于是永久生效。
当然这种方式是不允许在生产上采用的。因为要重启mysql，会中断mysql的业务。同时general.log会记录所有的关于mysql的DDL和DML语句，非常消耗资源，一般都是在协助排除mysql故障时，临时短暂的开启几分钟。事后都要关闭的。




https://www.cnblogs.com/liurong07/p/12919427.html


mysql查看执行sql语句的记录日志
1、使用processlist，但是有个弊端，就是只能查看正在执行的sql语句，对应历史记录，查看不到。好处是不用设置，不会保存。
-- use information_schema;
-- show processlist;
或者：
-- select * from information_schema.`PROCESSLIST` where info is not null;
2、开启日志模式
-- 1、设置
-- SET GLOBAL log_output = 'TABLE';SET GLOBAL general_log = 'ON';  //日志开启
-- SET GLOBAL log_output = 'TABLE'; SET GLOBAL general_log = 'OFF';  //日志关闭
-- 2、查询
SELECT * from mysql.general_log ORDER BY event_time DESC;
-- 3、清空表（delete对于这个表，不允许使用，只能用truncate）
-- truncate table mysql.general_log;
在查询sql语句之后，在对应的  C:\Program Files\MySQL\MySQL Server 5.7\data   文件夹下面有对应的log记录
ps:在查询到所需要的记录之后，应尽快关闭日志模式，占用磁盘空间比较大

https://www.cnblogs.com/gavinwu-blog/p/13565460.html

