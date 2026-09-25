# L16 Kafka：分布式消息与日志系统

> 阅读：Kreps et al., *Kafka: A Distributed Messaging System for Log Processing*, NetDB 2011；
> 辅读：*Beyond A Log: A Short Primer to the Kafka API* / KIP 事务与 exactly-once 文档
> 主线：把"复制日志"从内部机制提升为对外的一等抽象（L03/L05 的日志公开化）。

## 1. 核心问题

- 流式数据处理需要：多个消费者按各自进度读取同一批事件、高吞吐、持久、可回放。
- 传统消息队列（ActiveMQ/RabbitMQ）为"低延迟 + 灵活路由"设计 →
  大量小消息、随机磁盘 I/O → **吞吐被磁盘寻道卡死**。
- Kafka 的反直觉取舍：**牺牲灵活性，换取"顺序写 + 零拷贝 + 批量"的极致吞吐**——
  消息队列被重构成"分布式提交日志（commit log）"。

## 2. 设计与取舍

### 2.1 核心抽象：Partition = 有序不可变追加日志
- Topic 分成多个 **partition**（并行与有序的粒度）；每条消息拿到单调 **offset**
  （分区内 = Lamport 时钟，L07）。
- **顺序保证只在 partition 内**：全局有序要退化成单分区（吞吐换顺序）。
- 消费者用 **consumer group**：组内分区不重叠分配（各分区一个消费者）→
  扩容 = 加分区，天然负载均衡（对照 L02 MapReduce 的分片并行）。

### 2.2 高吞吐三支柱
- **顺序磁盘写 + OS page cache**：不做 fsync 到每个副本（靠多副本换持久性），
  写即追加段文件 → 磁盘当"廉价 RAM"用，避免 JVM 堆缓存的双缓存。
- **零拷贝 sendfile**：数据从 page cache 直接到网卡，不经用户态 → 吞吐核心魔法
  （对接 CSAPP/体系结构的 DMA 知识）。
- **批量 + 压缩**：producer 攒批、按批压缩，摊薄网络与 I/O 固定开销（L01 RPC 的批量优化）。

### 2.3 复制：ISR 与"min-in-sync-replicas"
- 每分区：leader + 若干 follower，**同步镜像日志**（像 Raft 但不逐条强一致）。
- **ISR（in-sync replicas）**：追上 leader 的副本集合；acks=all 即写全 ISR。
- leader 挂了从 ISR 选新 leader → 避免"旧 leader 复活覆盖已提交消息"
  （Kafka 0.11 前的著名 bug：**unclean leader election** 丢数据；
  修复引入 leader epoch，L05 的 term 复刻）。
- 本质：**Kafka 复制是"可容忍少数不一致的高性能复制"，比 Raft 松**——
  换吞吐；这是 L05 vs L16 的核心权衡对照。

### 2.4 元数据：从 ZooKeeper 到 KRaft
- 早期把 broker 注册/controller 选举交给 ZK（L12）；
- **KRaft（2024 GA）**：内置 Raft 管理元数据分区，去 ZK 依赖 → 
  运维简化 + 元数据操作也日志化。**一次"外包共识 → 自建共识"的返祖**（L05/L12 应用）。

## 3. 语义：at-least-once 与"exactly-once"

- 消费端手动提交 offset → 崩溃重放（at-least-once）→ 
  靠**幂等 producer + 事务（transactional API）** 实现
  "读-处理-写" 的 effectively-once（对照 L01 RPC 幂等、L14 2PC）。
- Kafka 事务 = 跨分区原子写 + "isolation.level=read_committed" 让消费只看到已提交
  → 把 L14 的两阶段提交做进日志系统。

## 4. 论文间脉络

- L03 GFS/L05 Raft 的"追加日志"到 L16 变成对外可订阅的产品——**日志即数据库**
  （event sourcing）。
- L02 MapReduce（批）→ L16 Kafka（流）：本课"数据处理"从批到流的两端；
  L17 Spark Streaming / Flink 站在 Kafka 之上。
- L12 ZooKeeper：Kafka 元数据的旧家与新家（KRaft）是共识产品化的活教材。

## 5. 跨课程联系

- **CSAPP/自顶向下**：sendfile 零拷贝、page cache、DMA 是吞吐的物理来源。
- **15-445**：WAL（write-ahead log）与 Kafka log 概念同源；offset ↔ LSN；
  consumer group ↔ 物化视图的增量维护。
- **CS149**：partition 并行 + 分区内顺序 = 数据并行的流式版（BSP 的连续超步）。
- **MLC/15-442**：训练数据管道、在线特征回填大量用 Kafka 做高吞吐缓冲。

## 6. 开源项目中的应用

- **Apache Kafka / Redpanda（C++ 重写，单二进制）/ Pulsar（存算分离 + bookkeeper）**：
  云原生日志三杰。
- **Kafka Streams / Flink / Spark Structured Streaming**：流处理引擎的默认数据源。
- **Debezium / Maxwell（CDC）**：把数据库变更日志导出成 Kafka topic（L14↔L16）。
- **LinkedIn/Uber/Netflix 的事件驱动架构**、**OpenSearch/Elastic 的 ingest 缓冲**。

## 7. 延伸阅读

- *Designing Data-Intensive Applications*（Kleppmann）第 9–12 章——日志/流/一致性最佳综述。
- Confluent 博客 "Exactly-once semantics in Kafka" 与 KIP-98（事务设计原文）。
- *Tiered Storage*（KIP-405）：Kafka 冷数据下沉 S3（L13↔L16 合流）。
- 对照 Raft：本目录 notes/L05/L06，思考"若 Kafka 用 Raft 复制会损失多少吞吐"。
