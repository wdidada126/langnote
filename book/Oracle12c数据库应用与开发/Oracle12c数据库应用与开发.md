# Oracle12c数据库应用与开发

12c
c是cloud的缩写

重点看第7章

https://book.douban.com/subject/30708610/

https://www.zhihu.com/pub/reader/119582341/chapter/1183442066088026112
中原学院 老师授课教材



源代码在此文件相同目录下
Oracle12c数据库应用与开发资源.zip



容器数据库
可插拔数据库

C## 开头

导入数据

sqlldr MYSHOP/5Edidada@192.168.1.158:1521/TEST control=C:\Users\edidada\Desktop\data\input_login.ctl log=C:\Users\edidada\Desktop\data\input_test.log bad=C:\Users\edidada\Desktop\data\input_test.bad


sqlldr MYSHOP/5Edidada@192.168.1.158:1521/TEST control=C:\Users\edidada\Desktop\data\input_course.ctl log=C:\Users\edidada\Desktop\data\input_test.log bad=C:\Users\edidada\Desktop\data\input_test.bad

sqlldr MYSHOP/5Edidada@192.168.1.158:1521/TEST control=C:\Users\edidada\Desktop\data\input_student.ctl log=C:\Users\edidada\Desktop\data\input_test.log bad=C:\Users\edidada\Desktop\data\input_test.bad

sqlldr MYSHOP/5Edidada@192.168.1.158:1521/TEST control=C:\Users\edidada\Desktop\data\input_sc.ctl log=C:\Users\edidada\Desktop\data\input_test.log bad=C:\Users\edidada\Desktop\data\input_test.bad



sqlldr icrm/icrm@18.20.20.20:1521/crmdb 
data = '/home/lee/dapai.dat'  #数据文件目录
bad = /home/lee/adpai.bad   #错误数据存放
control = /home/lee/adpai.ctl # 控制文件
direct = y  #这块需要特别注意，根据实际业务场景使用，不要随便使用
log = /home/lee/adpai.log    #日志文件
errors = 100000


是user，同一个数据库，不同的it项目访问，一个项目对应一个用户


表在scheme下面

user和scheme同名

## Chap. 1 Oracle 12c和云计算

ORAC（Oracle Real Application Cluster，Oracle 真正应用集群）

OASM（Oracle Automatic Storage Management，Oracle 自动存储管理）





ODI（Oracle 数据集成器）

OBDC（Oracle Big Data Connectors）

`SELECT con_id,dbid,name,open_mode FROM v$pdbs;`

## Chap. 2 CDB和PDB操作

1



## Chap. 3 Oracle 12c服务与SQLPlus

1



## Chap. 4 PL/SQL 语言基础

1



## Chap. 5 表空间 概要 用户 角色

1



## Chap. 6 数据表

1



## Chap. 7 数据查询

1



## Chap. 8 表的DML操作

1



## Chap. 9 视图 物化视图 物化视图日志

1



## Chap. 10 索引 聚簇 序列 同义词

1


## 跨年摘录（2020–2026 日常笔记聚合，2026-09-23 整理）

### 2022-11
> [315]何丹丹,王立娟,秦放.基于项目驱动的《Oracle数据库应用》教学改革探讨[J].价值工程,2014,33(10):235-236.DOI:10.14018/j.cnki.cn13-1085/n.2014.10.119.

