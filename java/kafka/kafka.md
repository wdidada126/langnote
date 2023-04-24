# kafka



kafka stream



- 深入理解Kafka与Pulsar
- Kafka权威指南（第2版）



主题 topic

分区



message是分区内有序



broker，发布消息的中心点

broker是kafka集群中的一个节点



### kafka配置项



acks 定义了集群中多少个broker确认才能确定消息写入是成功的



### kafka可执行程序



xxx.sh --topic 



Kafka Stream是Apache Kafka从0.10版本引入的一个新Feature。它是提供了对存储于Kafka内的数据进行流式处理和分析的功能。

Kafka Stream的特点如下：

- Kafka Stream提供了一个非常简单而轻量的Library，它可以非常方便地嵌入任意Java应用中，也可以任意方式打包和部署
- 除了Kafka外，无任何外部依赖
- 充分利用Kafka分区机制实现水平扩展和顺序性保证
- 通过可容错的state store实现高效的状态操作（如windowed join和aggregation）
- 支持正好一次处理语义
- 提供记录级的处理能力，从而实现毫秒级的低延迟
- 支持基于事件时间的窗口操作，并且可处理晚到的数据（late arrival of records）
- 同时提供底层的处理原语Processor（类似于Storm的spout和bolt），以及高层抽象的DSL（类似于Spark的map/group/reduce）





[淘宝ONS(RocketMQ) vs kafa](http://blog.sina.com.cn/s/blog_693f08470102vjc7.html)



[MQ(消息队列)常见的应用场景解析](https://zhuanlan.zhihu.com/p/35998206)

#### MQ特点
1. 先进先出
2. 发布订阅
3. 持久化
4. 分布式

#### 应用场景

1. 应用解耦（异步）
2. 通知 一对一 一堆多
3. 限流 流量削峰
4. 数据分发
5. 分布式事务




LinkedIn三人小组离职创立Confluent，已获690万美元融资

11月7日消息，LinkedIn 有个三人小组出来创业了——正是当时开发出 Apache Kafka 实时信息列队技术的团队成员，基于这项技术 Jay Kreps 带头创立了新公司Confluent，致力于为各行各业的公司提供实时数处理服务解决方案，其他两位成员是 Neha Narkhede 和 Jun Rao。该公司已获 Benchmark、LinkedIn、Data Collective 690 万美金融资。

　　不同于传统的企业信息列队系统，Kafka是以近乎实时的方式处理流经一个公司的所有数据，目前已经为LinkedIn，Netflix，Uber和Verizon 建立了实时信息处理平台。Confluent 的愿景便是让其他公司也能用上这种平台。Confluent 已经向 Kafka 用户了解了他们的使用模型。现在还没有产品出来，但这些实践足以启示 Confluent应当打造何种产品。


使用tcpdump+Wireshark抓包分析kafka通信协议
https://blog.csdn.net/icycode/article/details/80034774

完整的协议介绍可以参考： 
A Guide To The Kafka Protocol：

https://cwiki.apache.org/confluence/display/KAFKA/A+Guide+To+The+Kafka+Protocol 

kafka协议指南：

http://colobu.com/2017/01/26/A-Guide-To-The-Kafka-Protocol/ 



kafka ui
https://github.com/linxin26/kafka-monitor

jsp写的web ui工具

kafka往zk中存了哪些数据？
Kafka在Zookeeper中存储的信息都在 / 根路径下，大致分为5大类1：

/brokers 目录下存储着kafka集群broker的相关信息，包括：
/broker/ids/ 目录，采用 临时znode 的方式，存储所有的broker节点，每个broker的配置文件中都需要指定一个数字类型的id（全局不可重复）；
/broker/topics/ 目录，采用 持久znode 的方式，存储所有的topic注册信息；
/brokers/topics/ [topic_name]/partitions/ 目录，采用 持久znode 的方式，存储某个topic的partitions所有分配信息；
/controller 目录存储着Controller中央控制器所在kafka broker的信息；


个人kafka测试代码
bitbucket.org/sandisks/kafkatest

maven kafka-client
org.apache.kafka.common.serialization.Serializer

kafka集群依赖zk
最新版本不依赖

kafka
maven包

kafka自身，待Main函数，有api Scala写的

apache-kafka
spring-kafka


kafka broker  代理

一对多（包含一对一）
多对一


apache项目

kafka客户端
scala
java



Apache kafka实战 (胡夕)

[Kafka client](https://zhuanlan.zhihu.com/p/93623447)

https://www.jianshu.com/p/80a10811d5cb

```powershell

cd D:\Program\kafka_2.12-0.11.0.3

bin\windows\zookeeper-server-start.bat config\zookeeper.properties
bin\windows\kafka-server-start.bat config\server.properties
bin\windows\kafka-topics.bat --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test
bin\windows\kafka-topics.bat --list --zookeeper localhost:2181
bin\windows\kafka-console-producer.bat --broker-list localhost:9092 --topic test
bin\windows\kafka-console-producer.bat --broker-list localhost:9092 --topic test --partition 1


bin\windows\kafka-console-consumer.bat --bootstrap-server localhost:9092 --topic test --from-beginning


bin\windows\kafka-console-consumer.bat --bootstrap-server localhost:9092 --topic test --partition 1 --offset 2

bin\windows\kafka-topics.bat --describe --zookeeper localhost:2181 --topic test
Topic:test      PartitionCount:1        ReplicationFactor:1     Configs:
        Topic: test     Partition: 0    Leader: 0       Replicas: 0     Isr: 0
```



```shell
cd D:\Program\kafka_2.11-1.0.0
D:\Program\kafka_2.11-1.0.0> .\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties
cd D:\Program\kafka_2.11-1.0.0
.\bin\windows\kafka-server-start.bat config\server.properties


.\bin\windows\kafka-console-producer.bat --broker-list localhost:9092 --topic test
>dfads
>fasdfsa
>fdsafas
>终止批处理操作吗(Y/N)? Y
```

```shell
bin\windows\kafka-console-producer.bat
Read data from standard input and publish it to Kafka.
Option                                   Description
------                                   -----------
--batch-size <Integer: size>             Number of messages to send in a single
                                           batch if they are not being sent
                                           synchronously. (default: 200)
--broker-list <String: broker-list>      REQUIRED: The broker list string in
                                           the form HOST1:PORT1,HOST2:PORT2.
--compression-codec [String:             The compression codec: either 'none',
  compression-codec]                       'gzip', 'snappy', or 'lz4'.If
                                           specified without value, then it
                                           defaults to 'gzip'
--key-serializer <String:                The class name of the message encoder
  encoder_class>                           implementation to use for
                                           serializing keys. (default: kafka.
                                           serializer.DefaultEncoder)
--line-reader <String: reader_class>     The class name of the class to use for
                                           reading lines from standard in. By
                                           default each line is read as a
                                           separate message. (default: kafka.
                                           tools.
                                           ConsoleProducer$LineMessageReader)
--max-block-ms <Long: max block on       The max time that the producer will
  send>                                    block for during a send request
                                           (default: 60000)
--max-memory-bytes <Long: total memory   The total memory used by the producer
  in bytes>                                to buffer records waiting to be sent
                                           to the server. (default: 33554432)
--max-partition-memory-bytes <Long:      The buffer size allocated for a
  memory in bytes per partition>           partition. When records are received
                                           which are smaller than this size the
                                           producer will attempt to
                                           optimistically group them together
                                           until this size is reached.
                                           (default: 16384)
--message-send-max-retries <Integer>     Brokers can fail receiving the message
                                           for multiple reasons, and being
                                           unavailable transiently is just one
                                           of them. This property specifies the
                                           number of retires before the
                                           producer give up and drop this
                                           message. (default: 3)
--metadata-expiry-ms <Long: metadata     The period of time in milliseconds
  expiration interval>                     after which we force a refresh of
                                           metadata even if we haven't seen any
                                           leadership changes. (default: 300000)
--old-producer                           Use the old producer implementation.
--producer-property <String:             A mechanism to pass user-defined
  producer_prop>                           properties in the form key=value to
                                           the producer.
--producer.config <String: config file>  Producer config properties file. Note
                                           that [producer-property] takes
                                           precedence over this config.
--property <String: prop>                A mechanism to pass user-defined
                                           properties in the form key=value to
                                           the message reader. This allows
                                           custom configuration for a user-
                                           defined message reader.
--queue-enqueuetimeout-ms <Integer:      Timeout for event enqueue (default:
  queue enqueuetimeout ms>                 2147483647)
--queue-size <Integer: queue_size>       If set and the producer is running in
                                           asynchronous mode, this gives the
                                           maximum amount of  messages will
                                           queue awaiting sufficient batch
                                           size. (default: 10000)
--request-required-acks <String:         The required acks of the producer
  request required acks>                   requests (default: 1)
--request-timeout-ms <Integer: request   The ack timeout of the producer
  timeout ms>                              requests. Value must be non-negative
                                           and non-zero (default: 1500)
--retry-backoff-ms <Integer>             Before each retry, the producer
                                           refreshes the metadata of relevant
                                           topics. Since leader election takes
                                           a bit of time, this property
                                           specifies the amount of time that
                                           the producer waits before refreshing
                                           the metadata. (default: 100)
--socket-buffer-size <Integer: size>     The size of the tcp RECV size.
                                           (default: 102400)
--sync                                   If set message send requests to the
                                           brokers are synchronously, one at a
                                           time as they arrive.
--timeout <Integer: timeout_ms>          If set and the producer is running in
                                           asynchronous mode, this gives the
                                           maximum amount of time a message
                                           will queue awaiting sufficient batch
                                           size. The value is given in ms.
                                           (default: 1000)
--topic <String: topic>                  REQUIRED: The topic id to produce
                                           messages to.
--value-serializer <String:              The class name of the message encoder
  encoder_class>                           implementation to use for
                                           serializing values. (default: kafka.
                                           serializer.DefaultEncoder)
```


offset(偏移量)：一种元数据，它是一个不断递增的整数值，在创建消息时，kafka会把它添加到消息里。kafka为每条在分区的消息保存这个offset，这也是消费者在分区的位置。比如一个偏移量为10的消费者，表示它已经消费了0-9偏移量的消息，下一个要消费的消息是偏移量为10的。kafka 0.9版本之前存在zookeeper，0.9之后存在kafka。
https://blog.csdn.net/jsbylibo/article/details/106380733



要使用Java API将消息发送到指定的分区，请使用以下代码：
```java
ProducerRecord<String, String> record = new ProducerRecord<>("test", 1, "key", "value");
producer.send(record);
```

公司用kafka
异步
dubbo：同步？

kafka 推送消息，企业项目中用到

Scala 2.12
https://spark.apache.org/docs/0.9.1/scala-programming-guide.html

scala写的
现在有java版本吗？目前没有

### 面试题

Kafka 消息分发时间配置参数(Message Delivery Time)
默认情况下，Kafka会使用生产者提供的时间戳。

如何保证接受消息有序？

答：在同一个分区里面接受消息就可以了。一个主题只设置一个消息



订阅开发者邮箱

MQ解耦

幂等

多个消费者
序列化

[kafka官网](http://kafka.apache.org/)

[Kafka史上最详细原理总结](https://blog.csdn.net/lingbo229/article/details/80761778)

[英语](http://kafka.apache.org/21/documentation/streams/architecture)

### books

- [Kafka权威指南](https://book.douban.com/subject/27665114/)
- [Kafka](https://book.douban.com/subject/26828527/)
- [Kafka技术内幕](https://book.douban.com/subject/27179953/)

[Kafka史上最详细原理总结](https://zhuanlan.zhihu.com/p/79579389)

kafka 0.11 2018
更新历史
https://kafka.apache.org/downloads


```shell

bin/kafka-console-producer.sh --broker-list localhost:9092 --topic test


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----        2019/11/14     10:40                windows
-a----        2017/10/27     23:56           1335 connect-distributed.sh
-a----        2017/10/27     23:56           1332 connect-standalone.sh
-a----        2017/10/27     23:56            861 kafka-acls.sh
-a----        2017/10/27     23:56            873 kafka-broker-api-versions.sh
-a----        2017/10/27     23:56            864 kafka-configs.sh
-a----        2017/10/27     23:56            945 kafka-console-consumer.sh
-a----        2017/10/27     23:56            944 kafka-console-producer.sh
-a----        2017/10/27     23:56            871 kafka-consumer-groups.sh
-a----        2017/10/27     23:56            948 kafka-consumer-perf-test.sh
-a----        2017/10/27     23:56            869 kafka-delete-records.sh
-a----        2017/10/27     23:56            863 kafka-log-dirs.sh
-a----        2017/10/27     23:56            862 kafka-mirror-maker.sh
-a----        2017/10/27     23:56            886 kafka-preferred-replica-election.sh
-a----        2017/10/27     23:56            959 kafka-producer-perf-test.sh
-a----        2017/10/27     23:56            874 kafka-reassign-partitions.sh
-a----        2017/10/27     23:56            868 kafka-replay-log-producer.sh
-a----        2017/10/27     23:56            874 kafka-replica-verification.sh
-a----        2017/10/27     23:56           7579 kafka-run-class.sh
-a----        2017/10/27     23:56           1376 kafka-server-start.sh
-a----        2017/10/27     23:56            975 kafka-server-stop.sh
-a----        2017/10/27     23:56            870 kafka-simple-consumer-shell.sh
-a----        2017/10/27     23:56            945 kafka-streams-application-reset.sh
-a----        2017/10/27     23:56            863 kafka-topics.sh
-a----        2017/10/27     23:56            958 kafka-verifiable-consumer.sh
-a----        2017/10/27     23:56            958 kafka-verifiable-producer.sh
-a----        2017/10/27     23:56           1722 trogdor.sh
-a----        2017/10/27     23:56            867 zookeeper-security-migration.sh
-a----        2017/10/27     23:56           1393 zookeeper-server-start.sh
-a----        2017/10/27     23:56            978 zookeeper-server-stop.sh
-a----        2017/10/27     23:56            968 zookeeper-shell.sh
```






- RabbitMQ 消费者默认是推模式（也支持拉模式）。
- Kafka 默认是拉模式。
- Push方式：优点是可以尽可能快地将消息发送给消费者，缺点是如果消费者处理能力跟不上，消费者的缓冲区可能会溢出。
- Pull方式：优点是消费端可以按处理能力进行拉去，缺点是会增加消息延迟。





#### Kafka如何保证消息不丢失不重复

 https://blog.csdn.net/matrix_google/article/details/79888144 



#### 面试官问：为什么kafka这么快，又能保证消息不丢失？


  https://blog.csdn.net/assasin0308/article/details/91638528 





#### Kafka - 偏移量提交



 https://blog.csdn.net/u011669700/article/details/80053313 





#### kafka分区数量的判定

 https://blog.csdn.net/qq_36066039/article/details/88399091 





### kafka应用场景



大数据



linkin

