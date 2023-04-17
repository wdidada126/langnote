# mi note




MySQL中，DATETIME和TIMESTAMP都可以用来表示日期和时间。它们的区别在于存储和使用方式不同：
DATETIME：用于存储日期和时间，占用8个字节的存储空间，范围从1000-01-01 00:00:00到9999-12-31 23:59:59，精确到秒。
TIMESTAMP：用于存储日期和时间，占用4个字节的存储空间，范围从1970-01-01 00:00:01到2038年某一时刻，精确到秒。与DATETIME不同的是，TIMESTAMP存储的值会随着时区变化而变化，因此其值不是一个确定的时间点。
在使用方面，DATETIME和TIMESTAMP也有一些区别：
当插入一条记录时，如果某个字段使用了TIMESTAMP类型，则其默认值为当前时间，而如果使用DATETIME类型，则默认值为NULL。
如果想要在表中使用自动更新时间戳功能，可以将TIMESTAMP类型字段的默认值设置为CURRENT_TIMESTAMP，每次插入或更新记录时都会自动更新该字段的值。而DATETIME类型字段没有自动更新时间戳的功能。
TIMESTAMP类型的数据存储和传输更加高效，占用空间更小，因此在需要大量存储时间戳的场景下，建议使用TIMESTAMP类型。但是需要注意的是，由于TIMESTAMP类型存储的值受时区影响，因此在进行跨时区的数据操作时需要特别注意。



MySQL 5.7 支持的表字段类型如下：

数值类型
TINYINT: -128 到 127，有符号。
SMALLINT: -32768 到 32767，有符号。
MEDIUMINT: -8388608 到 8388607，有符号。
INT: -2147483648 到 2147483647，有符号。
BIGINT: -9223372036854775808 到 9223372036854775807，有符号。
FLOAT: 单精度浮点数。
DOUBLE: 双精度浮点数。
DECIMAL: 用于精确数值计算的任意精度数字。
日期和时间类型
DATE: 日期值，格式为 'YYYY-MM-DD'。
TIME: 时间值，格式为 'HH:MM:SS'。
DATETIME: 日期和时间值，格式为 'YYYY-MM-DD HH:MM:SS'。
TIMESTAMP: 时间戳，格式为 'YYYY-MM-DD HH:MM:SS'。默认值为当前时间戳。
字符串类型
CHAR: 固定长度字符串，最多 255 字节。
VARCHAR: 可变长度字符串，最多 65535 字节。
TINYTEXT: 短文本字符串，最多 255 字节。
TEXT: 文本字符串，最多 65535 字节。
MEDIUMTEXT: 中等长度文本字符串，最多 16777215 字节。
LONGTEXT: 长文本字符串，最多 4294967295 字节。
ENUM: 枚举类型，存储从一个列表中选择的值。
SET: 集合类型，存储一个列表中的零个或多个选择值。
二进制类型
BINARY: 固定长度二进制字符串，最多 255 字节。
VARBINARY: 可变长度二进制字符串，最多 65535 字节。
TINYBLOB: 短二进制字符串，最多 255 字节。
BLOB: 二进制字符串，最多 65535 字节。
MEDIUMBLOB: 中等长度二进制字符串，最多 16777215 字节。
LONGBLOB: 长二进制字符串，最多 4294967295 字节。
对于不同的数据类型，其默认值也不同。例如，整数类型的默认值为 0，字符串类型的默认值为 NULL。如果在创建表时没有指定默认值，则使用对应类型的默认值。


MySQL 5.7及以上版本支持JSON数据类型，可以在表中定义JSON类型的列。JSON类型的列可以存储JSON格式的数据，包括JSON对象、数组、字符串、数字、布尔值和null。

在MySQL中，可以使用以下函数来处理JSON类型的列：

JSON_EXTRACT：从JSON数据中提取指定路径的数据
JSON_ARRAY：创建JSON数组
JSON_OBJECT：创建JSON对象
JSON_ARRAY_APPEND：向JSON数组末尾添加数据
JSON_ARRAY_INSERT：向JSON数组指定位置插入数据
JSON_OBJECT_APPEND：向JSON对象添加数据
JSON_OBJECT_INSERT：向JSON对象指定位置插入数据
JSON_CONTAINS：判断JSON数据是否包含指定的值
JSON_CONTAINS_PATH：判断JSON数据是否包含指定的路径
JSON_KEYS：获取JSON数据的所有键
JSON_LENGTH：获取JSON数据的长度
MySQL 8.0版本进一步增强了JSON的支持，提供了更多的函数和操作符，例如：

JSON_TABLE：将JSON数据转换成关系型数据
JSON_MODIFY：修改JSON数据中指定路径的值
JSON_MERGE_PATCH：合并两个JSON对象
->、->>、JSON_ARRAYAGG等操作符：方便地处理JSON数据。







Oracle 12c 支持以下列数据类型：

CHAR(n)：定长字符串，最多存储 n 个字符。
VARCHAR2(n)：变长字符串，最多存储 n 个字符。
NUMBER(p, s)：定点数，p 表示数字总位数，s 表示小数位数。
FLOAT(p)：浮点数，p 表示数字总位数。
DATE：日期类型。
TIMESTAMP：日期和时间类型。
INTERVAL YEAR TO MONTH：表示两个日期之间的年和月数。
INTERVAL DAY TO SECOND：表示两个日期之间的天、小时、分钟和秒数。
RAW(n)：二进制数据类型，最多存储 n 个字节。
LONG RAW：长二进制数据类型，最多存储 2GB 的二进制数据。
BLOB：二进制大对象类型，用于存储大的二进制数据。
CLOB：字符大对象类型，用于存储大的文本数据。
NCLOB：国际化字符大对象类型，用于存储大的国际化文本数据。
XMLType：用于存储 XML 数据。
默认值取决于具体的数据类型，例如：
CHAR(n) 的默认值是一个由空格组成的 n 个字符的字符串。
VARCHAR2(n) 的默认值是 NULL。
NUMBER 的默认值是 0。
DATE 的默认值是当前日期和时间。
BLOB、CLOB、NCLOB、XMLType 的默认值是 NULL。

















计算内部收益率（IRR）可以使用许多Java库。以下是几个常用的Java库，您可以根据您的需要选择其中之一：

Apache Commons Math：这是一个流行的Java数学库，提供了许多数学算法和工具，包括IRR的计算。
JQuantLib：这是一个基于QuantLib的Java金融库，提供了许多金融计算工具和算法，包括IRR、NPV等。
Jama：这是一个纯Java矩阵库，提供了矩阵计算和线性代数的工具，包括IRR的计算。
Colt：这是一个高性能的Java数值计算库，提供了许多数学和统计算法的实现，包括IRR的计算。
Apfloat：这是一个用于高精度浮点数计算的Java库，可以用于计算较复杂的金融计算，包括IRR。
这些库都是免费开源的，可以通过Maven等工具方便地集成到您的Java项目中。您可以根据您的需求和偏好选择其中的任意一个。

















银行的IT核心系统架构图可能因银行规模和业务特点而异，但一般而言，银行的IT核心系统架构图应包含以下组件：

前端系统：包括网银、手机银行、ATM等，提供给客户进行交易、查询、管理等操作的界面和渠道。
核心系统：包括账户管理、支付结算、信贷管理、风险控制等，是银行各项业务的核心处理系统。
数据库系统：用于存储银行业务数据，包括账户信息、交易记录、客户信息、统计报表等。
网络与通信系统：用于处理银行各种业务的网络和通信设施，如交易通道、数据传输线路、安全加密技术等。
业务应用系统：为银行提供特定业务的支持，如证券交易系统、外汇交易系统、贷款管理系统等。
安全系统：包括身份认证、访问控制、数据加密、防火墙等，用于保护银行业务和客户数据的安全。
监控与管理系统：用于监控银行系统运行状态和业务流程，包括性能监控、错误日志、告警处理等。
以上是一个比较常见的银行IT核心系统架构图，不同银行在实际实现中可能会有所差异。



是的，MySQL数据库支持schema模式，它与数据库实例相关联，并提供了一种在数据库中对表进行分组的方式。在MySQL中，schema与database是等价的，两者可以互换使用。一个数据库实例可以包含多个schema，每个schema可以包含多个表。
在MySQL中，使用CREATE SCHEMA语句可以创建一个新的schema。例如，创建一个名为test的schema：




在C++中连接和操作MySQL数据库，可以使用多种MySQL库，例如：
MySQL Connector/C++：官方提供的C++库，支持MySQL服务器的所有功能，包括事务、存储过程、预处理语句、批量插入等等。
MySQL++：一个开源的C++库，提供了简单的接口，支持常见的数据库操作，例如查询、插入、更新、删除等等。
SOCI：一个轻量级的C++库，提供了统一的接口，支持多种数据库，包括MySQL、SQLite、Oracle等等。



OCI（Oracle Call Interface）是Oracle提供的用于访问Oracle数据库的C语言API。OCI工具包括OCI库和OCI头文件。


这个说法是不准确的。Redis支持全量复制和增量复制两种方式。
在Redis 2.8版本之前，Redis只支持全量复制，即Slave节点在复制Master节点时需要将Master的所有数据全部复制一遍，对于大数据集而言，这种方式显然效率很低，会导致复制期间网络传输占用过多，同时可能还会因为复制期间的网络抖动而导致复制失败。但是从Redis 2.8版本开始，Redis引入了部分重同步（Partial Resynchronization）的机制，从而支持了增量复制。
部分重同步是指Slave节点在复制Master节点时，可以只复制Master节点在上次同步之后的变更数据。具体实现方式是：Slave节点会记录上次同步时的偏移量（offset）和复制时的当前偏移量，然后在复制数据时，只复制偏移量之后的变更数据。
需要注意的是，增量复制也有一些限制，例如：在进行增量复制时，如果Master节点在同步期间发生了重启或崩溃，那么就需要重新进行全量复制了。
部分重同步（Partial Resynchronization）的机制设置
Redis的部分重同步机制可以通过min-slaves-to-write和min-slaves-max-lag参数来设置。
min-slaves-to-write参数表示至少需要有多少个从节点在线，主节点才会执行写操作。默认值为0，表示不进行从节点个数的限制。
min-slaves-max-lag参数表示从节点的复制偏差值（复制的延迟）不能超过主节点的多少倍。默认值为10，表示从节点的复制偏差值不能超过主节点的10倍。如果从节点的复制偏差值超过了这个阈值，则主节点不会再将数据同步给这个从节点。可以通过设置该参数的值来调整部分重同步机制的敏感度。
这两个参数可以根据实际情况进行调整，以达到适合自己的复制策略。需要注意的是，部分重同步机制只适用于旧版的Redis，而在新版的Redis中已经被废弃了。新版的Redis使用复制积压缓冲区（Replication Backlog）机制来实现主从节点的同步。







什么是Kafka？它的主要特点是什么？
Kafka是一个分布式流媒体平台，主要特点包括：

高性能：Kafka通过分布式、分区和批量发送等方式提高了消息处理的性能。
可扩展性：Kafka的分布式架构允许它水平扩展，可以轻松地添加或移除服务器节点。
可靠性：Kafka提供了消息的持久化和副本机制，确保消息不会丢失。
支持流处理：Kafka可以处理流式数据，支持实时流式处理和流式处理分析。
Kafka如何保证高可靠性？
Kafka通过以下方式保证高可靠性：

消息持久化：Kafka将消息存储到磁盘上，确保消息即使在服务器出现故障时也不会丢失。
副本机制：Kafka支持多副本机制，确保即使其中一个broker宕机，消息也不会丢失。
重试机制：Kafka提供了重试机制，确保消息发送失败时可以重新发送。
可扩展性：Kafka可以水平扩展，可以轻松地添加或移除服务器节点，提高了系统的可靠性。
Kafka的主要组件有哪些？
Kafka的主要组件包括：

Producer：生产者，负责向Kafka集群发送消息。
Consumer：消费者，负责从Kafka集群中消费消息。
Broker：消息服务器，存储和处理消息。
Topic：消息主题，将消息按照一定的规则进行分类。
Partition：消息分区，将每个Topic分成多个Partition，提高并发处理能力。
Offset：消息偏移量，用于标识Consumer已经消费了哪些消息。
ZooKeeper：Kafka依赖于ZooKeeper实现分布式协调和管理。
Kafka的消费模式有哪些？
Kafka的消费模式包括以下两种：

Pull模式：消费者从Kafka中主动拉取消息，可以控制消费速率，适合于处理大量消息的场景。
Push模式：Kafka主动将消息推送给消费者，实时性较高，适合于处理实时消息的场景。




rocketmq比如支持主从模式和双写模式，保证消息的可靠性和高可用性。


Collector：表示一个归约器，用于将 Stream 中的元素归约为一个结果。

Comparator：表示一个比较器，用于对 Stream 中的元素进行排序。

kafka produce如何保证消息有序

Kafka Producer默认会将消息发送到同一个分区中，但是不会保证消息的顺序。如果要保证消息的有序性，需要使用自定义分区器，并在分区器中实现业务逻辑，保证同一业务相关的消息被发送到同一个分区中。

具体实现时，可以在消息体中添加业务相关的唯一标识符，例如订单ID，然后在自定义分区器中根据这个标识符计算分区号，保证相同的标识符的消息被发送到同一个分区中，从而实现有序性。

需要注意的是，Kafka Producer在保证有序性的同时，也会对性能产生影响，因为相同的分区只能由一个Producer线程写入。如果业务场景允许，可以使用多个分区来提高性能，但需要确保业务处理时不会出现分区间的依赖关系，从而保证整体有序性。



拜占庭问题

统一号令

在存在消息丢失的不可靠信道上试图通过消息传递的方式达到一致性是不可能的。

k8s部署spring boot项目，feign只配置name如何找到http server ip

在Kubernetes中，您可以使用Kubernetes Service对象作为Feign客户端请求的目标。通过使用Kubernetes Service对象，您可以将HTTP请求路由到适当的Pod，而无需知道Pod的IP地址和端口号。
具体来说，您可以按照以下步骤在Kubernetes中部署Spring Boot应用程序和Feign客户端：
部署Spring Boot应用程序
使用Kubernetes部署您的Spring Boot应用程序，并创建一个Service对象来暴露应用程序的Pod。



Katacoda是一种在线教育平台，提供Kubernetes和其他技术的学习环境。您可以在Katacoda上创建一个虚拟Kubernetes集群，并在其中练习Kubernetes操作和部署应用程序。














如何保证分布式一致性

2pc 3pc tcc

Paxos  分主次结点的。分类的思想 palc四个抽象的概念 主节点选举和数据同步

Raft

分布式hash？

分布式id


k8s常用版本


Kubernetes 的发展非常迅速，目前有许多不同的版本和发行版可供选择。以下是一些常见的 Kubernetes 版本：
Kubernetes v1.22：当前的稳定版本，支持 IPv6、Pod 网络代理等新特性，增强了安全性和可靠性。
Kubernetes v1.21：2021年4月发布的版本，引入了 KubeEdge 和 KubeArmor 等新特性，增强了多租户和安全性等方面。
Kubernetes v1.20：2020年12月发布的版本，引入了 Volume Snapshot 和 Volume Cloning 等新特性，增强了存储和管理方面。
Kubernetes v1.19：2020年8月发布的版本，引入了 PodSecurityPolicy 默认禁用和 IngressClass 等新特性，增强了安全性和网络方面。
此外，还有一些 Kubernetes 的发行版可供选择，例如：
Red Hat OpenShift：基于 Kubernetes 的企业级容器平台，提供了多种工具和服务来简化 Kubernetes 的使用和管理。
Rancher：基于 Kubernetes 的容器管理平台，提供了多种工具和服务来简化 Kubernetes 的部署、管理和监控。
Canonical Kubernetes：Ubuntu 官方提供的 Kubernetes 发行版，支持多云部署和自动化管理等功能。
Alibaba Cloud ACK：阿里云提供的 Kubernetes 服务，提供了多种工具和服务来简化 Kubernetes 的部署和管理。
总的来说，选择哪个版本或发行版取决于您的具体需求和使用场景，您需要考虑功能、性能、安全性、易用性等方面。



k8s deploy service区别


在 Kubernetes 中，Deployment 和 Service 是两个不同的资源对象，它们分别用于不同的目的。
Deployment 是一种资源对象，用于在 Kubernetes 集群上部署应用程序或服务。它提供了声明式方式来定义应用程序的期望状态，并确保在任何时候该状态都能得到满足。Deployment 通过创建和管理 Pod 对象来实现应用程序的部署。
Service 也是一种资源对象，用于公开应用程序或服务，使得其他应用程序或服务可以访问它们。Service 提供了一种抽象层，可以将多个 Pod 组合在一起，并使用负载均衡算法将流量分发到这些 Pod 上。这样，即使 Pod 发生变化，Service 也能确保对外提供的服务仍然是可用的。
Deployment 和 Service 之间的区别在于它们的作用和职责不同。Deployment 负责管理应用程序的部署和更新，而 Service 负责公开应用程序或服务，并提供一种负载均衡机制。通常情况下，您需要先创建一个 Deployment 对象来部署应用程序，然后再创建一个 Service 对象来将其公开，并使其他应用程序或服务可以访问它。




vue打包文件部署到nginx





Nginx是一个高性能的开源Web服务器和反向代理服务器。它的主要用途包括：

Web服务器：Nginx可以作为一个独立的Web服务器，用于处理静态资源（如HTML、CSS、JavaScript文件等）和动态请求（如CGI脚本、PHP脚本等）。

反向代理服务器：Nginx可以作为反向代理服务器，将客户端的请求转发到后端服务器（如Apache、Tomcat等）处理，并将处理结果返回给客户端。反向代理服务器可以提高应用程序的可扩展性和可靠性，以及提供负载均衡、缓存、SSL终止等功能。

负载均衡器：Nginx可以作为负载均衡器，将客户端的请求均匀地分配给多个后端服务器，以提高应用程序的性能和可扩展性。

静态文件服务器：Nginx可以作为一个高性能的静态文件服务器，处理静态资源请求。

安全策略：Nginx可以作为一个反向代理服务器，通过限制请求速率、防止DDoS攻击等手段提高应用程序的安全性。

HTTP缓存：Nginx可以作为一个缓存服务器，将动态请求的响应缓存到内存或磁盘中，以提高应用程序的性能。

总之，Nginx是一个功能强大的Web服务器和反向代理服务器，可以为应用程序提供高性能、高可用性和高安全性的支持。



用大型系统优化的经验

去做it系统优化

计算机网络 顶会

行业头部公司









Ai Python

https://www.zhihu.com/question/56055999







