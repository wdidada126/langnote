# cassandra

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

基于列 Java写的
Cassandra是一套开源分布式NoSQL数据库系统。它最初由Facebook开发，用于储存收件箱等简单格式数据，集GoogleBigTable的数据模型与Amazon Dynamo的完全分布式的架构于一身Facebook于2008将 Cassandra 开源，此后，由于Cassandra良好的可扩展性，被等知名网站所采纳，成为了一种流行的分布式结构化数据存储方案。



特征处理里用的多，适合一对一检索，比如现在的人脸比对；

还有现在时兴的图片搜索，人脸比对就是图片搜索中的其中一个应用



```asciidoc
docker pull cassandra:latest
```

https://blog.csdn.net/itcast_cn/article/details/107559490

https://blog.csdn.net/itcast_cn/article/details/107559499

https://blog.csdn.net/itcast_cn/article/details/107559525



cassandra -v
4.0.1



gossip

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





```asciidoc
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





配置文件

.yaml
集群名称
绑定ip
用户名密码


https://github.com/apache/cassandra


Cassandra实战





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