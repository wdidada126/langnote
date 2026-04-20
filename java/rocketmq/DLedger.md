# DLedger

https://github.com/openmessaging/dledger

A raft-based java library for building high-available, high-durable, strong-consistent commitlog.

Features
Leader election
Preferred leader election
Pre-vote protocol
High performance, high reliable storage support
Parallel log replication between leader and followers
Asynchronous replication
State machine
Multi-Raft
High tolerance of symmetric network partition
High tolerance of asymmetric network partition
Jepsen verification with fault injection

New features waiting to be added
Snapshot (working in progress)
Dynamic membership & configuration change
SSL/TLS support

下面把 DLedger GitHub 上的 Features 一条一条用通俗+工程化语言讲清楚，不搞玄学，直接对应 Raft 原理和生产意义。

# 已支持特性逐条解释

## 1. Leader election
领导者选举
- 标准 Raft 核心功能：节点启动/Leader 挂掉时，自动投票选出新 Leader。
- 保证同一时刻只有一个 Leader 提供写入服务，避免脑裂。

## 2. Preferred leader election
优先指定 Leader 选举
- 可以手动指定某个节点“优先当 Leader”。
- 生产常用：让性能更好/机房更好的节点优先成为主节点，避免随机选主导致不稳定。

## 3. Pre-vote protocol
预投票机制
- Raft 优化：选举前先做一轮“试探投票”，确认自己能拿到足够票数，再真正发起选举。
- 作用：防止网络差的节点频繁扰乱选举、减少不必要选举、提升集群稳定性。

## 4. High performance, high reliable storage support
高性能、高可靠存储支持
- 底层用顺序文件存储（类似 RocketMQ CommitLog）。
- 支持同步/异步刷盘，保证数据不丢，同时吞吐量高。

## 5. Parallel log replication between leader and followers
Leader 与 Follower 之间并行日志复制
- Leader 不串行发日志，而是并行向多个 Follower 发送数据。
- 大幅提升复制速度，降低写入延迟。

## 6. Asynchronous replication
异步复制
- Leader 写完本地就返回，不用等 Follower 同步完。
- 性能极高，但有极低概率丢消息（适合日志、监控等可丢数据场景）。

## 7. State machine
状态机
- Raft 基本模型：
  - 日志复制到多数节点
  - 提交后应用到状态机
  - 所有节点最终状态一致
- DLedger 支持上层（如 RocketMQ）对接自己的状态机。

## 8. Multi-Raft
多 Raft 组
- 一个进程内可以跑多个独立 Raft 集群。
- 适合大规模分布式系统：不同分片用不同 Raft group，提升扩展性。
- RocketMQ 未来多副本分片架构会用到。

## 9. High tolerance of symmetric network partition
高容忍对称网络分区
- 比如 3 节点被切成 1:2 两边，互相不通。
- Raft 保证：只有多数派那侧能选主、能写入，少数派只读/不可用。
- 不会出现双主、不会数据不一致。

## 10. High tolerance of asymmetric network partition
高容忍非对称网络分区
- 更复杂的网络故障：
  - A 能连 B
  - B 能连 C
  - A 不能连 C
- DLedger 能在这种不对称分区下依然保持选举稳定、不脑裂。

## 11. Jepsen verification with fault injection
经过 Jepsen 故障注入测试验证
- Jepsen 是分布式系统界最权威的正确性验证工具。
- 故意制造：断网、延时、丢包、crash、时钟漂移……
- 证明 DLedger 在极端故障下：
  - 不丢数据
  - 不脏数据
  - 不脑裂
  - 强一致性保证有效

# 即将添加的新特性逐条解释

## 1. Snapshot (working in progress)
快照（开发中）
- Raft 日志会越来越大，需要定期打快照，丢弃旧日志。
- 作用：
  - 减少存储空间
  - 新节点加入时快速追数据（不用从头同步所有日志）
- 当前 DLedger 还在实现中。

## 2. Dynamic membership & configuration change
动态成员变更、配置热更新
- 运行时直接增加/减少节点，不用重启集群。
- 标准 Raft 重要功能：集群扩缩容、节点替换。

## 3. SSL/TLS support
SSL/TLS 加密支持
- Raft 内部通信（选举、日志复制）加密传输。
- 适合金融、政务、跨公网部署的安全要求。


# 一句话总结（面试/讲架构专用）
DLedger 是一个完整、生产级、经过 Jepsen 验证的 Java Raft 实现，支持标准选举、预投票、并行复制、多 Raft 组、强网络容错，并正在完善快照、动态成员、TLS 加密，是 RocketMQ 高可用的核心底层。

需要我给你整理一段DLedger 面试背诵版话术吗？

RocketMQ 本身没有原生内置完整的 Raft 实现，但通过独立组件 DLedger 完整实现了 Raft 协议，并深度整合进 Broker 存储层。

### 一、RocketMQ 与 Raft 的关系（清晰版）
1. 4.5.0 以前：无 Raft，只有 Master-Slave 主从复制，不能自动选主，故障需人工切换。
2. 4.5.0+（主流）：引入 DLedger（独立开源组件），基于 Raft 完整实现，替换 CommitLog 存储层。
3. 5.x+：新增 Controller 模式，用 DLedger 做元数据 Raft 一致性，管理 Broker 选主。

### 二、DLedger：RocketMQ 的 Raft 实现（核心）
DLedger 是一套完整的 Raft 实现，完全符合 Raft 论文：
- 角色：Leader / Follower / Candidate
- 选举：随机超时、过半投票、任期（Term）递增
- 日志复制：Leader 写 → 复制到 Follower → 过半确认（N/2+1） 才返回成功
- 故障转移：Leader 挂 → 自动重新选举、秒级切换
- 一致性：WAL 日志强一致、数据不丢、不脑裂

### 三、RocketMQ 中 Raft 的两种使用形态
#### 1. DLedger CommitLog（存储层 Raft，生产主流）
- 作用：Broker 消息存储（CommitLog）用 Raft 保证多副本强一致。
- 架构：3+ 节点一组，自动选主、自动故障转移、消息不丢失。
- 配置：`enableDLegerCommitLog=true`（你上一轮用的就是这个）。

#### 2. DLedger Controller（5.x 元数据 Raft）
- 作用：独立 Controller 集群（可嵌 NameServer），用 Raft 管理Broker 主从状态与选主。
- 数据：只存元数据（Broker 状态、SyncStateSet），不存业务消息。
- 优势：解耦选主与存储，支持更大集群。

### 四、常见误区澄清
- ❌ RocketMQ 内核自带 Raft？
  否。Raft 由 DLedger 库 实现，RocketMQ 只是整合使用。
- ❌ NameServer 用 Raft？
  否。NameServer 无状态、无持久化、无 Raft。
- ❌ DLedger 只是简易 Raft？
  否。完整实现 Raft 所有核心特性（选举、日志复制、安全性、快照）。
- ✅ RocketMQ + DLedger = 真正的 Raft 高可用：自动选主、过半确认、消息不丢、自动容灾。

### 五、一句话总结
RocketMQ 自身不带 Raft，但通过 DLedger 完整实现 Raft 协议，并提供两种 Raft 模式：存储层强一致（DLedger CommitLog）与元数据管控（Controller 模式），是生产级金融级消息不丢的标准方案。

要不要我帮你梳理一份 RocketMQ 传统主从 vs DLedger Raft vs Controller 模式 的核心对比表（含选主、一致性、故障切换、适用场景）？
