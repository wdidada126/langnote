# NaiveDB

https://www.writebug.com/git/goodwill/NaiveDB.git
NaiveDB是一个关系数据库管理系统，采用客户端/服务器架构。主要分为存储模块、查询模块、元数据管理模块、事务模块(https://www.writebug.com/git/goodwill/NaiveDB)
NaiveDB:清华软院大三下《数据库原理》大作业

sql解析
.g4

没有实现MVCC
有实现x锁，s锁

.log数据存文件的

MYDB实现了MVCC

https://github.com/edidada/mydb

java面试指北

https://github.com/CN-GuoZiyang/MYDB

mvcc读更新场景，读的是上一个版本的数据，如果没有上一个版本的数据，等待

当前读，快照读

补充，单条数据，读写删除 三个都有的场景

整个表，读写更新
