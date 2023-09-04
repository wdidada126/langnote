# mysql

flex/bison与antlr的联系与区别

可执行程序
flex bison
anltr.bat

.l .y
.g4

c、c++代码嵌入.y文件，自定义头文件。各种内置函数
l y .a库

yyparse
localytext


listener visit模式
antlr-runtime 库

antlr flex/bison都可以实现计算器


### IDEA gateway

你和答主说的不是同一个东西 答主说的是新的gateway 你说的是deployment

unicoude云服务器错误，没有4G剩余空间

miniob ob数据库跟华中科技合作的数据库竞赛 使用了flex bison

mysql使用 .yy .ll

sql_yacc.yy
sql_hints.yy
MySQL内核源码解读-SQL解析一
https://blog.51cto.com/wangwei007/2300217

京东商城数据库技术部傅志宇
MySQL内核源码解读-SQL解析之解析器浅析
https://blog.51cto.com/wangwei007/2300959
京东商城数据库技术部郭光欣

编译原理 极客时间 宫

mvcc 多版本并发控制
java代码实现
https://blog.csdn.net/weixin_29132813/article/details/114537588

https://github.com/edidada/MYDB

yes的练级攻略

mysql 锁的
https://zhuanlan.zhihu.com/p/393683080


	CREATE TABLE `yes` (
	  `id` bigint(20) NOT NULL AUTO_INCREMENT,
	  `name` varchar(45) DEFAULT NULL,
	  `address` varchar(45) DEFAULT NULL,
	  PRIMARY KEY (`id`)
	) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4

查看事务隔离级别 mysql5.7.20 之后
show variables like 'transaction_isolation';
SELECT @@transaction_isolation;


mysql5.7.20 之后
SELECT @@tx_isolation;
show variables like 'tx_isolation';



https://blog.csdn.net/weixin_40964170/article/details/114958297

CREATE TABLE `yes`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `address` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

INSERT INTO `yes` VALUES (1, 'yes', 'hz');
INSERT INTO `yes` VALUES (2, 'xx', 'hz');
INSERT INTO `yes` VALUES (3, 'aa', 'd');

select * from yes where name = 'yes' for update;

select * from yes where name = 'xx' for update;

开启事务？

mysql 日志

redo log
undo log
bin log

又一个是存储改变之前的数据，改变之后的数据
区别如下： redo log 是InnoDB 引擎特有的；binlog 是MySQL 的Server 层实现的，所有引擎都可以使用。 redo log 是物理日志，记录的是“在某个数据页上做了什么修改”；binlog 是逻辑日志，记录的是这个语句的原始逻辑。
https://segmentfault.com/a/1190000023827696

[MySQL]源码角度看redo log
https://www.dazhuanlan.com/alaskawind/topics/1167481

自己实现innodb wal机制？
总的来说，MySQL中事务的原子性是通过 undo log 来实现的，事务的持久性性是通过 redo log 来实现的，事务的隔离性是通过读写锁+MVCC来实现的。

https://www.modb.pro/db/234350
http://catkang.github.io/2020/02/27/mysql-redo.html

实验课
https://gitee.com/edidada/naivedb
https://www.writebug.com/git/goodwill/NaiveDB
NaiveDB 是一个关系数据库管理系统，采用客户端/服务器架构。主要分为存储模块、查询模块、元数据管理模块、事务模块(https://www.writebug.com/git/goodwill/NaiveDB)


##### 事务模块

* 服务器支持多客户端并发
* 实现 begin transaction 和 commit。
* 使用二级锁协议，实现 read committed 隔离级别。
* 实现单一事务的 WAL 机制，可以读写 log 并恢复数据。
* 完善数据库存储模块与 bug 修改。

## MySQL中有7种日志文件
1. 重做日志（redo log）
2. 回滚日志（undo log)
3. 二进制日志（bin log）
4. 错误日志（error log）
5. 慢查询日志（slow query log）
6. 一般查询日志（general log）
7. 中继日志（relay log）

https://github.com/bingoohuang/blog/issues/137

redo日志文件名格式为 ib_logfile0或ib_logfile1

可使用find命令模糊查找

在Apache Ratis项目中，实现了一种更为高效的WAL机制

WAL会被删除吗
如果WAL内的transaction已经被成功apply到状态机里去了，就可以被删除掉了

[Rocksdb 的 WAL实现 底层探索](https://blog.csdn.net/Z_Stand/article/details/108025338)

update 一次更新多条数据，或者不是一条数据
根据主键来更新
方案1，先查询，只有一条再更新

mysql server日志，显示封锁

数据库4种隔离级别与3级封锁协议
MySQL事务提出了4个不同的隔离级别，而这些隔离级别的实现本质上就是通过加锁，解锁来实现的。
https://blog.csdn.net/weixin_44795128/article/details/119825139

lock in share mode
for update
说到共享锁和排他锁，就会想到悲观锁，这两个都属于数据库带的悲观锁，乐观锁不是数据库带的。

乐观锁：可以给表加一个version字段，先查询version字段放在缓存里，每次修改之前，在查询一次version字段，若跟缓存里的数值不一致，则回滚。

https://zhuanlan.zhihu.com/p/372090999

https://blog.csdn.net/gklifg/article/details/38752691

意向锁
对任何一个结点加锁时，必须先对它的上层结点加意向锁。

三种常用的意向锁：
1）意向共享锁（IS锁）：
对一个数据对象加IS锁，表示它的后裔结点拟（意向）加S锁。
事务T1对数据对象A加上IS锁后，事务T2可以继续加除X锁以外的锁。
2）意向排他锁（IX锁）：
对一个数据对象加IX锁，表示它的后裔结点拟（意向）加X锁。
事务T1对数据对象A加上IX锁后，事务T2只能继续加IS或IX锁。
3）共享意向排他锁（SIX = S+IX锁）：
对一个数据对象先加S锁，再加IX锁。例如对某个表加SIX锁，则表示该事务要读（S）整个表，同时会更新（IX
）个别元组。
https://blog.csdn.net/Ha1f_Awake/article/details/84994697

X > SIX > S / IX > IS


Mysql 插入意向锁
https://blog.csdn.net/u010648194/article/details/123659594


三、锁的分类。
数据库里有的锁有很多种，为了方面理解，所以我根据其相关性"人为"的对锁进行了一个分类，分别如下
基于锁的属性分类：共享锁、排他锁。
基于锁的粒度分类：表锁、行锁、记录锁、间隙锁、临键锁。
基于锁的状态分类：意向共享锁、意向排它锁。
1、属性锁
共享锁(Share Lock)
共享锁又称读锁，简称S锁；当一个事务为数据加上读锁之后，其他事务只能对该数据加读锁，而不能对数据加写锁，直到所有的读锁释放之后其他事务才能对其进行加持写锁。
共享锁的特性主要是为了支持并发的读取数据，读取数据的时候不支持修改，避免出现重复读的问题。
排他锁(eXclusive Lock)
排他锁又称写锁，简称X锁；当一个事务为数据加上写锁时，其他请求将不能再为数据加任何锁，直到该锁释放之后，其他事务才能对数据进行加锁。
排他锁的目的是在数据修改时候，不允许其他人同时修改，也不允许其他人读取。避免了出现脏数据和脏读的问题。
2、粒度锁
表锁
表锁是指上锁的时候锁住的是整个表，当下一个事务访问该表的时候，必须等前一个事务释放了锁才能进行对表进行访问；
特点： 粒度大，加锁简单，容易冲突；
行锁
行锁是指上锁的时候锁住的是表的某一行或多行记录，其他事务访问同一张表时，只有被锁住的记录不能访问，其他的记录可正常访问；
特点：粒度小，加锁比表锁麻烦，不容易冲突，相比表锁支持的并发要高；
记录锁(Record Lock)
记录锁也属于行锁中的一种，只不过记录锁的范围只是表中的某一条记录，记录锁是说事务在加锁后锁住的只是表的某一条记录。
触发条件：精准条件命中，并且命中的条件字段是唯一索引；
例如：update user_info set name=’张三’ where id=1 ,这里的id是唯一索引。
记录锁的作用：加了记录锁之后数据可以避免数据在查询的时候被修改的重复读问题，也避免了在修改的事务未提交前被其他事务读取的脏读问题。

间隙锁(Gap Lock)
间隙锁属于行锁中的一种，间隙锁是在事务加锁后其锁住的是表记录的某一个区间，当表的相邻ID之间出现空隙则会形成一个区间，遵循左开右闭原则。
比如下面的表里面的数据ID 为 1,4,5,7,10 ,那么会形成以下几个间隙区间，-n-1区间，1-4区间，7-10区间，10-n区间 (-n代表负无穷大，n代表正无穷大)
触发条件：范围查询并且查询未命中记录，查询条件必须命中索引、间隙锁只会出现在REPEATABLE_READ(重复读)的事务级别中。
例如：对应上图的表执行select * from user_info where id>1 and id<4(这里的id是唯一索引) ，这个SQL查询不到对应的记录，那么此时会使用间隙锁。
间隙锁作用：防止幻读问题，事务并发的时候，如果没有间隙锁，就会发生如下图的问题，在同一个事务里，A事务的两次查询出的结果会不一样。

临键锁(Next-Key Lock)
临键锁也属于行锁的一种，并且它是INNODB的行锁默认算法，总结来说它就是记录锁和间隙锁的组合，临键锁会把查询出来的记录锁住，同时也会把该范围查询内的所有间隙空间也会锁住，再之它会把相邻的下一个区间也会锁住。
例如：下面表的数据执行 select * from user_info where id>1 and id<=13 for update ;
会锁住ID为 1,5,10的记录；同时会锁住，1至5,5至10,10至15的区间。
触发条件：范围查询并命中，查询命中了索引。
临键锁的作用：结合记录锁和间隙锁的特性，临键锁避免了在范围查询时出现脏读、重复读、幻读问题。加了临键锁之后，在范围区间内数据不允许被修改和插入。

3、状态锁
状态锁包括意向共享锁和意向排它锁，把他们区分为状态锁的一个核心逻辑，是因为这两个锁都是都是描述是否可以对某一个表进行加表锁的状态。
意向锁的解释：当一个事务试图对整个表进行加锁(共享锁或排它锁)之前，首先需要获得对应类型的意向锁(意向共享锁或意向共享锁)
意向共享锁
当一个事务试图对整个表进行加共享锁之前，首先需要获得这个表的意向共享锁。
意向排他锁
当一个事务试图对整个表进行加排它锁之前，首先需要获得这个表的意向排它锁。
为什么我们需要意向锁？
意向锁光从概念上可能有点难理解，所以我们有必要从一个案例来分析其作用，这里首先我们先要有一个概念那就是innodb加锁的方式是基于索引，并且加锁粒度是行锁，然后我们来看下面的案例。

第一步：
事务A对user_info表执行一个SQL:update user_info set name =”张三” where id=6 加锁情况如下图;
第二步：
与此同时数据库又接收到事务B修改数据的请求：SQL: update user_info set name =”李四”；
1、因为事务B是对整个表进行修改操作，那么此SQL是需要对整个表进行加排它锁的(update加锁类型为排他锁)；
2、我们首先做的第一件事是先检查这个表有没有被别的事务锁住，只要有事务对表里的任何一行数据加了共享锁或排他锁我们就无法对整个表加锁(排他锁不能与任何属性的锁兼容)。
3、因为INNODB锁的机制是基于行锁，那么这个时候我们会对整个索引每个节点一个个检查，我们需要检查每个节点是否被别的事务加了共享锁或排它锁。
4、最后检查到索引ID为6的节点被事务A锁住了，最后导致事务B只能等待事务A锁的释放才能进行加锁操作。

思考：
在A事务的操作过程中，后面的每个需要对user_info加持表锁的事务都需要遍历整个索引树才能知道自己是否能够进行加锁，这种方式是不是太浪费时间和损耗数据库性能了？
所以就有了意向锁的概念：如果当事务A加锁成功之后就设置一个状态告诉后面的人，已经有人对表里的行加了一个排他锁了，你们不能对整个表加共享锁或排它锁了，那么后面需要对整个表加锁的人只需要获取这个状态就知道自己是不是可以对表加锁，避免了对整个索引树的每个节点扫描是否加锁，而这个状态就是我们的意向锁。
https://blog.csdn.net/weixin_36372610/article/details/113300372




Innodb存储引擎支持多粒度的锁定，换句话说，允许事务在表级和行级上同时持有锁。意向锁是一种表级锁，它是由存储引擎自己维护的，不需要用户手动命令干预。如果事务想要给表中几行数据加上行级共享锁，那么需要先在表级别加上意向共享锁（IS）；如果事务想要给表中几行数据加上行级排他锁，那么需要先在表级别加上意向排他锁（IX）

https://blog.csdn.net/Chasing__Dreams/article/details/108847570



锁 隔离级别 出现的问题 脏读，不可重复读 幻读


```sql
SELECT 
        COLUMNS .column_name, 
        COLUMNS .column_comment, 
        COLUMNS .TABLE_NAME, 
        TABLES .table_comment 
FROM 
        information_schema. COLUMNS COLUMNS 
LEFT JOIN information_schema. TABLES TABLES ON TABLES .TABLE_NAME = COLUMNS .TABLE_NAME 
WHERE 
        COLUMNS .table_schema = 'paps' 
AND COLUMNS .table_name LIKE 'paps%';
```

Mybatis插入时返回自增主键（selectKey和useGeneratedKeys）
https://blog.csdn.net/qq_34122822/article/details/79254361

GROUP BY关键字与WITH ROLLUP一起使用
https://www.cnblogs.com/caicaizi/p/4988390.html

MySQLfunction.xmind

https://gitee.com/edidada/test-my-sqlbuilt-in-function

https://dev.mysql.com/doc/refman/8.0/en/built-in-function-reference.html

Flow Control Functions
Name     Description
CASE     Case operator
IF()     If/else construct
IFNULL() Null if/else construct
NULLIF() Return NULL if expr1 = expr2

cast as char
COALESCE()
GREATEST()
IN()
INTERVAL()
IS
IS NOT
IS NOT NULL

CASE
IF()
IFNULL()
NULLIF()

ABS()
ACOS()
ASIN()
ATAN()
CEIL()
CEILING()
CONV()
COS()
COT()
CRC32()
DEGREES()

Arithmetic Operators
%, MOD
DIV

12.6.2 Mathematical Functions
12.7 Date and Time Functions
DATE_FORMAT()
NOW()
12.8 String Functions and Operators

CONCAT()

12.8.1 String Comparison Functions and Operators


LIKE
NOT LIKE
STRCMP()

12.20 Aggregate Functions
sum avg min max count

12.20.1 Aggregate Function Descriptions
12.20.2 GROUP BY Modifiers

新特性解读 | GROUPING() 函数用法解析
https://zhuanlan.zhihu.com/p/178817990

12.20.3 MySQL Handling of GROUP BY
12.20.4 Detection of Functional Dependence


AVG()
COUNT()
MAX()
MIN()
SUM()

工作流
掌握Activiti，camunda等工作流框架中的至少一种

stored procedure
```
CREATE PROCEDURE p ()
BEGIN
  DECLARE i INT DEFAULT 0;
  DECLARE d DECIMAL(10,4) DEFAULT 0;
  DECLARE f FLOAT DEFAULT 0;
  WHILE i < 10000 DO
    SET d = d + .0001;
    SET f = f + .0001E0;
    SET i = i + 1;
  END WHILE;
  SELECT d, f;
END;
```

mysql explain 优化sql
type
https://dev.mysql.com/doc/refman/5.7/en/explain.html


SpringBoot从配置文件中获取属性的四种方法
https://wenku.baidu.com/view/de957e73ae02de80d4d8d15abe23482fb5da0252.html

java代码 Boolean 默认 false
bool 没有默认值

Integer
int 


mysql查看所有表的所有字段

```sql
SELECT 
    COLUMNS .column_name, 
    COLUMNS .column_comment, 
    COLUMNS .TABLE_NAME, 
    TABLES .table_comment 
FROM 
    information_schema. COLUMNS COLUMNS 
LEFT JOIN information_schema. TABLES TABLES ON TABLES .TABLE_NAME = COLUMNS .TABLE_NAME 
WHERE 
    COLUMNS .table_schema = 'paps' 
AND COLUMNS .table_name LIKE 'paps%';
```

[mysql查看执行sql语句的记录日志 ](https://www.cnblogs.com/xcsn/p/11485939.html)

```sql
SET GLOBAL log_output = 'TABLE';
SET GLOBAL general_log = 'ON';
```

mysql内置函数

ifnull
date_format

需要整理，写demo

product_name

select id from tableA where columnA = ''

select * from tableb where XXid = 上面查出来的id


select curdate() into @today;

select @today;

https://www.cnblogs.com/Fengge518/p/13451919.html

https://www.cnblogs.com/bingco/p/11381107.html



中国银行协同项目cims

大量实用临时表



select max (substr(columnName,13)) +1 from tableName where columnName like concat()





mysql中的instr()函数的用法
https://www.cnblogs.com/qingmuchuanqi48/articles/15418961.html



`SELECT INSTR("abcd",'b');`
INSTR(STR,SUBSTR) 在一个字符串(STR)中搜索指定的字符(SUBSTR),返回发现指定的字符的位置(INDEX);
STR 被搜索的字符串
SUBSTR 希望搜索的字符串
结论：在字符串STR里面,字符串SUBSTR出现的第一个位置(INDEX)，INDEX是从1开始计算，如果没有找到就直接返回0，没有返回负数的情况





MySQL软件支持的字符串函数表如下：

| 函数                 | 功能                                                   |
| -------------------------- | ------------------------------------------------------------ |
| CONCAT(str1,str2,...,strn) | 将str1,str2,...,strn连接为一个完整的字符串                   |
| INSERT(str,x,y,instr)      | 将字符串str从第x开始，y个字符串长度的子串替换为字符串instr   |
| LOWER(str)                 | 将字符串str中的所有字母变成小写                              |
| UPPER(str)                 | 将字符串str中的所有字母变成大写                              |
| LEFT(str,x)                | 返回字符串最左边的x个字符                                    |
| RIGHT(str,x)               | 返回字符串最右边的x个字符                                    |
| LPAD(str,n,pad)            | 使用字符串pad对字符串str最左边进行填充，直到长度为n个字符长度 |
| RPAD(str,n,pad)            | 使用字符串pad对字符串str最右边进行填充，直到长度为n个字符长度 |
| LTRIM(str)                 | 去掉str左边的空格                                            |
| RTRIM(str)                 | 去掉str右边的空格                                            |
| REPEAT(str,x)              | 返回字符串str重复x次的结果                                   |
| REPLACE(str,a,b)           | 使用字符串b替换字符串str中所有出现的字符串a                  |
| STRCMP(str1,str2)          | 比较字符串str1和str2                                         |
| TRIM(str)                  | 去掉字符串行头和行尾的空格                                   |
| SUBSTRING(str,x,y)         | 返回字符串str中从x位置起y个字符串长度的字符串                |

mysql架构
连接管理器
缓存
存储引擎
文件系统

innodb如何实现join操作
InnoDB是MySQL的默认存储引擎，它支持事务、行级锁定和外键等特性。在InnoDB中，join操作主要通过以下几种方式实现：

嵌套循环连接（Nested Loop Join）：这是最基本的连接方式，适用于小表和结果集较小的场景。在嵌套循环连接中，驱动表（outer table）的每一行都会与目标表（inner table）的每一行进行比较，直到找到匹配的记录。
哈希连接（Hash Join）：哈希连接利用哈希表的特性，通过将两个表中的某个字段哈希，然后在哈希表中进行匹配。哈希连接适用于两个表按照一个共同的字段进行连接，并且这两个表的行数都比较大。
排序合并连接（Sort-Merge Join）：对于两个已经按照连接字段排好序的表，可以使用排序合并连接。这种方式会先遍历两个表中的第一行，选择最小的那一行作为结果集的第一行，然后继续遍历两个表，选择下一个最小的行作为结果集的第二行，以此类推。
索引连接（Index Join）：在InnoDB中，可以利用覆盖索引（Covering Index）来实现join操作。覆盖索引是指包含所有查询需要的数据的索引，不需要回表查询原表。通过在索引上执行join操作，可以避免访问原表的数据，从而提高查询效率。
需要注意的是，InnoDB的join操作性能还受到其他因素的影响，如表的行数、索引的选择和使用、查询语句的优化等。在实际应用中，需要根据具体的业务场景和数据特点来选择适合的join方式，并进行相应的优化。
frm
ibd
文件读写

mvcc是个概念，不同rdbms实现不同，核心目的是提高软件系统并发量
java里面也需要自己去实现


数据库表外键，删除表的时候不方便

实现了四个标准的隔离级别，默认级别是可重复读(REPEATABLE READ)。在可重复读隔离级别下，通过多版本并发控制(MVCC)+ 间隙锁(Next-Key Locking)防止幻影读。

mysql
varchar 字符串长度需要注意
索引 char like %xx%看执行计划 不走

mysql 共享锁 排他锁

s锁

x锁
mysql的相关技术细节，需要搞清楚是mysql server的还是存储引擎的

mysql
pgsql如何实现sql join
https://www.cnblogs.com/flying-tiger/p/8331425.html

matlab 关系运算

a left join b on a.id = b.id
a left join b on a.id > b.id


mysql关闭ssl

D:\Mysql\mysql-5.7.31-winx64\data\

private_key.pem
public_key.pem
server-cert.pem
server-key.pem



net stop mysql



skipssl

useSSL=false

通配符的分类:
%百分号通配符: 表示任何字符出现任意次数(可以是0次).
_下划线通配符:表示只能匹配单个字符,不能多也不能少,就是一个字符.

like操作符: 
LIKE作用是指示mysql后面的搜索模式是利用通配符而不是直接相等匹配进行比较. 
注意: 如果在使用like操作符时,后面的没有使用通用匹配符效果是和=一致的,SELECT * FROM products WHERE products.prod_name like '1000';只能匹配的结果为1000,而不能匹配像JetPack 1000这样的结果.
1)%通配符使用:
匹配以"yves"开头的记录:(包括记录"yves") 
SELECT * FROM products WHERE products.prod_name like 'yves%';
匹配包含"yves"的记录(包括记录"yves") 
SELECT * FROM products WHERE products.prod_name like '%yves%';
匹配以"yves"结尾的记录(包括记录"yves",不包括记录"yves ",也就是yves后面有空格的记录,这里需要注意) 
SELECT * FROM products WHERE products.prod_name like '%yves';
2)_通配符使用: 
SELECT * FROM products WHERE products.prod_name like '_yves'; 
匹配结果为: 像"yyves"这样记录.
SELECT * FROM products WHERE products.prod_name like 'yves__'; 
匹配结果为: 像"yvesHe"这样的记录.(一个下划线只能匹配一个字符,不能多也不能少)
注意事项:
注意大小写,在使用模糊匹配时,也就是匹配文本时,mysql是可能区分大小的,也可能是不区分大小写的,这个结果是取决于用户对MySQL的配置方式.如果是区分大小写,那么像YvesHe这样记录是不能被"yves__"这样的匹配条件匹配的.
注意尾部空格,"%yves"是不能匹配"heyves "这样的记录的.
注意NULL,%通配符可以匹配任意字符,但是不能匹配NULL,也就是说SELECT * FROM products WHERE products.prod_name like '%;是匹配不到products.prod_name为NULL的的记录.
技巧与建议: 
正如所见， MySQL的通配符很有用。但这种功能是有代价的：通配符搜索的处理一般要比前面讨论的其他搜索所花时间更长。这里给出一些使用通配符要记住的技巧。
不要过度使用通配符。如果其他操作符能达到相同的目的，应该 使用其他操作符。
在确实需要使用通配符时，除非绝对有必要，否则不要把它们用 在搜索模式的开始处。把通配符置于搜索模式的开始处，搜索起 来是最慢的。
仔细注意通配符的位置。如果放错地方，可能不会返回想要的数.



expain出来的信息有10列，分别是id、select_type、table、type、possible_keys、key、key_len、ref、rows、extra
下面对这些字段出现的可能进行解释：
一、 id
     我的理解是SQL执行的顺序的标识,SQL从大到小的执行
1. id相同时，执行顺序由上至下
2. 如果是子查询，id的序号会递增，id值越大优先级越高，越先被执行
3.id如果相同，可以认为是一组，从上往下顺序执行；在所有组中，id值越大，优先级越高，越先执行
二、select_type
      示查询中每个select子句的类型
(1) SIMPLE(简单SELECT,不使用UNION或子查询等)
(2) PRIMARY(查询中若包含任何复杂的子部分,最外层的select被标记为PRIMARY)
(3) UNION(UNION中的第二个或后面的SELECT语句)
(4) DEPENDENT UNION(UNION中的第二个或后面的SELECT语句，取决于外面的查询)
(5) UNION RESULT(UNION的结果)
(6) SUBQUERY(子查询中的第一个SELECT)
(7) DEPENDENT SUBQUERY(子查询中的第一个SELECT，取决于外面的查询)
(8) DERIVED(派生表的SELECT, FROM子句的子查询)
(9) UNCACHEABLE SUBQUERY(一个子查询的结果不能被缓存，必须重新评估外链接的第一行)
三、table
显示这一行的数据是关于哪张表的，有时不是真实的表名字,看到的是derivedx(x是个数字,我的理解是第几步执行的结果)
四、type
表示MySQL在表中找到所需行的方式，又称“访问类型”。
常用的类型有： ALL, index,  range, ref, eq_ref, const, system, NULL（从左到右，性能从差到好）
ALL：Full Table Scan， MySQL将遍历全表以找到匹配的行
index: Full Index Scan，index与ALL区别为index类型只遍历索引树
range:只检索给定范围的行，使用一个索引来选择行
ref: 表示上述表的连接匹配条件，即哪些列或常量被用于查找索引列上的值
eq_ref: 类似ref，区别就在使用的索引是唯一索引，对于每个索引键值，表中只有一条记录匹配，简单来说，就是多表连接中使用primary key或者 unique key作为关联条件
const、system: 当MySQL对查询某部分进行优化，并转换为一个常量时，使用这些类型访问。如将主键置于where列表中，MySQL就能将该查询转换为一个常量,system是const类型的特例，当查询的表只有一行的情况下，使用system
NULL: MySQL在优化过程中分解语句，执行时甚至不用访问表或索引，例如从一个索引列里选取最小值可以通过单独索引查找完成。
五、possible_keys
指出MySQL能使用哪个索引在表中找到记录，查询涉及到的字段上若存在索引，则该索引将被列出，但不一定被查询使用
六、Key
key列显示MySQL实际决定使用的键（索引）
七、key_len
表示索引中使用的字节数，可通过该列计算查询中使用的索引的长度（key_len显示的值为索引字段的最大可能长度，并非实际使用长度，即key_len是根据表定义计算而得，不是通过表内检索出的）
八、ref
表示上述表的连接匹配条件，即哪些列或常量被用于查找索引列上的值
九、rows
 表示MySQL根据表统计信息及索引选用情况，估算的找到所需的记录所需要读取的行数
十、Extra
该列包含MySQL解决查询的详细信息,有以下几种情况：
Using where:列数据是从仅仅使用了索引中的信息而没有读取实际的行动的表返回的，这发生在对表的全部的请求列都是同一个索引的部分的时候，表示mysql服务器将在存储引擎检索行后再进行过滤
Using temporary：表示MySQL需要使用临时表来存储结果集，常见于排序和分组查询
Using filesort：MySQL中无法利用索引完成的排序操作称为“文件排序”
Using join buffer：改值强调了在获取连接条件时没有使用索引，并且需要连接缓冲区来存储中间结果。如果出现了这个值，那应该注意，根据查询的具体情况可能需要添加索引来改进能。
Impossible where：这个值强调了where语句会导致没有符合条件的行。
Select tables optimized away：这个值意味着仅通过使用索引，优化器可能仅从聚合函数结果中返回一行





Heal表的大小可通过称为 max_heap_table_size 的 Mysql 配置变量来控制。


mysql gtid
https://www.cnblogs.com/zhang-ding-1314/p/15125188.html



家人们mysql每天几十万的数据同步，从一个库到另一个库，有没有什么好的方案
canal也行
直接kettle
阿里愚公也是java写的


自建mysql数据库主从同步(GTID方式)
https://www.cnblogs.com/zhang-ding-1314/p/15125188.html



https://baijiahao.baidu.com/s?id=1741371045827915061


关系数据库事务四大特性

ACID

- 原子性
- 一致性
- 隔离性
- 持久性


隔离级别
在MySQL 中,可以通过
`
show variables like '%tx_isolation%'
`
或
`
select @@tx_isolation;
`
语句来查看当前事务隔离级别。

读未提交 RU
读已提交 RC
可重复读 RR
串行化 S

现象

脏读。读到的是另一个事物未提交的事物

不可重复读  不可重复读，是指在数据库访问中，一个事务范围内两个相同的查询却返回了不同数据。

幻读
幻读（Phantom Read），是指当事务不是独立执行时发生的一种现象。
幻读问题在 “当前读” 下才会出现。



什么是当前读、什么是快照读。
快照读：读取快照中的数据，不需要进行加锁。看到快照这两个字，各位肯定马上就想到 MVCC 了，是这样，MVCC 作用于读取已提交和可重复读（默认）这两个隔离级别，这俩隔离级别下的普通 select 操作就是快照读。

当前读：读取的是最新版本的数据, 并且对读取的记录加锁, 阻塞其他事务同时改动相同记录，避免出现安全问题。

除了读取已提交和可重复读这俩隔离级别下的普通 select 操作，其余操作都是当前读：

```sql
select...lock in share mode (共享读锁)
select...for update
update, delete, insert
```


mysql脏读和幻读区别
Mysql之脏读、不可重复读、幻读的区别
数据库在在高并发时，事务会出现三种异常问题。

脏读：在事物还没有提交前，修改的数据可以被其他事物所看到。
不可重复读：在一个事物中使用相同的条件查询一条数据，前后两次查询所得到的数据不同，这是因为同时其他事物对这条数据进行了修改（已提交事物），第二次查询返回了其他事物修改的数据。
幻读：在一个事物A中使用相同的条件查询了多条数据，同时其他事物添加或删除了符合事物A中查询条件的数据，这时候当事物A再次查询时候会发现数据多了或者少了，与前一次查询的结果不相同。

注意：不可重复读与幻读很容易搞混，他们的区别在于：
不可重复读：是同一条记录（一条数据）的内容被其他事物修改了，关注的是update、delete操作一条数据的操作.
幻读：是查询某个范围（多条数据）的数据行变多或变少了，在于insert、delete的操作。

修改隔离级别
有两种方法可以改变当前会话的隔离级别

SET session TRANSACTION ISOLATION LEVEL Serializable;
SET @@tx_isolation='read-committed';
参数可以为：

Read uncommitted
Read committed
Repeatable Read
Serializable
查看当前会话的隔离级别

select @@tx_isolation;
https://www.jianshu.com/p/fb312164f03d




### 共享锁
select a from t where id = 1 lock in share mode;
### 排他锁
select a from t where id = 1 for update;


可以认为 多版本并发控制（MVCC） 是行级锁的一个变种
MySQL中的MDL锁
S锁和X锁。

S锁，英文为Shared Lock，中文译作共享锁，有时候我们也称之为读锁，即Read Lock。S 锁之间是共享的，或者说是互不阻塞的。
X锁，英文为Exclusive Lock，中文译作排他锁，有时候我们也称之为写锁，即Write Lock。如同它的名字，X锁是具有排他性的，即一个写锁会阻塞其他的X锁和S锁。

MySQL是server和engine分离的
Driv的engine是？

Cluster index聚集索引
Unclusrer index 非聚集索引

covering index 覆盖索引
覆盖索引 covering index
https://blog.csdn.net/yinni11/article/details/81812309

https://www.hollischuang.com/archives/3818



最左匹配

select where 的and条件 mysql会优化

MYSQL binlog优化几点思考
https://zhuanlan.zhihu.com/p/147459036

WAL机制
redo log顺序追加写入。事务提交时，只需要保证事务的redo log落盘即可，通过redo log的顺序写代替页面的随机写提升数据库系统的性能。

问题1：如何解决事务提交时flush redo log带来的性能损失
Redo log组提交技术
问题2：binlog和引擎层事务提交的顺序问题
内部XA事务

my.cnf配置
log_bin
bin_alive 大致 

### mysql 源码编译
ubuntu 16
centos 7/8

MySQL Benchmark Tool
DBT2
SysBench
flexAsynch


mysql支持的数据类型 json
text
varchar
date
timestamp


https://dev.mysql.com/doc/refman/5.7/en/json.html

索引下推和覆盖索引都是优化MySQL查询性能的方法，但它们的实现方式有所不同。
索引下推是指MySQL在执行查询时，尽可能地利用索引来减少需要扫描的行数，从而提高查询性能。具体来说，当MySQL使用一个覆盖索引来执行一个查询时，它会首先扫描索引，然后只返回满足查询条件的索引列，而不需要再去检查数据行，因为索引列已经包含了需要的数据。这种方法可以减少磁盘I/O和CPU开销，从而提高查询性能。
覆盖索引是指一个索引包含了查询所需要的所有列，因此MySQL可以直接从索引中获取需要的数据，而不需要再去检查数据行。这种方法可以减少磁盘I/O和CPU开销，从而提高查询性能。覆盖索引通常用于查询只需要返回少量列数据的情况下，例如只需要返回某些列的值或者只需要计算总数的情况下。
虽然索引下推和覆盖索引都能提高查询性能，但它们适用于不同的查询场景。索引下推通常适用于需要返回大量列数据的查询，而覆盖索引通常适用于需要返回少量列数据的查询。

05 如何设计高性能的索引

icp 索引下推


索引下推的一个简单例子是使用SELECT语句查询一个包含多列的表，但只需要返回其中的一列数据。
假设有一个包含以下列的表：
```
CREATE TABLE my_table (
  id INT NOT NULL,
  name VARCHAR(50) NOT NULL,
  age INT NOT NULL,
  address VARCHAR(100) NOT NULL,
  PRIMARY KEY (id),
  INDEX idx_age (age)
);
```

现在需要查询年龄大于等于20岁的所有用户的姓名，可以使用以下查询语句：

```
SELECT name FROM my_table WHERE age >= 20;
```

在执行该查询时，MySQL会使用索引idx_age来定位符合条件的行，然后再到数据行中获取需要的name列数据。但是，如果使用索引下推的话，MySQL会在索引中就获取需要的name列数据，而不需要再到数据行中获取，从而减少了不必要的磁盘I/O和CPU开销，提高了查询性能。可以使用以下查询语句来启用索引下推：

```
SELECT name FROM my_table WHERE age >= 20 AND name IS NOT NULL;
```
在这个查询语句中，增加了一个额外的条件name IS NOT NULL，这个条件的作用是强制MySQL在使用索引idx_age定位符合条件的行时，检查name列是否为NULL，从而在索引中获取需要的name列数据。这样，MySQL就可以使用索引下推来提高查询性能。



MySQL查看和修改事务隔离级别
http://c.biancheng.net/view/7266.html

银行 建议隔离级别 RC
默认 RR
引擎是innodb


查看活跃连接数
https://www.cnblogs.com/caoshousong/p/10845396.html

show processlist;
+------+------+----------------------+---------+---------+------+----------+------------------+
| Id   | User | Host                 | db      | Command | Time | State    | Info             |
+------+------+----------------------+---------+---------+------+----------+------------------+
| 6288 | root | 58.243.43.2:14387    | db_blog | Sleep   | 1852 |          | NULL             |
| 6289 | root | 58.243.43.2:14388    | db_blog | Sleep   | 1852 |          | NULL             |
| 6290 | root | 118.182.97.157:33162 | db_blog | Sleep   |    0 |          | NULL             |
| 6291 | root | 118.182.97.157:33164 | db_blog | Sleep   |    0 |          | NULL             |
| 6292 | root | 118.182.97.157:33166 | db_blog | Sleep   |    0 |          | NULL             |
| 6293 | root | 118.182.97.157:33168 | db_blog | Sleep   |    0 |          | NULL             |
| 6294 | root | 118.182.97.157:33170 | db_blog | Sleep   |    1 |          | NULL             |
| 6295 | root | 118.182.97.157:33172 | db_blog | Sleep   |    0 |          | NULL             |
| 6296 | root | 118.182.97.157:33176 | db_blog | Sleep   |    0 |          | NULL             |
| 6297 | root | 118.182.97.157:33178 | db_blog | Sleep   |    0 |          | NULL             |
| 6298 | root | 118.182.97.157:33180 | db_blog | Sleep   |    0 |          | NULL             |
| 6299 | root | 118.182.97.157:33182 | db_blog | Sleep   |    0 |          | NULL             |
| 6300 | root | 58.243.43.2:14391    | db_blog | Query   |    0 | starting | show processlist |
| 6301 | root | 58.243.43.2:14392    | NULL    | Sleep   |  136 |          | NULL             |
+------+------+----------------------+---------+---------+------+----------+------------------+
14 rows in set (0.12 sec)

mysql doc 5.7 中英文版本
https://www.docs4dev.com/docs/zh/mysql/5.7/reference/innodb-benefits.html
没找到索引相关的，看英文原文


mysql 5.0中文翻译
QQ:362606856
http://www.deituicms.com/mysql8cn/cn/web.html



gitbook
https://github.com/mowangjuanzi/mysql-chinese-doc

https://github.com/shlomi-noach/awesome-mysql
https://github.com/jobbole/awesome-mysql-cn
https://github.com/tmcallaghan/iibench-mysql

http://lists.mysql.com/


mysql> select str_to_date('2016-09-09 15:43:28','%Y-%m-%d %H:%i:%s');
+--------------------------------------------------------+
| str_to_date('2016-09-09 15:43:28','%Y-%m-%d %H:%i:%s') |
+--------------------------------------------------------+
| 2016-09-09 15:43:28                                    |
+--------------------------------------------------------+
1 row in set (0.01 sec)

mysql> select date_format(now(), '%Y-%m-%d %h:%i:%s');
+-----------------------------------------+
| date_format(now(), '%Y-%m-%d %h:%i:%s') |
+-----------------------------------------+
| 2021-01-21 04:28:13                     |
+-----------------------------------------+
1 row in set (0.01 sec)



Mysql中字符串互转时间类型,date_format()和str_to_date()函数
字符串 日期对象相互转换

https://blog.csdn.net/lyg1153/article/details/79755768

str_to_date()有两个参数？对
select str_to_date('2016-09-09 15:43:28','%Y-%m-%d %H:%i:%s');
select date_format(now(), '%Y-%m-%d %h:%i:%s');
2016-09-09 15:43:28
2021-01-25 04:26:40

附加：MySQL now()函数
now()函数是通用的
https://www.w3school.com.cn/sql/func_now.asp





SELECT function(列) FROM 表




SQL 函数
- SQL avg()       平均数
- SQL count() 计数
- SQL first() 首个
- SQL last() 最后一个 作用在cloumn_name上
- SQL max() 最大值
- SQL min() 最小值
- SQL sum() 求和
- SQL Group By 分组
- SQL Having 分组条件
- SQL ucase() 全部大写
- SQL lcase() 全部小写
- SQL mid() 
- SQL len()
- SQL round()
- SQL now()
- SQL format()



Mysql关键字和保留字 - 版本5.7
https://blog.csdn.net/qq_15071263/article/details/77985485


MySQL关键字大全
https://blog.csdn.net/benxiaohai888/article/details/77803090

MySQL Aggregate Functions and Grouping
Aggregate Functions and Grouping
AVG()
BIT_AND()
BIT_OR()
BIT_XOR()
COUNT()
GROUP_CONCAT()
MAX()
MIN()
STD()
STDDEV_POP()
STDDEV_SAMP()
STDDEV()
SUM()
VAR_POP()
VAR_SAMP()
VARIANCE()

https://www.w3resource.com/mysql/aggregate-functions-and-grouping/aggregate-functions-and-grouping-group_concat.php
https://www.educative.io/edpresso/what-is-the-groupconcat-function-in-mysql
https://mariadb.com/kb/en/group_concat/

内置函数 聚合函数
https://mariadb.com/kb/en/built-in-functions/
https://mariadb.com/kb/en/aggregate-functions/

不要光盯着mysql，关注下mariadb和percona等其他mysql分支

String相关函数
Date相关函数

李春 mysql
maridb
XtraBackup和pt-Toolkits
innodb Oracle 收紧
用户返回的问题，test case，Oracle不反馈给社区



DB2 大型机
VLDB、SIGMOD
https://www.cnblogs.com/oxspirt/p/6208912.html
清华大学李国良教授写的"大数据下的数据管理领域研究体会"一文。
ICDE
PVLDB指的是VLDB会议论文集，被VLDB会议接受的论文，按期将会刊登在PVLDB中。VLDBJ则是VLDB基金会主管的期刊，其论文篇幅长，审稿周期长。
关于POLARDB的一篇论文《PolarFS： An Ultra-low Latency and Failure Resilient Distributed File System for Shared Storage Cloud Database》就被数据库顶级学术会议VLDB 2018接收
国际数据工程会议（International Conference on Data Engineering，简称ICDE）是全球范围内顶级三大数据 库学术会议之一



（1）*.frm--表定义，是描述表结构的文件。
（2）*.MYD--"D"数据信息文件，是表的数据文件。
（3）*.MYI--"I"索引信息文件，是表数据文件中任何索引的数据树。



ibd InnoDB存储数据的物理文件通常以ibd作为其文件名后缀

cvs

https://dev.mysql.com/doc/refman/8.0/en/explain.html
https://www.kancloud.cn/baoguoxiao0538/mysql-8-0-chinese-doc/1117563

mysql 存储过程 源码实现
.ibd

开启 general log 将所有到达MySQL Server的SQL语句记录下来。存储方式有两种，一种是file ，一种是table
一般不会开启开功能，因为log的量会非常庞大。但个别情况下可能会临时的开一会儿general log以供排障使用。 
相关参数一共有3：general_log、log_output、general_log_file

https://blog.csdn.net/intelrain/article/details/80451120

mysql 日志 查看select的结果


MYSQL-DBA书籍推荐
https://blog.csdn.net/qq_35254185/article/details/95341993


MySQL查询日志介绍
https://www.cnblogs.com/kerrycode/p/7130403.html

desc mysql.general_log;
select * from mysql.general_log order by event_time desc limit 0,11;

Available parameters are [collection, list]
决解Mybatis传递List集合报错 Available parameters are [collection, list]
https://blog.csdn.net/sinat_28978689/article/details/79406832


只有输入的sql，没有查询到的结果	



mysqlbinlog

两个最重要的使用场景: 
其一：MySQL Replication在Master端开启binlog，Mster把它的二进制日志传递给slaves来达到master-slave数据一致的目的。 
其二：自然就是数据恢复了，通过使用mysqlbinlog工具来使恢复数据。

二进制日志包括两类文件： 
二进制日志索引文件（文件名后缀为.index）用于记录所有的二进制文件； 
二进制日志文件（文件名后缀为.00000*）记录数据库所有的DDL和DML(除了数据查询语句)语句事件。



show variables like 'log_bin';
general_log
general_log_file
log_output  FILE
slow_query_log
slow_query_log_file  D:\devtools\mysql-5.7.31-winx64\data\chengwu2-slow.log



高性能MySQL（第3版）
MySQLDBA修炼之道
MySQL王者晋级之路
MySQL运维内参：MySQL、Galera、Inception核心原理与最佳实践
MySQL技术内幕++InnoDB存储引擎（第二版）
MySQL5.7-官方文档

官网上能下载pdf版的，不建议直接读官方文档，怕大家扛不住！！！学到后期，你会发现很多知识网上不好找到了，这时官方文档的作用就出来了。建议都备着一份吧。



X Protocol
[MySQL 数据库的提速器-写缓存（Change Buffer）](https://www.cnblogs.com/jamaler/p/12371205.html)



mysql protocol
https://blog.csdn.net/caisini_vc/article/details/5356136



mysql 存储过程 函数

http://blog.sina.com.cn/s/blog_52d20fbf0100ofd5.html
https://blog.csdn.net/u011983531/article/details/67639678
https://blog.csdn.net/u013488847/article/details/53819976
http://www.cnblogs.com/xuanzhi201111/p/4175635.html



mysql select 查询时间测试



导入数据的方式
1 sql文件 在使用syslog导入
2 写存储过程



https://www.cnblogs.com/1175429393wljblog/p/5918150.html



生成插入数据库的sql备份文件



sqlyog
导出 导入脚本



https://blog.csdn.net/qq_20975027/article/details/78343972



命令行测试select查询效率



https://blog.csdn.net/weixin_37288522/article/details/79710909
https://blog.csdn.net/blueheart20/article/details/51007659



数据库图形工具



navicate 导入失败
sqlyog 数据库必须存在 导入sql文件



[MySQL 索引](https://zhuanlan.zhihu.com/p/90076968)

MySQL索引
https://blog.csdn.net/weixin_43844718/article/details/128225216

空间索引（spatial index）
MySQL在5.7版本以后 MyISAM 和 InnoDB 中都支持了空间索引，对空间数据类型的字段建立的索引，底层可通过 R树 实现，R树索引 用于多维信息的空间索引，使用较少。

添加空间索引（空间类型的字段必须为非空 字段的数字类型必须是geometry）：


```sql
alter table 表名 add 列 geometry;
alter table 表名 add spatial index 索引名 (列名);
```

聚簇索引（clustered index）
聚簇索引只有 InnoDB 支持，InnoDB 中的主键索引就是一种聚簇索引。

聚簇索引就是一个正常的B+树结构，其叶子节点中的data存放数据表中所有每一行的完整数据。
非聚簇索引其叶子节点的 data 中存的不是完整的数据，而是主键值。

因索引结构会产生两个情况：索引覆盖 和 回表。

索引覆盖：创建一个索引，该索引包含查询中用到的所有字段，只需要通过索引就可以查找和返回查询所需要的数据。
可以一次性完成查询工作，有效减少IO，提高查询效率。

索引覆盖
结合上面的知识储备，我们进一步来优化一下刚才的SQL

select *from lyb_test where age = 12

当这条语句执行时，我们知道会进行两次索引树查询，第一次在二级索引上查询到主键索引的引用，然后到主键索引树中查询到所需要的数据，这个过程我们称之为回表。那为什么要有回表操作呢？由于查询的结果是所有字段，所需要的数据只有主键上才有，所以不得不回表。我们如果将sql改造为下面这种方式：

select id from lyb_test where age = 12

由于查询的值是ID，而id的值已经在age索引树上了，因此可以直接提供查询结果，不需要回表。也就是说，当SQL语句的所有查询字段(select列)和查询条件字段(where子句)全都包含在一个索引中，便可以直接使用索引查询而不需要回表。即在这个查询里，索引age已经“覆盖了”我们的查询需求，故称为索引覆盖。

select * from user_table where username like 'b%' and age >= 13

语句的执行过程有两种可能性：

根据(username，age)联合索引查询所有满足名称以"b"开头的索引，然后回表查询出相应的全行数据，再筛选出满足年龄大于等于13的用户数据。如果表中user_name以b开头的数据有n条，则需要回表n次
根据(username,age)联合索引查询所有满足名称以"b"开头的索引，然后直接再筛选出年龄大于等于13的索引，之后再回表查询全行数据。经过两次筛选之后，回表次数一定小于上述第一种情况
我们把第二种语句执行的过程称之为索引下推
在MySQL中，索引下推是默认启用的状态。在使用InnoDB存储引擎的数据表中，索引下推只能用于二级索引。我们可以通过修改MySQL系统变量来控制索引下推是否开启。设置如下：
SET optimizer_switch = 'index_condition_pushdown=off';// 关闭
SET optimizer_switch = 'index_condition_pushdown=on';// 开启
索引下推一般可用于所求查询字段(select列)不是/不全是联合索引的字段，查询条件为多条件查询且查询条件子句(where/order by)字段全是联合索引。假设表t有联合索引（a,b）,下面语句可以使用索引下推提高效率


回表：顾名思义就是回到表中重新查询一次，也就是先通过二级索引查找到主键ID，然后在通过主键ID去查询聚簇索引找到一行的完整数据。
所以回表的产生也是需要一定条件的，如果一次索引查询就能获得所有的select 记录就不需要回表，如果select 所需获得列中有其他的非索引列，就会发生回表动作。即基于非主键索引的查询需要多扫描一棵索引树。


hash 索引
平衡树
b-树
b+树


InnoDB支持外键，而MyISAM不支持。
3，InnoDB是聚集索引，使用B+Tree作为索引结构，数据文件是和（主键）索引绑在一起的（表数据文件本身就是按B+Tree组织的一个索引结构），必须要有主键，通过主键索引效率很高。MyISAM是非聚集索引，也是使用B+Tree作为索引结构，索引和数据文件是分离的，索引保存的是数据文件的指针。主键索引和辅助索引是独立的。
4，InnoDB不保存表的具体行数，执行select count(*) from table时需要全表扫描。而MyISAM用一个变量保存了整个表的行数，执行上述语句时只需要读出该变量即可，速度很快。
5，Innodb不支持全文索引，而MyISAM支持全文索引，查询效率上MyISAM要高；5.7以后的InnoDB支持全文索引了。
6，InnoDB支持表、行级锁(默认)，而MyISAM支持表级锁。；
7，InnoDB表必须有主键（用户没有指定的话会自己找或生产一个主键），而Myisam可以没有。
8，Innodb存储文件有frm、ibd，而Myisam是frm、MYD、MYI。
Innodb：frm是表定义文件，ibd是数据文件。
Myisam：frm是表定义文件，myd是数据文件，myi是索引文件。


阿里 P8 架构师谈:MySQL 慢查询优化、索引优化、以及表等优化总结
https://www.bilibili.com/video/av583428536/?vd_source=71b9c2a5f966942c83677c2110efde22

根据红黑树的算法来分析TreeMap的实现
https://www.cnblogs.com/coderising/articles/5719517.html



二叉树是不是不能有重复的元素？
没有重复元素


二叉查找树 又叫 二叉排序树，二叉搜索树。Binary Search Tree(BST)

对于二叉查找树中的每一个节点如果存在左节点，左节点的值一定小于该节点的值
对于二叉查找树中的每一个节点如果存在右节点，右节点的值一定大于该节点的值
也就是说对于二叉查找树中的任何一个非叶子节点，左节点值小于当前节点值，右节点值大于当前节点值
二叉查找树的任何一个非叶子节点的左子树中的任何一个节点的值都要小于当前节点值，右子树中的任何一个节点的值都要大于当前节点值。
如果对二叉查找树进行中序遍历，可以得到一个从小到大的序列 ，所以也叫作二叉排序树







一、二叉树-BST  (binary search/sort tree)
二叉树又名二叉查找/搜索/排序树  
或者是一棵空树；
或者是具有下列性质的二叉树：
（1）若它的左子树不空，则左子树上所有结点的值均小于它的父结点的值；
（2）若它的右子树不空，则右子树上所有结点的值均大于它的父结点的值；
（3）它的左、右子树也分别为二叉排序树。

二、平衡二叉树（Self-balancing binary search tree）  
自平衡二叉查找树  又被称为AVL树（有别于AVL算法）  字母是发明者的名字
它是一棵空树或它的左右两个子树的高度差(平衡因子)的绝对值不超过1，并且左右两个子树都是一棵平衡二叉树，平衡二叉树必定是二叉搜索树，反之则不一定

平衡因子（平衡度）：平衡度为1，既每个结点的平衡因子都为 1、－1、0 的二叉排序树。或者说每个结点的左右子树的高度最多差1的二叉排序树。
平衡二叉树的目的是为了减少二叉查找树层次，提高查找速度
平衡二叉树的常用实现方法有AA树、AVL树、红黑树、树堆Treap、伸展树等

三、红黑树-R-B Tree，全称是Red-Black Tree
又称为“红黑树”，它一种平衡二叉树。红黑树的每个节点上都有存储位表示节点的颜色，可以是红(Red)或黑(Black)。
红黑树的特性:
（1）每个节点或者是黑色，或者是红色。
（2）根节点是黑色。
（3）每个叶子节点（NIL）是黑色。 [注意：这里叶子节点，是指为空(NIL或NULL)的叶子节点！]
（4）如果一个节点是红色的，则它的子节点必须是黑色的。（不存在连续的两个红色节点
（5）从一个节点到该节点的子孙节点的所有路径上包含相同数目的黑节点。

注意：
(01) 特性(3)中的叶子节点，是只为空(NIL或null)的节点。
(02) 特性(5)，确保没有一条路径会比其他路径长出俩倍。因而，红黑树是相对是接近平衡的二叉树

B-树是一种多路搜索树（并不一定是二叉的）








单机 索引 实际操作



mysql连接池

具体到Java代码，Connection对象不能随便新建，需要池化复用


下面对一些重要的数据字典表做一些说明：
SCHEMATA表：提供了关于数据库的信息。
TABLES表：给出了关于数据库中的表的信息。
COLUMNS表：给出了表中的列信息。
STATISTICS表：给出了关于表索引的信息。
USER_PRIVILEGES表：给出了关于全程权限的信息。该信息源自mysql.user授权表。
SCHEMA_PRIVILEGES表：给出了关于方案（数据库）权限的信息。该信息来自mysql.db授权表。
TABLE_PRIVILEGES表：给出了关于表权限的信息。该信息源自mysql.tables_priv授权表。
COLUMN_PRIVILEGES表：给出了关于列权限的信息。该信息源自mysql.columns_priv授权表。
CHARACTER_SETS表：提供了关于可用字符集的信息。
COLLATIONS表：提供了关于各字符集的对照信息。
COLLATION_CHARACTER_SET_APPLICABILITY表：指明了可用于校对的字符集。
TABLE_CONSTRAINTS表：描述了存在约束的表。
KEY_COLUMN_USAGE表：描述了具有约束的键列。
ROUTINES表：提供了关于存储子程序（存储程序和函数）的信息。此时，ROUTINES表不包含自定义函数（UDF）。
VIEWS表：给出了关于数据库中的视图的信息。
TRIGGERS表：提供了关于触发程序的信息。



一个read commited下的死锁分析
http://blog.itpub.net/30221425/viewspace-2134433

max.connections.size.per.query=1

Mysql的XA事务分为外部XA和内部XA
https://blog.csdn.net/michaelwubo/article/details/81476591


Caused by: com.mysql.jdbc.exceptions.jdbc4.CommunicationsException: Communications link failure
The last packet sent successfully to the server was 0 milliseconds ago. The driver has not received any packets from the server.




Mysql Server的代码虽然多，但是比较好理解了，我看过下面这些



https://www.zhihu.com/question/22364529






线上业务先和DBA确认服务器磁盘是否是SSD

Mysql 为我们提供了分布式事务解决方案（https://dev.mysql.com/doc/refman/5.7/en/xa.html 这是mysql5.7的文档）
这里先声明两个概念：
资源管理器（resource manager）：用来管理系统资源，是通向事务资源的途径。数据库就是一种资源管理器。资源管理还应该具有管理事务提交或回滚的能力。
事务管理器（transaction manager）：事务管理器是分布式事务的核心管理者。事务管理器与每个资源管理器（resource
manager）进行通信，协调并完成事务的处理。事务的各个分支由唯一命名进行标识。

版权声明：本文为CSDN博主「唐大麦」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/soonfly/article/details/70677138





XA的性能很低。一个数据库的事务和多个数据库间的XA事务性能对比可发现，性能差10倍左右。因此要尽量避免XA事务，例如可以将数据写入本地，用高性能的消息系统分发数据。或使用数据库复制等技术。只有在这些都无法实现，且性能不是瓶颈时才应该使用XA。


MySQL XA 的限制
在MySQL 5.7.7 之前，MySQL一直存在一个"bug"。在事务达到PREPARED状态后，客户端断开与MySQL的连接，MySQL 会自动回滚该事务，这个行为不符合分布式事务的规范，MySQL将PREPARED的事务丢失了。之所以MySQL这么实现是因为MySQL 5.7.7 之前PREPARED的事务并不会记录到binlog中。客户端退出后会丢失该信息，如果允许再提交，那么binlog缺少事务信息，会造成主从不一致。

在MySQL 5.7.7 之后，MySQL 新增了一个XA_prepare_log_event的事件，会把xa start到xa prepare中间的操作记录到Binlog中。Slave读取Relay log 进行回放，当SQL Thread读取到PREPARED的事务后，在读取xa commit或者xa rollback前，会进行一个类似客户端断开的操作，继续读取后续的事务信息，不会阻塞SQL Thread的执行。从以上的结果看，Oracle在MySQL 5.7.7 上确实完美的解决了MySQL XA一直存在的一个"bug"。

MySQL XA 的实践
本人曾在某公司的分布式数据库项目组中实践过基于MySQL XA的分布式事务。MySQL XA 要满足线上高并发的访问要求，在使用时还需要解决两个问题：分布式死锁问题和分布式读一致性问题。分布式死锁问题是指MySQL Server 是可以检测和解决单个MySQL实例中的死锁问题，但涉及到跨越多个MySQL 实例的分布式事务时候，需要程序层面实现死锁的检测和解决。分布式读一致性问题是指MySQL的read view 也是实例级别的，对于全局分布式事务来说无法实现读一致，只能通过select ... lock in share mode在读请求上加锁的串行化隔离级别来实现，这必然会带来并发性能的下降。这就需要在程序层面构建全局的read view来实现全局的MVCC 。当然这两个问题，当时团队的大牛们都已经解决了，我也很有幸参与其中。


ddd：https://www.jianshu.com/p/7003d58ea182


MySQL书籍
http://mingxinglai.com/cn/2015/12/material-of-mysql/

http://blog.codinglabs.org/articles/theory-of-mysql-index.html

https://segmentfault.com/a/1190000012166738

```

查询Mysql最大连接数和当前连接数
最大连接数
`show variables like '%max_connections%'; `
当前连接数
`show full processlist;`
有多少条结果就有多少连接
[mysql: show processlist详解](https://zhuanlan.zhihu.com/p/30743094)

```

[MySQL查看 InnoDB表中每个索引的高度](https://www.cnblogs.com/waterystone/p/6638531.html)

[files-in-innodb-sources](https://dev.mysql.com/doc/internals/en/files-in-innodb-sources.html)

在select窗口中，执行以下语句：

set profiling =1; -- 打开profile分析工具
show variables like '%profil%'; -- 查看是否生效


+------------------------+-------+
| Variable_name          | Value |
+------------------------+-------+
| have_profiling         | YES   |
| profiling              | ON    |
| profiling_history_size | 15    |
+------------------------+-------+


show processlist; -- 查看进程
use cmc; -- 选择数据库
show PROFILE all; -- 全部分析的类型


+----------------+----------+----------+------------+-------------------+---------------------+--------------+---------------+---------------+-------------------+-------------------+-------------------+-------+-----------------------+--------------+-------------+
| Status         | Duration | CPU_user | CPU_system | Context_voluntary | Context_involuntary | Block_ops_in | Block_ops_out | Messages_sent | Messages_received | Page_faults_major | Page_faults_minor | Swaps | Source_function       | Source_file  | Source_line |
+----------------+----------+----------+------------+-------------------+---------------------+--------------+---------------+---------------+-------------------+-------------------+-------------------+-------+-----------------------+--------------+-------------+
| starting       | 0.000175 | 0.000000 | 0.000000   | NULL              | NULL                | NULL         | NULL          | NULL          | NULL              | NULL              | NULL              | NULL  | NULL                  | NULL         | NULL        |
| query end      | 0.000007 | 0.000000 | 0.000000   | NULL              | NULL                | NULL         | NULL          | NULL          | NULL              | NULL              | NULL              | NULL  | mysql_execute_command | sql_parse.cc |        4956 |
| closing tables | 0.000003 | 0.000000 | 0.000000   | NULL              | NULL                | NULL         | NULL          | NULL          | NULL              | NULL              | NULL              | NULL  | mysql_execute_command | sql_parse.cc |        5009 |
| freeing items  | 0.000035 | 0.000000 | 0.000000   | NULL              | NULL                | NULL         | NULL          | NULL          | NULL              | NULL              | NULL              | NULL  | mysql_parse           | sql_parse.cc |        5622 |
| cleaning up    | 0.000011 | 0.000000 | 0.000000   | NULL              | NULL                | NULL         | NULL          | NULL          | NULL              | NULL              | NULL              | NULL  | dispatch_command      | sql_parse.cc |        1931 |
+----------------+----------+----------+------------+-------------------+---------------------+--------------+---------------+---------------+-------------------+-------------------+-------------------+-------+-----------------------+--------------+-------------+


show index from t_log_account; ##查看某个表的索引
show index from t_car_copy; ##查看某个表的索引
-- 使用explain命令查看query语句的性能：
EXPLAIN select * from t_car_copy ; ##查看执行计划中的sql性能
EXPLAIN select * from t_car_copy where org_id = '3';
EXPLAIN select * from t_car_copy where 1=1 and org_id = '3';



```shell

 (B-TREE)


  File Name   What Name Stands For         Size     Comment Inside File
  ---------   --------------------         ------   -------------------
  btr0btr.c   B-tree / B-tree              82,400   B-tree
  btr0cur.c   B-tree / Cursor             103,233   index tree cursor
  btr0sea.c   B-tree / Search              41,788   index tree adaptive search
  btr0pcur.c  B-tree / persistent cursor   16,720   index tree persistent cursor

```


### sql语句执行返回值
insert，返回值是：新插入行的主键（primary key）；需要包含<selectKey>语句，才会返回主键，否则返回值为null。
update/delete，返回值是：更新或删除的行数；无需指明resultClass；但如果有约束异常而删除失败，只能去捕捉异常。


MySQL 添加列，修改列，删除列
ALTER TABLE：添加，修改，删除表的列，约束等表的定义。

查看列：desc 表名;
修改表名：alter table t_book rename to bbb;
添加列：alter table 表名 add column 列名 varchar(30);
删除列：alter table 表名 drop column 列名;
修改列名MySQL： alter table bbb change nnnnn hh int;
修改列名SQLServer：exec sp_rename't_student.name','nn','column';
修改列名Oracle：lter table bbb rename column nnnnn to hh int;
修改列属性：alter table t_book modify name varchar(22);
sp_rename：SQLServer 内置的存储过程，用与修改表的定义。


MySQL 查看约束，添加约束，删除约束 添加列，修改列，删除列

查看表的字段信息：desc 表名;
查看表的所有信息：show create table 表名;
添加主键约束：alter table 表名 add constraint 主键 （形如：PK_表名） primary key 表名(主键字段);
添加外键约束：alter table 从表 add constraint 外键（形如：FK_从表_主表） foreign key 从表(外键字段) references 主表(主键字段);
删除主键约束：alter table 表名 drop primary key;
删除外键约束：alter table 表名 drop foreign key 外键（区分大小写）;
修改表名：alter table t_book rename to bbb;
添加列：alter table 表名 add column 列名 varchar(30);
删除列：alter table 表名 drop column 列名;
修改列名MySQL： alter table bbb change nnnnn hh int;
修改列名SQLServer：exec sp_rename't_student.name','nn','column';
修改列名Oracle：alter table bbb rename column nnnnn to hh int;
修改列属性：alter table t_book modify name varchar(22);


mysql出现unblock with 'mysqladmin flush-hosts'
https://www.cnblogs.com/abclife/p/9469622.html

每个InnoDB表有一个特殊的指数称为聚集索引所在的行的数据存储。通常，聚集索引是主键的同义词。从查询，插入性能最好，和其他的数据库操作，必须了解InnoDB使用聚集索引来优化每个表最常见的查询和DML操作。 当你定义你的表的主键，InnoDB使用它作为聚集索引。为您创建的每个表定义一个主键。如果没有逻辑唯一的和非空的列或列集，添加一个新的自动增量列，它的值自动填充。 如果你不确定你的表的主键、唯一索引，MySQL定位第一所有键列不为空，InnoDB使用它作为聚集索引。 如果表没有主键或唯一索引InnoDB。

information_schema mysql元数据数据库 权限 密码 表引擎

面试题1 ：为什么用 B/B+ 树这种结构来实现索引呢？
红黑树等结构也可以用来实现索引，但是文件系统及数据库系统普遍使用 B/B+ 树结构来实现索引。MySQL 是基于磁盘的数据库，索引是以索引文件的形式存在于磁盘中的，索引的查找过程就会涉及到磁盘 IO 消耗，磁盘 IO 的消耗相比较于内存 IO 的消耗要高好几个数量级，所以索引的组织结构要设计得在查找关键字时要尽量减少磁盘 IO 的次数。为什么要使用 B/B+ 树，跟磁盘的存储原理有关。
这里，局部性原理与磁盘预读。为了提升效率，要尽量减少磁盘 IO 的次数。实际过程中，磁盘并不是每次严格按需读取，而是每次都会预读。磁盘读取完需要的数据后，会按顺序再多读一部分数据到内存中，这样做的理论依据是计算机科学中注明的局部性原理：当一个数据被用到时，其附近的数据也通常会马上被使用。程序运行期间所需要的数据通常比较集中。（1）由于磁盘顺序读取的效率很高(不需要寻道时间，只需很少的旋转时间)，因此对于具有局部性的程序来说，预读可以提高 I/O 效率.预读的长度一般为页(page)的整倍数。（2）MySQL(默认使用InnoDB引擎),将记录按照页的方式进行管理,每页大小默认为16K(这个值可以修改)。Linux 默认页大小为4K。
B-Tree 借助计算机磁盘预读的机制，并使用如下技巧：每次新建节点时，直接申请一个页的空间，这样就保证一个节点物理上也存储在一个页里，加之计算机存储分配都是按页对齐的，就实现了一个结点只需一次 I/O。假设 B-Tree 的高度为 h, B-Tree 中一次检索最多需要 h-1 次 I/O（根节点常驻内存），渐进复杂度为 O(h)=O(logdN)O(h)=O(logdN)。一般实际应用中，出度 d 是非常大的数字，通常超过 100，因此 h 非常小（通常不超过3，也即索引的 B+ 树层次一般不超过三层，所以查找效率很高）。而红黑树这种结构，h 明显要深的多。由于逻辑上很近的节点（父子）物理上可能很远，无法利用局部性，所以红黑树的 I/O 渐进复杂度也为 O(h)，效率明显比 B-Tree 差很多。

面试题2 ：为什么 MySQL 的索引使用 B+ 树而不是 B 树呢？
（1）B+ 树更适合外部存储(一般指磁盘存储),由于内节点(非叶子节点)不存储 data，所以一个节点可以存储更多的内节点，每个节点能索引的范围更大更精确。也就是说使用 B+ 树单次磁盘 IO 的信息量相比较 B 树更大，IO 效率更高。（2）MySQL 是关系型数据库，经常会按照区间来访问某个索引列，B+ 树的叶子节点间按顺序建立了链指针，加强了区间访问性，所以B+树对索引列上的区间范围查询很友好。而 B 树每个节点的 key 和 data 在一起，无法进行区间查找。

官方文档

菜鸟教程

视频

书籍

https://dev.mysql.com/doc/refman/5.7/en/innodb-storage-engine.html

25-MySQL数据库多实例的多种配置方案介绍

同一台主机，3306 3307端口都用

docker

```shell
docker run -p 3306:3306 --name mysql --restart=always --privileged=true -v /usr/local/mysql/log:/var/log/mysql -v /usr/local/mysql/data:/var/lib/mysql -v /usr/local/mysql/conf:/etc/mysql -v /etc/localtime:/etc/localtime:ro -e MYSQL_ROOT_PASSWORD=123456 -d mysql:latest
```


docker run -p 3306:3306 --name mysql -e MYSQL_ROOT_PASSWORD=123456 -d mysql:latest

ng Redis都可以用

mysql只能改表名，不能改数据库名称

`help alter table`

mysql cluster是分布式集群吗？
试用

doc
3.6.2 
select max
left join
limit

如果max有多个，limit只有一个


深入理解MySQL核心技术
对源码的文件对应的功能有讲解
分模块

SELECT p1.name, p1.sex, p2.name, p2.sex, p1.species FROM pet AS p1 INNER JOIN pet AS p2         ON p1.species = p2.species AND p1.sex = 'f' AND p1.death IS NULL  AND p2.sex = 'm' AND p2.death IS NULL;
+--------+------+-------+------+---------+ 
| name   | sex  | name  | sex  | species 
| +--------+------+-------+------+---------+ 
| Fluffy | f    | Claws | m    | cat     | 
| Buffy  | f    | Fang  | m    | dog     
| +--------+------+-------+------+---------+

```
mysql your-database-name

```

线程管理器 入口
sql/mysqld.cc
static void create_new_thread(THD *thd)


sql/sql_class.h
THD类定义

连接管理器
sql/mysqld.cc

void handle_connections_sockets();



XA 分布式事务

```mysql

SHOW VARIABLES LIKE '%xa%';

```


后台开发中经常需要给前端提供接口，返回的字段为null的时候需要设置字段的默认值。

select ifnull(字段,0) from 表名

[java se transactions](https://docs.oracle.com/javase/tutorial/jdbc/basics/transactions.html)

```java

Connection conn = DriverManager.getConnection(...);
try{
  con.setAutoCommit(false);
  Statement stmt = con.createStatement();

   //1 or more queries or updates

   con.commit();
}catch(Exception e){
   con.rollback();
}finally{
   con.close();
}

```


[mysql transaction](https://www.runoob.com/mysql/mysql-transaction.html)

```shell

mysql> use RUNOOB;
Database changed
mysql> CREATE TABLE runoob_transaction_test( id int(5)) engine=innodb;  # 创建数据表
Query OK, 0 rows affected (0.04 sec)
 
mysql> select * from runoob_transaction_test;
Empty set (0.01 sec)
 
mysql> begin;  # 开始事务
Query OK, 0 rows affected (0.00 sec)
 
mysql> insert into runoob_transaction_test value(5);
Query OK, 1 rows affected (0.01 sec)
 
mysql> insert into runoob_transaction_test value(6);
Query OK, 1 rows affected (0.00 sec)
 
mysql> commit; # 提交事务
Query OK, 0 rows affected (0.01 sec)
 
mysql>  select * from runoob_transaction_test;
+------+
| id   |
+------+
| 5    |
| 6    |
+------+
2 rows in set (0.01 sec)
 
mysql> begin;    # 开始事务
Query OK, 0 rows affected (0.00 sec)
 
mysql>  insert into runoob_transaction_test values(7);
Query OK, 1 rows affected (0.00 sec)
 
mysql> rollback;   # 回滚
Query OK, 0 rows affected (0.00 sec)
 
mysql>   select * from runoob_transaction_test;   # 因为回滚所以数据没有插入
+------+
| id   |
+------+
| 5    |
| 6    |
+------+
2 rows in set (0.01 sec)

```





 在MYSQL 8以前，写日志被保护在一把大锁之下，本来并行事务日志写入被人为串行化处理。虽简化了逻辑，但也极大限制了整体的性能表现。8.0很大的一部分工作便是将日志系统并行化。 





mysql -u用户名 -p --default-character-set=utf-8



[mysql中的文件排序(filesort)](https://www.cnblogs.com/chafanbusi/p/10648026.html)





mysql是server和存储引擎分离的

mysql是一个c实现的客户端

mysqld

mysqld_safe

自动开启事务，默认是开启的

刚安装之后

命名管道      ---------      Windows

Unix套接字  ---------      nux



授权的功能

user pwd



还有数据库 表权限控制

访问来源（ip）控制





默认的表：

- mysql

user表

- perfermance_scheme

- information_schema



innodb存储的文件

.frm

.bgd



.frm是表结构文件

.bgd是数据文件



Unix/Linus文件是区分大小写（大小写敏感）

Windows Mac默认是不区分大小写的





INDEX(普通索引)
`mysql>ALTER TABLE `table_name` ADD INDEX index_name ( `column` )`

```
create table test1(
     id int(11) NOT NULL AUTO_INCREMENT COMMENT  '主键id',
     username VARCHAR(25) DEFAULT NULL COMMENT  '用户名',
     password VARCHAR(25) NOT NULL COMMENT  '密码',
     birthday DATE NOT NULL COMMENT  '生日',
     telephone VARCHAR(25) DEFAULT NULL COMMENT  '手机号码',
     PRIMARY KEY (id),
     INDEX  t_tel  (telephone)
 ) 
 COMMENT = '记录用户表';
```

3，删除索引

DROP INDEX index_name ON talbe_name

ALTER TABLE table_name DROP INDEX index_name
1
2
3
4
4，添加索引

ALTER TABLE table_name ADD INDEX index_name (column_list)

ALTER TABLE table_name ADD UNIQUE (column_list)

ALTER TABLE table_name ADD PRIMARY KEY (column_list)
————————————————


refence：https://blog.csdn.net/sddh1988/article/details/78611949


refence：https://blog.csdn.net/sddh1988/article/details/78611949

版权声明：本文为CSDN博主「song_suo」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/sddh1988/article/details/78611949






mysql执行.sql文件



导入sql文件前，如果不存在数据库，一定要新建数据库.



mysql -u root -pxxx database < xxx.sql



```shell
mysql -u root -e 'CREATE DATABASE stockmarket;'
mysql -u root -e "CREATE USER 'makler'@'localhost' IDENTIFIED BY 'makler';"
mysql -u root -e "GRANT ALL ON stockmarket.* TO 'makler'@'localhost';"
```



tidb

5.7.25-TiDB-v3.0.3





[MySQL内核源码解读-SQL解析之解析器浅析](https://blog.51cto.com/wangwei007/2300959)



先登录mysql数据库

mysql -u root

进入到mysql的目录下载进行操作

use mysql

select host, user from user;



[MySQL内核源码解读-SQL解析之解析器浅析](https://blog.51cto.com/wangwei007/2300959)



SQL规范与性能优化

1.2.1、先提前声明，博主工作用到是MySQL，可能有些场景只针对MySQL。说到SQL优化，一些概念必须要理解，不然死记硬背一两天就忘记了。特别是执行计划的概念。

1.2.2、什么是执行计划：a.决定如何访问表数据，是否通过索引，是否排序等。b.多表关联是先访问哪个表。c.多表关联时，使用哪种连接方式，不过现在MySQL只有嵌套连接（嵌套循环，顾名思义就是将一个表为出发点，将该表全部记录逐条去遍历另外一张表的记录）。

1.2.3、SQL执行顺序：a.检查语法是否正确。b.检查表是否存在、权限是否满足等。c.根据统计信息(如data length,rows,index length、索引唯一度)，生成较优的执行计划。d.根据执行计划，进行数据检索、过滤、合并、排序等操作。访问数据时，内存中如存在表数据，则直接进行操作；否则，从磁带读取表数据，放入内存，再进行操作；如内存不足，则内存中较冷数据涮出内存，再从内存中读取数据。

1.2.4、索引：查询的时候如果使用上了索引，可以提高效率，因为建立了索引后，可以理解为数据字典的结构存储，因此根据条件查询的时候更加高效。下面看一下MySQL常用的索引类型的概念。 

a．普通索引：在创建普通索引时，不附加任何限制条件。这类索引可以创建在任何数据类型中，其值是否唯一和非空由字段本身的完整性约束条件决定。建立索引以后，查询时可以通过索引进行查询。例如，在student表的stu_id字段上建立一个普通索引。查询记录时，就可以根据该索引进行查询。

b．唯一性索引:使用UNIQUE参数可以设置索引为唯一性索引。在创建唯一性索引时，限制该索引的值必须是唯一的。例如，在student表的stu_name字段中创建唯一性索引，那么stu_name字段的值就必需是唯一的。通过唯一性索引，可以更快速地确定某条记录。主键就是一种特殊唯一性索引。

c．单列索引:在表中的单个字段上创建索引。单列索引只根据该字段进行索引。单列索引可以是普通索引，也可以是唯一性索引，还可以是全文索引。只要保证该索引只对应一个字段 即可。

d．多列索引：多列索引是在表的多个字段上创建一个索引。该索引指向创建时对应的多个字段，可以通过这几个字段进行查询。但是，只有查询条件中使用了这些字段中第一个字段时，索引才会被使用。例如，在表中的id、name和sex字段上建立一个多列索引，那么，只有查询条件使用了id字段时该索引才会被使用。

e . 全文索引：使用FULLTEXT参数可以设置索引为全文索引。全文索引只能创建在CHAR、VARCHAR或TEXT类型的字段上。查询数据量较大的字符串类型的字段时，使用全文索引可以提高查询速度。例如，student表的information字段是TEXT类型，该字段包含了很多的文字信息。在information字段上建立全文索引后，可以提高查询information字段的速度。MySQL数据库从3.23.23版开始支持全文索引，但只有MyISAM存储引擎支持全文检索。在默认情况下，全文索引的搜索执行方式不区分大小写。但索引的列使用二进制排序后，可以执行区分大小写的全文索引。

还有空间索引，平时也比较少用。目前只有MyISAM存储引擎支持空间检索。目前博主也只接触过InnoDB存储引擎。

1.2.5、一般一张表索引不要超过5个，而且避免重复索引，而且也不是建了索引，根据索引字段条件查询，索引就会起作用。

1.2.6、一般哪些场景会导致索引失效：a.使用like关键字匹配字符串第一个为”%”的场景。b.条件中包含or、in、not in、<>关键字，默认不走索引的。c.访问表上的数据行超出表总记录数30%，变成全表扫描。d.查询条件使用函数在索引列上，或者对索引列进行运算。e.多列索引中，第一个索引列使用范围查询，只能用到部份或无法使用索引。f.多列索引中，第一个查询条件不是最左索引列，上面多列索引概念中也有提到。肯定还有更多的场景，但是博主现在能想到的场景就这些了。

1.2.7、不能同时使用两个索引，一个过滤数据，一个用于排序（主键除外）。

1.2.8、DML语句如果使用索引，会导致lock全表；如果使用了非唯一索引，可能只是锁住一定范围。对此，建议更新/删除数据尽量用上索引，如果可以最好用上主键或唯一索引，另外事务要及时提交。

1.2.9、最后一点，如何看执行计划，分析SQL的性能。这个吧，三言两语说不清楚，直接看其他博主的博文吧：[mysql explain执行计划详解](https://link.zhihu.com/?target=http%3A//www.cnblogs.com/xiaoboluo768/p/5400990.html)。一定要看！

[启用mysql的sql日志](https://blog.csdn.net/aochijing0046/article/details/101493526)


[如何在MySql中记录SQL日志](https://www.cnblogs.com/liuliu/archive/2009/09/04/1560327.html)





https://www.cnblogs.com/liuliu/archive/2009/09/04/1560327.html



在mysql命令行或者客户端管理工具中执行：SHOW VARIABLES LIKE "general_log%";

结果：

general_log OFF
general_log_file /var/lib/mysql/localhost.log

OFF说明没有开启日志记录

分别执行开启日志以及日志路径和日志文件名

SET GLOBAL general_log_file = '/var/lib/mysql/localhost.log';
SET GLOBAL general_log = 'ON';

还要注意

这时执行的所有sql都会别记录下来，方便查看，但是如果重启mysql就会停止记录需要重新设置

 

SHOW VARIABLES LIKE "log_output%";

查询结果FILE



[Mysql 配置慢查询日志（SlowQueryLog）以及使用日志分析工具](https://www.cnblogs.com/codelife1988/p/4159964.html)

MySQL

检查配置文件是否正确？？？



MySQL日志主要包含：错误日志、查询日志、慢查询日志、事务日志、二进制日志。
https://www.cnblogs.com/mungerz/p/10442791.html

show variables like 'general_log_file';
查看本地日志路径

show variables like 'slow_query_log_file';
慢查询日志



错误日志： -log-err
查询日志： -log
慢查询日志: -log-slow-queries
更新日志: -log-update
二进制日志： -log-bin




[windows下启动mysql服务的命令行启动和手动启动方法](https://www.cnblogs.com/xuyou551/p/7998365.html)

1、图形界面下启动mysql服务。
在图形界面下启动mysql服务的步骤如下：
（1）打开控制面板->管理工具->服务，如下图所示：
下面讲通过命令行的方式启动mysql服务：
2、命令行下启动mysql服务。
（1）先找到mysql的安装位置，如我的电脑的安装位置是：D:\Program Files\MySQL\MySQL Server 5.0，我就执行下面的操作：
开始->运行->输入“cmd”开启命令行，然后输入“D:”定位到D盘符。如图
进入Mysql目录下的bin目录中，如图：
（2）输入mysql命令行的服务启用命令：

net start mysql （对应的服务关闭命令为 net stop mysql）





#### 查看mysql版本

centos 7

mysql -V



mysql 命令行

`status;`

`select version();`

net start mysql （对应的服务关闭命令为 net stop mysql）

