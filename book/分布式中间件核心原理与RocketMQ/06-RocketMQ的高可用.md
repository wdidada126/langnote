# 第 6 章　RocketMQ 的高可用

> 原书第 6 章是 **RocketMQ 运维与高可用的核心章**：讲 Broker 主从架构（同步/读写分离/宕机处理）、
> Dledger 如何实现自动切换与选主、横向对比 RabbitMQ/Kafka 高可用，最后给三套实战——
> 部署集群、可视化监控、生产参数调优。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 6.1 Broker 的主从架构 | 主从同步、读写分离、宕机处理、Dledger | 主从解决「单点」，Dledger 解决「自动切换」 |
| 6.1.1 主从消息同步 | 主写从同步 | 异步复制高性能、同步双写更可靠 |
| 6.1.2 读写分离 | 从节点承担读（消费） | 分担主压力 |
| 6.1.3 主宕机处理 | 从节点继续提供读，写需切换 | 纯主从不自动切换，需 Dledger |
| 6.1.4 Dledger 实现高可用 | Raft 式日志复制 | 自动选主、自动切换 |
| 6.2 Dledger 的自动切换原理 | 替换 CommitLog、选主、数据同步 | 基于 Raft，多数派存活即可服务 |
| 6.3 其他消息中间件的高可用 | RabbitMQ（镜像/Quorum）、Kafka | 各 MQ 高可用思路对比 |
| 6.4 部署一个 RocketMQ 集群 | 单机/3 机 NameServer/3 机 Broker | 实战落地 |
| 6.5 可视化监控管理 | 部署控制台、使用控制台 | 用 Dashboard 看集群状态 |
| 6.6 生产环境参数调整 | OS/JVM/RocketMQ 参数 | 性能与稳定调优 |
| 6.7 小结 | 收束高可用章 | 进入第 7 章生产者消费者 |

## 核心精讲

（以下为教学性梳理，代码均**教学示意，不参与构建**。）本章重点是「**主从 vs Dledger**」与「**复制策略**」。

### 6.1.1 主从同步：异步复制 vs 同步双写

| 策略 | 机制 | 优点 | 缺点 |
| --- | --- | --- | --- |
| 异步复制 | 主写成功即返回，异步推从 | 低延迟、高吞吐 | 主宕可能丢未同步消息 |
| 同步双写 | 主从都写成功才返回 | 不丢消息 | 延迟升高、可用性下降（从挂则写失败） |

### 6.2 Dledger（Raft 日志复制，教学示意）

```text
# 教学示意，不参与构建：Dledger 选主与复制（概念模型）
- 一组 Broker（如 3 节点）组成 Dledger Group，只有 Leader 提供写；
- Leader 把消息作为 Raft 日志 append，多数派（≥2/3）确认才算提交；
- Leader 宕机，剩余节点重新选主（任期 term + 日志最新者胜出）；
- CommitLog 由 Dledger 接管，保证切换后数据连续不丢。
```

> 关键认知：**纯主从（6.1）不自动切换**——主挂了从能读但不能自动顶上写，需人工或 Dledger。
> **Dledger 用 Raft 把「选主 + 日志复制」标准化**，是实现「故障自动切换、消息不丢」的推荐路径。

### 6.3 其他 MQ 高可用对照

| MQ | 高可用机制 |
| --- | --- |
| RabbitMQ | 镜像队列（老，已废弃）→ **Quorum Queue（Raft）** |
| Kafka | 多副本 + ISR + Controller（2023 后 KRaft 去 ZK） |
| RocketMQ | 主从 + Dledger（Raft） |

## 版本演进

- **本书基于 RocketMQ 4.x 主从 + Dledger（Raft）**，监控用 `rocketmq-externals` 的 Dashboard 控制台。
- **🔧 2026 视角：云原生部署**。除裸机部署外，2026 多用 `apache/rocketmq-operator`（K8s StatefulSet + Operator）
  或云厂商托管，主从/Dledger 的运维被平台吸收。
- **🔧 2026 视角：可观测性升级**。原书 6.5 的「控制台」在 2026 应扩展为
  **Prometheus + Grafana + RocketMQ Exporter（或 5.x 内置 metrics）** 的指标体系，
  看 TPS、堆积量、P99、消费滞后（lag），而非只看控制台面板。
- **🔧 2026 视角：Kafka KRaft**。Kafka 已去 Zookeeper（6.3 的 Kafka 高可用描述在 2026 应改写为 KRaft/Raft）。

## 经典论文与原始文献

| 文献 | 出处 | 贡献 |
| --- | --- | --- |
| Ongaro & Ousterhout《In Search of an Understandable Consensus Algorithm (Raft)》 | USENIX ATO 2014 | Dledger 选主/复制的理论底座 |
| RocketMQ Dledger 文档（github.com/apache/rocketmq/tree/master/docs/cn） | apache | Dledger 实现权威出处 |
| RabbitMQ Quorum Queue 文档（rabbitmq.com） | rabbitmq.com | 镜像队列替代方案 |
| Kafka KRaft 文档（kafka.apache.org） | apache | Kafka 去 ZK 元数据协调 |

> 第 6 章是实战章，原书不引论文；上表补 Raft 论文与各 MQ 官方文档。

## 近年研究与工业界开源实践（2015–2026）

- **实测 star（2026-09，`gh api` 实测）**：

| 项目 | 定位 | star |
| --- | --- | --- |
| `apache/rocketmq` | RocketMQ 本体 | 22621 |
| `apache/rocketmq-externals` | 官方 Dashboard 控制台 | 4592 |
| `apache/rocketmq-operator` | K8s Operator 部署 | 336 |
| `apache/kafka` | Kafka（KRaft） | 33854 |
| `rabbitmq/rabbitmq-server` | RabbitMQ（Quorum Queue） | 13880 |

- **趋势**：消息中间件高可用从「主从 + 人工切换」全面走向「Raft 自动切换」（RocketMQ Dledger、
  Kafka KRaft、RabbitMQ Quorum 同此潮流）；运维侧从「控制台」走向「Prometheus 指标体系」。

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「主从 = 高可用」 | 纯主从不自动切换，主挂需人工/Dledger |
| 2 | 「异步复制也能不丢」 | 异步复制主宕会丢未同步消息，零丢失需同步双写/Dledger |
| 3 | 「从节点能自动顶写」 | 仅 Dledger/Raft 组能自动选主接管写 |
| 4 | 🔧 本书监控只讲控制台 | 2026 必须补 Prometheus + Grafana + Exporter 指标 |
| 5 | 🔧 本书 6.3 Kafka 高可用偏旧 | 2026 应改写为 KRaft（去 Zookeeper） |
| 6 | 🔧 本书未提云原生部署 | 2026 可补 rocketmq-operator / 托管云服务 |

## 与其他章 / 其他书的联系

- **本书内**：
  - 6.1/6.2 高可用 → 第 7 章 Broker 持久化与刷盘、第 8 章消息不丢（同步刷盘配合）；
  - 6.4 部署 → 第 3 章容器、第 12 章电商集群；
  - 6.5 监控 → 第 8 章问题排查的可观测底座。
- 跨书：[../分布式中间件技术实战/05-消息中间件RabbitMQ.md](../分布式中间件技术实战/05-消息中间件RabbitMQ.md)
  中 RabbitMQ 镜像队列→Quorum 的演变，可与 6.3 对读。
