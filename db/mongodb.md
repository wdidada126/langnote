# MongoDB

叶翔MongoDB
叶翔：MongoDB江浙地区用户会主席 在此之前也是淘宝Tair分布式KV系统的技术负责人，负责过阿里云Memcache，Redis服务等，在阿里集团工作8年，一直在做NoSQL相关的技术。 

https://mongoing.com/ychtiger

面试题：分区 一致性hash



杨亚洲(专注mongodb及高性能中间件)2020 年 10 月 13 日加入

万亿级mongodb集群性能优化实践

Qcon讲师，滴滴出行专家工程师/OPPO-mongodb负责人，负责数万亿级数据量文档数据库mongodb内核研发、性能优化及运维工作。后续持续分享《MongoDB内核源码设计、性能优化、最佳实践》,https://github.com/y123456yz





https://www.jianshu.com/p/e62405f72163

mongodb 索引简介
为了方便理解后面的优化思路，先简单介绍 mongodb 的索引，但不会太详细，只会涉及到本次优化中使用到的索引类型。

mongodb 的索引类型分为：

单键索引（Single Field Index）
复合索引（Compound Index）
多键索引（Multikey Index）
地理空间索引（Geospatial Index）
文本索引（Text Indexes）
哈希索引（Hashed Indexes）

如果我们想要定义某个索引为唯一索引，可以使用索引的属性来定义，索引的属性有：
唯一索引
部分索引
稀疏索引
TTL索引


Bully算法和Raft算法在MongoDB选举中的应用。
https://www.jianshu.com/p/916e5e443ad7
https://blog.csdn.net/weixin_32353247/article/details/112045788
https://www.infoq.cn/article/2014/08/ark-mongodb

崔鑫，华为云DDS数据库架构师，十二年存储与数据库研发与运维经验。目前在华为云DDS团队领导GaussDB(for Mongo)和DDS的内核创新/研发/运维。
https://docs.mongoing.com/



mongodb本身的failover机制，无需使用如MHA之类的方式实现。

Mongodb慢查询笔记 (Mongodb slow query log)
https://www.cnblogs.com/seasonzone/p/3816157.html

/var/log/mongodb/mongod.log
`systemctl start mongod`

配置选项
https://docs.mongodb.com/manual/reference/configuration-options/

慢查询日志

```shell
     operationProfiling:
           slowOpThresholdMs: 200
           mode: slowOp
```


operationProfiling:
   mode: <string>
   slowOpThresholdMs: <int>
   slowOpSampleRate: <double>





operationProfiling:
   mode: all
   slowOpThresholdMs: 200
   slowOpSampleRate: 1.0

记一次 MongoDB 慢日志优化历程
https://blog.csdn.net/weixin_38625669/article/details/103954564
db.getCollection('system.profile').find({})
先开启 profiling 功能，此处已把需要优化的 DB 的 profiling 级别设置为 1，设置的命令为 db.setProfilingLevel(1)，默认执行时间大于 100ms 的操作命令都会被记录。
有两种方式可以查看慢日志，一种是直接查看日志文件（文件的位置和配置有关，此处是 /home/ocean/log/mongodb，每天产生一个新的日志文件），另一张是查看 db.system.profile 这个 collection。


极客时间 Mac高手可
MongoDB 4.0已经支持事务了



git remote add origin https://github.com/edidada/mongodb.git
git push -u origin main

centos 7 tencent云主机安装

MongoDB Server
shell
windows export 是单独的

图形工具

Robo 3T 1.4.1

Studio 3T 可以导入导出

Studio 3T 需要license


DBeaver企业版支持连接MongoDB数据库

MongoDB和MySQL对比分析及选型
MongoDB不支持事务，扩容方便

优点： 
1）社区活跃，用户较多，应用广泛。 
2）MongoDB在内存充足的情况下数据都放入内存且有完整的索引支持，查询效率较高。 
3）MongoDB的分片机制，支持海量数据的存储和扩展。 
缺点： 
1）不支持事务 
2）不支持join、复杂查询

https://blog.csdn.net/liao0801_123/article/details/89373494
