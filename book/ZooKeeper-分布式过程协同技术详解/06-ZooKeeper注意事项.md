# 第 6 章　ZooKeeper 注意事项

> 原书第 6 章是「踩坑集」：把前几章那些**看起来能用、实则危险**的写法集中点名。重点是
> 「伪同步（pseudo-sync）」「羊群效应（herd effect）」「锁配方的漏洞」「顺序保障的正确用法」
> 以及「隔离令牌（fencing token）」。这一章密度极高——很多 ZK 线上事故，根因都在这里。

## 本章地图

| 节 | 内容 | 结论 |
| --- | --- | --- |
| 伪同步（pseudo-sync） | 用 ZK 做「多进程同时开工」的互斥，却漏了「崩溃后仍持有锁」的窗口 | 锁不是「拿到了就永远安全」，要考虑持锁者崩溃 |
| 羊群效应（herd effect） | 一个节点变化触发大量客户端同时回读，瞬时风暴 | watch 要「只通知相关者」，避免一变全醒 |
| 锁配方与漏洞 | 朴素「抢建锁节点」有竞态；顺序临时节点的锁配方需正确处理「只 watch 前驱」 | 锁配方必须配合 fencing token 才完整 |
| 顺序保障的正确用法 | ZK 保证的是「更新顺序」，不保证「你读到的一定最新」 | 读场景要分清是否需要 `sync` / 强一致 |
| 隔离令牌（fencing） | 给每次「取得领导权」发一个单调递增令牌，旧主凭旧令牌写会被拒绝 | 光有锁不够，还要让存储侧能**拒绝旧主的写入** |
| 隐式约束与容量 | ZK 不适合大 payload、高频写；watch 数量爆炸会拖垮 server | 把 ZK 当协调元数据，别当通用存储 |

## 核心精讲

（以下为教学性梳理，伪代码/示意均**教学示意，不参与构建**。）

### 6.1 伪同步：最隐蔽的坑

场景：用「抢建 `/lock` 临时节点」来给一段代码加锁，但持锁者拿到锁后**崩溃**，ZK 在会话超时才删
节点——这段超时里，锁其实已经「名存实亡」，别的进程却还以为锁被持有。

```text
# 教学示意，不参与构建：伪同步的时间窗
T0: A 抢到 /lock(临时)
T1: A 开始写共享资源
T2: A 崩溃（不优雅）
T3..T3+sessionTimeout: /lock 仍在，B 抢不到 -> 但 A 已死，资源无人管
T4: 超时到达，/lock 被删，B 抢到 -> 但 A 若在 T3 后曾"短暂恢复"残留写入会污染资源
```

- 这说明：**单靠「锁存在」不能保证互斥**，因为「持锁者崩溃」到「锁释放」之间有可见性空窗；
- 解法见 6.5 的 fencing token：让存储侧能识别「这是旧主的过期写入」并拒绝。

### 6.2 羊群效应：一变全醒

错误写法：100 个客户端都 `getChildren("/tasks", watch=true)`，每当新增一个任务，100 个客户端
**同时被唤醒**去读 `/tasks`——99 个其实用不上。

```text
# 教学示意，不参与构建：羊群 vs 分工
错误:  100 个 client 都 watch 同一个 /tasks   -> 一变全醒 -> 风暴
正确:  只有 master watch /tasks；worker 只 watch 自己的 /assign/<me>
       (职责分离，谁关心谁才 watch)
```

- 更细的分工：锁场景里，**不要所有竞争者都 watch 锁节点**，而是「只 watch 序号比自己小一号的
  那个节点」（见 6.3），这样释放锁时只唤醒**下一个**等待者，而非所有人。

### 6.3 锁配方：顺序临时节点的正确姿势

```text
# 教学示意，不参与构建：公平锁（只 watch 前驱）
每个竞争者: create("/lock/req-", EPHEMERAL_SEQUENTIAL) -> 得到 /lock/req-00000003
            children = getChildren("/lock", false)
            if 我是最小序号: 获得锁
            else: watch("/lock/req-<比我小一号的那个>")
收到前驱删除事件 -> 重新判断自己是否最小 -> 是则获得锁
```

- 关键：**watch 前驱而非父节点**，释放锁时只唤醒真正的下一位，避免羊群；
- 漏洞：即便如此，6.1 的「持锁者崩溃 + 旧写入」问题仍在，必须加 fencing。

### 6.4 顺序保障的边界

- ZK 保证：**同一客户端的更新按序生效（FIFO 客户端序）**，且**所有写经 leader 获得全局 zxid 全序**；
- 但它**不保证**「你 `getData` 读到的一定是最新值」——读 follower 有「时效界（timeliness）」，
  不是严格实时线性一致；
- 需要强一致读时，要么读 leader，要么先 `sync(path)` 再读（把本地与 leader 对齐）。

### 6.5 隔离令牌（fencing token）：锁的完整拼图

```text
# 教学示意，不参与构建：fencing 让旧主写入失效
每次选出新主: fencing = 单调递增计数器 (由 ZK 顺序节点 / 外部单调源给出)
主写入资源时附带 fencing 值
存储侧规则: 只接受 fencing 值 > 已见过最大值的写入
-> 旧主若带着更小的 fencing 残留写入，被直接拒绝
```

- 光有锁，解决「谁在做」；加 fencing，解决「旧主的过期写入能否污染资源」；
- 这是把「伪同步」漏洞补上的关键一环，原书明确强调。

## 版本演进

- **本书无第二版**；本节写 2013 年口径 → 2026 年视角的变化。
- **Curator 的 `InterProcessMutex` / `LeaderLatch` 已内置正确锁配方 + 重试**，但**默认不含
  fencing token**——2026 年若用 ZK 锁保护共享存储，仍需自己在写入侧加单调令牌（或用支持 fencing
  的存储）。读第 6 章理解「为什么 Curator 还不够」非常关键（第 8 章会点出）。
- **etcd 的 `lease + compare-and-swap` 天然提供 fencing 思路**（每次续约 lease 有唯一 ID），
  在「领导权互斥」场景比 ZK 锁 + 手工 fencing 更内聚。
- **现代共识库（如用 Raft `leader lease`）把 fencing 内建进协议**，而不是留给应用层补——这是
  2026 年「为什么新系统选 Raft 系」的隐性理由之一。

## 经典论文与原始文献

| 文献 | 出处 | 贡献 |
| --- | --- | --- |
| Hunt et al.《ZooKeeper: Wait-free Coordination for Internet-scale Systems》 | USENIX ATC 2010 | **recipes（锁/屏障/队列）与 caveats 的原始出处** |
| Burrows《The Chubby lock service》 | OSDI 2006 | Chubby 早已强调「锁 + 租约 + 顺序令牌」的 fencing 思路，ZK 同谱系 |
| Lamport《Time, Clocks, and the Ordering of Events》 | CACM 1978 | 全序与「谁先谁后」的形式化，6.4/6.5 的理论底 |

## 近年研究与工业界开源实践（2015–2026）

- **Curator 配方库**：`apache/curator`（3173★）提供 `InterProcessMutex`、`LeaderLatch`、
  `DistributedBarrier` 等，把 6.3 的正确锁配方封装好；但**fencing 仍需应用自己加**（见版本演进）。
- **etcd `lease` + `txn`**：`etcd-io/etcd`（52309★）的租约唯一 ID 可作为天然 fencing token，
  在领导权互斥场景比「ZK 锁 + 手写令牌」更内聚。
- **Kubernetes 用 Lease 选主 + endpoint`leader-election` 注解**：基于 etcd lease 实现 master 选举，
  是「fencing 内建于协议」的大规模工业实践，对照第 6 章「锁的完整性」。
- **Jepsen 测试揭示的协调漏洞**：多个系统在故障注入下暴露「锁未防住旧主写入」类问题，
  与 6.1/6.5 的警示互证（本书时代尚无此工程视角）。

## 常见误区与本书需修正之处

| # | 误区 | 修正 |
| --- | --- | --- |
| 1 | 「抢到 ZK 锁就绝对互斥」 | 持锁者崩溃到会话超时之间锁名存实亡，需 fencing token 兜底（6.1/6.5） |
| 2 | 「所有竞争者 watch 同一个锁节点」 | 会羊群效应；应只 watch 自己的前驱节点（6.3） |
| 3 | 「ZK 读一定是最新值」 | 读 follower 有时效界，强一致需 `sync` 或读 leader（6.4） |
| 4 | 「锁配方 = 完整互斥方案」 | 缺 fencing，仍可能旧主残留写入污染资源（6.5） |
| 5 | 「watch 越多越实时」 | watch 爆炸会拖垮 server，要按职责最小注册（6.2） |
| 6 | 「ZK 能当通用存储放大对象」 | 协调元数据定位，大 payload / 高频写是反模式（6.6） |
| 7 | 🔧 第 6 章未提示 Curator 锁不含 fencing | 2026 年直接用 `InterProcessMutex` 仍要自己加 fencing，需点明 |
| 8 | 🔧 未对比 etcd lease 内建 fencing | Raft 系把 fencing 内聚进协议，是选型的隐性优势 |
| 9 | 🔧 未提 Jepsen 式故障验证 | 锁/选举的正确性今天要经故障注入测试证伪，工程视角需补 |

## 与其他章 / 其他书的联系

- **本书内**：
  - 第 6 章的 **锁配方/前驱 watch** → 第 4 章 watch 机制的正确高级用法；
  - 第 6 章的 **fencing** → 第 5 章故障恢复「旧状态残留」问题的根治；
  - 第 6 章的 **顺序保障边界** → 第 2 章 guarantees 与第 9 章 Zab 全序；
  - 第 6 章的 **配方** → 第 8 章 Curator 把这些配方产品化（含其局限）。
- [../深入理解分布式共识算法/00-总览与阅读地图.md](../深入理解分布式共识算法/00-总览与阅读地图.md)
  ——leader lease、Raft 的 fencing 内建机制，与 6.5 的应用层 fencing 对照。
- [../设计数据密集型应用/09-一致性与共识.md](../设计数据密集型应用/09-一致性与共识.md)
  ——「线性一致、 fencing 令牌、领导者租约」的现代讲法，与 6.4/6.5 精确对读。
- [../凤凰架构/](../凤凰架构/) ——云原生 leader-election（K8s Lease）与本章锁/选举的 2026 年实践。
