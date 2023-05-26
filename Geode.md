# Geode


Geode有以下几个方面超前于其它缓存解决方案的架构设计:
1. 分布式和嵌入式混合部署
Geode可以作为传统的分布式缓存集群运行,也可以作为嵌入式本地缓存直接在应用中使用。
这给开发者带来很高的灵活性。
2. 多种数据复制模式
Geode提供多种数据复制策略:全同步、部分同步、异步复制等。让用户根据需求配置最合适的数据一致性。
3. 多级缓存架构
Geode支持配置本地缓存和堆外缓存,形成多级缓存架构。可显著提高性能和吞吐量。
4. 丰富的资源管理特性
Geode提供丰富的资源管理和调度功能:镜像、全局锁、Lru/HeapLRU/FIFO等方式的资源拥有策略。
5. 健壮的集群组件
Geode的各个集群组件(server、locator、gateway等)设计得较为松耦合,同时功能强大。可构建高度可选择和可配置的集群。
6. 数据本地化
Geode支持数据的区域化和本地化,能很好地支撑地理分布式的数据访问。
7. 分布式查询
Geode还提供一种ODBC兼容的分布式查询语言(GQL),可以跨集群执行分布式查询。
以上各个方面都体现了Geode架构设计的先进性。
它可以小而美地作为快速嵌入式解决方案,也可以大而全地提供复杂的企业级分布式功能。这点相比于其它缓存产品有不错的前瞻性。

希望通过阐述Geode架构的几个重要特点,可以让您更好地理解其先进之处。如果仍有任何疑问,欢迎继续提问。


```shell
<!-- Apache Geode -->
		<dependency>
			<groupId>org.apache.geode</groupId>
			<artifactId>geode-core</artifactId>
			<version>${geode.version}</version>
        </dependency>
```


docker pull apachegeode/geode:1.14.1

docker run -itd --name geode -p 40404:40404 -p 10334:10334 -p 7070:7070 -p 8080:8080 apachegeode/geode:1.14.1


```shell
gfsh start server  --name=Server1
....
Server in C:\Users\admin\Server1 on JT121379[40404] as Server1 is currently online.
Process ID: 35860
Uptime: 5 seconds
Geode Version: 1.14.4
Java Version: 1.8.0_371
Log File: C:\Users\admin\Server1\Server1.log
JVM Arguments: -Dgemfire.start-dev-rest-api=false -Dgemfire.use-cluster-configuration=true -XX:OnOutOfMemoryError=taskkill /F /PID %p -Dgemfire.launcher.registerSignalHandlers=true -Djava.awt.headless=true -Dsun.rmi.dgc.server.gcInterval=9223372036854775806
Class-Path: D:\dev_tools\apache-geode-1.14.4\lib\geode-core-1.14.4.jar;D:\dev_tools\apache-geode-1.14.4\lib\geode-dependencies.jar
```


gfsh>connect
Connecting to Locator at [host=localhost, port=10334] ..
Connecting to Manager at [host=JT121379, port=1099] ..
Successfully connected to: [host=JT121379, port=1099]

You are connected to a cluster of version: 1.14.4









gfsh>list members
Member Count : 1

  Name   | Id
-------- | -----------------------------------------------------------------
Locator1 | 172.19.17.240(Locator1:17764:locator)<ec><v0>:41000 [Coordinator]


stop locator --name=Locator1

start locator --name=Locator1



stop server --name=Server1

Geode的server和locator有如下主要区别和联系:

区别:
1.  server负责缓存数据,提供数据访问服务。客户端通过与server交互来读取和修改数据。
2.  locator负责注册和查找集群中其他成员(server、其他locator)。locator不存储任何数据。

联系:
1. server和locator都是Geode集群的必需组件。一个集群至少需要一个locator和一个server。
2. server启动时需要连接到locator来加入集群。locator知道整个集群的成员信息。
3. locator负责注册和查找集群中其他成员。server通过locator可以找到其他server之间的通信路由。

作用:
1. server负责处理客户端的数据读写请求。实现集群的存储功能。
2. locator用来维护集群成员(server、locator)的注册表,实现成员发现和路由功能。

关系:
1. locator完全独立于server,不依赖于server也不存储任何数据。
2. server依赖locator来加入集群,并与集群中的其他server交互。

总的来说:
- locator提供注册表和路由服务,集群中的其他成员通过它来找到彼此
- server提供缓存服务和数据存储,与客户端交互处理数据访问请求
- locator和server通过注册表和路由功能协作,构成一个完整的Geode分布式缓存集群  

希望以上内容可以帮助您更好理解Geode中server和locator的作用以及它们之间的关联。如果仍有任何疑问,欢迎继续提问。




start server --name=Server1  --locators=localhost[10334] --cache-xml-file=cache.xml
create cache --name=exampleCache --type=partition


Apache Geode文档
https://wjw465150.github.io/GeodeUserGuide/Geode_1_Getting_Started_with_Apache_Geode.html


https://geode.apache.org/


https://twitter.com/apachegeode

建议了解一下Geode，是基于商业版本的GemFire内存数据网格完全开源出来的顶级产品，而GemFire作为具有数据库功能的IMDG已经有十几年的历史了，在美国金融行业几乎是随处可见。


https://geode.apache.org/

https://www.infoq.cn/article/introduction-of-apache-geode

http://github.com/apache/geode


Geode（原名GemFire）是一个分布式缓存系统，它可以在多个节点之间共享数据，并提供高可用性、高性能、可伸缩性和可靠性。Geode 最初是由 GemStone Systems 公司开发的，后来被 VMware 收购，现在是 Apache 基金会的一个开源项目。

Geode 的主要特点包括：

1. 数据分布和复制：Geode 可以将数据分布到多个节点，并在节点之间复制数据，从而提高数据的可用性和可靠性。
2. 高性能：Geode 使用内存作为主要的数据存储，可以提供非常高的读写性能。此外，Geode 还提供了许多优化技术，如数据压缩、数据预取等，可以进一步提高性能。
3. 可靠性：Geode 提供了多种故障恢复机制，可以保证数据的完整性和可靠性。例如，当一个节点失败时，Geode 可以自动将数据迁移到其他节点上，保证数据的可用性。
4. 可伸缩性：Geode 可以根据需要增加或减少节点，从而实现水平扩展和收缩。
5. 支持多种数据存储方式：Geode 支持多种数据存储方式，包括内存存储、磁盘存储和混合存储等，可以根据应用场景选择合适的存储方式。
6. 支持多种数据访问方式：Geode 支持多种数据访问方式，包括 Java API、REST API、SQL 等，可以根据应用场景选择合适的访问方式。
总之，Geode 是一个功能强大的分布式缓存系统，可以在多个节点之间共享数据，并提供高可用性、高性能、可伸缩性和可靠性。它被广泛用于各种大规模分布式应用场景，如金融、电信、电子商务等领域。


### 下载和版本

https://geode.apache.org/releases/

1.15



### gerde vs redis

Geode 和 Redis 都是广泛使用的分布式缓存系统，它们有一些相似之处，也有一些不同之处。

相似之处：
1. 都是分布式缓存系统，可以将数据存储在多个节点上，从而提高数据的可用性和可靠性。
2. 都支持多种数据结构和数据类型，如字符串、哈希、列表、集合等。
3. 都提供了高性能的读写操作，并支持事务和批量操作等高级功能。
4. 都可以通过主从复制和分片等方式实现数据的高可用性和可伸缩性。

不同之处：
1. 存储方式不同：Geode 使用内存作为主要的数据存储，可以提供非常高的读写性能；而 Redis 既可以使用内存作为数据存储，也可以使用磁盘作为数据存储。
2. 数据复制方式不同：Geode 使用多副本复制方式来保证数据的可用性和可靠性；而 Redis 使用主从复制方式来实现数据的高可用性。
3. 数据访问方式不同：Geode 提供了多种数据访问方式，如 Java API、REST API、SQL 等；而 Redis 主要使用 Redis 协议进行数据的访问。
4. 应用场景不同：Geode 主要用于大规模分布式应用场景，如金融、电信、电子商务等领域；而 Redis 更适用于高并发、高性能、低延迟的应用场景，如缓存、会话管理、排行榜等。
总之，Geode 和 Redis 都是优秀的分布式缓存系统，具有各自的特点和优势。在选择使用哪种系统时，应该根据具体的应用场景和需求进行选择。

For more information see the [Geode
Examples](https://github.com/apache/geode-examples) repository or the
[documentation](https://geode.apache.org/docs/).

