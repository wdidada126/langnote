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

## 消息队列综合笔记（截至 2026-08）

### MQ 的本质与边界

消息队列/流平台将生产与消费解耦，并提供持久化、缓冲、路由、重试、消费进度和可观测性。它常用于异步化、削峰、事件分发和跨服务数据流；它不是“只要引入 MQ 就自动实现分布式事务”。数据库本地提交、向 broker 发送、消费者执行业务、调用第三方系统是多个独立步骤，网络超时和进程崩溃使重复与不确定结果不可避免。

| 模型 | 代表 | 核心抽象 | 适合 |
| --- | --- | --- | --- |
| Queue / work queue | RabbitMQ、ActiveMQ | 消息由竞争消费者处理，确认后删除/推进 | 任务分发、命令、路由模式复杂的业务集成。 |
| Partitioned log | Kafka、Pulsar | 可保留、可回放的分区日志和消费位点 | 事件流、日志、CDC、流计算和高吞吐多消费者。 |
| 业务消息平台 | RocketMQ | Topic、Group、Tag、顺序/延迟/事务消息 | 交易事件、可靠异步、延迟与顺序业务消息。 |
| 进程内/轻量通信 | ZeroMQ 等 | socket/库，而非完整持久 broker | 低延迟内部通信；可靠存储需自行设计。 |

先定义业务语义，再选产品：消息是命令还是不可变事实事件；是否需要回放；顺序范围是单订单、单账户、单分区还是全局；可接受多久延迟；保留多久；失败后谁补偿；以及数据合规/审计要求。不要先建 Topic 再让业务猜语义。

### 可靠投递：至少一次是默认现实

端到端“恰好一次”通常需要把多个边界拆开讨论：producer 到 broker、broker 副本持久化、broker 到 consumer、consumer 业务库提交、以及外部副作用。producer 收不到 ACK 时，消息可能没有到达，也可能已经持久化而 ACK 丢失；consumer 成功写库后在 ACK 前崩溃时，broker 会重投。因此可靠系统通常选择 **at-least-once 传递 + 幂等业务处理**。

```text
本地事务：写 order + 写 outbox_event（同一 DB 事务）
后台 relay：读取 outbox -> 发送 MQ -> 标记已投递
消费者：按 event_id 去重 -> 写业务结果/inbox -> ACK

任一边超时：允许重试，依靠 event_id/业务唯一键避免重复副作用
```

| 目标 | 必要机制 | 不能替代 |
| --- | --- | --- |
| producer 不静默丢消息 | 超时、重试、broker ACK、持久化与副本确认、outbox | 仅靠客户端 `send()` 返回。 |
| consumer 不漏处理 | 手动 ACK/位点提交在业务成功之后，重试与 DLQ | 先 ACK 再把任务丢给无监督线程。 |
| consumer 幂等 | `event_id`/业务唯一键、inbox/唯一索引、状态机 | 只依赖“broker 不会重复投递”。 |
| 跨服务最终一致 | outbox、补偿、对账、可观测状态 | MQ 事务消息替所有参与者原子提交。 |

RocketMQ 官方说明消费者投递语义为至少一次；事务消息通过 half message、执行本地事务与 broker 回查实现本地事务和消息发送的最终一致，并不保证下游消费与上游状态同步完成。RabbitMQ 的 publisher confirm 只确认 broker/队列已接管消息，consumer acknowledgement 只确认消费处理结果；两者都无法单独消除网络造成的重复。参考：[RocketMQ 事务消息](https://rocketmq.apache.org/docs/featureBehavior/04transactionmessage/)、[RocketMQ FAQ](https://rocketmq.apache.org/docs/faq/)、[RabbitMQ confirms](https://www.rabbitmq.com/docs/next/confirms)。

### 顺序、并发、重试与死信

顺序永远有范围。Kafka 的顺序通常仅在一个 partition 内；RocketMQ 顺序消息通常按 sharding key/queue；RabbitMQ 在多个消费者、重投和优先级下不能假设全局顺序。把同一订单/账户/聚合根映射到同一分区或同一有序队列，消费端按键串行化；若要求跨所有键全局顺序，吞吐与可用性会明显下降。

重试解决短暂故障，不解决永久数据错误或系统过载。重试应具有指数退避、最大次数、可观测原因和 DLQ；DLQ 不是垃圾桶，必须有告警、查询、修复、重放和审计流程。对毒消息先区分 schema 不兼容、缺失依赖、权限、业务状态、超时和代码 bug，再决定修复后重放、人工补偿还是丢弃。

```text
Ready -> Inflight -> 成功 ACK/提交位点
                   -> 暂时失败：延迟重试
                   -> 超过阈值：DLQ + 告警 + 人工/自动处置
```

不要把“返回消费失败”当限流手段。持续过载会形成 retry storm 并挤占正常流量；应使用 consumer 并发/拉取批次/预取、配额、背压、暂停消费或上游限流。RocketMQ 官方也将消费重试定位为偶发处理失败的保护机制，而不是业务流程控制或节流工具。

### schema、Topic 与治理

消息是长期 API。定义 `event_id`、`event_type`、`occurred_at`、producer、schema version、业务主键、trace context 和幂等键；payload 使用明确的 JSON Schema/Avro/Protobuf 等契约。演进采用向后/向前兼容策略：新增可选字段通常安全，删除/改语义/改枚举/改单位要走新版本或双读期。禁止把完整数据库行、密码、token、无界大对象或依赖内部字段直接塞进消息。

Topic 不应只是“一个业务系统一个 Topic”或“每种事件一个 Topic”的口号。按事件边界、保留/权限、吞吐、分区/顺序键、消费者群体和回放需求划分；Tag/filter 是辅助筛选，不应掩盖完全不同的生命周期和安全边界。生产前明确 retention、compaction、分区数、单消息大小、延迟等级、重试/DLQ、ACL、加密、跨区域复制和成本。

### 产品选择与运行

| 需求 | 优先评估 | 核心验证 |
| --- | --- | --- |
| 高吞吐事件流、回放、流计算 | Kafka/Pulsar | partition 热点、consumer lag、保留成本、再均衡和 schema。 |
| 灵活 exchange/routing、工作队列 | RabbitMQ | publisher confirms、manual ACK、prefetch、quorum queue 与故障恢复。 |
| 交易事件、延迟/顺序/事务消息 | RocketMQ | 事务回查、消费幂等、重试/DLQ、Broker/NameServer 容量。 |
| 已有 JMS/传统集成 | ActiveMQ Artemis 等 | 协议兼容、升级路径和运维生态。 |

集群健康不只看 broker 存活：监控 producer error/latency、未确认消息、入/出流量、partition 或 queue 深度、consumer lag、重试/DLQ、磁盘与副本 ISR/仲裁、连接/文件句柄、GC、网络、ACL 拒绝和 schema 失败率。压测必须包含慢消费者、broker 重启、网络分区、重复投递、消息乱序、DLQ 重放和磁盘满，而不是只测单 producer 的发送 QPS。

仓库可继续参考 [RabbitMQ](RabbitMQ.md)、[AMQP](AMQP.md)、[RocketMQ](../java/rocketmq/rocketmq.md)、[Kafka](../java/kafka/kafka.md)。能写清事件语义、幂等键、ACK 时机、重试/DLQ、顺序范围和对账路径，才算完成 MQ 设计。
