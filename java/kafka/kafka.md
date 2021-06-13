# kafka



kafka stream





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

　　不同于传统的企业信息列队系统，Kafka 是以近乎实时的方式处理流经一个公司的所有数据，目前已经为 LinkedIn，Netflix，Uber 和 Verizon 建立了实时信息处理平台。Confluent 的愿景便是让其他公司也能用上这种平台。Confluent 已经向 Kafka 用户了解了他们的使用模型。现在还没有产品出来，但这些实践足以启示 Confluent应当打造何种产品。



https://blog.csdn.net/icycode/article/details/80034774


kfuka ui
https://github.com/linxin26/kafka-monitor



个人kafka测试代码
bitbucket.org/sandisks/kafkatest

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
skala
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
bin\windows\kafka-console-producer.bat --broker-list localhost:2181 --topic test
bin\windows\kafka-console-consumer.bat --bootstrap-server localhost:2181 --topic test --from-beginning
```


公司用kafka
异步
dubbo：同步？

kafka 推送消息，企业项目中用到

Scala 2.12
https://spark.apache.org/docs/0.9.1/scala-programming-guide.html

scala写的
现在有java版本吗？目前没有

面试题
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