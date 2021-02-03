# mysql_optimize

查询的CPU消耗：or>in>union

mysql where in 优化建议

改为union

mybatis xml怎么写？
https://blog.csdn.net/nangeali/article/details/80767662


MySQL深入学习笔记及实战指南
http://www.notedeep.com/note/38/page/329


一、数据库设计
一般都使用 INNODB 存储引擎，除非读写比率 < 1%, 才考虑使用 MYISAM 存储引擎；其 他存储引擎请在 DBA 的建议下使用。
Stored procedure (包括存储过程，函数，触发器) 对于 MYSQL 来说还不是很成熟， 没有完善的出错记录处理，不建议使用。
UUID ()，USER () 这样的 MySQL INSIDE 函数对于复制来说是很危险的，会导致主备数据不一致，所以请不要使用。如果一定要使用 UUID 作为主键，让应用程序来产生。
不要使用外键约束，如果数据存在外键关系，请在程序层面实现。
采用 UTF8 编码。

视图？
语法
作用

https://learnku.com/articles/25116

阿里新零售数据库设计与实战 （升级版）
https://ctc.koogua.com/course/1208
百度云下载

菜鸟也能飞：SQL数据库实战专业教程（二）
https://developer.aliyun.com/article/135597


MySQL8.0实战(二) - 数据库设计
https://cloud.tencent.com/developer/article/1450563


项目实战：数据库设计精选视频课程-架构师必修课-肖海鹏-专题视频课程
https://blog.csdn.net/XiaoGong1688/article/details/83574283


【实战演练】数据库基本知识与原理系列02-数据库设计与开发的范式
https://zhuanlan.zhihu.com/p/104183969

项目实战：数据库设计精选视频课程-架构师课
https://edu.51cto.com/course/7127.html


阿里新零售数据库设计与实战 （升级版）
https://coding.imooc.com/class/353.html


MySQL8.0实战(二) - 数据库设计
https://juejin.cn/post/6844903873933475848


同一表中，所有 varchar 字段的长度加起来，不能大于 65535. 如果有这样的需求，请使用 TEXT/LONGTEXT 类型。

TINYTEXT	256 bytes	 
TEXT	65,535 bytes	~64kb               最大2147483647个字符
MEDIUMTEXT	 16,777,215 bytes	~16MB
LONGTEXT	4,294,967,295 bytes	~4GB        4294967295


-----------       + -------------------------------------
TINYTEXT      | 255（2 8 -1）个字节
TEXT          | 65,535（2 16 -1）个字节= 64个KiB
MEDIUMTEXT | 16,777,215（2 24 -1）字节= 16 MiB
LONGTEXT    | 4,294,967,295（2 32 -1）个字节= 4个GiB
需要注意的是数目将取决于字符编码。


https://cloud.tencent.com/developer/ask/26839
