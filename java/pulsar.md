# pulsar

是的，Apache Pulsar是一个分布式的消息和流处理平台，与传统的消息队列系统不同，Pulsar采用了存储和计算分离的架构。

在传统的消息队列系统中，存储和计算通常是耦合在一起的。消息被写入队列后，存储和计算都在同一个节点上进行处理。这种架构在规模较小的系统中效果良好，但在大规模系统中可能会面临扩展性和性能的挑战。

Pulsar通过将存储和计算分离，实现了更高的可扩展性和灵活性。消息被写入持久化的存储层（称为存储服务），而计算逻辑（如消费者）则可以从存储服务中读取消息进行处理。存储服务可以横向扩展以处理大规模的数据量，而计算节点可以根据需要进行动态伸缩。

这种分离的架构带来了一些好处：
- 可以独立扩展存储和计算能力，根据需求分别进行优化和调整。
- 存储和计算节点可以部署在不同的硬件或云环境中，提供更大的灵活性和弹性。
- 可以实现多租户的架构，不同的租户可以共享相同的存储服务而独立进行计算。
总体而言，Pulsar的存储和计算分离架构为构建大规模、高可扩展性的消息和流处理系统提供了更好的基础。

https://pulsar.apache.org/

https://github.com/apache/pulsar

Java写的

## 版本

3.0.0 2023.04发布

pulsar-2.2.0                2018-10-23 22:58  
pulsar-2.2.1                2018-12-24 20:13  
pulsar-2.3.0                2019-02-21 05:04  
pulsar-2.3.1                2019-04-13 00:53  
pulsar-2.3.2                2019-05-30 18:41  
pulsar-2.4.0                2019-07-02 08:35  
pulsar-2.4.1                2019-09-03 06:15  
pulsar-2.4.2                2019-12-04 05:13  
pulsar-2.5.0                2020-01-15 10:37  
pulsar-2.5.1                2020-04-20 07:51  
pulsar-2.5.2                2020-05-18 23:36  
pulsar-2.6.0                2020-07-03 04:10  
pulsar-2.6.1                2020-11-05 18:51  
pulsar-2.6.2                2020-11-09 05:32  
pulsar-2.6.3                2021-01-21 03:44  
pulsar-2.6.4                2021-06-02 17:03  
pulsar-2.7.0                2020-11-30 13:44  
pulsar-2.7.1                2021-03-16 02:42  
pulsar-2.7.2                2021-05-10 09:45  
pulsar-2.7.3                2021-08-02 13:45  
pulsar-2.7.4                2021-12-24 02:38  
pulsar-2.7.5                2022-09-01 12:20  
pulsar-2.8.0                2021-06-15 09:30  
pulsar-2.8.1                2021-09-07 13:33  
pulsar-2.8.2                2021-12-29 08:13  
pulsar-2.8.3                2022-06-17 11:41  
pulsar-2.8.4                2022-09-02 09:02  
pulsar-2.9.0                2021-11-25 11:23  
pulsar-2.9.1                2022-06-17 11:42  
pulsar-2.9.2                2022-06-17 11:40  
pulsar-2.9.3                2022-07-18 02:38  
pulsar-2.9.4                2022-12-29 07:39  
pulsar-2.9.5                2023-04-21 02:31  

pulsar-2.10.0               2022-06-17 11:39  
pulsar-2.10.1               2022-06-28 15:43  
pulsar-2.10.2               2022-10-19 02:43  
pulsar-2.10.3               2023-01-04 03:42  
pulsar-2.10.4               2023-04-20 09:26  
pulsar-2.10.5               2023-07-30 12:04  
pulsar-2.11.0               2023-01-10 06:28  
pulsar-2.11.1               2023-04-19 03:23  
pulsar-2.11.2               2023-07-18 08:22  


pulsar-3.0.0                2023-05-02 22:40  
pulsar-3.0.1                2023-08-04 09:59  
pulsar-3.1.0                2023-08-14 02:12  

存储和计算分离？

中国银行用？

在腾讯中应该有不同BG的不同团队，都在使用Pulsar中
https://zhuanlan.zhihu.com/p/357351711

张超，腾讯数据平台部 MQ 团队高级工程师；Apache TubeMQ(incubating) PMC；Kafka-on-Pulsar Maintainer；Apache Pulsar Contributor

Pulsar也不是特别年轻的项目了，2013年开始开发，2017年正式开源。
秦金卫 中行用Pulsar
### todo
消息队列需要存储哪些数据？
需要哪些计算？

Pulsar shell 
Offloaders
Connectors
Pulsar Manager
Pulsar Adapters
Pulsar C++ Client

## 书籍 book

Mastering Apache Pulsar Cloud Native Event Streaming at Scale 
Apache Pulsar in Action (David... (Z-Library).pdf

## source code
git clone -b v3.1.2 https://github.com/apache/pulsar.git
cd pulsar
./mvnw install -DskipTests
cd ../
git clone -b v0.5.3 https://github.com/apache/pulsar-client-reactive.git
cd pulsar-client-reactive
./gradlew build

## 多租户

你问得非常好！我们来深入解释 Apache Pulsar 的“多租户”（Multi-tenancy） 到底是什么意思，以及它是否涉及 消息、Topic 的隔离。

##  一、什么是 Pulsar 的“多租户”？

在 Apache Pulsar 中，多租户 是指：  
> 一个 Pulsar 集群可以安全地服务于多个独立的用户、团队或应用（即“租户”），每个租户拥有独立的命名空间、资源配额、权限控制和隔离机制，互不干扰。

这就像一栋写字楼（Pulsar 集群）出租给多个公司（租户），每家公司有自己的办公室、门禁、网络和资源配额。

##  二、多租户的核心组成：层级命名空间

Pulsar 的多租户是通过 层级命名空间（Hierarchical Namespace） 实现的：

```
persistent://租户/命名空间/Topic
```

### 示例：
```bash
persistent://acme-corp/team-logs/prod-nginx-logs
persistent://acme-corp/team-analytics/user-clicks
persistent://partner-xyz/iot-data/sensor-updates
```

其中：
- `acme-corp`, `partner-xyz`：租户（Tenant）
- `team-logs`, `team-analytics`, `iot-data`：命名空间（Namespace）
- `prod-nginx-logs`, `user-clicks`：Topic

##  三、多租户是否实现消息和 Topic 隔离？

###  是的，Pulsar 的多租户实现了严格的隔离，包括：

| 隔离维度 | 是否支持 | 说明 |
|---------|----------|------|
| Topic 隔离 |  是 | 不同租户的 Topic 名字空间完全独立 |
| 消息隔离 |  是 | 消息存储、访问、权限控制按租户/命名空间隔离 |
| 权限控制 |  是 | 可为租户设置独立的认证和授权（如 JWT、OAuth） |
| 资源配额 |  是 | 可限制每个租户的带宽、内存、Topic 数量 |
| 存储隔离 |  是（可选） | 可配置不同租户使用不同的 BookKeeper 集群 |
| 网络隔离 |  是 | 可结合 VPC、防火墙实现租户间网络隔离 |


##  四、具体隔离机制详解

### 1. 命名空间隔离（Namespace Isolation）

- 一个租户可以有多个命名空间（如 `dev`, `prod`, `staging`）
- 每个命名空间可独立配置：
  - 消息 TTL
  - 存储配额
  - 副本数（ensemble size）
  - 生产/消费速率限制
  - 认证权限

```bash
# 创建租户
bin/pulsar-admin tenants create acme-corp --admin-roles=admin@acme-corp

# 创建命名空间
bin/pulsar-admin namespaces create acme-corp/prod

# 设置配额
bin/pulsar-admin namespaces set-backlog-quota acme-corp/prod \
  --limit 10G --policy producer_request_hold
```

### 2. 权限与认证隔离

- 每个租户可配置独立的 认证机制（如 JWT、Kafka SASL、OAuth2）
- 可精细控制：
  - 哪些用户/应用可以访问该租户
  - 能否创建 Topic
  - 能否生产/消费消息

```bash
# 授权 user@acme-corp 在 acme-corp/prod 命名空间下有生产权限
bin/pulsar-admin namespaces grant-permission acme-corp/prod \
  --role user@acme-corp --actions produce,consume
```

### 3. 资源配额隔离

- 防止某个租户“耗尽”整个集群资源
- 可设置：
  - 带宽（publish/consume rate）
  - 内存使用
  - 磁盘配额（backlog quota）

```bash
# 限制 acme-corp/prod 的生产速率
bin/pulsar-admin namespaces set-publish-rate acme-corp/prod \
  --msg-publish-rate 1000 --byte-publish-rate 1048576
```

### 4. 存储隔离（可选）

- Pulsar 支持 计算与存储分离（Broker + BookKeeper）
- 可为不同租户分配不同的 BookKeeper 集群，实现物理存储隔离
- 适用于金融、医疗等对数据隔离要求极高的场景

##  五、对比 Kafka 的多租户能力

| 特性 | Apache Pulsar | Apache Kafka |
|------|---------------|--------------|
| 原生多租户支持 |  是（核心设计） |  否（需外部实现） |
| 租户级命名空间 |  是 |  无（Topic 名称无层级） |
| 租户级权限控制 |  精细控制 |  较弱（需 Kafka ACL + 外部系统） |
| 租户级资源配额 |  支持 |  有限（如 quota） |
| 租户间 Topic 隔离 |  是（通过租户/命名空间） |  否（所有 Topic 扁平共存） |

>  Kafka 本质上是“单租户”系统，多租户需要通过命名规范（如 `acme-logs`, `xyz-events`）和外部权限系统模拟，容易出错。


##  六、多租户的典型应用场景

| 场景 | 说明 |
|------|------|
| SaaS 平台 | 每个客户是一个租户，数据完全隔离 |
| 企业内部共享消息平台 | 不同部门（财务、研发、运营）作为不同租户 |
| 云服务商 | 提供 Pulsar 即服务（PaaS），多个客户共享集群 |
| 微服务架构 | 每个业务域（domain）使用独立命名空间 |

##  总结

| 问题 | 回答 |
|------|------|
| Pulsar 的多租户是什么？ | 支持多个独立用户/团队共享一个集群，互不干扰 |
| 是否实现消息和 Topic 隔离？ |  是，通过 `租户/命名空间/Topic` 层级结构实现 |
| 如何隔离？ | 命名空间、权限、配额、存储、网络等多维度隔离 |
| 相比 Kafka 有何优势？ | Pulsar 是原生多租户，Kafka 是事后补充，Pulsar 更安全、更易管理 |

>  一句话总结：  
> Pulsar 的多租户不是“功能”，而是架构设计的核心原则，它让 Pulsar 天然适合云原生、SaaS 和大规模企业级部署。

这也是它被视为 Kafka有力竞争者的关键原因之一。

你说的应该是 Apache Pulsar（常被误写为 Pular MQ）。它是下一代云原生消息流平台，相比 Kafka、RocketMQ、RabbitMQ，核心优势在于：存算分离、无限扩容、强多租户、跨地域复制、统一队列与流、海量 Topic 支持、分层存储。

下面从架构、功能、场景做清晰对比，突出 Pulsar 独有的优势。

---

## 一、Pulsar 核心架构（决定优势的根本）
Pulsar 采用三层云原生架构：
- Broker（无状态计算层）：负责消息路由、生产消费、负载均衡
- BookKeeper（分布式存储层）：负责持久化、多副本、分片存储
- ZooKeeper / Pulsar Metadata Store：元数据管理


与其他 MQ 最大区别：计算与存储彻底分离

---

## 二、Pulsar vs Kafka：核心优势
### Kafka 特点
- 高吞吐、日志型、分区绑定 Broker、存储与计算耦合
- 适合大数据日志、流处理、高吞吐低延迟场景

### Pulsar 相对 Kafka 的优势
1. 真正无限水平扩展
   - Kafka：分区数有限、扩容需数据迁移、Rebalance 卡顿
   - Pulsar：Broker 无状态，可秒扩；BookKeeper 独立扩容，无数据迁移、无 Rebalance

2. 百万级 Topic 支持
   - Kafka：Topic 多后性能急剧下降
   - Pulsar：原生支持百万 Topic稳定运行（SaaS/多租户必备）

3. 更强的消息可靠性与一致性
   - Pulsar 支持强一致性（Quorum ACK）、多副本跨机架部署
   - 单 Bookie 宕机不影响读写，自动 Failover

4. 分层存储（Tiered Storage）
   - 热数据放内存/SSD，冷数据自动落 S3/OSS/HDFS
   - 无限消息保留、成本大幅降低

5. 统一队列 + 流双模型
   - Kafka 只有流（Log）；Pulsar 同时支持：
     - 流模式（类似 Kafka）
     - 队列模式（类似 RabbitMQ/RocketMQ，独占、共享、重试、死信）

6. 原生跨地域集群复制（Geo-Replication）
   - Kafka 需 MirrorMaker 等工具，复杂、延迟高、一致性弱
   - Pulsar 内置跨区域同步/异步复制，多活、灾备极简单

---

## 三、Pulsar vs RocketMQ：核心优势
### RocketMQ 特点
- 金融级可靠、事务消息、顺序消息、低延迟
- 阿里开源，适合电商、交易、金融场景

### Pulsar 相对 RocketMQ 的优势
1. 原生多租户（企业级/SaaS 杀手级功能）
   - RocketMQ 多租户靠业务隔离，不彻底
   - Pulsar：租户 → 命名空间 → Topic 三级隔离
   - 权限、配额、TTL、备份策略全隔离

2. 存算分离，扩容更优雅
   - RocketMQ 存储与 Broker 绑定，扩容需迁移数据
   - Pulsar：Broker 可随时扩缩，不迁移数据、不停服

3. 跨地域复制更成熟
   - RocketMQ 开源版无原生跨城复制（商业版才有）
   - Pulsar 开源即支持全局多活、异地灾备

4. 海量 Topic + 海量订阅
   - Pulsar 单集群可支撑百万 Topic + 百万消费者

5. 云原生友好（K8s 天然适配）
   - 无状态 Broker、弹性伸缩、自愈、快速部署
   - 非常适合容器化、Serverless 环境

6. Pulsar Functions（内置轻量级流计算）
   - 内置轻量计算，无需依赖 Flink/Spark
   - 过滤、转换、聚合、路由一站式完成

## 四、Pulsar vs RabbitMQ：核心优势
### RabbitMQ 特点
- 灵活路由、多种交换机、可靠、易用
- 适合传统企业、复杂业务队列、微服务解耦

### Pulsar 相对 RabbitMQ 的优势
1. 超高吞吐 + 海量堆积
   - RabbitMQ 堆积能力弱、延迟随堆积上升
   - Pulsar：高吞吐 + 无限堆积 + 稳定低延迟

2. 分布式与扩展性碾压
   - RabbitMQ 集群弱、队列镜像、扩容复杂
   - Pulsar：分布式无中心、水平扩展、高可用

3. 流处理能力（RabbitMQ 完全没有）
   - Pulsar 原生支持流：回放、重放、事件溯源、长时保留

4. 跨地域、多租户、百万 Topic
   - RabbitMQ 几乎不支持大规模多租户与跨地域

## 五、Pulsar 独有的“全能优势”（一句话总结）
Pulsar = RabbitMQ 的灵活队列 + Kafka 的高吞吐流 + 原生多租户 + 存算分离无限扩容 + 跨地域复制 + 分层存储 + 百万 Topic + 内置轻量计算

一句话选型：
- 传统企业、简单队列 → RabbitMQ
- 大数据、日志、高吞吐 → Kafka
- 金融、事务、顺序消息 → RocketMQ
- 云原生、多租户、跨地域、全场景统一、海量 Topic、无限扩容 → Pulsar

## 六、适合 Pulsar 的典型场景
- SaaS 平台（多租户隔离）
- 全球化/多数据中心业务
- 云原生/K8s 微服务
- 需同时支持队列 + 流的业务
- 百万级 Topic、海量设备接入
- 低成本长期消息留存（分层存储）
- 异地多活、灾备

要不要我帮你整理一份 Pulsar、Kafka、RocketMQ、RabbitMQ 核心特性对比表，方便你快速选型？
