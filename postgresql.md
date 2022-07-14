# postgresql

### pg scheme
pg数据库下面有模式(scheme)，模式下面有表

[PostgreSQL 在国内公司应用](https://www.zhihu.com/question/19685185)

Greenplum开源
Massively Parallel Postgres for Analytics
Experience Greenplum Database, an open-source massively parallel data platform for analytics, machine learning and AI 



支持存储过程debug



sp（存储过程的作用

编程，避免大量的sql中间数据在网络上传输





### windows 10 安装版本

PostgreSQL 10.8
[PostgreSQL查看版本信息](https://blog.csdn.net/kmblack1/article/details/78721653)

PostgreSQL 10.12 Documentation

https://www.postgresql.org/docs/10/index.html


卸载了，腾讯云安装







开发语言 c

sql解析 flex bison

source repo
https://github.com/postgres/postgres



maillist





centos 7安装


https://www.postgresql.org/download/linux/redhat/



postgresql权限管理，如何添加一个网段的ssl访问权限？
配置参考文档：https://www.jianshu.com/p/21d25c0d6ab4



180.167.0.0/16
PostgreSQL安装后默认只能localhost:5432访问


本机登录
su - postgres
qsql -U postgres ？？？



核心的登录命令
psql "postgresql://[用户名]:[密码]@[服务器地址]:[端口]/[数据库名称]"
示例：psql postgresql://postgres:123456@192.168.51.17:5432/database

https://www.jianshu.com/p/823702d6643e
psql -Upostgres -h 118.182.97.157 -p 5432 -d postgres
psql -Upostgres -h 118.182.97.157 sonarqube
CREATE DATABASE sonarqube;
\q

命令行方式登录PostgreSQL

配置文件
/var/lib/pgsql/10/data/pg_hba.conf

### pgsql 创建数据库
navicate图形界面创建数据库？ 登录，进命令行 CREATE DATABASE dbname;


PostgreSQL 创建数据库
https://www.runoob.com/postgresql/postgresql-create-database.html


PostgreSQL 数据库内核分析

https://book.douban.com/subject/6971366/





适合刚开始研读PG源代码的朋友

数据库执行计划用到了动态规划和图论等相关知识

开源数据库中，对空间地理数据支持比较好的要数PG的插件Postgi





Oracle ACE

第九届PostgreSQL中国技术大会

张文升
著有书籍《PostgreSQL实战》
《PostgreSQL指南：内幕探索》



/postgres# find . -name "*.y"
./contrib/cube/cubeparse.y
./contrib/seg/segparse.y
./src/test/isolation/specparse.y
./src/backend/replication/repl_gram.y
./src/backend/replication/syncrep_gram.y
./src/backend/utils/adt/jsonpath_gram.y
./src/backend/bootstrap/bootparse.y
./src/backend/parser/gram.y
./src/bin/pgbench/exprparse.y
./src/pl/plpgsql/src/pl_gram.y

