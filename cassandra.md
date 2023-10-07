# cassandra

## book书籍
Cassandra The Definitive Guide, (Revised) Third... (Z-Library).pdf
Cassandra实战

特征处理里用的多，适合一对一检索，比如现在的人脸比对；还有现在时兴的图片搜索，人脸比对就是图片搜索中的其中一个应用

datastax 基于cassandra的数据库？

库：spring-data-cassandra

https://blog.csdn.net/cnhome/article/details/85069997

修改cassandra.yaml，将

authenticator: AllowAllAuthenticator
修改为：
authenticator: PasswordAuthenticator
这样做的目的是为了，可以使用用户名和密码，进行远程连接。默认的策略，好像只能本地连接。

cassandra 常用端口
7199 - JMX（8080 pre Cassandra 0.8.xx）
7000 - 节点间通信（如果启用了TLS，则不使用）
7001 - TLS节点间通信（使用TLS时使用）
9160 - Thrift客户端API
9042 - CQL本地传输端口

Cassandra传统上被人们认为是一个极为强大的数据库，可以在绝大多数使用场景中脱颖而出，然而也是比较难学习和操作的数据库之一。
DataStax的团队由Cassandra数据库演进过程中的领军人物组成，他们贡献了Cassandra 3.0版本中大部分的代码。在4.0及之后的版本中，我们的团队也在持续积极地与开源社区紧密合作，为Cassandra的未来贡献所能。
DataStax致力于与Cassandra社区一起让Cassandra成为更容易为个人使用、为企业采用和延伸的技术。

- 将提供简化的开发者接口APIs，包括REST和GraphQL
- 将在CQL中添加更多与SQL类似的功能，包括索引(indexing)、表的合并(Joins)、ACID（Atomicity原子性、Consistency一致性、Isolation隔离性、Durability持久性）及对JSON的完全支持
- 标准的管理接口APIs及正式的、有官方支持的Kubernetes Operator
- 将使存储引擎变为可插拔的，并同其它接口APIs一起实现数据库部署和配置的定制化


https://github.com/apache/cassandra

基于列，Java写的
Cassandra是一套开源分布式NoSQL数据库系统。它最初由Facebook开发，用于储存收件箱等简单格式数据，集GoogleBigTable的数据模型与Amazon Dynamo的完全分布式的架构于一身Facebook于2008将Cassandra开源，此后，由于Cassandra良好的可扩展性，被等知名网站所采纳，成为了一种流行的分布式结构化数据存储方案。

特征处理里用的多，适合一对一检索，比如现在的人脸比对；
还有现在时兴的图片搜索，人脸比对就是图片搜索中的其中一个应用
Cassandra 最主要的使用场景是作为大数据量的高可用分布式数据库。它适用于需要以下特点的场景:
- 高吞吐量:Cassandra可以很容易地承载TB和PB级的数据量,提供高达数十万的读写QPS能力。
- 高可用性:Cassandra提供主从高可用架构,通过复制保证可靠性和故障转移。
- 无单点故障:Cassandra通过分布式设计,没有单点故障。任何一个节点宕机不会影响集群整体。
- 易扩展:Cassandra可以很容易地在服务器间增加节点,实现线性伸缩。
- 无关系:Cassandra不需要严格的表名和列名,适用于半结构化和非结构化数据。
- 支持CDC:Cassandra提供变更数据捕获(CDC)功能,可以记录数据的每一次变更。
基于这些特点,Cassandra常见的使用场景包括:
- 网站访问解析:比如记录每次网站访问,分析访问量。
- 物联网日记记录:比如记录智能设备每次上报的数据,实现追踪和分析。
- 网站点击流:记录用户每次点击日志,分析用户行为。
- 交易日志:记录每一笔交易信息,实现数据分析和审计。
- 搜索引擎存储:作为搜索引擎关键数据的后端存储。
- 用户活动轨迹:记录用户各种活动信息,分析用户画像。
- 实时指标监控:比如多数分布式应用的性能指标采集。
总的来说,Cassandra适合需要:
- 高性能
- 高可用
- 大容量
- 实时读写
这些需求的场景。只要能充分利用它的优点,Cassandra都能派上用场。

```shell
docker pull cassandra:latest
```

https://blog.csdn.net/itcast_cn/article/details/107559490

https://blog.csdn.net/itcast_cn/article/details/107559499

https://blog.csdn.net/itcast_cn/article/details/107559525



cassandra -v
4.0.1


Cassandra中Gossip具体实现方式
https://blog.csdn.net/zhangzhaokun/article/details/5859760


cassandra根据用户名密码登录cqlsh

https://www.cnblogs.com/zzd-zxj/p/6062768.html

```shell
cqlsh -ucassandra -pcassandra
Connected to Test Cluster at 127.0.0.1:9042
[cqlsh 6.0.0 | Cassandra 4.0.1 | CQL spec 3.4.5 | Native protocol v5]
Use HELP for help.
cassandra@cqlsh>
```



```
CREATE USER test WITH PASSWORD '123456' SUPERUSER; 
Unauthorized: Error from server: code=2100 [Unauthorized] message="Only superusers can create a role with superuser status"
```

java代码访问cassandra

https://docs.datastax.com/en/developer/java-driver/4.0/manual/

KEYSPACE
TABLE

在Cassandra中, KEYSPACE相当于数据库(database),TABLE相当于数据库表(table)。
- KEYSPACE概念:
一个Cassandra服务器可以包含多个keyspace。每个keyspace代表了一个独立的命名空间。
一个keyspace包含:
- 一个或多个表(tables)
- 一个选项的列家族(column families)
- 其他键空间(keyspaces)的集合
一个keyspace可包含多个用户、权限和配额。
- TABLE概念:
表(table)存储具有相似结构的行。
Cassandra的表非常相似于传统关系型数据库管理系统中的表。
每个表包含:
- 一组列(columns)
- 一组行(rows)

不同之处在于:

- Cassandra不要求严格的列定义
- 支持高度可扩展的列数和行数
- 采用分布式冗余设计

总的来说:

- KEYSPACE相当于数据库
- 包含一个或多个table
- 一个keyspace具有独立的命名空间和权限

- TABLE相当于数据库表
- 包含列和行构成
- Cassandra表的结构更灵活
KEYSPACE和TABLE共同构成了Cassandra的数据模型。方便地组织和管理数据。
希望能为你解决KEYSPACE和TABLE概念!


Cassandra本身不是一个关系数据库,也不完全支持SQL。不过Cassandra提供了部分SQL的支持:
1. CQL(Cassandra Query Language)
CQL是Cassandra定义的自己的查询语言。是扩展自SQL的。
通过CQL,用户可以使用类似SQL的语法与Cassandra交互:
- 创建键空间(create keyspace) 
- 创建表(create table)
- 查询数据(select)
- 更新数据(update)
- 删除数据(delete)等
2. CQL Shell
Cassandra提供一个CQL Shell的命令行工具。用户可以在命令行使用CQL交互式执行CQL语句。
3. Cassandra Thrift API
Cassandra还提供一个Thrift API,支持使用类SQL语句与Cassandra交互。
4. Spark SQL支持
Cassandra可以作为数据源,集成到Spark SQL中。用户可以使用Spark SQL的SQL语法查询Cassandra数据。
5. Hadoop SQL支持
Cassandra也可以作为数据源与Hadoop集成。使用Hive或Impala的SQL访问Cassandra数据。
总的来说:
- CQL是Cassandra自己的查询语言,类似但不完全兼容SQL 
- Cassandra提供CQL Shell使用CQL交互
- 提供Thrift API使用SQL语句
- 支持Spark SQL和Hadoop SQL访问
但Cassandra本身仍然是一个非关系型数据库,不支持所有SQL功能,也不存在表 joins 等关系操作。
需要使用基于CQL的方式访问。


```shell
CREATE KEYSPACE IF NOT EXISTS store WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : '1' };

CREATE TABLE IF NOT EXISTS store.shopping_cart (
userid text PRIMARY KEY,
item_count int,
last_update_timestamp timestamp
);


INSERT INTO store.shopping_cart
(userid, item_count, last_update_timestamp)
VALUES ('9876', 2, toTimeStamp(now()));
INSERT INTO store.shopping_cart
(userid, item_count, last_update_timestamp)
VALUES ('1234', 5, toTimeStamp(now()));
```


.cql

9042 cql shell

```


 SELECT * FROM store.shopping_cart;
 INSERT INTO store.shopping_cart (userid, item_count) VALUES ('4567', 20);



cassandra@cqlsh>  SELECT * FROM store.shopping_cart;

 userid | item_count | last_update_timestamp
--------+------------+---------------------------------
   1234 |          5 | 2021-11-07 06:56:45.641000+0000
   9876 |          2 | 2021-11-07 06:56:44.978000+0000

(2 rows)
cassandra@cqlsh>  INSERT INTO store.shopping_cart (userid, item_count) VALUES ('4567', 20);
cassandra@cqlsh>  SELECT * FROM store.shopping_cart;

 userid | item_count | last_update_timestamp
--------+------------+---------------------------------
   4567 |         20 |                            null
   1234 |          5 | 2021-11-07 06:56:45.641000+0000
   9876 |          2 | 2021-11-07 06:56:44.978000+0000

```



```
cassandra@cqlsh> select release_version from system.local;

 release_version
-----------------
           4.0.1

(1 rows)
```

4.1.2

配置文件

.yaml
集群名称
绑定ip
用户名密码


https://github.com/apache/cassandra

https://www.bilibili.com/video/BV1aQ4y1Z7Nj



刚毕业，导师是专门做文档数据库相关的大牛，具体是谁不提了，以前是华盛顿智力委员会下面数据库方向管批钱的。MongoDB只是一种可能，现在比较热门的Apache Cassandra所代表的NoSql是未来数据库唯一的方向。她以前一直给我们强调关系数据库的诞生是因为技术上的不足从而用逻辑和冗余规则约束数据，真正的数据最核心在于free，本身必须是纯粹的文本，规则来自于使用，而不是使用屈服于规则。数据库最前沿也许我还不敢说，但是数据库的终极目的是解放数据而不是约束

cassandra不仅吸收了dynamo论文中的如何做分布式，如何做副本复制，故障容错等方面成功的经验，又吸取了google bigtable中的LSM单机引擎层面精华。理论扎实，工程实现靠谱，所以面世以来，不断受到人们的追捧。

zoom用了 跨全球数据中心



Cassandra是一套开源分布式NoSQL数据库系统。它最初由Facebook开发，用于储存收件箱等简单格式数据，集Google BigTable的数据模型与Amazon Dynamo的完全分布式的架构于一身Facebook于2008将 Cassandra 开源，此后，由于Cassandra良好的可扩展性，被Digg、Twitter等知名Web 2.0网站所采纳，成为了一种流行的分布式结构化数据存储方案。

Cassandra是一个混合型的非关系的数据库，类似于Google的BigTable。其主要功能比Dynamo （分布式的Key-Value)存储系统更丰富，但支持度却不如文档存储MongoDB（介于关系数据库和非关系数据库之间的开源产品，是非关系数据库当中功能最丰富，最像关系数据库的。支持的数据结构非常松散，是类似json的bjson格式，因此可以存储比较复杂的数据类型）。Cassandra最初由Facebook开发，后转变成了开源项目。它是一个网络社交云计算方面理想的数据库。以Amazon专有的完全分布式的Dynamo为基础，结合了Google BigTable基于列族（Column Family）的数据模型。P2P去中心化的存储。很多方面都可以称之为Dynamo 2.0





java写的

用了antlr

全球跨集群部署

nosql评测
https://www.datastax.com/products/compare/nosql-performance-benchmarks?spm=a2c4e.10696291.0.0.244f19a4wV7yvT


https://github.com/jeffreyscarpenter/cassandra-guide


https://cassandra.apache.org/



https://www.cnblogs.com/ctgulong/p/10982145.html
https://blog.csdn.net/kobejayandy/article/details/12392609
https://zhuanlan.zhihu.com/p/78255146

### 架构亮点

Cassandra 4的主要架构亮点有:
1. 支持插件式存储引擎
Cassandra 4引入了插件式存储引擎,默认还是使用SSTable存储。但开发者可以根据需求开发自己的存储插件。
2. 支持多数据模型
除了传统的列存储外,Cassandra 4还支持多数据模型,包括键值存储、文档存储、表格存储等。
3. 优化的负载平衡
Cassandra 4对负载平衡进行了优化。利用 solicited load reports 主动上报节点负载,实现更智能的负载分配。
4. STCS新一代一致性算法
Cassandra 4引入了全新的一致性算法 Slot-Tenant Consistency Service(STCS),替代原来的 Gossiping Property Verifier。
5. 支持全局序列号
Cassandra 4提供全局唯一且递增的序列号生成。能解决分布式系统中处理序列号和全局排序的难题。
6. 改进的网络层
Cassandra 4改进了网络层,基于 Netty,提供更高性能的网络IO。减少 CPU 和内存消耗。
7. SQL接入层
Cassandra 4支持使用SQL语法访问数据。内置了Spark SQL访问层,方便与Spark集成。
8. 升级 quartz 到 2.3
Cassandra 4将内置的 quartz 调度器升级到 2.3 版,提供更多的新特性。
9. 更多新特性
如:演进后的集群拓扑结构、内置的库存管理功能等。
总的来说,Cassandra 4在原有稳定基础上,提供了一系列优化和新功能。
尤其是支持插件式存储引擎、多数据模型、改进的网络层等,都带来了不小的提升。
