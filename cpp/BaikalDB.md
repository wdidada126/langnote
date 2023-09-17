# BaikalDB

https://github.com/baidu/BaikalDB

Baidu的HTAP数据库BaikalDB
https://www.oschina.net/p/BaikalDB

BaikalDB是一个分布式可扩展的存储系统，支持PB级结构化数据的随机实时读写。
提供MySQL接口，支持常用的SELECT，UPDATE，INSERT，DELETE语法。提供各种WHERE过滤、GROUP BY聚合，HAVING过滤，ORDER BY排序等功能，用户可以组合实现各种在线OLAP需求，具备秒级别的亿级数据扫描聚合能力。另外，为了满足各种业务的检索需求，该系统内置全文检索需求，满足大部分快速检索的业务场景。
在虚拟化部署方面，该系统采用share-nothing的架构，可部署在容器中，也实现了多租户隔离，有自定义用户的身份识别和权限访问控制等功能。

BaikalDB的主要特性如下：
全自主化的容量管理，可以自动扩容和自动数据均衡，支持自动故障迁移，无单点，很容易实现云化，目前运行在Paas虚拟化平台之上。
面向查询优化，支持各种二级索引，包括全文索引，支持常用的OLAP需求，支持层级模型。
兼容mysql协议，对应用方提供SQL界面，支持高性能的Schema加列。
基于RocksDB实现单机存储，基于Multi Raft协议（我们使用braft库）保障副本数据一致性，基于brpc实现节点通讯交互。
支持多租户，meta信息共享，数据存储完全隔离。

BaikalStore负责数据存储，用region组织，三个Store的三个region形成一个Raft group实现三副本，多实例部署，Store实例宕机可以自动迁移Region数据。
BaikalMeta负责元信息管理，包括分区，容量，权限，均衡等，Raft保障的3副本部署，Meta宕机只影响数据无法扩容迁移，不影响数据读写。
BaikaDB负责前端SQL解析，查询计划生成执行，无状态全同构多实例部署，宕机实例数不超过qps承载极限即可。