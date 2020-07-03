# MySQL技术内幕

https://book.douban.com/subject/24708143/

https://book.douban.com/subject/26436525/



[承尧](https://book.douban.com/search/姜承尧)

mysql 命令行工具使用



select now();

select now()\G

select now(),user(),version()\G

\G 竖直显示



## Chap. 7



c语言访问MySQL



## Chap. 10 MySQL管理简介



1、mysql 交互程序，向服务器发送SQL语句和查看结果

2、mysqladmin

3、mysqldump



## Chap. 11 MySQL数据目录



数据目录

cmake编译，指定-DMYSQL_DATADIR=dir_name

配置文件

[mysqld]

datadir=/path/to/data/directory

mysqld --verbose --help



mysql命令行下

SHOW VARIABLES LIKE 'datadir'；



mysqladmin variables

Unix域套接字 Unix

TCP/IP端口Unix/Windows

命名管道 Windows





.frm表格式描述信息

数据行和索引信息



视图和触发器在文件系统里面的表示

.frm视图

.trg触发器

alter table 时会更改frm文件



用mysqldump工具将各个数据库转储出来：

mysqldump --database db_name > db_name.sql







系统表空间

独立表空间



mysql允许的数据库名和表名的最大长度是64个字符

Unix大小写敏感，Windows mac 系统大小写不敏感（mac有其他分区对大小写敏感



mysql 表长度的限制





## Chap. 12

