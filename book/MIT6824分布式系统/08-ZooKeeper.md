# 第 08 讲 Zookeeper：用「wait-free 原语」做协调

> 官方标题：**Zookeeper**（LEC 8，主讲 fk）
> 指定必读：**ZooKeeper (2010)**
> 对应：**Lab 3: KV Raft**（本讲之后布置）

## 本章地图

前面几讲都在讲「怎么让一堆机器对一件事达成一致」；本讲问的是：
**达成一致之后，应用到底需要什么样的 API？**

ZooKeeper 的答案是：**不要给我锁服务，给我一组「不会阻塞的原语」**——
顺序节点（sequential znode）、临时节点（ephemeral znode）、一次性监听（watch）、版本号 CAS。
应用拿这些原语自己拼出锁、选主、成员管理、屏障。

主线：ZK 是什么（不是什么）→ 数据模型与 API → **保证（线性一致写 + FIFO 客户端序）** →
为什么叫 wait-free → 四个经典用法（锁 / 选主 / 配置 / 成员）→ 读的陈旧问题与 `sync` → 与 Raft KV 的对照。

## 核心精讲

### 8.1 ZK 是什么，不是什么

| 是 | 不是 |
| --- | --- |
| 协调服务（naming / configuration / group membership / leader election / locks / barriers） | 通用数据库（数据须容纳在内存，znode 有大小限制） |
| 一个「像文件系统」的**树形命名空间**（znode 树） | 文件系统（**不提供 rename** 等通用 FS 操作） |
| 提供**原语**，由应用拼出高级语义 | 提供「锁服务」「选主服务」这类成品 API |
| **写全部经 leader 广播**（Zab 原子广播，不是 Raft，但目标相同） | 强一致的读（默认读本地，可能陈旧，见 8.5） |

### 8.2 数据模型与关键 API

- **znode**：树节点，可存少量数据；
- **ephemeral（临时节点）**：与客户端**会话（session）**绑定，会话结束（超时/断开）自动删除；
- **sequential（顺序节点）**：创建时自动追加单调递增序号（`/lock/req-0000000003`）；
- **watch（监听）**：一次性（触发一次后失效，必须重新注册）；
- **version + CAS**：`setData`/`delete` 带版本号，版本不匹配则失败（乐观并发控制）；
- **sync**：让本服务器在下次读之前追上 leader 的最新状态。

### 8.3 ZK 的三条核心保证

1. **线性一致的写（Linearizable writes）**：所有更新请求经 leader 定序，等价于「串行执行且尊重因果先后」；
2. **FIFO 客户端序（FIFO client order）**：**同一个客户端**发出的请求，按发送顺序执行；
3. **（论文术语）A-linearizability**：论文把「线性一致写 + FIFO 客户端序」的组合称为
   **asynchronous linearizability（A-linearizability）**——
   即：写是线性一致的，而读允许读到稍旧的值，但每个客户端自己的操作序列看起来是自洽的。

> 记住这个组合的意义：**不强求读也线性一致**，就可以让读完全由本地副本服务（极快），
> 需要强读的客户端自己用 `sync` 升级。这是本讲最重要的设计取舍。

### 8.4 为什么强调 wait-free

Herlihy 的 wait-free 含义是「任何一个客户端都能在有限步内完成操作，不依赖其他客户端的进展」。
ZK 之所以要这样设计：**如果 API 会阻塞（例如「等锁」），那么一个慢/挂掉的客户端就会拖住别人**。

ZK 的做法是：提供**非阻塞的读 + 事件通知（watch）**，
「等锁」由客户端用 watch 自己实现——客户端挂了，只是它的临时节点消失，别人不受影响。

### 8.5 读的陈旧问题与 `sync`

- 默认：`getData` 由客户端连接的**那台服务器本地**处理 → **可能读到旧值**（不线性一致）；
- `sync()` + `getData()`：先让该服务器追上 leader（把读之前的写都应用完），再读 → 得到**不落后于 sync 时刻**的值；
- 这是「**读性能 vs 读新鲜度**」的显式开关，对应 [07-容错Raft二.md](07-容错Raft二.md) 的 ReadIndex：
  那边的 ReadIndex 是**默认强**，这边是**默认弱、按需加强**。

### 8.6 四个经典用法（本讲的精华）

**(a) 锁（用顺序临时节点，避免惊群）**

```
1. n = create("/lock/req-", EPHEMERAL|SEQUENTIAL)   // 得到 req-0000000007
2. children = getChildren("/lock", watch=false)
3. 若 n 是 children 里序号最小的 → 拿到锁
4. 否则 → exists(下一个更小的节点, watch=true)
   // 只监听「前驱」，而不是监听 /lock 的 children
5. 前驱被删除（持锁者挂了/释放）→ 收到事件 → 回到步骤 2 重新判定
```

> 关键：**只 watch 前驱**。若所有等待者都 watch `/lock` 的 children，
> 一次释放会唤醒所有人（**惊群 / herd effect**），而只有一个人能拿到锁，其余白醒。

**(b) 选主（leader election）**：与锁同构——抢到「序号最小」的临时节点者为主，其余 watch 前驱。
主挂掉 → 临时节点消失 → 下一个自动接上。

**(c) 配置/约定点（rendezvous）**：把配置写进一个 znode，worker 启动时读它并对它设 watch；
配置变更 → 所有 worker 收到通知 → 重新读。经典的「ready znode」模式：
主进程创建一个 `/ready` 节点表示「配置已就绪」，worker 只等这个节点出现。

**(d) 组成员管理**：每个成员创建 `/group/member-i`（临时节点），
监控者 `getChildren("/group", watch=true)` 就能拿到「当前活着谁」。
成员崩溃 → 会话超时 → 临时节点消失 → 监控者收到事件。

### 8.7 教学示意：把锁的判定写清楚

> **教学示意，不参与构建**——只表达判定顺序。

```go
// 教学示意，不参与构建
func tryLock(zk ZK, path string) (acquired bool, watchOn string) {
    mine := zk.Create(path+"/req-", Ephemeral|Sequential)
    siblings := zk.GetChildren(path) // 注意：这里没有 watch
    sortBySeq(siblings)

    if mine.seq == siblings[0].seq {
        return true, "" // 我最小 → 拿到锁
    }
    predecessor := siblingJustSmallerThan(siblings, mine.seq)

    // 双重检查：对前驱 exists 一次，若它已经没了，说明我该重新判定一次
    // （watch 是一次性的，且「注册 watch」与「读取状态」之间必须有明确的先后）
    if !zk.Exists(predecessor) {
        return tryLockAgain(zk, path, mine)
    }
    return false, predecessor // 监听前驱的删除事件
}
```

> 正确性依赖两条：**(1) 写是线性一致的**（序号分配不会重复/乱序）；
> **(2) FIFO 客户端序**（我「取 children」与「对前驱设 watch」的相对顺序对我自己是可控的）。
> 二者缺一，锁就可能发给两个人。

## 版本演进

- **2006**：Google **Chubby**（OSDI 2006）提出「用类文件系统的接口提供粗粒度锁服务」，
  ZK 的直接思想来源（**Chubby 不是 2020 课表的必读**，本讲只读 ZooKeeper 论文）。
- **2007–2010**：Yahoo! 研发 ZooKeeper，明确与 Chubby 拉开距离——
  不做锁服务，做 **wait-free 原语 + 顺序/临时节点 + watch**。
- **2010s**：ZK 成为 Hadoop/HBase/Kafka 生态的事实协调服务。
- **2013**：etcd 出现（用 **Raft** 而非 Zab），随 Kubernetes 成为云原生默认；
  新系统更多选 etcd，ZK 主要留在存量生态里。
- **2020（本讲）**：课程把 ZK 作为「**共识之上该给应用什么 API**」的范例，
  并与即将做的 Lab 3（KV Raft）对照：同样的共识层，API 设计不同，能力差别巨大。
- **2026**：ZK 的存量生态在收缩——Kafka 引入 **KRaft**（自带元数据 quorum）
  并在后续大版本中不再依赖 ZooKeeper（具体版本以官方发布说明为准）；
  新的协调需求多数直接用 etcd 或 Kubernetes 的 API server（它本身就是一个带 watch 的复制状态机）。

## 经典论文与原始文献

| 论文 | 出处 | 本讲为何读它 |
| --- | --- | --- |
| Hunt, Konar, Junqueira & Reed《ZooKeeper: Wait-free Coordination for Internet-scale Systems》 | **USENIX ATC 2010** | L8 **指定必读**（课程站点 `zookeeper.pdf`，另有 zookeeper-faq） |
| （对照，**非本讲指定**）Burrows《The Chubby lock service for loosely-coupled distributed systems》 | OSDI 2006 | ZK 的思想前身；不在 2020 reading list 上，作背景读 |
| （对照）Ongaro & Ousterhout《Raft》 | USENIX ATC 2014 | Zab 与 Raft 的目标相同（原子广播/复制日志），实现路径不同 |
| （对照）Herlihy《Wait-Free Synchronization》 | TOPLAS 1991 | 「wait-free」一词的出处 |

## 近年研究与工业界开源实践（2015–2026）

- **近年研究**：
  - **watch 语义的规范化**：一次性 watch 易漏事件，后续系统（etcd v3、K8s API）普遍改为
    「带 revision 的流式 watch」——客户端可指定从哪个版本开始监听，不会丢事件；
  - **租约（lease）替代临时节点**：etcd 用 TTL lease 表达「会话存活」，语义类似 ephemeral 但更通用；
  - **协调服务下沉到平台**：Kubernetes 把「配置、成员、选主」变成 API 对象（ConfigMap/Lease），
    协调功能不再需要独立的 ZK 集群。
- **工业界开源（star 数 2026-09-26 `gh api` 实测）**：
  - `apache/zookeeper`（**12811★**）：论文的实现本体，仍广泛用于 Hadoop / HBase / 老版本 Kafka 生态。
  - `etcd-io/etcd`（**52310★**）：Raft 版协调服务；Kubernetes 的元数据存储。
    与 ZK 的关键差异：**Raft 共识 + revision 化 watch + lease**，以及默认强一致读。
  - `apache/kafka`（**33848★**）：曾是 ZK 最大的使用者；引入 **KRaft**（自管理的元数据 Raft quorum）
    后逐步摆脱对 ZK 的依赖（具体版本以官方发布说明为准）——是本讲「协调服务被吸收进系统内部」的最佳样本。

## 常见误区与本课程需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「ZK 是锁服务」 | 它是**原语集合**；锁是应用用 ephemeral+sequential+watch 拼出来的 |
| 2 | 「ZK 的读是线性一致的」 | 默认读本地、**可能陈旧**；需要新鲜度要 `sync` |
| 3 | 「watch 会一直生效」 | watch 是**一次性**的，触发后必须重新注册；两次注册之间可能漏事件 |
| 4 | 「大家都 watch `/lock` 的 children 就行」 | 会惊群；正确做法是**只 watch 前驱** |
| 5 | 「临时节点在客户端断开时立刻消失」 | 与**会话超时**绑定，不是连接断开；会话由心跳维持，且会话可在服务器间迁移 |
| 6 | 🔧 2020 课程未覆盖 | **流式 watch 与 revision**：一次性 watch 的缺陷已被 etcd v3 / K8s 的「版本号 + 长连接流」解决；ZK 论文的模型是旧形态 |
| 7 | 🔧 2020 课程未覆盖 | **etcd 与 Raft 取代 Zab 成为新默认**：新系统多用 etcd；读论文时应把它当「API 设计范本」而非「选型答案」 |
| 8 | 🔧 2020 课程未覆盖 | **Kafka KRaft**：最大的 ZK 使用者已自带元数据 quorum，说明「协调服务」正在被吸收进各系统内部 |
| 9 | 🔧 2020 课程未覆盖 | **ZK 的 znode 数据必须放内存 + 单节点大小受限**：这决定了它不能当数据库用；2026 的「协调数据」常直接放进业务库或 K8s CRD |

## 与其他章 / 其他书的联系

- **本目录内**：
  - [07-容错Raft二.md](07-容错Raft二.md)——ReadIndex 与本讲的「默认陈旧读 + sync」是同一问题的两种默认策略；
  - [02-RPC与线程.md](02-RPC与线程.md)——ZK 的 session/序号去重是 `kv.go` 去重表在集群环境下的形态；
  - [09-CRAQ与链式复制.md](09-CRAQ与链式复制.md)——下一讲继续讨论「谁来服务读」；
  - [04-主从复制与VMwareFT.md](04-主从复制与VMwareFT.md)——ZK 的 leader 也是单点写，但**可以被替换**（有共识保障），而 FT 的主不能被误判。
- **跨书**：
  - [../深入理解分布式共识算法/06-ZAB与ZooKeeper.md](../深入理解分布式共识算法/06-ZAB与ZooKeeper.md)——Zab 协议与 ZK 的中文详解，与本讲互补；
  - [../设计数据密集型应用/09-一致性与共识.md](../设计数据密集型应用/09-一致性与共识.md)——「线性一致 + 顺序保证」的现代表述；
  - [../分布式系统/06-协调.md](../分布式系统/06-协调.md)——教材口径的分布式互斥、选举、组成员；
  - `book/ZooKeeper-分布式过程协同技术详解.md`、`book/ZooKeeper_Dubbo3分布式高性能RPC通信.md`（仓库单文件）——ZK 的使用层资料。

> **Lab 提示（思路，不给代码）**：Lab 3（KV Raft）看似是「Raft 上加 KV」，
> 真正的难点是**重复请求去重（session + 序号）**与**读的线性一致性**——
> 这两点恰好就是本讲 ZK 的 API 设计要解决的问题。先想清楚语义，再写代码。
> 本目录不提供、也不链接任何公开解答仓库。
