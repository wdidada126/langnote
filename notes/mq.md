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

#### DLQ：死信队列 / 死信主题的完整处理模型

死信队列（Dead Letter Queue，DLQ）用于保存**某一消费者组**反复处理失败、且不应继续自动重试的消息。它把异常消息从正常工作流中隔离出来，避免两种坏结果：

1. 毒消息被无限快速重投，占用消费者、连接、下游数据库或第三方配额，进而拖慢甚至阻塞正常消息。
2. 为恢复吞吐而直接丢弃异常消息，造成业务动作、资金/库存变化或审计线索不可追溯的数据丢失。

“死信”是对某个消费链路的状态判断，不是消息的全局属性。同一条订单事件可以被风控消费者成功处理，却因通知服务缺少收件人而进入通知消费者组的 DLQ。因此 DLQ 的命名、权限、监控和处置责任都应至少包含 `业务域 + 原 Topic/Queue + consumer group + 环境`；不要让多个无关消费者共用一个无法定位责任方的 `dlq`。

##### 进入 DLQ 前的决策

只有短暂故障才值得自动重试，例如下游临时超时、连接抖动、依赖限流后可恢复。下列情况通常应尽早结束自动重试或在修复前暂停重放：

| 失败类型 | 典型例子 | 正常处理 |
| --- | --- | --- |
| 瞬时故障 | 网络超时、服务滚动发布、短暂限流 | 有上限的延迟重试，使用退避和抖动。 |
| 业务可等待 | 订单状态尚未推进、依赖数据稍后到达 | 业务定义的延迟重试或补偿任务；必须有最终截止时间。 |
| 不可恢复数据 | schema 不兼容、字段缺失、反序列化失败、违反业务不变量 | 直接 DLQ 或极少次数验证性重试，修复数据/兼容代码后再处理。 |
| 程序缺陷 | 空指针、版本发布错误、固定 SQL 错误 | 触发告警并止损；修复和验证前不要反复重放。 |
| 外部永久拒绝 | 无权限、账号失效、订单已取消且不可逆 | DLQ 后人工补偿、标记终态或按业务规则丢弃。 |

重试阈值不能只写成一个孤立数字。应同时定义最大尝试次数、最大持续时间、单次处理超时、退避曲线、消息业务有效期和熔断条件。例如“最多重试 5 次”如果在数秒内完成，仍可能压垮本已限流的依赖；如果消息的业务有效期只有 10 分钟，数小时的重试又没有意义。重试次数要覆盖可预期的瞬时恢复窗口，但必须在业务截止时间之前结束。

##### DLQ 中应保存什么

DLQ 不是只有原始 payload 的备份队列。至少保留以下可定位和可重放的信息；敏感字段仍应遵守脱敏、加密和最小权限原则：

| 类别 | 建议字段 |
| --- | --- |
| 原始消息 | `event_id`、业务主键、原 topic/queue、partition/offset 或 message id、消息体、schema version、生产时间。 |
| 消费上下文 | consumer group、消费者版本/镜像版本、首次投递时间、最后失败时间、累计投递/重试次数、ACK/超时信息。 |
| 失败诊断 | 异常类型、错误码、截断后的堆栈、失败阶段、下游请求标识、trace id/span id。 |
| 处置审计 | 分类结论、负责人、修复记录、重放批次号、重放时间、最终结果和丢弃依据。 |

原始消息体过大或含敏感信息时，可将 payload 存入受控对象存储/审计库，DLQ 只保存不可变引用、摘要和校验和；但引用的保留期必须不短于 DLQ 处置期，否则会得到一条无法修复的“空死信”。

##### 处置与安全重放

```text
DLQ 告警
  -> 按错误签名聚合，区分单条坏数据与系统性故障
  -> 保留原消息和失败上下文，创建处置工单
  -> 修复代码 / 数据 / 依赖配置，并在隔离环境验证
  -> 以受控速率重放到指定 retry/replay 通道
  -> 目标消费者按 event_id 幂等处理
  -> 成功后记录审计；仍失败则回到 DLQ 或转人工补偿
```

不要把 DLQ 消费者直接“原样写回原 Topic”并无限循环。重放必须具备独立开关、限速、批次范围、目标版本、幂等校验和审计；对于有序消息，要确认重放不会让旧事件覆盖新状态。涉及付款、库存、发券、邮件或第三方调用时，重放前先查业务状态，必要时走补偿命令而不是重复执行原命令。

DLQ 本身也需要可靠性设计：独立的保留期和容量告警、受限写入/读取权限、备份或副本策略、按错误签名的仪表盘，以及“最老死信年龄、增长速率、重放成功率、重复入 DLQ 比例、未处置数量”等指标。没有 owner、SLA 和定期清理/归档策略的 DLQ，只是把丢失延后。

##### 常见消息产品的差异

| 产品 | DLQ 机制 | 需要特别注意 |
| --- | --- | --- |
| RabbitMQ | 队列配置 Dead Letter Exchange（DLX）后，消息可被重新路由到死信目标 | 触发不仅是消费失败且 `requeue=false`，还包括消息 TTL 到期、队列超长和 quorum queue 超过 `delivery-limit`。优先用 policy 配置；若目标 DLX 不存在，消息可能被静默丢弃。`x-death`、`x-first-death-*`、`x-last-death-*` 有助于追踪来源。 |
| Kafka | Kafka broker 的普通 consumer group 没有统一内建 DLQ；应用通常自行生产到专用 DLQ topic | Kafka Connect 支持 `errors.deadletterqueue.topic.name`，可附加错误上下文 header。业务消费者仍须自行设计重试 topic、DLQ topic、提交 offset 的时机和幂等重放。 |
| RocketMQ | broker 按消费者组的重试策略重投；超过最大重试后进入 DLQ | 5.x 文档将其定义为 consumer group 元数据的一部分；4.x PushConsumer 约定死信 topic 为 `%DLQ%<ConsumerGroup>`。DLQ 是消费逻辑的保护措施，不应承担业务流程控制。 |
| Pulsar | 消费者侧 `DeadLetterPolicy` 将达到最大重投次数的消息写入 dead letter topic | 可配 retry letter topic 实现延迟重试；默认名为 `<topic>-<subscription>-DLQ`。要保证最大次数真的生效，应启用 retry 并使用 `reconsumeLater`，而不只依赖内存中的 negative acknowledgment 计数。 |

参考：[RabbitMQ Dead Letter Exchanges](https://www.rabbitmq.com/docs/next/dlx)、[Kafka Connect 错误处理与 DLQ](https://kafka.apache.org/30/kafka-connect/user-guide/)、[RocketMQ 消费重试](https://rocketmq.apache.org/docs/featureBehavior/10consumerretrypolicy/)、[Pulsar Retry Letter Topic 与 Dead Letter Topic](https://pulsar.apache.org/docs/next/concepts-messaging/)。

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
