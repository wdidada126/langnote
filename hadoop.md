# hadoop

## 版本

release-3.3.6
rel/release-3.3.3
rel/release-3.2.4
rel/release-3.3.2 2022
release-3.3.1   2021

## 源代码托管地址
https://github.com/apache/hadoop
For the latest information about Hadoop, please visit our website at:

   http://hadoop.apache.org/

and our wiki, at:

   https://cwiki.apache.org/confluence/display/HADOOP/

### 集群部署
基于Docker快速搭建多节点Hadoop集群
https://dockone.io/article/8868

Hadoop 是一个分布式系统基础架构，由Apache基金会开发。用户可以在不了解分布式底层细节的情况下，开发分布式程序。充分利用集群的威力高速运算和存储。

## HDFS
Hadoop实现了一个分布式文件系统（Hadoop Distributed File System），简称HDFS。HDFS有着高容错性的特点，并且设计用来部署在低廉的（low-cost）硬件上。而且它提供高传输率（high throughput）来访问应用程序的数据，适合那些有着超大数据集（large data set）的应用程序。HDFS放宽了（relax）POSIX的要求（requirements）这样可以流的形式访问（streaming access）文件系统中的数据。

hadoop

百度C++自研，后来用hadoop

## hadoop商业级产品

Hortonworks 免费
HDP, CDH.
Hortonwork Hadoop 与 Cloudera Hadoop 是两大 Hadoop 实施商。
Cloudera 是老牌的 Hadoop 供应商，除了定制化的 Hadoop 还提供培训以及支持。
Hortonworks 是新兴的 Hadoop 供应商，与 Cloudear 最大的不同，他是免费的。但同样也提供培训与支持，培训与支持是收费的。

hadoop 官网支支持linux
yarn
hdfs配置


## MapReduce算法
是的，Hadoop实现了MapReduce算法。MapReduce是一种计算模型，被广泛使用的开源大数据技术Hadoop实现了这种模型。在Hadoop的MapReduce实现中，输入和输出都是以key-value键值对的形式体现的。 MapReduce将复杂的、运行于大规模集群上的并行计算过程高度地抽象到了两个函数——Map和Reduce上，并且允许用户在不了解分布式系统底层细节地情况下开发并行应用程序，并将其运行于廉价计算机集群上，完成海量数据地处理。