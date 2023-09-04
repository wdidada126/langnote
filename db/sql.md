# SQL

常见的SQL面试题：经典50题 - 知乎 https://zhuanlan.zhihu.com/p/38354000 SQL面试必会50题 - 知乎 https://zhuanlan.zhihu.com/p/43289968
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

[某音春招数据分析岗真题详解](https://www.zhihu.com/column/c_1352655958959734784)

题目（1）有用户表行为记录表t_act_records表，包含两个字段：uid（用户ID），imp_date（日期）1. 计算2020年每个月，每个用户连续签到的最多天数2. 计算2020年每个月，连续2天都有登陆的用户名单3. 计算2020年每个月，连续5天都有登陆的用户数难度：★★★★★<1> 计算2020年每个月，每个用户连续签到的最多天数考点：1. 连续时间问题；2. 时间限定；3. 聚类第一步：从时间上限定出2020年数据where imp_date between 20200101 and 20201231第二步：解决连续时间问题排序：row_number() over (partition by month(imp_date), uid) as rank 相减：date_diff(imp_date, rank) as sign 第三步：按月聚类求出最大连续签到天数组装构成答案

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
select month(imp_date) as month
    ,uid
from ( 
        select uid
            ,imp_date
            ,date_sub(imp_date, rank) as diff
        from(
                select uid
                    ,imp_date
                    ,row_number() over (partition by month(imp_date), uid) as rank 
                from t_act_records
                where imp_date between 20200101 and 20201231
            )
    )
group by month(imp_date)
    ,uid
having count(diff)>=2;
```

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


SQL92
SQL99
03

sqlzoo sql练习网站



```sql
mysql> select * from 't_blog' limit 1;
1064 - You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near ''t_blog' limit 1' at line 1
mysql> select * from "t_blog" limit 1;
1064 - You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '"t_blog" limit 1' at line 1
```



SQL注释

/*

*/


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


