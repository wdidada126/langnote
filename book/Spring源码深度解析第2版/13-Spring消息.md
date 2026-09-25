# 第 13 章 Spring 消息

> Spring 消息抽象：JMS（`JmsTemplate`、`MessageListenerContainer`、`@JmsListener`）、AMQP/RabbitMQ（`RabbitTemplate`）、消息驱动 POJO（MDP）、事务与确认。讲「Spring 如何统一不同消息中间件」。

## 一、核心精讲

### 13.1 🔧 模板 + 监听容器
- 发送：`JmsTemplate`/`RabbitTemplate`（模板方法，处理连接/Session/异常，见第 8 章模式）；接收：`MessageListenerContainer`（`DefaultMessageListenerContainer`/`SimpleMessageListenerContainer`）多线程拉消息（🔧 容器管理线程与事务，是「并发 + 消息」的结合点）。

### 13.2 消息驱动 POJO
- `@JmsListener`/`@RabbitListener` 把普通方法变成消息处理器，由 `MessageListenerAdapter` 做消息→方法参数转换（🔧 与 SpringMVC 的参数解析器思路一致）。

### 13.3 确认与事务
- `AUTO_ACKNOWLEDGE`/`CLIENT_ACKNOWLEDGE`/事务会话；消息事务与 DB 事务需「最终一致」（🔧 本地消息表/事务消息；RocketMQ 事务消息，见尼恩 15 章可靠投递）。

## 二、版本演进 / 论文 / 前沿

- 文献：JMS 规范（JSR 914）；AMQP 0-9-1；Spring Reference（JMS/AMQP）；Hohpe-Woolf《Enterprise Integration Patterns》(2003)。
- 工业界：RabbitMQ、RocketMQ（22k）、Kafka（29k）、Spring Cloud Stream（统一绑定层）。
- 开源 stars（2026-09）：rocketmq 22k / kafka 29k.

## 三、常见误区

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | "消息与 DB 事务天然一致" | 需事务消息/最终一致 |
| 2 | "Listener 单线程" | 容器多线程，需并发安全 |
| 3 | "AUTO_ACK 不丢消息" | 处理失败会丢，按需 CLIENT/事务 |
