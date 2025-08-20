# zookeeper_zab

zab协议

ZAB（ZooKeeper Atomic Broadcast）协议和 Raft 协议都是分布式系统中用于实现数据一致性和高可用的共识（Consensus）算法。它们主要用于在多个节点组成的集群中，确保即使部分节点发生故障，整个系统依然能够对外提供一致、可靠的服务。

虽然目标相似，但它们在设计、实现和应用场景上存在一些关键区别。

---

### 1. ZAB 协议 (ZooKeeper Atomic Broadcast)

*   应用场景：专为 Apache ZooKeeper 设计，是其核心通信协议。
*   设计目标：
    *   实现原子广播（Atomic Broadcast）：确保所有节点以相同的顺序接收并应用相同的消息（写请求）。
    *   保证顺序一致性（Sequential Consistency）。
    *   支持崩溃恢复（Crash Recovery）。
*   核心机制：
    *   角色：`Leader`（领导者）、`Follower`（跟随者）、`Observer`（观察者，不参与投票）。
    *   两阶段提交（简化版）：
        1.  发现（Discovery） / 同步（Synchronization）：选举出新 Leader 后，Leader 与 Follower 同步状态，确保所有节点具有最新的、一致的事务日志。
        2.  广播（Broadcast）：Leader 将客户端的写请求封装成事务（Proposal），广播给所有 Follower。Follower 收到后写入日志并回复 `ACK`。当 Leader 收到过半数（Quorum）的 `ACK` 后，提交该事务，并通知 Follower 提交。读请求由 Leader 或 Follower 直接处理（Follower 需与 Leader 保持一定同步）。
    *   选举：使用一种基于 ZAB 选举算法（通常基于节点ID、事务ID等）的机制来选举 Leader。
    *   强 Leader：所有写操作必须通过 Leader，Leader 拥有绝对的决策权。
*   特点：
    *   为 ZooKeeper 量身定制：紧密集成，优化了 ZooKeeper 的读多写少、顺序写入的场景。
    *   恢复模式：ZAB 有明确的恢复阶段（Leader 选举和状态同步），之后才进入广播阶段。
    *   保证事务ID（zxid）的全局单调递增。

---

### 2. Raft 协议

*   应用场景：通用的共识算法，被广泛应用于各种分布式系统（如 etcd, Consul, TiKV, LogCabin 等）。
*   设计目标：
    *   易于理解（Understandability）：Raft 的最大设计目标之一是比 Paxos 等算法更容易理解和实现。
    *   实现复制状态机（Replicated State Machine）。
*   核心机制：
    *   角色：`Leader`（领导者）、`Follower`（跟随者）、`Candidate`（候选者）。
    *   任期（Term）：时间被划分为连续的任期（Term），每个任期从一次选举开始。任期号单调递增，用于识别过期的信息。
    *   Leader 选举：
        *   Follower 在等待 Leader 心跳超时后，转变为 Candidate，增加任期号，并发起选举（为自己投票并请求其他节点投票）。
        *   获得过半数投票的 Candidate 成为新 Leader。
        *   选举超时和随机化（每个节点等待超时的时间是随机的）减少了选举冲突。
    *   日志复制（Log Replication）：
        *   Leader 接收客户端请求，将其作为新日志条目追加到自己的日志中。
        *   Leader 并行地向所有 Follower 发送 `AppendEntries` 请求（包含心跳和日志复制）。
        *   Follower 收到请求后，检查日志连续性（prevLogIndex 和 prevLogTerm），如果匹配则追加日志并返回成功。
        *   当 Leader 确认某个日志条目被过半数节点成功复制后，该条目即为 `committed`（已提交），Leader 将其应用到状态机并通知 Follower 提交。
    *   安全性：通过 `选举限制`（Election Restriction，要求投票给拥有更完整日志的 Candidate）和 `提交规则`（只能提交当前任期的日志条目）等机制保证一致性。
*   特点：
    *   强 Leader：与 ZAB 一样，所有写请求必须由 Leader 处理。
    *   模块化设计：将问题分解为 Leader 选举、日志复制、安全性三个子问题，清晰明了。
    *   易于教学和实现：相比 ZAB 和 Paxos，Raft 的文档和逻辑更直观。

---

### ZAB 与 Raft 的主要区别

| 特性 | ZAB (ZooKeeper) | Raft |
| :--- | :--- | :--- |
| 设计初衷 | 为 ZooKeeper 实现原子广播 | 通用共识算法，强调可理解性 |
| 状态模型 | 原子广播 + 崩溃恢复 | 复制状态机 |
| 选举机制 | 基于 ZAB 特定算法（如 Fast Leader Election） | 基于任期（Term）和超时的随机选举 |
| 日志/事务提交 | Leader 收到过半数 `ACK` 后提交 | Leader 收到过半数 `AppendEntries` 成功响应后，确认日志条目 `committed` |
| 日志连续性保证 | 强调 Leader 与 Follower 的日志同步（恢复阶段） | 通过 `prevLogIndex` 和 `prevLogTerm` 在 `AppendEntries` 中保证 |
| 可理解性 | 相对复杂，与 ZooKeeper 实现耦合较深 | 设计目标就是易于理解，文档清晰 |
| 通用性 | 主要用于 ZooKeeper | 通用性强，被广泛采用 |

---

### 总结

*   相似点：两者都是强 Leader 模型的共识算法，依赖过半数原则（Quorum），都包含 Leader 选举和日志/事务复制阶段，都能容忍 `⌊(n-1)/2⌋` 个节点故障。
*   不同点：ZAB 是为 ZooKeeper 量身定制的原子广播协议，而 Raft 是一个通用、模块化、易于理解的复制状态机共识算法。Raft 的设计使其在教学、实现和社区支持方面更具优势，因此近年来应用更为广泛。

你可以将 ZAB 看作是 ZooKeeper 的“专用引擎”，而 Raft 则是一个“标准化、易用的通用发动机”。
