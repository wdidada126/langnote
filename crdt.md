# crdt

分布式领域的理论

Conflict-free Replicated Data Types

无冲突复制数据类型



crdt理论详细说明

http://www.codeorg.cn/article/detail/architect/1184



Riak是CRDT最受欢迎的开源库

https://qa.1r1g.com/sf/ask/2393459841/



Riak

https://github.com/basho/riak



Riak是以 Erlang 编写的一个高度可扩展的分布式数据存储，Riak的实现是基于Amazon的[Dynamo](http://www.oschina.net/p/dynamo)论文，Riak的设计目标之一就是高可用。Riak支持多节点构建的系统，每次读写请求不需要集群内所有节点参与也能胜任。提供一个灵活的 map/reduce 引擎，一个友好的 HTTP/JSON 查询接口。

Riak 非常易于部署和扩展。可以无缝地向群集添加额外的节点。link walking 之类的特性以及对 Map/Reduce 的支持允许实现更加复杂的查询。除了 HTTP API 外，Riak 还提供了一个原生 Erlang API 以及对 Protocol Buffer 的支持。

目前有三种方式可以访问 Riak：HTTP API（RESTful 界面）、Protocol Buffers 和一个原生 Erlang 界面。提供多个界面使您能够选择如何集成应用程序。如果您使用 Erlang 编写应用程序，那么应当使用原生的 Erlang 界面，这样就可以将二者紧密地集成在一起。其他一些因素也会影响界面的选择，比如性能。例如，使用 Protocol Buffers 界面的客户端的性能要比使用 HTTP API 的客户端性能更高一些；从性能方面讲，数据通信量变小，解析所有这些 HTTP 标头的开销相对更高。然而，使用 HTTP API 的优点是，如今的大部分开发人员（特别是 Web 开发人员）非常熟悉 RESTful 界面，再加上大多数编程语言都有内置的原语，支持通过 HTTP 请求资源，例如，打开一个 URL，因此不需要额外的软件。在本文中，我们将重点介绍 HTTP API。









DOI：

10.1007/978-3-642-24550-3_29

Conflict-Free_Replicated_Data_Types.pdf





Using Erlang, Riak and the ORSWOT.pdf





工业界比较有名的包括Redis系统的企业版，提供CRDT支持，Riak中提供了CRDT支持



https://github.com/ljwagerfield/crdt



https://stackoverflow.com/questions/34192283/what-is-crdt-in-distributed-systems



https://www.tiny.cloud/blog/real-time-collaboration-ot-vs-crdt/





https://zhuanlan.zhihu.com/p/86256851



https://zhuanlan.zhihu.com/p/83298388



https://www.cnblogs.com/princessd8251/articles/6062219.html



https://github.com/RBMHTechnology/eventuate



http://m.myexception.cn/open-source/1610862.html



https://www.jishuwen.com/d/21dr



分布式领域的理论





Riak是一个分布式的key-value数据仓库。另外实现了一个Ejabberd CRDT library处理写冲突问题



CouchBase 2.0已经发布，构架和Riak十分相似，而且凭着couchDB的良好口碑，用CouchBase的人会越来越多。





