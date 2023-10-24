# PrestoDB

针对大数据的分布式查询引擎

Presto是Facebook开源的MPP（Massive Parallel Processing）SQL引擎，其理念来源于一个叫Volcano的并行数据库，该数据库提出了一个并行执行SQL的模型，它被设计为用来专门进行高速、实时的数据分析。Presto是一个SQL计算引擎，分离计算层和存储层，其不存储数据，通过Connector SPI实现对各种数据源（Storage）的访问。

Presto的企业实践-滴滴-知乎.mhtml