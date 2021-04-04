# oracle_learn

c## 
table_name
两部分

create table c##.xxx 看得到
create table xxx  navicate工具看不到



Oracle的性能视图

windows E盘 

# README

```sql
CREATE TABLE "C##TEST01"."tb_user" ("ID" NUMBER(24,0) VISIBLE primary key,"user_name" VARCHAR2(255 BYTE) VISIBLE,"password" VARCHAR2(255 BYTE) VISIBLE,  "name" VARCHAR2(255 BYTE) VISIBLE,  "age" NUMBER(3,0) VISIBLE,  "sex" NUMBER(3,0) VISIBLE,  "birthday" DATE VISIBLE,  "created" DATE VISIBLE,  "updated" DATE VISIBLE);
INSERT INTO "C##TEST01"."tb_user" VALUES ('1', 'tom', 'da', 'dad', '1', '1', TO_DATE('2021-04-03 11:15:56', 'SYYYY-MM-DD HH24:MI:SS'), TO_DATE('2021-04-03 11:15:56', 'SYYYY-MM-DD HH24:MI:SS'), TO_DATE('2021-04-03 11:15:56', 'SYYYY-MM-DD HH24:MI:SS'));
INSERT INTO "C##TEST01"."tb_user" VALUES ('2', 'tom', 'da', 'dad', '1', '1', TO_DATE('2021-04-03 11:15:56', 'SYYYY-MM-DD HH24:MI:SS'), TO_DATE('2021-04-03 11:15:56', 'SYYYY-MM-DD HH24:MI:SS'), TO_DATE('2021-04-03 11:15:56', 'SYYYY-MM-DD HH24:MI:SS'));
INSERT INTO "C##TEST01"."tb_user" VALUES ('3', 'tom', 'da', 'dad', '1', '1', TO_DATE('2021-04-03 11:15:56', 'SYYYY-MM-DD HH24:MI:SS'), TO_DATE('2021-04-03 11:15:56', 'SYYYY-MM-DD HH24:MI:SS'), TO_DATE('2021-04-03 11:15:56', 'SYYYY-MM-DD HH24:MI:SS'));
commit;
```

```shell script
select * from C##TEST01.tb_user where id = 1;
select * from C##TEST01.tb_user where id = 1
                        *
第 1 行出现错误:
ORA-00942: 表或视图不存在
```

C##TEST01.tb_user
"C##TEST01"."tb_user"


[JDBC连接ORACLE的三种URL格式](https://blog.csdn.net/u012062455/article/details/52442838)


### The error may exist in UserMapper.xml
### The error may involve defaultParameterMap
### The error occurred while setting parameters
### SQL: select ID id,user_name userName from "C##TEST01"."tb_user" where id = ?
### Cause: java.sql.SQLSyntaxErrorException: ORA-00904: "USER_NAME": 标识符无效



select ID id,user_name userName from "C##TEST01"."tb_user" where id = 1;

oracle分页 失败


### The error occurred while setting parameters
### SQL: update "C##TEST01"."tb_user" tb          SET tb.name = ?          where tb.id = ?
### Cause: java.sql.SQLSyntaxErrorException: ORA-00904: "TB"."NAME": 标识符无效

https://www.linuxidc.com/Linux/2019-05/158743.htm

加引号


Exception in thread "main" org.apache.ibatis.exceptions.PersistenceException: 
### Error querying database.  Cause: org.apache.ibatis.executor.result.ResultMapException: Error attempting to get column 'AGE' from result set.  Cause: java.sql.SQLException: 无法转换为内部表示
### The error may exist in UserMapper.xml



### TODO
复杂跨表join查询
批量插入，批量删除
增删改查单元测试 内存数据库h2
集成测试


