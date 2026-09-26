# 第 14–15 章 Hashicorp Raft 与基于 Raft 的分布式 KV 系统实战

> 覆盖原书：第 14 章「Hashicorp Raft」（14.1 如何跨过理论和代码之间的鸿沟 / 14.2 如何以集群节点为中心使用 API / 14.3 小结）
> + 第 15 章「基于Raft的分布式KV系统开发实战」（15.1 如何设计架构 / 15.2 如何实现代码 / 15.3 小结）。
> 两章合并的理由：第 14 章是**读别人的 Raft 库**，第 15 章是**用它写一个 KV 系统**，是一条完整的落地链。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 14.1.1 Raft 如何实现领导者选举 | `hashicorp/raft` 的选举流程与状态机 | 库把论文里的「超时/任期/日志比较」落成具体回调与配置 |
| 14.1.2 Raft 如何复制日志 | `Apply()` → `FSM.Apply()` | **Raft 只负责日志一致，状态机语义由你实现**——这是库与论文的边界 |
| 14.2 以集群节点为中心使用 API | 创建/增加/移除/查看节点 | 生产系统的运维动作必须走 Raft 的**成员变更**，不能直接改配置 |
| 15.1 架构设计 | 接入协议 / KV 操作 / 分布式集群 | 三层拆分：网络层 → KV 层 → 共识层 |
| 15.2 代码实现 | 三段代码骨架 | 关键在**只有 Leader 接受写**，读要决定一致性档位 |
| 15.3 小结 | 从论文到系统的鸿沟 | 论文 20 页之外，工程量最大的是成员管理、快照、读路径与可观测性 |

## 核心精讲

### 14.1 理论与代码之间的鸿沟在哪

Raft 论文（USENIX ATC 2014）只有约 20 页，描述的是**算法核心**。
一个生产可用的 Raft 库（`hashicorp/raft`）至少需要补上：

| 论文没写、但必须有的部分 | 说明 |
| --- | --- |
| 日志压缩 / 快照 | 日志无限增长 → 必须定期快照并截断 |
| 成员变更的**编排** | 谁发起、如何等待提交、失败如何回滚 |
| 传输层 | 论文假设有 RPC；库要提供可替换的 `Transport`（TCP + 可选 mTLS） |
| 持久化 | 论文只说「持久化」；库要做 `LogStore`（ BoltDB 等）与 `StableStore` |
| 读一致性 | 论文用 Read Index；库要暴露「强读/弱读」选择 |
| 快照传输 | 落后太多的 follower 需要**整包快照**而非逐条日志 |
| 进度/指标与可观测性 | Leader 是谁、落后多少、有没有在追日志 |

### 14.1.2 复制日志的调用链

```
教学示意，不参与构建
// 1) 客户端向 Leader 提交
leaderRaft.Apply(cmdBytes, timeout)    // 返回 ApplyFuture
//   内部：追加日志 -> 复制到多数派 -> 提交 -> 交给 FSM
// 2) 由你实现的状态机
func (f *KVFSM) Apply(log *raft.Log) interface{} {
    switch log.Type {
    case raft.LogCommand:
        var c Command
        decode(log.Data, &c)
        switch c.Op {
        case "set": f.store[c.Key] = c.Value
        case "del": delete(f.store, c.Key)
        }
        return nil
    }
    return nil
}
// 3) 快照（论文不管，工程必须）
func (f *KVFSM) Snapshot() (raft.FSMSnapshot, error) { return &KVSnap{clone(f.store)}, nil }
func (f *KVFSM) Restore(rc io.ReadCloser) error      { return decodeInto(&f.store, rc) }
// 关键洞察：所有节点按**同一日志序列**执行同一段代码 -> 状态必然一致
//           所以 FSM.Apply 必须是**确定性的**（不能有随机数/本地时间/外部 IO）
```

> **FSM 确定性的要求**是「从论文到代码」最容易踩的坑：
> 一旦 `Apply` 里读了本地时钟、随机数或未排序的 map 迭代，副本就会静默发散。

### 14.2 以集群节点为中心使用 API

```
教学示意，不参与构建
// 创建第一个节点（bootstrap）
cfg := raft.DefaultConfig()
cfg.LocalID = raft.ServerID("node1")
transport := raft.NewNetworkTransport(...)
store    := raftboltdb.NewBoltStore("raft-log.bolt")
snaps    := raft.NewFileSnapshotStore("snapshots", 3, os.Stdout)
r, _ := raft.NewRaft(cfg, fsm, store, store, snaps, transport)
r.BootstrapCluster(raft.Configuration{
    Servers: []raft.Server{{ID: "node1", Address: transport.LocalAddr()}},
})
// 增加节点（走成员变更，不是改配置文件）
r.AddVoter(raft.ServerID("node2"), raft.ServerAddress("10.0.0.2:8300"), 0, timeout)
// 移除节点
r.RemoveServer(raft.ServerID("node2"), 0, timeout)
// 查看状态
fmt.Println(r.State())        // Leader / Follower / Candidate
fmt.Println(r.Leader())       // 当前 Leader 地址
r.Stats()                     // 任期、提交索引、各 peer 的追赶进度
r.GetConfiguration().Configuration().Servers   // 成员列表
```

**为什么成员变更必须走 API**：直接改配置会让不同节点持有不同成员视图，
可能同时选出两个 Leader（新旧多数派不相交）。`AddVoter`/`RemoveServer`
内部会像普通日志项一样走一遍共识——**成员变更本身也是一条日志**。

### 15.1 架构设计：三层拆分

```
教学示意，不参与构建
┌──────────────────────────────────────────┐
│ 接入层（15.1.1 接入协议）                  │
│   - 自定义二进制/TCP 协议，或 HTTP/gRPC    │
│   - 非 Leader 收到写请求 -> 转发或返回重定向│
├──────────────────────────────────────────┤
│ KV 层（15.1.2 KV 操作）                    │
│   - set / get / del                       │
│   - 内存 map 作为状态机（可换 BoltDB）     │
├──────────────────────────────────────────┤
│ 共识层（15.1.3 分布式集群）                │
│   - hashicorp/raft                        │
│   - 只有 Leader 调用 Apply                 │
│   - 读：强读（走日志/Read Index）/ 弱读    │
└──────────────────────────────────────────┘
```

### 15.2 代码骨架：读写路径

```
教学示意，不参与构建
func (s *Server) handleSet(req SetReq) Resp {
    if s.raft.State() != raft.Leader {
        return Resp{RedirectTo: s.leaderAddr()}   // 或转发给 Leader
    }
    cmd, _ := encode(Command{Op: "set", Key: req.Key, Value: req.Val})
    f := s.raft.Apply(cmd, 5*time.Second)         // 走共识
    if err := f.Error(); err != nil { return Resp{Err: err} }
    return Resp{OK: true}
}

func (s *Server) handleGet(req GetReq) Resp {
    switch s.readLevel {
    case StrongConsistent:
        // 走一次日志（最朴素、最安全，性能最差）
        f := s.raft.Apply(encode(Command{Op: "get", Key: req.Key}), timeout)
        return f.Response().(Resp)
        // 生产实现：Read Index（发一轮心跳确认自己是 Leader，再读本地 FSM）
    case Stale:
        return Resp{Value: s.fsm.store[req.Key]}  // 可能陈旧，但零 RTT
    }
}
```

### 15.3 从论文到系统还差什么

| 缺口 | 影响 | 建议 |
| --- | --- | --- |
| FSM 非确定性 | 副本静默发散 | `Apply` 只做纯内存计算；时间由 Leader 统一分配 |
| 快照与压缩 | 磁盘爆、重启慢 | 设阈值 + 定时快照 |
| 读路径没设计 | 读到陈旧值 | 明确强读（Read Index）/ 弱读两档 |
| 成员变更无编排 | 双 Leader | 一次只改一个，等提交后再改下一个 |
| 无混沌测试 | 上线才发现错 | 用故障注入/Jepsen 类方法验证 |

## 版本演进

- **2014**：Raft 论文发表（USENIX ATC 2014）+ Ongaro 的博士论文给出工程细节。
- **2014–2015**：CoreOS 的 etcd、HashiCorp 的 `hashicorp/raft` 库先后出现；`hashicorp/raft` 成为 **Go 生态事实标准 Raft 库**。
- **2016–2019**：Consul、InfluxDB Enterprise、Nomad 等采用 `hashicorp/raft`；
  国内出现 `sofastack/sofa-jraft`（Java）与 `baidu/braft`（C++）。
- **2022（本书）**：第 14、15 章给出**可直接照做的 Go 代码路径**——这是本书区别于其他中文分布式书的核心价值。
- **2026 视角**：
  - `hashicorp/raft` 仍被广泛使用，但**etcd 的 Raft 实现（`etcd-io/raft`）**因 K8s 生态而成为另一极；
  - **etcd lease（租约）**与**客户端分布式锁**的关系常被混淆：etcd 的 lease 是**服务端 TTL + 续租**，
    用它实现锁（配合 `revision` 与事务 `Txn`）在实践中可行；但它与 Redis 侧的 **Redlock** 是完全不同的机制族；
  - **服务发现的迁移潮**：新建系统多用 etcd / Consul / K8s 原生机制，
    K8s 甚至提供内置的 **coordination.k8s.io/Lease** 对象用于领导者选举——
    「自己写一个 Raft KV 系统」在 2026 年更多是**学习路径**而非生产首选；
  - 若真要自建，**Multi-Raft 分组**（TiKV 模式）才是能扩数据的形态，单组 Raft 只能做元信息存储。

## 经典论文与原始文献

| 论文/文献 | 出处 | 贡献 |
| --- | --- | --- |
| Ongaro & Ousterhout《In Search of an Understandable Consensus Algorithm》 | USENIX ATC 2014 | 本章的理论依据 |
| Ongaro《Consensus: Bridging Theory and Practice》 | PhD dissertation, Stanford 2014 | 论文未覆盖的**工程细节**（日志压缩、客户端会话），正是本章 14.1 的鸿沟 |
| Hunt et al.《ZooKeeper: Wait-free coordination for Internet-scale systems》 | USENIX ATC 2010 | 读/写请求处理的对照实现（本书第 6 章 6.4） |
| Gray & Cheriton《Leases: An Efficient Fault-Tolerant Mechanism for Distributed File Cache Consistency》 | SOSP 1989 | **租约**原始论文：etcd lease、Leader 租约、TTL 键的共同源头 |
| Chandra & Toueg《Unreliable Failure Detectors for Reliable Distributed Systems》 | JACM 1996 | 失败检测器；解释了为什么选举需要超时 |
| Lamport《Time, Clocks, and the Ordering of Events in a Distributed System》 | CACM 1978 | 逻辑时钟；Raft term 的思想背景 |

## 近年研究与工业界开源实践（2015–2026）

- **近年研究**：
  - **Raft 的形式化验证**：etcd 对成员变更给出 **TLA+ 规格**；多个团队用 Coq/Isabelle 验证安全性，
    印证「论文 20 页不足以覆盖实现」；
  - **Multi-Raft 分组**（TiKV/PD、CockroachDB）与 **Parallel Raft**（PolarFS, 2018）解决单组 Raft 的吞吐上限；
  - **租约读的时钟风险**被反复强调：VM 暂停、NTP 跳变会破坏基于时钟的 Lease Read，
    因此 etcd 默认 **Read Index**。
- **工业界开源**（star 数 2026-09 `gh api` 实测）：
  - `hashicorp/raft`（**9136★**）：本书第 14 章主角，Go 生态事实标准 Raft 库。
  - `etcd-io/etcd`（**52310★**）：Raft + **lease（租约）+ watch + revision**，K8s 元数据存储；
    其 `etcd-io/raft` 子项目是另一个主流 Raft 实现。
  - `sofastack/sofa-jraft`（**3824★**）：Java 生产级实现，含 Read Index/Lease Read、快照、成员变更。
  - `baidu/braft`（**4227★**）：C++ 实现；常与 `apache/brpc`（**17620★**）配合使用。
  - `tikv/tikv`（**16878★**）：Multi-Raft 分组 + PD 调度，是「Raft 如何支撑大规模数据」的样本。
  - `hashicorp/consul`（**30085★**）：`hashicorp/raft` 的最知名使用者之一（服务目录走 Raft）。
  - `kubernetes/kubernetes`（**128012★**）：内置 **Lease API**（`coordination.k8s.io/v1`）用于领导者选举，
    是 2026 年「不用自己写 Raft 也能选主」的现成方案。
  - `redisson/redisson`（**24403★**）：Redis 侧分布式锁实现（Redlock 相关），是本章锁议题的对照物。
- **Jepsen 实测**（`jepsen-io/jepsen`，**7504★**）：etcd、Consul 均有专项报告；
  结论一致——**共识层安全性良好，问题集中在读路径、会话语义与时钟假设**。
  自建 Raft KV 系统上线前应做同等强度的故障注入测试。

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「FSM 里可以自由写代码」 | 必须**确定性**：禁用本地时钟、随机数、无序 map 迭代、外部 IO |
| 2 | 「改配置文件就能加节点」 | 成员变更必须**走 Raft 日志**（`AddVoter`），否则会双 Leader |
| 3 | 「Raft 写成功就是线性一致读」 | 两回事。读必须显式选择强读（Read Index / 走日志）或弱读 |
| 4 | 「单组 Raft 可以存业务数据」 | 单组容量与吞吐都受单 Leader 限制；业务数据要 **Multi-Raft 分组** |
| 5 | 🔧 2026 补丁：Redlock 争议本书完全未涉及 | 2016 年 **antirez（Salvatore Sanfilippo）与 Martin Kleppmann** 就 Redis 分布式锁（Redlock）公开辩论：焦点是**时钟跳跃、GC 停顿与异步模型下的安全性**。2026 年共识：对正确性敏感的场景应使用**共识系统（etcd/ZooKeeper）的锁 + fencing token**，而非纯客户端 TTL 锁。本书第 15 章讲 KV 系统但没有讨论锁，读者需自行补这一课 |
| 6 | 🔧 2026 补丁：etcd 租约 ≠ 客户端锁 | etcd 的 **lease** 是服务端 TTL + 续租机制（源于 Gray & Cheriton 1989），用它配合 `Txn` 与 `revision` 可实现**服务端状态的锁**；而 Redlock 是**多个独立 Redis 实例上的客户端锁**。两者威胁模型不同：前者安全性来自共识，后者依赖时钟假设。etcd 官方明确建议用其 lease + 事务实现锁 |
| 7 | 🔧 2026 补丁：服务发现已迁向 etcd/Consul/K8s | 本书第 15 章「自研 Raft KV」在 2026 年更多是**学习路径**。生产上：元信息用 etcd，服务发现用 Consul 或 K8s Service，选主可直接用 **K8s Lease API**。自研只应在「有明确理由」时进行 |
| 8 | 🔧 2026 补丁：TTL/租约在云原生的落地本书未展开 | 云原生的 TTL 机制无处不在：etcd lease（键 TTL）、K8s Lease（选主）、对象存储生命周期规则、Consul 健康检查 TTL。共同点是**「过期即失效」的声明式假设 + 续租压力**。本章只讲了 Raft 代码，读者应把租约这一维度单独补齐 |

## 与其他章 / 其他书的联系

- **本目录内**：
  - 本章是 [03-Raft选举日志复制与成员变更](03-Raft选举日志复制与成员变更.md) 的**代码落地**，两章必须连读；
  - 本章的「CP 元信息存储」对应 [11-InfluxDB企业版一致性实现剖析](11-InfluxDB企业版一致性实现剖析.md) 13.2 的 META 节点；
  - 本章的读路径选择可用 [07-Quorum-NWR](07-Quorum-NWR.md) 的「档位化」思路理解；
  - 本章用到的成员变更安全性论证在 [02-Paxos与Multi-Paxos](02-Paxos与Multi-Paxos.md) 的「多数派相交」。
- **跨书**：
  - [../深入理解分布式共识算法/08-Raft工程实践与SOFAJRaft.md](../深入理解分布式共识算法/08-Raft工程实践与SOFAJRaft.md)——**同一主题的 Java 版本**：五种读方案、Parallel Raft、SOFAJRaft 源码，与本章 Go 版本并读最佳；
  - [../深入理解分布式共识算法/07-Raft.md](../深入理解分布式共识算法/07-Raft.md)——Raft 论文逐节重述；
  - [../深入理解分布式共识算法/05-Multi-Paxos与PhxPaxos工程实现.md](../深入理解分布式共识算法/05-Multi-Paxos与PhxPaxos工程实现.md)——另一条工程路线（C++ Paxos），可对照「Paxos 落地比 Raft 难在哪」；
  - [../深入理解分布式系统/07-Raft与拜占庭容错.md](../深入理解分布式系统/07-Raft与拜占庭容错.md)——Raft 与 BFT 并列；
  - [../软件架构设计/11-多副本一致性.md](../软件架构设计/11-多副本一致性.md)——判断「什么时候该自研、什么时候该用现成的」。
