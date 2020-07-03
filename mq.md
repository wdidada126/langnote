# mq

考虑是否支持分布式事务

分布式事务大部分是mq实现的

### ActiveMQ



Artemis

The Next Generation Message Broker by ActiveMQ

#### AMQP
amqp
#### RabbitMQ

rabbitmq

#### Kafka

https://zhuanlan.zhihu.com/p/101556617 

RocketMQ建议一个业务系统只使用一个Topic，不同类型的消息通过tag来区分。tag可以在构造Message的时候指定，下面代码就指定了发送的消息的tag都为tag0。 

 https://blog.csdn.net/elim168/article/details/103747754 



消息队列主要解决了应用耦合、异步处理、流量削锋等问题。

当前使用较多的消息队列有RabbitMQ、RocketMQ、ActiveMQ、Kafka、ZeroMQ、MetaMq等



#### 二、消息队列使用场景

消息队列在实际应用中包括如下四个场景：

- 应用耦合：多应用间通过消息队列对同一消息进行处理，避免调用接口失败导致整个过程失败；
- 异步处理：多应用对消息队列中同一消息进行处理，应用间并发处理消息，相比串行处理，减少处理时间；
- 限流削峰：广泛应用于秒杀或抢购活动中，避免流量过大导致应用系统挂掉的情况；
- 消息驱动的系统：系统分为消息队列、消息生产者、消息消费者，生产者负责产生消息，消费者(可能有多个)负责对消息进行处理；

下面详细介绍上述四个场景以及消息队列如何在上述四个场景中使用：