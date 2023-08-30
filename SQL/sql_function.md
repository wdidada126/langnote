# SQL



mybatis select resultMap resultType区别

map是别名
Type 结果集必须跟类中属性名称完全一样


sql中 count 
sum avg max min是不是函数？

group by才能使用的函数


聚合函数不能嵌套调用。比如不能出现类似“AVG(SUM(字段名称))”形式的调用。


使用GROUP BY关键字结合聚合函数将数据进行分组
聚合函数作用于一组数据，并对一组数据返回一个值。

MySQL提供了许多聚合函数，包括 AVG ， COUNT ， SUM ， MIN ， MAX 等。除 COUNT 函数外，其它聚合函数在执行计算时会忽略 NULL 值。
聚合函数是多对一函数。 它们使用来自多个记录的值作为输入，并将这些值转换为一个值来汇总所有记录。 Sum(), Count(), Avg(), Min(), 和Only() 都是聚合函数。

https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html
https://blog.51cto.com/xdr630/5104122

非法使用聚合函数 ： 不能在 WHERE 子句中使用聚合函数。


select veresion() from dual;
select now() from dual;

聚集函数
窗口函数



## function分类

windows function



aggrete function



select max(column_name) +1 aggregate from table;



学习sql

从数据的生命周期来看

先插入，可能同时往多个表插入数据



select 各种函数，各种跨表join



索引

索引类型

normal/unique

多列索引 复合索引

最左匹配



where and，optiname 执行计划，会根据索引来优化



索引方式

基本btree，不用hash？


## Oracle function
