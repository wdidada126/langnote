# db
https://github.com/pingcap/awesome-database-learning
miniob

分区 parti by
窗口函数

从Redis 4.0为了解决Redis能支持持久存储的能力，在跟进开源Redis的基础上，开始全新架构自研阶段，内部称为 PegaDB，接下来我们简单来梳理下百度内存数据库的十三年沉淀和演进之路。

duckdb

sr还没实现Radix Partitioning HashJoin吧？

Radix Partitioning HashJoin（基数分区哈希连接）是一种在数据库查询优化中使用的技术，特别是在处理大型数据集时。该技术结合了哈希连接（Hash Join）和分区（Partitioning）的概念，以提高连接操作的效率。以下是对Radix Partitioning HashJoin的详细解释：

1. 哈希连接（Hash Join）基础
概念：哈希连接是一种利用哈希函数来实现和加速数据库中连接（join）操作的算法。它主要适用于等值连接（equi-join）。
步骤：
构建哈希表（Build）：选择两个输入关系（relation）中基数（cardinality）较小的一个（通常称为构建关系或build relation），使用哈希函数将其中的每一条记录的主键（key）值计算为一个哈希值，并根据哈希值将该记录插入到哈希表中。
探测（Probe）：选择另一个基数较大的关系（通常称为探测关系或probe relation），针对其中的每一条记录（通常采用流式遍历的方式），使用和构建关系中相同的哈希函数，计算出相应的哈希值，并根据哈希值在哈希表中寻找到需要比较的记录。如果满足等值条件，则直接输出，得到最终结果。
2. 分区（Partitioning）
概念：当哈希表太大而无法完全存储在内存中时，可以使用分区技术将其分割成多个较小的部分（或分区），每个部分都可以独立地存储在内存中或磁盘上。
作用：通过分区，可以减少内存使用，提高I/O效率，并允许并行处理多个分区，从而进一步提高连接操作的性能。
3. Radix Partitioning HashJoin
概念：Radix Partitioning HashJoin是哈希连接的一种扩展，它使用基数分区策略来优化连接操作。基数分区基于连接键的哈希值将构建关系和探测关系分割成多个不相连的分区，然后各自相应的分区再做哈希连接。
优点：
减少内存使用：通过将哈希表分割成多个较小的分区，可以确保每个分区都能完全存储在内存中，从而避免使用磁盘存储导致的性能下降。
提高并行性：每个分区都可以独立地进行哈希连接操作，从而允许多个处理器或线程并行处理不同的分区，进一步提高整体性能。
适用于大型数据集：基数分区策略可以很好地处理大型数据集，因为它允许将数据集分割成多个较小的部分进行处理。
4. 总结
Radix Partitioning HashJoin是一种高效的数据库连接技术，它结合了哈希连接和分区策略的优点，适用于处理大型数据集和等值连接操作。通过将哈希表分割成多个较小的分区，并在每个分区上独立执行哈希连接操作，可以显著提高连接操作的性能和效率。


国内代码抄袭已经是常态了，思科压根告不赢啊，你当是国外啊，国外这么弄，后果很严重，说到路由器，你可以去看看openwrt怎么出来的，和思科啥关系就知道后果了

说的不是性能，而是公开的有记录可查的专利数据。http://www.icsmart.cn/36500/

专利的数量和质量高说明他们掌握了相关领域的关键技术。掌握了关键技术不代表产品化可以做得好。举个最直观的例子，GPT的几个关键算法基本都是Google提出来的，但是Google的Bard做得就是不如Open API的Chat-GPT。

以前我们这边也都是几千行，十几张表关联很常见。现在数据治理完，好了很多

触发器，视图，存储过程是高级功能

太武断了。没搞过复杂系统。连存储过程、函数都没写过。
视图

在数据库领域中，RBO（Rule-Based Optimization）和CBO（Cost-Based Optimization）是两种重要的查询优化技术，它们的主要目的是生成最佳的执行计划以提高查询效率。
RBO（基于规则优化）
RBO是一种根据预先定义的一套规则来选择执行计划的方法。它不考虑数据的分布和统计信息，仅根据操作符的类型和顺序来决定优先级。RBO的优点在于简单易懂，不依赖于数据的变化，适合于数据量小或者统计信息不准确的情况。然而，RBO的缺点也很明显，它不能适应复杂的查询场景，不能充分利用数据的特征，可能导致执行效率低下。
CBO（基于代价优化）
CBO则是一种根据数据的分布和统计信息来估算每个执行计划的代价，并选择代价最低的执行计划的方法。CBO的优点在于能够根据数据的实际情况来做出最优的选择，适合于数据量大或者查询复杂的情况。然而，CBO的缺点是需要维护数据的统计信息，否则可能导致代价估算不准确，影响执行效果。
在实际应用中，随着数据库技术的发展和数据的增长，CBO逐渐成为主流的优化方法。它可以根据数据的实际情况进行灵活调整，以获取更好的查询性能。同时，随着技术的进步，一些数据库系统也提供了更先进的优化策略，如动态调整执行计划、优化子查询和连接操作等，以进一步提高查询效率。
需要注意的是，无论是RBO还是CBO，都有其适用的场景和限制。在选择使用哪种优化方法时，需要根据具体的数据库环境、数据特点和查询需求进行综合考虑。

意向锁的含义是如果对一个结点加意向锁，则说明该结点的下层结点正在被加锁;对任一结点加锁时，必须先对它的上层结点加意向锁。

并发控制是事务的重要成分，他们会决定事务的调度、处理、abort顺序。
事务的并发控制可以大致分为：
乐观的并发控制
OCC
TS
悲观的并发控制
2PL

阿里数据库开发
https://zhuanlan.zhihu.com/p/686713613

OCC
乐观并行控制协议（OCC）-知乎.mhtml

https://github.com/CN-GuoZiyang/MYDB
https://github.com/edidada/mydb

数据库管理系统-清华大学李国良
https://github.com/edidada/huadb


https://dbdb.io/db/tidb
https://dbdb.io/db/oracle-rdbms

从哪些维度分析一款数据库
并发控制 -> mvcc 乐观 悲观
数据模型 kv 关系表  Relational Key/Value Document/XML Graph Triplestore/RDF
外键
隔离级别
join
日志
查询计划 Query Execution
查询接口 sql
Storage Architecture 


数据库完整性分为以下几类：实体完整性、域完整性、参照完整性和用户自定义完整性。其中，实体完整性是指关系的主关键字不能取“空值"，一个关系对应现实世界中一个实体集，现实世界中的实体是可以相互区分、识别的，也即它们应具有某种惟一性标识。在关系模式中，以主关键字作为惟一性标识，而主关键字中的属性(称为主属性)不能取空值，否则，表明关系模式中存在着不可标识的实体(因空值是“不确定\"的)，这与现实世界的实际情况相矛盾，这样的实体就不是一个完整实体。 

数据库不建议存哪些东西

有的存储设备没有OS
对象存储 块存储 文件存储

https://www.zhihu.com/question/21536660

分布式存储系统
由不同的网络存储协议实现

国内四大单机数据库：

武汉达梦DM

人大金仓 Kingbase

南大通用Gbase

神通OSCAR

国产分布式数据库：

蚂蚁金服 OceanBase

腾讯 TDSQL
中兴 GoldenDB
华为 GaussDB200
巨杉 SequoiaDB
易鲸捷 EsgynDB
万里开源 GreatDB
星环科技 KunDB

国产云数据库：
阿里 AnalyticDB
腾讯 CynosDB
华为 HWSQL
百度 TDB
京东云DRDS
金山 KTS
阿里 PolarDB
浪潮 K-DB
东软 OpenBASE
亚信 AntDB
小米 Pegasus
青云 RadonDB

国外单机数据库：
Oracle
Microsoft SQL Server
IBM DB2
MySQL

开源数据库：
MySQL
MariaDB
PostgreSQL
Greenplum
TiDB

另外还有一些高校也在从事数据库的开发，比如人大，南开，华科，华师。前段时间，OceanBase与华师成立联合实验室，探索产学研结合，希望以后能够发挥高校专长，推进数据库国产化进度。





MySQL的RSS RSS什么鬼？



互联网架构里，数据库只负责数据存储读取，不再承担任何业务逻辑。存储过程和触发器之类是完全不用的。



好资料

https://github.com/pingcap/awesome-database-learning

金融级分布式数据库 TDSQL：在微众银行的大规模实践之路

[腾讯推出的 TDSQL(TencentDistributed SQL) 金融级分布式数据库架构](

 [DynamoDB](https://en.wikipedia.org/wiki/Amazon_DynamoDB),
 [Cassandra](https://en.wikipedia.org/wiki/Apache_Cassandra) or [Riak](https://en.wikipedia.org/wiki/Riak)

[我们为什么放弃了TiDB，选择自研NewSQL](https://mp.weixin.qq.com/s?__biz=MzI4NTA1MDEwNg==&mid=2650784647&idx=1&sn=bfcdbfc2d81bea8b08289453f0c52a8f&chksm=f3f97612c48eff04816c65258e3a9040a623f021eb2698b195268cfa8320b5264cd1c081f39c&mpshare=1&scene=1&srcid=&sharer_sharetime=1579142520564&sharer_shareid=fda52355dcc136785a322db49091f33f&key=80835432ad7ecc2c6650a1fee594ab4162c2432b015ec052293884f5dd7c458742b87c0cf107ec8ef6f5ffdc968321c241cd1bc0e33237f602214755e89c0bf7fb3f734df934ed1de3cb9e8bfd310b55&ascene=1&uin=MjY1MTA3MzYyMQ%3D%3D&devicetype=Windows+10&version=62070158&lang=zh_CN&exportkey=Af0mVBrBZE3AbKCZloFvmU4%3D&pass_ticket=S5ME3darOKtxQuEhoespl3tBDIp9h3EgzeRvYqa8Y2q66xb60VjtjrwDQ5z2sibD)

李鑫，滴滴资深软件开发工程师，多年分布式存储领域设计及开发经验。曾参与NoSQL/NewSQL数据库Fusion、分布式时序数据库sentry、NewSQL数据库SDB等系统的设计开发工作。


**DB-Engines数据库排行榜**

**一、RDBMS**

- MySQL发布8.0.20版本，5.6版本于2021年2月停止更新
- DB2发布11.5.2版本，且看容器化是否可为DB2注入新活力
- PostgreSQL所有版本的小版本更新到最新版，停止维护9.4
- OceanBase发布2.2.5版本

**二、NoSQL**

- Redis发布6 RC1版本，值得期待（把玩有风险，上线需谨慎）
- RocksDB发布6.7.3版本
- ArangoDB发布3.6版本

**三、NewSQL**

- TiDB发布4.0 RC版本
- SequoiaDB发布v5.0 Beta版本

**四、时序数据库**

- InfluxDB发布2.0.0 Beta 8版本
- TimescaleDB发布1.6.1版本

五、大数据生态圈

- Flink发布1.9.2版本，带来大量bug修复
- Elasticsearch发布7.6.2版本
- Greenplum发布6.7版本

六、国产数据库

- ArkDB发布3.0版本
- QianBase发布1.5.4正式版
- OushuDB即将发布4.0版本
七、云数据库

- 阿里云三款数据库产品更新
- 腾讯云六款产品更新
- 京东智联云五款数据库产品更新
- RadonDB即将发布1.1.0版本





详细解读分布式锁原理及三种实现方式
https://m.jb51.net/article/125918.htm

[数据库内核杂谈（六）：表的 JOIN（连接）](https://www.infoq.cn/article/6XGx92FyQ45cMXpj2mgZ)



[数据库内核杂谈（五）：如何实现排序和聚合](https://www.infoq.cn/article/czK9lVhe0N42JOd6tHjc)

[数据库内核杂谈（四）：执行模式](https://www.infoq.cn/article/spfiSuFZENC6UtrftSDD)

#### 数据库方向的三大顶级国际会议

https://www.jianshu.com/p/65570efd0ca3 

IEEE的数据库会议。IEEE的会议一般都比ACM对应会议差一些，ICDE也不例外。

多关注数据库的三大顶级会议, 还有OSDI等.

将motivation和workload作为最根本的方法论。

彻底搞明白存储精髓WAL+RSM.

好好阅读经典论文, 搞清楚workload和motivation.

牢记两个基本观点:

没有抽象的技术, 凡技术都有自己适用的应用场景.

没有广谱的系统, 凡系统都有自己典型的workload.

建议看先阅读下面两本书: 
1. Stonebraker的Architecture of a database system.

2. Jim Gray的Transaction.

1. Stonebraker的Architecture of a database system.

2. Jim Gray的Transaction.

学习分布式的RoadMap

1. WAL + RSM 
2. 研究分布式共识算法, 因为这个是日志复制协议的基石:  TOB协议, Quorum-based协议(mpaxos, raft),  Primary-backup协议.
3. partitioning & replication + local storage engine. 
4. local storage engine: bdb, innodb, leveldb([可以参考我写的源码阅读](http://www.grakra.com/2017/06/17/Leveldb-RTFSC/)). 
5. 磁盘和网络优化技术.  
6. 分布式一致性(隔离性). 
7. 分布式事务: stm, mvcc, 乐观锁.  
8. 分布式查询优化.

工程实现超高的编程技巧

1.能够像haskell那样impure和pure分离.
2.幂等的设计, 让部分有状态的模块成为metal unit, 同时幂等设计和failstop能够将有效地避bf. 
3.元编程能力, 降低代码的冗余和耦合, 代码更适合扩展和组合.
4.超高的系统编程能力.
5.单测, mock测试设计能力.
6.漂亮的日志输出. 
7.会做性能分析, [参考大牛博客](http://www.brendangregg.com/).
8.会使用docker加速自己的开发效率. 

周边涉及

1.精通MySQL sharding, 不知道它的痛，就不知道为什么要坚定不移地搞分布式关系数据库.

2.精通大数据的BI解决方案, 不知道它的痛，就不知道为什么要搞全新的分布式列式数据库.

3.区块链，分布式计算引擎也了解一点.

分布式存储的源码分析方法([详情可以参考我的分享](https://zhuanlan.zhihu.com/p/28156653))



处于迷茫中的青年才俊, 在某个领域投入时间首要考虑产出收益, 窄谱技术收益不高, 多花时间于广谱技术. 努力不如选择重要, 遇到好boss和好项目就加把劲往上冲. 

 [grakra](https://www.zhihu.com/people/grakra) 网易



嵌入式数据库

 [H2](https://www.h2database.com/), [HSQL](http://hsqldb.org/), and [Derby](https://db.apache.org/derby/)  



spring，选择则数据库连接池

 `spring.datasource.type` 



到了 2013 年时，几乎所有支付宝核心数据库，都完成了水平拆分，拆分维度为用户，拆分为 100 个数据分区。此时系统的部署模式是这样的


https://github.com/Tencent/MMKV


[关于数据库建模，概念模型、逻辑模型、物理模型的区别和转化](https://blog.csdn.net/zmx729618/article/details/45059805)





https://github.com/percona/percona-xtrabackup

Mysql 热备份

[Percona XtraBackup](https://www.percona.com/software/mysql-database/percona-xtrabackup) 是 Percona 公司开发的一个用于 MySQL 数据库物理热备的备份工具，支持 MySQl（Oracle）、Percona Server 和 MariaDB，并且全部开源，真可谓是业界良心。







数据库索引，一个列，需要建索引吗？



相当于中分搜索，对这种没有优化，没用







物理模型是对真实数据库的描述。如关系数据库中的一些对象为表、视图、字段、数据类型、长度、主键、外键、索引、约束、是否可为空、默认值。


面试知识点6：MySQL中InnoDB的一级索引、二级索引
https://blog.csdn.net/RoxLiu/article/details/70160664

没有技巧，只能多练。说白了这跟数据库范式的感觉是差不多的，数据又要好计算、又要缓存友好、又不能冗余，是你设计数据结构的三大目标。一般来说，如果太麻烦，我会选择忽略缓存友好，然会让用户加钱买硬件

3范式
Bncf

https://blog.csdn.net/ljp812184246/article/details/50706596

知乎阿里巴巴数据库选型
没有用Oracle，使用了自研分布式数据库中间件，现在遇到瓶颈

sharding-jdbc脱坑了

mybatis-plus的动态表名

再也不担心SQL不支持了


为了用sharding-jdbc搞的我们一些好用的postgresql的功能不能用


@Chow.X 你觉得 sharding-jdbc 大概都有哪些语句不支持？


子查询嵌套查询，复杂的左连接查询

postgresql的 正则表达式查询




有大佬知道  SELECT COUNT(1) FROM t_waybill_9 WHERE finish_time>='2019-09-26 00:00:00' AND finish_time<='2019-09-26 23:59:59' and month=9;  SELECT COUNT(1) FROM t_waybill_9 WHERE finish_time>='2019-09-26 00:00:00' AND finish_time<='2019-09-26 23:59:59' ; 这样的一条语句,加了 moth=9就会变得很慢. 知道这个原因嘛   finish_time是索引

加个联合索引，finish_time与month，就好了/撩一撩


 不适合加联合索引  这个month在一张表就是一个固定的值 9


${}不能防止sql 注入 怎么解决
@S #{}

叫spring是怎么保证在事务里用的是同一个数据库连接

那你告诉我threadLocal的ThreadLocalMap的entry的key为毛是弱引用呢

如果换成普通强引用，有啥后果吗
我的理解就是，WeakReference对应用的对象userInfoLocal是弱引用，不会影响到userInfoLocal的GC行为。如果是强引用的话，在线程运行过程中，我们不再使用userInfoLocal了，将userInfoLocal置为null，但userInfoLocal在线程的ThreadLocalMap里还有引用，导致其无法被GC回收（当然，可以等到线程运行结束后，整个Map都会被回收，但很多线程要运行很久，如果等到线程结束，便会一直占着内存空间）。而Entry声明为WeakReference，userInfoLocal置为null后，线程的threadLocalMap就不算强引用了，userInfoLocal就可以被GC回收了。map的后续操作中，也会逐渐把对应的"stale entry"清理出去，避免内存泄漏。
　　所以，我们在使用完ThreadLocal变量时，尽量用threadLocal.remove()来清除，避免threadLocal=null的操作。前者remove()会同时清除掉线程threadLocalMap里的entry，算是彻底清除；而后者虽然释放掉了threadLocal，但线种threadLocalMap里还有其"stale entry"，后续还需要处理。

Mysql in exist






分布式数据库，底层存储常见有两种：

- KV存储，以Cockroach、TiDB为代表，底层是rocksdb；

- 底层也是关系库，以Aurora、PolarDB为代表，OceanBase也类似。

  s

这两种各有优势：
- 1.KV就像题主说的，操作简单，摆脱掉了行的约束，维护/优化也方便；
- 2.底层是关系库的话，单机事务什么的就有了，但是问题也来了，全局的事务就需要在外层考虑了。因为采用了一个具体的基座，优化也是一个问题，什么样的东西可以优化，并且下推到基座去处理，什么样的东西不能下推，要全局的做优化。


KV的话，就没这两个问题：
分布式情况下，全局事务+kv的版本就可以了，单机事务其实是个伪命题。
所有的额外信息在基座外部，这样就全局的优化就很容易。
并且，基座不依赖于具体的关系库，就是可替换的，例如TiDB第一个适配基座是Hbase，后面换的rocksdb。

其实不管是KV还是关系库做基座/存储层，对于接入层都需要适配和兼容/模拟关系库的行为，TiDB是MySQL，Cockroach是PG，由于计算层和存储层的分离，（用户一般不会直接访问到底层基座），所以这一层的工作少不了，并不会因为引入关系库而降低开发维护代价。

简单在接入层处理一下，然后透传，这是数据库中间件干的活（DRDS、mycat、sharding-proxy），不是一个分布式数据库的事儿。



知乎 赵伟 数据库

https://www.zhihu.com/people/zhaowei-db/activities



数据库管理系统（DBMS） 管理的是符合特定数据模型的数据，最普遍的是关系数据模型（relational data model）。使用关系模型的DBMS成为RDBMS。关系数据模型中，用户的数据是一个个 ‘关系表’，每个表是数据行的集合，这些数据行具有相同的结构。这个结构主要是指一个关系表包含若干个列，每个列具备一些属性和特征，包括数据类型，完整性约束（是否允许 null 值，是否unique），用户自定义的约束等，这些特征决定了一个列的数据格式，数据使用方法，允许的操作类型和方法，以及确保数据正确的约束条件等。 

除了关系数据模型，数据库系统还出现过其他数据模型，包括层次，网状和对象数据模型，不过这些模型曾经热闹过一阵子后都沉寂下来了。唯二比较流行的是key-value 数据，和json数据模型。这两种nosql数据模型的优点是简单和灵活性，易于快速搭建业务系统，但是通常随着业务系统稳定下来之后，系统开发者又会逐步发现nosql的灵活性的另一面，就是缺乏规范性，任意加减字段等经常会把系统搞崩溃，本质原因是这种做法违背了早已被验证的系统设计理念 --- ‘程序与数据分离’。

除了具备特定的数据模型，数据库系统还需要在其数据模型之上实现方便易用的数据读写方式，对于关系数据库来说，这个读写方式就是SQL语言，对于key-value和json数据来说，通常是API 编程读写，也就是‘程序与数据绑定’了，这显然是个巨大的缺陷。另外对于json数据模型来说，也有厂家自定义的查询语言，但是并没有标准化，比如mongodb有自己的json数据查询语言。另外目前SQL标准当中已经有了json扩展，mysql和postgresql都支持json数据的存取，并且可以与关系数据同时使用，从而大大增加了便利性。

最后，关系数据库还有事务处理系统，实现ACID属性。本质上来说，就是确保并发读写数据的多个用户连接可以同时正确滴工作，互不干扰。并且用户的所有数据读写操作被划分为‘事务’的单位，每个事务要么完全成功执行并且其写入操作持久存在；要么完全不执行----无论系统经历任何故障和错误，都不会出现执行了一部分的事务的写入数据被其他事务读取到的错误情况。

最最后，现代数据库系统还有高可靠性（high availability）和高可扩展性（high scalability）机制，确保DBMS系统在部分节点故障情况下仍然可以对外提供服务，确保系统处理能力可以随着数据库节点的增加而增加。

可以看到数据库管理系统（DBMS）把用户管理其数据的任务从用户软件中独立出来，用户只需要使用简单易用的接口即可通过DBMS 管理和访问其数据。当然，其数据必须是符合特定模型的，比如关系模型，或者json数据格式。从其近50年的发展来看，关系数据模型具备非常普遍的适用性，能够满足大多数数据处理需求。

文件系统是DBMS之下的系统功能。文件系统所管理的数据是‘文件’，而文件的具体格式和内容则并不关心。在文件系统看来，一个文件中存放的就是一串子节或者字符，仅此而已。这种简单性让它具有更加广泛的适用性，但是缺点就是用户需要做的事情就多了很多很多，上述RDBMS可以做的事情，假入使用文件系统来做的话，则需要用户实现全部RDBMS的功能，这是一个难度极其巨大的任务。

数据库与新硬件
https://zedware.github.io/NEW-HARDWARE/

## 教学的db

清华大学李国良
huadb
github.com/thu-db/huadb.git

https://github.com/cmu-db/bustub
c++的

risinglight
Rust的

https://github.com/ruc-deke/rucbase-lab