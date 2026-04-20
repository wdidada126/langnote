# pika

# 一、`import pika` 到底是啥？一句话总结
pika = RabbitMQ 官方推荐、纯Python实现的 AMQP 0-9-1 协议客户端库
你写Python生产者/消费者，必须用pika跟RabbitMQ服务器通信，它负责：TCP连接、协议编码解码、创建信道、声明交换机队列、发送消息、消费消息、ACK确认、重连、限流、持久化等全部底层网络通信。

> RabbitMQ官方教程强制使用pika，不是第三方杂牌库。

# 二、官方主页、代码仓库、文档（全部官方地址）
## 1. GitHub 开源代码仓库（主仓库）
https://github.com/pika/pika
- 协议：BSD-3-Clause 开源
- 纯Python实现，无C扩展依赖
- 支持同步`BlockingConnection`、异步`SelectConnection`两种模式
- 支持Python 3.7+

## 2. 官方主页（项目官网）
https://pika.github.io/

## 3. 官方详细文档（ReadTheDocs）
https://pika.readthedocs.io/

## 4. RabbitMQ官方教程（pika示例）
https://www.rabbitmq.com/tutorials/tutorial-one-python.html

# 三、pika 核心定位（面试可直接背）
1. AMQP 0-9-1 协议纯Python客户端（RabbitMQ标准协议）
2. RabbitMQ官方唯一推荐Python客户端
3. 提供：连接、信道、交换机、队列、发布、消费、ACK、事务、死信、TLS、背压限流全套API
4. 非线程安全（Connection/Channel不能多线程共用，面试高频坑）
5. 同步阻塞 / 异步回调双模式

# 四、你要的：真正 RabbitMQ 生产者（pika完整版标准代码）
```python
import pika

# 1. 连接RabbitMQ服务
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host="127.0.0.1",
        port=5672,
        credentials=pika.PlainCredentials("guest", "guest")
    )
)
# 2. 创建信道（所有操作都在channel，不要直接用connection）
channel = connection.channel()

# 3. 声明队列（幂等，不存在才创建）
channel.queue_declare(queue="demo_queue", durable=True)

# 4. 生产者发布消息（真正发送）
channel.basic_publish(
    exchange="",          # 默认交换机
    routing_key="demo_queue",
    body=b"hello rabbitmq pika producer",
    properties=pika.BasicProperties(
        delivery_mode=2, # 消息持久化
    )
)

print("消息发送成功")
connection.close()
```

# 五、补充：和你之前Java RabbitTemplate对比
- Java：Spring AMQP / RabbitTemplate（封装pika同款AMQP客户端）
- Python：原生pika（最底层、最正宗、官方标准）

需要我再给你写一份pika消费者+ACK手动确认+消息持久化完整代码吗？
