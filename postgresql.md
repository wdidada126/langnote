# postgresql

Posgres的MVCC实现牛逼不，牛。serial snapshot isolation是很强。
是的,PostgreSQL的MVCC(Multiversion Concurrency Control,多版本并发控制)实现确实非常强大和出色。其中的串行快照隔离(Serial Snapshot Isolation)是PostgreSQL MVCC的核心机制之一,是它支持高并发读写的关键所在。
具体来说,PostgreSQL的MVCC及串行快照隔离机制有以下几个优点:
1. 高并发性能
   - MVCC允许多个事务并发读取同一数据,而不会相互阻塞。这大大提升了数据库的并发处理能力。
   - 串行快照隔离确保每个事务看到的数据都是一致的,不会出现脏读、不可重复读等问题。
2. 事务隔离性
   - 串行快照隔离是最高级别的隔离级别,可以避免幻读等隔离问题。
   - 即使事务之间存在并发,也能保证事务的原子性和隔离性。
3. 快照一致性
   - MVCC机制会为每个事务维护一个数据快照,确保事务内部看到的数据是一致的。
   - 即使数据在事务执行过程中发生变更,事务内部也能看到一致的快照数据。
4. 数据库恢复
   - MVCC的快照机制有利于数据库的恢复和审计,可以轻松地实现点in时间恢复。
5. 低锁开销
   - MVCC不需要对数据行加锁即可实现并发控制,大大降低了锁的开销。

总的来说,PostgreSQL的MVCC及串行快照隔离机制是其数据库引擎的核心优势之一,确实是非常出色的并发控制技术。这也是PostgreSQL广受欢迎的重要原因之一。

好的,让我来详细介绍一下串行快照隔离(Serializable Snapshot Isolation,SSI)的论文和代码实现。

论文方面:

- 串行快照隔离最初由Michael Cahill等人在2008年发表于SIGMOD会议上的论文《Serializable Isolation for Snapshot Databases》中提出。
- 论文中提出了一种基于依赖图的SSI算法,可以在不牺牲并发性的情况下实现可串行化的事务隔离。
- 论文详细阐述了SSI的原理和实现细节,包括如何检测和解决可串行化冲突。

代码实现方面:

- PostgreSQL就是最著名采用SSI机制的数据库系统之一。
- PostgreSQL的SSI实现主要集中在以下几个模块:
  1. 事务管理模块:维护事务的快照信息和依赖关系。
  2. 锁管理模块:检测可串行化冲突并加锁。
  3. 查询执行模块:根据事务快照提供一致的数据视图。
  4. 恢复模块:支持基于SSI的数据库恢复。
- PostgreSQL的SSI实现在9.1版本中引入,并在之后的版本中不断完善和优化。
- 除了PostgreSQL,Oracle数据库和某些NoSQL数据库如FaunaDB也采用了类似的SSI机制。

总的来说,串行快照隔离是一种非常强大的并发控制技术,通过精心设计的算法和数据结构实现,确保了数据库事务的正确性和高并发性能。PostgreSQL在这方面的实现可以说是业界的标杆之一。

产品架构  Shared-Everything

https://zhuanlan.zhihu.com/p/656483356

德歌
https://github.com/digoal/blog

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


卸载了，中国电信云安装


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

在 PostgreSQL 10 中，要允许任何 IP 地址访问数据库，您需要进行以下配置更改：
1. 找到 PostgreSQL 的配置文件 `postgresql.conf`。在 Linux 上，该文件通常位于 `/etc/postgresql/10/main` 目录下；在 Windows 上，它通常位于 `C:\Program Files\PostgreSQL\10\data` 目录下。
2. 打开 `postgresql.conf` 文件，并找到以下配置项：

   ````conf
   #listen_addresses = 'localhost'    # 默认值为 'localhost'
   ```

   ````
2. 将 `listen_addresses` 的值修改为 `'*'`，以允许来自任何 IP 地址的连接：
   ````conf
   listen_addresses = '*'
   ```

   ````
3. 保存并关闭 `postgresql.conf` 文件。
4. 在 PostgreSQL 10 中，还需要修改 `pg_hba.conf` 文件来配置访问控制规则。找到并打开 `pg_hba.conf` 文件。
5. 在 `pg_hba.conf` 文件中，为允许任何 IP 地址访问数据库，请添加以下规则到文件的末尾：

   ````conf
   # 允许来自任何 IP 地址的连接
   host    all             all             0.0.0.0/0               md5
   ```

   这条规则允许任何 IP 地址以 `md5` 加密方式连接到任何数据库。

   ````
6. 保存并关闭 `pg_hba.conf` 文件。
7. 重新启动 PostgreSQL 服务器，以使配置更改生效。
请注意，允许任何 IP 地址访问数据库存在一定的安全风险。建议仅在开发或受信任的环境中使用此配置。在生产环境中，应该明确指定允许访问数据库的 IP 地址范围，并采取其他安全措施来保护数据库。

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
