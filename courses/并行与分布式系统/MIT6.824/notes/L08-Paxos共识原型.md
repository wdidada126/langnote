# L08 Paxos：共识的原型与难点

> 阅读：Lamport, *Paxos Made Simple* (2001)；节选 *The Part-Time Parliament* (1998)
> 主线：先有 Paxos 证明"共识可解"，Raft（L05/L06）是它的可理解化重写。

## 1. 核心问题

- 共识不可能无代价：FLP 定理（1985）证明——**异步系统里即使只有一个进程可能崩溃，
  也没有确定性共识算法能保证终止**。工程对策：靠随机超时（Raft）、
  部分同步假设（Paxos/Lamport）、leader 化来"绕开"FLOP 前提。
- Single-decree consensus：一组提案值，进程对"哪个值胜出"达成一致，
  满足安全性（只一个值胜出、胜出的必是被提出过的）+ 活性。

## 2. 两阶段算法（Prepare / Accept）

角色逻辑上分 Proposer / Acceptor / Learner（实践中同一进程全包）。
- **阶段 1 Prepare(n)**：向多数派问"你是否承诺不再接受编号 < n 的提案？
  并交出你已接受过的最大编号值"。任一 Acceptor 首次可随意承诺；
  一旦承诺 n，就拒绝了所有 < n 的 prepare/accept。
- **阶段 2 Accept(n, v)**：Proposer 收集多数派回应，
  **若其中有已接受值，必须选编号最大的那个 v（不能改！）**，否则自由选。
- 多数派接受 → 该值被选定（chosen）。

### 为什么这样对
- 两个多数派必相交；相交节点"承诺不回退 + 交出已接受最大编号"
  → 任何新提案只能继承已被多数派接受的旧值 → **一旦被选定，不可被推翻**。
- 与 Raft 对照：Prepare≈选举限制/term，Accept≈日志复制；
  n 即 term，"交出已接受值"即"新 leader 须包含已提交日志"。

## 3. Multi-Paxos 与实际困难

- 每命令跑一遍两阶段 = 每条 2 RTT + 无定序 → 工程上：
  **稳定 leader + 连续槽位（slot）批量提案**，跳过 prepare（等价 Raft 的常态）。
- Lamport 自承"Paxos Made Simple 其实不好懂"：论文里充满
  "how to build a system" 的空白（活锁、无 leader、日志压缩、成员变更都留给读者）。
  这正是 Raft 出现的动机：**把 Multi-Paxos 已经形成的工程惯例显式化、可讲解化**。

## 4. 论文间脉络

- L05/L06 已建立 Raft 直觉，本讲回补"为什么共识长这样"的理论根基。
- L15 Spanner 用 **Paxos**（非 Raft）做全局提交与分片复制 → 读懂本讲才能读 Spanner。
- L12 ZooKeeper 的 ZAB、L06 成员变更，都是 Paxos/Raft 谱系的具体方言。
- 主线：Paxos 证明"多数派 + 承诺不回退"是安全性的通用配方，
  后面所有系统（Raft/ZAB/PBFT）换的是"活性怎么给、工程怎么做"。

## 5. 跨课程联系

- **6.S081/CS162**：Paxos 两阶段 ↔ 数据库两阶段提交（L14 2PC）结构神似但
  语义不同：2PC 有协调者单点阻塞，Paxos 无；对比是理解"共识 vs 原子提交"的关键。
- **15-445**：可串行化的"提交顺序唯一"↔ Paxos 对 slot 序列的唯一决定。
- **CS149**：barrier/gather-scatter 的两轮同步模式，是并行版的两阶段。
- **数学（6.042 类）**：多数派相交 = 鸽巢原理的直接应用，安全性证明本质是组合论证。

## 6. 开源项目中的应用

- **Google Chubby / Spanner / Megastore**：Paxos 的原生阵地。
- **CockroachDB**：早期 Raft（`raft` 库源自 etcd），Raft 即 Multi-Paxos 的工程化代表。
- **Redis Cluster（异步复制 + 故障转移用类 Paxos 投票）**、**Aurora**（存储层用 quorum 协议）。
- **Apache ZooKeeper/JGroups/Java `jgroups-raft`**：多种共识实现。
- **区块链共识**（L24）：PoW/PoS 本质是"用算力/权益替代多数派假设"的 Paxos 变体思路。

## 7. 延伸阅读

- Lamport, *Paxos Made Live* (2004)——Google 实现 Chubby 时踩的坑，最好的"理论到实践"反思。
- TLA+ 规范 Paxos（Lamport 用它找出论文 bug，对接 L22 IronFleet 的形式化传统）。
- *There Is More Consensus in Egalitarian Parliaments*（Irene 论文）——去 leader 的方向。
- 对照阅读：本目录 notes/L05、L06 把同一配方以 Raft 语言重述了一遍。
