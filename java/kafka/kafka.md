# kafka

kafka社区上有一些数据防止丢失的问题，没有解决
Kafka社区上有关数据防止丢失的问题还没有最佳解决方案,主要有以下几点:
1. Kafka默认设置会导致数据丢失
Kafka有以下设计会导致数据丢失:
- 分区日志由多个segment组成,segment超过配置值会删除。新生产的消息会写入新segment,旧segment会 delete。
- 配置只保留一定时间的消息,超时的消息会定期删除。
- replicas角色有LEADER和FOLLOWERS,FOLLOWERS不会写消息,只负责复制LEADER。但如果LEADER故障,FOLLOWERS之间没有消息交换,会导致部分消息丢失。
因此如果不采取额外措施,Kafka无法保证绝对不丢失任何消息。
2. Kafka社区提议的可选方案
Kafka社区曾提议一些可选方案:

- 使用更高的replica数,增加容错性
- 同步所有FOLLOWERS以减少消息丢失
- 将消息持久化到外部存储系统,如Hadoop HDFS
- 合理配置retention.ms和segment.ms,延长消息保留时间
- 使用Kafka Streams进行exactly-once processing 
- 等等

但是都存在各自的缺点和限制。

3. 没有最佳方案
最终 Kafka社区还没有采用一个最佳的防止消息丢失的标准方案。
常见做法是使用上述可选方案中的一种或者多种。但都不完全能保证绝对没有消息丢失。
Kafka官方网站为:https://kafka.apache.org/ ,里面提供了大量的使用文档、讨论和解决方案。


kafka配置项目

配置文件备份
kafka_server.properties


num.network.threads=3
num.io.threads=8  包括磁盘io


```xml
# Switch to enable topic deletion or not, default value is false
delete.topic.enable=true
auto.create.topics.enable=false
```

### kafka springboot
https://gitee.com/edidada/testspringbootkafka
springboot项目中直接注入
```java
    @Autowired
    private KafkaTemplate<String, String> kafkaTemplate;
```

org.springframework.boot.autoconfigure.kafka.KafkaAutoConfiguration.kafkaTemplate，这个bean自动注入的

kafka消费者默认使用
org.springframework.kafka.annotation.KafkaListener注解
参数：
1、topic
2、groupId

源代码
```java
@Target({ElementType.TYPE, ElementType.METHOD, ElementType.ANNOTATION_TYPE})
@Retention(RetentionPolicy.RUNTIME)
@MessageMapping
@Documented
@Repeatable(KafkaListeners.class)
public @interface KafkaListener {
    String id() default "";

    String containerFactory() default "";

    String[] topics() default {};

    String topicPattern() default "";

    TopicPartition[] topicPartitions() default {};

    String containerGroup() default "";

    String errorHandler() default "";

    String groupId() default "";

    boolean idIsGroup() default true;

    String clientIdPrefix() default "";

    String beanRef() default "__listener";
}
```

如果你需要使用 Kafka 的其他高级功能，例如事务、定时器、分区器等，可以通过在应用程序中添加相应的 Bean 来实现。例如，在 Spring Boot 应用程序中，你可以使用以下代码来创建一个自定义的 KafkaProducerFactory Bean：
```java
@Bean
public ProducerFactory<String, String> producerFactory() {
    Map<String, Object> configProps = new HashMap<>();
    configProps.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
    configProps.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
    configProps.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
    configProps.put(ProducerConfig.TRANSACTIONAL_ID_CONFIG, "my-transactional-id");

    DefaultKafkaProducerFactory<String, String> factory = new DefaultKafkaProducerFactory<>(configProps);
    factory.setTransactionIdPrefix("my-");
    return factory;
}
```


### spring kafka

https://gitee.com/edidada/testkafkaspring

        <dependency>
            <groupId>org.springframework.kafka</groupId>
            <artifactId>spring-kafka</artifactId>
            <version>2.8.0</version>
        </dependency>
依赖
    <dependency>
      <groupId>org.apache.kafka</groupId>
      <artifactId>kafka-clients</artifactId>
      <version>3.0.0</version>
    </dependency>


老版本

https://gitee.com/edidada/kafka-examples



https://gitee.com/edidada/testkafka





kafka broker设置不能自动创建主题

发送消息向不存在的主题，报错：Topic my-topic not present in metadata
```shell
Exception in thread "main" org.springframework.kafka.KafkaException: Send failed; nested exception is org.apache.kafka.common.errors.TimeoutException: Topic my-topic not present in metadata after 60000 ms.
	at org.springframework.kafka.core.KafkaTemplate.doSend(KafkaTemplate.java:660)
	at org.springframework.kafka.core.KafkaTemplate.send(KafkaTemplate.java:403)
	at cn.wdidada.testkafkaspring.KafkaProducer.sendMessage(KafkaProducer.java:11)
	at cn.wdidada.testkafkaspring.SpringKafkaMain.main(SpringKafkaMain.java:9)
Caused by: org.apache.kafka.common.errors.TimeoutException: Topic my-topic not present in metadata after 60000 ms.
```



### kafka自带解码器

Kafka 自带了一些内置的解码器，这些解码器可以用于将消息的二进制数据转换为特定的数据类型。以下是 Kafka 自带的一些内置解码器：
1. StringDecoder
StringDecoder 是 Kafka 自带的字符串解码器，它将消息的二进制数据解码为字符串类型。在使用 StringDecoder 时，需要确保生产者和消费者都使用相同的字符集。
在 Kafka 0.10 及更高版本中，建议使用 StringDeserializer 替代 StringDecoder。
2. ByteArrayDecoder
ByteArrayDecoder 是 Kafka 自带的字节数组解码器，它将消息的二进制数据解码为字节数组类型。
在 Kafka 0.10 及更高版本中，建议使用 ByteArrayDeserializer 替代 ByteArrayDecoder。
3. DefaultPartitioner
DefaultPartitioner 是 Kafka 自带的默认分区器，它使用消息的 key 值来确定消息被发送到哪个分区。如果消息没有 key 值，则使用轮询的方式将消息发送到不同的分区。
4. RoundRobinPartitioner
RoundRobinPartitioner 是 Kafka 自带的轮询分区器，它使用轮询的方式将消息发送到不同的分区。
5. TimeBasedPartitioner
TimeBasedPartitioner 是 Kafka 自带的基于时间的分区器，它使用消息的时间戳来确定消息被发送到哪个分区。如果消息没有时间戳，则使用当前时间作为时间戳。

需要注意的是，Kafka 的解码器和分区器是可扩展的，我们可以根据自己的需求实现自定义的解码器和分区器，并将其用于生产者和消费者中。此外，Kafka 还支持使用 Avro、JSON、Protobuf 等第三方序列化框架进行数据的序列化和反序列化。

Avro这个编码，kafka权威指南这本书上有讲解

kafka logs文件夹下.index文件是干嘛的？
Kafka是一个分布式流处理平台，它的数据存储采用了分片和索引机制。每个分区都会被分为多个段，每个段对应两个文件：“.index"索引文件和”.log"数据文件。索引文件中存储着大量元数据，而数据文件中存储着大量消息。由于生产者生产的消息会不断追加到log文件末尾，为防止log文件过大导致数据定位效率低下，Kafka采取了分片和索引机制，将每个partition分为多个segment。
.index文件是Kafka的偏移量索引或时间戳索引，用于定位指定偏移量或时间戳的数据。由于Kafka的数据都是按序插入的，offset也是按序增长的，因此很适合用二分查找定位指定偏移量或时间戳的数据。

https://blog.csdn.net/liu_feng_zi_/article/details/123207695
https://zhuanlan.zhihu.com/p/103249714


Kafka集群主从模型是主读主写，生产者写入消息、消费者读取消息的操作都是与 leader 副本进行交互的，从而实现的是一种「主写主读」的生产消费模型。 Kafka 并不支持「主写从读」

kafka分布式算法是raft
当Kafka的主节点不可用时，follower节点会进行选举，选出新的leader节点。选举的过程如下：
follower节点向其他follower节点发送请求，请求成为新的leader节点。
其他follower节点响应请求，如果同意，则将自己的状态改为candidate状态，并向其他follower节点发送投票请求。
其他follower节点收到投票请求后，如果同意，则将自己的状态改为voting状态，并向candidate节点发送投票。
candidate节点收到超过半数follower节点的投票后，将自己的状态改为leader状态，并向所有follower节点发送同步消息。
是的，Kafka的选主过程使用的是Raft协议。Raft协议是一种分布式一致性算法，用于解决分布式系统中的数据一致性问题。Kafka使用Raft协议来保证集群中的数据一致性和高可用性。
Kafka的Raft代码是使用自己编码实现的。Kafka使用了自己的Raft实现，而不是使用其他库来实现Raft协议。Kafka的Raft实现是基于Zookeeper的，它使用Zookeeper来存储集群中的元数据和状态信息。

Kafka的leader节点将消息发送给follower节点使用的是TCP协议。Kafka使用TCP协议来保证消息的可靠传输和顺序传输。

Kafka 是一个分布式的消息中间件系统，需要对其进行监控和运维，以确保系统的稳定性和可靠性。以下是一些常用的 Kafka 监控运维工具：
Kafka Manager：由 Yahoo 开发的开源项目，提供了一个易于使用的 Web 界面，用于监控和管理 Kafka 集群。它可以帮助管理员查看集群状态、创建和修改主题、查看消费者组信息、查看 Broker 日志等。
Kafka Offset Monitor：由 LinkedIn 开发的开源项目，用于监控 Kafka 消费者的位移（Offset），可以帮助管理员查看每个消费者组的位移信息、消费速率、延迟等。它还可以帮助管理员发现消费者出现问题，例如消费者组停止消费、消费速率慢等。
Prometheus：一个开源的监控系统，可以用于监控 Kafka 集群的各种指标，例如 Broker 的 CPU 使用率、磁盘空间使用率、网络带宽等。它支持通过标签（Label）来对指标进行分类和聚合，方便管理员进行快速的故障排查和性能优化。
Grafana：一个开源的数据可视化工具，可以与 Prometheus 集成，用于创建仪表盘（Dashboard），展示 Kafka 集群的各种指标，例如消费者组的消费速率、主题的生产速率、Broker 的磁盘空间使用率等。它可以帮助管理员更直观地了解 Kafka 集群的运行情况，发现问题并进行优化。
除了上述工具外，还有许多其他的 Kafka 监控运维工具，例如 Burrow、Kafka Eagle、Kafka Web Console 等。管理员可以根据自己的需求选择合适的工具来监控和管理 Kafka 集群。


是的，Kafka支持死信队列。Kafka的死信队列是通过Kafka Connect来实现的。Kafka Connect是一个用于连接Kafka和外部系统的框架，它可以将数据从Kafka导出到外部系统，也可以将数据从外部系统导入到Kafka。

kafka 2.12 windows 数据文件存储位置
kafka logs是数据文件吗？

是的，Kafka 中的 logs 目录是用于存储数据文件的。在 Kafka 中，每个主题（Topic）都有一个或多个分区（Partition），每个分区都对应一个数据文件，用于存储分区中的消息数据。
Kafka 中的数据文件被称为日志（Log），它是一个追加写的文件，可以保证数据的顺序性和一致性。每个日志文件都有一个唯一的名称，格式为 <topic>-<partition>_<start_offset>.log，例如 test-0_00000000000000000000.log 表示 test 主题的第 0 个分区中的第一条消息。
Kafka 使用日志文件来实现持久化存储和高可用性。当消息写入 Kafka 时，它们首先被追加到生产者所在的分区的日志文件中。消费者从分区的日志文件中读取数据，并且在读取完数据后，Kafka 将会定期清理过期数据文件。
因此，logs 目录中的文件是 Kafka 中存储消息数据的重要组成部分。如果某个分区的日志文件被删除或损坏，Kafka 可能无法恢复该分区中的数据，这可能导致消息丢失或无法处理。

要在 Kafka 消息接收者中打印消息 ID，你需要使用 ConsumerRecord 对象中的 offset 属性。这个属性代表消息在分区中的偏移量，可以用作唯一的消息标识符。以下是一个 Java 代码示例，展示了如何在 Kafka 消息接收者中打印消息 ID：
Kafka消息接收者可以通过获取消息的offset来获取消息id。offset是一个long类型的数字，它代表了一个消息在一个特定分区中的位置。Kafka使用offset来唯一标识一个消息，因此，如果您知道一个消息的offset，您就可以使用它来检索该消息。
如果您使用Kafka的高级API，那么您可以使用ConsumerRecord类来获取消息的offset。ConsumerRecord类是一个包含有关消费者记录的元数据的对象，包括消息的key、value、分区和偏移量等信息。
如果您使用Kafka的低级API，则需要使用KafkaConsumer.poll()方法来获取消息。该方法返回一个ConsumerRecords对象，其中包含从Kafka服务器接收到的所有记录。每个记录都包含有关消费者记录的元数据，包括消息的key、value、分区和偏移量等信息。


Kafka Rebalance 是指消费者组中的消费者数量发生变化（例如，有消费者加入或退出消费者组）时，Kafka 集群自动重新分配分区的过程。在这个过程中，分区被重新分配给新的消费者，这可能会导致消息重复处理或消息丢失等问题。为了解决这个问题，你可以采取以下措施：
提高每个消费者的消费能力：如果你的消费者组经常出现 Rebalance，这可能是因为某些消费者的消费能力不足，导致其他消费者无法及时消费消息。你可以尝试增加每个消费者的消费线程数或提高消费者的消费性能，以减少 Rebalance 的频率。
增加分区数：如果你的消费者组中的消费者数量经常变化，你可以考虑增加主题的分区数，这样可以减少 Rebalance 的影响。如果你正在使用自动分区分配，你可以考虑手动分配分区以提高灵活性。
避免过多的消费者退出：在 Rebalance 过程中，如果有太多的消费者退出消费者组，就会导致分区无法及时分配到新的消费者。因此，你应该避免过多的消费者退出，或者在消费者退出时等待一段时间，以确保新的消费者可以及时接管分区。
避免重复消费：当 Rebalance 完成后，消费者可能会重复消费之前未消费的消息。你可以通过将消费位移提交到 Kafka 的内部主题 __consumer_offsets 来解决这个问题，以便消费者在重启后可以正确地从之前的位置开始消费。

使用保证语义：如果你的应用程序需要保证消息只被消费一次，你可以使用 Kafka 的 Exactly Once 语义。这需要使用 Kafka 事务，并在消费者端处理重复消息的情况。
总之，解决 Kafka Rebalance 问题的关键是提高消费者组的稳定性和性能，并在 Rebalance 过程中避免消息丢失和重复消费的情况。



在 Kafka 中，序列化是将对象转换为字节流的过程，用于在生产者和消费者之间传输数据。序列化在 Kafka 中的作用如下：
支持多种数据格式
Kafka 支持多种数据格式，包括字符串、整数、浮点数、JSON、Avro、Protobuf 等。不同的序列化器可以将不同的数据格式转换为字节流，使得 Kafka 可以处理多种类型的数据。
提高传输效率
将数据序列化为字节流可以大大提高传输效率，因为字节流比文本格式更紧凑。这对于传输大量数据的应用程序尤为重要。
支持版本控制
在 Kafka 中，数据的格式可能会发生变化。序列化器可以支持不同版本的数据格式，以便生产者和消费者在不同的数据格式之间进行转换。
支持自定义类型
Kafka 中的序列化器可以支持自定义类型。这使得应用程序可以使用自定义的 Java 类型来传输数据。


### kafka支持json
写个例子



kafka stream


### kafka书籍
- 深入理解Kafka与Pulsar
- Kafka权威指南（第2版）
- Apache kafka实战 (胡夕)



主题 topic

分区



message是分区内有序



broker，发布消息的中心点

broker是kafka集群中的一个节点



### kafka配置项



acks 定义了集群中多少个broker确认才能确定消息写入是成功的
0
1
all？

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
RocketMQ支持事务 java写的
kafka scala/java写的


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
bitbucket.org/sandisks/

ProducerListenerAdapter作用？

<dependency>
    <groupId>org.springframework.kafka</groupId>
    <artifactId>spring-kafka-test</artifactId>
    <version>2.2.6.RELEASE</version>
</dependency>

        <dependency>
            <groupId>org.springframework.integration</groupId>
            <artifactId>spring-integration-kafka</artifactId>
            <version>3.0.3.RELEASE</version>
        </dependency>


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



1. 在配置 KafkaTemplate 时，可以通过设置不同的参数来控制 Kafka 生产者的行为，例如 `acks`、`retries`、`batch.size` 等。这些参数的含义和用法可以参考 Kafka 生产者的配置文档。

DefaultKafkaProducerFactory是否是自动创建topic？？
DefaultKafkaProducerFactory 是 Spring Kafka 提供的一个默认的 Kafka 生产者工厂实现类。它负责创建 KafkaProducer 实例，用于发送消息到 Kafka 集群。 
DefaultKafkaProducerFactory 并不会自动创建 Kafka 主题（topic），它只是提供了一个 KafkaProducer 实例，用于向已经存在的 Kafka 主题发送消息。如果要发送消息到一个不存在的主题，KafkaProducer 会在发送消息时自动创建该主题。但这种自动创建主题的行为并不是由 DefaultKafkaProducerFactory 控制的，而是由 Kafka 的 Broker 控制的。
需要注意的是，Kafka 自动创建主题的功能默认是开启的，可以通过 Kafka Broker 的配置文件或者命令行参数进行配置。此外，自动创建主题功能也可以被禁用，这样当向一个不存在的主题发送消息时，会抛出异常。
在 Spring Kafka 中，如果需要在生产者发送消息时自动创建主题，可以通过在 KafkaTemplate 中设置 `autoCreateTopics` 属性为 `true` 来实现。例如：
```java
@Bean
public KafkaTemplate<String, String> kafkaTemplate() {
    Map<String, Object> configs = new HashMap<>();
    configs.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
    configs.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class);
    configs.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class);

    // enable auto topic creation
    configs.put("auto.create.topics.enable", true);

    return new KafkaTemplate<>(new DefaultKafkaProducerFactory<>(configs));
}
```

在这个示例中，我们设置了 `auto.create.topics.enable` 属性为 `true`，以启用自动创建主题的功能。这样，在向一个不存在的主题发送消息时，Kafka 将会自动创建该主题。

Apache kafka实战 (胡夕)
[Kafka client](https://zhuanlan.zhihu.com/p/93623447)

https://www.jianshu.com/p/80a10811d5cb

```powershell

cd D:\Program\kafka_2.12-0.11.0.3

bin\windows\zookeeper-server-start.bat config\zookeeper.properties
bin\windows\kafka-server-start.bat config\server.properties
bin\windows\kafka-topics.bat --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test
bin\windows\kafka-topics.bat --list --zookeeper localhost:2181

bin\windows\kafka-topics.bat --delete --topic my-topics --zookeeper localhost:2181


bin\windows\kafka-topics.bat --create --topic myDemo --zookeeper localhost:2181 --partitions 2 --replication-factor 1 



bin\windows\kafka-console-producer.bat --broker-list localhost:9092 --topic test

bin\windows\kafka-console-producer.bat --broker-list localhost:9092 --topic test --property "parse.key=true" --property "key.separator=:" --property "partition.key=1"


bin\windows\kafka-console-consumer.bat --bootstrap-server localhost:9092 --topic testDemo --from-beginning

bin\windows\kafka-console-consumer.bat --bootstrap-server localhost:9092 --topic my-topic --from-beginning

bin\windows\kafka-console-consumer.bat --bootstrap-server localhost:9092 --topic test --partition 1 --offset 2

bin\windows\kafka-topics.bat --describe --zookeeper localhost:2181 --topic test
Topic:test      PartitionCount:1        ReplicationFactor:1     Configs:
        Topic: test     Partition: 0    Leader: 0       Replicas: 0     Isr: 0
```



[2023-04-28 13:45:48,851] INFO Loading logs. (kafka.log.LogManager)
[2023-04-28 13:45:48,945] WARN Found a corrupted index file due to requirement failed: Corrupt index found, index file (D:\tmp\kafka-logs\linlin-0\00000000000000000000.index) has non-zero size but the last offset is 0 which is no larger than the base offset 0.}. deleting D:\tmp\kafka-logs\linlin-0\00000000000000000000.timeindex, D:\tmp\kafka-logs\linlin-0\00000000000000000000.index, and D:\tmp\kafka-logs\linlin-0\00000000000000000000.txnindex and rebuilding index... (kafka.log.Log)
[2023-04-28 13:45:48,945] ERROR There was an error in one of the threads during logs loading: java.nio.file.FileSystemException: \tmp\kafka-logs\linlin-0\00000000000000000000.timeindex: 另一个程序正在使用此文件，进程无法访问。
 (kafka.log.LogManager)
[2023-04-28 13:45:48,961] FATAL [Kafka Server 0], Fatal error during KafkaServer startup. Prepare to shutdown (kafka.server.KafkaServer)
java.nio.file.FileSystemException: \tmp\kafka-logs\linlin-0\00000000000000000000.timeindex: 另一个程序正在使用此文件，进程无法访问。

        at sun.nio.fs.WindowsException.translateToIOException(WindowsException.java:86)
        at sun.nio.fs.WindowsException.rethrowAsIOException(WindowsException.java:97)
        at sun.nio.fs.WindowsException.rethrowAsIOException(WindowsException.java:102)
        at sun.nio.fs.WindowsFileSystemProvider.implDelete(WindowsFileSystemProvider.java:269)
        at sun.nio.fs.AbstractFileSystemProvider.deleteIfExists(AbstractFileSystemProvider.java:108)
        at java.nio.file.Files.deleteIfExists(Files.java:1165)
        at kafka.log.Log.$anonfun$loadSegmentFiles$3(Log.scala:318)
        at scala.collection.TraversableLike$WithFilter.$anonfun$foreach$1(TraversableLike.scala:789)
        at scala.collection.IndexedSeqOptimized.foreach(IndexedSeqOptimized.scala:32)
        at scala.collection.IndexedSeqOptimized.foreach$(IndexedSeqOptimized.scala:29)
        at scala.collection.mutable.ArrayOps$ofRef.foreach(ArrayOps.scala:191)
        at scala.collection.TraversableLike$WithFilter.foreach(TraversableLike.scala:788)
        at kafka.log.Log.loadSegmentFiles(Log.scala:279)
        at kafka.log.Log.loadSegments(Log.scala:383)
        at kafka.log.Log.<init>(Log.scala:186)
        at kafka.log.Log$.apply(Log.scala:1610)
        at kafka.log.LogManager.$anonfun$loadLogs$12(LogManager.scala:172)
        at kafka.utils.CoreUtils$$anon$1.run(CoreUtils.scala:57)
        at java.util.concurrent.Executors$RunnableAdapter.call(Executors.java:511)
        at java.util.concurrent.FutureTask.run(FutureTask.java:266)
        at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1149)
        at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:624)
        at java.lang.Thread.run(Thread.java:748)





这个错误表明另一个程序正在使用Kafka的时间索引文件，因此Kafka无法访问该文件。该文件是Kafka用于跟踪分区中消息的时间戳的一部分。通常情况下，这个错误发生时，可能是因为Kafka服务器已经在运行中，或者在上一次关闭时没有正常关闭，导致时间索引文件被占用。

你可以尝试以下几种解决方法：

关闭所有Kafka服务器并重启：首先，你可以尝试关闭所有Kafka服务器，然后再重新启动它们。这样可以确保Kafka服务器重新打开并释放时间索引文件的锁定。如果这个问题经常出现，你可能需要检查你的Kafka服务器是否正常关闭，并确保在关闭前完全清空了所有资源。

杀死占用文件的进程：如果Kafka服务器没有运行，那么这个错误可能是由于其他进程占用了时间索引文件。你可以尝试杀死这个进程，或者在使用文件之前等待该进程释放文件锁。

更改时间索引文件的位置：你也可以尝试更改时间索引文件的位置，使其不受其他进程的影响。你可以通过修改Kafka配置文件中的 log.dirs 参数来更改时间索引文件的位置



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



下面是删除主题命令行

```shell
PS D:\Program\kafka_2.12-0.11.0.3> bin\windows\kafka-topics.bat --list --zookeeper localhost:2181
__consumer_offsets
my-topic
my-topics
mytest
test
testTopic
PS D:\Program\kafka_2.12-0.11.0.3> bin\windows\kafka-topics.bat --delete --topic my-topics --zookeeper localhost:2181
Topic my-topics is marked for deletion.
Note: This will have no impact if delete.topic.enable is not set to true.
PS D:\Program\kafka_2.12-0.11.0.3>
PS D:\Program\kafka_2.12-0.11.0.3>
PS D:\Program\kafka_2.12-0.11.0.3> bin\windows\kafka-topics.bat --list --zookeeper localhost:2181
__consumer_offsets
my-topic
my-topics
mytest
test
testTopic
PS D:\Program\kafka_2.12-0.11.0.3> bin\windows\kafka-topics.bat --list --zookeeper localhost:2181
__consumer_offsets
my-topic
my-topics
mytest
test
testTopic
PS D:\Program\kafka_2.12-0.11.0.3> bin\windows\kafka-topics.bat --delete --topic my-topics --zookeeper localhost:2181
Topic my-topics is marked for deletion.
Note: This will have no impact if delete.topic.enable is not set to true.
PS D:\Program\kafka_2.12-0.11.0.3> bin\windows\kafka-topics.bat --delete --topic my-topics --zookeeper localhost:2181
Topic my-topics is already marked for deletion.
PS D:\Program\kafka_2.12-0.11.0.3> bin\windows\kafka-topics.bat --list --zookeeper localhost:2181
__consumer_offsets
my-topic
my-topics - marked for deletion
mytest
test
testTopic
PS D:\Program\kafka_2.12-0.11.0.3>
```



```shell
[2023-05-06 14:09:20,165] ERROR [KafkaApi-0] Error when handling request {controller_id=0,controller_epoch=6,delete_partitions=true,partitions=[{topic=my-topics,partition=0}]} (kafka.server.KafkaApis)
kafka.common.KafkaStorageException: Failed to rename log directory from D:\tmp\kafka-logs20230506\my-topics-0 to D:\tmp\kafka-logs20230506\my-topics-0.4e015dcb5f194710ac100c5998b3f188-delete
        at kafka.log.LogManager.asyncDelete(LogManager.scala:492)
        at kafka.cluster.Partition.$anonfun$delete$1(Partition.scala:155)
        at scala.runtime.java8.JFunction0$mcV$sp.apply(JFunction0$mcV$sp.java:12)
        at kafka.utils.CoreUtils$.inLock(CoreUtils.scala:213)
        at kafka.utils.CoreUtils$.inWriteLock(CoreUtils.scala:221)
        at kafka.cluster.Partition.delete(Partition.scala:150)
        at kafka.server.ReplicaManager.stopReplica(ReplicaManager.scala:291)
        at kafka.server.ReplicaManager.$anonfun$stopReplicas$2(ReplicaManager.scala:321)
        at scala.collection.Iterator.foreach(Iterator.scala:929)
        at scala.collection.Iterator.foreach$(Iterator.scala:929)
        at scala.collection.AbstractIterator.foreach(Iterator.scala:1417)
        at scala.collection.IterableLike.foreach(IterableLike.scala:71)
        at scala.collection.IterableLike.foreach$(IterableLike.scala:70)
        at scala.collection.AbstractIterable.foreach(Iterable.scala:54)
        at kafka.server.ReplicaManager.stopReplicas(ReplicaManager.scala:320)
        at kafka.server.KafkaApis.handleStopReplicaRequest(KafkaApis.scala:191)
        at kafka.server.KafkaApis.handle(KafkaApis.scala:102)
        at kafka.server.KafkaRequestHandler.run(KafkaRequestHandler.scala:66)
        at java.lang.Thread.run(Thread.java:748)
[2023-05-06 14:09:20,188] INFO [ReplicaFetcherManager on broker 0] Removed fetcher for partitions my-topics-0 (kafka.server.ReplicaFetcherManager)
```



Failed to rename log directory from D:\tmp\kafka-logs20230506\my-topics-0 to D:\tmp\kafka-logs20230506\my-topics-0.4e015dcb5f194710ac100c5998b3f188-delete





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

### kafkatest测试项目

kafka_2.10-0.8.2.2
集群版本

注意scala版本和java版本的kafka客户端
java版本 spring-kafka

在Kafka 0.8.2之前，kafka.javaapi.producer.Producer是为唯一官方用Scala实现的Java Client。
在Kafka 0.8.2之后，有新的Java Producer API，org.apache.kafka.clients.producer.KafkaProducer,完全用Java实现的。
https://blog.csdn.net/lavorange/article/details/78970977

kafka提供的库，在配对版本号的情况下，可以访问kafka 0.8.2.0
apache提供的库(spring kafka依赖的)，最低支持0.9版本的kafka，目前访问不了

可执行程序
- KafkaProducerOld
- KafkaConsumerOld
- KafkaProducerNew
- KafkaConsumerNew

old是旧版本
new是新版本

org.apache.kafka.common.errors.TimeoutException: Failed to update metadata after 60000 ms.

[spring boot 集成 kafka 之 spring-kafka 深入探秘](https://my.oschina.net/keking/blog/3056698)

kafka的Java客户端示例代码(kafka_2.11-0.8.2.2)
https://www.cnblogs.com/hd3013779515/p/6939013.html

```java
	at kafka.network.Processor.read(SocketServer.scala:450)
	at kafka.network.Processor.run(SocketServer.scala:340)
	at java.lang.Thread.run(Thread.java:745)
[2019-11-29 15:00:25,207] ERROR Closing socket for /192.168.196.37 because of error (kafka.network.Processor)
kafka.common.KafkaException: Wrong request type 18
	at kafka.api.RequestKeys$.deserializerForKey(RequestKeys.scala:64)
	at kafka.network.RequestChannel$Request.<init>(RequestChannel.scala:50)
```

需要kafka0.11以上
目前是0.8.2.2
[ApiKeys](https://github.com/apache/kafka/blob/trunk/clients/src/main/java/org/apache/kafka/common/protocol/ApiKeys.java#L23-L43)

        <dependency>
            <groupId>org.apache.kafka</groupId>
            <artifactId>kafka_2.11</artifactId>
            <version>0.10.2.0</version>
        </dependency>
上面是旧api，下面是新api
        <dependency>
            <groupId>org.apache.kafka</groupId>
            <artifactId>kafka-clients</artifactId>
            <version>2.0.1</version>
        </dependency>