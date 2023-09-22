# hadoop

## 版本

release-3.3.6
rel/release-3.3.3
rel/release-3.2.4
rel/release-3.3.2 2022
release-3.3.1 2021

## 源代码托管地址
https://github.com/apache/hadoop

For the latest information about Hadoop, please visit our website at:
http://hadoop.apache.org/

and our wiki, at:
https://cwiki.apache.org/confluence/display/HADOOP/

### 集群部署
基于Docker快速搭建多节点Hadoop集群
https://dockone.io/article/8868

Hadoop是一个分布式系统基础架构，由Apache基金会开发。用户可以在不了解分布式底层细节的情况下，开发分布式程序。充分利用集群的威力高速运算和存储。

## HDFS
Hadoop实现了一个分布式文件系统（Hadoop Distributed File System），简称HDFS。HDFS有着高容错性的特点，并且设计用来部署在低廉的（low-cost）硬件上。而且它提供高传输率（high throughput）来访问应用程序的数据，适合那些有着超大数据集（large data set）的应用程序。HDFS放宽了（relax）POSIX的要求（requirements）这样可以流的形式访问（streaming access）文件系统中的数据。

hadoop

百度C++自研，后来用hadoop

## hadoop商业级产品
Hortonworks免费
HDP,CDH.
Hortonwork Hadoop与Cloudera Hadoop是两大Hadoop实施商。
Cloudera是老牌的Hadoop供应商，除了定制化的Hadoop还提供培训以及支持。
Hortonworks是新兴的Hadoop供应商，与Cloudear最大的不同，他是免费的。但同样也提供培训与支持，培训与支持是收费的。

hadoop官网支支持linux
yarn
hdfs配置

## MapReduce算法
是的，Hadoop实现了MapReduce算法。MapReduce是一种计算模型，被广泛使用的开源大数据技术Hadoop实现了这种模型。在Hadoop的MapReduce实现中，输入和输出都是以key-value键值对的形式体现的。MapReduce将复杂的、运行于大规模集群上的并行计算过程高度地抽象到了两个函数——Map和Reduce上，并且允许用户在不了解分布式系统底层细节地情况下开发并行应用程序，并将其运行于廉价计算机集群上，完成海量数据地处理。

## 官方example

## Other Hadoop-related projects at Apache include:

Ambari™: A web-based tool for provisioning, managing, and monitoring Apache Hadoop clusters which includes support for Hadoop HDFS, Hadoop MapReduce, Hive, HCatalog, HBase, ZooKeeper, Oozie, Pig and Sqoop. Ambari also provides a dashboard for viewing cluster health such as heatmaps and ability to view MapReduce, Pig and Hive applications visually alongwith features to diagnose their performance characteristics in a user-friendly manner.
Avro™: A data serialization system.
Cassandra™: A scalable multi-master database with no single points of failure.
Chukwa™: A data collection system for managing large distributed systems.
HBase™: A scalable, distributed database that supports structured data storage for large tables.
Hive™: A data warehouse infrastructure that provides data summarization and ad hoc querying.
Mahout™: A Scalable machine learning and data mining library.
Ozone™: A scalable, redundant, and distributed object store for Hadoop.
Pig™: A high-level data-flow language and execution framework for parallel computation.
Spark™: A fast and general compute engine for Hadoop data. Spark provides a simple and expressive programming model that supports a wide range of applications, including ETL, machine learning, stream processing, and graph computation.
Submarine: A unified AI platform which allows engineers and data scientists to run Machine Learning and Deep Learning workload in distributed cluster.
Tez™: A generalized data-flow programming framework, built on Hadoop YARN, which provides a powerful and flexible engine to execute an arbitrary DAG of tasks to process data for both batch and interactive use-cases. Tez is being adopted by Hive™, Pig™ and other frameworks in the Hadoop ecosystem, and also by other commercial software (e.g. ETL tools), to replace Hadoop™ MapReduce as the underlying execution engine.
ZooKeeper™: A high-performance coordination service for distributed applications.
