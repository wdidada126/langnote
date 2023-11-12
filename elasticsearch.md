# elasticsearch


## 官方文档

es文档
https://www.elastic.co/guide/en/elasticsearch/reference/7.17/index.html

## analysis-ik分词器

ik版本必须跟es版本一致

./bin/elasticsearch-plugin install https://github.com/medcl/elasticsearch-analysis-ik/releases/download/v2.3.0/elasticsearch-analysis-ik-2.3.0.zip

https://github.com/medcl/elasticsearch-analysis-ik/releases?page=14

https://github.com/medcl/elasticsearch-analysis-ik/releases/download/v7.9.2/elasticsearch-analysis-ik-7.9.2.zip

## 核心概念

文档 document

item

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
