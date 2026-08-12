# raft


https://www.bilibili.com/video/BV1CK4y127Lj


https://github.com/RedisLabs/redisraft

2pc
3pc
共识算法？
pax
paxos

图示

[raft论文中文翻译](https://www.infoq.cn/article/raft-paper/)



[Raft 分布式系统 一致性协议](https://blog.csdn.net/LU_ZHAO/article/details/104934220)
time out信号



raft动画

http://thesecretlivesofdata.com/raft/



 [braft]( https://github.com/baidu/braft ) 
SOFAJRaft
https://gitee.com/sofastack/sofa-jraft

https://github.com/Tencent/phxpaxos

[腾讯开源的Paxos库PhxPaxos代码解读---Prepare阶段]( https://www.cnblogs.com/lijingshanxi/p/10165802.html ) 



如何评价 brpc 团队新的开源 Raft 库 braft？

https://www.zhihu.com/question/266834707 






作者提供了几个文档和benchmark数据，简单看了下，较忙没有看代码：

- 没有WAN高延迟环境数据，没有读的性能，没有延迟数据。实测的是log从propose到commit的性能，这不是通常的做法。文档提到类似的库粗糙不适合支持大量raft实例，但文档和benchmark中都看不到多个raft实例的实测性能或者具体设计。
- 作者提到了多组，但这库并不带调度、管理、监控修复多组raft的组件。没看代码，也不确定多组，比如数千组的时候，线程模型是怎么样。
- 22万qps的单组性能不算高，且测的方法只测到commit。损失单组为多组优化的系统，也应该能跑类似成绩。后台服务跑分不是目的，但跑分从一个侧面体现系统从设计到实现的质量。
- 作者认为batching是跑分的手段，是等特定的时间间隔、或等N个proposal然后合并处理，是显著的延迟换吞吐。显然，事实不是这样。请参考etcd raft的batching做法。
- 测试方法没有在文档中提到。和一般项目不同，共识库必须有近乎严酷加无聊的测试。代码中看到有内空的jepsen目录。Jepsen是系统成熟的必要非充分条件，因为它伸展不开，建议类似jepsen的测试，跑百万数量级的raft组，注入数亿规模随机异常事件，然后测linearizability。test目录有少许测试，测试的规模较小，自己的raft库测试代码就2万行，超过braft整个库大小。测试代码规模差数倍，说明问题的。
- 单语言支持，不带其它语言的binding。

在做多组raft库，近期开源。上述所有问题都有具体涵盖，非空谈。



上述提到的库已经开源，每秒千万级别的吞吐，欢迎试用，欢迎点Star





 https://github.com/sofastack/sofa-jraft 



整体源码都看过，功能完备程度很高，看这个特性列表

- Leader election.
- Replication and recovery.
- Snapshot and log compaction.      日志压缩
- Membership management.
- Fully concurrent replication.
- Fault tolerance.
- Asymmetric network partition tolerance.
- Workaround when quorate peers are dead.

并非虚言，特别是 Cli tools 这个接口和工具设计，对于运维管理是非常方便的。各个模块的分层也很清楚，存储部分都可以替换（LogStorage/MetaStorage/SnapshotStorage etc.)，灵活性很高。

测试方面，官方后来增加了 jepsen 的测试用例，覆盖了当机、配置变更、网络分区等场景，jepsen 确实是分布式测试神器。单元测试覆盖相对还是比较完善的。

关于性能，官方 [benchmark](https://link.zhihu.com/?target=https%3A//github.com/brpc/braft/blob/master/docs/cn/benchmark.md) 文档提到的关于 batch 和 pipeline 的观点，说是纯粹为了跑分过于偏激了。batch 和 pipeline 本质都是为了提高吞吐量，充分地利用 CPU 和带宽，况且 braft 内部其实也有多级的 batch：

- LogManager  的批量日志存储
- Leader Node  apply task 的批量处理
- Leader 到 follower 的日志批量发送等。
- 日志批量应用到状态机等。

> 而这时候工程师往往会沉浸在优化超时、batch size等调参工作，从而忽略了分析系统瓶颈这类真正有意义的事情



这一点理论上没有错，就像很多人解决性能问题就是加一层缓存一样，没有去分析根本性的性能瓶颈。但是，关于batch size 之类的调整，目前业界也有很多自适应的算法，例如 《[Adaptive Batching for Replicated Servers](https://link.zhihu.com/?target=https%3A//ieeexplore.ieee.org/stamp/stamp.jsp%3Farnumber%3D4032492)》，利用探针检测或者线程切换自适应累计等。braft 完全没有实现 pipeline，我个人认为是一个缺陷。要不要用是一个问题，有没有是另一个问题。

 RAFT 协议优化看多很多资料，除了基本的 batch + pipeline 之外，就是在三个环节：

- 日志复制
- 日志提交
- 日志应用到状态机

尝试做并行和异步化，有了 batch 和 pipeline 的能力，针对应用的存储类型，在满足业务语义的情况下做这三个阶段的并行优化。这一点可以看 PorlarDB 最近发在 VLDB2018 的论文。





我们开源了使用 java 重写的 jraft 项目 [alipay/sofa-jraft](https://link.zhihu.com/?target=https%3A//github.com/alipay/sofa-jraft)，基于  braft 移植而来，并且做了 pipeline 优化、线性一致读实现等。



Raft协议详解

https://zhuanlan.zhihu.com/p/27207160



开源实现非常多。这里有个列表，百八十种，各种语言

有一个raft的在线动画演示，可以点击节点控制宕机和重启

https://raft.github.io/





Asymmetric 不对称; 不对等的;



关于Raft算法，有两篇经典的论文，一篇是《In search of an Understandable Consensus Algorithm》，这是作者最开始讲述Raft算法原理的论文，但是这篇论文太简单了，很多算法的细节没有涉及到。更详细的论文是《CONSENSUS: BRIDGING THEORY AND PRACTICE》，除了包括第一篇论文的内容以外，还加上了很多细节的描述。在我阅读完etcd raft算法库的实现之后，发现这个库的代码基本就是按照后一篇论文来写的，甚至有部分测试用例的注释里也写明了是针对这篇论文的某一个小节的情况做验证。



https://www.codedump.info/post/20180921-raft/



Raft一致性算法流程描述

https://www.jianshu.com/p/37877e046132

https://zhuanlan.zhihu.com/p/91288179

## Raft 综合笔记（截至 2026-08）

### Raft 解决什么问题

Raft 是 **崩溃容错（crash fault）** 模型下的领导者型共识协议，用复制日志让多个副本按相同顺序执行命令，从而维护同一个确定性状态机。它解决的是“在节点宕机、重启、消息丢失/乱序/重复、网络分区存在时，哪些操作可以成为唯一确定的历史”，而不是通用的分布式事务或任意恶意节点（Byzantine）问题。

```text
客户端 -- 提议命令 --> Leader -- AppendEntries --> Follower 1
                            |                     Follower 2
                            |                     Follower 3
                            v
                 多数派持久化同一日志位置
                            |
                            v
             commitIndex 前进，所有副本按序 apply 到状态机
```

Raft 的输出是已提交日志的全序；状态机如何处理 KV、元数据、消息、配置或 SQL 事务是上层职责。典型使用包括 etcd、Consul、TiKV、CockroachDB 的元数据/分片副本组，以及 SOFAJRaft、braft、DLedger 等嵌入式实现。

| Raft 能保证 | Raft 不直接保证 |
| --- | --- |
| 已提交命令不会被后续 leader 覆盖，副本按同一顺序执行。 | 客户端请求恰好执行一次；超时重试仍可能重复提交。 |
| 多数派可通信时可继续选主和提交。 | 少数派分区仍可写；这是为了避免脑裂而主动牺牲可用性。 |
| 宕机恢复后可由持久日志/快照追赶。 | 磁盘永不损坏、时钟绝对正确、跨系统的原子提交。 |
| 在正确实现的读协议下可提供线性一致读。 | 任意 follower 本地读天然线性一致。 |

Raft 依赖 `2f + 1` 个投票成员来容忍最多 `f` 个崩溃成员。3 节点只能容忍 1 个故障；5 节点容忍 2 个故障。节点数从 3 增至 4 不增加故障容忍度，却把多数派从 2 提高到 3，因此通常选奇数投票成员。副本应跨独立故障域部署，但跨地域同步复制会把 RTT 直接带入写入尾延迟。

官方参考：

- 原始扩展论文：https://raft.github.io/raft.pdf
- Raft 项目与论文/学位论文入口：https://raft.github.io/
- etcd Raft 实现说明：https://github.com/etcd-io/raft

### 三个角色、任期与选举

每个节点在任意时刻是 Follower、Candidate 或 Leader。`term` 是单调递增的逻辑任期；看到更大 term 的 RPC/响应必须持久化新 term 并退回 Follower。每个 term 最多一个 leader，这是由“每节点每 term 至多投一票 + 获得多数票的两个集合必相交”共同保证的。

```text
Follower 超过随机 election timeout 未收到有效 leader 通信
  -> term++，投自己一票，成为 Candidate，发送 RequestVote
  -> 获得多数票：成为 Leader，立即发送 heartbeat / 当前 term 的 no-op
  -> 收到更高 term：转为 Follower
  -> 超时未获多数：新 term 后重新选举
```

投票不是只看“谁先发起”：候选人日志必须至少与投票者一样新，先比较 `lastLogTerm`，相同时再比较 `lastLogIndex`。这条限制使已提交日志必然存在于后续 leader 的日志中。随机选举超时降低了多个节点持续同时竞选的概率，但不能消除网络、GC stop-the-world、磁盘卡顿或错误超时配置造成的选举抖动。

| 参数/机制 | 目的 | 实践原则 |
| --- | --- | --- |
| Heartbeat interval | leader 宣告存活并携带提交进度 | 显著小于 election timeout。 |
| Election timeout | follower 判断 leader 失联 | 大于正常网络 RTT、磁盘抖动和调度停顿，并加入随机化。 |
| Pre-Vote | 先探测能否取得多数票再增加 term | 降低隔离旧节点恢复后扰乱集群的概率；属于常见工程扩展。 |
| Check Quorum | leader 周期确认仍联系多数派 | 失去多数派时主动退位，避免孤立 leader 持续服务。 |
| Leader transfer | 在计划维护前把领导权交给追平的节点 | 降低重启/升级引发的瞬时不可用，不替代故障选举。 |

不要把“leader 宕机后会自动恢复”理解成零中断：至少需要故障检测和一次选举，且新 leader 必须确认自己能安全服务。超时设得太小会导致频繁选举；设得太大则故障切换慢。应该依据 P99 网络时延、fsync、CPU/GC 暂停、虚拟化抖动和跨 zone RTT 压测，而不是复制某个博客的固定毫秒数。

### 日志复制、提交与四个安全性要点

leader 为每条客户命令分配连续 `(index, term)`，先追加本地日志，再以 `AppendEntries(prevLogIndex, prevLogTerm, entries, leaderCommit)` 复制到 followers。follower 只有在自己的 `prevLogIndex/prevLogTerm` 匹配时才接受；发生冲突时删除该位置及其后的 **未提交** 日志并接受 leader 的后缀。leader 按每个 follower 的 `nextIndex`/`matchIndex` 逐步回退或利用冲突提示快速定位，再把落后副本追到最新。

```text
日志位置:      1       2       3       4
leader:      (1,a)   (1,b)   (2,c)   (2,d)
follower:    (1,a)   (1,b)   (3,x)

leader 先用 prev=(2,1) 复制位置 3、4；follower 发现冲突，
删除未提交的 (3,x)，最终二者在 index 与 term 上一致。
```

`commitIndex` 是已达成共识的最大日志位置，`lastApplied` 是已执行到状态机的最大位置，必须满足 `lastApplied <= commitIndex`。leader 发现某一日志位置被多数派复制后可以推进提交，但有一个极易遗漏的限制：leader 只能凭“**当前 term 的日志项** 已复制到多数派”直接推进 `commitIndex`。旧 term 的条目会随着后续当前 term 条目提交而间接提交，不能仅因它已在多数派上就直接宣布提交。

Raft 的核心安全性可记为：

1. **Election Safety**：每个 term 最多一个 leader。
2. **Leader Append-Only**：leader 不覆盖或删除自己的日志，只追加。
3. **Log Matching**：两份日志若同一 index 的 term 相同，则该位置之前的所有日志相同。
4. **Leader Completeness / State Machine Safety**：已提交条目必在未来 leader 中出现，任何状态机在同一 index 不会应用不同命令。

客户端得到成功响应的正确时机是命令已提交并按上层协议完成必要持久化/应用，而不是仅“leader 已接收”或“写入 leader 内存”。请求超时并不等于命令失败，可能已提交但响应丢失。因此上层 API 应携带稳定的 `clientId + requestId`，状态机持久化去重结果或能以业务唯一键幂等执行；客户端重试应查询结果或带同一 request ID 重放。

### 持久化、状态机与恢复顺序

必须稳定保存的核心 Raft 状态包括 `currentTerm`、`votedFor` 和日志；快照包含被截断前缀的状态机状态以及 `lastIncludedIndex/lastIncludedTerm`。进程重启后不能仅恢复业务状态而丢失任期、投票或日志元数据，否则可能违反“每 term 一票”或覆盖已提交历史。

一个嵌入式 Raft 库通常只实现协议状态机，把网络、WAL、快照文件、RPC 编解码、线程模型和状态机应用交给调用方。以 etcd/raft 的 `Ready` 模型为例，安全的处理顺序是：

1. 先将新增 `Entries`、`HardState` 和 `Snapshot` 按实现要求写入稳定存储；若已有同 index 的持久日志，其后的旧条目必须被截断。
2. 在最新 `HardState` 已落盘后，再发送依赖它的网络消息；同一批日志可与 follower 复制并行，但不能违反持久化先行约束。
3. 按顺序安装 snapshot、执行 `CommittedEntries`，配置变更条目在状态机侧和 Raft 侧都要完成应用。
4. 只有处理完这批更新后才通知库推进下一批；所有 apply 必须串行、按 index、可恢复且幂等。

不要在 Raft 回调中直接执行耗时业务 RPC、非幂等外部副作用或无界阻塞 I/O。更可靠的设计是状态机先确定性地记录意图/任务，再由独立 worker 以可重试、可去重的方式执行外部动作；这就是 outbox/saga 与 Raft 结合时需要额外设计的原因。

### 读语义：本地读、ReadIndex 与 lease

复制日志天然顺序化写入，读是否线性一致取决于路径。最常见错误是“从任意 follower 读，因为它最终会同步”。这只能得到可能陈旧的读，适合监控、缓存或明确允许 stale read 的场景。

| 读方式 | 一致性 | 代价与条件 |
| --- | --- | --- |
| 任意副本本地读 | 可陈旧 | 无 quorum 往返，必须由业务接受旧值。 |
| 日志写入一个只读命令 | 线性一致 | 一次复制/提交，简单但吞吐与延迟较差。 |
| ReadIndex | 线性一致 | leader 向多数派确认自己仍是 leader 后返回安全 `readIndex`；副本 apply 到该 index 后读取。 |
| Leader lease | 可线性一致 | 省去每读一次 quorum 往返，但依赖严格时钟/租约假设与正确的失效处理。 |

新 leader 不应立刻仅凭本地日志服务线性一致读：它要先确认 leadership，常见方式是复制当前 term 的 no-op 或运行 quorum check。follower 也可向 leader 获取 ReadIndex，等本地 `lastApplied >= readIndex` 后再读，从而把读负载分散出去。lease 是性能优化而不是论文默认“免费能力”；若没有明确时钟界限、暂停处理和测试证明，优先使用 ReadIndex。

### 成员变更、Learner 与快照

成员变更不能直接从旧配置切到新配置，否则两个不相交的多数派可能各自选出 leader。经典 Raft 使用 **joint consensus**：先提交 `C_old,new`，该阶段需要旧配置和新配置都过半；再提交仅含新成员的 `C_new`。实际库可能采用“一次只允许一个成员变更、旧配置提交后生效”等等价安全变体，必须遵守所用库的 API 和语义，不能把不同实现的步骤混用。

推荐扩容/替换流程：

1. 以 learner/non-voting 成员加入，不参与投票和 quorum，先接收快照与增量日志。
2. 监控其 `matchIndex`、延迟、磁盘和网络，追平 leader 后再发起受控的 voter 变更。
3. 等配置变更已提交并应用，确认 quorum/leader 健康后，才移除旧 voter。
4. 一次只执行一个未完成的配置变更，避免交叠多数派和恢复路径难以推理。

Raft 日志不能无限增长。snapshot 将 `lastIncludedIndex` 之前的已应用状态压缩为一个状态机快照，leader 对落后太多的 follower 发送 `InstallSnapshot`，其安装后丢弃相应旧日志并继续增量复制。快照是一致性协议的一部分，不是简单复制数据库目录：需要校验、原子切换、版本兼容、限速、断点/重试和失败回滚；快照创建还要避免阻塞 apply 或产生不可恢复的半成品。

### 性能与 Multi-Raft 的工程边界

单个 Raft group 的写吞吐受 leader CPU、WAL fsync、网络带宽、最慢多数派以及状态机 apply 共同限制。批处理、pipeline、并行 follower 复制、流控、异步持久化边界和快照/日志压缩能改善吞吐或尾延迟，但不能绕开“写需多数派确认”的物理成本。只测 leader `propose` 到内存或日志进入队列的时间，不是端到端提交延迟。

Multi-Raft 用许多独立 Raft group 承载不同分片，以多个 leader 分摊 CPU、磁盘和网络，实现水平扩展；代价是调度、热点、数千组定时器、WAL/快照、复制流和元数据管理。生产系统通常还需要 placement、分片迁移、leader 均衡、限流、优先级、反熵/校验与可观测性，Raft 库本身通常不提供完整控制面。

| 优化 | 解决什么 | 不能解决什么 |
| --- | --- | --- |
| Batching | 合并多条日志的 RPC/fsync 开销 | 可能以排队时间换吞吐，应控制 P99。 |
| Pipeline | 同时在途多批 AppendEntries | follower 慢盘、网络丢包和状态机慢仍会形成背压。 |
| Flow control | 防止慢 follower 占满内存/网络 | 不能让失去多数派的集群继续提交。 |
| Snapshot/compaction | 控制日志空间和落后节点追赶成本 | 快照 I/O 过大可能反过来干扰线上复制。 |
| Learner | 让新节点先追平再投票 | learner 未晋升前不增加故障容忍度。 |

### 实现与系统映射

| 实现/系统 | 与 Raft 的关系 | 阅读重点 |
| --- | --- | --- |
| etcd/raft | 极简、确定性的 Go Raft 协议库，网络和磁盘由集成方负责 | `Ready` 持久化/发送/apply 顺序、ReadIndex、conf change。 |
| SOFAJRaft | Java Raft 库，提供存储、快照、CLI 与服务化集成点 | `Node`、`Replicator`、`BallotBox`、`FSMCaller`、存储 SPI。 |
| braft | C++ Raft 库，常与 brpc 集成 | 多 group、复制 pipeline、快照与运维接口。 |
| DLedger | Java Raft 风格 commit log 库，供 RocketMQ 等使用 | 消息日志、角色切换和复制确认语义。 |
| etcd/Consul | 把 Raft 放在控制面/元数据复制层 | 外部 API 的线性一致读、watch、快照、成员管理。 |

既有的 [SOFAJRaft](SOFAJRaft.md)、[JRaft API](jraft.md)、[etcd 笔记](../go/etcd/etcd.md)、[DLedger](../java/rocketmq/DLedger.md) 可作为源码与系统落地的下一步。不同项目对 PreVote、lease、conf change、learner、WAL 和读路径的实现并不完全相同；阅读源码时先写清它采用的语义与版本，再做比较。

### 排障、测试与面试要点

应监控 term、leader 变更次数与耗时、各 follower 的 `matchIndex/nextIndex`、commit/apply lag、WAL fsync、RPC RTT/丢包、snapshot 频率/耗时、磁盘与网络饱和、配置变更状态、客户端重试和状态机 apply 延迟。频繁选主往往不是“Raft 不稳定”，而是心跳/选举超时、GC、慢盘、网络或资源争用暴露了问题。

必须做故障注入而非只做单元测试：节点 kill -9/重启、WAL 截断或损坏、磁盘满/慢、消息重复/乱序/丢失、单节点和多数/少数网络分区、时钟跳变、snapshot 传输失败、leader 切换中的客户端超时、配置变更与故障交叠。测试断言应覆盖安全性和线性一致性，而不只断言“最终节点数量相同”。Jepsen、模型检查/TLA+、确定性模拟器和长期随机测试各有价值，彼此不能替代。

常见问答：

- **Raft 为什么不会脑裂写入？** 任何 leader 需要多数票/多数派复制，两套多数派必相交；少数派无法选主和提交。
- **日志复制到多数就能返回吗？** 需满足提交规则，尤其 leader 只能以当前 term 的多数派条目直接推进 commit；应用还要处理客户端重试幂等。
- **Raft 能保证 exactly-once 吗？** 不保证。它保证日志至多按一个值提交到某 index；API 仍要以 request ID 或业务唯一键去重。
- **为什么读也要协议？** leader 可能已失去多数派或 follower 未追平，直接读会返回旧值；使用 ReadIndex、正确 lease 或接受 stale read。
- **成员扩容为什么先加 learner？** 避免未追平节点影响 quorum，并降低一次性配置变更和快照追赶的风险。
- **Raft 与 Paxos 谁更强？** 两者都可实现 crash fault 共识；Raft 更强调可理解的领导者日志复制分解，系统质量取决于实现、存储、读路径、运维和测试。

学习顺序：先精读 Raft 扩展论文的 Figure 2 与第 5、6、7 节；用 [Raft 动画](http://thesecretlivesofdata.com/raft/) 手动推演选举和日志冲突；完成 MIT 6.824 的 Raft lab 或实现一个确定性单线程版本；再阅读 etcd/raft 的 `Ready` 循环和 SOFAJRaft 的复制/状态机代码。最终目标是能解释一个请求从 `propose` 到多数派持久化、commit、apply、响应、超时重试和故障恢复的完整路径。
