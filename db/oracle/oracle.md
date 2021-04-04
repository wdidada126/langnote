# oracle


ui工具 oracle develop 自带的

自增 存储过程
int 没有 只有number
datetime -> date

Oracle 12C 创建用户以c##开头
https://blog.csdn.net/songpeiying/article/details/82894922


```sql
create table C##TEST01.Users(id  number(3) primary key,name varchar2(20),email varchar2(20),country varchar2(20),password varchar2(20));
INSERT INTO C##TEST01.Users (id, name, email, country, password) VALUES (1, 'Pankaj', 'pankaj@apple.com', 'India', 'pankaj123');
INSERT INTO C##TEST01.Users (id, name, email, country, password) VALUES (4, 'David', 'david@gmail.com', 'USA', 'david123');
INSERT INTO C##TEST01.Users (id, name, email, country, password) VALUES (5, 'Raman', 'raman@google.com', 'UK', 'raman123');
commit;
```



### book

- Oracle Database 12c完全参考手册  第7版.pdf

表navicate上
所有者
表空间


https://github.com/edidada/testoracle

lsnrctl status
tnsping orcl

D:\Oracle\DataBase\app\edidada\product\12.1.0\dbhome_1\NETWORK\ADMIN
路径下三个文件sqlnet.ora listener.ora tnsnames.ora


oracle数据库tns配置方法详解
https://www.jb51.net/article/44668.htm
TNS是Oracle Net的一部分，专门用来管理和配置Oracle数据库和客户端连接的一个工具，在大多数情况下客户端和数据库要通讯，必须配置TNS，当然在少数情况下，不用配置TNS也可以连接Oracle数据库，比如通过JDBC。如果通过TNS连接Oracle，那么客户端必须安装Oracle client程序。


使用tcp.validnode_checking允许、限制机器访问数据库
https://www.cnblogs.com/lcword/p/8232066.html

https://blog.csdn.net/demonson/article/details/39506215

tnsping 192.168.0.104
TNS Ping Utility for 64-bit Windows: Version 12.1.0.2.0 - Production on 02-4月 -2021 21:37:09
Copyright (c) 1997, 2014, Oracle.  All rights reserved.
已使用的参数文件:
D:\Oracle\DataBase\app\edidada\product\12.1.0\dbhome_1\network\admin\sqlnet.ora
已使用 EZCONNECT 适配器来解析别名
尝试连接 (DESCRIPTION=(CONNECT_DATA=(SERVICE_NAME=))(ADDRESS=(PROTOCOL=TCP)(HOST=192.168.0.104)(PORT=1521)))
TNS-12541: TNS: 无监听程序


windows 防火墙开放端口访问
https://blog.csdn.net/weixin_43465312/article/details/102510619


刚装的Oracle 12c  访问 https://localhost:5500/em/login 使用 system 登录 报错 （权限/口令错误）

右键计算机 ->管理 -> 服务 ，右击名称 输入O 弹出以O开头的服务名称 ,找到 OracleJobSchedulerORCL
启动它。 再登录就OK了。




https://localhost:5500/em



在环境变量中把ORACLE_HOME 设置成D:\Oracle\DataBase\app\edidada\product\12.1.0\dbhome_1

netstat -an



windows服务
OracleOraDB12Home2TNSListener


如何实现Oracle的监听（listener）多个IP地址
https://blog.csdn.net/funnyfu0101/article/details/51029674

oracle工具
oracle net namager


https://blog.csdn.net/weixin_29888579/article/details/114017404

Oracle Database Express Edition (XE) Release 18.4.0.0.0 (18c)
https://www.oracle.com/database/technologies/xe-downloads.html

Linux on System z (64-bit)
HP-UX ia64
IBM AIX power
Oracle Solaris (SPARC systems, 64-bit)
Linux x86-64
Microsoft Windows x64 (64-bit)

20191212 搞Oracle 12

jdbc:oracle:thin:@192.168.3.98:1521:orcl
jdbc:表示采用jdbc方式连接数据库
oracle:表示连接的是oracle数据库
thin:表示连接时采用thin模式(oracle中有两种模式)

jdbc:oralce:thin:是一个jni方式的命名

@表示地址
1521和orcl表示端口和数据库名

@192.168.3.98:1521:orcl整个是一块
也就是说是这样[jdbc]:[oracle]:[thin]:[@192.168.3.98:1521:orcl]

二、

oracle的jdbc连接方式:oci和thin

oci和thin是Oracle提供的两套Java访问Oracle数据库方式。
thin是一种瘦客户端的连接方式，即采用这种连接方式不需要安装oracle客户端,只要求classpath中包含jdbc驱动的jar包就行。thin就是纯粹用Java写的ORACLE数据库访问接口。
oci是一种胖客户端的连接方式，即采用这种连接方式需要安装oracle客户端。oci是Oracle Call Interface的首字母缩写，是ORACLE公司提供了访问接口，就是使用Java来调用本机的Oracle客户端，然后再访问数据库，优点是速度 快，但是需要安装和配置数据库。
https://www.cnblogs.com/qingxinblog/p/4043173.html


Oracle 服务名/实例名，Service_name 和Sid的区别


Service_name 和Sid的区别
Service_name：该参数是由oracle8i引进的。
在8i以前，使用SID来表示标识数据库的一个实例，但是在Oracle的并行环境中，一个数据库对应多个实例，这样就需要多个网络服务名，设置繁琐。为了方便并行环境中的设置，引进了Service_name参数，该参数对应一个数据库，而不是一个实例，而且该参数有许多其它的好处。



oracle 查看用户、权限、角色命令
https://blog.csdn.net/nature_fly088/article/details/8504823


https://blog.csdn.net/make_zhf/article/details/70154160


/oradata/TEST30/APPADMIN_TEMP_01.dbf

TEST_01.dbf
D:\Oracle\DataBase\app\edidada\oradata\orcl\


在Maven仓库中添加Oracle JDBC驱动
https://www.cnblogs.com/leiOOlei/p/3380568.html


cd/d D:\Oracle\DataBase\app\edidada\product\12.1.0\dbhome_1\jdbc\lib\
mvn install:install-file -DgroupId=com.oracle -DartifactId=ojdbc7 -Dversion=12.1.0.2.0 -Dpackaging=jar -DgeneratePom=true -Dfile=ojdbc7.jar
上述命令报错，在powershell中报错，在cmd中先运行cmd之后运行成功
https://stackoverflow.com/questions/6704813/maven-generating-pom-file/11199865#11199865

https://www.e-learn.cn/content/qita/2671944


https://www.oracle.com/database/technologies/jdbc-drivers-12c-downloads.html










oracle rac集群



https://blog.csdn.net/stevensxiao/article/details/90605443 sample是linux的，不是windows的

https://www.cndba.cn/dave/article/1985



navicate

用户角色

defalut

sysdba

sysoper

https://www.cnblogs.com/sunnyliu357/articles/2301738.html



Oracle RAC

https://docs.oracle.com/database/121/index.htm
https://www.oracletutorial.com/getting-started/oracle-sample-database/
https://www.cnblogs.com/lcword/p/8231860.html
navicate 连接oracle，是自动提交的
OCP/OCA认证考试指南全册:Oracle Database 11g
待正式从业后，再择机通过OCM认证提高自己。
OCA,OCP
现在基本上都是OCP，网上听课，然后线下就近考点考试即可，考试通过可以拿个证书，但是对于有工作经验的人来说好像价值已经不大了，现在ocm都漫天飞了。


在cmd中
C:\Documents and Settings\Administrator>sqlplus/nolog
SQL*Plus: Release 9.2.0.1.0 - Production on 星期四 11月 1 15:14:12 2007
Copyright (c) 1982, 2002, Oracle Corporation. All rightsreserved.
SQL> connect/as sysdba
已连接。

新版本都是云的    19

18

IBM Aix

HP Unix





12c
https://www.oracle.com/database/technologies/database12c-win64-downloads.html

关于oracle sql语句查询时表名和字段名要加双引号的问题
https://blog.csdn.net/u011754180/article/details/85097434

1、oracle表和字段是有大小写的区别。oracle默认是大写，如果我们用双引号括起来的就区分大小写，如果没有，系统会自动转成大写。

2、我们在使用navicat使用可视化创建数据库时候，navicat自动给我们加上了“”。






https://docs.oracle.com/database/121/TDDDG/tdddg_dml.htm#TDDDG99941

```SQL
INSERT INTO EMPLOYEES (
  EMPLOYEE_ID,
  FIRST_NAME,
  LAST_NAME,
  EMAIL,
  PHONE_NUMBER,
  HIRE_DATE,
  JOB_ID,
  SALARY,
  COMMISSION_PCT,
  MANAGER_ID,
  DEPARTMENT_ID
)
VALUES (
  10,              -- EMPLOYEE_ID
  'George',        -- FIRST_NAME
  'Gordon',        -- LAST_NAME
  'GGORDON',       -- EMAIL
  '650.506.2222',  -- PHONE_NUMBER
  '01-JAN-07',     -- HIRE_DATE
  'SA_REP',        -- JOB_ID
  9000,            -- SALARY
  .1,              -- COMMISSION_PCT
  148,             -- MANAGER_ID
  80               -- DEPARTMENT_ID
);

```


select username,created from dba_users where created>sysdate-1;


sqlplus system/5Edidada@127.0.0.1:1521/ORCL

sqlplus system/5Edidada@127.0.0.1:1521/ORCL @mksample.sql 5Edidada 5Edidada 5Edidada 5Edidada 5Edidada 5Edidada 5Edidada 5Edidada users temp C:\Users\edidada\Desktop\db-sample-schemas-12.1.0.2\log\ 127.0.0.1:1521/ORCL
sqlplus system/5Edidada@127.0.0.1:1521/ORCL@drop_hr.sql


https://docs.oracle.com/en/database/oracle/oracle-database/12.2/comsc/installing-sample-schemas.html#GUID-1E645D09-F91F-4BA6-A286-57C5EC66321D

https://github.com/oracle/db-sample-schemas/releases/tag/v12.1.0.2

https://www.linuxidc.com/Linux/2017-08/146337.htm

http://www.uwenku.com/question/p-ymnovpyv-ts.html

https://docs.oracle.com/database/121/TDDDG/tdddg_connecting.htm#TDDDG99998

https://docs.oracle.com/database/121/TDDDG/tdddg_dml.htm#TDDDG99941

https://docs.oracle.com/database/121/CNCPT/tablecls.htm#CNCPT010
https://docs.oracle.com/database/121/index.htm#

登录https://localhost:5500/em/shell#/dbhome/show_regions
输入用户名system，密码5Edidada，可以登录


?\demo\db-sample-schemas-12.1.0.2\log\hr_main.log
127.0.0.1:1521/ORCL
D:/Oracle/DataBase/app/edidada/product/12.1.0/dbhome_1/demo/db-sample-schemas-12.1.0.2/human_resources


https://www.jianshu.com/p/7530246fc34b


```
conn as sysdba;
sys 5Edidada
alter session set container=PDBORCL;
DROP USER hr cascade;
CREATE USER hr IDENTIFIED BY "5Edidada";
ALTER USER hr DEFAULT TABLESPACE users;
ALTER USER hr TEMPORARY TABLESPACE temp;
GRANT CREATE SESSION, CREATE VIEW, ALTER SESSION, CREATE SEQUENCE TO hr;
GRANT CREATE SYNONYM, CREATE DATABASE LINK, RESOURCE , UNLIMITED TABLESPACE TO hr;
GRANT execute ON sys.dbms_stats TO hr;


show con_name;
select con_id,dbid,NAME,OPEN_MODE from v$pdbs;



CREATE TABLE employees( employee_id NUMBER(6),first_name VARCHAR2(20),last_name VARCHAR2(25) CONSTRAINT emp_last_name_nn NOT NULL,email VARCHAR2(25),phone_number VARCHAR2(20),hire_date DATE CONSTRAINT emp_hire_date_nn NOT NULL,job_id VARCHAR2(10)	CONSTRAINT     emp_job_nn  NOT NULL    , salary         NUMBER(8,2)    , commission_pct NUMBER(2,2),manager_id NUMBER(6),department_id NUMBER(4),CONSTRAINT emp_salary_min CHECK(salary > 0),CONSTRAINT emp_email_uk UNIQUE(email));

CREATE UNIQUE INDEX emp_emp_id_pk ON employees (employee_id);

ALTER TABLE employeesADD(CONSTRAINTemp_emp_id_pk PRIMARY KEY(employee_id),CONSTRAINT emp_dept_fk FOREIGN KEY(department_id) REFERENCES departments,CONSTRAINT emp_job_fk FOREIGN KEY(job_id) REFERENCES jobs (job_id),CONSTRAINT emp_manager_fk FOREIGN KEY(manager_id) REFERENCES employees);

ALTER TABLE departments ADD ( CONSTRAINT dept_mgr_fk FOREIGN KEY (manager_id)REFERENCES employees (employee_id));

```

登录sqlplus之后，执行sql脚本
@?/demo/hr_create.sql



https://www.jb51.net/article/92720.htm



cmd输入

```
查看oracle的sid叫什么，比如创建数据库的时候，实例名叫“orcl”，那么先手工设置一下oralce的sid，cmd命令窗口中，set ORACLE_SID=orcl（还是大写？？
不然报错：ORA-01034: ORACLE not available ORA-27101


用sqlplus / as sysdba登陆oracle系统，这种登录方式来使用的是操作系统的验证方式，因此，无源需输入用户名和密码即可直接登录进去。

sqlplus sys/orcl as sysdba       //orcl是数据库

select USERNAME, USER_ID  from dba_users;//查看数据库用户 前提是你度是有dba权限的帐号，如sys,system；
```




SYSTEM

SYS

HR       hr用户是个示例用户，是在创建数据库时选中“示例数据库”后产生的，实际上就是模拟一个人力资源部的数据库。

OE

PM

IX

SH

BI



Oracle数据库中sys，system，scott，hr用户的区别
https://blog.csdn.net/zhang18330699274/article/details/55517836



###### sys和system的区别？

存储的数据的重要性不同。所有oracle的数据字典的基表和视图都存放在sys用户中，这些基表和视图对于oracle的运行是至关重要的，由数据库自己维护，任何用户都不能手动更改。sys用户拥有dba,sysdba,sysoper等角色或权限，是oracle权限最高的用户。

　　system用户用于存放次一级的内部数据，如oracle的一些特性或工具的管理信息。system用户拥有普通dba角色权限。





cdb pdb

Oracle 12C引入了CDB与PDB的新特性

cdb容器数据库 pdb可插播数据库 

https://blog.csdn.net/qq877507054/article/details/81209967






新建数据库 C##开头





oracle12c 启用容器数据库之后，创建用户名只能c#[#开头，那怎么才能不适用c#](http://tieba.baidu.com/hottopic/browse/hottopic?topic_id=0&topic_name=开头，那怎么才能不适用c)#开头的用户呢。
如果你去搜索的话，90%的答案会告诉你重新创建数据库实例，然后把创“建为容器数据库”勾选掉。

其实并不用那么麻烦，只需要几部就可以创建不带C##的用户。
1.使用sqlplus 以 DBA 身份链接。 命令：sqlplus / as sysdba
2.在链接成功后，通过命令查看存在的PDB服务。语句：show pdbs;
3.切换到pdb服务上。语句：
alter session set container=pdb服务名;
alter pluggable database pdb服务名 open;
4.尝试创建不带C##的用户吧。

###### Oracle 12C 创建用户以c##开头

https://blog.csdn.net/songpeiying/article/details/82894922

角色





https://zhuanlan.zhihu.com/p/59402726



创建非cdb数据库



打开Database Configuration Assistant

点击“下一步”出现如下界面，在创建数据库的时候将“创建为容器数据库”项取消勾选。

数据库名要大写

TEST202005

5Edidada



ORA-03113:通信通道的文件结尾 解决办法
https://blog.csdn.net/zwk626542417/article/details/39667999




重点

https://blog.csdn.net/wangsimiao118/article/details/78818836




orcl表示数据库名

[oracle连接两种方式thin与oci区别](https://blog.csdn.net/kevin_pso/article/details/54949476)
thin:表示知连接时采用thin模式道(oracle中有两中模式)
Java连接Oracle两种方式thin与oci区别
1 从使用上来说，oci必须在客户机上安装oracle客户端或才能连接，而thin就不需要，因此从使用上来讲thin还是更加方便，这也是thin比较常见的原因。 
2 原理上来看，thin是纯java实现tcp/ip的c/s通讯；而oci方式,客户端通过native java method调用c library访问服务端，而这个c library就是oci(oracle called interface)，因此这个oci总是需要随着oracle客户端安装（从oracle10.1.0开始，单独提供OCI Instant Client，不用再完整的安装client） 
3 它们分别是不同的驱动类别，oci是二类驱动， thin是四类驱动，但它们在功能上并无差异。 
4 虽然很多人说oci的速度快于thin，但找了半天没有找到相关的测试报告。



oracle 命令行创建标（也可以用工具创建

https://jingyan.baidu.com/article/948f5924de98add80ef5f952.html





service name 和sid区别

https://www.cnblogs.com/matd/p/11051884.html

service name 该参数的缺省值为Db_name. Db_domain，即等于Global_name。一个数据库可以对应多个Service_name，以便实现更灵活的配置。该参数与SID没有直接关系，即不必Service name 必须与SID一样。Sid是数据库实例的名字，每个实例各不相同。



```
sqlplus查看服务名
查看服务名：

show parameter service

查看实例名：

select * from v$instance;

 查看数据库名：

select name from v$database;

查看数据库用到几个表空间：

select distinct TABLESPACE_NAME from tabs；

```





Oracle 12c 用户密码过期设置的一些问题

https://blog.csdn.net/seagal890/article/details/82716798


https://blog.csdn.net/weixin_39921821/article/details/82720851
oracle11g ORA-01078与LRM-00109 解决方法（详细）
https://blog.csdn.net/qq_15904277/article/details/86521808


新建数据库 ORA-03113: 通信通道的文件结尾

D:\Oracle\DataBase\app\edidada\admin

数据库文件



```
CREATE USER "AAA" IDENTIFIED BY "5Edidada" DEFAULT TABLESPACE "USERS" TEMPORARY TABLESPACE "TEMP";

GRANT "DBA" TO "AAA" WITH ADMIN OPTION;

ALTER USER "AAA" DEFAULT ROLE "DBA";

ALTER USER "AAA" QUOTA UNLIMITED ON "USERS";

GRANT UNLIMITED TABLESPACE TO "AAA" WITH ADMIN OPTION


```





oracle跟mysql区别在哪儿？

https://www.cnblogs.com/ios9/p/8227574.html#_label0





https://blog.csdn.net/qq_41303486/article/details/104452529





ORA-01034: ORACLE not available

https://blog.csdn.net/qq_22498277/article/details/51621863





web管理台

https://localhost:5500/em/shell#/dbhome/show_regions

https://www.cnblogs.com/sunsiyuan/p/8485418.html





Oracle 12c视频教程

https://www.bilibili.com/video/BV1d54y197n3?p=10





管理工具



sqlplus     有自己的指令

isqlplus是网页版

navicate

pl/sql

oem 数据库的企业管理功能





oracle账户

本地管理员

在sqlplus上输入用户名system as sysdba         （只输入system不行

密码输入5Edidada

system/5Edidada as sysdba

本地管理员可以不输入密码



disconn 断开

conn     连接

网络用户登录

username/pwd





连接时没有指定数据库，默认连接orcl



连接指定是数据库



