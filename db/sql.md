# SQL


drop     删除表（包括表结构和数据
trunacte 无条件全部删除数据
delete   有条件的删除数据


[某音春招数据分析岗真题详解](https://www.zhihu.com/column/c_1352655958959734784)

题目（1）有用户表行为记录表t_act_records表，包含两个字段：uid（用户ID），imp_date（日期）1. 计算2020年每个月，每个用户连续签到的最多天数2. 计算2020年每个月，连续2天都有登陆的用户名单3. 计算2020年每个月，连续5天都有登陆的用户数难度：★★★★★<1> 计算2020年每个月，每个用户连续签到的最多天数考点：1. 连续时间问题；2. 时间限定；3. 聚类第一步：从时间上限定出2020年数据where imp_date between 20200101 and 20201231第二步：解决连续时间问题排序：row_number() over (partition by month(imp_date), uid) as rank 相减：date_diff(imp_date, rank) as sign 第三步：按月聚类求出最大连续签到天数组装构成答案select month
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

<2> 计算2020年每个月，连续2天都有登陆的用户名单考点：1. 连续时间问题；2. 时间限定；3. 聚类不同点：与上题考点相似，唯一不同点为要求连续两天都有登陆count(diff)>=2组装构成答案select month(imp_date) as month
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


sql子查询的例子
1、单行子查询
        select ename,deptno,sal
        from emp
        where deptno=(select deptno from dept where loc='NEW YORK')；
     2、多行子查询
        SELECT ename,job,sal
        FROM EMP
        WHERE deptno in ( SELECT deptno FROM dept WHERE dname LIKE 'A%')；
     3、多列子查询
        SELECT deptno,ename,job,sal
        FROM EMP
        WHERE (deptno,sal) IN (SELECT deptno,MAX(sal) FROM EMP GROUP BY deptno)；
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


