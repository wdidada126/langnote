# L12 ZooKeeper：协调服务与 ZAB

> 阅读：Hunt, Konagai, Lepreau, *ZooKeeper: Wait-free Coordination for Internet-scale Systems*, USENIX ATC 2010
> 主线：把共识"产品化"为一个可被千万应用复用的协调原语库（对接 L05/L08）。

## 1. 核心问题

- 分布式应用的共同需求不是"通用 KV"，而是**协调小数据**：
  leader 选举、成员管理、配置、锁、屏障（barrier）、队列。
  每个应用各写一套容错协调既易错又浪费——**ZooKeeper 把它抽成共享服务**。
- 设计目标：
  1. **有序**：FIFO 客户端顺序 + 全局总顺序（total order）；
  2. **原子**：要么所有 client 看到变更要么都看不到；
  3. **单一系统镜像**：client 连到哪个 server 看到的逻辑状态都一样；
  4. **可靠性**：一旦应用就持久到被覆盖；
  5. **实时性**：请求延迟有界（读可容忍轻微过期）。
- 数据模型：分层命名空间的**小 znode 文件树**（每个 ≤1MB），
  全量装内存、写持久化到本地磁盘——"内存树 + 磁盘日志"是 RSM 的典型形态（对照 L05）。

## 2. ZAB：原子广播协议

- ZAB（ZooKeeper Atomic Broadcast）= **为 ZooKeeper 定制的共识**，
  与 Raft/Paxos 同族：leader 定序 + 多数派确认 + epoch（zxid 高 32 位）fencing。
- 两个阶段：
  - **崩溃恢复（leader election + 日志同步）**：选出"zxid 最大"（即日志最新）者为 leader，
    先把 follower 日志拉齐 → 安全性类比 Raft 的选举限制（L05）。
  - **消息广播**：leader 用单调 zxid 给请求定序，Proposal → 多数派 ACK → Commit。
- **zxid = <epoch, counter>**：epoch 每次新选举 +1（term），counter 事务序号
  （commit index）——三个概念一以贯之：Raft term / Paxos ballot / ZAB epoch。
- ZAB 的正确性核心是 **primary order ≡ proposal order ≡ commit order ≡ replay/apply order**
  的链条证明，比 Raft 更强调"历史重放可恢复"。

## 3. 客户端语义：会话、watch、顺序一致性≠线性一致

- **Session + ephemeral znode**：client 心跳维持会话；会话超时 →
  它创建的 ephemeral 节点自动删除 → **锁/leader 租约天然实现**（对接 L09 超时思想）。
- **Watch**：注册一次性通知；**通知不保证"此刻值"，只保证"至少看到过那一步"**
  → 读到的可能是稍旧值 → **ZK 承诺顺序一致，不承诺线性一致读**（L10 重点）。
- **版本 + CAS**：znode 带 `cversion/version`，`setData(..., version)` 实现
  乐观并发控制（OCC，对接 L22）→ 锁/队列都可用 create/ephemeral/sequence 组合出。
- 经典分布式锁配方：`create` 顺序临时节点 → 找最小者持锁 → watch 前驱 → 
  挂了就重选。**"herd effect"用 watch 前驱而非全体规避**。

## 4. 论文间脉络

- L05/L08 的共识 → L12 把共识封进黑盒对外只暴露协调 API；
  Chubby（Bigtable L04 用的锁）是它的闭源表亲。
- 对照 L11：Dynamo 用去中心 quorum 换 AP，ZooKeeper 用中心 leader + 共识换 CP。
- L14/L15：数据库/全局事务的协调者也常落到 ZK/K8s 这类共识存储上。
- 应用总纲：**"外包共识"模式**——业务系统不自研 Raft，而依赖 ZK/etcd
  （对照 Bigtable 外包给 Chubby，L04）。

## 5. 跨课程联系

- **6.S081**：ephemeral 节点 + 心跳 = 租约（lease），与内核里的文件锁/进程生命周期同构。
- **15-445**：znode 版本 CAS ↔ 乐观锁；leader 选举 ↔ 数据库主从选主。
- **CS149/自顶向下**：watch/通知模型 ↔ 事件驱动并行、异步 RPC（对照 L01 同步 RPC 取舍）。
- **CS242/PL**：ZK 的规范（Replay/Recover 状态机）是"以状态机 + 日志定义系统行为"的范本。

## 6. 开源项目中的应用

- **Kafka**：旧版 broker/controller 注册、topic 配置、ISR 变更全存 ZK
  → **KRaft（2023–2024 GA）用内置 Raft 干掉 ZK**：本讲与 L05 的正面对照
  （"外部通用共识 vs 领域定制共识"，Kafka 选后者换运维简单）。
- **HBase**：master 选举、region server 成员、表元数据托管给 ZK（L04 血统）。
- **etcd**：ZooKeeper 的"云原生精神续作"——Raft + HTTP/2 + gRPC watch，
  K8s 的唯一状态后端（L05/L10 应用）。
- **Solr/Elasticsearch（早期）、Dubbo/Zookeeper 服务注册、YARN/Tez**：协调即 ZK。

## 7. 延伸阅读

- Fournier, *ZooKeeper: Distributed System Coordination Made Simple and Fast*（IEEE Computer 2014）——作者团队自述设计动机。
- Castro & Liskov, *Zab: Some Technical Remarks* + Hermes 论文——ZAB 与共识的关系。
- Curator Recipes（Java）：分布式锁/信号量/屏障的标准实现，对照亲手写一遍。
- 本目录 notes/L05、L08、L10 与本讲互参；projects/p3 用内置 Raft 复刻 etcd 式核心。
