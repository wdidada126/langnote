# sqlplus


```cmd
set ORACLE_SID=ORCL
set ORACLE_SID=TEST
D:\Oracle\DataBase\app\edidada\product\12.1.0\dbhome_1\BIN\sqlplus.exe
```


用户名 sys as sysdba
密码5Edidada

用户名MYSHOP
密码5Edidada

ORA-12560: TNS: 协议适配器错误

http://blog.itpub.net/29785807/viewspace-2122348/



Windows Oracle注册表

SID 是ORCL



oracle默认数据库是orcl





sqlplus username/password as sysdba;



##### sqlplus 执行sql语句

1 select * from all_tables where owner = 'TEST';


2 desc all_tables;

查看当前用户下的所有表名称
3 select table_name from all_tables where owner = 'MYSHOP' ;


4 select * from user_tables;


5




Oracle中查看所有的表，用户表，列名，主键，外键
在Oracle中查看所有的表: 
select * from tab/dba_tables/dba_objects/cat; 
看用户建立的表 :  
select table_name from user_tables;  //当前用户的表 
select table_name from all_tables;  //所有用户的表 
select table_name from dba_tables;  //包括系统表 
select * from user_indexes //可以查询出所有的用户表索引

查所有用户的表在all_tables 
主键名称、外键在all_constraints 
索引在all_indexes 
但主键也会成为索引，所以主键也会在all_indexes里面。 
具体需要的字段可以DESC下这几个view，dba登陆的话可以把all换成dba

1、查找表的所有索引（包括索引名，类型，构成列）：
select t.*,i.index_type from user_ind_columns t,user_indexes i where t.index_name = i.index_name and t.table_name = i.table_name and t.table_name = 要查询的表
2、查找表的主键（包括名称，构成列）：
select cu.* from user_cons_columns cu, user_constraints au where cu.constraint_name = au.constraint_name and au.constraint_type = 'P' and au.table_name = 要查询的表
3、查找表的唯一性约束（包括名称，构成列）：
select column_name from user_cons_columns cu, user_constraints au where cu.constraint_name = au.constraint_name and au.constraint_type = 'U' and au.table_name = 要查询的表
4、查找表的外键（包括名称，引用表的表名和对应的键名，下面是分成多步查询）：
select * from user_constraints c where c.constraint_type = 'R' and c.table_name = 要查询的表
查询外键约束的列名：
select * from user_cons_columns cl where cl.constraint_name = 外键名称
查询引用表的键的列名：
select * from user_cons_columns cl where cl.constraint_name = 外键引用表的键名
5、查询表的所有列及其属性
select t.*,c.COMMENTS from user_tab_columns t,user_col_comments c where t.table_name = c.table_name and t.column_name = c.column_name and t.table_name = 要查询的表
https://www.cnblogs.com/top5/archive/2010/04/09/1708212.html

