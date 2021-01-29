# w3c sql


https://www.w3school.com.cn/sql/sql_distinct.asp

select distinct a,b,c from tableA;
注意此时是将a,b,c三列所有不同的组合全部列出来，而不仅仅只是distinct a

实验


首先我们明确一点，DISTINCT 用在所有的检测列之前，并且 它是作用于 所有列，不能部分使用
也就是类似
SELECT  id ,DISTINCT  corporation    
1
这种方式是错误的，那么 在使用 distinct 时候，我们可以把它后面的 所有参数当成一个 也就是 DISTINCT (id,corporation) ，即只有 （id,corporation ）这个组合的数据都相同时候，才会被“去重”，否则 还是会保留。



[distinct 多列 的 用法理解](https://blog.csdn.net/weixin_38656890/article/details/81477290)

https://www.cnblogs.com/wuyun-blog/p/6164618.html
[mysql实现distinct限制一列而查多列的方法](https://blog.csdn.net/liuxiao723846/article/details/79181857)
https://www.cnblogs.com/wuyun-blog/p/6164618.html

WHERE 子句中使用的运算符

BETWEEN 日期 数据
LIKE	字符串

!=
<>
SQL 使用单引号来环绕文本值（大部分数据库系统也接受双引号）。如果是数值，请不要使用引号。


文本值：
这是正确的：
SELECT * FROM Persons WHERE FirstName='Bush'
这是错误的：
SELECT * FROM Persons WHERE FirstName=Bush
数值：
这是正确的：
SELECT * FROM Persons WHERE Year>1965
这是错误的：
SELECT * FROM Persons WHERE Year>'1965'

where and or
结合AND和OR运算符
and > or
可以使用or来改变结合性


ORDER BY 语句默认按照升序对记录进行排序。
字典升序
字符
数字
日期呢？从远到近

order by 多个字段

ORDER BY Company DESC, OrderNumber ASC
ORDER BY Company DESC, OrderNumber  OrderNumber随机的？

insert
批量插入，括号，中间用，隔开
INSERT INTO Persons (LastName, Address) VALUES ('Wilson', 'Champs-Elysees')

insert into persons 
(id_p, lastname , firstName, city ) values (200,'haha' , 'deng' , 'shenzhen'),(201,'haha2' , 'deng' , 'GD'),(202,'haha3' , 'deng' , 'Beijing');

update语法
UPDATE 表名称 SET 列名称 = 新值 WHERE 列名称 = 某值
WHERE可以省略的

DELETE FROM 表名称 WHERE 列名称 = 值

DELETE FROM table_name
DELETE * FROM table_name


select like
MySQL 与 [charlist]% 通配符
https://www.cnblogs.com/cherrysu/p/8023371.html

regexp binary
rlike

select like 通配符有四个，不是% _两个，扩充知识面了
字符列中的任何单一字符
不在字符列中的任何单一字符

sql where
in
between 字符可以between


Mysql5.7版本中数据表字段可用的类型
bigint，binary，bit，blob，char，date，datetime，decimal，double，enum，float，geometry，geometrycollection，int，integer，json，linestring，longblob，longtext，mediumblob，mediumint，mediumtext，multilinestring，multipoint，multipolygon，numeric，point，polygon，real，set，smallint，text，time，timestamp，tinyblob，tinyint，tibytext，varbinary，varchar，year。
https://www.cnblogs.com/wangcp-2014/p/12144547.html


数字类型
日期 
字符串
BLOB是字符串

Json数据类型
自从Mysql5.7.8之后添加的一种类型，可以存储{“k1”: “val”, “k2”: 110}形式的数据。


不同日期

1.顾名思义，date只表示'YYYY-MM-DD'形式的日期，datetime表示'YYYY-MM-DD HH:mm:ss'形式的日期加时间，timestamp与datetime显示形式一样。
2.date和datetime可表示的时间范围为'1000-01-01'到'9999-12-31'，timestamp由于受32位int型的限制，能表示'1970-01-01 00:00:01'到'2038-01-19 03:14:07'的UTC时间。
3.mysql在存储timestamp类型时会将时间转为UTC时间，然后读取的时候再恢复成当前时区。 假如你存储了一个timestamp类型的值之后，修改了mysql的时区，当你再读取这个值时就会得到一个错误的时间。而这种情况在date和datetime中不会发生。
4.timestamp类型提供了自动更新的功能，你只需要将它的默认值设置为CURRENT_TIMESTAMP。
5.除了date是保留到天，datetime和timestamp都保留到秒，而忽略毫秒。
timestamp有时区的区别，timestamp自动更新 （设置默认值

https://www.cnblogs.com/371610785qq/p/7670218.html



SQL Alias
table_name AS alias_name
as可以省略？MySQL 5.7 windows版本可以
测试实验如下

```
mysql> select * from test_update as t where t.id = 888;
+-----+------+
| id  | name |
+-----+------+
| 888 | 12   |
+-----+------+
1 row in set (0.01 sec)

mysql> select * from test_update t where t.id = 888;
+-----+------+
| id  | name |
+-----+------+
| 888 | 12   |
+-----+------+
1 row in set (0.02 sec)

mysql> select t.id,t.name from test_update t where t.id = 888;
+-----+------+
| id  | name |
+-----+------+
| 888 | 12   |
+-----+------+
1 row in set (0.02 sec)

mysql> select t.id,t.name Name from test_update t where t.id = 888;
+-----+------+
| id  | Name |
+-----+------+
| 888 | 12   |
+-----+------+
1 row in set (0.02 sec)

mysql> select t.id,t.name as Name from test_update t where t.id = 888;
+-----+------+
| id  | Name |
+-----+------+
| 888 | 12   |
+-----+------+
1 row in set (0.03 sec)

mysql> select t.id,t.name as Name from test_update as t where t.id = 888;
+-----+------+
| id  | Name |
+-----+------+
| 888 | 12   |
+-----+------+
1 row in set (0.03 sec)
```

join
引用多个表
```sql
FROM Persons, Orders
WHERE Persons.Id_P = Orders.Id_P 
```

INNER JOIN（内连接）
JOIN: 如果表中有至少一个匹配，则返回行
LEFT JOIN: 即使右表中没有匹配，也从左表返回所有的行
RIGHT JOIN: 即使左表中没有匹配，也从右表返回所有的行
FULL JOIN: 只要其中一个表中存在匹配，就返回行


左外连接、右外连接、内连接、全连接
没有外连接
外连接分为做外连接 右外连接


sql中的join和inner join的区别
没区别

join 升级union
UNION 内部的 SELECT 语句必须拥有相同数量的列。列也必须拥有相似的数据类型。同时，每条 SELECT 语句中的列的顺序必须相同。
union/union all
如果允许重复的值，请使用 UNION ALL。

FIRST(OrderPrice) 作用在列上

