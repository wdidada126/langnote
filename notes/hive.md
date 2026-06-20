# hive

hive元数据信息对应的MySQL数据库表.mhtml

Hadoop 分布式集群中安装 Hive（CentOS 7系统） 
https://www.cnblogs.com/liyihua/p/14482435.html


Hive架构及原理
https://zhuanlan.zhihu.com/p/346668930

hive的架构简介.jpg


软件版本
电脑系统：macOS 10.14.6
虚拟机软件：Parallels Desktop15
Hadoop各节点节点操作系统：CentOS-7-x86_64-Minimal-1908.iso
CentOS 7 JDK版本：jdk1.8.0_162
Hadoop版本：hadoop-2.7.7
Hive版本：hive-2.3.3
MySQL版本：mysql-5.7.30

Apache Hive 是基于 Hadoop 的一个数据仓库工具，可以将结构化的数据文件映射为一张数据库表，并提供简单的 SQL 查询功能，可以将 SQL 语句转换为MapReduce 任务进行运行。其优点是学习成本低，可以通过类 SQL 语句快速实现简单的 MapReduce 统计，不必开发专门的 MapReduce 应用，十分适合数据仓库的统计分析。

hive基于hbase？
Hive可以使用HBase作为存储介质，即HBase可以作为Hive的表存储数据。此外，Hive和HBase也可以整合起来，使得在HBase表上使用HQL语句进行查询、插入操作变得可行，同时也可以进行Join和Union等复杂查询。因此，Hive不完全基于HBase。


在CentOS平台上搭建Hive集群需要进行以下步骤：
安装Hadoop：首先需要在CentOS上安装Hadoop，并确保其能够正常运行。可以参考Hadoop官方文档或在线教程进行安装和配置。
安装MySQL：Hive需要使用MySQL作为元数据存储，因此需要在CentOS上安装MySQL数据库。可以参考MySQL官方文档或在线教程进行安装和配置。
下载并解压Hive：从Apache Hive官方网站下载Hive安装包，并将其解压到合适的目录。
配置Hive：进入Hive的conf目录，修改hive-site.xml文件，添加以下内容：
```xml
<property>  
  <name>javax.jdo.option.ConnectionURL</name>  
  <value>jdbc:mysql://localhost/hive?createDatabaseIfNotExist=true</value>  
  <description>JDBC connect string for a JDBC metastore</description>  
</property>  
  
<property>  
  <name>javax.jdo.option.ConnectionDriverName</name>  
  <value>com.mysql.jdbc.Driver</value>  
  <description>Driver class name for a JDBC metastore</description>  
</property>  
  
<property>  
  <name>javax.jdo.option.ConnectionUserName</name>  
  <value>hive</value>  
  <description>username to use against metastore database</description>  
</property>  
  
<property>  
  <name>javax.jdo.option.ConnectionPassword</name>  
  <value>hive_password</value>  
  <description>password to use against metastore database</description>  
</property>
```
注意将localhost替换为MySQL所在的主机名或IP地址，将hive替换为MySQL中创建的Hive数据库的用户名，将hive_password替换为对应的密码。
5. 配置环境变量：编辑/etc/profile文件，添加以下内容：

```bash
export HIVE_HOME=/path/to/hive  
export PATH=$PATH:$HIVE_HOME/bin
```
注意将/path/to/hive替换为实际解压后的Hive目录。
6. 启动Hive：在终端运行hive命令启动Hive。如果一切配置正确，应该可以成功启动并进入Hive的命令行界面。
集群配置：如果要搭建Hive集群，还需要进行额外的配置。可以参考Hive官方文档或在线教程进行集群配置。主要的配置包括指定Hadoop集群的主节点、配置Hive Metastore服务、配置HiveServer2服务等。
以上是在CentOS平台上搭建Hive集群的基本步骤。在实际操作中，还需要注意一些细节和常见问题，例如防火墙设置、端口冲突等。可以参考官方文档和在线教程解决这些问题。

hive搭建
https://www.bilibili.com/read/cv7220228/
https://github.com/big-data-europe/docker-hive
https://www.cnblogs.com/reasonzzy/p/11127359.html
https://www.bilibili.com/read/cv7220228/

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
