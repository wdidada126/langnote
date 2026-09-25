# L23 结构化 P2P：Chord 与 CAN（DHT）

> 阅读：Stoica et al., *Chord: A Scalable Peer-to-peer Lookup Service for Internet Applications*, SIGCOMM 2001；
> 辅读：Ratnasamy et al., *A Scalable Content-Addressable Network (CAN)*, SIGCOMM 2001
> 主线：无中心、海量动态节点下如何 O(log N) 定位数据——去中心化"路由表"问题。

## 1. 核心问题

- 场景：N 台对等节点（随时加入/退出/宕机），要把 key 映射到持有它的节点：
  `lookup(key) -> node`。集中式索引（GFS master、Dynamo 协调者）违背 P2P 初衷且是单点。
- DHT（分布式哈希表）的答案：**把 key 空间哈希打散到全网，
  每节点只需维护 O(log N) 邻居即可路由**——"去中心化的哈希表"。
- 两大代表设计（同一问题两种几何）：Chord（环形 + 指针表）、CAN（d 维坐标系）。

## 2. Chord

- **一致性哈希环**：节点与 key 都哈希到 [0, 2^m) 环上；key 由其**顺时针第一个节点**
  （successor）负责（与 L11 Dynamo 的哈希环同源，但 Chord 解决"环上如何找后继"）。
- 朴素查找 O(N) → **finger table**：每节点存 2^i 距离处的后继，
  **每跳距离减半 → O(log N) 跳、表大小 O(log N)**（二分查找的分布式化）。
- 动态维护：join 时初始化前驱/后继/finger，**周期 stabilize**（向后继问 successor）
  修补链表——**最终一致的路由状态**，短暂窗口内可能查不到（Chord 论文给出
  "高概率正确"的界，而非绝对正确：**P2P 世界连一致性预算都要省**）。
- 节点 ID 与 key ID 解耦 → 负载天然均衡（哈希假设）。

## 3. CAN

- 把 key 空间映射成 **d 维笛卡尔坐标环面**，节点各占一块区域；
  每节点维护 2d 个邻居，路由 = 贪心走向目标坐标 → **O(N^(1/d)) 跳**；
  取 d ≈ log N → O(log N)，与 Chord 同阶。
- 特性差异：CAN 的**区域大小随节点数变化，容量不均**；
  Chord 的 successor 链表天然支持**区间查询**（遍历后继即可）→
  后来系统（Dynamo/TiKV range）都偏爱可范围扫的设计。

## 4. 设计谱系与工程现实

| 系统 | 结构 | 备注 |
|---|---|---|
| Chord/CAN/Kademlia | 环/坐标/异或距离 | 学术原型（Kademlia：BT/IPFS 用） |
| Dynamo/Cassandra | 环 + 中心协调者半 P2P | 节点内强管理（L11） |
| BitTorrent DHT/IPFS | Kademlia 变体 | 真实互联网环境：NAT/拜占庭 |
| TiKV/CockroachDB 调度 | range + 中心 PD/半去中心 | "管理良好的集群"不用 DHT |

- 经验教训：**企业集群里 DHT 几乎绝迹**（节点数 < 10³ 时中心路由完全够，
  且成员可信）；DHT 的主战场是公网 P2P——
  节点数无上限、成员不可信、churn 剧烈。
- 但**一致性哈希**作为其"遗产"活在所有分片系统里（L11/L04 slice/L13 Ark 分区）。

## 5. 论文间脉络

- 与 L11：Dynamo 拿走了 Chord 的环，扔掉了对等性（协调者还在）——
  "P2P 理想 vs 运维现实"的妥协样本。
- 与 L08/L24：Chord 假设成员诚实且只崩溃；公网环境需要抗拜占庭
  → 引出下讲 PBFT/比特币。
- 与 L12：中心协调派（ZK/Chubby）与去中心派（DHT）是"协调的两种拓扑"，
  一致性/可用性权衡在两派里都存在。

## 6. 跨课程联系

- **自顶向下网络**：DHT 是"应用层路由"——finger 表 vs BGP 表、
  迭代/递归查询 vs DNS 的同一结构；O(log N) 跳 × 互联网 RTT 的真实代价。
- **数据结构与算法（6.006/6.046）**：finger table = 分布式二分/skip list
  （Chord 与跳表等价）；CAN = kd 树的空间划分。
- **CS149**：贪心路由 = 规则映射（regular communication pattern）的近邻通信。
- **15-445**：区间查询支持与否决定系统适用面（哈希 vs B 树之争的 P2P 版）。

## 7. 开源项目中的应用

- **以太坊/Bitcoin 节点发现**：Kademlia（s-kademlia）用于对等发现与 gossip。
- **IPFS/Libp2p（Kademlia DHT）、Mainline DHT（BT 种子）、Tor（目录系统为混合派）**。
- **Cassandra/DynamoDB/Aerospike cluster**：一致性哈希环直接后代；
  gossip 协议（phi accrual 探测 + 状态广播）解决成员管理（Chord 的 stabilize 工业化）。
- **Akka Cluster（一致性哈希分片）、Swarm/Orbit 虚拟 actor**：把 DHT 思想用于
  有状态微服务定位——"虚拟节点 = 可迁移 actor"。

## 8. 延伸阅读

- Kademlia 论文（2002）——工程影响最大的 DHT（BT/IPFS/以太坊都靠它）。
- SOSP 2001 "DHT 三连发"：Chord/CAN/Pastry 对照读，体会"同一下界三种几何"。
- *The Golden Age of DHTs*（2021 系列博客）与 IPFS/Coral 的失败复盘——
  为什么"去中心化存储"商业上艰难（对接 L24 激励问题）。
- MIT 6.852（Distributed Algorithms, Karger）中 DHT 与自稳定系统的分析章节（理论补强）。
