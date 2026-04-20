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
这是一个常见但需要精确辨析的观点。准确的说法是：

Apache Spark 可以独立运行，不强制依赖 Hadoop，但在生产环境的大数据生态中，它与 Hadoop 高度集成，形成了事实上的“强依赖”关系。

核心辨析：技术依赖 vs. 生态依赖

1. 技术层面：Spark 可以完全独立

Spark 的核心是一个分布式计算引擎，它自己可以管理集群资源（通过 Standalone 模式）和处理数据。它不依赖 Hadoop 的任何组件来完成其核心计算任务。

独立运行的最小需求：
• Spark 本身（核心、SQL、Streaming等模块）
• 一个集群资源管理器（可选用其自带的 Standalone Cluster Manager）
• 存储系统（可以是本地文件系统、NFS、或云存储如 S3）

例如，你可以直接在 Amazon S3 上运行 Spark 作业，完全绕过 Hadoop。
# 独立模式启动 Spark，读取本地文件
./bin/spark-submit \
  --master spark://your-master:7077 \
  --class com.example.MyApp \
  my-spark-app.jar \
  file:///path/to/input \
  file:///path/to/output


2. 生产环境层面：与 Hadoop 紧密耦合形成“事实强依赖”
尽管技术上解耦，但生产环境中 Spark 几乎总是与 Hadoop 生态一起部署，原因如下：
依赖层面 Hadoop 组件 作用与优势 替代方案（但少见）
资源管理 YARN 业界标准，高效管理多租户、多应用（Spark/MapReduce/等）共享集群资源 Spark Standalone, Mesos, Kubernetes
存储系统 HDFS 高容错、高吞吐的分布式文件系统，与本地计算亲和性好 云存储（S3, ADLS）, NFS, 本地文件系统
数据格式 Hive / Parquet / ORC 列式存储格式，与 Spark SQL 深度集成，优化分析查询 自定义格式，其他列式存储
集群监控 Hadoop 生态工具 成熟、集成度高，如通过 YARN UI 和 HDFS UI 监控 各自独立的监控系统

为什么形成这种生态依赖？
1.  历史路径：Spark 诞生时，Hadoop（MapReduce + HDFS）是大数据的事实标准。Spark 作为更快的替代计算引擎，自然选择与最大的生态集成。
2.  HDFS 的本地性优势：Spark 强调“内存计算”，但数据源常来自 HDFS。YARN 能调度 Spark 任务到存有数据的节点上，减少网络传输，这是关键性能优化。
3.  成熟的管理与运维：YARN 经过多年大规模生产验证，在资源隔离、队列管理、多租户支持上非常成熟，Spark Standalone 模式难以比拟。
4.  统一的数据湖：企业将 HDFS 作为中央数据湖，Spark 作为主要计算引擎去消费和产出数据，形成了经典架构。

典型部署架构对比

graph TD
    subgraph A [独立部署模式]
        A1[Spark Standalone Master] --> A2[Spark Worker Node];
        A2 --> A3[本地磁盘/S3/NFS];
    end

    subgraph B [Hadoop 集成模式 (主流)]
        B1[YARN Resource Manager] --> B2[Node Manager];
        B2 --> B3[Spark Executor];
        B3 --> B4[HDFS DataNode];
        B4 --> B5[本地磁盘];
    end

    style B fill:#e1f5e1


主流模式 (Hadoop集成)： NodeManager（YARN）、Executor（Spark）、DataNode（HDFS）三者常部署在同一节点，实现 “计算靠近存储”。

现代趋势：依赖关系正在松动

随着云原生和 Kubernetes的兴起，Spark对Hadoop的生态依赖正在发生变化：
1.  Spark on Kubernetes：成为官方支持的一等公民。越来越多的企业直接在 K8s 上运行 Spark，使用云存储（S3, ADLS, GCS），完全脱离 Hadoop。
2.  云原生数据湖：Delta Lake、Iceberg、Hudi 等表格格式，可以与对象存储（S3）直接配合，提供 ACID 事务，减少对 HDFS 的依赖。
3.  无服务器 Spark：如 Google Dataproc Serverless、AWS Glue Spark，用户完全不用管理集群，包括 Hadoop 集群。

结论与建议
1.  学习角度：初学者可以先独立学习 Spark（用本地模式或 Standalone），理解其 RDD、DataFrame API 和计算模型，而不必先深入 Hadoop。
2.  生产角度：在可预见的未来，尤其是在企业私有化部署中， “Spark on YARN + HDFS” 仍是主流、稳定、成熟的选择。你需要熟悉 Hadoop 生态。
3.  未来趋势：对于云上部署， “Spark on Kubernetes + 对象存储” 是明显的趋势，依赖关系正在重构。

最终回答：Spark 对 Hadoop 不是技术强依赖，而是生态强依赖和生产部署强依赖。你可以不用 Hadoop 运行 Spark，但在真实的大数据工作中，你几乎不可避免地需要与 Hadoop 生态打交道。

https://archive.apache.org/dist/spark/spark-3.2.4/spark-3.2.4-bin-hadoop3.2.tgz

## 应用
### 豆瓣
- DPark（豆瓣自研分布式计算）- Python 版 Spark，用于日志分析、用户行为、推荐算法、榜单计算。

wget https://archive.apache.org/dist/spark/spark-3.2.1/spark-3.2.1-bin-hadoop3.2.tgz
tar -zxvf spark-3.2.1-bin-hadoop3.2.tgz
mkdir -p /opt/spark/spark3_2
sudo mv spark-3.2.1-bin-hadoop3.2 /opt/spark/spark3_2
vi ~/.bashrc
export SPARK_HOME=/opt/spark/spark3_2/spark-3.2.1-bin-hadoop3.2
export PATH=$PATH:$SPARK_HOME/bin
source ~/.bashrc
spark-shell

启动 spark-shell 后，浏览器打开：
http://localhost:4040

Ubuntu 24 完全支持 Spark 3.2.1
不需要安装 Hadoop
不需要配置任何复杂文件
运行模式：本地单机模式（local [*]），适合学习、测试、开发

