# SQL

[自己实现一个SQL解析引擎](https://blog.csdn.net/kxjrzyk/article/details/79341657)

[SQL中Truncate的用法](https://www.cnblogs.com/zhoufangcheng04050227/p/7991759.html)

DQL、DML、DDL、DCL、TCL和MySQL的部分DAL
<<<<<<< HEAD



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
=======
>>>>>>> a37e32040eec40d601569c731c313a398efb2dec
