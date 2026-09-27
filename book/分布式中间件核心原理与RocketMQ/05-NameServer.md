# 第 5 章　NameServer

> 原书第 5 章聚焦 RocketMQ 的**路由注册中心 NameServer**：它是什么、Broker 如何注册、
> 系统如何从它获取路由、它如何（以及系统如何）感知 Broker 宕机。NameServer 是 RocketMQ 轻量无状态的
> 「地址簿」，理解它是理解整个集群寻址的前提。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 5.1 NameServer 概述 | 轻量级、无状态、最终一致 | 对标 Zookeeper 但更轻，不参与消息流转 |
| 5.2 与其他组件的交互流程 | Broker 注册、系统获取、宕机感知 | 心跳 + 定期拉取构成路由发现 |
| 5.2.1 Broker 向 NameServer 注册 | 心跳上报 topic/queue/broker 信息 | 每 30s 心跳，NameServer 维护路由表 |
| 5.2.2 系统从 NameServer 获取信息 | Producer/Consumer 拉路由 | 客户端缓存路由，定时刷新 |
| 5.2.3 NameServer 感知 Broker 宕机 | 120s 无心跳则摘除 | 被动失效，不主动探活 |
| 5.2.4 系统感知到 Broker 宕机 | 客户端刷新路由后避开 | 配合主从/重试实现容错 |
| 5.3 小结 | 收束 NameServer 章 | 进入第 6 章高可用 |

## 核心精讲

（以下为教学性梳理，代码均**教学示意，不参与构建**。）NameServer 的设计哲学是「**无状态 + 各节点互不通信**」，
靠客户端心跳与拉取达成最终一致，避免了 Zookeeper 那样强一致的协调开销。

### 5.1 NameServer 的定位

- **无状态**：每个 NameServer 节点独立，不互相复制数据，客户端连任意一个都能拿到全量路由。
- **轻量**：只存路由元数据（Broker 地址、Topic 队列分布），不碰消息体。
- **最终一致**：Broker 向所有 NameServer 心跳，客户端从任一 NameServer 拉取；短暂不一致可容忍。

### 5.2.1–5.2.3 注册与失效（教学示意）

```java
// 教学示意，不参与构建：Broker 心跳注册（伪逻辑）
// 每 30s 向所有 NameServer 发送心跳，携带 brokerAddr / topicQueueTable
heartbeatExecutor.scheduleAtFixedRate(() -> {
    for (NameServer ns : nameServers) ns.registerBroker(brokerInfo);
}, 0, 30, SECONDS);

// NameServer 侧：超过 120s 未收到某 Broker 心跳，则从路由表摘除
if (now - lastHeartbeat > 120_000) routeTable.remove(brokerName);
```

> 关键认知：**NameServer 不主动探活，只「等心跳超时」**。这与 Zookeeper 的临时节点（会话断开即删）不同，
> RocketMQ 选择更简单的设计，把「探活」责任交给超时机制，减少了 NameServer 自身的复杂度。

## 版本演进

- **本书基于 RocketMQ 4.x 的 NameServer**（独立进程，端口 9876，客户端通过 `namesrvAddr` 配置）。
- **🔧 2026 视角：RocketMQ 5.x 的 Proxy 与多语言接入**。5.x 引入 **Proxy** 后，NameServer 之上多了
  gRPC 接入层；NameServer 本身职责大体不变，但「客户端直连 NameServer」的模式在 Proxy 模式下被收敛，
  多语言客户端经由 Proxy 间接寻址，NameServer 更退居内部组件。
- **🔧 2026 视角：NameServer 高可用部署**。生产至少部署 2 个 NameServer（无主从概念，纯多副本），
  原书 5.2 强调「各节点独立、不通信」仍是 2026 的正确心智模型。

## 经典论文与原始文献

| 文献 | 出处 | 贡献 |
| --- | --- | --- |
| RocketMQ 官方架构文档（rocketmq.apache.org/docs） | apache | NameServer 角色与设计权威出处 |
| Hunt 等《ZooKeeper: Wait-free coordination for Internet-scale systems》 | USENIX ATC 2010 | 对比参照：强一致协调服务的设计（RocketMQ 有意不采用） |
| Kafka 设计（Controller + Zookeeper/自管元数据） | Kafka 文档 | 对照：Kafka 用不同机制做元数据协调 |

> 第 5 章是组件章，原书不引论文；上表补 RocketMQ 官方文档与 ZooKeeper 论文，便于理解
> 「为什么 RocketMQ 不用 ZK 而自研轻量 NameServer」这一设计取舍。

## 近年研究与工业界开源实践（2015–2026）

- **实测 star（2026-09，`gh api` 实测）**：

| 项目 | 定位 | star |
| --- | --- | --- |
| `apache/rocketmq` | RocketMQ 本体（含 NameServer） | 22621 |
| `apache/rocketmq-externals` | Dashboard 等（可看 NameServer 路由） | 4592 |
| `apache/zookeeper` | 对照：强一致协调（Kafka 旧元数据底座） | 12811 |
| `etcd-io/etcd` | 对照：云原生协调（K8s 元数据） | 52309 |

- **趋势**：RocketMQ 坚持「轻量自研 NameServer」；而 Kafka 在 2023 年后推进 **KRaft**（去 Zookeeper，
  自管元数据，用 Raft），体现出「元数据协调」两种不同哲学。2026 年考察消息系统时应理解这一差异。

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「NameServer 是 Zookeeper」 | NameServer 无状态、节点不互通信、最终一致；ZK 是强一致协调 |
| 2 | 「NameServer 挂了集群就停」 | 客户端缓存路由，NameServer 全挂仅影响「新路由发现」，已建连仍可跑一段时间 |
| 3 | 「NameServer 参与消息转发」 | NameServer 只管路由，消息走 Broker，绝不经 NameServer |
| 4 | 🔧 本书未提 5.x Proxy 对寻址的改变 | 2026 多语言客户端经 Proxy 间接寻址，NameServer 更内部化 |
| 5 | 🔧 本书未提 Kafka KRaft 去 ZK | 2026 对照阅读：元数据协调的两条路线（轻量 vs Raft） |

## 与其他章 / 其他书的联系

- **本书内**：
  - 5.2 路由发现 → 第 7 章 Producer/Consumer 如何选 Broker 与 MessageQueue；
  - 5.2.3 宕机感知 → 第 6 章高可用（主从/Dledger 接住失效）；
  - 5.1 无状态设计 → 第 9 章 NameServer 源码（启动/网络初始化/Netty）。
- 跨书：可对照 [../分布式中间件技术实战/05-消息中间件RabbitMQ.md](../分布式中间件技术实战/05-消息中间件RabbitMQ.md)
  中 RabbitMQ 用 Erlang 分布式 mnesia 做元数据，与 RocketMQ NameServer 思路不同。
