# hive

数据仓库
版本2
可以执行sql

它提供SQL类型语言查询叫HiveQL或HQL


debry
hddfs
hsql 分解为map reduce





Apache Hive（TM）数据仓库软件有助于使用SQL读取，写入和管理驻留在分布式存储中的大型数据集。建立在Apache Hadoop（TM）之上，它提供：
通过SQL轻松访问数据的工具，从而实现数据仓库任务，例如提取/转换/加载（ETL），报告和数据分析
一种将结构强加于各种数据格式的机制
访问直接存储在Apache HDFS（TM）或其他数据存储系统（例如Apache HBase（TM））中的文件
使用Apache Hadoop MapReduce，Apache Tez或Apache Spark框架执行查询。
Hive提供了标准的SQL功能，包括2003年和2011年以后的许多分析功能。其中包括OLAP函数，子查询，公用表表达式等。Hive的SQL也可以通过用户定义的函数（UDF），用户定义的集合（UDAF）和用户定义的表函数（UDTF）扩展为用户代码。
Hive用户在执行SQL查询时可以选择3种运行时。用户可以选择Apache Hadoop MapReduce，Apache Tez或Apache Spark框架作为执行后端。MapReduce是一个成熟的框架，已得到大规模验证。但是，MapReduce是纯粹的批处理框架，使用它的查询可能会遇到更高的延迟（数十秒），即使是在较小的数据集上也是如此。Apache Tez专为交互式查询而设计，与MapReduce相比，已大大减少了开销。Apache Spark是一个集群计算框架，建立在MapReduce之外，但在HDFS之上，具有可称为项目的可组合且可转换的分布式集合的概念，称为弹性分布式数据集（RDD），它无需MapReduce引入的传统中间阶段即可进行处理和分析。
用户可以随时在这些框架之间来回切换。在每种情况下，Hive都最适合处理的数据量足以需要分布式系统的用例。
Hive不适用于在线交易处理。最好用于传统的数据仓库任务。Hive旨在最大程度地提高可扩展性（通过向Hadoop集群动态添加更多计算机来进行横向扩展），性能，可扩展性，容错以及输入格式的松散耦合。
