# Kafka权威指南2

https://book.douban.com/subject/36161660/

Windows 10电脑上有第一版pdf

Kafka权威指南.[美]Neha Narkhede(详细书签).pdf
2018年第一版

https://www.ituring.com.cn/book/2931

本书赞誉 xvii
第 2 版序 xix
第 1 版序 xxi
前言 xxiii
第 1 章 初识Kafka 1
1．1　发布与订阅消息系统 1
1．1．1　如何开始 2
1．1．2　独立的队列系统 3
1．2 Kafka登场 3
1．2．1　消息和批次 4
1．2．2　模式 4
1．2．3　主题和分区 4
1．2．4　生产者和消费者 5
1．2．5 broker和集群 6
1．2．6　多集群 7
1．3　为什么选择Kafka 8
1．3．1　多个生产者 8
1．3．2　多个消费者 8
1．3．3　基于磁盘的数据保留 9
1．3．4　伸缩性 9
1．3．5　高性能 9
1．3．6　平台特性 9
1．4　数据生态系统 9
1．5　起源故事 11
1．5．1 LinkedIn的问题 11
1．5．2 Kafka的诞生 12
1．5．3　走向开源 12
1．5．4　商业化 13
1．5．5　命名 13
1．6　开始Kafka之旅 13
第 2 章 安装Kafka 14
2．1　环境配置 14
2．1．1　选择操作系统 14
2．1．2　安装Java 14
2．1．3　安装ZooKeeper 15
2．2　安装broker 17
2．3　配置broker 18
2．3．1　常规配置参数 18
2．3．2　主题的默认配置 20
2．4　选择硬件 24
2．4．1　磁盘吞吐量 25
2．4．2　磁盘容量 25
2．4．3　内存 25
2．4．4　网络 25
2．4．5 CPU 26
2．5　云端的Kafka 26
2．5．1　微软Azure 26
2．5．2 AWS 26
2．6　配置Kafka集群 27
2．6．1　需要多少个broker 27
2．6．2 broker配置 28
2．6．3　操作系统调优 28
2．7　生产环境的注意事项 31
2．7．1　垃圾回收器选项 31
2．7．2　数据中心布局 32
2．7．3　共享ZooKeeper 32
2．8　小结 33
第 3 章 Kafka生产者——向Kafka写入数据 34
3．1　生产者概览 35
3．2　创建 Kafka生产者 36
3．3　发送消息到Kafka 37
3．3．1　同步发送消息 38
3．3．2　异步发送消息 39
3．4　生产者配置 39
3．4．1 client．id 40
3．4．2 acks 40
3．4．3　消息传递时间 41
3．4．4 linger．ms 43
3．4．5 buffer．memory 43
3．4．6 compression．type 43
3．4．7 batch．size 43
3．4．8 max．in．flight．requests．per．connection 43
3．4．9 max．request．size 44
3．4．10 receive．buffer．bytes和send．buffer．bytes 44
3．4．11 enable．idempotence 44
3．5　序列化器 45
3．5．1　自定义序列化器 45
3．5．2　使用Avro序列化数据 47
3．5．3　在Kafka中使用Avro记录 48
3．6　分区 51
3．7　标头 52
3．8　拦截器 53
3．9　配额和节流 54
3．10　小结 56
第 4 章 Kafka消费者——从Kafka读取数据 57
4．1 Kafka消费者相关概念 57
4．1．1　消费者和消费者群组 57
4．1．2　消费者群组和分区再均衡 60
4．1．3　群组固定成员 62
4．2　创建 Kafka消费者 63
4．3　订阅主题 63
4．4　轮询 64
4．5　配置消费者 66
4．5．1 fetch．min．bytes 66
4．5．2 fetch．max．wait．ms 66
4．5．3 fetch．max．bytes 66
4．5．4 max．poll．records 67
4．5．5 max．partition．fetch．bytes 67
4．5．6 session．timeout．ms和heartbeat．interval．ms 67
4．5．7 max．poll．interval．ms 67
4．5．8 default．api．timeout．ms 68
4．5．9 request．timeout．ms 68
4．5．10 auto．offset．reset 68
4．5．11 enable．auto．commit 68
4．5．12 partition．assignment．strategy 68
4．5．13 client．id 69
4．5．14 client．rack 69
4．5．15 group．instance．id 70
4．5．16 receive．buffer．bytes和send．buffer．bytes 70
4．5．17 offsets．retention．minutes 70
4．6　提交和偏移量 70
4．6．1　自动提交 71
4．6．2　提交当前偏移量 72
4．6．3　异步提交 73
4．6．4　同步和异步组合提交 74
4．6．5　提交特定的偏移量 75
4．7　再均衡监听器 76
4．8　从特定偏移量位置读取记录 78
4．9　如何退出 79
4．10　反序列化器 80
4．10．1　自定义反序列化器 81
4．10．2　在消费者里使用Avro反序列器 83
4．11 独立的消费者：为什么以及怎样使用不属于任何群组的消费者 83
4．12　小结 84
第 5 章 编程式管理Kafka 85
5．1 AdminClient概览 85
5．1．1　异步和最终一致性API 86
5．1．2　配置参数 86
5．1．3　扁平的结构 86
5．1．4　额外的话 86
5．2 AdminClient生命周期：创建、配置和关闭 87
5．2．1 client．dns．lookup 87
5．2．2 request．timeout．ms 88
5．3　基本的主题管理操作 88
5．4　配置管理 91
5．5　消费者群组管理 92
5．5．1　查看消费者群组 93
5．5．2　修改消费者群组 94
5．6　集群元数据 95
5．7　高级的管理操作 96
5．7．1　为主题添加分区 96
5．7．2　从主题中删除消息 96
5．7．3　首领选举 97
5．7．4　重新分配副本 98
5．8　测试 99
5．9　小结 101
第 6 章 深入Kafka 102
6．1　集群的成员关系 102
6．2　控制器 103
6．3　复制 105
6．4　处理请求 107
6．4．1　生产请求 109
6．4．2　获取请求 109
6．4．3　其他请求 111
6．5　物理存储 112
6．5．1　分层存储 113
6．5．2　分区的分配 114
6．5．3　文件管理 115
6．5．4　文件格式 115
6．5．5　索引 117
6．5．6　压实 117
6．5．7　压实的工作原理 118
6．5．8　被删除的事件 119
6．5．9　何时会压实主题 119
6．6　小结 120
第 7 章 可靠的数据传递 121
7．1　可靠性保证 121
7．2　复制 122
7．3 broker配置 123
7．3．1　复制系数 123
7．3．2　不彻底的首领选举 125
7．3．3　最少同步副本 126
7．3．4　保持副本同步 126
7．3．5　持久化到磁盘 126
7．4　在可靠的系统中使用生产者 127
7．4．1　发送确认 127
7．4．2　配置生产者的重试参数 128
7．4．3　额外的错误处理 129
7．5　在可靠的系统中使用消费者 129
7．5．1　消费者的可靠性配置 130
7．5．2　手动提交偏移量 130
7．6　验证系统可靠性 132
7．6．1　验证配置 132
7．6．2　验证应用程序 133
7．6．3　在生产环境中监控可靠性 133
7．7　小结 134
第 8 章 精确一次性语义 135
8．1　幂等生产者 135
8．1．1　幂等生产者的工作原理 136
8．1．2　幂等生产者的局限性 137
8．1．3　如何使用幂等生产者 138
8．2　事务 138
8．2．1　事务的应用场景 139
8．2．2　事务可以解决哪些问题 139
8．2．3　事务是如何保证精确一次性的 140
8．2．4　事务不能解决哪些问题 141
8．2．5　如何使用事务 143
8．2．6　事务ID和隔离 145
8．2．7　事务的工作原理 146
8．3　事务的性能 148
8．4　小结 148
第 9 章 构建数据管道 149
9．1　构建数据管道时需要考虑的问题 150
9．1．1　及时性 150
9．1．2　可靠性 150
9．1．3　高吞吐量和动态吞吐量 151
9．1．4　数据格式 151
9．1．5　转换 152
9．1．6　安全性 152
9．1．7　故障处理 153
9．1．8　耦合性和灵活性 153
9．2　何时使用Connect API或客户端API 154
9．3 Kafka Connect 154
9．3．1　运行Connect 155
9．3．2　连接器示例：文件数据源和文件数据池 157
9．3．3　连接器示例：从MySQL到ElasticSearch 159
9．3．4　单一消息转换 164
9．3．5　深入理解Connect 167
9．4 Connect之外的选择 169
9．4．1　其他数据存储系统的数据摄入框架 169
9．4．2　基于图形界面的ETL工具 169
9．4．3　流式处理框架 170
9．5　小结 170
第 10 章 跨集群数据镜像 171
10．1　跨集群镜像的应用场景 171
10．2　多集群架构 172
10．2．1　跨数据中心通信的一些现实情况 173
10．2．2　星型架构 173
10．2．3　双活架构 175
10．2．4　主备架构 176
10．2．5　延展集群 180
10．3 MirrorMaker 181
10．3．1　配置MirrorMaker 183
10．3．2　多集群复制拓扑 184
10．3．3　保护MirrorMaker 185
10．3．4　在生产环境中部署MirrorMaker 186
10．3．5 MirrorMaker调优 189
10．4　其他跨集群镜像方案 190
10．4．1 Uber的uReplicator 190
10．4．2 LinkedIn的Brooklin 191
10．4．3 Confluent的跨数据中心镜像解决方案 191
10．5　小结 193
第 11 章 保护Kafka 194
11．1　锁住 Kafka 194
11．2　安全协议 196
11．3　身份验证 197
11．3．1 SSL 198
11．3．2 SASL 201
11．3．3　重新认证 210
11．3．4　安全更新不停机 211
11．4　加密 212
11．5　授权 214
11．5．1 AclAuthorizer 214
11．5．2　自定义授权 217
11．5．3　安全方面的考虑 219
11．6　审计 219
11．7　保护ZooKeeper 220
11．7．1 SASL 220
11．7．2 SSL 221
11．7．3　授权 221
11．8　保护平台 222
11．9　小结 223
第 12 章 管理Kafka 225
12．1　主题操作 225
12．1．1　创建新主题 226
12．1．2　列出集群中的所有主题 227
12．1．3　列出主题详情 227
12．1．4　增加分区 228
12．1．5　减少分区 229
12．1．6　删除主题 229
12．2　消费者群组 230
12．2．1　列出并描述消费者群组信息 230
12．2．2　删除消费者群组 231
12．2．3　偏移量管理 232
12．3　动态配置变更 233
12．3．1　覆盖主题的默认配置 233
12．3．2　覆盖客户端和用户的默认配置 234
12．3．3　覆盖broker的默认配置 235
12．3．4　查看被覆盖的配置 236
12．3．5　移除被覆盖的配置 236
12．4　生产和消费 236
12．4．1　控制台生产者 237
12．4．2　控制台消费者 238
12．5　分区管理 241
12．5．1　首选首领选举 241
12．5．2　修改分区的副本 242
12．5．3　转储日志片段 246
12．5．4　副本验证 248
12．6　其他工具 248
12．7　不安全的操作 249
12．7．1　移动集群控制器 249
12．7．2　移除待删除的主题 249
12．7．3　手动删除主题 250
12．8　小结 250
第 13 章 监控Kafka 251
13．1　指标基础 251
13．1．1　指标来自哪里 251
13．1．2　需要哪些指标 252
13．1．3　应用程序健康检测 253
13．2　服务级别目标 254
13．2．1　服务级别定义 254
13．2．2　哪些指标是好的SLI 255
13．2．3　将SLO用于告警 255
13．3 broker的指标 256
13．3．1　诊断集群问题 257
13．3．2　非同步分区的艺术 257
13．3．3 broker指标 261
13．3．4　主题的指标和分区的指标 268
13．3．5 Java虚拟机监控 269
13．3．6　操作系统监控 270
13．3．7　日志 272
13．4　客户端监控 272
13．4．1　生产者指标 272
13．4．2　消费者指标 274
13．4．3　配额 276
13．5　滞后监控 277
13．6　端到端监控 277
13．7　小结 278
第 14 章 流式处理 279
14．1　什么是流式处理 280
14．2　流式处理相关概念 282
14．2．1　拓扑 282
14．2．2　时间 282
14．2．3　状态 284
14．2．4　流和表 284
14．2．5　时间窗口 285
14．2．6　处理保证 287
14．3　流式处理设计模式 287
14．3．1　单事件处理 287
14．3．2　使用本地状态 288
14．3．3　多阶段处理和重分区 289
14．3．4　使用外部查找：流和表的连接 290
14．3．5　表与表的连接 291
14．3．6　流与流的连接 291
14．3．7　乱序事件 292
14．3．8　重新处理 293
14．3．9　交互式查询 294
14．4 Streams示例 294
14．4．1　字数统计 294
14．4．2　股票市场统计 296
14．4．3　填充点击事件流 298
14．5 Streams架构概览 300
14．5．1　构建拓扑 300
14．5．2　优化拓扑 301
14．5．3　测试拓扑 301
14．5．4　扩展拓扑 302
14．5．5　在故障中存活下来 304
14．6　流式处理应用场景 305
14．7　如何选择流式处理框架 306
14．8　小结 307
附录 A 在其他操作系统中安装Kafka 309
附录 B 其他Kafka工具 314



### 第 1 章 初识Kafka

### 第 2 章 安装Kafka

### 第 3 章 Kafka生产者——向Kafka写入数据
参考
https://gitee.com/edidada/testkafka

jar包
```xml
         <dependency>
          <groupId>org.apache.kafka</groupId>
          <artifactId>kafka-clients</artifactId>
          <version>3.0.0</version>
        </dependency>
```

api
KafkaProducer
org.apache.kafka.clients.producer.KafkaProducer

Producer
org.apache.kafka.clients.producer.Producer

![kafka_Producer](../imgs/mq/kafka_Producer.png)

send()
Future<RecordMetadata> send(ProducerRecord<K, V> record);

![kafka_Future](../imgs/mq/kafka_Future.png)

三个必须配置项
kafka broker地址
org.apache.kafka.clients.producer.ProducerConfig#BOOTSTRAP_SERVERS_CONFIG
org.apache.kafka.clients.producer.ProducerConfig#KEY_SERIALIZER_CLASS_CONFIG
org.apache.kafka.clients.producer.ProducerConfig#VALUE_SERIALIZER_CLASS_CONFIG
kafka消息 kv
k的序列化器
v的序列化器


ShortSerializer (org.apache.kafka.common.serialization)
ListSerializer (org.apache.kafka.common.serialization)
DoubleSerializer (org.apache.kafka.common.serialization)
ByteArraySerializer (org.apache.kafka.common.serialization)
IntegerSerializer (org.apache.kafka.common.serialization)
UUIDSerializer (org.apache.kafka.common.serialization)
StringSerializer (org.apache.kafka.common.serialization)
VoidSerializer (org.apache.kafka.common.serialization)
ByteBufferSerializer (org.apache.kafka.common.serialization)
FloatSerializer (org.apache.kafka.common.serialization)
LongSerializer (org.apache.kafka.common.serialization)
BytesSerializer (org.apache.kafka.common.serialization)



### 第 4 章 Kafka消费者——从Kafka读取数据
KafkaConsumer
public void subscribe(Collection<String> topics) 
ConsumerRecords



### 第 5 章 编程式管理Kafka



### 第 6 章 深入Kafka 



### 第 7 章 可靠的数据传递



### 第 8 章 精确一次性语义



### 第 9 章 构建数据管道



### 第 10 章 跨集群数据镜像

https://cwiki.apache.org/confluence/display/KAFKA/Ecosystem
