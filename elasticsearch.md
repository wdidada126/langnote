# elasticsearch



## 竞品Splunk

## 官方文档

es文档
https://www.elastic.co/guide/en/elasticsearch/reference/7.17/index.html

## analysis-ik分词器

ik版本必须跟es版本一致

./bin/elasticsearch-plugin install https://github.com/medcl/elasticsearch-analysis-ik/releases/download/v2.3.0/elasticsearch-analysis-ik-2.3.0.zip

https://github.com/medcl/elasticsearch-analysis-ik/releases?page=14

https://github.com/medcl/elasticsearch-analysis-ik/releases/download/v7.9.2/elasticsearch-analysis-ik-7.9.2.zip


## 应用场景
应用程序搜索
网站搜索
企业搜索
日志处理和分析
基础设施指标和容器监测
应用程序性能监测
地理空间数据分析和可视化
安全分析
业务分析


## 核心概念

index 索引
ideices

文档 document

item

_doc 从6.x开始es慢慢放弃type，并统一默认type为_doc

_type

_search

restful api
java api

PUT
POST

NRT
Near Realtime，近实时，有两个层面的含义，一是从写入一条数据到这条数据可以被搜索，有一段非常小的延迟（大约1秒左右），二是基于Elasticsearch的搜索和分析操作，耗时可以达到秒级。

作者：阿甘
链接：https://zhuanlan.zhihu.com/p/646455006
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

Node单独一个Elasticsearch服务器实例称为一个node，node是集群的一部分，每个node有独立的名称，默认是启动时获取一个UUID作为名称，也可以自行配置，node名称特别重要，Elasticsearch集群是通过node名称进行管理和通信的，一个node只能加入一个Elasticsearch集群当中，集群提供完整的数据存储，索引和搜索的功能，它下面的每个node分摊上述功能（每条数据都会索引到node上）。shard分片，是单个Lucene索引，由于单台机器的存储容量是有限的（如1TB），而Elasticsearch索引的数据可能特别大（PB级别，并且30GB/天的写入量），单台机器无法存储全部数据，就需要将索引中的数据切分为多个shard，分布在多台服务器上存储。利用shard可以很好地进行横向扩展，存储更多数据，让搜索和分析等操作分布到多台服务器上去执行，提升集群整体的吞吐量和性能。shard在使用时比较简单，只需要在创建索引时指定shard的数量即可，剩下的都交给Elasticsearch来完成，只是创建索引时一旦指定shard数量，后期就不能再更改了。replica索引副本，完全拷贝shard的内容，shard与replica的关系可以是一对多，同一个shard可以有一个或多个replica，并且同一个shard下的replica数据完全一样，replica作为shard的数据拷贝，承担以下三个任务：shard故障或宕机时，其中一个replica可以升级成shard。replica保证数据不丢失（冗余机制），保证高可用。replica可以分担搜索请求，提升整个集群的吞吐量和性能。shard的全称叫primary shard，replica全称叫replica shard，primary shard数量在创建索引时指定，后期不能修改，replica shard后期可以修改。默认每个索引的primary shard值为5，replica shard值为1，含义是5个primary shard，5个replica shard，共10个shard。因此Elasticsearch最小的高可用配置是2台服务器。

## 查询
其中查询支持多种类型的复杂查询，如match解析查询、排序查询、分页查询、bool查询、fileter查询、多关键字查询、term精确查询、高亮查询

ElasticSearch使用倒排索引与Term Index来提高搜索效率，减少磁盘I/O。
ElasticSearch使用Skip List和Roaring Bitset来合并复杂条件查询的结果集。
https://zhuanlan.zhihu.com/p/646462877
## 客户端
Java High Level REST Client


{
  "_index": "test_index",
  "_type": "test_type",
  "_id": "1",
  "_version": 1,
  "found": true,
  "_source": {
    "test_content": "test test"
  }
}

链接：https://zhuanlan.zhihu.com/p/646647762

_id mysql中存在的唯一id，可以手动指定

## 学习资料
b站 
## books 书籍


Elasticsearch 技术解析与实战 作者: 朱林

[Elasticsearch源码解析与优化实战](https://book.douban.com/subject/30386800/)
张超 / 电子工业出版社 / 2019-1 /

[Elasticsearch实战与原理解析](https://book.douban.com/subject/35001679/)
牛冬 / 电子工业出版社 / 2020-3

[Elasticsearch搜索引擎构建入门与实战](https://book.douban.com/subject/35658411/)
高印会 / 机械工业出版社 / 2021-10

[Elasticsearch全面解析与实践](https://book.douban.com/subject/35702743/)
张文亮 / 机械工业出版社 / 2021-12-14 / 79.00

## Rust写的竞品 meilisearch

倒排索引

elasticsearch

https://book.douban.com/subject/25868239/

es其分布式设计理念和其他分布式Nosql数据库的设计理念都差不多
nosql

搜索，es

wukong搜索

订单表 优化

一共有20个field，分布在5个表中，现在要查询出完整的订单信息，如何做到接近实时查询

大公司的思路用ES建立索引，查询ES

例如，广州机房到北京机房，正常情况下 RTT 大约是 50 毫秒左右，遇到网络波动之类的情况，RTT 可能飙升到 500 毫秒甚至 1 秒，更不用说经常发生的线路丢包问题，那延迟可能就是几秒几十秒了。

nosql

## Windows电脑安装启动Elasticsearch

windows电脑安装了

cd F:\elasticsearch-7.3.2

.\bin\elasticsearch.bat

$env:JAVA_HOME = "F:\elasticsearch-7.3.2\jdk"

$env:Path = "F:\elasticsearch-7.3.2\jdk\bin;$env:Path"

F:\elasticsearch-7.3.2\bin\elasticsearch.bat

需要java11



http://127.0.0.1:9200/

http://127.0.0.1:9200/

{
  "name" : "DESKTOP-DAF8ST0",
  "cluster_name" : "elasticsearch",
  "cluster_uuid" : "IgkMeZyXQk2bmv4wbvgNpg",
  "version" : {
    "number" : "7.3.2",
    "build_flavor" : "default",
    "build_type" : "zip",
    "build_hash" : "1c1faf1",
    "build_date" : "2019-09-06T14:40:30.409026Z",
    "build_snapshot" : false,
    "lucene_version" : "8.1.0",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"
  },
  "tagline" : "You Know, for Search"
}

https://blog.csdn.net/qq_34383510/article/details/128132503



db-engines

search engine中排名



https://db-engines.com/en/ranking/search+engine



## Elasticsearch课程
Elasticsearch 核心技术与实战

https://time.geekbang.org/course/intro/100030501



快速构建分布式搜索和分析引擎

阮一鸣  eBay Pronto 平台技术负责人

Pronto 平台目前管理了 eBay 内部上百个 Elasticsearch 集群，包含了 4000 多个数据节点。这些集群目前被广泛使用在 eBay 的生产环境之中。涵盖了网站搜索，商品推荐，日志管理，风险控制，IT 运维，安全监控等多个领域。



![es学习路线](imgs/es_study.jpg)
