# spark
Spark的版本和Scala语言版本、Hadoop版本以及Hive都有对应关系。在运行Spark程序时，需要特别注意这些对应关系，否则可能会出现不兼容的错误。

例如，Hadoop 3.1.3可以与Spark 2.4.x或Spark 3.x版本兼容。具体来说，如果你想要在Hadoop 3.1.3上运行Spark，你可以选择以下其中一种组合：Spark 2.4.x + Hadoop 3.1.x或者Spark 3.x + Hadoop 3.1.x。此外，Spark运行在Java 8 +，Python 2.7 + / 3.4 +和R 3.1+上。对于Scala API，比如Spark 2.4.3使用Scala 2.12，因此你需要使用兼容的Scala版本（2.12.x）。

同时，虽然Spark和Hive本质上是没有关系的，两者可以互不依赖。但是在企业实际应用中，经常把二者结合起来使用，主要有hive on spark等方式。

## 书籍

scala编程语言写的
商业版有用c++写的，Photon
Spark的作者们自己重写了一个C++版本的Spark SQL，取名为photon。比原来的Spark SQL快，并且，这是一个闭源项目。
[building-spark](https://spark.apache.org/docs/latest/building-spark.html)

flink

取代hadoop中的MapReduce，继续用hadoop中的yarn，hdfs

拉钩教育有相关课程

kafka

spark只支持linux部署吗？
spark强依赖hadoop

https://archive.apache.org/dist/spark/spark-3.2.4/spark-3.2.4-bin-hadoop3.2.tgz
