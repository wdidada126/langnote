# Hekaton

并发控制协议_2PL_TS_OCC.mhtml


在关系型数据库系统（RDBMS）中，索引是一个重要组成部分，其主要作用是提升查询性能，侧重OLTP的关系型数据库常用的索引大致可以分为两大类：
基于树（tree-based）的B-tree索引。B-tree索引（这里B-tree代表B+-tree）适合以块或者页为单位的存储，支持高效的点查询（point query）和范围查询（range query），在数据库中已经广泛使用。
基于哈希(hash-based)的哈希索引。哈希索引更适合建在内存中，仅支持点查询，更多使用于内存数据库中，如MS SQL Server Hekaton, SAP ASE In Memory Row Store等。
http://mysql.taobao.org/monthly/2020/05/02/


数据库引擎Hekaton
日前，微软首度在台揭露SQL Server 2014预览版，新版最重要的特色是新增了线上交易（OLTP）数据处理引擎Hekaton（在希腊文里，是一百倍的意思），至少能提升10倍数据处理性能。是微软研究院5年前对产品部门发表研究成果的专案名称，SQL Server 2014预览版本数据处理效能至少可以提升10倍的关键，就是采用了命名为Hekaton技术。

跟spark 和impala 比怎么样呢


