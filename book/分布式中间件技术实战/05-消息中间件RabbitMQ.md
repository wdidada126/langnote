# 第 5 章　消息中间件 RabbitMQ

> 原书第 5 章是**消息队列的理论章**：讲清 RabbitMQ 是什么、Spring Boot 怎么整合、几种消息模型怎么写，
> 重点讲**确认消费机制**（保证不丢消息），最后用一个「用户登录成功写日志」的场景把异步解耦落下来。
> 这是第 6 章死信/延迟队列的基础。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 5.1 RabbitMQ 简介 | AMQP 协议、Broker/Exchange/Queue/Binding、Erlang 实现 | RabbitMQ 是 AMQP 主流实现，路由灵活 |
| 5.2 Spring Boot 整合 RabbitMQ | starter + `spring.rabbitmq.*` 配置 | 自动装配出 `RabbitTemplate` 与监听容器 |
| 5.3 多种消息模型实战 | 直连/扇出/主题/头部交换机 | 不同 Exchange 类型决定路由语义 |
| 5.4 确认消费机制 | 生产者 Confirm、消费者 ACK/NACK、手动 ACK | 保证「不丢消息」是 MQ 的核心诉求 |
| 5.5 登录成功写日志实战 | 登录后发消息、异步写日志，解耦主流程 | 典型「异步化」场景 |
| 5.6 总结 | 收束 MQ 理论章 | 下一章用死信/延迟队列进阶 |

## 核心精讲

（以下为教学性梳理，代码均**教学示意，不参与构建**。）

### 5.1 RabbitMQ 核心概念

- **AMQP 模型**：Producer → **Exchange**（按路由键路由）→ **Queue** ← Consumer。
- **Exchange 类型**：

| 类型 | 路由语义 | 典型用途 |
| --- | --- | --- |
| Direct | 精确匹配 routing key | 点对点、任务分发 |
| Fanout | 广播到所有绑定队列 | 事件通知 |
| Topic | 通配符 `#`/`*` 匹配 | 按主题分类（日志级别等） |
| Headers | 按消息头匹配 | 少用 |

### 5.2–5.3 整合与模型（教学示意）

```yaml
# 教学示意，不参与构建：application.yml
spring:
  rabbitmq:
    host: localhost
    port: 5672
    username: guest
    password: guest
```

```java
// 教学示意，不参与构建：发消息 + 收消息
rabbitTemplate.convertAndSend("user.exchange", "user.login", loginEvent);

@RabbitListener(queues = "user.login.log")
public void handle(LoginEvent e) { logService.save(e); }  // 异步写日志
```

### 5.4 确认消费机制（本章重点）

- **生产者端 Confirm**：Broker 收到消息后回 ack，未收到可重发——防「发丢」。
- **消费者端 ACK/NACK**：处理成功回 `basicAck`，失败/`NACK` 可 requeue 或进死信——防「消费丢」。
- **务必用手动 ACK**：自动 ACK 会在消息**刚投递就确认**，处理崩了就丢；手动 ACK 在业务处理完再确认。

```java
// 教学示意，不参与构建：手动 ACK
@RabbitListener(queues = "q")
public void on(Message m, Channel c) throws IOException {
    try {
        business(m);
        c.basicAck(m.getMessageProperties().getDeliveryTag(), false);
    } catch (Exception e) {
        c.basicNack(m.getMessageProperties().getDeliveryTag(), false, true); // 重入队
    }
}
```

### 5.5 登录写日志实战

- 主流程只管「登录成功」，发一条消息到 MQ；日志服务异步消费并落库——**主流程不被日志 IO 拖慢**，
  这就是消息队列「异步解耦」的典型价值。

## 版本演进

- **本书基于 RabbitMQ 3.x（Erlang）**；到 2026 年 RabbitMQ 仍在活跃演进（4.x 主线）。
- **🔧 Quorum Queue（仲裁队列）**：替代镜像队列（mirror queue，已废弃），基于 Raft 提供更强一致与容错；
  本书讲的「镜像队列高可用」在 2026 年应改写为 Quorum Queue。
- **🔧 流式队列 Stream Queue**：RabbitMQ 3.9+ 引入，支持重复消费、多消费者偏移，逼近 Kafka 能力；
  本书未覆盖。
- **🔧 消息队列选型格局变化**：2020 年 RabbitMQ 是 Java 生态默认；2026 年高吞吐/日志场景大量转向
  Kafka / RocketMQ / Pulsar（见 00-缺口与第 6 章）。RabbitMQ 仍适合「低延迟、复杂路由、任务分发」。

## 经典论文与原始文献

| 文献 | 出处 | 贡献 |
| --- | --- | --- |
| AMQP 0-9-1 协议规范（OASIS / rabbitmq.com） | rabbitmq.com | RabbitMQ 所实现的协议权威出处 |
| RabbitMQ 官方文档（rabbitmq.com/documentation） | rabbitmq.com | 交换机/队列/确认/Quorum 的权威出处 |
| Vinoski《Advanced Message Queuing Protocol》 | IEEE Internet Computing 2006 | AMQP 设计背景 |

> 第 5 章是工程实战章，原书不引论文；上表补协议与文档出处。

## 近年研究与工业界开源实践（2015–2026）

- **实测 star（2026-09，`gh api` 实测）**：

| 项目 | 定位 | star |
| --- | --- | --- |
| `rabbitmq/rabbitmq-server` | RabbitMQ 本体（Erlang） | 13880 |
| `rabbitmq/rabbitmq-java-client` | Java 客户端（Spring AMQP 底层） | 1313 |
| `spring-projects/spring-amqp` | Spring 对 AMQP 的抽象层 | 860 |
| `spring-projects/spring-boot` | 项目基座 | 81511 |

- **Kafka / RocketMQ / Pulsar 在「高吞吐、日志、流处理」场景持续挤压 RabbitMQ 份额**；
  但 RabbitMQ 凭借灵活路由、低延迟、易上手，在「任务队列、事件通知、复杂 routing」仍占优。
- **云托管**：云厂商托管 RabbitMQ / Kafka / MQ 已成主流，呼应 00-实验工具链。

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「消息队列=异步，所以不会丢」 | 不配 Confirm/ACK 一样丢；可靠性要显式开启 |
| 2 | 「自动 ACK 方便」 | 自动 ACK 在投递即确认，处理失败即丢；生产用手动 ACK |
| 3 | 「消息发出就消费成功」 | 需幂等消费（重复投递常见），消费端去重 |
| 4 | 「RabbitMQ 能当数据库」 | MQ 是管道不是存储；消息应小、可丢失可重放，落地靠 DB |
| 5 | 🔧 本书镜像队列高可用 | 2026 用 Quorum Queue（Raft），镜像队列已废弃 |
| 6 | 🔧 本书未提 Stream Queue | 3.9+ 流式队列支持重复消费/偏移，逼近 Kafka |
| 7 | 🔧 本书只讲 RabbitMQ | 2026 应选型对照 Kafka/RocketMQ/Pulsar（见 00-缺口） |

## 与其他章 / 其他书的联系

- **本书内**：
  - 5.2 整合 → [02-搭建微服务项目.md](02-搭建微服务项目.md)；
  - 5.4 确认机制 → [06-死信队列延迟队列实战.md](06-死信队列延迟队列实战.md)（失败消息进死信）；
  - 5.5 异步解耦思想 → [04-Redis典型应用场景实战之抢红包系统.md](04-Redis典型应用场景实战之抢红包系统.md)（4.7 异步化）。
- [../RabbitMQ实战指南.md](../RabbitMQ实战指南.md)、[../深入RabbitMQ.md](../深入RabbitMQ.md)
  ——RabbitMQ 集群、镜像/Quorum、模式的系统讲法，补本章高可用。
- [../分布式消息中间件实践.md](../分布式消息中间件实践.md)、[../Kafka权威指南.md](../Kafka权威指南.md)
  ——消息中间件横向选型，补本书只讲 RabbitMQ 的缺口。
